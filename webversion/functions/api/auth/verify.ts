// JWT 验证端点
// 验证 token 并返回用户信息

interface Env {
    JWT_SECRET: string;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    smartbank_db: any;
}

// 简单的 JWT 验证实现
function base64UrlDecode(str: string): string {
    str = str.replace(/-/g, '+').replace(/_/g, '/');
    while (str.length % 4) str += '=';
    return atob(str);
}

async function verifyJWT(token: string, secret: string): Promise<Record<string, unknown> | null> {
    try {
        const parts = token.split('.');
        if (parts.length !== 3) return null;

        const [headerB64, payloadB64, signatureB64] = parts;
        const message = `${headerB64}.${payloadB64}`;

        // 验证签名
        const key = await crypto.subtle.importKey(
            'raw',
            new TextEncoder().encode(secret),
            { name: 'HMAC', hash: 'SHA-256' },
            false,
            ['verify']
        );

        const signature = Uint8Array.from(base64UrlDecode(signatureB64), c => c.charCodeAt(0));
        const isValid = await crypto.subtle.verify(
            'HMAC',
            key,
            signature,
            new TextEncoder().encode(message)
        );

        if (!isValid) return null;

        // 解析 payload
        const payload = JSON.parse(base64UrlDecode(payloadB64));

        // 检查过期时间
        if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) {
            return null;
        }

        return payload;
    } catch {
        return null;
    }
}

export async function onRequestGet(context: { request: Request; env: Env }) {
    const { request, env } = context;

    const authHeader = request.headers.get('Authorization');
    if (!authHeader?.startsWith('Bearer ')) {
        return new Response(JSON.stringify({ error: '未提供 token' }), {
            status: 401,
            headers: { 'Content-Type': 'application/json' },
        });
    }

    const token = authHeader.substring(7);
    const payload = await verifyJWT(token, env.JWT_SECRET);

    if (!payload) {
        return new Response(JSON.stringify({ error: 'token 无效或已过期' }), {
            status: 401,
            headers: { 'Content-Type': 'application/json' },
        });
    }

    // 从数据库获取最新的用户信息
    const user = await env.smartbank_db.prepare(
        'SELECT id, username, avatar_url, email, role, credits, daily_used FROM users WHERE id = ?'
    ).bind(payload.sub).first();

    if (!user) {
        return new Response(JSON.stringify({ error: '用户不存在' }), {
            status: 404,
            headers: { 'Content-Type': 'application/json' },
        });
    }

    return new Response(JSON.stringify({
        user: {
            id: user.id,
            username: user.username,
            avatar_url: user.avatar_url,
            email: user.email,
            role: user.role,
            credits: user.credits,
            daily_used: user.daily_used,
        },
        token_payload: payload,
    }), {
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
    });
}

// 对话历史 API
// GET /api/history - 获取对话列表
// POST /api/history - 保存对话
// DELETE /api/history?id=xxx - 删除对话

interface Env {
    JWT_SECRET: string;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    smartbank_db: any;
}

// JWT 验证函数
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

        const key = await crypto.subtle.importKey(
            'raw',
            new TextEncoder().encode(secret),
            { name: 'HMAC', hash: 'SHA-256' },
            false,
            ['verify']
        );

        const signature = Uint8Array.from(base64UrlDecode(signatureB64), c => c.charCodeAt(0));
        const isValid = await crypto.subtle.verify('HMAC', key, signature, new TextEncoder().encode(message));

        if (!isValid) return null;

        const payload = JSON.parse(base64UrlDecode(payloadB64));
        if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) return null;

        return payload;
    } catch {
        return null;
    }
}

// 从请求中获取用户 ID
async function getUserId(request: Request, secret: string): Promise<string | null> {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader?.startsWith('Bearer ')) return null;

    const token = authHeader.substring(7);
    const payload = await verifyJWT(token, secret);
    return payload?.sub as string || null;
}

// CORS headers
const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export async function onRequestGet(context: { request: Request; env: Env }) {
    const { request, env } = context;

    const userId = await getUserId(request, env.JWT_SECRET);
    if (!userId) {
        return new Response(JSON.stringify({ error: '未登录' }), {
            status: 401,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }

    try {
        // 获取用户的对话列表
        const histories = await env.smartbank_db.prepare(
            'SELECT id, title, mode, created_at, updated_at FROM chat_history WHERE user_id = ? ORDER BY updated_at DESC LIMIT 50'
        ).bind(userId).all();

        return new Response(JSON.stringify({ histories: histories.results }), {
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    } catch (err) {
        return new Response(JSON.stringify({ error: err instanceof Error ? err.message : '获取失败' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }
}

export async function onRequestPost(context: { request: Request; env: Env }) {
    const { request, env } = context;

    const userId = await getUserId(request, env.JWT_SECRET);
    if (!userId) {
        return new Response(JSON.stringify({ error: '未登录' }), {
            status: 401,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }

    try {
        const body = await request.json() as {
            id?: number;
            title?: string;
            mode: string;
            messages: unknown[];
        };

        const messagesJson = JSON.stringify(body.messages);
        const title = body.title || '新对话';

        if (body.id) {
            // 更新现有对话
            await env.smartbank_db.prepare(
                'UPDATE chat_history SET title = ?, mode = ?, messages = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?'
            ).bind(title, body.mode, messagesJson, body.id, userId).run();

            return new Response(JSON.stringify({ id: body.id, success: true }), {
                headers: { 'Content-Type': 'application/json', ...corsHeaders },
            });
        } else {
            // 创建新对话
            const result = await env.smartbank_db.prepare(
                'INSERT INTO chat_history (user_id, title, mode, messages) VALUES (?, ?, ?, ?)'
            ).bind(userId, title, body.mode, messagesJson).run();

            return new Response(JSON.stringify({ id: result.meta?.last_row_id, success: true }), {
                headers: { 'Content-Type': 'application/json', ...corsHeaders },
            });
        }
    } catch (err) {
        return new Response(JSON.stringify({ error: err instanceof Error ? err.message : '保存失败' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }
}

export async function onRequestDelete(context: { request: Request; env: Env }) {
    const { request, env } = context;

    const userId = await getUserId(request, env.JWT_SECRET);
    if (!userId) {
        return new Response(JSON.stringify({ error: '未登录' }), {
            status: 401,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }

    const url = new URL(request.url);
    const id = url.searchParams.get('id');

    if (!id) {
        return new Response(JSON.stringify({ error: '缺少 id 参数' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }

    try {
        await env.smartbank_db.prepare(
            'DELETE FROM chat_history WHERE id = ? AND user_id = ?'
        ).bind(id, userId).run();

        return new Response(JSON.stringify({ success: true }), {
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    } catch (err) {
        return new Response(JSON.stringify({ error: err instanceof Error ? err.message : '删除失败' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }
}

export async function onRequestOptions() {
    return new Response(null, { headers: corsHeaders });
}

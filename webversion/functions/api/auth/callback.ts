// GitHub OAuth 回调端点
// 处理 GitHub 返回的授权码，获取用户信息，生成 JWT

interface Env {
    GITHUB_CLIENT_ID: string;
    GITHUB_CLIENT_SECRET: string;
    JWT_SECRET: string;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    smartbank_db: any; // D1Database
}

interface GitHubUser {
    id: number;
    login: string;
    avatar_url: string;
    email: string | null;
}

// 简单的 JWT 实现（生产环境建议使用标准库）
function base64UrlEncode(data: string): string {
    return btoa(data).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

async function createJWT(payload: Record<string, unknown>, secret: string): Promise<string> {
    const header = { alg: 'HS256', typ: 'JWT' };
    const now = Math.floor(Date.now() / 1000);
    const tokenPayload = { ...payload, iat: now, exp: now + 7 * 24 * 3600 }; // 7天过期

    const headerB64 = base64UrlEncode(JSON.stringify(header));
    const payloadB64 = base64UrlEncode(JSON.stringify(tokenPayload));
    const message = `${headerB64}.${payloadB64}`;

    // 使用 Web Crypto API 签名
    const key = await crypto.subtle.importKey(
        'raw',
        new TextEncoder().encode(secret),
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign']
    );
    const signature = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(message));
    const signatureB64 = base64UrlEncode(String.fromCharCode(...new Uint8Array(signature)));

    return `${message}.${signatureB64}`;
}

export async function onRequestGet(context: { request: Request; env: Env }) {
    const { request, env } = context;

    const url = new URL(request.url);
    const code = url.searchParams.get('code');

    if (!code) {
        return new Response('Missing code parameter', { status: 400 });
    }

    try {
        // 用授权码换取 access token
        const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                client_id: env.GITHUB_CLIENT_ID,
                client_secret: env.GITHUB_CLIENT_SECRET,
                code,
            }),
        });

        const tokenData = await tokenResponse.json() as { access_token?: string; error?: string };

        if (!tokenData.access_token) {
            return new Response(`GitHub OAuth error: ${tokenData.error}`, { status: 400 });
        }

        // 获取用户信息
        const userResponse = await fetch('https://api.github.com/user', {
            headers: {
                'Authorization': `Bearer ${tokenData.access_token}`,
                'User-Agent': 'SmartBank-Agent',
            },
        });

        const githubUser = await userResponse.json() as GitHubUser;

        // 存储或更新用户到 D1
        await env.smartbank_db.prepare(`
            INSERT INTO users (id, username, avatar_url, email, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                username = excluded.username,
                avatar_url = excluded.avatar_url,
                email = COALESCE(excluded.email, users.email),
                updated_at = CURRENT_TIMESTAMP
        `).bind(
            String(githubUser.id),
            githubUser.login,
            githubUser.avatar_url,
            githubUser.email
        ).run();

        // 生成 JWT
        const jwt = await createJWT({
            sub: String(githubUser.id),
            username: githubUser.login,
            avatar: githubUser.avatar_url,
        }, env.JWT_SECRET);

        // 返回 HTML，通过 postMessage 将 token 发送给父窗口
        const html = `
<!DOCTYPE html>
<html>
<head><title>登录成功</title></head>
<body>
<script>
    // 将 token 发送给打开此窗口的父页面
    if (window.opener) {
        window.opener.postMessage({ type: 'github-oauth', token: '${jwt}' }, '*');
        window.close();
    } else {
        // 如果不是弹窗，重定向回主页
        localStorage.setItem('smartbank-token', '${jwt}');
        window.location.href = '/';
    }
</script>
<p>登录成功，正在关闭窗口...</p>
</body>
</html>`;

        return new Response(html, {
            headers: { 'Content-Type': 'text/html; charset=utf-8' },
        });

    } catch (err) {
        const message = err instanceof Error ? err.message : 'Unknown error';
        return new Response(`OAuth callback error: ${message}`, { status: 500 });
    }
}

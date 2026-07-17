// Magic Link 验证端点
// 用户点击邮件中的链接后，验证 token 并完成登录

interface Env {
    JWT_SECRET: string;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    smartbank_db: any; // D1Database
}

// JWT 工具函数
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
    const token = url.searchParams.get('token');

    if (!token) {
        return new Response(generateErrorPage('缺少登录令牌'), {
            status: 400,
            headers: { 'Content-Type': 'text/html; charset=utf-8' },
        });
    }

    try {
        // 查询 token
        const tokenRecord = await env.smartbank_db.prepare(`
            SELECT * FROM magic_tokens WHERE token = ?
        `).bind(token).first();

        if (!tokenRecord) {
            return new Response(generateErrorPage('无效的登录链接'), {
                status: 400,
                headers: { 'Content-Type': 'text/html; charset=utf-8' },
            });
        }

        // 检查是否已使用
        if (tokenRecord.used) {
            return new Response(generateErrorPage('此链接已被使用，请重新申请'), {
                status: 400,
                headers: { 'Content-Type': 'text/html; charset=utf-8' },
            });
        }

        // 检查是否过期
        if (new Date(tokenRecord.expires_at).getTime() < Date.now()) {
            return new Response(generateErrorPage('链接已过期，请重新申请'), {
                status: 400,
                headers: { 'Content-Type': 'text/html; charset=utf-8' },
            });
        }

        const email = tokenRecord.email;

        // 标记 token 为已使用
        await env.smartbank_db.prepare(`
            UPDATE magic_tokens SET used = 1 WHERE token = ?
        `).bind(token).run();

        // 查找或创建用户
        let user = await env.smartbank_db.prepare(`
            SELECT * FROM users WHERE id = ?
        `).bind(`email:${email}`).first();

        if (!user) {
            // 从邮箱提取用户名（@前面的部分）
            const username = email.split('@')[0];

            // 创建新用户
            await env.smartbank_db.prepare(`
                INSERT INTO users (id, username, avatar_url, email, role, credits)
                VALUES (?, ?, ?, ?, 'student', 100)
            `).bind(
                `email:${email}`,
                username,
                null,
                email
            ).run();

            user = await env.smartbank_db.prepare(`
                SELECT * FROM users WHERE id = ?
            `).bind(`email:${email}`).first();
        }

        // 生成 JWT
        const jwt = await createJWT({
            sub: user.id,
            username: user.username,
            email: user.email,
        }, env.JWT_SECRET);

        // 返回成功页面，通过 postMessage 将 token 发送给父窗口
        return new Response(generateSuccessPage(jwt, user.username), {
            headers: { 'Content-Type': 'text/html; charset=utf-8' },
        });

    } catch (err) {
        const message = err instanceof Error ? err.message : '登录失败';
        return new Response(generateErrorPage(message), {
            status: 500,
            headers: { 'Content-Type': 'text/html; charset=utf-8' },
        });
    }
}

function generateSuccessPage(jwt: string, username: string): string {
    return `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>登录成功 - SmartBank Agent</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 400px;
        }
        .icon {
            font-size: 64px;
            margin-bottom: 16px;
        }
        h1 {
            color: #10b981;
            margin: 0 0 8px;
            font-size: 24px;
        }
        p {
            color: #666;
            margin: 0 0 24px;
        }
        .btn {
            display: inline-block;
            padding: 12px 32px;
            background: #10b981;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 16px;
            transition: background 0.2s;
        }
        .btn:hover {
            background: #059669;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">✅</div>
        <h1>登录成功</h1>
        <p>欢迎回来，${username}！</p>
        <a href="/" class="btn">进入 SmartBank Agent</a>
    </div>
    <script>
        // 存储 token
        localStorage.setItem('smartbank-token', '${jwt}');
        // 通知父窗口（如果是在弹窗中打开）
        if (window.opener) {
            window.opener.postMessage({ type: 'magic-link-login', token: '${jwt}' }, '*');
        }
    </script>
</body>
</html>`;
}

function generateErrorPage(message: string): string {
    return `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>登录失败 - SmartBank Agent</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 400px;
        }
        .icon {
            font-size: 64px;
            margin-bottom: 16px;
        }
        h1 {
            color: #ef4444;
            margin: 0 0 8px;
            font-size: 24px;
        }
        p {
            color: #666;
            margin: 0 0 24px;
        }
        .btn {
            display: inline-block;
            padding: 12px 32px;
            background: #ef4444;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 16px;
            transition: background 0.2s;
        }
        .btn:hover {
            background: #dc2626;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">❌</div>
        <h1>登录失败</h1>
        <p>${message}</p>
        <a href="/" class="btn">返回首页</a>
    </div>
</body>
</html>`;
}

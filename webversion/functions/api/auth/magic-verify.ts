// Magic Link 验证端点 - 已禁用
// 登录功能已取消，此端点不再支持

export async function onRequestGet() {
    return new Response(generateErrorPage('登录功能已禁用，所有用户可直接使用'), {
        status: 403,
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
    });
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

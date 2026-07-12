// GitHub OAuth 发起端点
// 重定向用户到 GitHub 授权页面

interface Env {
    GITHUB_CLIENT_ID: string;
}

export async function onRequestGet(context: { env: Env }) {
    const { env } = context;

    const clientId = env.GITHUB_CLIENT_ID;
    // 回调地址必须与 GitHub OAuth App 配置一致
    const redirectUri = 'https://smartbanking.pages.dev/api/auth/callback';

    // 生成随机 state 防止 CSRF
    const state = crypto.randomUUID();

    // 构建 GitHub OAuth URL
    const githubAuthUrl = new URL('https://github.com/login/oauth/authorize');
    githubAuthUrl.searchParams.set('client_id', clientId);
    githubAuthUrl.searchParams.set('redirect_uri', redirectUri);
    githubAuthUrl.searchParams.set('scope', 'read:user user:email');
    githubAuthUrl.searchParams.set('state', state);

    // 重定向到 GitHub
    return Response.redirect(githubAuthUrl.toString(), 302);
}

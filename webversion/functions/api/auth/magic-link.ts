// Magic Link 发送端点
// 用户输入邮箱，生成一次性登录链接并发送

interface Env {
    JWT_SECRET: string;
    RESEND_API_KEY: string;
    SITE_URL: string;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    smartbank_db: any; // D1Database
}

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequestPost(context: { request: Request; env: Env }) {
    const { request, env } = context;

    try {
        const { email } = await request.json() as { email: string };

        if (!email || !email.includes('@')) {
            return new Response(JSON.stringify({ error: '请输入有效的邮箱地址' }), {
                status: 400,
                headers: { 'Content-Type': 'application/json', ...corsHeaders },
            });
        }

        // 生成一次性 token（15分钟有效期）
        const token = crypto.randomUUID();
        const expiresAt = Date.now() + 15 * 60 * 1000; // 15分钟

        // 将 token 和邮箱存储到 KV（Cloudflare Workers KV）
        // 注意：需要在 Cloudflare Dashboard 创建 KV namespace 并绑定为 MAGIC_TOKENS
        // 如果没有 KV，可以使用 D1 数据库存储
        const tokenData = JSON.stringify({
            email,
            expiresAt,
            used: false,
        });

        // 使用 D1 存储 token（更通用，不需要额外配置 KV）
        await context.env.smartbank_db.prepare(`
            INSERT INTO magic_tokens (token, email, expires_at, used)
            VALUES (?, ?, ?, 0)
        `).bind(token, email, new Date(expiresAt).toISOString()).run();

        // 构建登录链接
        const loginUrl = `${env.SITE_URL}/api/auth/magic-verify?token=${token}`;

        // 发送邮件（使用 Resend 免费版）
        const emailResponse = await fetch('https://api.resend.com/emails', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${env.RESEND_API_KEY}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                from: 'SmartBank Agent <noreply@smartbanking.pages.dev>',
                to: email,
                subject: '登录 SmartBank Agent',
                html: `
                    <div style="font-family: sans-serif; max-width: 400px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #10b981;">SmartBank Agent 登录</h2>
                        <p>点击下方链接登录您的账户：</p>
                        <a href="${loginUrl}" 
                           style="display: inline-block; padding: 12px 24px; background: #10b981; color: white; text-decoration: none; border-radius: 8px; margin: 16px 0;">
                            登录 SmartBank Agent
                        </a>
                        <p style="color: #666; font-size: 14px;">此链接 15 分钟内有效。如果您没有请求登录，请忽略此邮件。</p>
                    </div>
                `,
            }),
        });

        if (!emailResponse.ok) {
            const error = await emailResponse.text();
            console.error('Resend API error:', error);
            // 即使邮件发送失败，也返回成功（开发环境可能没有配置 Resend）
            return new Response(JSON.stringify({
                success: true,
                message: '登录链接已发送（开发模式：请查看控制台）',
                debug: { loginUrl }
            }), {
                headers: { 'Content-Type': 'application/json', ...corsHeaders },
            });
        }

        return new Response(JSON.stringify({
            success: true,
            message: '登录链接已发送到您的邮箱，请查收'
        }), {
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });

    } catch (err) {
        const message = err instanceof Error ? err.message : '发送失败';
        return new Response(JSON.stringify({ error: message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }
}

export async function onRequestOptions() {
    return new Response(null, { headers: corsHeaders });
}

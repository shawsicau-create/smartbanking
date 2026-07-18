// JWT 验证端点 - 已禁用
// 登录功能已取消，此端点不再支持

export async function onRequestGet() {
    return new Response(JSON.stringify({
        error: '登录功能已禁用',
        message: '此应用已取消登录功能，所有用户可直接使用'
    }), {
        status: 403,
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
    });
}

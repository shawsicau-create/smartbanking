// Magic Link 发送端点 - 已禁用
// 登录功能已取消，此端点不再支持

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequestPost() {
    return new Response(JSON.stringify({
        error: '登录功能已禁用',
        message: '此应用已取消登录功能，所有用户可直接使用'
    }), {
        status: 403,
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
}

export async function onRequestOptions() {
    return new Response(null, { headers: corsHeaders });
}

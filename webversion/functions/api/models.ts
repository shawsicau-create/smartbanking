// Cloudflare Pages Function: /api/models
// 返回可用模型列表（无状态，模型选择由前端管理）

interface Env {
    MIMO_API_KEY: string;
    BAILIAN_API_KEY?: string;
}

const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
};

const MODELS = [
    {
        id: 'mimo',
        name: 'MiMo',
        enabled: true,
        priority: 1,
        current: true,
    },
    {
        id: 'bailian',
        name: '百炼',
        enabled: true,
        priority: 2,
        current: false,
    },
    {
        id: 'paieas',
        name: 'PAI-EAS微调模型',
        enabled: true,
        priority: 3,
        current: false,
    },
];

// GET /api/models - 返回模型列表
export async function onRequestGet(context: { env: Env }) {
    const models = MODELS.map(m => ({
        ...m,
        enabled: m.id === 'bailian' ? !!context.env.BAILIAN_API_KEY : !!context.env.MIMO_API_KEY,
    }));
    return new Response(JSON.stringify({ current: 'mimo', models }), {
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
}

// POST /api/models/switch - 前端切换模型（无状态，仅返回确认）
export async function onRequestPost(context: { request: Request; env: Env }) {
    try {
        const { model } = await context.request.json();
        if (!model || !MODELS.find(m => m.id === model)) {
            return new Response(JSON.stringify({ error: '无效的模型ID', available: MODELS.map(m => m.id) }), {
                status: 400,
                headers: { 'Content-Type': 'application/json', ...corsHeaders },
            });
        }
        return new Response(JSON.stringify({ success: true, current: model, name: MODELS.find(m => m.id === model)?.name }), {
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    } catch {
        return new Response(JSON.stringify({ error: '请求格式错误' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }
}

// OPTIONS /api/models - CORS preflight
export async function onRequestOptions() {
    return new Response(null, { headers: corsHeaders });
}

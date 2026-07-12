// Cloudflare Pages Function: /api/chat
// 使用 MiMo API 作为 LLM 后端

interface Env {
    MIMO_API_KEY: string;
    TUSHARE_TOKEN: string;
}

const MIMO_API_URL = 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions';
const MIMO_MODEL = 'mimo-v2.5-pro';

const SYSTEM_PROMPT = `你是 SmartBank Agent，由四川农业大学智慧银行实验室开发的金融实验教学智能体。
你的职责是帮助学生理解金融概念、分析市场数据、完成金融实验任务。
你可以调用以下金融工具获取实时数据：
- query_stock: 查询A股个股行情
- query_stock_basic: 根据名称模糊搜索股票代码
- query_index: 查询指数行情
- query_macro_gdp: 查询世界银行GDP数据
- query_macro_indicator: 查询世界银行宏观指标
请用中文回答，数据展示时使用表格格式，分析要结合金融理论。`;

const tools = [
    {
        type: 'function',
        function: {
            name: 'query_stock',
            description: '查询A股个股行情数据，返回近期日线数据（开盘价、收盘价、最高价、最低价、成交量等）',
            parameters: {
                type: 'object',
                properties: {
                    ts_code: {
                        type: 'string',
                        description: '股票代码，格式如 000001.SZ（深圳）、600000.SH（上海）',
                    },
                    start_date: {
                        type: 'string',
                        description: '起始日期，格式 YYYYMMDD，默认为近30天',
                    },
                    end_date: {
                        type: 'string',
                        description: '结束日期，格式 YYYYMMDD，默认为今天',
                    },
                },
                required: ['ts_code'],
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'query_stock_basic',
            description: '根据股票名称模糊搜索股票代码和基本信息',
            parameters: {
                type: 'object',
                properties: {
                    name: {
                        type: 'string',
                        description: '股票名称或关键词，如"平安银行"、"贵州茅台"',
                    },
                },
                required: ['name'],
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'query_index',
            description: '查询A股指数行情数据（如上证指数、深证成指、沪深300等）',
            parameters: {
                type: 'object',
                properties: {
                    ts_code: {
                        type: 'string',
                        description: '指数代码，如 000001.SH（上证指数）、399001.SZ（深证成指）、000300.SH（沪深300）',
                    },
                    start_date: {
                        type: 'string',
                        description: '起始日期，格式 YYYYMMDD，默认为近30天',
                    },
                    end_date: {
                        type: 'string',
                        description: '结束日期，格式 YYYYMMDD，默认为今天',
                    },
                },
                required: ['ts_code'],
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'query_macro_gdp',
            description: '查询世界银行GDP数据（美元），返回近5年数据',
            parameters: {
                type: 'object',
                properties: {
                    country: {
                        type: 'string',
                        description: '国家代码，如 CN（中国）、US（美国）、JP（日本）、DE（德国）、GB（英国）',
                    },
                },
                required: ['country'],
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'query_macro_indicator',
            description: '查询世界银行宏观指标数据，如CPI、失业率、贸易额等',
            parameters: {
                type: 'object',
                properties: {
                    country: {
                        type: 'string',
                        description: '国家代码，如 CN（中国）、US（美国）',
                    },
                    indicator: {
                        type: 'string',
                        description: '指标代码，如 FP.CPI.TOTL.ZG（CPI通胀率）、SL.UEM.TOTL.ZS（失业率）、NE.EXP.GNFS.ZS（贸易占GDP比）',
                    },
                },
                required: ['country', 'indicator'],
            },
        },
    },
];

interface ChatMessage {
    role: string;
    content: string;
    tool_calls?: Array<{
        id: string;
        type: string;
        function: { name: string; arguments: string };
    }>;
    tool_call_id?: string;
}

interface ToolCallResult {
    name: string;
    args: Record<string, string>;
    result: unknown;
}

async function callLLM(messages: ChatMessage[], useTools: boolean, env: Env) {
    const body: Record<string, unknown> = {
        model: MIMO_MODEL,
        messages,
        temperature: 0.7,
        max_tokens: 2048,
    };
    if (useTools) {
        body.tools = tools;
        body.tool_choice = 'auto';
    }
    const resp = await fetch(MIMO_API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${env.MIMO_API_KEY}`,
        },
        body: JSON.stringify(body),
    });
    if (!resp.ok) {
        const text = await resp.text();
        throw new Error(`MiMo API error ${resp.status}: ${text}`);
    }
    return resp.json();
}

async function callTushare(apiName: string, params: Record<string, string>, fields: string, env: Env) {
    const resp = await fetch('https://api.tushare.pro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            api_name: apiName,
            token: env.TUSHARE_TOKEN,
            params,
            fields,
        }),
    });
    if (!resp.ok) throw new Error(`Tushare API error: ${resp.status}`);
    return resp.json();
}

function today(): string {
    return new Date().toISOString().slice(0, 10).replace(/-/g, '');
}

function thirtyDaysAgo(): string {
    const d = new Date();
    d.setDate(d.getDate() - 30);
    return d.toISOString().slice(0, 10).replace(/-/g, '');
}

async function executeTool(name: string, args: Record<string, string>, env: Env): Promise<unknown> {
    switch (name) {
        case 'query_stock': {
            const data = await callTushare(
                'daily',
                {
                    ts_code: args.ts_code,
                    start_date: args.start_date || thirtyDaysAgo(),
                    end_date: args.end_date || today(),
                },
                'ts_code,trade_date,open,high,low,close,vol,amount',
                env,
            );
            return {
                count: data.data?.items?.length || 0,
                fields: data.data?.fields,
                items: data.data?.items?.slice(0, 10),
            };
        }
        case 'query_stock_basic': {
            const data = await callTushare(
                'stock_basic',
                { name: args.name },
                'ts_code,name,industry,market,list_date',
                env,
            );
            return {
                count: data.data?.items?.length || 0,
                items: data.data?.items,
            };
        }
        case 'query_index': {
            const data = await callTushare(
                'index_daily',
                {
                    ts_code: args.ts_code,
                    start_date: args.start_date || thirtyDaysAgo(),
                    end_date: args.end_date || today(),
                },
                'ts_code,trade_date,open,high,low,close,vol,amount',
                env,
            );
            return {
                count: data.data?.items?.length || 0,
                fields: data.data?.fields,
                items: data.data?.items?.slice(0, 10),
            };
        }
        case 'query_macro_gdp': {
            const endYear = new Date().getFullYear();
            const startYear = endYear - 5;
            const url = `https://api.worldbank.org/v2/country/${args.country}/indicator/NY.GDP.MKTP.CD?format=json&date=${startYear}:${endYear}`;
            const resp = await fetch(url);
            if (!resp.ok) throw new Error(`World Bank API error: ${resp.status}`);
            const json = await resp.json();
            const records = json[1] || [];
            return {
                country: args.country,
                data: records.map((r: { date: string; value: number | null }) => ({
                    year: r.date,
                    value: r.value,
                })),
            };
        }
        case 'query_macro_indicator': {
            const endYear = new Date().getFullYear();
            const startYear = endYear - 5;
            const ind = args.indicator.includes('.')
                ? args.indicator
                : args.indicator.replace(/_/g, '.');
            const url = `https://api.worldbank.org/v2/country/${args.country}/indicator/${ind}?format=json&date=${startYear}:${endYear}`;
            const resp = await fetch(url);
            if (!resp.ok) throw new Error(`World Bank API error: ${resp.status}`);
            const json = await resp.json();
            const records = json[1] || [];
            return {
                country: args.country,
                indicator: ind,
                data: records.map((r: { date: string; value: number | null }) => ({
                    year: r.date,
                    value: r.value,
                })),
            };
        }
        default:
            throw new Error(`Unknown tool: ${name}`);
    }
}

export async function onRequestPost(context: { request: Request; env: Env }) {
    const { request, env } = context;

    // CORS headers
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    };

    try {
        const { messages } = (await request.json()) as { messages: Array<{ role: string; content: string }> };

        if (!messages?.length) {
            return new Response(JSON.stringify({ error: 'messages 不能为空' }), {
                status: 400,
                headers: { 'Content-Type': 'application/json', ...corsHeaders },
            });
        }

        const chatMessages: ChatMessage[] = [
            { role: 'system', content: SYSTEM_PROMPT },
            ...messages,
        ];

        const data = await callLLM(chatMessages, true, env);
        const assistantMsg = data.choices?.[0]?.message;

        if (!assistantMsg) {
            return new Response(JSON.stringify({ error: 'MiMo 未返回有效响应' }), {
                status: 502,
                headers: { 'Content-Type': 'application/json', ...corsHeaders },
            });
        }

        const toolCallResults: ToolCallResult[] = [];

        if (assistantMsg.tool_calls?.length) {
            chatMessages.push(assistantMsg as ChatMessage);

            for (const tc of assistantMsg.tool_calls) {
                let args: Record<string, string> = {};
                try {
                    args = JSON.parse(tc.function.arguments);
                } catch { /* keep empty */ }

                let result: unknown;
                try {
                    result = await executeTool(tc.function.name, args, env);
                } catch (err) {
                    result = { error: err instanceof Error ? err.message : '工具执行失败' };
                }

                toolCallResults.push({ name: tc.function.name, args, result });

                chatMessages.push({
                    role: 'tool',
                    tool_call_id: tc.id,
                    content: JSON.stringify(result),
                });
            }

            const finalData = await callLLM(chatMessages, false, env);
            const finalContent = finalData.choices?.[0]?.message?.content || '';

            return new Response(
                JSON.stringify({ content: finalContent, toolCalls: toolCallResults }),
                { headers: { 'Content-Type': 'application/json', ...corsHeaders } },
            );
        }

        return new Response(
            JSON.stringify({ content: assistantMsg.content || '' }),
            { headers: { 'Content-Type': 'application/json', ...corsHeaders } },
        );
    } catch (err) {
        const message = err instanceof Error ? err.message : '服务器内部错误';
        return new Response(JSON.stringify({ error: message }), {
            status: 500,
            headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
    }
}

export async function onRequestOptions() {
    return new Response(null, {
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
    });
}

// Cloudflare Pages Function: /api/chat
// 使用 MiMo API 作为 LLM 后端

import { search, extract, batchSearch } from './search';

interface Env {
    MIMO_API_KEY: string;
    TUSHARE_TOKEN: string;
    BAILIAN_API_KEY?: string;
}

// 多模型配置
const MODEL_CONFIGS: Record<string, { url: string; model: string; name: string; getKey: (env: Env) => string }> = {
    mimo: {
        url: 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions',
        model: 'mimo-v2.5-pro',
        name: 'MiMo',
        getKey: (env) => env.MIMO_API_KEY,
    },
    bailian: {
        url: 'https://ws-paxy280v9746pda1.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions',
        model: 'qwen-plus',
        name: '百炼',
        getKey: (env) => env.BAILIAN_API_KEY || '',
    },
};

const DEFAULT_MODEL = 'mimo';

const SYSTEM_PROMPT = `你是 SmartBank Agent，由四川农业大学智慧银行实验室开发的金融实验教学智能体。
你的职责是帮助学生理解金融概念、分析市场数据、完成金融实验任务。

## 联网检索优先原则
当用户询问以下类型问题时，**必须优先使用web_search工具**获取最新信息：
1. **实时市场行情**：今日大盘走势、某股票最新价格、今日涨跌
2. **最新财经新闻**：今日财经要闻、最新政策、市场动态
3. **时事热点**：最新事件、当前形势、实时数据
4. **任何需要"今天"、"最新"、"现在"等时效性信息的问题**

搜索策略：
- 先用web_search搜索关键词获取最新信息
- 如需详细了解某个搜索结果，再用web_extract提取网页内容
- 综合多个搜索结果给出完整回答

## 可用工具
- **web_search**: 实时网页搜索（获取最新新闻、市场动态）
- **web_extract**: 提取网页详细内容
- **batch_search**: 批量搜索多个关键词
- **query_stock/query_index**: 查询A股历史行情
- **query_macro_***: 宏观经济指标

## 回答规范
1. 使用中文回答
2. 数据展示使用表格格式
3. 分析结合金融理论
4. 涉及实时信息时，必须先搜索再回答，不要凭记忆编造数据
5. 引用数据时注明来源（如"根据今日搜索结果..."）`;

const tools = [
    {
        type: 'function',
        function: {
            name: 'web_search',
            description: '使用AnySearch进行实时网页搜索，获取最新信息。适用于查询新闻、市场动态、行业信息等。',
            parameters: {
                type: 'object',
                properties: {
                    query: {
                        type: 'string',
                        description: '搜索关键词，如"贵州茅台最新财报"、"央行降息最新消息"',
                    },
                    max_results: {
                        type: 'number',
                        description: '最大返回结果数，默认为5',
                    },
                },
                required: ['query'],
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'web_extract',
            description: '提取指定网页的详细内容，返回Markdown格式。适用于获取文章、报告、公告的完整内容。',
            parameters: {
                type: 'object',
                properties: {
                    url: {
                        type: 'string',
                        description: '要提取内容的网页URL',
                    },
                },
                required: ['url'],
            },
        },
    },
    {
        type: 'function',
        function: {
            name: 'batch_search',
            description: '批量搜索多个关键词，用于对比分析多个主题。',
            parameters: {
                type: 'object',
                properties: {
                    queries: {
                        type: 'array',
                        items: {
                            type: 'object',
                            properties: {
                                query: { type: 'string', description: '搜索关键词' },
                                max_results: { type: 'number', description: '最大返回结果数' },
                            },
                            required: ['query'],
                        },
                        description: '搜索查询数组',
                    },
                },
                required: ['queries'],
            },
        },
    },
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

async function callLLM(messages: ChatMessage[], useTools: boolean, env: Env, modelId: string = DEFAULT_MODEL) {
    const config = MODEL_CONFIGS[modelId] || MODEL_CONFIGS[DEFAULT_MODEL];
    const apiKey = config.getKey(env);
    if (!apiKey) throw new Error(`${config.name} API Key 未配置`);

    const body: Record<string, unknown> = {
        model: config.model,
        messages,
        temperature: 0.7,
        max_tokens: 2048,
    };
    if (useTools) {
        body.tools = tools;
        body.tool_choice = 'auto';
    }
    const resp = await fetch(config.url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${apiKey}`,
        },
        body: JSON.stringify(body),
    });
    if (!resp.ok) {
        const text = await resp.text();
        throw new Error(`${config.name} API error ${resp.status}: ${text}`);
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
        case 'web_search': {
            const query = args.query;
            const maxResults = parseInt(args.max_results || '5', 10);
            const result = await search(query, maxResults);
            return result;
        }
        case 'web_extract': {
            const url = args.url;
            const result = await extract(url);
            return result;
        }
        case 'batch_search': {
            // 解析queries参数，需要处理JSON字符串
            let queries: Array<{ query: string; max_results?: number }> = [];
            try {
                // args.queries可能是JSON字符串
                const queriesStr = args.queries || '[]';
                queries = JSON.parse(queriesStr);
            } catch {
                // 如果解析失败，尝试从args中构造
                queries = [{ query: args.query || '', max_results: parseInt(args.max_results || '5', 10) }];
            }
            const result = await batchSearch(queries);
            return result;
        }
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
        const { messages, model: requestModel } = (await request.json()) as { messages: Array<{ role: string; content: string }>; model?: string };
        const modelId = requestModel && MODEL_CONFIGS[requestModel] ? requestModel : DEFAULT_MODEL;

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

        const data = await callLLM(chatMessages, true, env, modelId);
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

            const finalData = await callLLM(chatMessages, false, env, modelId);
            const finalContent = finalData.choices?.[0]?.message?.content || '';

            return new Response(
                JSON.stringify({ content: finalContent, toolCalls: toolCallResults }),
                { headers: { 'Content-Type': 'application/json', ...corsHeaders } },
            );
        }

        // 防护：如果模型返回原始 <tool_call> 标签而非结构化tool_calls，解析并执行
        let content = assistantMsg.content || '';
        if (content.includes('<tool_call>') && content.includes('<function=')) {
            const toolMatch = content.match(/<function=([^>]+)>([\s\S]*?)<\/function>/);
            if (toolMatch) {
                const toolName = toolMatch[1];
                const paramMatches = [...toolMatch[2].matchAll(/<parameter=([^>]+)>([^<]*)<\/parameter>/g)];
                const parsedArgs: Record<string, string> = {};
                for (const pm of paramMatches) { parsedArgs[pm[1]] = pm[2].trim(); }
                let result: unknown;
                try { result = await executeTool(toolName, parsedArgs, env); } catch (err) { result = { error: err instanceof Error ? err.message : '工具执行失败' }; }
                toolCallResults.push({ name: toolName, args: parsedArgs, result });
                // 把工具结果反馈给模型获取最终回答
                chatMessages.push({ role: 'assistant', content });
                chatMessages.push({ role: 'user', content: '工具执行结果：\n' + JSON.stringify(result, null, 2) + '\n\n请根据以上工具返回的数据，用中文给出完整回答。' });
                const retryData = await callLLM(chatMessages, false, env);
                content = retryData.choices?.[0]?.message?.content || content;
            }
        }

        return new Response(
            JSON.stringify({ content, toolCalls: toolCallResults }),
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

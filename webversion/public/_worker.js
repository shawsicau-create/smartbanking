// Cloudflare Pages Advanced Mode Worker - SmartBank Agent API
// 使用 MiMo API + Tushare + World Bank

export default {
    async fetch(request, env) {
        const url = new URL(request.url);
        if (url.pathname === '/api/chat') {
            return handleChatRequest(request, env);
        }
        if (env.ASSETS) {
            return env.ASSETS.fetch(request);
        }
        return new Response('Not Found', { status: 404 });
    }
};

async function handleChatRequest(request, env) {
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
        return new Response(null, { headers: corsHeaders });
    }
    if (request.method !== 'POST') {
        return new Response(JSON.stringify({ error: 'Method not allowed' }), {
            status: 405, headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
    }

    try {
        const { messages } = await request.json();
        if (!messages?.length) {
            return new Response(JSON.stringify({ error: 'messages 不能为空' }), {
                status: 400, headers: { 'Content-Type': 'application/json', ...corsHeaders }
            });
        }

        const MIMO_API_URL = 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions';
        const MIMO_MODEL = 'mimo-v2.5-pro';

        const SYSTEM_PROMPT = `你是 SmartBank Agent，由四川农业大学智慧银行实验室开发的金融实验教学智能体。
你的职责是帮助学生理解金融概念、分析市场数据、完成金融实验任务。

当需要查询实时数据时，你必须在回复中使用以下格式调用工具：

<tool_call>
<function=工具名>
<parameter=参数名>参数值</parameter>
</function>
</tool_call>

可用工具：
1. query_stock - 查询A股个股日线行情（参数：ts_code如600519.SH，可选start_date/end_date为YYYYMMDD）
2. query_stock_basic - 根据名称搜索股票代码（参数：name如"贵州茅台"）
3. query_index - 查询指数行情（参数：ts_code如000001.SH）
4. query_macro_gdp - 查询世界银行GDP数据（参数：country如CN/US）
5. query_macro_indicator - 查询宏观指标（参数：country, indicator如FP.CPI.TOTL.ZG）

规则：
- 每次只调用一个工具，等待结果返回后再决定下一步
- 常见股票代码：贵州茅台=600519.SH, 平安银行=000001.SZ, 上证指数=000001.SH
- 数据展示时使用表格格式，分析要结合金融理论
- 请用中文回答`;

        const chatMessages = [
            { role: 'system', content: SYSTEM_PROMPT },
            ...messages
        ];

        // 第一次调用 LLM
        const llmResponse = await fetch(MIMO_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${env.MIMO_API_KEY}` },
            body: JSON.stringify({ model: MIMO_MODEL, messages: chatMessages, temperature: 0.7, max_tokens: 2048 })
        });

        if (!llmResponse.ok) {
            const errorText = await llmResponse.text();
            throw new Error(`MiMo API error: ${llmResponse.status} - ${errorText}`);
        }

        const llmData = await llmResponse.json();
        let assistantContent = llmData.choices?.[0]?.message?.content || '';

        if (!assistantContent) {
            throw new Error('MiMo 未返回有效响应');
        }

        const toolCallResults = [];
        let maxRounds = 5; // 防止无限循环

        // 循环处理工具调用
        while (maxRounds-- > 0) {
            // 检测 <tool_call> 格式
            const toolCallMatch = assistantContent.match(/<tool_call>\s*<function=(\w+)>([\s\S]*?)<\/function>\s*<\/tool_call>/);

            if (!toolCallMatch) break; // 没有工具调用，退出循环

            const toolName = toolCallMatch[1];
            const paramsBlock = toolCallMatch[2];

            // 解析参数
            const args = {};
            const paramRegex = /<parameter=(\w+)>([\s\S]*?)<\/parameter>/g;
            let paramMatch;
            while ((paramMatch = paramRegex.exec(paramsBlock)) !== null) {
                args[paramMatch[1]] = paramMatch[2].trim();
            }

            // 执行工具
            let result;
            try {
                result = await executeTool(toolName, args, env);
            } catch (err) {
                result = { error: err.message || '工具执行失败' };
            }

            toolCallResults.push({ name: toolName, args, result });

            // 将工具调用和结果加入对话
            chatMessages.push({ role: 'assistant', content: assistantContent });
            chatMessages.push({
                role: 'user',
                content: `工具 ${toolName} 的执行结果是：\n${JSON.stringify(result)}\n\n请基于以上数据回答用户的问题。不要再调用工具。`
            });

            // 再次调用 LLM 获取最终回答
            const nextResponse = await fetch(MIMO_API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${env.MIMO_API_KEY}` },
                body: JSON.stringify({ model: MIMO_MODEL, messages: chatMessages, temperature: 0.7, max_tokens: 2048 })
            });

            const nextData = await nextResponse.json();
            assistantContent = nextData.choices?.[0]?.message?.content || '';

            // 如果仍有 tool_call，继续循环；否则返回
            if (!assistantContent.includes('<tool_call>')) break;
        }

        // 清理回复中的 <tool_call> 标签
        assistantContent = assistantContent.replace(/<tool_call>[\s\S]*?<\/tool_call>/g, '').trim();

        return new Response(JSON.stringify({
            content: assistantContent,
            toolCalls: toolCallResults
        }), { headers: { 'Content-Type': 'application/json', ...corsHeaders } });

    } catch (err) {
        return new Response(JSON.stringify({ error: err.message || '服务器内部错误' }), {
            status: 500, headers: { 'Content-Type': 'application/json', ...corsHeaders }
        });
    }
}

async function executeTool(name, args, env) {
    const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const thirtyDaysAgo = (() => {
        const d = new Date();
        d.setDate(d.getDate() - 30);
        return d.toISOString().slice(0, 10).replace(/-/g, '');
    })();

    const callTushare = async (apiName, params, fields) => {
        const resp = await fetch('https://api.tushare.pro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_name: apiName, token: env.TUSHARE_TOKEN, params, fields })
        });
        const data = await resp.json();
        if (data.code !== 0) throw new Error(`Tushare: ${data.msg}`);
        return data;
    };

    switch (name) {
        case 'query_stock': {
            const data = await callTushare('daily', {
                ts_code: args.ts_code,
                start_date: args.start_date || thirtyDaysAgo,
                end_date: args.end_date || today
            }, 'ts_code,trade_date,open,high,low,close,vol,amount');
            const items = data.data?.items || [];
            return { count: items.length, items: items.slice(0, 10) };
        }
        case 'query_stock_basic': {
            // Tushare stock_basic 不支持 name 过滤，获取全部后本地搜索
            const data = await callTushare('stock_basic', { list_status: 'L' }, 'ts_code,name,industry,market,list_date');
            const allItems = data.data?.items || [];
            const filtered = allItems.filter(item =>
                String(item[1] || '').includes(args.name)
            );
            return { count: filtered.length, items: filtered.slice(0, 10) };
        }
        case 'query_index': {
            const data = await callTushare('index_daily', {
                ts_code: args.ts_code,
                start_date: args.start_date || thirtyDaysAgo,
                end_date: args.end_date || today
            }, 'ts_code,trade_date,open,high,low,close,vol,amount');
            const items = data.data?.items || [];
            return { count: items.length, items: items.slice(0, 10) };
        }
        case 'query_macro_gdp': {
            const endYear = new Date().getFullYear();
            const url = `https://api.worldbank.org/v2/country/${args.country}/indicator/NY.GDP.MKTP.CD?format=json&date=${endYear - 5}:${endYear}`;
            const resp = await fetch(url);
            const json = await resp.json();
            return { country: args.country, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) };
        }
        case 'query_macro_indicator': {
            const endYear = new Date().getFullYear();
            const ind = args.indicator.includes('.') ? args.indicator : args.indicator.replace(/_/g, '.');
            const url = `https://api.worldbank.org/v2/country/${args.country}/indicator/${ind}?format=json&date=${endYear - 5}:${endYear}`;
            const resp = await fetch(url);
            const json = await resp.json();
            return { country: args.country, indicator: ind, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) };
        }
        default:
            throw new Error(`Unknown tool: ${name}`);
    }
}

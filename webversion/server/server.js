import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;
app.use(cors());
app.use(express.json({ limit: '10mb' }));
const MIMO_API_URL = 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions';
const MIMO_MODEL = 'mimo-v2.5-pro';
const AMAP_API_KEY = '63f93d2223f744affebade9ef7982732';
const TC_OPEN = String.fromCharCode(60) + 'tool_call' + String.fromCharCode(62);
const TC_CLOSE = String.fromCharCode(60) + '/tool_call' + String.fromCharCode(62);
function fnTag(name) { return String.fromCharCode(60) + 'function=' + name + String.fromCharCode(62); }
function pmTag(name) { return String.fromCharCode(60) + 'parameter=' + name + String.fromCharCode(62); }
const FN_CLOSE = String.fromCharCode(60) + '/function' + String.fromCharCode(62);
const PM_CLOSE = String.fromCharCode(60) + '/parameter' + String.fromCharCode(62);
async function callMiMo(messages, temperature, maxTokens) {
    const resp = await fetch(MIMO_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + process.env.MIMO_API_KEY },
        body: JSON.stringify({ model: MIMO_MODEL, messages, temperature: temperature || 0.7, max_tokens: maxTokens || 2048 }),
    });
    if (!resp.ok) throw new Error('MiMo API error: ' + resp.status);
    const data = await resp.json();
    const c = data.choices?.[0]?.message?.content || '';
    if (!c) throw new Error('MiMo empty');
    return c;
}
async function callTushare(apiName, params, fields) {
    const resp = await fetch('https://api.tushare.pro', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_name: apiName, token: process.env.TUSHARE_TOKEN, params, fields }),
    });
    const data = await resp.json();
    if (data.code !== 0) throw new Error('Tushare: ' + data.msg);
    return data;
}
function parseToolCall(text) {
    const re1 = new RegExp(TC_OPEN.replace(/[.*+?^${}()|[\]\]/g, '\\$&') + '[\s\S]*?' + TC_CLOSE.replace(/[.*+?^${}()|[\]\]/g, '\\$&'));
    const match = text.match(re1);
    if (!match) return null;
    const inner = match[0];
    const fnMatch = inner.match(/<function=(\w+)>([\s\S]*?)<\/function>/);
    if (!fnMatch) return null;
    const args = {};
    const paramRe = /<parameter=(\w+)>([\s\S]*?)<\/parameter>/g;
    let m;
    while ((m = paramRe.exec(fnMatch[2])) !== null) args[m[1]] = m[2].trim();
    return { toolName: fnMatch[1], args };
}
function today() { return new Date().toISOString().slice(0, 10).replace(/-/g, ''); }
function thirtyAgo() { const d = new Date(); d.setDate(d.getDate() - 30); return d.toISOString().slice(0, 10).replace(/-/g, ''); }
async function executeTool(name, args) {
    switch (name) {
        case 'query_stock': { const data = await callTushare('daily', { ts_code: args.ts_code, start_date: args.start_date || thirtyAgo(), end_date: args.end_date || today() }, 'ts_code,trade_date,open,high,low,close,vol,amount'); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) }; }
        case 'query_stock_basic': { const data = await callTushare('stock_basic', { list_status: 'L' }, 'ts_code,name,industry,market,list_date'); const f = (data.data?.items || []).filter(i => String(i[1] || '').includes(args.name)); return { count: f.length, items: f.slice(0, 10) }; }
        case 'query_index': { const data = await callTushare('index_daily', { ts_code: args.ts_code, start_date: args.start_date || thirtyAgo(), end_date: args.end_date || today() }, 'ts_code,trade_date,open,high,low,close,vol,amount'); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) }; }
        case 'query_stock_info': { const q = args.name || args.ts_code; const data = await callTushare('stock_basic', { list_status: 'L' }, 'ts_code,name,industry,market,list_date'); const f = (data.data?.items || []).filter(i => String(i[0]) === q || String(i[1]).includes(q)); return { count: f.length, items: f.slice(0, 5) }; }
        case 'query_fund_flow': { const data = await callTushare('moneyflow_hsgt', { start_date: args.start_date || thirtyAgo(), end_date: args.end_date || today() }, 'trade_date,ggt_ss,ggt_sz,hgt,sgt,north_money,south_money'); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 15) }; }
        case 'query_financial': { const tm = { income: 'income', balancesheet: 'balancesheet', cashflow: 'cashflow' }; const a = tm[args.type] || 'income'; const fm = { income: 'ts_code,ann_date,revenue,n_income,total_profit,operate_profit', balancesheet: 'ts_code,ann_date,total_assets,total_liab,total_hldr_eqy_exc_min_int', cashflow: 'ts_code,ann_date,n_cashflow_act,n_cashflow_inv_act,n_cash_flows_fnc_act' }; const data = await callTushare(a, { ts_code: args.ts_code }, fm[a]); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 5) }; }
        case 'query_stock_basic_info': { const data = await callTushare('daily_basic', { ts_code: args.ts_code }, 'ts_code,trade_date,pe,pb,ps,total_mv,circ_mv,turnover_rate'); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 5) }; }
        case 'query_top_holders': { const data = await callTushare('top10_holders', { ts_code: args.ts_code, ...(args.quarter ? { end_date: args.quarter } : {}) }, 'ts_code,ann_date,end_date,holder_name,hold_amount,hold_ratio'); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) }; }
        case 'query_trade_cal': { const data = await callTushare('trade_cal', { start_date: args.start_date || '20250101', end_date: args.end_date || '20251231', exchange: args.exchange || 'SSE' }, 'exchange,cal_date,is_open'); const o = (data.data?.items || []).filter(i => i[2] === '1'); return { total: data.data?.items?.length || 0, trading_days: o.length, items: o.slice(0, 10) }; }
        case 'query_macro_gdp': { const y = new Date().getFullYear(); const resp = await fetch('https://api.worldbank.org/v2/country/' + args.country + '/indicator/NY.GDP.MKTP.CD?format=json&date=' + (y - 5) + ':' + y); const json = await resp.json(); return { country: args.country, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) }; }
        case 'query_macro_indicator': { const y = new Date().getFullYear(); const ind = args.indicator.includes('.') ? args.indicator : args.indicator.replace(/_/g, '.'); const resp = await fetch('https://api.worldbank.org/v2/country/' + args.country + '/indicator/' + ind + '?format=json&date=' + (y - 5) + ':' + y); const json = await resp.json(); return { country: args.country, indicator: ind, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) }; }
        case 'query_macro_compare': { const countries = (args.countries || 'CN,US').split(',').map(s => s.trim()); const results = []; for (const c of countries.slice(0, 5)) { const resp = await fetch('https://api.worldbank.org/v2/country/' + c + '/indicator/' + args.indicator + '?format=json&date=2019:2024'); const json = await resp.json(); results.push({ country: c, data: (json[1] || []).map(r => ({ year: r.date, value: r.value, country_name: r.country?.value })) }); } return { indicator: args.indicator, comparison: results }; }
        case 'query_macro_findex': { const y = new Date().getFullYear(); const ind = args.indicator || 'FX.OWN.TOTL.ZS'; const resp = await fetch('https://api.worldbank.org/v2/country/' + (args.country || 'CN') + '/indicator/' + ind + '?format=json&date=' + (y - 8) + ':' + y); const json = await resp.json(); return { country: args.country, indicator: ind, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) }; }
        case 'search_bank_branch': { const resp = await fetch('https://restapi.amap.com/v3/place/text?key=' + AMAP_API_KEY + '&keywords=' + encodeURIComponent(args.keywords || '银行') + '&city=' + encodeURIComponent(args.city || '成都') + '&types=160100&offset=10&page=1'); const json = await resp.json(); return { count: json.count || 0, pois: (json.pois || []).map(p => ({ name: p.name, address: p.address, location: p.location, tel: p.tel })) }; }
        case 'search_nearby': { const resp = await fetch('https://restapi.amap.com/v3/place/around?key=' + AMAP_API_KEY + '&location=' + (args.location || '104.06,30.67') + '&keywords=' + encodeURIComponent(args.keywords || '银行') + '&radius=' + (args.radius || '2000') + '&offset=10'); const json = await resp.json(); return { count: json.count || 0, pois: (json.pois || []).map(p => ({ name: p.name, address: p.address, location: p.location, distance: p.distance })) }; }
        case 'generate_chart': { try { const chartData = typeof args.data === 'string' ? JSON.parse(args.data) : args.data; const chartResp = await fetch('https://mcp-server-chart.vercel.app/generate_' + (args.type || 'bar') + '_chart', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ type: args.type || 'bar', title: args.title || '金融数据图表', data: chartData, width: args.width || 600, height: args.height || 400 }) }); if (chartResp.ok) { const cj = await chartResp.json(); return { chart_url: cj.url || cj.imageUrl }; } return { config: chartData, note: '图表服务暂不可用' }; } catch (e) { return { error: '图表生成失败: ' + e.message }; } }
        default: throw new Error('Unknown tool: ' + name);
    }
}
const PROMPTS = {
    chat: (mode) => {
        const bmad = { 'bmad-analyst': '\n你当前扮演 BMAD 方法论中的**需求分析师(Analyst)**角色。', 'bmad-pm': '\n你当前扮演 BMAD 方法论中的**产品经理(PM)**角色。', 'bmad-architect': '\n你当前扮演 BMAD 方法论中的**架构师(Architect)**角色。', 'bmad-dev': '\n你当前扮演 BMAD 方法论中的**开发者(Developer)**角色。', 'bmad-qa': '\n你当前扮演 BMAD 方法论中的**质量保障(QA)**角色。' };
        return '你是 SmartBank Agent，由四川农业大学智慧银行实验室开发的金融实验教学智能体。\n你的职责是帮助学生理解金融概念、分析市场数据、完成金融实验任务。\n\n本智能体基于《智慧银行实验教程》教材，采用MCP+Skill+BMAD三位一体架构。' + (bmad[mode] || '') + '\n\n当需要查询实时数据时，使用 <tool_call> 格式调用工具。\n\n工具列表：\n1. query_stock - 查询A股个股日线行情（参数：ts_code）\n2. query_stock_basic - 根据名称搜索股票代码（参数：name）\n3. query_index - 查询指数行情（参数：ts_code）\n4. query_fund_flow - 查询沪深港通资金流向\n5. query_financial - 查询财务数据（参数：ts_code, type）\n6. query_macro_gdp - 查询世界银行GDP数据（参数：country）\n7. query_macro_indicator - 查询宏观指标（参数：country, indicator）\n8. query_macro_compare - 多国指标对比\n9. search_bank_branch - 搜索银行网点\n10. generate_chart - 生成金融图表\n\n规则：\n- 每次只调用一个工具\n- 数据展示时使用表格格式\n- 分析要结合金融理论\n- 请用中文回答';
    },
    bull: '你是一位资深的**多头分析师**（看涨派）。从增长潜力、政策利好等角度分析，提供3-5个核心看多论据，每个论据配数据支撑。请用中文回答，Markdown格式。',
    bear: '你是一位资深的**空头分析师**（看跌派）。从风险隐患、利空因素等角度分析，提供3-5个核心看空论据。请用中文回答，Markdown格式。',
    moderator: '你是金融辩论主持人。客观总结双方核心论据，评估论证严密性，给出综合裁决和投资建议。请用中文回答，Markdown格式，用表格对比。',
    quiz: (topic, difficulty, count) => '请生成' + count + '道关于 + topic + 的选择题，难度 + difficulty + 。每题4个选项(A/B/C/D)，一个正确答案。JSON格式返回。',
    generateOutline: (topic) => '请为 + topic + 设计结构化教学大纲，3-5个模块，JSON格式返回。',
    generateContent: (moduleTitle, topics) => '请为模块 + moduleTitle + 生成详细教学内容。覆盖：' + topics + '。Markdown格式。',
};
// --- /api/chat ---
app.post('/api/chat', async (req, res) => {
    try {
        const { messages, mode } = req.body;
        if (!messages?.length) return res.status(400).json({ error: 'messages 不能为空' });
        const chatMessages = [{ role: 'system', content: PROMPTS.chat(mode) }, ...messages];
        let assistantContent = await callMiMo(chatMessages);
        const toolCallResults = [];
        let maxRounds = 5;
        while (maxRounds-- > 0) {
            const tc = parseToolCall(assistantContent);
            if (!tc) break;
            let result;
            try { result = await executeTool(tc.toolName, tc.args); } catch (err) { result = { error: err.message }; }
            toolCallResults.push({ name: tc.toolName, args: tc.args, result });
            chatMessages.push({ role: 'assistant', content: assistantContent });
            chatMessages.push({ role: 'user', content: '工具 ' + tc.toolName + ' 结果：\n' + JSON.stringify(result) + '\n请基于数据回答，不要再调用工具。' });
            assistantContent = await callMiMo(chatMessages);
            if (!assistantContent.includes('<' + 'tool_call')) break;
        }
        assistantContent = assistantContent.replace(/<tool_call>[\s\S]*?<\/tool_call>/g, '').trim();
        res.json({ content: assistantContent, toolCalls: toolCallResults });
    } catch (err) { res.status(500).json({ error: err.message || '服务器内部错误' }); }
});
// --- /api/debate ---
app.post('/api/debate', async (req, res) => {
    try {
        const { topic } = req.body;
        if (!topic) return res.status(400).json({ error: 'topic 不能为空' });
        const bull = await callMiMo([{ role: 'system', content: PROMPTS.bull }, { role: 'user', content: topic }], 0.8);
        const bear = await callMiMo([{ role: 'system', content: PROMPTS.bear }, { role: 'user', content: topic }], 0.8);
        const mod = await callMiMo([{ role: 'system', content: PROMPTS.moderator }, { role: 'user', content: '话题：' + topic + '\n\n多头观点：\n' + bull + '\n\n空头观点：\n' + bear }], 0.5);
        res.json({ topic, bull, bear, moderator: mod });
    } catch (err) { res.status(500).json({ error: err.message }); }
});
// --- /api/quiz ---
app.post('/api/quiz', async (req, res) => {
    try {
        const { topic, difficulty = '基础', count = 5 } = req.body;
        if (!topic) return res.status(400).json({ error: 'topic 不能为空' });
        const content = await callMiMo([{ role: 'system', content: PROMPTS.quiz(topic, difficulty, count) }, { role: 'user', content: '请生成题目。' }], 0.7, 4096);
        try { const jm = content.match(/\{[\s\S]*\}/); res.json(JSON.parse(jm ? jm[0] : content)); } catch { res.status(500).json({ error: '测验生成失败', raw: content }); }
    } catch (err) { res.status(500).json({ error: err.message }); }
});
// --- /api/generate ---
app.post('/api/generate', async (req, res) => {
    try {
        const { topic } = req.body;
        if (!topic) return res.status(400).json({ error: 'topic 不能为空' });
        const oc = await callMiMo([{ role: 'system', content: PROMPTS.generateOutline(topic) }, { role: 'user', content: '请设计教学大纲。' }], 0.7, 4096);
        let outline;
        try { outline = JSON.parse((oc.match(/\{[\s\S]*\}/) || [oc])[0]); } catch { return res.status(500).json({ error: '大纲生成失败', raw: oc }); }
        const contents = [];
        for (const mod of (outline.modules || []).slice(0, 5)) {
            const topics = mod.topics?.map(t => t.title).join('、') || mod.title;
            const c = await callMiMo([{ role: 'system', content: PROMPTS.generateContent(mod.title, topics) }, { role: 'user', content: '请生成教学内容。' }], 0.7, 4096);
            contents.push({ moduleId: mod.id, title: mod.title, difficulty: mod.difficulty, content: c });
        }
        res.json({ outline, contents });
    } catch (err) { res.status(500).json({ error: err.message }); }
});
// --- /api/tts ---
app.post('/api/tts', (req, res) => {
    const { text } = req.body;
    if (!text) return res.status(400).json({ error: 'text 不能为空' });
    res.json({ fallback: true, text, message: '使用浏览器内置语音合成' });
});
// --- Health check ---
app.get('/api/health', (req, res) => res.json({ status: 'ok', timestamp: new Date().toISOString() }));
app.listen(PORT, () => { console.log('SmartBank Agent API running on port ' + PORT); });

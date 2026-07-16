// Cloudflare Pages Advanced Mode Worker - SmartBank Agent API
// 借鉴 OpenMAIC 多Agent课堂 + 互动仿真 + 测验 + PBL + 内容生成 + TTS
// 使用 MiMo API + Tushare + World Bank

const CORS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

// ─── JWT 工具函数 ─────────────────────────────────────────────────
function base64UrlEncode(data) {
    return btoa(data).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function base64UrlDecode(str) {
    str = str.replace(/-/g, '+').replace(/_/g, '/');
    while (str.length % 4) str += '=';
    return atob(str);
}
async function createJWT(payload, secret) {
    const header = { alg: 'HS256', typ: 'JWT' };
    const now = Math.floor(Date.now() / 1000);
    const tokenPayload = { ...payload, iat: now, exp: now + 7 * 24 * 3600 };
    const headerB64 = base64UrlEncode(JSON.stringify(header));
    const payloadB64 = base64UrlEncode(JSON.stringify(tokenPayload));
    const message = headerB64 + '.' + payloadB64;
    const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
    const signature = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(message));
    const signatureB64 = base64UrlEncode(String.fromCharCode(...new Uint8Array(signature)));
    return message + '.' + signatureB64;
}
async function verifyJWT(token, secret) {
    try {
        const parts = token.split('.');
        if (parts.length !== 3) return null;
        const [headerB64, payloadB64, signatureB64] = parts;
        const message = headerB64 + '.' + payloadB64;
        const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['verify']);
        const signature = Uint8Array.from(base64UrlDecode(signatureB64), c => c.charCodeAt(0));
        const isValid = await crypto.subtle.verify('HMAC', key, signature, new TextEncoder().encode(message));
        if (!isValid) return null;
        const payload = JSON.parse(base64UrlDecode(payloadB64));
        if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) return null;
        return payload;
    } catch { return null; }
}
async function getUserId(request, secret) {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader?.startsWith('Bearer ')) return null;
    const token = authHeader.substring(7);
    const payload = await verifyJWT(token, secret);
    return payload?.sub || null;
}

const MIMO_API_URL = 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions';
const MIMO_MODEL = 'mimo-v2.5-pro';
const BAILIAN_API_URL = 'https://ws-paxy280v9746pda1.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions';
const BAILIAN_MODEL = 'qwen-plus';
const LOCAL_API_URL = 'http://127.0.0.1:8000/v1/chat/completions';
const LOCAL_MODEL = 'Qwen2.5-7B-Instruct-4bit';
const LOCAL_API_KEY = 'omlx-local-key';
const AMAP_API_KEY = '63f93d2223f744affebade9ef7982732';

// Tool call tag builders (avoid literal tags in source)
const TC_OPEN = '<tool_call>';
const TC_CLOSE = '</tool_call>';
function fnTag(name) { return '<function=' + name + '>'; }
function pmTag(name) { return '<parameter=' + name + '>'; }
const FN_CLOSE = '</' + 'function>';
const PM_CLOSE = '</' + 'parameter>';

const PROMPTS = {
    chat: (mode) => {
        const bmad = {
            'bmad-analyst': '\n你当前扮演 BMAD 方法论中的**需求分析师(Analyst)**角色。帮助学生分析金融业务需求，输出用户故事、需求文档和验收标准。',
            'bmad-pm': '\n你当前扮演 BMAD 方法论中的**产品经理(PM)**角色。帮助学生制定产品路线图、优先级排序、PRD文档编写。',
            'bmad-architect': '\n你当前扮演 BMAD 方法论中的**架构师(Architect)**角色。帮助学生设计系统架构、技术选型、API设计、数据库设计。',
            'bmad-dev': '\n你当前扮演 BMAD 方法论中的**开发者(Developer)**角色。帮助学生编写代码、调试问题、实现功能模块。',
            'bmad-qa': '\n你当前扮演 BMAD 方法论中的**质量保障(QA)**角色。帮助学生设计测试用例、代码审查、质量评估。',
        };
        return '你是 SmartBank Agent，由四川农业大学智慧银行实验室开发的金融实验教学智能体。\n你的职责是帮助学生理解金融概念、分析市场数据、完成金融实验任务。\n\n本智能体基于《智慧银行实验教程——AI驱动的金融科技实践》教材，采用MCP+Skill+BMAD三位一体架构：\n- MCP协议（Model Context Protocol）：通过JSON-RPC 2.0连接20+金融数据源\n- Skill体系：167个专业技能分20个分类，涵盖金融分析、文档生成、数据可视化等\n- BMAD方法论：Analyst→PM→Architect→Dev→QA五角色全流程项目指导\n' + (bmad[mode] || '') + '\n\n当需要查询实时数据时，你必须在回复中使用以下格式调用工具：\n\n' + TC_OPEN + '\n' + fnTag('工具名') + '\n' + pmTag('参数名') + '参数值' + PM_CLOSE + '\n' + FN_CLOSE + '\n' + TC_CLOSE + '\n\n【Tushare金融数据组】\n1. query_stock - 查询A股个股日线行情（参数：ts_code如600519.SH，可选start_date/end_date为YYYYMMDD）\n2. query_stock_basic - 根据名称搜索股票代码（参数：name如\"贵州茅台\"）\n3. query_stock_info - 查询股票基本信息（参数：ts_code或name）\n4. query_index - 查询指数行情（参数：ts_code如000001.SH）\n5. query_fund_flow - 查询沪深港通资金流向（参数：可选start_date/end_date）\n6. query_financial - 查询上市公司财务数据（参数：ts_code, type如income/balancesheet/cashflow）\n7. query_stock_basic_info - 查询个股基本信息含行业/市值（参数：ts_code）\n8. query_top_holders - 查询前十大股东（参数：ts_code, 可选quarter如20241231）\n9. query_trade_cal - 查询交易日历（参数：可选start_date/end_date/exchange）\n\n【世界银行宏观经济组】\n10. query_macro_gdp - 查询GDP数据（参数：country如CN/US/JP）\n11. query_macro_indicator - 查询宏观指标（参数：country, indicator如FP.CPI.TOTL.ZG）\n12. query_macro_compare - 多国指标对比（参数：countries如CN,US,JP, indicator）\n13. query_macro_findex - 查询金融账户拥有率等Findex数据（参数：country, indicator如FX.OWN.TOTL.ZS）\n\n【高德地图MCP组】\n14. search_bank_branch - 搜索银行网点（参数：city如成都, keywords如工商银行）\n15. search_nearby - 搜索附近金融机构（参数：location如104.06,30.67, radius, keywords）\n\n【图表可视化组】\n16. generate_chart - 生成金融图表（参数：type如line/bar/pie, title, data为JSON数组）\n\n【Skill知识库】本智能体还支持以下Skill能力（需要时主动介绍）：\n- 金融数据分析Skill：调用Tushare/iFinD/World Bank进行投研分析\n- 学术写作Skill：LaTeX论文排版、参考文献管理\n- 演示文稿Skill：PPT/PDF/海报自动生成\n- 可视化Skill：统计图表/因果图/网络图/思维导图\n- 文档处理Skill：Word/Excel/PDF自动化\n- 研究方法Skill：系统文献综述、计量经济学分析\n\n常见股票代码速查：贵州茅台=600519.SH, 平安银行=000001.SZ, 招商银行=600036.SH, 宁德时代=300750.SZ, 比亚迪=002594.SZ, 上证指数=000001.SH, 沪深300=000300.SH, 创业板指=399006.SZ\n\n规则：\n- 每次只调用一个工具，等待结果返回后再决定下一步\n- 数据展示时使用表格格式，分析要结合金融理论（如CAPM、有效市场假说、信息不对称理论等）\n- 涉及宏观数据时引用世界银行、OECD等权威来源\n- 涉及银行业务时结合《巴塞尔协议》等监管框架\n- 请用中文回答，专业术语附英文原文';
    },
    bull: '你是一位资深的**多头分析师**（看涨派）。当用户提出一个金融话题时，你需要：\n1. 从增长潜力、政策利好、竞争优势、估值合理性等角度分析\n2. 提供3-5个核心看多论据，每个论据配数据支撑\n3. 给出目标价或预期涨幅\n4. 风格：自信但不盲目，数据驱动\n请用中文回答，使用 Markdown 格式。',
    bear: '你是一位资深的**空头分析师**（看跌派）。当用户提出一个金融话题时，你需要：\n1. 从风险隐患、利空因素、估值泡沫、竞争压力等角度分析\n2. 提供3-5个核心看空论据，每个论据配数据支撑\n3. 给出风险预警和建议规避理由\n4. 风格：理性审慎，重视风险\n请用中文回答，使用 Markdown 格式。',
    moderator: '你是一位金融辩论主持人。你将收到多头和空头分析师的观点，你需要：\n1. 客观总结双方核心论据（各列出3点）\n2. 评估双方论证的逻辑严密性和数据支撑力度\n3. 给出综合裁决（偏多/偏空/中性），附理由\n4. 给出投资建议（买入/持有/观望/减持）\n5. 提醒关键风险点\n请用中文回答，使用 Markdown 格式，用表格对比双方观点。',
    quiz: (topic, difficulty, count) => '你是一位金融教育专家。请生成' + count + '道关于"' + topic + '"的选择题，难度为"' + difficulty + '"。\n要求：\n- 每题4个选项（A/B/C/D），只有一个正确答案\n- 题目贴近金融实务\n- ' + (difficulty === '基础' ? '考察基本概念和定义' : difficulty === '进阶' ? '考察分析和计算能力' : '考察综合判断和案例分析') + '\n请严格按JSON格式返回：{"questions":[{"id":"q1","question":"题目","options":["A. 选项1","B. 选项2","C. 选项3","D. 选项4"],"answer":"A","explanation":"解析"}]}',
    generateOutline: (topic) => '你是一位金融教育课程设计师。请为"' + topic + '"设计结构化教学大纲。\n要求：3-5个模块，每模块2-3个子知识点，标注难度。\n请严格按JSON格式返回：{"title":"课程标题","modules":[{"id":"m1","title":"模块标题","difficulty":"基础","topics":[{"id":"t1","title":"知识点"}]}]}',
    generateContent: (moduleTitle, topics) => '你是一位金融教育专家。请为模块"' + moduleTitle + '"生成详细教学内容。\n覆盖知识点：' + topics + '\n要求：每知识点200-300字+案例+思考题，Markdown格式，通俗易懂。',
};

async function callMiMo(messages, env, temperature, maxTokens, modelId) {
    let apiUrl, modelName, apiKey, modelLabel;
    if (modelId === 'local') {
        apiUrl = LOCAL_API_URL;
        modelName = LOCAL_MODEL;
        apiKey = LOCAL_API_KEY;
        modelLabel = '本地模型';
    } else if (modelId === 'bailian' && env.BAILIAN_API_KEY) {
        apiUrl = BAILIAN_API_URL;
        modelName = BAILIAN_MODEL;
        apiKey = env.BAILIAN_API_KEY;
        modelLabel = '百炼';
    } else {
        apiUrl = MIMO_API_URL;
        modelName = MIMO_MODEL;
        apiKey = env.MIMO_API_KEY;
        modelLabel = 'MiMo';
    }
    const resp = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + apiKey },
        body: JSON.stringify({ model: modelName, messages, temperature: temperature || 0.7, max_tokens: maxTokens || 2048 }),
    });
    if (!resp.ok) throw new Error(modelLabel + ' API error: ' + resp.status);
    const data = await resp.json();
    const c = data.choices?.[0]?.message?.content || '';
    if (!c) throw new Error('AI 未返回有效响应');
    return c;
}

async function callTushare(apiName, params, fields, env) {
    const resp = await fetch('https://api.tushare.pro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_name: apiName, token: env.TUSHARE_TOKEN, params, fields }),
    });
    const data = await resp.json();
    if (data.code !== 0) throw new Error('Tushare: ' + data.msg);
    return data;
}

function parseToolCall(text) {
    const match = text.match(/<tool_call>[\s\S]*?<function=(\w+)>([\s\S]*?)<\/function>[\s\S]*?<\/tool_call>/);
    if (!match) return null;
    const args = {};
    const re = /<parameter=(\w+)>([\s\S]*?)<\/parameter>/g;
    let m;
    while ((m = re.exec(match[2])) !== null) args[m[1]] = m[2].trim();
    return { toolName: match[1], args };
}

async function executeTool(name, args, env) {
    const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const thirtyAgo = (() => { const d = new Date(); d.setDate(d.getDate() - 30); return d.toISOString().slice(0, 10).replace(/-/g, ''); })();
    switch (name) {
        case 'query_stock': {
            const data = await callTushare('daily', { ts_code: args.ts_code, start_date: args.start_date || thirtyAgo, end_date: args.end_date || today }, 'ts_code,trade_date,open,high,low,close,vol,amount', env);
            return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) };
        }
        case 'query_stock_basic': {
            const data = await callTushare('stock_basic', { list_status: 'L' }, 'ts_code,name,industry,market,list_date', env);
            const filtered = (data.data?.items || []).filter(item => String(item[1] || '').includes(args.name));
            return { count: filtered.length, items: filtered.slice(0, 10) };
        }
        case 'query_index': {
            const data = await callTushare('index_daily', { ts_code: args.ts_code, start_date: args.start_date || thirtyAgo, end_date: args.end_date || today }, 'ts_code,trade_date,open,high,low,close,vol,amount', env);
            return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) };
        }
        case 'query_macro_gdp': {
            const endYear = new Date().getFullYear();
            const resp = await fetch('https://api.worldbank.org/v2/country/' + args.country + '/indicator/NY.GDP.MKTP.CD?format=json&date=' + (endYear - 5) + ':' + endYear);
            const json = await resp.json();
            return { country: args.country, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) };
        }
        case 'query_macro_indicator': {
            const endYear = new Date().getFullYear();
            const ind = args.indicator.includes('.') ? args.indicator : args.indicator.replace(/_/g, '.');
            const resp = await fetch('https://api.worldbank.org/v2/country/' + args.country + '/indicator/' + ind + '?format=json&date=' + (endYear - 5) + ':' + endYear);
            const json = await resp.json();
            return { country: args.country, indicator: ind, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) };
        }
        // ── Tushare扩展工具 ──
        case 'query_stock_info': {
            const q = args.name || args.ts_code;
            const data = await callTushare('stock_basic', { list_status: 'L' }, 'ts_code,name,industry,market,list_date', env);
            const found = (data.data?.items || []).filter(item => String(item[0]) === q || String(item[1]).includes(q));
            return { count: found.length, items: found.slice(0, 5) };
        }
        case 'query_fund_flow': {
            const data = await callTushare('moneyflow_hsgt', { start_date: args.start_date || thirtyAgo, end_date: args.end_date || today }, 'trade_date,ggt_ss,ggt_sz,hgt,sgt,north_money,south_money', env);
            return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 15) };
        }
        case 'query_financial': {
            const typeMap = { income: 'income', balancesheet: 'balancesheet', cashflow: 'cashflow' };
            const apiName = typeMap[args.type] || 'income';
            const fieldMap = {
                income: 'ts_code,ann_date,revenue,n_income,total_profit,operate_profit',
                balancesheet: 'ts_code,ann_date,total_assets,total_liab,total_hldr_eqy_exc_min_int',
                cashflow: 'ts_code,ann_date,n_cashflow_act,n_cashflow_inv_act,n_cash_flows_fnc_act',
            };
            const data = await callTushare(apiName, { ts_code: args.ts_code }, fieldMap[apiName], env);
            return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 5) };
        }
        case 'query_stock_basic_info': {
            const data = await callTushare('daily_basic', { ts_code: args.ts_code }, 'ts_code,trade_date,pe,pb,ps,total_mv,circ_mv,turnover_rate', env);
            return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 5) };
        }
        case 'query_top_holders': {
            const data = await callTushare('top10_holders', { ts_code: args.ts_code, ...(args.quarter ? { end_date: args.quarter } : {}) }, 'ts_code,ann_date,end_date,holder_name,hold_amount,hold_ratio', env);
            return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) };
        }
        case 'query_trade_cal': {
            const data = await callTushare('trade_cal', { start_date: args.start_date || '20250101', end_date: args.end_date || '20251231', exchange: args.exchange || 'SSE' }, 'exchange,cal_date,is_open', env);
            const openDays = (data.data?.items || []).filter(item => item[2] === '1');
            return { total: data.data?.items?.length || 0, trading_days: openDays.length, items: openDays.slice(0, 10) };
        }
        // ── 世界银行扩展工具 ──
        case 'query_macro_compare': {
            const countries = (args.countries || 'CN,US').split(',').map(s => s.trim());
            const results = [];
            for (const c of countries.slice(0, 5)) {
                const resp = await fetch('https://api.worldbank.org/v2/country/' + c + '/indicator/' + args.indicator + '?format=json&date=2019:2024');
                const json = await resp.json();
                results.push({ country: c, data: (json[1] || []).map(r => ({ year: r.date, value: r.value, country_name: r.country?.value })) });
            }
            return { indicator: args.indicator, comparison: results };
        }
        case 'query_macro_findex': {
            const endYear = new Date().getFullYear();
            const ind = args.indicator || 'FX.OWN.TOTL.ZS';
            const resp = await fetch('https://api.worldbank.org/v2/country/' + (args.country || 'CN') + '/indicator/' + ind + '?format=json&date=' + (endYear - 8) + ':' + endYear);
            const json = await resp.json();
            return { country: args.country, indicator: ind, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) };
        }
        // ── 高德地图工具 ──
        case 'search_bank_branch': {
            const resp = await fetch('https://restapi.amap.com/v3/place/text?key=' + AMAP_API_KEY + '&keywords=' + encodeURIComponent(args.keywords || '银行') + '&city=' + encodeURIComponent(args.city || '成都') + '&types=160100&offset=10&page=1');
            const json = await resp.json();
            return { count: json.count || 0, pois: (json.pois || []).map(p => ({ name: p.name, address: p.address, location: p.location, tel: p.tel })) };
        }
        case 'search_nearby': {
            const resp = await fetch('https://restapi.amap.com/v3/place/around?key=' + AMAP_API_KEY + '&location=' + (args.location || '104.06,30.67') + '&keywords=' + encodeURIComponent(args.keywords || '银行') + '&radius=' + (args.radius || '2000') + '&offset=10');
            const json = await resp.json();
            return { count: json.count || 0, pois: (json.pois || []).map(p => ({ name: p.name, address: p.address, location: p.location, distance: p.distance })) };
        }
        // ── 图表生成工具 ──
        case 'generate_chart': {
            try {
                const chartData = typeof args.data === 'string' ? JSON.parse(args.data) : args.data;
                const chartConfig = {
                    type: args.type || 'bar',
                    title: args.title || '金融数据图表',
                    data: chartData,
                    width: args.width || 600,
                    height: args.height || 400,
                };
                const chartResp = await fetch('https://mcp-server-chart.vercel.app/generate_' + (args.type || 'bar') + '_chart', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(chartConfig),
                });
                if (chartResp.ok) {
                    const chartJson = await chartResp.json();
                    return { chart_url: chartJson.url || chartJson.imageUrl, config: chartConfig };
                }
                return { config: chartConfig, note: '图表生成服务暂时不可用，请使用文字描述数据' };
            } catch (e) { return { error: '图表生成失败: ' + e.message }; }
        }
        default: throw new Error('Unknown tool: ' + name);
    }
}

function jsonResponse(data, status) {
    return new Response(JSON.stringify(data), { status: status || 200, headers: { 'Content-Type': 'application/json', ...CORS } });
}

// ─── /api/models ────────────────────────────────────────────────────────────
function handleModelsRequest(request, env) {
    const method = request.method;
    if (method === 'GET') {
        return jsonResponse({
            current: 'mimo',
            models: [
                { id: 'mimo', name: 'MiMo', enabled: !!env.MIMO_API_KEY, priority: 1, current: true },
                { id: 'bailian', name: '百炼', enabled: !!env.BAILIAN_API_KEY, priority: 2, current: false },
                { id: 'local', name: '本地模型', enabled: true, priority: 3, current: false },
            ]
        });
    }
    if (method === 'POST') {
        return request.json().then(({ model }) => {
            if (!model) return jsonResponse({ error: '缺少model参数' }, 400);
            const nameMap = { mimo: 'MiMo', bailian: '百炼', local: '本地模型' };
            return jsonResponse({ success: true, current: model, name: nameMap[model] || model });
        }).catch(() => jsonResponse({ error: '请求格式错误' }, 400));
    }
    return jsonResponse({ error: 'Method not allowed' }, 405);
}

// ─── /api/models/switch ─────────────────────────────────────────────────────
async function handleModelSwitch(request, env) {
    const { model } = await request.json();
    if (!model) return jsonResponse({ error: '缺少model参数' }, 400);
    const nameMap = { mimo: 'MiMo', bailian: '百炼', local: '本地模型' };
    return jsonResponse({ success: true, current: model, name: nameMap[model] || model });
}

// ─── /api/models/test ──────────────────────────────────────────────────────
async function handleModelTest(request, env) {
    const { model } = await request.json();
    const modelId = model || 'mimo';
    const start = Date.now();
    try {
        const testMsg = [{ role: 'user', content: '你好' }];
        let apiUrl, modelName, apiKey, modelLabel;
        if (modelId === 'local') {
            apiUrl = LOCAL_API_URL;
            modelName = LOCAL_MODEL;
            apiKey = LOCAL_API_KEY;
            modelLabel = '本地模型';
        } else if (modelId === 'bailian' && env.BAILIAN_API_KEY) {
            apiUrl = BAILIAN_API_URL;
            modelName = BAILIAN_MODEL;
            apiKey = env.BAILIAN_API_KEY;
            modelLabel = '百炼';
        } else {
            apiUrl = MIMO_API_URL;
            modelName = MIMO_MODEL;
            apiKey = env.MIMO_API_KEY;
            modelLabel = 'MiMo';
        }
        const resp = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + apiKey },
            body: JSON.stringify({ model: modelName, messages: testMsg, max_tokens: 10 }),
        });
        const latency = Date.now() - start;
        if (resp.ok) return jsonResponse({ success: true, model: modelLabel, latency: latency + 'ms' });
        return jsonResponse({ success: false, model: modelLabel, error: 'HTTP ' + resp.status });
    } catch (e) {
        const nameMap = { mimo: 'MiMo', bailian: '百炼', local: '本地模型' };
        return jsonResponse({ success: false, model: nameMap[modelId] || modelId, error: e.message });
    }
}

// ─── /api/chat ───────────────────────────────────────────────────────────────
async function handleChatRequest(request, env) {
    const { messages, mode, model } = await request.json();
    if (!messages?.length) return jsonResponse({ error: 'messages 不能为空' }, 400);
    const chatMessages = [{ role: 'system', content: PROMPTS.chat(mode) }, ...messages];
    let assistantContent = await callMiMo(chatMessages, env, undefined, undefined, model);
    const toolCallResults = [];
    let maxRounds = 5;
    while (maxRounds-- > 0) {
        const tc = parseToolCall(assistantContent);
        if (!tc) break;
        let result;
        try { result = await executeTool(tc.toolName, tc.args, env); }
        catch (err) { result = { error: err.message }; }
        toolCallResults.push({ name: tc.toolName, args: tc.args, result });
        chatMessages.push({ role: 'assistant', content: assistantContent });
        chatMessages.push({ role: 'user', content: '工具 ' + tc.toolName + ' 结果：\n' + JSON.stringify(result) + '\n请基于数据回答，不要再调用工具。' });
        assistantContent = await callMiMo(chatMessages, env);
        if (!assistantContent.includes(TC_OPEN)) break;
    }
    assistantContent = assistantContent.replace(/<tool_call>[\s\S]*?<\/tool_call>/g, '').trim();
    return jsonResponse({ content: assistantContent, toolCalls: toolCallResults });
}

// ─── /api/debate ─────────────────────────────────────────────────────────────
async function handleDebateRequest(request, env) {
    const { topic } = await request.json();
    if (!topic) return jsonResponse({ error: 'topic 不能为空' }, 400);
    const bull = await callMiMo([{ role: 'system', content: PROMPTS.bull }, { role: 'user', content: topic }], env, 0.8);
    const bear = await callMiMo([{ role: 'system', content: PROMPTS.bear }, { role: 'user', content: topic }], env, 0.8);
    const mod = await callMiMo([{ role: 'system', content: PROMPTS.moderator }, { role: 'user', content: '话题：' + topic + '\n\n多头观点：\n' + bull + '\n\n空头观点：\n' + bear }], env, 0.5);
    return jsonResponse({ topic, bull, bear, moderator: mod });
}

// ─── /api/quiz ───────────────────────────────────────────────────────────────
async function handleQuizRequest(request, env) {
    const { topic, difficulty = '基础', count = 5 } = await request.json();
    if (!topic) return jsonResponse({ error: 'topic 不能为空' }, 400);
    const content = await callMiMo([{ role: 'system', content: PROMPTS.quiz(topic, difficulty, count) }, { role: 'user', content: '请生成题目。' }], env, 0.7, 4096);
    try {
        const jm = content.match(/\{[\s\S]*\}/);
        return jsonResponse(JSON.parse(jm ? jm[0] : content));
    } catch { return jsonResponse({ error: '测验生成失败', raw: content }, 500); }
}

// ─── /api/generate ───────────────────────────────────────────────────────────
async function handleGenerateRequest(request, env) {
    const { topic } = await request.json();
    if (!topic) return jsonResponse({ error: 'topic 不能为空' }, 400);
    const oc = await callMiMo([{ role: 'system', content: PROMPTS.generateOutline(topic) }, { role: 'user', content: '请设计教学大纲。' }], env, 0.7, 4096);
    let outline;
    try { outline = JSON.parse((oc.match(/\{[\s\S]*\}/) || [oc])[0]); }
    catch { return jsonResponse({ error: '大纲生成失败', raw: oc }, 500); }
    const contents = [];
    for (const mod of (outline.modules || []).slice(0, 5)) {
        const topics = mod.topics?.map(t => t.title).join('、') || mod.title;
        const c = await callMiMo([{ role: 'system', content: PROMPTS.generateContent(mod.title, topics) }, { role: 'user', content: '请生成教学内容。' }], env, 0.7, 4096);
        contents.push({ moduleId: mod.id, title: mod.title, difficulty: mod.difficulty, content: c });
    }
    return jsonResponse({ outline, contents });
}

// ─── /api/tts ────────────────────────────────────────────────────────────────
async function handleTtsRequest(request, env) {
    const { text } = await request.json();
    if (!text) return jsonResponse({ error: 'text 不能为空' }, 400);
    return jsonResponse({ fallback: true, text, message: '使用浏览器内置语音合成' });
}

// ─── Router ──────────────────────────────────────────────────────────────────
export default {
    async fetch(request, env) {
        const url = new URL(request.url);
        if (request.method === 'OPTIONS') return new Response(null, { headers: CORS });
        const routes = {
            '/api/chat': handleChatRequest,
            '/api/models': handleModelsRequest,
            '/api/models/switch': handleModelSwitch,
            '/api/models/test': handleModelTest,
            '/api/debate': handleDebateRequest,
            '/api/quiz': handleQuizRequest,
            '/api/generate': handleGenerateRequest,
            '/api/tts': handleTtsRequest,
        };
        const handler = routes[url.pathname];
        if (handler) {
            if (!url.pathname.startsWith('/api/models') && request.method !== 'POST') return jsonResponse({ error: 'Method not allowed' }, 405);
            try { return await handler(request, env); }
            catch (err) { return jsonResponse({ error: err.message || '服务器内部错误' }, 500); }
        }
        if (env.ASSETS) return env.ASSETS.fetch(request);
        return new Response('Not Found', { status: 404 });
    },
};

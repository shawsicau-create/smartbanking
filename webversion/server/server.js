import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// ============ 配置 ============
const MIMO_API_URL = 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions';
const MIMO_MODEL = 'mimo-v2.5-pro';
const AMAP_API_KEY = '63f93d2223f744affebade9ef7982732';

// 同花顺 Authorization Token
const HEXIN_AUTH = 'eyJraWQiOiJtY3AtYXBpIiwidWlkIjoiODE2MDUzMDE2IiwiYWxnIjoiUlNBLU9BRVAtMjU2IiwiZW5jIjoiQTI1NkdDTSJ9.KtqPG6B9QChrXsWD2Fwc_o6ESx7onPclJLV3Ae2P2ywdxle3qBZekY3s7UdjEfIzey8SK8_-rYzrTwIxjBQPTKwdPCZJiPJyXTU30f3thyzeyJzFIHLkl9CYRCmL3tJO-XaAyZPhobaA1YJxf1dwjele_qVMkNuwlyh-OQkgvhhe2LKoB-qC00IfkFjSfnk8Haj6GguQbgZxmpHmtjwqikHKDExGqHwyuD0NAI2xE7KCUhEU2_R9jlgtam8KFrP1EKLopgXoi1vLnPAKOuWIjpBbf3ssiq8skvEOo-1tCKXbBkAl3KA2gINfiAUQiGQkHYelk8K7OLGXFM26tE6BSw.PCIeejE9EP506onn.KcJz5gKDLa4dUcb9_kRypPwcUg19p9xQCXtD3YT0minWofhcPilz3zHXHJfdcLo77arm1GrqwWxDeOoLsd_1fotHRpKairs8x_92SR6Xr6GrplCQ5OmSRG0rWEq78RhgBxaPZ3mHx4BZsaX-QWcwdJYs5gIFdDYS1jIfz8TZnAUQexzh9BvGIolYKcC-acqV0LclsSeG2XzM7OdHocKjAhtXJFgbuqf-6STc_UlyTswqiDF91lmE1Mc2Tz51EE9KClLL-oRlhq1Y8sAMhHr4bMrobjNrI1YqwaSIZBStHA94GYlfKsXowUyOz4Wb65qETn_eIo5LDyJEmJzGLvdrFWzKdzplqDmGJsTcWXLE0J2ppRNo-MM_DmNKgUcQmWwu4NMw5_ujCUPIbx_NnchwcClnKLQDfTMAOGOxUdqA-3XNACkHF4143E9MZAcbpVNEoCbAeA.m70gN5uS8LDeAf3LrwS_zg';
const TUSHARE_TOKEN = process.env.TUSHARE_TOKEN || '99882e4e66b875e8d7776fed9e84e14a949447d9cde3d2fbeac443ba';

// ============ 内存存储（对话历史） ============
const chatHistoryStore = new Map(); // session_id -> [{id, title, mode, messages, created_at, updated_at}]
let historyIdCounter = 1;

// ============ AnySearch 搜索服务 ============
const SEARCH_API = 'https://api.anysearch.com/v1/search';
const EXTRACT_API = 'https://api.anysearch.com/v1/extract';

async function anySearch(query, maxResults = 10) {
    try {
        const resp = await fetch(SEARCH_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'User-Agent': 'SmartBank-Agent/1.0' },
            body: JSON.stringify({ query, max_results: maxResults }),
            signal: AbortSignal.timeout(15000),
        });
        if (!resp.ok) throw new Error(`Search API error: ${resp.status}`);
        const raw = await resp.json();
        const data = raw?.data || raw;
        const items = (data?.results || data?.items || (Array.isArray(data) ? data : []));
        return {
            query,
            results: items.filter(i => typeof i === 'object' && i !== null).map(i => ({
                title: String(i.title || i.name || '').trim(),
                url: String(i.url || i.link || '').trim(),
                snippet: String(i.description || i.snippet || '').trim(),
            })).filter(i => i.title || i.url),
            error: null,
        };
    } catch (error) {
        return { query, results: [], error: error.message };
    }
}

async function anyExtract(url) {
    try {
        const resp = await fetch(EXTRACT_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'User-Agent': 'SmartBank-Agent/1.0' },
            body: JSON.stringify({ url }),
            signal: AbortSignal.timeout(15000),
        });
        if (!resp.ok) throw new Error(`Extract API error: ${resp.status}`);
        const data = await resp.json();
        return { url, content: data.content || data.data?.content || '', error: null };
    } catch (error) {
        return { url, content: '', error: error.message };
    }
}

async function batchSearch(queries) {
    const results = await Promise.all(queries.map(q => anySearch(q.query, q.max_results || 5)));
    return { results, error: null };
}

// ============ 同花顺 iFinD MCP 服务 ============
async function callHexinMcp(toolName, args) {
    const servers = {
        'hexin_stock': 'hexin-ifind-ds-stock-mcp',
        'hexin_fund': 'hexin-ifind-ds-fund-mcp',
        'hexin_edb': 'hexin-ifind-ds-edb-mcp',
        'hexin_news': 'hexin-ifind-ds-news-mcp',
        'hexin_bond': 'hexin-ifind-ds-bond-mcp',
        'hexin_global_stock': 'hexin-ifind-ds-global-stock-mcp',
        'hexin_index': 'hexin-ifind-ds-index-mcp',
    };
    const serverName = servers[toolName];
    if (!serverName) throw new Error(`Unknown hexin server: ${toolName}`);

    const url = `https://api-mcp.51ifind.com:8643/ds-mcp-servers/${serverName}`;
    try {
        const resp = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': HEXIN_AUTH,
            },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'tools/call',
                params: { name: args.tool_name, arguments: args.arguments || {} },
                id: 1,
            }),
            signal: AbortSignal.timeout(30000),
        });
        if (!resp.ok) throw new Error(`Hexin MCP error: ${resp.status}`);
        const data = await resp.json();
        return data.result?.content?.[0]?.text ? JSON.parse(data.result.content[0].text) : data;
    } catch (error) {
        return { error: error.message };
    }
}

// ============ World Bank Data360 ============
async function worldbankData360(toolName, args) {
    const url = 'https://maimcpext.worldbank.org/ext/data360/mcp';
    try {
        const resp = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'tools/call',
                params: { name: toolName, arguments: args },
                id: 1,
            }),
            signal: AbortSignal.timeout(30000),
        });
        if (!resp.ok) throw new Error(`WorldBank Data360 error: ${resp.status}`);
        const data = await resp.json();
        return data.result?.content?.[0]?.text ? JSON.parse(data.result.content[0].text) : data;
    } catch (error) {
        return { error: error.message };
    }
}

// ============ OpenEcon Data ============
async function openeconData(toolName, args) {
    const url = 'https://data.openecon.ai/mcp';
    try {
        const resp = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'tools/call',
                params: { name: toolName, arguments: args },
                id: 1,
            }),
            signal: AbortSignal.timeout(30000),
        });
        if (!resp.ok) throw new Error(`OpenEcon error: ${resp.status}`);
        const data = await resp.json();
        return data.result?.content?.[0]?.text ? JSON.parse(data.result.content[0].text) : data;
    } catch (error) {
        return { error: error.message };
    }
}

// ============ Finance MCP ============
async function financeMcp(toolName, args) {
    const url = 'https://finvestai.top/mcp';
    try {
        const resp = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Tushare-Token': TUSHARE_TOKEN,
            },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'tools/call',
                params: { name: toolName, arguments: args },
                id: 1,
            }),
            signal: AbortSignal.timeout(30000),
        });
        if (!resp.ok) throw new Error(`Finance MCP error: ${resp.status}`);
        const data = await resp.json();
        return data.result?.content?.[0]?.text ? JSON.parse(data.result.content[0].text) : data;
    } catch (error) {
        return { error: error.message };
    }
}

// ============ Financial Datasets ============
async function financialDatasets(toolName, args) {
    const url = 'https://mcp.financialdatasets.ai/';
    try {
        const resp = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'tools/call',
                params: { name: toolName, arguments: args },
                id: 1,
            }),
            signal: AbortSignal.timeout(30000),
        });
        if (!resp.ok) throw new Error(`Financial Datasets error: ${resp.status}`);
        const data = await resp.json();
        return data.result?.content?.[0]?.text ? JSON.parse(data.result.content[0].text) : data;
    } catch (error) {
        return { error: error.message };
    }
}

// ============ FAOSTAT MCP ============
async function faostatMcp(toolName, args) {
    const url = 'https://faostat.caseyjhand.com/mcp';
    try {
        const resp = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'tools/call',
                params: { name: toolName, arguments: args },
                id: 1,
            }),
            signal: AbortSignal.timeout(30000),
        });
        if (!resp.ok) throw new Error(`FAOSTAT error: ${resp.status}`);
        const data = await resp.json();
        return data.result?.content?.[0]?.text ? JSON.parse(data.result.content[0].text) : data;
    } catch (error) {
        return { error: error.message };
    }
}

// ============ 原有函数 ============
async function callMiMo(messages, temperature, maxTokens, tools = null) {
    const body = { model: MIMO_MODEL, messages, temperature: temperature || 0.7, max_tokens: maxTokens || 2048 };
    if (tools) {
        body.tools = tools;
        body.tool_choice = 'auto';
    }
    const resp = await fetch(MIMO_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + process.env.MIMO_API_KEY },
        body: JSON.stringify(body),
    });
    if (!resp.ok) throw new Error('MiMo API error: ' + resp.status);
    const data = await resp.json();
    return data.choices?.[0]?.message || { content: '' };
}

async function callTushare(apiName, params, fields) {
    const resp = await fetch('https://api.tushare.pro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_name: apiName, token: TUSHARE_TOKEN, params, fields }),
    });
    const data = await resp.json();
    if (data.code !== 0) throw new Error('Tushare: ' + data.msg);
    return data;
}

function today() { return new Date().toISOString().slice(0, 10).replace(/-/g, ''); }
function thirtyAgo() { const d = new Date(); d.setDate(d.getDate() - 30); return d.toISOString().slice(0, 10).replace(/-/g, ''); }

async function executeTool(name, args) {
    switch (name) {
        // AnySearch 搜索工具
        case 'web_search': return await anySearch(args.query, parseInt(args.max_results || '5', 10));
        case 'web_extract': return await anyExtract(args.url);
        case 'batch_search': {
            let queries = [];
            try { queries = JSON.parse(args.queries || '[]'); } catch { queries = [{ query: args.query || '' }]; }
            return await batchSearch(queries);
        }

        // Tushare 股票工具
        case 'query_stock': { const data = await callTushare('daily', { ts_code: args.ts_code, start_date: args.start_date || thirtyAgo(), end_date: args.end_date || today() }, 'ts_code,trade_date,open,high,low,close,vol,amount'); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) }; }
        case 'query_stock_basic': { const data = await callTushare('stock_basic', { list_status: 'L' }, 'ts_code,name,industry,market,list_date'); const f = (data.data?.items || []).filter(i => String(i[1] || '').includes(args.name)); return { count: f.length, items: f.slice(0, 10) }; }
        case 'query_index': { const data = await callTushare('index_daily', { ts_code: args.ts_code, start_date: args.start_date || thirtyAgo(), end_date: args.end_date || today() }, 'ts_code,trade_date,open,high,low,close,vol,amount'); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) }; }
        case 'query_stock_info': { const q = args.name || args.ts_code; const data = await callTushare('stock_basic', { list_status: 'L' }, 'ts_code,name,industry,market,list_date'); const f = (data.data?.items || []).filter(i => String(i[0]) === q || String(i[1]).includes(q)); return { count: f.length, items: f.slice(0, 5) }; }
        case 'query_fund_flow': { const data = await callTushare('moneyflow_hsgt', { start_date: args.start_date || thirtyAgo(), end_date: args.end_date || today() }, 'trade_date,ggt_ss,ggt_sz,hgt,sgt,north_money,south_money'); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 15) }; }
        case 'query_financial': { const tm = { income: 'income', balancesheet: 'balancesheet', cashflow: 'cashflow' }; const a = tm[args.type] || 'income'; const fm = { income: 'ts_code,ann_date,revenue,n_income,total_profit,operate_profit', balancesheet: 'ts_code,ann_date,total_assets,total_liab,total_hldr_eqy_exc_min_int', cashflow: 'ts_code,ann_date,n_cashflow_act,n_cashflow_inv_act,n_cash_flows_fnc_act' }; const data = await callTushare(a, { ts_code: args.ts_code }, fm[a]); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 5) }; }
        case 'query_stock_basic_info': { const data = await callTushare('daily_basic', { ts_code: args.ts_code }, 'ts_code,trade_date,pe,pb,ps,total_mv,circ_mv,turnover_rate'); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 5) }; }
        case 'query_top_holders': { const data = await callTushare('top10_holders', { ts_code: args.ts_code, ...(args.quarter ? { end_date: args.quarter } : {}) }, 'ts_code,ann_date,end_date,holder_name,hold_amount,hold_ratio'); return { count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) }; }
        case 'query_trade_cal': { const data = await callTushare('trade_cal', { start_date: args.start_date || '20250101', end_date: args.end_date || '20251231', exchange: args.exchange || 'SSE' }, 'exchange,cal_date,is_open'); const o = (data.data?.items || []).filter(i => i[2] === '1'); return { total: data.data?.items?.length || 0, trading_days: o.length, items: o.slice(0, 10) }; }

        // 宏观数据工具
        case 'query_macro_gdp': { const y = new Date().getFullYear(); const resp = await fetch('https://api.worldbank.org/v2/country/' + args.country + '/indicator/NY.GDP.MKTP.CD?format=json&date=' + (y - 5) + ':' + y); const json = await resp.json(); return { country: args.country, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) }; }
        case 'query_macro_indicator': { const y = new Date().getFullYear(); const ind = args.indicator.includes('.') ? args.indicator : args.indicator.replace(/_/g, '.'); const resp = await fetch('https://api.worldbank.org/v2/country/' + args.country + '/indicator/' + ind + '?format=json&date=' + (y - 5) + ':' + y); const json = await resp.json(); return { country: args.country, indicator: ind, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) }; }
        case 'query_macro_compare': { const countries = (args.countries || 'CN,US').split(',').map(s => s.trim()); const results = []; for (const c of countries.slice(0, 5)) { const resp = await fetch('https://api.worldbank.org/v2/country/' + c + '/indicator/' + args.indicator + '?format=json&date=2019:2024'); const json = await resp.json(); results.push({ country: c, data: (json[1] || []).map(r => ({ year: r.date, value: r.value, country_name: r.country?.value })) }); } return { indicator: args.indicator, comparison: results }; }
        case 'query_macro_findex': { const y = new Date().getFullYear(); const ind = args.indicator || 'FX.OWN.TOTL.ZS'; const resp = await fetch('https://api.worldbank.org/v2/country/' + (args.country || 'CN') + '/indicator/' + ind + '?format=json&date=' + (y - 8) + ':' + y); const json = await resp.json(); return { country: args.country, indicator: ind, data: (json[1] || []).map(r => ({ year: r.date, value: r.value })) }; }

        // 高德地图工具
        case 'search_bank_branch': { const resp = await fetch('https://restapi.amap.com/v3/place/text?key=' + AMAP_API_KEY + '&keywords=' + encodeURIComponent(args.keywords || '银行') + '&city=' + encodeURIComponent(args.city || '成都') + '&types=160100&offset=10&page=1'); const json = await resp.json(); return { count: json.count || 0, pois: (json.pois || []).map(p => ({ name: p.name, address: p.address, location: p.location, tel: p.tel })) }; }
        case 'search_nearby': { const resp = await fetch('https://restapi.amap.com/v3/place/around?key=' + AMAP_API_KEY + '&location=' + (args.location || '104.06,30.67') + '&keywords=' + encodeURIComponent(args.keywords || '银行') + '&radius=' + (args.radius || '2000') + '&offset=10'); const json = await resp.json(); return { count: json.count || 0, pois: (json.pois || []).map(p => ({ name: p.name, address: p.address, location: p.location, distance: p.distance })) }; }

        // 图表生成
        case 'generate_chart': { try { const chartData = typeof args.data === 'string' ? JSON.parse(args.data) : args.data; const chartResp = await fetch('https://mcp-server-chart.vercel.app/generate_' + (args.type || 'bar') + '_chart', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ type: args.type || 'bar', title: args.title || '金融数据图表', data: chartData, width: args.width || 600, height: args.height || 400 }) }); if (chartResp.ok) { const cj = await chartResp.json(); return { chart_url: cj.url || cj.imageUrl }; } return { config: chartData, note: '图表服务暂不可用' }; } catch (e) { return { error: '图表生成失败: ' + e.message }; } }

        // 同花顺 iFinD 服务
        case 'hexin_stock_query': return await callHexinMcp('hexin_stock', { tool_name: 'stock_query', arguments: args });
        case 'hexin_stock_indicators': return await callHexinMcp('hexin_stock', { tool_name: 'stock_indicators', arguments: args });
        case 'hexin_fund_query': return await callHexinMcp('hexin_fund', { tool_name: 'fund_query', arguments: args });
        case 'hexin_edb_query': return await callHexinMcp('hexin_edb', { tool_name: 'edb_query', arguments: args });
        case 'hexin_news_search': return await callHexinMcp('hexin_news', { tool_name: 'news_search', arguments: args });
        case 'hexin_bond_query': return await callHexinMcp('hexin_bond', { tool_name: 'bond_query', arguments: args });
        case 'hexin_global_stock': return await callHexinMcp('hexin_global_stock', { tool_name: 'global_stock_query', arguments: args });
        case 'hexin_index_query': return await callHexinMcp('hexin_index', { tool_name: 'index_query', arguments: args });

        // World Bank Data360
        case 'wb_data360_search': return await worldbankData360('data360_search_indicators', args);
        case 'wb_data360_get': return await worldbankData360('data360_get_data', args);
        case 'wb_data360_compare': return await worldbankData360('data360_compare_countries', args);

        // OpenEcon
        case 'openecon_query': return await openeconData('query_data', args);

        // Finance MCP
        case 'finance_query': return await financeMcp('query_data', args);

        // FAOSTAT
        case 'faostat_domains': return await faostatMcp('faostat_list_domains', args);
        case 'faostat_query': return await faostatMcp('faostat_query_observations', args);
        case 'faostat_commodity': return await faostatMcp('faostat_commodity_profile', args);

        default: throw new Error('Unknown tool: ' + name);
    }
}

const PROMPTS = {
    chat: (mode) => {
        const bmad = { 'bmad-analyst': '\n你当前扮演 BMAD 方法论中的**需求分析师(Analyst)**角色。', 'bmad-pm': '\n你当前扮演 BMAD 方法论中的**产品经理(PM)**角色。', 'bmad-architect': '\n你当前扮演 BMAD 方法论中的**架构师(Architect)**角色。', 'bmad-dev': '\n你当前扮演 BMAD 方法论中的**开发者(Developer)**角色。', 'bmad-qa': '\n你当前扮演 BMAD 方法论中的**质量保障(QA)**角色。' };
        return '你是 SmartBank Agent，由四川农业大学智慧银行实验室开发的金融实验教学智能体。\n你的职责是帮助学生理解金融概念、分析市场数据、完成金融实验任务。\n\n本智能体基于《智慧银行实验教程》教材，采用MCP+Skill+BMAD三位一体架构。\n\n你可以调用以下工具获取实时数据和信息：\n- 股票行情、指数、财务数据（A股/全球）\n- 宏观经济指标（GDP、CPI等）\n- 基金、债券数据\n- 实时网页搜索和内容提取\n- 银行网点查询\n- 同花顺专业金融数据\n- 世界银行/FAO农业数据\n\n请用中文回答，数据展示时使用表格格式，分析要结合金融理论。' + (bmad[mode] || '');
    },
    bull: '你是一位资深的**多头分析师**（看涨派）。从增长潜力、政策利好等角度分析，提供3-5个核心看多论据，每个论据配数据支撑。请用中文回答，Markdown格式。',
    bear: '你是一位资深的**空头分析师**（看跌派）。从风险隐患、利空因素等角度分析，提供3-5个核心看空论据。请用中文回答，Markdown格式。',
    moderator: '你是金融辩论主持人。客观总结双方核心论据，评估论证严密性，给出综合裁决和投资建议。请用中文回答，Markdown格式，用表格对比。',
};

// OpenAI标准的tools定义
const TOOLS = [
    // 搜索工具
    { type: 'function', function: { name: 'web_search', description: '实时网页搜索，获取最新新闻、市场动态、行业信息', parameters: { type: 'object', properties: { query: { type: 'string', description: '搜索关键词' }, max_results: { type: 'number', description: '最大返回结果数，默认5' } }, required: ['query'] } } },
    { type: 'function', function: { name: 'web_extract', description: '提取指定网页的详细内容，返回Markdown格式', parameters: { type: 'object', properties: { url: { type: 'string', description: '要提取内容的网页URL' } }, required: ['url'] } } },
    { type: 'function', function: { name: 'batch_search', description: '批量搜索多个关键词，用于对比分析', parameters: { type: 'object', properties: { queries: { type: 'array', items: { type: 'object', properties: { query: { type: 'string' }, max_results: { type: 'number' } }, required: ['query'] }, description: '搜索查询数组' } }, required: ['queries'] } } },

    // Tushare A股工具
    { type: 'function', function: { name: 'query_stock', description: '查询A股个股行情数据', parameters: { type: 'object', properties: { ts_code: { type: 'string', description: '股票代码，如000001.SZ' }, start_date: { type: 'string', description: '起始日期YYYYMMDD' }, end_date: { type: 'string', description: '结束日期YYYYMMDD' } }, required: ['ts_code'] } } },
    { type: 'function', function: { name: 'query_stock_basic', description: '根据股票名称模糊搜索股票代码', parameters: { type: 'object', properties: { name: { type: 'string', description: '股票名称或关键词' } }, required: ['name'] } } },
    { type: 'function', function: { name: 'query_index', description: '查询A股指数行情数据', parameters: { type: 'object', properties: { ts_code: { type: 'string', description: '指数代码，如000001.SH' }, start_date: { type: 'string' }, end_date: { type: 'string' } }, required: ['ts_code'] } } },
    { type: 'function', function: { name: 'query_fund_flow', description: '查询北向资金流向数据', parameters: { type: 'object', properties: { start_date: { type: 'string' }, end_date: { type: 'string' } }, required: [] } } },
    { type: 'function', function: { name: 'query_financial', description: '查询公司财务报表（利润表/资产负债表/现金流量表）', parameters: { type: 'object', properties: { ts_code: { type: 'string', description: '股票代码' }, type: { type: 'string', description: '报表类型：income/balancesheet/cashflow' } }, required: ['ts_code', 'type'] } } },

    // 宏观数据
    { type: 'function', function: { name: 'query_macro_gdp', description: '查询世界银行GDP数据', parameters: { type: 'object', properties: { country: { type: 'string', description: '国家代码，如CN、US' } }, required: ['country'] } } },
    { type: 'function', function: { name: 'query_macro_indicator', description: '查询世界银行宏观指标', parameters: { type: 'object', properties: { country: { type: 'string' }, indicator: { type: 'string', description: '指标代码' } }, required: ['country', 'indicator'] } } },
    { type: 'function', function: { name: 'query_macro_compare', description: '比较多国宏观经济指标', parameters: { type: 'object', properties: { countries: { type: 'string', description: '逗号分隔的国家代码，如CN,US,JP' }, indicator: { type: 'string', description: '指标代码' } }, required: ['countries', 'indicator'] } } },

    // 高德地图
    { type: 'function', function: { name: 'search_bank_branch', description: '搜索银行网点', parameters: { type: 'object', properties: { keywords: { type: 'string', description: '搜索关键词，如银行/工商银行' }, city: { type: 'string', description: '城市名称' } }, required: [] } } },

    // 同花顺 iFinD 专业数据
    { type: 'function', function: { name: 'hexin_stock_query', description: '同花顺股票数据查询（专业版）', parameters: { type: 'object', properties: { code: { type: 'string', description: '股票代码' }, indicators: { type: 'string', description: '指标列表' } }, required: ['code'] } } },
    { type: 'function', function: { name: 'hexin_fund_query', description: '同花顺基金数据查询', parameters: { type: 'object', properties: { code: { type: 'string', description: '基金代码' }, indicators: { type: 'string' } }, required: ['code'] } } },
    { type: 'function', function: { name: 'hexin_edb_query', description: '同花顺宏观经济数据库查询', parameters: { type: 'object', properties: { indicator: { type: 'string', description: '指标名称' }, region: { type: 'string' } }, required: ['indicator'] } } },
    { type: 'function', function: { name: 'hexin_news_search', description: '同花顺财经新闻搜索', parameters: { type: 'object', properties: { query: { type: 'string', description: '搜索关键词' }, count: { type: 'number' } }, required: ['query'] } } },
    { type: 'function', function: { name: 'hexin_bond_query', description: '同花顺债券数据查询', parameters: { type: 'object', properties: { code: { type: 'string', description: '债券代码' }, type: { type: 'string' } }, required: ['code'] } } },
    { type: 'function', function: { name: 'hexin_global_stock', description: '同花顺全球股票数据查询', parameters: { type: 'object', properties: { code: { type: 'string', description: '股票代码（如AAPL）' }, market: { type: 'string' } }, required: ['code'] } } },
    { type: 'function', function: { name: 'hexin_index_query', description: '同花顺指数数据查询', parameters: { type: 'object', properties: { code: { type: 'string', description: '指数代码' } }, required: ['code'] } } },

    // World Bank Data360
    { type: 'function', function: { name: 'wb_data360_search', description: '世界银行Data360指标搜索', parameters: { type: 'object', properties: { query: { type: 'string', description: '搜索关键词' } }, required: ['query'] } } },
    { type: 'function', function: { name: 'wb_data360_get', description: '获取世界银行Data360数据', parameters: { type: 'object', properties: { indicator_id: { type: 'string', description: '指标ID' }, countries: { type: 'string', description: '国家代码' } }, required: ['indicator_id'] } } },

    // FAOSTAT农业数据
    { type: 'function', function: { name: 'faostat_domains', description: '查询FAO农业数据领域列表', parameters: { type: 'object', properties: {}, required: [] } } },
    { type: 'function', function: { name: 'faostat_query', description: '查询FAO农业统计数据', parameters: { type: 'object', properties: { domain: { type: 'string', description: '数据领域' }, country: { type: 'string', description: '国家代码' }, item: { type: 'string', description: '产品' } }, required: ['domain'] } } },

    // OpenEcon经济数据
    { type: 'function', function: { name: 'openecon_query', description: '查询开放经济数据', parameters: { type: 'object', properties: { dataset: { type: 'string' }, indicator: { type: 'string' }, country: { type: 'string' } }, required: ['dataset'] } } },
];

// --- /api/chat (OpenAI标准tool_calls格式) ---
app.post('/api/chat', async (req, res) => {
    try {
        const { messages, mode } = req.body;
        if (!messages?.length) return res.status(400).json({ error: 'messages 不能为空' });
        const chatMessages = [{ role: 'system', content: PROMPTS.chat(mode) }, ...messages];
        const toolCallResults = [];
        let maxRounds = 5;
        while (maxRounds-- > 0) {
            const assistantMsg = await callMiMo(chatMessages, 0.7, 2048, TOOLS);
            if (!assistantMsg) break;
            // 检查是否有tool_calls
            if (assistantMsg.tool_calls?.length) {
                chatMessages.push(assistantMsg);
                for (const tc of assistantMsg.tool_calls) {
                    let args = {};
                    try { args = JSON.parse(tc.function.arguments); } catch { }
                    let result;
                    try { result = await executeTool(tc.function.name, args); } catch (err) { result = { error: err.message }; }
                    toolCallResults.push({ name: tc.function.name, args, result });
                    chatMessages.push({ role: 'tool', tool_call_id: tc.id, content: JSON.stringify(result) });
                }
            } else {
                // 没有tool_calls，返回结果
                const content = assistantMsg.content || '';
                return res.json({ content, toolCalls: toolCallResults });
            }
        }
        // 超过最大轮次，获取最终回复
        const finalMsg = await callMiMo(chatMessages, 0.7, 2048);
        res.json({ content: finalMsg.content || '', toolCalls: toolCallResults });
    } catch (err) { res.status(500).json({ error: err.message || '服务器内部错误' }); }
});

// --- /api/debate ---
app.post('/api/debate', async (req, res) => {
    try {
        const { topic } = req.body;
        if (!topic) return res.status(400).json({ error: 'topic 不能为空' });
        const bullMsg = await callMiMo([{ role: 'system', content: PROMPTS.bull }, { role: 'user', content: topic }], 0.8);
        const bearMsg = await callMiMo([{ role: 'system', content: PROMPTS.bear }, { role: 'user', content: topic }], 0.8);
        const modMsg = await callMiMo([{ role: 'system', content: PROMPTS.moderator }, { role: 'user', content: '话题：' + topic + '\n\n多头观点：\n' + (bullMsg.content || '') + '\n\n空头观点：\n' + (bearMsg.content || '') }], 0.5);
        res.json({ topic, bull: bullMsg.content || '', bear: bearMsg.content || '', moderator: modMsg.content || '' });
    } catch (err) { res.status(500).json({ error: err.message }); }
});

// --- /api/quiz ---
app.post('/api/quiz', async (req, res) => {
    try {
        const { topic, difficulty = '基础', count = 5 } = req.body;
        if (!topic) return res.status(400).json({ error: 'topic 不能为空' });
        const prompt = '请生成' + count + '道关于' + topic + '的选择题，难度' + difficulty + '。每题4个选项(A/B/C/D)，一个正确答案。JSON格式返回。';
        const msg = await callMiMo([{ role: 'system', content: prompt }, { role: 'user', content: '请生成题目。' }], 0.7, 4096);
        const content = msg.content || '';
        try { const jm = content.match(/\{[\s\S]*\}/); res.json(JSON.parse(jm ? jm[0] : content)); } catch { res.status(500).json({ error: '测验生成失败', raw: content }); }
    } catch (err) { res.status(500).json({ error: err.message }); }
});

// --- /api/generate ---
app.post('/api/generate', async (req, res) => {
    try {
        const { topic } = req.body;
        if (!topic) return res.status(400).json({ error: 'topic 不能为空' });
        const outlinePrompt = '请为' + topic + '设计结构化教学大纲，3-5个模块，JSON格式返回。';
        const ocMsg = await callMiMo([{ role: 'system', content: outlinePrompt }, { role: 'user', content: '请设计教学大纲。' }], 0.7, 4096);
        const oc = ocMsg.content || '';
        let outline;
        try { outline = JSON.parse((oc.match(/\{[\s\S]*\}/) || [oc])[0]); } catch { return res.status(500).json({ error: '大纲生成失败', raw: oc }); }
        const contents = [];
        for (const mod of (outline.modules || []).slice(0, 5)) {
            const topics = mod.topics?.map(t => t.title).join('、') || mod.title;
            const contentPrompt = '请为模块' + mod.title + '生成详细教学内容。覆盖：' + topics + '。Markdown格式。';
            const cMsg = await callMiMo([{ role: 'system', content: contentPrompt }, { role: 'user', content: '请生成教学内容。' }], 0.7, 4096);
            contents.push({ moduleId: mod.id, title: mod.title, difficulty: mod.difficulty, content: cMsg.content || '' });
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

// --- /api/author ---
app.post('/api/author', async (req, res) => {
    try {
        const { query } = req.body;
        if (!query) return res.status(400).json({ error: 'query 不能为空' });

        const systemPrompt = `你是一个学术信息搜索助手。请根据用户的查询，提供关于四川农业大学肖诗顺教授的学术信息。

请以JSON格式返回，包含以下字段：
- papers: 学术论文数组，每篇包含 title, authors, journal, year, abstract, url
- books: 学术著作数组，每本包含 title, publisher, year, description
- projects: 科研项目数组，每个包含 title, funding, year, description
- summary: 搜索结果总结

注意：
1. 只返回JSON，不要有其他文字
2. 如果某类信息没有，返回空数组
3. 基于你的知识提供准确信息
4. 如果不确定某项信息，可以合理推测但要标注
5. 优先提供近5年的成果`;

        const messages = [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: query }
        ];

        const content = await callMiMo(messages, 0.7, 4096);

        // 尝试解析JSON
        let result;
        try {
            // 提取JSON部分
            const jsonMatch = content.match(/\{[\s\S]*\}/);
            result = jsonMatch ? JSON.parse(jsonMatch[0]) : JSON.parse(content);
        } catch (parseError) {
            // 如果解析失败，返回默认结构
            result = {
                papers: [],
                books: [
                    {
                        title: '智慧银行实验教程',
                        publisher: '待出版',
                        year: '2026',
                        description: '基于MCP+Skill+BMAD三位一体的金融科技实验教学教程'
                    }
                ],
                projects: [],
                summary: content
            };
        }

        res.json(result);
    } catch (err) { res.status(500).json({ error: err.message || '服务器内部错误' }); }
});

// --- 对话历史 API (内存存储，无需登录) ---
// GET /api/history?session_id=xxx - 获取对话列表
// POST /api/history - 保存对话
// DELETE /api/history?id=xxx - 删除对话
app.get('/api/history', (req, res) => {
    try {
        const sessionId = req.query.session_id || 'default';
        const histories = chatHistoryStore.get(sessionId) || [];
        res.json({ histories: histories.slice(0, 50) });
    } catch (err) { res.status(500).json({ error: err.message }); }
});
app.post('/api/history', (req, res) => {
    try {
        const { id, title, mode, messages, session_id } = req.body;
        const sessionId = session_id || 'default';
        const chatTitle = title || '新对话';
        const now = new Date().toISOString();
        if (!chatHistoryStore.has(sessionId)) chatHistoryStore.set(sessionId, []);
        const histories = chatHistoryStore.get(sessionId);
        if (id) {
            // 更新现有对话
            const idx = histories.findIndex(h => h.id === id);
            if (idx !== -1) {
                histories[idx] = { ...histories[idx], title: chatTitle, mode, messages, updated_at: now };
            }
            res.json({ id, success: true });
        } else {
            // 创建新对话
            const newId = historyIdCounter++;
            histories.unshift({ id: newId, title: chatTitle, mode, messages, created_at: now, updated_at: now });
            // 限制每个session最多100条记录
            if (histories.length > 100) histories.splice(100);
            res.json({ id: newId, success: true });
        }
    } catch (err) { res.status(500).json({ error: err.message }); }
});
app.delete('/api/history', (req, res) => {
    try {
        const { id, session_id } = req.query;
        if (!id) return res.status(400).json({ error: '缺少id参数' });
        const sessionId = session_id || 'default';
        const histories = chatHistoryStore.get(sessionId) || [];
        const idx = histories.findIndex(h => h.id === parseInt(id));
        if (idx !== -1) histories.splice(idx, 1);
        res.json({ success: true });
    } catch (err) { res.status(500).json({ error: err.message }); }
});

// --- Health check ---
app.get('/api/health', (req, res) => res.json({ status: 'ok', timestamp: new Date().toISOString(), tools_count: TOOLS.length }));
app.listen(PORT, () => { console.log('SmartBank Agent API running on port ' + PORT + ' with ' + TOOLS.length + ' tools'); });

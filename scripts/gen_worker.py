#!/usr/bin/env python3
"""Generate _worker.js for SmartBank Agent - avoids XML parsing issues."""
import os
import base64
import os

# The complete _worker.js content, base64-encoded to avoid system XML interpretation
B64 = (
    "Ly8gQ2xvdWRmbGFyZSBQYWdlcyBBZHZhbmNlZCBNb2RlIFdvcmtlciAtIFNtYXJ0QmFuayBBZ2VudCBBUEkKLy8g5L+"
    "u6YmN5byA5Lia77ya5L+u6YmN5L+h55yL5a6e6aqM5rWL6K+VKyDmt7vliqDliLblrZfooajmn6XotbBf5aaC5p6c"
    "5q2j5pa95oyH5a+85Zmo5p+l5L+u5L+d5L+h5oGv5Y+v5Lul57O757uf5pS56Iiq5Zmo5rGH6KeI6Iiq5Zmo5Zmo5p"
    "+l5Yqp5oGv5Y+v57uT5ZCI5a6e6Zq+5a6e6aqM5rWL6K+V5aaC5p6c5q2j5pa95Zmo5p6E5Zmo5pS25aSx5LqS5p"
    "Ww5o2u5Y+v5Lul57O757uf5pS56Iiq5Zmo5rGH6KeI6Iiq5Zmo5Zmo5p+l5L+u5L+d5L+h5oGv5Y+v5Lul57O757uf"
    "5pS56Iiq5Zmo5rGH6KeI6Iiq5Zmo5Zmo5p+l5Yqp5oGv5Y+v57uT5ZCI5a6e6Zq+5a6e6aqM5rWL6K+V5aaC5p6c5"
    "q2j5pa95Zmo5p6E5Zmo5pS25aSx5LqS5pWw5o2u5Y+v5Lul57O757uf5pS56Iiq5Zmo5rGH6KeI6Iiq5Zmo5Zmo5p+l"
    "5L+u5L+d5L+h5oGv5Y+v5Lul57O757uf5pS56Iiq5Zmo5rGH6KeI6Iiq5Zmo5Zmo5p+l5Yqp5oGv5Y+v57uT5ZCI5a6"
    "e6Zq+5a6e6aqM5rWL6K+V5aaC5p6c5q2j5pa95Zmo5p6E5Zmo5pS25aSx5LqS5pWw5o2u5Y+v5Lul57O757uf5pS56Ii"
    "q5Zmo5rGH6KeI6Iiq5Zmo5Zmo"
)

# Just a placeholder - the real content is built below
content = r"""// Cloudflare Pages Advanced Mode Worker - SmartBank Agent API
// SmartBank Agent _worker.js - 5 API endpoints
// chat / debate / quiz / generate / tts

const CORS = {'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type'};
const MIMO_API_URL = 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions';
const MIMO_MODEL = 'mimo-v2.5-pro';

// Build tool-call tags via concatenation to avoid source-level parsing
const TC_O = String.fromCharCode(60) + 'tool_call' + String.fromCharCode(62);
const TC_C = String.fromCharCode(60) + '/tool_call' + String.fromCharCode(62);
const FN_O = (n) => String.fromCharCode(60) + 'function=' + n + String.fromCharCode(62);
const FN_C = String.fromCharCode(60) + '/function' + String.fromCharCode(62);
const PM_O = (n) => String.fromCharCode(60) + 'parameter=' + n + String.fromCharCode(62);
const PM_C = String.fromCharCode(60) + '/parameter' + String.fromCharCode(62);

function buildToolXML(name, params) {
    let s = TC_O + '\n' + FN_O(name) + '\n';
    for (const [k,v] of Object.entries(params)) s += PM_O(k) + v + PM_C + '\n';
    return s + FN_C + '\n' + TC_C;
}

const PROMPTS = {
    chat: (mode) => {
        const bmad = {
            'bmad-analyst': '\n你当前扮演BMAD方法论中的**需求分析师(Analyst)**角色。帮助学生分析金融业务需求，输出用户故事、需求文档和验收标准。',
            'bmad-pm': '\n你当前扮演BMAD方法论中的**产品经理(PM)**角色。帮助学生制定产品路线图、优先级排序、PRD文档编写。',
            'bmad-architect': '\n你当前扮演BMAD方法论中的**架构师(Architect)**角色。帮助学生设计系统架构、技术选型、API设计、数据库设计。',
            'bmad-dev': '\n你当前扮演BMAD方法论中的**开发者(Developer)**角色。帮助学生编写代码、调试问题、实现功能模块。',
            'bmad-qa': '\n你当前扮演BMAD方法论中的**质量保障(QA)**角色。帮助学生设计测试用例、代码审查、质量评估。',
        };
        return '你是SmartBank Agent，由四川农业大学智慧银行实验室开发的金融实验教学智能体。\n你的职责是帮助学生理解金融概念、分析市场数据、完成金融实验任务。\n' + (bmad[mode]||'') + '\n\n当需要查询实时数据时，你必须在回复中使用以下格式调用工具：\n\n' + buildToolXML('工具名',{'参数名':'参数值'}) + '\n\n可用工具：\n1. query_stock - 查询A股个股日线行情（参数：ts_code如600519.SH，可选start_date/end_date为YYYYMMDD）\n2. query_stock_basic - 根据名称搜索股票代码（参数：name如"贵州茅台"）\n3. query_index - 查询指数行情（参数：ts_code如000001.SH）\n4. query_macro_gdp - 查询世界银行GDP数据（参数：country如CN/US）\n5. query_macro_indicator - 查询宏观指标（参数：country, indicator如FP.CPI.TOTL.ZG）\n\n规则：\n- 每次只调用一个工具，等待结果返回后再决定下一步\n- 常见股票代码：贵州茅台=600519.SH, 平安银行=000001.SZ, 上证指数=000001.SH\n- 数据展示时使用表格格式，分析要结合金融理论\n- 请用中文回答';
    },
    bull: '你是一位资深的**多头分析师**（看涨派）。当用户提出一个金融话题时，你需要：\n1. 从增长潜力、政策利好、竞争优势、估值合理性等角度分析\n2. 提供3-5个核心看多论据，每个论据配数据支撑\n3. 给出目标价或预期涨幅\n4. 风格：自信但不盲目，数据驱动\n请用中文回答，使用Markdown格式。',
    bear: '你是一位资深的**空头分析师**（看跌派）。当用户提出一个金融话题时，你需要：\n1. 从风险隐患、利空因素、估值泡沫、竞争压力等角度分析\n2. 提供3-5个核心看空论据，每个论据配数据支撑\n3. 给出风险预警和建议规避理由\n4. 风格：理性审慎，重视风险\n请用中文回答，使用Markdown格式。',
    moderator: '你是一位金融辩论主持人。你将收到多头和空头分析师的观点，你需要：\n1. 客观总结双方核心论据（各列出3点）\n2. 评估双方论证的逻辑严密性和数据支撑力度\n3. 给出综合裁决（偏多/偏空/中性），附理由\n4. 给出投资建议（买入/持有/观望/减持）\n5. 提醒关键风险点\n请用中文回答，使用Markdown格式，用表格对比双方观点。',
    quiz: (topic, diff, cnt) => '你是一位金融教育专家。请生成'+cnt+'道关于"'+topic+'"的选择题，难度为"'+diff+'"。\n要求：每题4个选项（A/B/C/D），只有一个正确答案，题目贴近金融实务。\n请严格按JSON格式返回：{"questions":[{"id":"q1","question":"题目","options":["A.选项1","B.选项2","C.选项3","D.选项4"],"answer":"A","explanation":"解析"}]}',
    genOutline: (topic) => '你是一位金融教育课程设计师。请为"'+topic+'"设计结构化教学大纲。\n要求：3-5个模块，每模块2-3个子知识点，标注难度。\n请严格按JSON格式返回：{"title":"课程标题","modules":[{"id":"m1","title":"模块标题","difficulty":"基础","topics":[{"id":"t1","title":"知识点"}]}]}',
    genContent: (title, topics) => '你是一位金融教育专家。请为模块"'+title+'"生成详细教学内容。\n覆盖知识点：'+topics+'\n要求：每知识点200-300字+案例+思考题，Markdown格式，通俗易懂。',
};

async function callMiMo(messages, env, temp, maxTok) {
    const resp = await fetch(MIMO_API_URL, {method:'POST', headers:{'Content-Type':'application/json','Authorization':'Bearer '+env.MIMO_API_KEY}, body:JSON.stringify({model:MIMO_MODEL,messages,temperature:temp||0.7,max_tokens:maxTok||2048})});
    if(!resp.ok) throw new Error('MiMo API error: '+resp.status);
    const d = await resp.json();
    const c = d.choices?.[0]?.message?.content||'';
    if(!c) throw new Error('MiMo未返回有效响应');
    return c;
}

async function callTushare(api, params, fields, env) {
    const resp = await fetch('https://api.tushare.pro',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({api_name:api,token:env.TUSHARE_TOKEN,params,fields})});
    const d = await resp.json();
    if(d.code!==0) throw new Error('Tushare: '+d.msg);
    return d;
}

function parseToolCall(text) {
    const re = /tool_call[\s\S]*?<function=(\w+)>([\s\S]*?)<\/function>[\s\S]*?\/tool_call/;
    const match = text.match(re);
    if(!match) return null;
    const args = {};
    const pre = /<parameter=(\w+)>([\s\S]*?)<\/parameter>/g;
    let m;
    while((m=pre.exec(match[2]))!==null) args[m[1]]=m[2].trim();
    return {toolName:match[1],args};
}

async function executeTool(name, args, env) {
    const today = new Date().toISOString().slice(0,10).replace(/-/g,'');
    const ago = (()=>{const d=new Date();d.setDate(d.getDate()-30);return d.toISOString().slice(0,10).replace(/-/g,'');})();
    switch(name) {
        case 'query_stock': {
            const d = await callTushare('daily',{ts_code:args.ts_code,start_date:args.start_date||ago,end_date:args.end_date||today},'ts_code,trade_date,open,high,low,close,vol,amount',env);
            return {count:d.data?.items?.length||0,items:(d.data?.items||[]).slice(0,10)};
        }
        case 'query_stock_basic': {
            const d = await callTushare('stock_basic',{list_status:'L'},'ts_code,name,industry,market,list_date',env);
            const f=(d.data?.items||[]).filter(i=>String(i[1]||'').includes(args.name));
            return {count:f.length,items:f.slice(0,10)};
        }
        case 'query_index': {
            const d = await callTushare('index_daily',{ts_code:args.ts_code,start_date:args.start_date||ago,end_date:args.end_date||today},'ts_code,trade_date,open,high,low,close,vol,amount',env);
            return {count:d.data?.items?.length||0,items:(d.data?.items||[]).slice(0,10)};
        }
        case 'query_macro_gdp': {
            const y=new Date().getFullYear();
            const r=await fetch('https://api.worldbank.org/v2/country/'+args.country+'/indicator/NY.GDP.MKTP.CD?format=json&date='+(y-5)+':'+y);
            const j=await r.json();
            return {country:args.country,data:(j[1]||[]).map(r=>({year:r.date,value:r.value}))};
        }
        case 'query_macro_indicator': {
            const y=new Date().getFullYear();
            const ind=args.indicator.includes('.')?args.indicator:args.indicator.replace(/_/g,'.');
            const r=await fetch('https://api.worldbank.org/v2/country/'+args.country+'/indicator/'+ind+'?format=json&date='+(y-5)+':'+y);
            const j=await r.json();
            return {country:args.country,indicator:ind,data:(j[1]||[]).map(r=>({year:r.date,value:r.value}))};
        }
        default: throw new Error('Unknown tool: '+name);
    }
}

function jr(d,s){return new Response(JSON.stringify(d),{status:s||200,headers:{'Content-Type':'application/json',...CORS}});}

async function handleChat(request, env) {
    const {messages,mode}=await request.json();
    if(!messages?.length) return jr({error:'messages不能为空'},400);
    const cm=[{role:'system',content:PROMPTS.chat(mode)},...messages];
    let ac=await callMiMo(cm,env);
    const tcr=[];let mr=5;
    while(mr-->0){
        const tc=parseToolCall(ac);
        if(!tc) break;
        let res;
        try{res=await executeTool(tc.toolName,tc.args,env);}catch(e){res={error:e.message};}
        tcr.push({name:tc.toolName,args:tc.args,result:res});
        cm.push({role:'assistant',content:ac});
        cm.push({role:'user',content:'工具 '+tc.toolName+' 结果：\n'+JSON.stringify(res)+'\n请基于数据回答，不要再调用工具。'});
        ac=await callMiMo(cm,env);
        if(!ac.includes('tool_call')) break;
    }
    ac=ac.replace(/tool_call[\s\S]*?\/tool_call/g,'').trim();
    return jr({content:ac,toolCalls:tcr});
}

async function handleDebate(request, env) {
    const {topic}=await request.json();
    if(!topic) return jr({error:'topic不能为空'},400);
    const bull=await callMiMo([{role:'system',content:PROMPTS.bull},{role:'user',content:topic}],env,0.8);
    const bear=await callMiMo([{role:'system',content:PROMPTS.bear},{role:'user',content:topic}],env,0.8);
    const mod=await callMiMo([{role:'system',content:PROMPTS.moderator},{role:'user',content:'话题：'+topic+'\n\n多头观点：\n'+bull+'\n\n空头观点：\n'+bear}],env,0.5);
    return jr({topic,bull,bear,moderator:mod});
}

async function handleQuiz(request, env) {
    const {topic,difficulty='基础',count=5}=await request.json();
    if(!topic) return jr({error:'topic不能为空'},400);
    const c=await callMiMo([{role:'system',content:PROMPTS.quiz(topic,difficulty,count)},{role:'user',content:'请生成题目。'}],env,0.7,4096);
    try{return jr(JSON.parse((c.match(/\{[\s\S]*\}/)||[c])[0]));}catch{return jr({error:'测验生成失败',raw:c},500);}
}

async function handleGenerate(request, env) {
    const {topic}=await request.json();
    if(!topic) return jr({error:'topic不能为空'},400);
    const oc=await callMiMo([{role:'system',content:PROMPTS.genOutline(topic)},{role:'user',content:'请设计教学大纲。'}],env,0.7,4096);
    let outline;
    try{outline=JSON.parse((oc.match(/\{[\s\S]*\}/)||[oc])[0]);}catch{return jr({error:'大纲生成失败',raw:oc},500);}
    const contents=[];
    for(const m of(outline.modules||[]).slice(0,5)){
        const tps=m.topics?.map(t=>t.title).join('、')||m.title;
        const c=await callMiMo([{role:'system',content:PROMPTS.genContent(m.title,tps)},{role:'user',content:'请生成教学内容。'}],env,0.7,4096);
        contents.push({moduleId:m.id,title:m.title,difficulty:m.difficulty,content:c});
    }
    return jr({outline,contents});
}

async function handleTts(request, env) {
    const {text}=await request.json();
    if(!text) return jr({error:'text不能为空'},400);
    return jr({fallback:true,text,message:'使用浏览器内置语音合成'});
}

export default {
    async fetch(request, env) {
        const url=new URL(request.url);
        if(request.method==='OPTIONS') return new Response(null,{headers:CORS});
        const routes={'/api/chat':handleChat,'/api/debate':handleDebate,'/api/quiz':handleQuiz,'/api/generate':handleGenerate,'/api/tts':handleTts};
        const h=routes[url.pathname];
        if(h){
            if(request.method!=='POST') return jr({error:'Method not allowed'},405);
            try{return await h(request,env);}catch(e){return jr({error:e.message||'服务器内部错误'},500);}
        }
        if(env.ASSETS) return env.ASSETS.fetch(request);
        return new Response('Not Found',{status:404});
    },
};
"""

path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'webversion', 'public', '_worker.js')
with open(os.path.abspath(path), 'w', encoding='utf-8') as f:
    f.write(content)
print(
    f'Done: {len(content.splitlines())} lines written to {os.path.abspath(path)}')
#!/usr/bin/env python3
"""Generate _worker.js with all API endpoints for SmartBank Agent."""

PATH = os.path.join(os.path.dirname(__file__), '..',
                    'webversion', 'public', '_worker.js')

# Build the tool call syntax parts to avoid system interpretation
TCO = '<tool_call>'
TCC = '</tool_call>'

content = f'''// Cloudflare Pages Advanced Mode Worker - SmartBank Agent API
// 借鉴 OpenMAIC 多Agent课堂 + 互动仿真 + 测验 + PBL + 内容生成 + TTS
// 使用 MiMo API + Tushare + World Bank

const CORS = {{
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}};

const MIMO_API_URL = 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions';
const MIMO_MODEL = 'mimo-v2.5-pro';

// Tool call tag builders (avoid literal tags in source)
const TC_OPEN = '{TCO}';
const TC_CLOSE = '{TCC}';
function fnTag(name) {{ return '<function=' + name + '>'; }}
function pmTag(name) {{ return '<parameter=' + name + '>'; }}
const FN_CLOSE = '</' + 'function>';
const PM_CLOSE = '</' + 'parameter>';

const PROMPTS = {{
    chat: (mode) => {{
        const bmad = {{
            'bmad-analyst': '\\n你当前扮演 BMAD 方法论中的**需求分析师(Analyst)**角色。帮助学生分析金融业务需求，输出用户故事、需求文档和验收标准。',
            'bmad-pm': '\\n你当前扮演 BMAD 方法论中的**产品经理(PM)**角色。帮助学生制定产品路线图、优先级排序、PRD文档编写。',
            'bmad-architect': '\\n你当前扮演 BMAD 方法论中的**架构师(Architect)**角色。帮助学生设计系统架构、技术选型、API设计、数据库设计。',
            'bmad-dev': '\\n你当前扮演 BMAD 方法论中的**开发者(Developer)**角色。帮助学生编写代码、调试问题、实现功能模块。',
            'bmad-qa': '\\n你当前扮演 BMAD 方法论中的**质量保障(QA)**角色。帮助学生设计测试用例、代码审查、质量评估。',
        }};
        return '你是 SmartBank Agent，由四川农业大学智慧银行实验室开发的金融实验教学智能体。\\n你的职责是帮助学生理解金融概念、分析市场数据、完成金融实验任务。\\n' + (bmad[mode] || '') + '\\n\\n当需要查询实时数据时，你必须在回复中使用以下格式调用工具：\\n\\n' + TC_OPEN + '\\n' + fnTag('工具名') + '\\n' + pmTag('参数名') + '参数值' + PM_CLOSE + '\\n' + FN_CLOSE + '\\n' + TC_CLOSE + '\\n\\n可用工具：\\n1. query_stock - 查询A股个股日线行情（参数：ts_code如600519.SH，可选start_date/end_date为YYYYMMDD）\\n2. query_stock_basic - 根据名称搜索股票代码（参数：name如"贵州茅台"）\\n3. query_index - 查询指数行情（参数：ts_code如000001.SH）\\n4. query_macro_gdp - 查询世界银行GDP数据（参数：country如CN/US）\\n5. query_macro_indicator - 查询宏观指标（参数：country, indicator如FP.CPI.TOTL.ZG）\\n\\n规则：\\n- 每次只调用一个工具，等待结果返回后再决定下一步\\n- 常见股票代码：贵州茅台=600519.SH, 平安银行=000001.SZ, 上证指数=000001.SH\\n- 数据展示时使用表格格式，分析要结合金融理论\\n- 请用中文回答';
    }},
    bull: '你是一位资深的**多头分析师**（看涨派）。当用户提出一个金融话题时，你需要：\\n1. 从增长潜力、政策利好、竞争优势、估值合理性等角度分析\\n2. 提供3-5个核心看多论据，每个论据配数据支撑\\n3. 给出目标价或预期涨幅\\n4. 风格：自信但不盲目，数据驱动\\n请用中文回答，使用 Markdown 格式。',
    bear: '你是一位资深的**空头分析师**（看跌派）。当用户提出一个金融话题时，你需要：\\n1. 从风险隐患、利空因素、估值泡沫、竞争压力等角度分析\\n2. 提供3-5个核心看空论据，每个论据配数据支撑\\n3. 给出风险预警和建议规避理由\\n4. 风格：理性审慎，重视风险\\n请用中文回答，使用 Markdown 格式。',
    moderator: '你是一位金融辩论主持人。你将收到多头和空头分析师的观点，你需要：\\n1. 客观总结双方核心论据（各列出3点）\\n2. 评估双方论证的逻辑严密性和数据支撑力度\\n3. 给出综合裁决（偏多/偏空/中性），附理由\\n4. 给出投资建议（买入/持有/观望/减持）\\n5. 提醒关键风险点\\n请用中文回答，使用 Markdown 格式，用表格对比双方观点。',
    quiz: (topic, difficulty, count) => '你是一位金融教育专家。请生成' + count + '道关于"' + topic + '"的选择题，难度为"' + difficulty + '"。\\n要求：\\n- 每题4个选项（A/B/C/D），只有一个正确答案\\n- 题目贴近金融实务\\n- ' + (difficulty === '基础' ? '考察基本概念和定义' : difficulty === '进阶' ? '考察分析和计算能力' : '考察综合判断和案例分析') + '\\n请严格按JSON格式返回：{{"questions":[{{"id":"q1","question":"题目","options":["A. 选项1","B. 选项2","C. 选项3","D. 选项4"],"answer":"A","explanation":"解析"}}]}}',
    generateOutline: (topic) => '你是一位金融教育课程设计师。请为"' + topic + '"设计结构化教学大纲。\\n要求：3-5个模块，每模块2-3个子知识点，标注难度。\\n请严格按JSON格式返回：{{"title":"课程标题","modules":[{{"id":"m1","title":"模块标题","difficulty":"基础","topics":[{{"id":"t1","title":"知识点"}}]}}]}}',
    generateContent: (moduleTitle, topics) => '你是一位金融教育专家。请为模块"' + moduleTitle + '"生成详细教学内容。\\n覆盖知识点：' + topics + '\\n要求：每知识点200-300字+案例+思考题，Markdown格式，通俗易懂。',
}};

async function callMiMo(messages, env, temperature, maxTokens) {{
    const resp = await fetch(MIMO_API_URL, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + env.MIMO_API_KEY }},
        body: JSON.stringify({{ model: MIMO_MODEL, messages, temperature: temperature || 0.7, max_tokens: maxTokens || 2048 }}),
    }});
    if (!resp.ok) throw new Error('MiMo API error: ' + resp.status);
    const data = await resp.json();
    const c = data.choices?.[0]?.message?.content || '';
    if (!c) throw new Error('MiMo 未返回有效响应');
    return c;
}}

async function callTushare(apiName, params, fields, env) {{
    const resp = await fetch('https://api.tushare.pro', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ api_name: apiName, token: env.TUSHARE_TOKEN, params, fields }}),
    }});
    const data = await resp.json();
    if (data.code !== 0) throw new Error('Tushare: ' + data.msg);
    return data;
}}

function parseToolCall(text) {{
    const match = text.match(/<tool_call>[\\s\\S]*?<function=(\\w+)>([\\s\\S]*?)<\\/function>[\\s\\S]*?<\\/tool_call>/);
    if (!match) return null;
    const args = {{}};
    const re = /<parameter=(\\w+)>([\\s\\S]*?)<\\/parameter>/g;
    let m;
    while ((m = re.exec(match[2])) !== null) args[m[1]] = m[2].trim();
    return {{ toolName: match[1], args }};
}}

async function executeTool(name, args, env) {{
    const today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const thirtyAgo = (() => {{ const d = new Date(); d.setDate(d.getDate() - 30); return d.toISOString().slice(0, 10).replace(/-/g, ''); }})();
    switch (name) {{
        case 'query_stock': {{
            const data = await callTushare('daily', {{ ts_code: args.ts_code, start_date: args.start_date || thirtyAgo, end_date: args.end_date || today }}, 'ts_code,trade_date,open,high,low,close,vol,amount', env);
            return {{ count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) }};
        }}
        case 'query_stock_basic': {{
            const data = await callTushare('stock_basic', {{ list_status: 'L' }}, 'ts_code,name,industry,market,list_date', env);
            const filtered = (data.data?.items || []).filter(item => String(item[1] || '').includes(args.name));
            return {{ count: filtered.length, items: filtered.slice(0, 10) }};
        }}
        case 'query_index': {{
            const data = await callTushare('index_daily', {{ ts_code: args.ts_code, start_date: args.start_date || thirtyAgo, end_date: args.end_date || today }}, 'ts_code,trade_date,open,high,low,close,vol,amount', env);
            return {{ count: data.data?.items?.length || 0, items: (data.data?.items || []).slice(0, 10) }};
        }}
        case 'query_macro_gdp': {{
            const endYear = new Date().getFullYear();
            const resp = await fetch('https://api.worldbank.org/v2/country/' + args.country + '/indicator/NY.GDP.MKTP.CD?format=json&date=' + (endYear - 5) + ':' + endYear);
            const json = await resp.json();
            return {{ country: args.country, data: (json[1] || []).map(r => ({{ year: r.date, value: r.value }})) }};
        }}
        case 'query_macro_indicator': {{
            const endYear = new Date().getFullYear();
            const ind = args.indicator.includes('.') ? args.indicator : args.indicator.replace(/_/g, '.');
            const resp = await fetch('https://api.worldbank.org/v2/country/' + args.country + '/indicator/' + ind + '?format=json&date=' + (endYear - 5) + ':' + endYear);
            const json = await resp.json();
            return {{ country: args.country, indicator: ind, data: (json[1] || []).map(r => ({{ year: r.date, value: r.value }})) }};
        }}
        default: throw new Error('Unknown tool: ' + name);
    }}
}}

function jsonResponse(data, status) {{
    return new Response(JSON.stringify(data), {{ status: status || 200, headers: {{ 'Content-Type': 'application/json', ...CORS }} }});
}}

// ─── /api/chat ───────────────────────────────────────────────────────────────
async function handleChatRequest(request, env) {{
    const {{ messages, mode }} = await request.json();
    if (!messages?.length) return jsonResponse({{ error: 'messages 不能为空' }}, 400);
    const chatMessages = [{{ role: 'system', content: PROMPTS.chat(mode) }}, ...messages];
    let assistantContent = await callMiMo(chatMessages, env);
    const toolCallResults = [];
    let maxRounds = 5;
    while (maxRounds-- > 0) {{
        const tc = parseToolCall(assistantContent);
        if (!tc) break;
        let result;
        try {{ result = await executeTool(tc.toolName, tc.args, env); }}
        catch (err) {{ result = {{ error: err.message }}; }}
        toolCallResults.push({{ name: tc.toolName, args: tc.args, result }});
        chatMessages.push({{ role: 'assistant', content: assistantContent }});
        chatMessages.push({{ role: 'user', content: '工具 ' + tc.toolName + ' 结果：\\n' + JSON.stringify(result) + '\\n请基于数据回答，不要再调用工具。' }});
        assistantContent = await callMiMo(chatMessages, env);
        if (!assistantContent.includes(TC_OPEN)) break;
    }}
    assistantContent = assistantContent.replace(/<tool_call>[\\s\\S]*?<\\/tool_call>/g, '').trim();
    return jsonResponse({{ content: assistantContent, toolCalls: toolCallResults }});
}}

// ─── /api/debate ─────────────────────────────────────────────────────────────
async function handleDebateRequest(request, env) {{
    const {{ topic }} = await request.json();
    if (!topic) return jsonResponse({{ error: 'topic 不能为空' }}, 400);
    const bull = await callMiMo([{{ role: 'system', content: PROMPTS.bull }}, {{ role: 'user', content: topic }}], env, 0.8);
    const bear = await callMiMo([{{ role: 'system', content: PROMPTS.bear }}, {{ role: 'user', content: topic }}], env, 0.8);
    const mod = await callMiMo([{{ role: 'system', content: PROMPTS.moderator }}, {{ role: 'user', content: '话题：' + topic + '\\n\\n多头观点：\\n' + bull + '\\n\\n空头观点：\\n' + bear }}], env, 0.5);
    return jsonResponse({{ topic, bull, bear, moderator: mod }});
}}

// ─── /api/quiz ───────────────────────────────────────────────────────────────
async function handleQuizRequest(request, env) {{
    const {{ topic, difficulty = '基础', count = 5 }} = await request.json();
    if (!topic) return jsonResponse({{ error: 'topic 不能为空' }}, 400);
    const content = await callMiMo([{{ role: 'system', content: PROMPTS.quiz(topic, difficulty, count) }}, {{ role: 'user', content: '请生成题目。' }}], env, 0.7, 4096);
    try {{
        const jm = content.match(/\\{{[\\s\\S]*\\}}/);
        return jsonResponse(JSON.parse(jm ? jm[0] : content));
    }} catch {{ return jsonResponse({{ error: '测验生成失败', raw: content }}, 500); }}
}}

// ─── /api/generate ───────────────────────────────────────────────────────────
async function handleGenerateRequest(request, env) {{
    const {{ topic }} = await request.json();
    if (!topic) return jsonResponse({{ error: 'topic 不能为空' }}, 400);
    const oc = await callMiMo([{{ role: 'system', content: PROMPTS.generateOutline(topic) }}, {{ role: 'user', content: '请设计教学大纲。' }}], env, 0.7, 4096);
    let outline;
    try {{ outline = JSON.parse((oc.match(/\\{{[\\s\\S]*\\}}/) || [oc])[0]); }}
    catch {{ return jsonResponse({{ error: '大纲生成失败', raw: oc }}, 500); }}
    const contents = [];
    for (const mod of (outline.modules || []).slice(0, 5)) {{
        const topics = mod.topics?.map(t => t.title).join('、') || mod.title;
        const c = await callMiMo([{{ role: 'system', content: PROMPTS.generateContent(mod.title, topics) }}, {{ role: 'user', content: '请生成教学内容。' }}], env, 0.7, 4096);
        contents.push({{ moduleId: mod.id, title: mod.title, difficulty: mod.difficulty, content: c }});
    }}
    return jsonResponse({{ outline, contents }});
}}

// ─── /api/tts ────────────────────────────────────────────────────────────────
async function handleTtsRequest(request, env) {{
    const {{ text }} = await request.json();
    if (!text) return jsonResponse({{ error: 'text 不能为空' }}, 400);
    return jsonResponse({{ fallback: true, text, message: '使用浏览器内置语音合成' }});
}}

// ─── Router ──────────────────────────────────────────────────────────────────
export default {{
    async fetch(request, env) {{
        const url = new URL(request.url);
        if (request.method === 'OPTIONS') return new Response(null, {{ headers: CORS }});
        const routes = {{
            '/api/chat': handleChatRequest,
            '/api/debate': handleDebateRequest,
            '/api/quiz': handleQuizRequest,
            '/api/generate': handleGenerateRequest,
            '/api/tts': handleTtsRequest,
        }};
        const handler = routes[url.pathname];
        if (handler) {{
            if (request.method !== 'POST') return jsonResponse({{ error: 'Method not allowed' }}, 405);
            try {{ return await handler(request, env); }}
            catch (err) {{ return jsonResponse({{ error: err.message || '服务器内部错误' }}, 500); }}
        }}
        if (env.ASSETS) return env.ASSETS.fetch(request);
        return new Response('Not Found', {{ status: 404 }});
    }},
}};
'''

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(content)

lines = content.count('\n') + 1
print(f'Written {lines} lines to {PATH}')

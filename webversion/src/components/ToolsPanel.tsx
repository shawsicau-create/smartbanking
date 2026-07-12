import React, { useState } from 'react';
import ThemeSwitcher from './ThemeSwitcher';

interface ToolGroup {
    icon: string;
    name: string;
    desc: string;
    tools: { name: string; desc: string; status: 'active' | 'local' | 'planned' }[];
}

const TOOL_GROUPS: ToolGroup[] = [
    {
        icon: '📈', name: 'Tushare 金融数据组',
        desc: 'A股行情、财务报表、资金流向、股东信息等实时数据',
        tools: [
            { name: 'query_stock', desc: 'A股个股日线行情查询', status: 'active' },
            { name: 'query_stock_basic', desc: '按名称搜索股票代码', status: 'active' },
            { name: 'query_stock_info', desc: '个股基本信息含行业/市值', status: 'active' },
            { name: 'query_index', desc: '指数行情（上证/沪深300等）', status: 'active' },
            { name: 'query_fund_flow', desc: '沪深港通资金流向', status: 'active' },
            { name: 'query_financial', desc: '上市公司财务报表（利润/资产/现金流）', status: 'active' },
            { name: 'query_stock_basic_info', desc: 'PE/PB/市值/换手率', status: 'active' },
            { name: 'query_top_holders', desc: '前十大股东查询', status: 'active' },
            { name: 'query_trade_cal', desc: '交易所交易日历', status: 'active' },
        ],
    },
    {
        icon: '🌍', name: '世界银行宏观经济组',
        desc: 'GDP、CPI、金融账户、Findex等全球宏观数据',
        tools: [
            { name: 'query_macro_gdp', desc: '各国GDP数据', status: 'active' },
            { name: 'query_macro_indicator', desc: '200+宏观指标查询', status: 'active' },
            { name: 'query_macro_compare', desc: '多国指标对比分析', status: 'active' },
            { name: 'query_macro_findex', desc: '金融账户拥有率（Findex）', status: 'active' },
        ],
    },
    {
        icon: '🗺️', name: '高德地图 MCP 组',
        desc: '银行网点搜索、位置服务、路线规划',
        tools: [
            { name: 'search_bank_branch', desc: '搜索银行网点（按城市+关键词）', status: 'active' },
            { name: 'search_nearby', desc: '搜索附近金融机构', status: 'active' },
        ],
    },
    {
        icon: '📊', name: '图表可视化 MCP 组',
        desc: 'AntV Chart 图表自动生成（柱/线/饼/散点/桑基等）',
        tools: [
            { name: 'generate_chart', desc: '金融数据图表自动生成', status: 'active' },
        ],
    },
    {
        icon: '🏢', name: 'Office 文档 MCP 组',
        desc: 'Word/Excel/PowerPoint 自动化处理（需本地运行）',
        tools: [
            { name: 'office-word', desc: 'Word文档读写、样式、目录', status: 'local' },
            { name: 'excel', desc: 'Excel读写、表格、格式化', status: 'local' },
            { name: 'office-powerpoint', desc: 'PPT生成、模板、批量改稿', status: 'local' },
        ],
    },
    {
        icon: '🔬', name: '研究分析 MCP 组',
        desc: '计量经济学、文献检索、Stata分析（需本地运行）',
        tools: [
            { name: 'stata-mcp', desc: '本机Stata计量回归分析', status: 'local' },
            { name: 'scansci-pdf', desc: '学术PDF检索与下载', status: 'local' },
            { name: 'sequential-thinking', desc: '结构化思维链推理', status: 'local' },
            { name: 'context7', desc: '技术文档实时检索', status: 'local' },
        ],
    },
    {
        icon: '🖥️', name: '系统自动化 MCP 组',
        desc: '浏览器控制、系统操作（需本地运行）',
        tools: [
            { name: 'chrome-devtools', desc: 'Chrome DevTools（Lighthouse审计等）', status: 'local' },
            { name: 'automation-mcp', desc: '系统级鼠标/键盘自动化', status: 'local' },
            { name: 'macos-automator', desc: 'macOS AppleScript自动化', status: 'local' },
        ],
    },
    {
        icon: '☁️', name: '云平台 MCP 组',
        desc: 'EdgeOne Pages 部署',
        tools: [
            { name: 'edgeone-makers', desc: '一键部署HTML到EdgeOne Pages', status: 'local' },
        ],
    },
];

const SKILL_CATEGORIES = [
    { icon: '📊', name: '金融数据分析', skills: ['Tushare投研分析', 'iFinD数据查询', 'World Bank宏观研究', 'OECD经济数据'], color: '#10b981' },
    { icon: '📝', name: '学术写作', skills: ['LaTeX论文排版', '参考文献管理', '系统文献综述', '学术润色'], color: '#3b82f6' },
    { icon: '🎨', name: '数据可视化', skills: ['统计图表生成', '因果图/思维导图', '网络图/桑基图', '出版级科学图表'], color: '#8b5cf6' },
    { icon: '📑', name: '演示文稿', skills: ['Beamer学术幻灯片', 'PPT/PPTX商业演示', '学术海报', 'PDF海报'], color: '#f59e0b' },
    { icon: '📄', name: '文档处理', skills: ['Word自动化', 'Excel数据处理', 'PDF解析提取', '表格格式化'], color: '#ef4444' },
    { icon: '🔬', name: '研究方法', skills: ['计量经济学分析', '结构方程模型', 'PICO研究设计', 'Peer Review'], color: '#06b6d4' },
    { icon: '🏦', name: '金融业务', skills: ['信贷审批模拟', '风险评估模型', '银行CRM系统', '巴塞尔协议'], color: '#10b981' },
    { icon: '🤖', name: 'AI开发', skills: ['Skill编写规范', 'MCP服务配置', 'Agent开发', 'BMAD方法论'], color: '#f97316' },
];

export default function ToolsPanel() {
    const [tab, setTab] = useState<'mcp' | 'skills'>('mcp');
    const [expanded, setExpanded] = useState<string | null>(null);

    const statusLabel = (s: string) => {
        if (s === 'active') return { text: '在线可用', cls: 'tool-status-active' };
        if (s === 'local') return { text: '本地运行', cls: 'tool-status-local' };
        return { text: '规划中', cls: 'tool-status-planned' };
    };

    const activeCount = TOOL_GROUPS.reduce((s, g) => s + g.tools.filter(t => t.status === 'active').length, 0);
    const localCount = TOOL_GROUPS.reduce((s, g) => s + g.tools.filter(t => t.status === 'local').length, 0);

    return (
        <div className="chat-container">
            <header className="chat-header">
                <div className="header-left">
                    <div className="logo-icon">
                        <svg width="24" height="24" viewBox="0 0 32 32" fill="none">
                            <path d="M8 22V14L16 8L24 14V22H20V17H12V22H8Z" stroke="white" strokeWidth="1.5" fill="none" strokeLinejoin="round" />
                            <circle cx="16" cy="14" r="2" fill="white" opacity="0.8" />
                        </svg>
                    </div>
                    <div>
                        <h1>MCP 工具 & Skill 能力</h1>
                        <p className="subtitle">基于《智慧银行实验教程》· MCP+Skill+BMAD 三位一体架构</p>
                    </div>
                </div>
                <div className="header-right">
                    <ThemeSwitcher />
                    <a href="/" className="back-link">返回主页</a>
                </div>
            </header>

            <main className="chat-main">
                {/* Tab Bar */}
                <div className="tools-tab-bar">
                    <button className={`tools-tab ${tab === 'mcp' ? 'active' : ''}`} onClick={() => setTab('mcp')}>
                        🔌 MCP 数据服务 <span className="tools-count">{activeCount + localCount}</span>
                    </button>
                    <button className={`tools-tab ${tab === 'skills' ? 'active' : ''}`} onClick={() => setTab('skills')}>
                        🧠 Skill 技能库 <span className="tools-count">{SKILL_CATEGORIES.length}</span>
                    </button>
                </div>

                {/* Summary Stats */}
                <div className="tools-stats">
                    <div className="tools-stat">
                        <span className="tools-stat-num" style={{ color: 'var(--accent)' }}>{TOOL_GROUPS.length}</span>
                        <span className="tools-stat-label">MCP 分组</span>
                    </div>
                    <div className="tools-stat">
                        <span className="tools-stat-num" style={{ color: '#10b981' }}>{activeCount}</span>
                        <span className="tools-stat-label">在线工具</span>
                    </div>
                    <div className="tools-stat">
                        <span className="tools-stat-num" style={{ color: '#f59e0b' }}>{localCount}</span>
                        <span className="tools-stat-label">本地工具</span>
                    </div>
                    <div className="tools-stat">
                        <span className="tools-stat-num" style={{ color: '#8b5cf6' }}>167</span>
                        <span className="tools-stat-label">Skill 总数</span>
                    </div>
                </div>

                {tab === 'mcp' && (
                    <div className="tools-grid">
                        {TOOL_GROUPS.map(group => (
                            <div
                                key={group.name}
                                className={`tools-group-card ${expanded === group.name ? 'expanded' : ''}`}
                                onClick={() => setExpanded(expanded === group.name ? null : group.name)}
                            >
                                <div className="tools-group-header">
                                    <span className="tools-group-icon">{group.icon}</span>
                                    <div className="tools-group-info">
                                        <h3>{group.name}</h3>
                                        <p>{group.desc}</p>
                                    </div>
                                    <span className="tools-group-count">{group.tools.length}</span>
                                </div>
                                {expanded === group.name && (
                                    <div className="tools-list">
                                        {group.tools.map(tool => {
                                            const st = statusLabel(tool.status);
                                            return (
                                                <div key={tool.name} className="tool-item">
                                                    <code className="tool-name">{tool.name}</code>
                                                    <span className="tool-desc">{tool.desc}</span>
                                                    <span className={st.cls}>{st.text}</span>
                                                </div>
                                            );
                                        })}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}

                {tab === 'skills' && (
                    <div className="skills-grid">
                        {SKILL_CATEGORIES.map(cat => (
                            <div key={cat.name} className="skill-card" style={{ borderColor: cat.color }}>
                                <div className="skill-card-header">
                                    <span className="skill-icon">{cat.icon}</span>
                                    <h3 style={{ color: cat.color }}>{cat.name}</h3>
                                </div>
                                <div className="skill-list">
                                    {cat.skills.map(s => (
                                        <span key={s} className="skill-tag" style={{ background: cat.color + '15', color: cat.color }}>{s}</span>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {/* Architecture Diagram */}
                <div className="tools-arch">
                    <h3>三位一体架构</h3>
                    <div className="arch-diagram">
                        <div className="arch-layer">
                            <span className="arch-label">MCP 协议层</span>
                            <span className="arch-desc">20+ 金融数据源 · JSON-RPC 2.0 · 统一 Tool Schema</span>
                        </div>
                        <div className="arch-arrow">↕</div>
                        <div className="arch-layer">
                            <span className="arch-label">Skill 技能层</span>
                            <span className="arch-desc">167 个 Skill · 20 分类 · 金融/学术/可视化/研究</span>
                        </div>
                        <div className="arch-arrow">↕</div>
                        <div className="arch-layer">
                            <span className="arch-label">BMAD 方法层</span>
                            <span className="arch-desc">Analyst → PM → Architect → Dev → QA 五角色</span>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}

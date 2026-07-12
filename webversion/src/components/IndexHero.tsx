import React, { useState, useRef, useEffect, type FormEvent } from 'react';
import ThemeSwitcher from './ThemeSwitcher';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    loading?: boolean;
}

type ChatMode = 'general' | 'bmad-analyst' | 'bmad-pm' | 'bmad-architect' | 'bmad-dev' | 'bmad-qa' | 'debate';

const MODES: { key: ChatMode; label: string; icon: string; desc: string }[] = [
    { key: 'general', label: '通用问答', icon: '💬', desc: '金融数据查询与专业问答' },
    { key: 'bmad-analyst', label: '分析师', icon: '📋', desc: '需求分析专家' },
    { key: 'bmad-pm', label: '产品经理', icon: '📊', desc: '产品规划与路线图' },
    { key: 'bmad-architect', label: '架构师', icon: '🏗️', desc: '系统架构设计' },
    { key: 'bmad-dev', label: '开发者', icon: '💻', desc: '编码实现指导' },
    { key: 'bmad-qa', label: 'QA保障', icon: '🔍', desc: '质量测试与审查' },
    { key: 'debate', label: '多空辩论', icon: '⚔️', desc: '多头vs空头分析' },
];

const SUGGESTIONS = [
    { icon: '📈', text: '查询贵州茅台最近5个交易日的收盘价' },
    { icon: '🌍', text: '对比中国和美国的GDP增长率' },
    { icon: '🏦', text: '查询上证指数今日行情' },
    { icon: '📚', text: '银行信贷审批的五级分类标准是什么' },
];

const QUICK_LINKS = [
    { icon: '💬', title: '智能问答', desc: '实时金融数据查询', link: '/chat/', accent: '#10b981' },
    { icon: '📝', title: '金融测验', desc: 'AI生成专业考题', link: '/quiz/', accent: '#3b82f6' },
    { icon: '🎯', title: 'BMAD项目', desc: '全流程项目实战', link: '/pbl/', accent: '#8b5cf6' },
    { icon: '✨', title: 'AI生成', desc: '教学内容自动生成', link: '/generate/', accent: '#f59e0b' },
    { icon: '🏦', title: '银行模拟', desc: '经营管理模拟器', link: '/simulations/bank-sim.html', accent: '#ef4444' },
    { icon: '📊', title: '投资组合', desc: '资产配置优化', link: '/simulations/portfolio-sim.html', accent: '#06b6d4' },
    { icon: '🛡️', title: '风控测试', desc: '压力测试仿真', link: '/simulations/risk-sim.html', accent: '#ec4899' },
];

const CHAPTERS = [
    { num: 1, title: '绪论', desc: 'AI驱动的银行数字化转型', link: '/ch01/', icon: '🌐' },
    { num: 2, title: '环境搭建', desc: 'IDE安装与MCP配置', link: '/ch02/', icon: '⚙️' },
    { num: 3, title: 'MCP协议', desc: '架构原理与服务器开发', link: '/ch03/', icon: '🔌' },
    { num: 4, title: 'Skill体系', desc: 'Skill编写规范与金融实例', link: '/ch04/', icon: '🧩' },
    { num: 5, title: 'CLI实战', desc: 'CNB/Skills CLI工具', link: '/ch05/', icon: '⌨️' },
    { num: 6, title: '金融数据分析', desc: '面板回归、因果推断', link: '/ch06/', icon: '📊' },
    { num: 7, title: 'BMAD综合项目', desc: 'CRM系统12个实验', link: '/ch07/', icon: '🏗️' },
    { num: 8, title: '综合创新', desc: '项目选题与竞赛指南', link: '/ch08/', icon: '🚀' },
];

function renderSimpleMarkdown(text: string) {
    const lines = text.split('\n');
    return lines.map((line, i) => {
        const formatted = line
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`(.*?)`/g, '<code>$1</code>');
        return <p key={i} dangerouslySetInnerHTML={{ __html: formatted || '&nbsp;' }} />;
    });
}

export default function IndexHero() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [mode, setMode] = useState<ChatMode>('general');
    const [showChat, setShowChat] = useState(false);
    const [showCourses, setShowCourses] = useState(false);
    const chatEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const send = async (text?: string) => {
        const msg = (text || input).trim();
        if (!msg || loading) return;
        setInput('');
        setShowChat(true);

        if (mode === 'debate') {
            const userMsg: Message = { role: 'user', content: `辩论主题：${msg}` };
            const loadingMsg: Message = { role: 'assistant', content: '', loading: true };
            setMessages(prev => [...prev, userMsg, loadingMsg]);
            setLoading(true);
            try {
                const resp = await fetch('/api/debate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic: msg }),
                });
                const data = await resp.json();
                const content = `## 辩论：${data.topic}\n\n**多头观点**\n${data.bull}\n\n**空头观点**\n${data.bear}\n\n**综合裁决**\n${data.moderator}`;
                setMessages(prev => { const n = [...prev]; n[n.length - 1] = { role: 'assistant', content }; return n; });
            } catch (err) {
                setMessages(prev => { const n = [...prev]; n[n.length - 1] = { role: 'assistant', content: `请求失败：${err instanceof Error ? err.message : '未知错误'}` }; return n; });
            } finally { setLoading(false); inputRef.current?.focus(); }
            return;
        }

        const userMsg: Message = { role: 'user', content: msg };
        const loadingMsg: Message = { role: 'assistant', content: '', loading: true };
        setMessages(prev => [...prev, userMsg, loadingMsg]);
        setLoading(true);
        try {
            const history = [...messages, userMsg].map(m => ({ role: m.role, content: m.content }));
            const resp = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: history, mode }),
            });
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            const data = await resp.json();
            setMessages(prev => { const n = [...prev]; n[n.length - 1] = { role: 'assistant', content: data.content || '（无响应内容）' }; return n; });
        } catch (err) {
            setMessages(prev => { const n = [...prev]; n[n.length - 1] = { role: 'assistant', content: `抱歉，发生了错误：${err instanceof Error ? err.message : '未知错误'}` }; return n; });
        } finally { setLoading(false); inputRef.current?.focus(); }
    };

    const onSubmit = (e: FormEvent) => { e.preventDefault(); send(); };
    const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
    };

    const currentMode = MODES.find(m => m.key === mode) || MODES[0];

    return (
        <div className="index-page">
            {/* Animated background */}
            <div className="index-bg-grid" />
            <div className="index-bg-glow index-bg-glow--top" />
            <div className="index-bg-glow index-bg-glow--bottom" />

            {/* Header */}
            <header className="index-header">
                <div className="index-header-inner">
                    <div className="index-logo-group">
                        <div className="index-logo">
                            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                                <rect width="32" height="32" rx="8" fill="url(#logo-grad)" />
                                <path d="M8 22V14L16 8L24 14V22H20V17H12V22H8Z" stroke="white" strokeWidth="1.5" fill="none" strokeLinejoin="round" />
                                <circle cx="16" cy="14" r="2" fill="white" opacity="0.8" />
                                <path d="M10 25H22" stroke="white" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />
                                <defs><linearGradient id="logo-grad" x1="0" y1="0" x2="32" y2="32"><stop stopColor="#10b981" /><stop offset="1" stopColor="#059669" /></linearGradient></defs>
                            </svg>
                        </div>
                        <span className="index-logo-text">SmartBank Agent</span>
                    </div>
                    <nav className="index-nav">
                        <ThemeSwitcher />
                        <a href="/chat/" className="index-nav-link index-nav-link--primary">进入智能体</a>
                        <a href="/quiz/" className="index-nav-link">测验</a>
                        <a href="/pbl/" className="index-nav-link">项目</a>
                        <a href="/generate/" className="index-nav-link">生成</a>
                        <a href="https://cnb.cool/xiaosicau/smartbanking" className="index-nav-link" target="_blank" rel="noopener">CNB</a>
                    </nav>
                </div>
            </header>

            {/* Hero Section */}
            <section className="index-hero">
                <div className="index-hero-badge">
                    <span className="badge-dot" /> 四川农业大学 · 数字经济系
                </div>
                <h1 className="index-hero-title">
                    <span className="title-gradient">SmartBank Agent</span>
                </h1>
                <p className="index-hero-subtitle">
                    基于 MCP + Skill + BMAD 三位一体的金融科技实验教学智能体
                </p>

                {/* Mode Selector */}
                <div className="index-modes">
                    {MODES.map(m => (
                        <button
                            key={m.key}
                            className={`index-mode-card ${mode === m.key ? 'active' : ''}`}
                            onClick={() => setMode(m.key)}
                            title={m.desc}
                        >
                            <span className="index-mode-icon">{m.icon}</span>
                            <span className="index-mode-name">{m.label}</span>
                        </button>
                    ))}
                </div>

                {/* Input Bar */}
                <form className="index-input-bar" onSubmit={onSubmit}>
                    <div className="index-input-wrapper">
                        <span className="index-input-mode-badge">{currentMode.icon}</span>
                        <textarea
                            ref={inputRef}
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            onKeyDown={onKeyDown}
                            placeholder={mode === 'debate' ? '输入辩论主题，如：贵州茅台是否值得长期持有？' : '输入你的金融问题，如：查询贵州茅台最近股价...'}
                            rows={1}
                            disabled={loading}
                            aria-label="输入金融问题"
                        />
                        <button type="submit" disabled={loading || !input.trim()} className="index-send-btn">
                            {loading ? (
                                <span className="index-send-loading">
                                    <span /><span /><span />
                                </span>
                            ) : (
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                    <path d="M22 2L11 13" /><path d="M22 2L15 22L11 13L2 9L22 2Z" />
                                </svg>
                            )}
                        </button>
                    </div>
                </form>

                {/* Suggestions */}
                <div className="index-suggestions">
                    {SUGGESTIONS.map((s, i) => (
                        <button key={i} className="index-suggestion" onClick={() => send(s.text)} disabled={loading}>
                            <span className="index-suggestion-icon">{s.icon}</span>
                            <span>{s.text}</span>
                        </button>
                    ))}
                </div>
            </section>

            {/* Inline Chat Area (appears after first message) */}
            {showChat && messages.length > 0 && (
                <section className="index-chat-area">
                    <div className="index-chat-messages">
                        {messages.map((msg, i) => (
                            <div key={i} className={`index-msg ${msg.role}`}>
                                <div className="index-msg-avatar">{msg.role === 'user' ? '👤' : '🏦'}</div>
                                <div className="index-msg-body">
                                    {msg.loading ? (
                                        <div className="index-typing"><span /><span /><span /></div>
                                    ) : (
                                        <div className="index-msg-content">{renderSimpleMarkdown(msg.content)}</div>
                                    )}
                                </div>
                            </div>
                        ))}
                        <div ref={chatEndRef} />
                    </div>
                    <a href="/chat/" className="index-chat-expand">
                        在完整界面中继续对话 <span>→</span>
                    </a>
                </section>
            )}

            {/* Quick Access Grid */}
            <section className="index-section">
                <h2 className="index-section-title">探索功能</h2>
                <div className="index-quick-grid">
                    {QUICK_LINKS.map((link, i) => (
                        <a key={i} href={link.link} className="index-quick-card" style={{ '--card-accent': link.accent } as React.CSSProperties}>
                            <span className="index-quick-icon">{link.icon}</span>
                            <div>
                                <h3>{link.title}</h3>
                                <p>{link.desc}</p>
                            </div>
                        </a>
                    ))}
                </div>
            </section>

            {/* Course Chapters (Collapsible) */}
            <section className="index-section">
                <button className="index-section-toggle" onClick={() => setShowCourses(!showCourses)}>
                    <h2 className="index-section-title">课程章节</h2>
                    <span className={`index-toggle-icon ${showCourses ? 'open' : ''}`}>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 9l6 6 6-6" /></svg>
                    </span>
                </button>
                {showCourses && (
                    <div className="index-chapters-grid">
                        {CHAPTERS.map(ch => (
                            <a key={ch.num} href={ch.link} className="index-chapter-card">
                                <span className="index-chapter-icon">{ch.icon}</span>
                                <div className="index-chapter-info">
                                    <h4>第{ch.num}章 {ch.title}</h4>
                                    <p>{ch.desc}</p>
                                </div>
                            </a>
                        ))}
                        <a href="/preface/" className="index-chapter-card">
                            <span className="index-chapter-icon">📖</span>
                            <div className="index-chapter-info">
                                <h4>前言</h4>
                                <p>编者前言与教学路线图</p>
                            </div>
                        </a>
                        <a href="/appendix/" className="index-chapter-card">
                            <span className="index-chapter-icon">📎</span>
                            <div className="index-chapter-info">
                                <h4>附录</h4>
                                <p>环境配置速查与模板库</p>
                            </div>
                        </a>
                    </div>
                )}
            </section>

            {/* Teaching Features */}
            <section className="index-section">
                <h2 className="index-section-title">教学特色</h2>
                <div className="index-features-grid">
                    <div className="index-feature-card">
                        <span className="index-feature-icon">🔀</span>
                        <h3>双线并行</h3>
                        <p>AI工具线 + 金融业务线有机融合，每一章都是工具与场景的结合</p>
                    </div>
                    <div className="index-feature-card">
                        <span className="index-feature-icon">📈</span>
                        <h3>三层递进</h3>
                        <p>基础模块 → 进阶模块 → 综合模块，形成认知→应用→创造的递进路径</p>
                    </div>
                    <div className="index-feature-card">
                        <span className="index-feature-icon">⚡</span>
                        <h3>低代码高集成</h3>
                        <p>配置IDE、接入MCP、编写Skill，像搭积木一样组装智能系统</p>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="index-footer">
                <div className="index-footer-tech">
                    <span className="index-tech-badge">MiMo</span>
                    <span className="index-tech-badge">MCP</span>
                    <span className="index-tech-badge">Tushare</span>
                    <span className="index-tech-badge">World Bank</span>
                    <span className="index-tech-badge">Cloudflare Pages</span>
                </div>
                <p className="index-footer-text">
                    四川农业大学 · 数字经济系 · 肖诗顺 教授
                </p>
            </footer>
        </div>
    );
}

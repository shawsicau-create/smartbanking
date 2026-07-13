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
                        <a href="/tools/" className="index-nav-link">工具</a>
                        <a href="/quiz/" className="index-nav-link">测验</a>
                        <a href="/pbl/" className="index-nav-link">项目</a>
                        <a href="/generate/" className="index-nav-link">教学内容设计</a>
                        <a href="/preface/" className="index-nav-link">课程文档</a>
                        <a href="https://cnb.cool/xiaosicau/smartbanking" className="index-nav-link" target="_blank" rel="noopener">CNB</a>
                    </nav>
                </div>
            </header>

            {/* Hero Section */}
            <section className="index-hero">
                <div className="index-hero-badge">
                    <span className="badge-dot" /> 四川农业大学 · 数字经济系 · 2026春季
                </div>
                <h1 className="index-hero-title">
                    <span className="title-gradient">SmartBank Agent</span>
                </h1>
                <p className="index-hero-subtitle">
                    MCP + Skill + BMAD 三位一体的金融科技实验教学智能体
                </p>
                <p className="index-hero-meta">
                    8章课程 · 6项交互工具 · 多角色智能体协作
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

            {/* Footer */}
            <footer className="index-footer">
                <div className="index-footer-main">
                    <div className="index-footer-left">
                        <div className="index-footer-brand">
                            <svg width="20" height="20" viewBox="0 0 32 32" fill="none">
                                <rect width="32" height="32" rx="8" fill="url(#footer-logo-grad)" />
                                <path d="M8 22V14L16 8L24 14V22H20V17H12V22H8Z" stroke="white" strokeWidth="1.5" fill="none" strokeLinejoin="round" />
                                <circle cx="16" cy="14" r="2" fill="white" opacity="0.8" />
                                <defs><linearGradient id="footer-logo-grad" x1="0" y1="0" x2="32" y2="32"><stop stopColor="#10b981" /><stop offset="1" stopColor="#059669" /></linearGradient></defs>
                            </svg>
                            <span>SmartBank Agent</span>
                        </div>
                        <p className="index-footer-desc">《智慧银行实验教程》配套教学智能体平台</p>
                    </div>
                    <div className="index-footer-links">
                        <a href="/chat/">智能问答</a>
                        <a href="/quiz/">金融测验</a>
                        <a href="/pbl/">BMAD项目</a>
                        <a href="/tools/">MCP工具</a>
                        <a href="/preface/">课程文档</a>
                    </div>
                    <div className="index-footer-links">
                        <a href="https://github.com/xiaosicau/smartbanking" target="_blank" rel="noopener">GitHub</a>
                        <a href="https://cnb.cool/xiaosicau/smartbanking" target="_blank" rel="noopener">CNB仓库</a>
                    </div>
                </div>
                <div className="index-footer-tech">
                    <span className="index-tech-badge">MiMo</span>
                    <span className="index-tech-badge">MCP</span>
                    <span className="index-tech-badge">Tushare</span>
                    <span className="index-tech-badge">World Bank</span>
                    <span className="index-tech-badge">Cloudflare Pages</span>
                </div>
                <div className="index-footer-bottom">
                    <p className="index-footer-text">
                        四川农业大学 · 数字经济系 · 肖诗顺 教授
                    </p>
                    <p className="index-footer-copyright">
                        &copy; 2026 SmartBank Agent. Built with Astro + Starlight.
                    </p>
                </div>
            </footer>
        </div>
    );
}

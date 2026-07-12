import React, { useState, useRef, useEffect, type FormEvent } from 'react';
import ThemeSwitcher from './ThemeSwitcher';

interface ToolCall {
    name: string;
    args: Record<string, string>;
    result: unknown;
}

interface Message {
    role: 'user' | 'assistant';
    content: string;
    toolCalls?: ToolCall[];
    loading?: boolean;
}

type ChatMode = 'general' | 'bmad-analyst' | 'bmad-pm' | 'bmad-architect' | 'bmad-dev' | 'bmad-qa' | 'debate';

const MODES: { key: ChatMode; label: string; icon: string; desc: string }[] = [
    { key: 'general', label: '通用', icon: '💬', desc: '金融问答与数据查询' },
    { key: 'bmad-analyst', label: '分析师', icon: '📋', desc: '需求分析师' },
    { key: 'bmad-pm', label: '产品', icon: '📊', desc: '产品经理' },
    { key: 'bmad-architect', label: '架构', icon: '🏗️', desc: '架构师' },
    { key: 'bmad-dev', label: '开发', icon: '💻', desc: '开发者' },
    { key: 'bmad-qa', label: 'QA', icon: '🔍', desc: '质量保障' },
    { key: 'debate', label: '辩论', icon: '⚔️', desc: '多空辩论' },
];

const SUGGESTIONS = [
    { icon: '📈', text: '查询贵州茅台最近5个交易日的收盘价' },
    { icon: '🌍', text: '对比中国和美国的GDP增长率' },
    { icon: '🏦', text: '查询上证指数今日行情' },
    { icon: '📚', text: '银行信贷审批的五级分类标准是什么' },
];

function speak(text: string) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text.replace(/[\*\#\|\`\>\-]/g, '').slice(0, 500));
    u.lang = 'zh-CN'; u.rate = 1;
    window.speechSynthesis.speak(u);
}

function exportChat(messages: Message[]) {
    const text = messages.map(m => `[${m.role === 'user' ? '用户' : '智能体'}]\n${m.content}`).join('\n\n---\n\n');
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'smartbank-chat-' + new Date().toISOString().slice(0, 10) + '.txt';
    a.click();
}

const TOOL_LABELS: Record<string, string> = {
    query_stock: '查询A股个股行情',
    query_stock_basic: '搜索股票代码',
    query_index: '查询指数行情',
    query_macro_gdp: '查询世界银行GDP数据',
    query_macro_indicator: '查询宏观指标',
};

function renderContent(text: string) {
    // Simple markdown: bold, code, tables (basic)
    const lines = text.split('\n');
    const elements: JSX.Element[] = [];
    let inTable = false;
    let tableRows: string[][] = [];

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];

        // Table detection
        if (line.includes('|') && line.trim().startsWith('|')) {
            const cells = line
                .split('|')
                .map((c) => c.trim())
                .filter((c) => c && !c.match(/^[-:]+$/));
            if (cells.length > 0) {
                if (!inTable) inTable = true;
                tableRows.push(cells);
                continue;
            }
        }

        if (inTable && tableRows.length > 0) {
            elements.push(
                <table key={`table-${i}`} className="msg-table">
                    <tbody>
                        {tableRows.map((row, ri) => (
                            <tr key={ri}>
                                {row.map((cell, ci) =>
                                    ri === 0 ? (
                                        <th key={ci}>{cell}</th>
                                    ) : (
                                        <td key={ci}>{cell}</td>
                                    )
                                )}
                            </tr>
                        ))}
                    </tbody>
                </table>
            );
            tableRows = [];
            inTable = false;
        }

        // Bold
        const formatted = line
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`(.*?)`/g, '<code>$1</code>');

        elements.push(
            <p
                key={i}
                dangerouslySetInnerHTML={{ __html: formatted || '&nbsp;' }}
            />
        );
    }

    if (tableRows.length > 0) {
        elements.push(
            <table key="table-end" className="msg-table">
                <tbody>
                    {tableRows.map((row, ri) => (
                        <tr key={ri}>
                            {row.map((cell, ci) =>
                                ri === 0 ? (
                                    <th key={ci}>{cell}</th>
                                ) : (
                                    <td key={ci}>{cell}</td>
                                )
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    }

    return <div className="msg-content">{elements}</div>;
}

export default function ChatAgent() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [mode, setMode] = useState<ChatMode>('general');
    const chatEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);
    const [speaking, setSpeaking] = useState(false);

    useEffect(() => {
        const check = () => setSpeaking(window.speechSynthesis?.speaking || false);
        const id = setInterval(check, 500);
        return () => clearInterval(id);
    }, []);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const sendDebate = async (topic: string) => {
        const userMsg: Message = { role: 'user', content: `⚖️ 辩论主题：${topic}` };
        const loadingMsg: Message = { role: 'assistant', content: '', loading: true };
        setMessages((prev) => [...prev, userMsg, loadingMsg]);
        setLoading(true);
        try {
            const resp = await fetch('/api/debate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic }),
            });
            if (!resp.ok) throw new Error('请求失败');
            const data = await resp.json();
            const content = `## ⚖️ 辩论：${data.topic}\n\n---\n\n### 🟢 多头观点\n${data.bull}\n\n---\n\n### 🔴 空头观点\n${data.bear}\n\n---\n\n### 📊 主持人综合裁决\n${data.moderator}`;
            setMessages((prev) => {
                const next = [...prev];
                next[next.length - 1] = { role: 'assistant', content };
                return next;
            });
        } catch (err) {
            setMessages((prev) => {
                const next = [...prev];
                next[next.length - 1] = { role: 'assistant', content: `辩论请求失败：${err instanceof Error ? err.message : '未知错误'}` };
                return next;
            });
        } finally { setLoading(false); inputRef.current?.focus(); }
    };

    const send = async (text?: string) => {
        const msg = (text || input).trim();
        if (!msg || loading) return;
        if (mode === 'debate') { setInput(''); sendDebate(msg); return; }

        setInput('');
        const userMsg: Message = { role: 'user', content: msg };
        const loadingMsg: Message = { role: 'assistant', content: '', loading: true };
        setMessages((prev) => [...prev, userMsg, loadingMsg]);
        setLoading(true);

        try {
            const history = [...messages, userMsg].map((m) => ({ role: m.role, content: m.content }));
            const resp = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: history, mode }),
            });
            if (!resp.ok) {
                const err = await resp.json().catch(() => ({ error: '请求失败' }));
                throw new Error(err.error || `HTTP ${resp.status}`);
            }
            const data = await resp.json();
            setMessages((prev) => {
                const next = [...prev];
                next[next.length - 1] = { role: 'assistant', content: data.content || '（无响应内容）', toolCalls: data.toolCalls };
                return next;
            });
        } catch (err) {
            setMessages((prev) => {
                const next = [...prev];
                next[next.length - 1] = { role: 'assistant', content: `抱歉，发生了错误：${err instanceof Error ? err.message : '未知错误'}。请稍后重试。` };
                return next;
            });
        } finally { setLoading(false); inputRef.current?.focus(); }
    };

    const onSubmit = (e: FormEvent) => {
        e.preventDefault();
        send();
    };

    const onKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            send();
        }
    };

    const currentMode = MODES.find(m => m.key === mode) || MODES[0];

    return (
        <div className="chat-container">
            {/* Header */}
            <header className="chat-header">
                <div className="header-left">
                    <div className="logo-icon">
                        <svg width="24" height="24" viewBox="0 0 32 32" fill="none">
                            <path d="M8 22V14L16 8L24 14V22H20V17H12V22H8Z" stroke="white" strokeWidth="1.5" fill="none" strokeLinejoin="round" />
                            <circle cx="16" cy="14" r="2" fill="white" opacity="0.8" />
                            <path d="M10 25H22" stroke="white" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />
                        </svg>
                    </div>
                    <div>
                        <h1>SmartBank Agent</h1>
                        <p className="subtitle">{currentMode.icon} {currentMode.label}模式 · 四川农业大学智慧银行实验室</p>
                    </div>
                </div>
                <div className="header-right">
                    <ThemeSwitcher />
                    {messages.length > 0 && (
                        <button className="icon-btn" title="导出对话" onClick={() => exportChat(messages)}>📥</button>
                    )}
                    <a href="/" className="back-link">返回主页</a>
                </div>
            </header>

            {/* Mode Selector */}
            <div className="mode-bar">
                {MODES.map(m => (
                    <button key={m.key} className={`mode-btn ${mode === m.key ? 'active' : ''}`} onClick={() => setMode(m.key)} title={m.desc}>
                        <span>{m.icon}</span>
                        <span className="mode-label">{m.label}</span>
                    </button>
                ))}
            </div>

            {/* Chat Area */}
            <main className="chat-main">
                {messages.length === 0 ? (
                    <div className="welcome">
                        <div className="welcome-icon">🏦</div>
                        <h2>欢迎使用 SmartBank Agent</h2>
                        <p>我是你的金融科技AI助手，可以查询实时金融数据、解答专业问题、指导 BMAD 项目开发。</p>
                        <p className="powered-by" style={{ marginTop: '-8px' }}>{currentMode.icon} 当前模式：{currentMode.label} - {currentMode.desc}</p>
                        <div className="suggestions">
                            {SUGGESTIONS.map((s, i) => (
                                <button
                                    key={i}
                                    className="suggestion-btn"
                                    onClick={() => send(s.text)}
                                    disabled={loading}
                                >
                                    <span className="suggestion-icon">{s.icon}</span>
                                    <span>{s.text}</span>
                                </button>
                            ))}
                        </div>
                        <p className="powered-by">Powered by MiMo · MCP · Tushare · World Bank</p>
                    </div>
                ) : (
                    <div className="messages">
                        {messages.map((msg, i) => (
                            <div key={i} className={`message ${msg.role}`}>
                                <div className="message-avatar">
                                    {msg.role === 'user' ? '👤' : '🏦'}
                                </div>
                                <div className="message-body">
                                    {msg.loading ? (
                                        <div className="typing-indicator">
                                            <span></span><span></span><span></span>
                                        </div>
                                    ) : (
                                        <>
                                            {msg.toolCalls && msg.toolCalls.length > 0 && (
                                                <div className="tool-calls">
                                                    {msg.toolCalls.map((tc, j) => (
                                                        <div key={j} className="tool-call">
                                                            <span className="tool-icon">🔧</span>
                                                            <span className="tool-name">
                                                                {TOOL_LABELS[tc.name] || tc.name}
                                                            </span>
                                                            <span className="tool-args">
                                                                {Object.entries(tc.args)
                                                                    .map(([k, v]) => `${k}=${v}`)
                                                                    .join(', ')}
                                                            </span>
                                                        </div>
                                                    ))}
                                                </div>
                                            )}
                                            {renderContent(msg.content)}
                                            <div className="msg-actions">
                                                <button className="msg-action-btn" title="朗读" onClick={() => speak(msg.content)}>🔊</button>
                                            </div>
                                        </>
                                    )}
                                </div>
                            </div>
                        ))}
                        <div ref={chatEndRef} />
                    </div>
                )}
            </main>

            {/* Input */}
            <form className="chat-input" onSubmit={onSubmit}>
                {speaking && (
                    <button type="button" className="icon-btn" onClick={() => window.speechSynthesis.cancel()} title="停止朗读">⏹️</button>
                )}
                <textarea
                    ref={inputRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={onKeyDown}
                    placeholder={mode === 'debate' ? '输入辩论主题，如：贵州茅台是否值得长期持有？' : '输入金融问题，如：查询贵州茅台最近股价...'}
                    rows={1}
                    disabled={loading}
                    name="message"
                    aria-label={mode === 'debate' ? '输入辩论主题' : '输入金融问题'}
                />
                <button type="submit" disabled={loading || !input.trim()}>
                    {loading ? '...' : '发送'}
                </button>
            </form>
        </div>
    );
}

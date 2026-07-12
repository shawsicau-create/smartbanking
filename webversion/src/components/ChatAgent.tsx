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
    { key: 'general', label: '通用问答', icon: '💬', desc: '金融问答与数据查询' },
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

// ── localStorage 历史记录管理 ────────────────────────────
const STORAGE_KEY = 'smartbank-chat-history';

function saveChatHistory(messages: Message[], mode: ChatMode) {
    try {
        const data = { messages, mode, timestamp: Date.now() };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
        console.warn('保存对话历史失败:', e);
    }
}

function loadChatHistory(): { messages: Message[]; mode: ChatMode } | null {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) return null;
        const data = JSON.parse(raw);
        if (data && Array.isArray(data.messages)) {
            return { messages: data.messages, mode: data.mode || 'general' };
        }
    } catch (e) {
        console.warn('加载对话历史失败:', e);
    }
    return null;
}

function clearChatHistory() {
    localStorage.removeItem(STORAGE_KEY);
}

const TOOL_LABELS: Record<string, string> = {
    query_stock: '查询A股个股行情',
    query_stock_basic: '搜索股票代码',
    query_index: '查询指数行情',
    query_macro_gdp: '查询世界银行GDP数据',
    query_macro_indicator: '查询宏观指标',
};

function renderInlineFormatting(text: string): string {
    // 处理行内格式：粗体、行内代码、链接、行内数学
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
        .replace(/\$([^$]+)\$/g, '<span class="msg-math">$1</span>');
}

function renderContent(text: string) {
    const lines = text.split('\n');
    const elements: React.ReactElement[] = [];
    let i = 0;

    while (i < lines.length) {
        const line = lines[i];
        const trimmed = line.trim();

        // 代码块检测 (```language ... ```)
        if (trimmed.startsWith('```')) {
            const langMatch = trimmed.match(/^```(\w*)/);
            const lang = langMatch ? langMatch[1] : '';
            const codeLines: string[] = [];
            i++;
            while (i < lines.length && !lines[i].trim().startsWith('```')) {
                codeLines.push(lines[i]);
                i++;
            }
            i++; // skip closing ```
            elements.push(
                <div key={`code-${elements.length}`} className="msg-code-block">
                    {lang && <div className="msg-code-lang">{lang}</div>}
                    <pre><code>{codeLines.join('\n')}</code></pre>
                </div>
            );
            continue;
        }

        // 表格检测
        if (trimmed.includes('|') && trimmed.startsWith('|')) {
            const tableRows: string[][] = [];
            while (i < lines.length && lines[i].trim().includes('|') && lines[i].trim().startsWith('|')) {
                const cells = lines[i]
                    .split('|')
                    .map((c) => c.trim())
                    .filter((c) => c && !c.match(/^[-:]+$/));
                if (cells.length > 0) {
                    tableRows.push(cells);
                }
                i++;
            }
            if (tableRows.length > 0) {
                elements.push(
                    <table key={`table-${elements.length}`} className="msg-table">
                        <tbody>
                            {tableRows.map((row, ri) => (
                                <tr key={ri}>
                                    {row.map((cell, ci) =>
                                        ri === 0 ? (
                                            <th key={ci} dangerouslySetInnerHTML={{ __html: renderInlineFormatting(cell) }} />
                                        ) : (
                                            <td key={ci} dangerouslySetInnerHTML={{ __html: renderInlineFormatting(cell) }} />
                                        )
                                    )}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                );
            }
            continue;
        }

        // 标题检测 (h1-h6)
        const headingMatch = trimmed.match(/^(#{1,6})\s+(.+)$/);
        if (headingMatch) {
            const level = headingMatch[1].length;
            const headingText = headingMatch[2];
            const className = `msg-h${level}`;
            elements.push(
                React.createElement(
                    `h${level}`,
                    {
                        key: `heading-${elements.length}`,
                        className,
                        dangerouslySetInnerHTML: { __html: renderInlineFormatting(headingText) }
                    }
                )
            );
            i++;
            continue;
        }

        // 分隔线检测 (--- 或 ***)
        if (trimmed.match(/^[-*]{3,}$/)) {
            elements.push(<hr key={`hr-${elements.length}`} className="msg-hr" />);
            i++;
            continue;
        }

        // 引用块检测 (> text)
        if (trimmed.startsWith('> ')) {
            const quoteLines: string[] = [];
            while (i < lines.length && lines[i].trim().startsWith('> ')) {
                quoteLines.push(lines[i].trim().substring(2));
                i++;
            }
            elements.push(
                <blockquote key={`quote-${elements.length}`} className="msg-blockquote">
                    {quoteLines.map((ql, qi) => (
                        <p key={qi} dangerouslySetInnerHTML={{ __html: renderInlineFormatting(ql) }} />
                    ))}
                </blockquote>
            );
            continue;
        }

        // 无序列表检测 (- item 或 * item)
        if (trimmed.match(/^[-*]\s+/)) {
            const listItems: string[] = [];
            while (i < lines.length && lines[i].trim().match(/^[-*]\s+/)) {
                listItems.push(lines[i].trim().replace(/^[-*]\s+/, ''));
                i++;
            }
            elements.push(
                <ul key={`ul-${elements.length}`} className="msg-list">
                    {listItems.map((item, li) => (
                        <li key={li} dangerouslySetInnerHTML={{ __html: renderInlineFormatting(item) }} />
                    ))}
                </ul>
            );
            continue;
        }

        // 有序列表检测 (1. item)
        if (trimmed.match(/^\d+\.\s+/)) {
            const listItems: string[] = [];
            while (i < lines.length && lines[i].trim().match(/^\d+\.\s+/)) {
                listItems.push(lines[i].trim().replace(/^\d+\.\s+/, ''));
                i++;
            }
            elements.push(
                <ol key={`ol-${elements.length}`} className="msg-ordered-list">
                    {listItems.map((item, li) => (
                        <li key={li} dangerouslySetInnerHTML={{ __html: renderInlineFormatting(item) }} />
                    ))}
                </ol>
            );
            continue;
        }

        // 空行
        if (trimmed === '') {
            i++;
            continue;
        }

        // 普通段落
        elements.push(
            <p
                key={`p-${elements.length}`}
                dangerouslySetInnerHTML={{ __html: renderInlineFormatting(trimmed) || '&nbsp;' }}
            />
        );
        i++;
    }

    return <div className="msg-content">{elements}</div>;
}

export default function ChatAgent() {
    // 初始化时从 localStorage 加载历史记录
    const [messages, setMessages] = useState<Message[]>(() => {
        const saved = loadChatHistory();
        return saved?.messages || [];
    });
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [mode, setMode] = useState<ChatMode>(() => {
        const saved = loadChatHistory();
        return saved?.mode || 'general';
    });
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

    // 消息或模式变化时自动保存到 localStorage
    useEffect(() => {
        if (messages.length > 0) {
            saveChatHistory(messages, mode);
        }
    }, [messages, mode]);

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
                        <>
                            <button className="icon-btn" title="导出对话" onClick={() => exportChat(messages)}>📥</button>
                            <button className="icon-btn" title="清除历史" onClick={() => {
                                clearChatHistory();
                                setMessages([]);
                                setMode('general');
                            }}>🗑️</button>
                        </>
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
                    {loading ? (
                        <span className="send-loading-dots"><span /><span /><span /></span>
                    ) : (
                        <>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M12 19V5M5 12l7-7 7 7" />
                            </svg>
                            发送
                        </>
                    )}
                </button>
            </form>
        </div>
    );
}

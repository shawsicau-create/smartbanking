import React, { useState, useRef, useEffect, type FormEvent } from 'react';

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

const SUGGESTIONS = [
    { icon: '📈', text: '查询贵州茅台最近5个交易日的收盘价' },
    { icon: '🌍', text: '对比中国和美国的GDP增长率' },
    { icon: '🏦', text: '查询上证指数今日行情' },
    { icon: '📚', text: '银行信贷审批的五级分类标准是什么' },
];

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
    const chatEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const send = async (text?: string) => {
        const msg = (text || input).trim();
        if (!msg || loading) return;

        setInput('');
        const userMsg: Message = { role: 'user', content: msg };
        const loadingMsg: Message = { role: 'assistant', content: '', loading: true };
        setMessages((prev) => [...prev, userMsg, loadingMsg]);
        setLoading(true);

        try {
            const history = [...messages, userMsg].map((m) => ({
                role: m.role,
                content: m.content,
            }));

            const resp = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: history }),
            });

            if (!resp.ok) {
                const err = await resp.json().catch(() => ({ error: '请求失败' }));
                throw new Error(err.error || `HTTP ${resp.status}`);
            }

            const data = await resp.json();
            setMessages((prev) => {
                const next = [...prev];
                next[next.length - 1] = {
                    role: 'assistant',
                    content: data.content || '（无响应内容）',
                    toolCalls: data.toolCalls,
                };
                return next;
            });
        } catch (err) {
            setMessages((prev) => {
                const next = [...prev];
                next[next.length - 1] = {
                    role: 'assistant',
                    content: `抱歉，发生了错误：${err instanceof Error ? err.message : '未知错误'}。请稍后重试。`,
                };
                return next;
            });
        } finally {
            setLoading(false);
            inputRef.current?.focus();
        }
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

    return (
        <div className="chat-container">
            {/* Header */}
            <header className="chat-header">
                <div className="header-left">
                    <div className="logo-icon">SB</div>
                    <div>
                        <h1>SmartBank Agent</h1>
                        <p className="subtitle">金融实验教学智能体 · 四川农业大学智慧银行实验室</p>
                    </div>
                </div>
                <a href={import.meta.env.BASE_URL} className="back-link">返回课程</a>
            </header>

            {/* Chat Area */}
            <main className="chat-main">
                {messages.length === 0 ? (
                    <div className="welcome">
                        <div className="welcome-icon">🏦</div>
                        <h2>欢迎使用 SmartBank Agent</h2>
                        <p>我可以帮你查询实时金融数据、解答金融专业问题、指导 BMAD 项目开发。</p>
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
                <textarea
                    ref={inputRef}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={onKeyDown}
                    placeholder="输入金融问题，如：查询贵州茅台最近股价..."
                    rows={1}
                    disabled={loading}
                    name="message"
                    aria-label="输入金融问题"
                />
                <button type="submit" disabled={loading || !input.trim()}>
                    {loading ? '...' : '发送'}
                </button>
            </form>
        </div>
    );
}

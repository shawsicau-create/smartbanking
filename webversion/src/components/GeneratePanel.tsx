import React, { useState } from 'react';
import ThemeSwitcher from './ThemeSwitcher';

interface Module {
    id: string;
    title: string;
    difficulty: string;
    topics: { id: string; title: string }[];
}

interface Content {
    moduleId: string;
    title: string;
    difficulty: string;
    content: string;
}

export default function GeneratePanel() {
    const [topic, setTopic] = useState('');
    const [outline, setOutline] = useState<{ title: string; modules: Module[] } | null>(null);
    const [contents, setContents] = useState<Content[]>([]);
    const [loading, setLoading] = useState(false);
    const [activeModule, setActiveModule] = useState<string | null>(null);
    const [error, setError] = useState('');

    const generate = async () => {
        if (!topic.trim()) return;
        setLoading(true);
        setError('');
        setOutline(null);
        setContents([]);
        try {
            const resp = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic }),
            });
            const data = await resp.json();
            if (data.error) throw new Error(data.error);
            setOutline(data.outline);
            setContents(data.contents || []);
            if (data.contents?.length > 0) setActiveModule(data.contents[0].moduleId);
        } catch (err) {
            setError(err instanceof Error ? err.message : '生成失败');
        } finally { setLoading(false); }
    };

    const activeContent = contents.find(c => c.moduleId === activeModule);

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
                        <h1>AI内容生成</h1>
                        <p className="subtitle">一键生成结构化教学大纲与内容</p>
                    </div>
                </div>
                <div className="header-right">
                    <ThemeSwitcher />
                    <a href="/" className="back-link">返回主页</a>
                </div>
            </header>

            <main className="chat-main">
                {!outline ? (
                    <div className="welcome">
                        <div className="welcome-icon">✨</div>
                        <h2>AI教学内容生成</h2>
                        <p>输入金融主题，AI自动设计教学大纲并生成详细内容</p>
                        <div className="generate-input-area">
                            <input
                                className="generate-input"
                                value={topic}
                                onChange={e => setTopic(e.target.value)}
                                placeholder="输入金融主题，如：商业银行资产负债管理"
                                onKeyDown={e => e.key === 'Enter' && generate()}
                                disabled={loading}
                            />
                            <button className="generate-btn" onClick={generate} disabled={loading || !topic.trim()}>
                                {loading ? '生成中...' : '开始生成'}
                            </button>
                        </div>
                        {error && <p className="error-text">{error}</p>}
                        <div className="generate-examples">
                            <p>示例主题：</p>
                            {['商业银行风险管理', '资产证券化原理与实务', '数字人民币与支付体系', '绿色金融与ESG投资'].map(t => (
                                <button key={t} className="example-chip" onClick={() => setTopic(t)} disabled={loading}>{t}</button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div className="generate-layout">
                        <aside className="generate-sidebar">
                            <h3>{outline.title}</h3>
                            <div className="module-list">
                                {outline.modules.map(m => {
                                    const hasContent = contents.some(c => c.moduleId === m.id);
                                    return (
                                        <button key={m.id} className={`module-item ${activeModule === m.id ? 'active' : ''} ${hasContent ? 'has-content' : ''}`} onClick={() => setActiveModule(m.id)}>
                                            <span className="module-title">{m.title}</span>
                                            <span className="module-diff">{m.difficulty}</span>
                                        </button>
                                    );
                                })}
                            </div>
                            <button className="generate-btn" style={{ marginTop: '12px', width: '100%' }} onClick={() => { setOutline(null); setContents([]); }}>
                                重新生成
                            </button>
                        </aside>
                        <section className="generate-content">
                            {activeContent ? (
                                <div className="content-article">
                                    <h2>{activeContent.title}</h2>
                                    <span className="content-diff">{activeContent.difficulty}</span>
                                    <div className="content-body" dangerouslySetInnerHTML={{ __html: activeContent.content.replace(/\n/g, '<br/>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
                                </div>
                            ) : (
                                <div className="content-placeholder">
                                    <p>选择一个模块查看生成内容</p>
                                </div>
                            )}
                        </section>
                    </div>
                )}
            </main>
        </div>
    );
}

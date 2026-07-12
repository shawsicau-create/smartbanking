import React, { useState } from 'react';

const BMAD_PHASES = [
    { id: 'analyst', icon: '📋', title: 'Phase 1: 需求分析', role: 'Analyst', desc: '定义用户故事、需求文档和验收标准', color: '#10b981' },
    { id: 'pm', icon: '📊', title: 'Phase 2: 产品规划', role: 'PM', desc: '制定路线图、PRD文档、优先级排序', color: '#3b82f6' },
    { id: 'architect', icon: '🏗️', title: 'Phase 3: 架构设计', role: 'Architect', desc: '系统架构、技术选型、API和数据库设计', color: '#8b5cf6' },
    { id: 'dev', icon: '💻', title: 'Phase 4: 开发实现', role: 'Developer', desc: '编码实现、单元测试、集成测试', color: '#f59e0b' },
    { id: 'qa', icon: '🔍', title: 'Phase 5: 质量保障', role: 'QA', desc: '测试用例设计、代码审查、质量报告', color: '#ef4444' },
];

const PROJECTS = [
    { id: 'crm', title: '银行CRM系统', desc: '基于BMAD方法论构建客户关系管理系统', phases: BMAD_PHASES.map(p => ({ ...p, status: 'pending' })) },
    { id: 'credit', title: '智能信贷审批', desc: '利用AI辅助信贷风险评估和审批流程', phases: BMAD_PHASES.map(p => ({ ...p, status: 'pending' })) },
    { id: 'fraud', title: '反欺诈检测系统', desc: '实时交易监控与异常行为识别平台', phases: BMAD_PHASES.map(p => ({ ...p, status: 'pending' })) },
    { id: 'wealth', title: '智能投顾平台', desc: '基于用户画像的个性化投资建议系统', phases: BMAD_PHASES.map(p => ({ ...p, status: 'pending' })) },
];

interface Phase {
    id: string;
    icon: string;
    title: string;
    role: string;
    desc: string;
    color: string;
    status: string;
}

interface Project {
    id: string;
    title: string;
    desc: string;
    phases: Phase[];
}

export default function PblDashboard() {
    const [selected, setSelected] = useState<Project | null>(null);
    const [activePhase, setActivePhase] = useState<string | null>(null);
    const [chatInput, setChatInput] = useState('');
    const [chatHistory, setChatHistory] = useState<{ role: string; content: string }[]>([]);
    const [loading, setLoading] = useState(false);

    const askBmad = async (text: string) => {
        if (!text.trim() || !activePhase) return;
        const userMsg = { role: 'user', content: text };
        setChatHistory(prev => [...prev, userMsg]);
        setChatInput('');
        setLoading(true);
        try {
            const mode = `bmad-${activePhase}`;
            const resp = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: [userMsg], mode }),
            });
            const data = await resp.json();
            setChatHistory(prev => [...prev, { role: 'assistant', content: data.content || '（无响应）' }]);
        } catch {
            setChatHistory(prev => [...prev, { role: 'assistant', content: '请求失败，请重试' }]);
        } finally { setLoading(false); }
    };

    if (selected) {
        const phase = selected.phases.find(p => p.id === activePhase);
        return (
            <div className="chat-container">
                <header className="chat-header">
                    <div className="header-left">
                        <button className="icon-btn" onClick={() => { setSelected(null); setActivePhase(null); setChatHistory([]); }}>←</button>
                        <div>
                            <h1>{selected.title}</h1>
                            <p className="subtitle">{selected.desc}</p>
                        </div>
                    </div>
                    <a href="/" className="back-link">返回主页</a>
                </header>
                <div className="pbl-phase-bar">
                    {selected.phases.map(p => (
                        <button key={p.id} className={`phase-btn ${activePhase === p.id ? 'active' : ''}`} style={activePhase === p.id ? { borderColor: p.color, color: p.color } : {}} onClick={() => { setActivePhase(p.id); setChatHistory([]); }}>
                            <span>{p.icon}</span>
                            <span className="phase-label">{p.role}</span>
                        </button>
                    ))}
                </div>
                {phase && (
                    <main className="chat-main">
                        <div className="pbl-phase-info" style={{ borderLeftColor: phase.color }}>
                            <h3>{phase.title}</h3>
                            <p>{phase.desc}</p>
                            <p className="pbl-hint">向 {phase.role} 提问，获取专业指导</p>
                        </div>
                        {chatHistory.length > 0 && (
                            <div className="messages">
                                {chatHistory.map((msg, i) => (
                                    <div key={i} className={`message ${msg.role}`}>
                                        <div className="message-avatar">{msg.role === 'user' ? '👤' : '🏦'}</div>
                                        <div className="message-body">
                                            <div className="msg-content">
                                                <p>{msg.content}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </main>
                )}
                <form className="chat-input" onSubmit={e => { e.preventDefault(); askBmad(chatInput); }}>
                    <textarea value={chatInput} onChange={e => setChatInput(e.target.value)} placeholder={phase ? `向${phase.role}提问...` : '选择阶段后提问'} rows={1} disabled={loading || !activePhase} />
                    <button type="submit" disabled={loading || !chatInput.trim()}>{loading ? '...' : '发送'}</button>
                </form>
            </div>
        );
    }

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
                        <h1>BMAD项目指导</h1>
                        <p className="subtitle">问题驱动式学习 · 全流程项目实战</p>
                    </div>
                </div>
                <a href="/" className="back-link">返回主页</a>
            </header>
            <main className="chat-main">
                <div className="welcome">
                    <div className="welcome-icon">🎯</div>
                    <h2>选择一个项目开始实战</h2>
                    <p>基于BMAD方法论，体验从需求分析到质量保障的全流程项目开发</p>
                </div>
                <div className="pbl-grid">
                    {PROJECTS.map(p => (
                        <button key={p.id} className="pbl-card" onClick={() => { setSelected(p); setActivePhase('analyst'); setChatHistory([]); }}>
                            <div className="pbl-card-header">
                                <span className="pbl-card-icon">{p.phases[0].icon}</span>
                                <h3>{p.title}</h3>
                            </div>
                            <p>{p.desc}</p>
                            <div className="pbl-phases-preview">
                                {p.phases.map(ph => (
                                    <span key={ph.id} className="phase-dot" style={{ background: ph.color }} title={ph.title} />
                                ))}
                            </div>
                        </button>
                    ))}
                </div>
            </main>
        </div>
    );
}

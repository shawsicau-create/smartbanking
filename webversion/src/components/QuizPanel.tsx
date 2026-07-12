import React, { useState } from 'react';

interface Question {
    id: string;
    question: string;
    options: string[];
    answer: string;
    explanation: string;
}

const TOPICS = ['商业银行风险管理', '证券投资分析', '国际金融与汇率', '金融科技与区块链', '信贷审批实务', '资产定价理论'];
const DIFFICULTIES = ['基础', '进阶', '高级'];

export default function QuizPanel() {
    const [questions, setQuestions] = useState<Question[]>([]);
    const [current, setCurrent] = useState(0);
    const [selected, setSelected] = useState<string | null>(null);
    const [showResult, setShowResult] = useState(false);
    const [score, setScore] = useState(0);
    const [loading, setLoading] = useState(false);
    const [topic, setTopic] = useState(TOPICS[0]);
    const [difficulty, setDifficulty] = useState(DIFFICULTIES[0]);
    const [count, setCount] = useState(5);

    const generate = async () => {
        setLoading(true);
        setSelected(null);
        setShowResult(false);
        setCurrent(0);
        setScore(0);
        try {
            const resp = await fetch('/api/quiz', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic, difficulty, count }),
            });
            const data = await resp.json();
            setQuestions(data.questions || []);
        } catch {
            setQuestions([]);
        } finally { setLoading(false); }
    };

    const submit = () => {
        if (!selected) return;
        setShowResult(true);
        if (selected === questions[current].answer) setScore(s => s + 1);
    };

    const next = () => {
        if (current < questions.length - 1) {
            setCurrent(c => c + 1);
            setSelected(null);
            setShowResult(false);
        }
    };

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
                        <h1>金融测验</h1>
                        <p className="subtitle">AI生成选择题 · 支持多种难度</p>
                    </div>
                </div>
                <a href="/" className="back-link">返回主页</a>
            </header>

            <main className="chat-main">
                {questions.length === 0 ? (
                    <div className="welcome">
                        <div className="welcome-icon">📝</div>
                        <h2>AI金融测验</h2>
                        <p>选择主题和难度，AI为你生成专属测验题</p>
                        <div className="quiz-config">
                            <div className="config-row">
                                <label>主题</label>
                                <select value={topic} onChange={e => setTopic(e.target.value)}>
                                    {TOPICS.map(t => <option key={t} value={t}>{t}</option>)}
                                </select>
                            </div>
                            <div className="config-row">
                                <label>难度</label>
                                <div className="btn-group">
                                    {DIFFICULTIES.map(d => (
                                        <button key={d} className={`btn-option ${difficulty === d ? 'active' : ''}`} onClick={() => setDifficulty(d)}>{d}</button>
                                    ))}
                                </div>
                            </div>
                            <div className="config-row">
                                <label>题数</label>
                                <select value={count} onChange={e => setCount(Number(e.target.value))}>
                                    {[3, 5, 8, 10].map(n => <option key={n} value={n}>{n}题</option>)}
                                </select>
                            </div>
                            <button className="generate-btn" onClick={generate} disabled={loading}>
                                {loading ? '生成中...' : '开始测验'}
                            </button>
                        </div>
                    </div>
                ) : current < questions.length ? (
                    <div className="quiz-area">
                        <div className="quiz-progress">
                            <span>第 {current + 1}/{questions.length} 题</span>
                            <span className="quiz-score">得分：{score}/{questions.length}</span>
                        </div>
                        <div className="quiz-question">
                            <h3>{questions[current].question}</h3>
                        </div>
                        <div className="quiz-options">
                            {questions[current].options.map((opt, i) => {
                                const letter = String.fromCharCode(65 + i);
                                const isCorrect = letter === questions[current].answer;
                                const isSelected = selected === letter;
                                let cls = 'quiz-option';
                                if (showResult) {
                                    if (isCorrect) cls += ' correct';
                                    else if (isSelected && !isCorrect) cls += ' wrong';
                                } else if (isSelected) cls += ' selected';
                                return (
                                    <button key={i} className={cls} onClick={() => !showResult && setSelected(letter)}>
                                        <span className="option-letter">{letter}</span>
                                        <span>{opt.replace(/^[A-D]\.\s*/, '')}</span>
                                    </button>
                                );
                            })}
                        </div>
                        {showResult && (
                            <div className="quiz-explanation">
                                <p><strong>解析：</strong>{questions[current].explanation}</p>
                            </div>
                        )}
                        <div className="quiz-actions">
                            {!showResult ? (
                                <button className="generate-btn" onClick={submit} disabled={!selected}>提交答案</button>
                            ) : current < questions.length - 1 ? (
                                <button className="generate-btn" onClick={next}>下一题</button>
                            ) : (
                                <div className="quiz-final">
                                    <h3>测验完成！</h3>
                                    <p>总得分：{score}/{questions.length} ({Math.round(score / questions.length * 100)}分)</p>
                                    <button className="generate-btn" onClick={() => setQuestions([])}>重新开始</button>
                                </div>
                            )}
                        </div>
                    </div>
                ) : null}
            </main>
        </div>
    );
}

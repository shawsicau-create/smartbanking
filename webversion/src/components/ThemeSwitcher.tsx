import React, { useState, useEffect, useRef } from 'react';

const THEMES = [
    { key: 'terminal', label: 'Terminal', desc: 'Bloomberg终端风格', color: '#10b981', emoji: '🖥️' },
    { key: 'ocean', label: 'Ocean', desc: 'Coursera学术蓝', color: '#3b82f6', emoji: '🌊' },
    { key: 'ember', label: 'Ember', desc: 'MasterClass奢华金', color: '#f59e0b', emoji: '🔥' },
    { key: 'nebula', label: 'Nebula', desc: 'Stripe未来紫', color: '#8b5cf6', emoji: '🌌' },
];

export default function ThemeSwitcher() {
    const [current, setCurrent] = useState('terminal');
    const [open, setOpen] = useState(false);
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const saved = localStorage.getItem('sb-theme') || 'terminal';
        document.documentElement.setAttribute('data-theme', saved);
        setCurrent(saved);
    }, []);

    useEffect(() => {
        const handler = (e: MouseEvent) => {
            if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
        };
        document.addEventListener('mousedown', handler);
        return () => document.removeEventListener('mousedown', handler);
    }, []);

    const select = (key: string) => {
        document.documentElement.setAttribute('data-theme', key);
        localStorage.setItem('sb-theme', key);
        setCurrent(key);
        setOpen(false);
    };

    const currentTheme = THEMES.find(t => t.key === current) || THEMES[0];

    return (
        <div className="theme-switcher" ref={ref}>
            <button
                className="theme-switcher-btn"
                onClick={() => setOpen(!open)}
                title="切换配色方案"
                aria-label="切换配色方案"
            >
                <span className="theme-color-dot" style={{ background: currentTheme.color }} />
                <span className="theme-switcher-label">{currentTheme.label}</span>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M6 9l6 6 6-6" /></svg>
            </button>
            {open && (
                <div className="theme-dropdown">
                    {THEMES.map(t => (
                        <button
                            key={t.key}
                            className={`theme-option ${current === t.key ? 'active' : ''}`}
                            onClick={() => select(t.key)}
                        >
                            <span className="theme-option-dot" style={{ background: t.color }} />
                            <div className="theme-option-info">
                                <span className="theme-option-name">{t.emoji} {t.label}</span>
                                <span className="theme-option-desc">{t.desc}</span>
                            </div>
                            {current === t.key && (
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M20 6L9 17l-5-5" /></svg>
                            )}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}

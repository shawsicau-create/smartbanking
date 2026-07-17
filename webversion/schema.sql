-- SmartBank Agent 数据库表结构

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,                    -- GitHub ID
    username TEXT NOT NULL,                 -- GitHub 用户名
    avatar_url TEXT,                        -- 头像 URL
    email TEXT,                             -- 邮箱
    role TEXT DEFAULT 'student',            -- 角色: student/teacher
    credits INTEGER DEFAULT 100,            -- 积分余额
    daily_used INTEGER DEFAULT 0,           -- 今日已用次数
    daily_reset_date DATE,                  -- 每日重置日期
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 对话历史表
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    title TEXT DEFAULT '新对话',            -- 对话标题
    mode TEXT NOT NULL DEFAULT 'general',   -- 对话模式
    messages TEXT NOT NULL,                 -- JSON 格式的消息数组
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 积分日志表
CREATE TABLE IF NOT EXISTS credit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    amount INTEGER NOT NULL,                -- 正数=充值，负数=消耗
    reason TEXT,                            -- 原因描述
    balance_after INTEGER,                  -- 变动后余额
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Magic Link 登录令牌表
CREATE TABLE IF NOT EXISTS magic_tokens (
    token TEXT PRIMARY KEY,                 -- UUID 格式的登录令牌
    email TEXT NOT NULL,                    -- 关联的邮箱
    expires_at DATETIME NOT NULL,           -- 过期时间
    used INTEGER DEFAULT 0,                 -- 是否已使用
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX IF NOT EXISTS idx_credit_logs_user_id ON credit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_users_daily_reset ON users(daily_reset_date);
CREATE INDEX IF NOT EXISTS idx_magic_tokens_email ON magic_tokens(email);
CREATE INDEX IF NOT EXISTS idx_magic_tokens_expires ON magic_tokens(expires_at);

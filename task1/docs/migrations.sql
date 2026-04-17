-- 1. 用户表
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('professor', 'student')),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 2. 分类表
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    priority INTEGER DEFAULT 5,
    keywords TEXT[] DEFAULT ARRAY[]::TEXT[]
);

INSERT INTO categories (name, priority, keywords) VALUES
    ('学术问题', 1, ARRAY['作业', '考试', '课程', '成绩', '学分', '论文', '项目', '实验']::TEXT[]),
    ('行政事务', 2, ARRAY['请假', '证明', '注册', '退课', '选课', '缴费']::TEXT[]),
    ('常见问题', 3, ARRAY['时间', '地点', '办公', '咨询', '截止']::TEXT[]),
    ('其他', 5, ARRAY[]::TEXT[])
ON CONFLICT DO NOTHING;

-- 3. 资料源表
CREATE TABLE IF NOT EXISTS knowledge_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50),
    keywords TEXT[] DEFAULT ARRAY[]::TEXT[],
    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. 邮件表
CREATE TABLE IF NOT EXISTS emails (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    sender_email VARCHAR(255) NOT NULL,
    sender_name VARCHAR(100),
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    is_duplicate BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'classified', 'replied', 'approved', 'sent')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_emails_status ON emails(status);

-- 5. 回复表
CREATE TABLE IF NOT EXISTS replies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_id UUID NOT NULL REFERENCES emails(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_auto BOOLEAN DEFAULT TRUE,
    is_approved BOOLEAN DEFAULT FALSE,
    referenced_sources UUID[] DEFAULT ARRAY[]::UUID[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

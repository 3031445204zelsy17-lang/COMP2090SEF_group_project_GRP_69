/**
 * API 封装
 */

const API_BASE = '/api';

/**
 * 获取认证请求头（包含 Authorization 和 Content-Type）
 */
function getAuthHeaders(includeContentType = true) {
    const headers = {};
    const token = localStorage.getItem('token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    if (includeContentType) {
        headers['Content-Type'] = 'application/json';
    }
    return headers;
}

const API = {
    auth: {
        async login(email, password) {
            const response = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify({ email, password }),
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || '登录失败');
            }
            return response.json();
        },

        async register(name, email, password, role) {
            const response = await fetch(`${API_BASE}/auth/register`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify({ name, email, password, role }),
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || '注册失败');
            }
            return response.json();
        },
    },

    emails: {
        async list(params = {}) {
            const query = new URLSearchParams(params).toString();
            const response = await fetch(`${API_BASE}/emails?${query}`, {
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('获取邮件失败');
            return response.json();
        },

        async get(id) {
            const response = await fetch(`${API_BASE}/emails/${id}`, {
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('获取邮件失败');
            return response.json();
        },

        async create(data) {
            const response = await fetch(`${API_BASE}/emails`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || '创建邮件失败');
            }
            return response.json();
        },

        async updateCategory(id, categoryId) {
            const response = await fetch(`${API_BASE}/emails/${id}/category`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify({ category_id: categoryId }),
            });
            if (!response.ok) throw new Error('更新分类失败');
            return response.json();
        },
    },

    replies: {
        async getOrGenerate(emailId) {
            const response = await fetch(`${API_BASE}/emails/${emailId}/reply`, {
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('获取回复失败');
            return response.json();
        },

        async generate(emailId) {
            const response = await fetch(`${API_BASE}/emails/${emailId}/generate`, {
                method: 'POST',
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('生成回复失败');
            return response.json();
        },

        async update(replyId, content) {
            const response = await fetch(`${API_BASE}/replies/${replyId}`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify({ content }),
            });
            if (!response.ok) throw new Error('更新回复失败');
            return response.json();
        },

        async approve(replyId) {
            const response = await fetch(`${API_BASE}/replies/${replyId}/approve`, {
                method: 'POST',
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('审核失败');
            return response.json();
        },

        async chat(replyId, message) {
            const response = await fetch(`${API_BASE}/replies/${replyId}/chat`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify({ message }),
            });
            if (!response.ok) throw new Error('对话编辑失败');
            return response.json();
        },

        async send(replyId) {
            const response = await fetch(`${API_BASE}/replies/${replyId}/send`, {
                method: 'POST',
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('发送失败');
            return response.json();
        },

        async regenerate(emailId) {
            const response = await fetch(`${API_BASE}/emails/${emailId}/regenerate`, {
                method: 'POST',
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('重新生成失败');
            return response.json();
        },
    },

    knowledge: {
        async list() {
            const response = await fetch(`${API_BASE}/knowledge`, {
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('获取资料源失败');
            return response.json();
        },

        async get(id) {
            const response = await fetch(`${API_BASE}/knowledge/${id}`, {
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('获取资料源失败');
            return response.json();
        },

        async create(data) {
            const response = await fetch(`${API_BASE}/knowledge`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || '创建资料源失败');
            }
            return response.json();
        },

        async update(id, data) {
            const response = await fetch(`${API_BASE}/knowledge/${id}`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify(data),
            });
            if (!response.ok) throw new Error('更新资料源失败');
            return response.json();
        },

        async delete(id) {
            const response = await fetch(`${API_BASE}/knowledge/${id}`, {
                method: 'DELETE',
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('删除资料源失败');
            return response.json();
        },
    },

    stats: {
        async get() {
            const response = await fetch(`${API_BASE}/stats`, {
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('获取统计失败');
            return response.json();
        },

        async dashboard() {
            const response = await fetch(`${API_BASE}/stats/dashboard`, {
                headers: getAuthHeaders(false),
            });
            if (!response.ok) throw new Error('获取仪表盘数据失败');
            return response.json();
        },
    },
};

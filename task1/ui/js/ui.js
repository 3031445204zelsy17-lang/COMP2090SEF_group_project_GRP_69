/**
 * UI 工具函数
 */

const UI = {
    // 显示 Toast 通知
    toast(message, type = 'info', duration = 3000) {
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:8px;';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.style.cssText = 'padding:12px 20px;border-radius:8px;font-size:14px;color:#fff;min-width:200px;box-shadow:0 4px 12px rgba(0,0,0,0.15);transition:opacity 0.3s;opacity:1;';

        const colors = { success: '#10b981', error: '#ef4444', info: '#3b82f6', warning: '#f59e0b' };
        toast.style.background = colors[type] || colors.info;
        toast.textContent = message;

        container.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },

    // 显示加载状态
    showLoading(element) {
        element.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">⏳</div>
                <div class="empty-state-title">${t('loading')}</div>
            </div>
        `;
    },

    // 显示空状态
    showEmpty(container, icon, title, text) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">${icon}</div>
                <div class="empty-state-title">${title}</div>
                <div class="empty-state-text">${text}</div>
            </div>
        `;
    },

    // 显示错误
    showError(container, message) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">❌</div>
                <div class="empty-state-title">${t('error')}</div>
                <div class="empty-state-text">${message}</div>
            </div>
        `;
    },

    // 格式化时间
    formatTime(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;

        if (diff < 60000) return t('just_now');
        if (diff < 3600000) return `${Math.floor(diff / 60000)}${t('minutes_ago')}`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}${t('hours_ago')}`;
        if (diff < 604800000) return `${Math.floor(diff / 86400000)}${t('days_ago')}`;

        const locale = currentLang() === 'zh' ? 'zh-CN' : 'en-US';
        return date.toLocaleDateString(locale);
    },

    // 渲染邮件卡片
    renderEmailCard(email) {
        const tags = [];

        if (email.category) {
            tags.push(`<span class="tag tag-category">${this.escapeHtml(email.category.name)}</span>`);
        }

        if (email.is_duplicate) {
            tags.push(`<span class="tag tag-duplicate">${t('duplicate_tag')}</span>`);
        }

        const statusMap = {
            pending:    { text: t('status_pending'),    class: 'tag-status' },
            classified: { text: t('status_classified'), class: 'tag-status' },
            replied:    { text: t('status_replied'),    class: 'tag-status' },
            approved:   { text: t('status_approved'),   class: 'tag-status' },
            sent:       { text: t('status_sent'),       class: 'tag-status' },
        };

        const status = statusMap[email.status] || statusMap.pending;
        tags.push(`<span class="tag ${status.class}">${status.text}</span>`);

        return `
            <div class="email-card" data-id="${email.id}">
                <div class="email-card-header">
                    <div class="email-subject">${this.escapeHtml(email.subject)}</div>
                </div>
                <div class="email-meta">
                    <span class="email-sender">${this.escapeHtml(email.sender_name || email.sender_email)}</span>
                    <span class="email-time">${this.formatTime(email.created_at)}</span>
                </div>
                <div class="email-preview">${this.escapeHtml(email.body.substring(0, 100))}...</div>
                <div class="email-tags">${tags.join('')}</div>
            </div>
        `;
    },

    // 渲染已发送邮件卡片
    renderSentEmailCard(email) {
        const tags = [];

        if (email.category) {
            tags.push(`<span class="tag tag-category">${this.escapeHtml(email.category.name)}</span>`);
        }

        tags.push(`<span class="tag tag-sent">${t('status_sent_check')}</span>`);

        return `
            <div class="email-card sent" data-id="${email.id}">
                <div class="email-card-header">
                    <div class="email-subject">Re: ${this.escapeHtml(email.subject)}</div>
                </div>
                <div class="email-meta">
                    <span class="email-sender">${t('recipient_label')}${this.escapeHtml(email.sender_name || email.sender_email)}</span>
                    <span class="email-time">${this.formatTime(email.updated_at || email.created_at)}</span>
                </div>
                <div class="email-tags">${tags.join('')}</div>
            </div>
        `;
    },

    // 渲染资料源卡片
    renderSourceCard(source) {
        const keywords = source.keywords.map(kw =>
            `<span class="keyword-tag">${this.escapeHtml(kw)}</span>`
        ).join('');

        return `
            <div class="source-card" data-id="${source.id}">
                <div class="source-card-header">
                    <div class="source-title">${this.escapeHtml(source.title)}</div>
                    <div class="source-actions">
                        <button class="btn btn-sm btn-secondary" onclick="App.editSource('${source.id}')">${t('edit_btn')}</button>
                        <button class="btn btn-sm btn-danger" onclick="App.deleteSource('${source.id}')">${t('delete_btn')}</button>
                    </div>
                </div>
                <div class="source-content">${this.escapeHtml(source.content)}</div>
                <div class="source-keywords">${keywords}</div>
            </div>
        `;
    },

    // 渲染统计卡片
    renderStatCard(value, label) {
        return `
            <div class="stat-card">
                <div class="stat-value">${value}</div>
                <div class="stat-label">${label}</div>
            </div>
        `;
    },

    // HTML 转义
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    // 显示模态框
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            // Re-apply translations for modal content
            applyLang();
        }
    },

    // 隐藏模态框
    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
        }
    },

    // 初始化模态框关闭事件
    initModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });

            const closeBtn = modal.querySelector('.modal-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    modal.classList.remove('active');
                });
            }

            const cancelBtn = modal.querySelector('.modal-cancel');
            if (cancelBtn) {
                cancelBtn.addEventListener('click', () => {
                    modal.classList.remove('active');
                });
            }
        });
    },
};

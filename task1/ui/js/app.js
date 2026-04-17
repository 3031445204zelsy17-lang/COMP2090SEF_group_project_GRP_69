/**
 * 主应用逻辑
 */

const App = {
    state: {
        currentView: 'inbox',
        emails: [],
        selectedEmail: null,
        sources: [],
        stats: null,
    },

    // 初始化
    async init() {
        // 登录校验
        const token = localStorage.getItem('token');
        if (!token) {
            window.location.href = '/ui/login.html';
            return;
        }

        console.log('App initialized');

        // 初始化移动端菜单
        this.initMobileMenu();

        // 初始化模态框
        UI.initModals();

        // 绑定导航事件
        this.bindNavigation();

        // 绑定模态框事件
        this.bindModals();

        // 加载初始数据
        await this.loadInbox();

        // 退出按钮
        document.getElementById('logoutBtn')?.addEventListener('click', () => {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/ui/login.html';
        });

        // 显示用户名
        try {
            const user = JSON.parse(localStorage.getItem('user') || '{}');
            const userNameEl = document.getElementById('userName');
            if (userNameEl && user.name) {
                userNameEl.textContent = user.name;
            }
        } catch (e) {}
    },

    // 初始化移动端菜单
    initMobileMenu() {
        const menuToggle = document.getElementById('menuToggle');
        const overlay = document.getElementById('sidebarOverlay');
        const sidebar = document.querySelector('.sidebar');
        const logoutMobile = document.getElementById('logoutBtnMobile');

        if (menuToggle) {
            menuToggle.addEventListener('click', () => {
                sidebar.classList.add('active');
                overlay.classList.add('active');
            });
        }

        if (overlay) {
            overlay.addEventListener('click', () => {
                sidebar.classList.remove('active');
                overlay.classList.remove('active');
            });
        }

        if (logoutMobile) {
            logoutMobile.addEventListener('click', () => {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                window.location.href = '/ui/login.html';
            });
        }

        // 点击导航项时自动关闭移动端侧边栏
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('active');
                    overlay.classList.remove('active');
                }
            });
        });
    },

    // 绑定导航
    bindNavigation() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const view = item.dataset.view;
                this.switchView(view);
            });
        });
    },

    // 切换视图
    async switchView(view) {
        // 关闭所有 Modal
        document.querySelectorAll('.modal.active').forEach(m => m.classList.remove('active'));

        // 更新导航状态
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.view === view);
        });

        this.state.currentView = view;

        // 加载对应视图
        switch (view) {
            case 'inbox':
                await this.loadInbox();
                break;
            case 'sent':
                await this.loadSent();
                break;
            case 'knowledge':
                await this.loadKnowledge();
                break;
            case 'stats':
                await this.loadStats();
                break;
        }
    },

    // 加载收件箱
    async loadInbox() {
        const container = document.getElementById('mainContent');
        UI.showLoading(container);

        try {
            const emails = await API.emails.list({ limit: 50 });
            // 收件箱显示所有未发送的邮件（包括待处理、已分类、已回复）
            const inboxEmails = emails.filter(e => e.status !== 'sent');
            this.state.emails = inboxEmails;

            // 更新待处理数量
            const pendingCount = inboxEmails.filter(e => e.status === 'pending').length;
            document.getElementById('pendingCount').textContent = pendingCount;

            if (inboxEmails.length === 0) {
                UI.showEmpty(container, '📭', t('inbox_empty_title'), t('inbox_empty_text'));
                return;
            }

            container.innerHTML = `
                <div class="content-header">
                    <h1>${t('inbox_title')}</h1>
                    <button class="btn btn-primary" id="newEmailBtn">${t('new_email_btn')}</button>
                </div>
                <div class="content-body">
                    <div class="email-list">
                        ${inboxEmails.map(email => UI.renderEmailCard(email)).join('')}
                    </div>
                </div>
            `;

            // 在按钮渲染后绑定事件
            document.getElementById('newEmailBtn')?.addEventListener('click', () => {
                UI.showModal('newEmailModal');
            });

            // 绑定邮件点击事件
            container.querySelectorAll('.email-card').forEach(card => {
                card.addEventListener('click', () => {
                    this.showEmailDetail(card.dataset.id);
                });
            });

        } catch (error) {
            UI.showError(container, error.message);
        }
    },

    // 加载已发送
    async loadSent() {
        const container = document.getElementById('mainContent');
        UI.showLoading(container);

        try {
            const emails = await API.emails.list({ status: 'sent', limit: 50 });

            if (emails.length === 0) {
                container.innerHTML = `
                    <div class="content-header">
                        <h1>${t('sent_title')}</h1>
                    </div>
                    <div class="content-body">
                        <div class="empty-state">
                            <div class="empty-state-icon">📤</div>
                            <div class="empty-state-title">${t('sent_empty_title')}</div>
                            <div class="empty-state-text">${t('sent_empty_text')}</div>
                        </div>
                    </div>
                `;
                return;
            }

            container.innerHTML = `
                <div class="content-header">
                    <h1>${t('sent_title')}</h1>
                </div>
                <div class="content-body">
                    <div class="email-list">
                        ${emails.map(email => UI.renderSentEmailCard(email)).join('')}
                    </div>
                </div>
            `;

        } catch (error) {
            UI.showError(container, error.message);
        }
    },

    // 显示邮件详情
    async showEmailDetail(emailId) {
        const container = document.getElementById('mainContent');
        UI.showLoading(container);

        try {
            const email = await API.emails.get(emailId);

            // 检查是否已有回复
            let reply = null;
            try {
                reply = await API.replies.getOrGenerate(emailId);
            } catch (e) {
                // 没有回复
            }

            this.state.selectedEmail = { email, reply };

            // 如果没有回复，显示生成按钮
            if (!reply) {
                container.innerHTML = `
                    <div class="content-header">
                        <button class="btn btn-secondary" onclick="App.switchView('inbox')">${t('back')}</button>
                        <h1>${t('email_detail_title')}</h1>
                    </div>
                    <div class="content-body">
                        <div class="email-detail-container">
                            <!-- 左侧：原始邮件 -->
                            <div class="detail-left">
                                <div class="email-detail">
                                    <div class="detail-header">
                                        <div class="detail-subject">${UI.escapeHtml(email.subject)}</div>
                                        <div class="detail-meta">
                                            <span>${t('sender_label')}${UI.escapeHtml(email.sender_name || email.sender_email)}</span>
                                            <span>${t('time_label')}${UI.formatTime(email.created_at)}</span>
                                        </div>
                                    </div>
                                    <div class="detail-body">${UI.escapeHtml(email.body)}</div>
                                </div>

                                <!-- 生成回复按钮 -->
                                <div class="reply-empty">
                                    <div class="empty-state">
                                        <div class="empty-state-icon">🤖</div>
                                        <div class="empty-state-title">${t('no_reply_title')}</div>
                                        <div class="empty-state-text">${t('no_reply_text')}</div>
                                        <button class="btn btn-primary btn-large" onclick="App.generateReply()">
                                            ${t('generate_reply_btn')}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                return;
            }

            // 有回复，显示双栏布局 + 对话面板
            const sourcesHtml = reply.referenced_sources?.length > 0
                ? reply.referenced_sources.map(s => `<span class="source-tag">${UI.escapeHtml(s.title)}</span>`).join('')
                : `<span class="text-muted">${t('ref_none')}</span>`;

            container.innerHTML = `
                <div class="content-header">
                    <button class="btn btn-secondary" onclick="App.switchView('inbox')">${t('back')}</button>
                    <h1>${t('email_detail_title')}</h1>
                </div>
                <div class="content-body">
                    <div class="email-detail-container">
                        <!-- 左侧：原始邮件 + 回复预览 -->
                        <div class="detail-left">
                            <div class="email-detail">
                                <div class="detail-header">
                                    <div class="detail-subject">${UI.escapeHtml(email.subject)}</div>
                                    <div class="detail-meta">
                                        <span>${t('sender_label')}${UI.escapeHtml(email.sender_name || email.sender_email)}</span>
                                        <span>${t('time_label')}${UI.formatTime(email.created_at)}</span>
                                    </div>
                                </div>
                                <div class="detail-body">${UI.escapeHtml(email.body)}</div>
                            </div>

                            <!-- 回复预览 -->
                            <div class="reply-preview">
                                <div class="reply-preview-header">
                                    <h3>${t('reply_section')}</h3>
                                    <span class="status-badge ${reply.is_approved ? 'approved' : 'pending'}">
                                        ${reply.is_approved ? t('approved_badge') : t('pending_badge')}
                                    </span>
                                </div>
                                <textarea id="replyContent" class="reply-textarea">${UI.escapeHtml(reply.content)}</textarea>
                                <div class="reply-sources">
                                    <span class="sources-label">${t('ref_sources')}</span>
                                    ${sourcesHtml}
                                </div>
                            </div>
                        </div>

                        <!-- 右侧：对话面板 -->
                        <div class="chat-panel">
                            <div class="chat-header">
                                ${t('chat_header')}
                            </div>

                            <div class="chat-messages" id="chatMessages">
                                <div class="message assistant">
                                    ${t('chat_intro')}
                                    <br>• ${t('chat_hint_en')}
                                    <br>• ${t('chat_hint_formal')}
                                    <br>• ${t('chat_hint_add')}
                                </div>
                            </div>

                            <div class="chat-input-area">
                                <input type="text" id="chatInput" placeholder="${t('chat_placeholder')}" onkeypress="if(event.key==='Enter')App.sendChatMessage()">
                                <button class="btn btn-primary" onclick="App.sendChatMessage()">${t('send_btn')}</button>
                            </div>

                            <div class="chat-actions">
                                <button class="btn btn-secondary" onclick="App.regenerateReply()">${t('regen_btn')}</button>
                                <button class="btn btn-success" onclick="App.approveAndSend()">${t('approve_send_btn')}</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

        } catch (error) {
            UI.showError(container, error.message);
        }
    },

    // 生成回复
    async generateReply() {
        if (!this.state.selectedEmail) return;

        const container = document.getElementById('mainContent');
        UI.showLoading(container);

        try {
            await API.replies.generate(this.state.selectedEmail.email.id);
            // 重新加载详情页
            await this.showEmailDetail(this.state.selectedEmail.email.id);
        } catch (error) {
            UI.toast(t('toast_generate_fail') + error.message, 'error');
            await this.switchView('inbox');
        }
    },

    // 发送对话消息
    async sendChatMessage() {
        if (!this.state.selectedEmail || !this.state.selectedEmail.reply) return;

        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        if (!message) return;

        const chatMessages = document.getElementById('chatMessages');
        const replyContent = document.getElementById('replyContent');

        // 添加用户消息
        chatMessages.innerHTML += `
            <div class="message user">${UI.escapeHtml(message)}</div>
        `;
        input.value = '';

        // 添加加载提示
        chatMessages.innerHTML += `
            <div class="message assistant loading">${t('chat_thinking')}</div>
        `;
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const result = await API.replies.chat(this.state.selectedEmail.reply.id, message);

            // 移除加载提示
            const loadingMsg = chatMessages.querySelector('.loading');
            if (loadingMsg) loadingMsg.remove();

            // 添加 AI 回复
            chatMessages.innerHTML += `
                <div class="message assistant">${t('chat_updated')}</div>
            `;

            // 更新回复文本框
            replyContent.value = result.content;

            // 更新状态
            this.state.selectedEmail.reply.content = result.content;

            chatMessages.scrollTop = chatMessages.scrollHeight;

        } catch (error) {
            // 移除加载提示
            const loadingMsg = chatMessages.querySelector('.loading');
            if (loadingMsg) loadingMsg.remove();

            chatMessages.innerHTML += `
                <div class="message assistant error">${t('toast_edit_fail')}${error.message}</div>
            `;
        }
    },

    // 批准并发送
    async approveAndSend() {
        if (!this.state.selectedEmail || !this.state.selectedEmail.reply) return;

        try {
            // 先保存当前编辑的内容
            const replyContent = document.getElementById('replyContent').value;
            if (replyContent !== this.state.selectedEmail.reply.content) {
                await API.replies.update(this.state.selectedEmail.reply.id, replyContent);
            }

            // 发送
            await API.replies.send(this.state.selectedEmail.reply.id);
            UI.toast(t('toast_reply_sent'), 'success');

            // 返回收件箱
            await this.switchView('inbox');

        } catch (error) {
            UI.toast(t('toast_send_fail') + error.message, 'error');
        }
    },

    // 重新生成回复
    async regenerateReply() {
        if (!this.state.selectedEmail) return;

        try {
            await API.replies.regenerate(this.state.selectedEmail.email.id);
            UI.toast(t('toast_reply_generated'), 'success');
            await this.showEmailDetail(this.state.selectedEmail.email.id);
        } catch (error) {
            UI.toast(t('toast_regen_fail') + error.message, 'error');
        }
    },

    // 编辑回复
    editReply() {
        if (!this.state.selectedEmail) return;
        const reply = this.state.selectedEmail.reply;

        const newContent = prompt(t('edit_btn') + ':', reply.content);
        if (newContent && newContent !== reply.content) {
            this.updateReplyContent(reply.id, newContent);
        }
    },

    async updateReplyContent(replyId, content) {
        try {
            await API.replies.update(replyId, content);
            UI.toast(t('toast_reply_updated'), 'success');
            await this.showEmailDetail(this.state.selectedEmail.email.id);
        } catch (error) {
            UI.toast(t('toast_update_fail') + error.message, 'error');
        }
    },

    // 审核回复
    async approveReply() {
        if (!this.state.selectedEmail) return;

        try {
            await API.replies.approve(this.state.selectedEmail.reply.id);
            UI.toast(t('toast_reply_approved'), 'success');
            await this.showEmailDetail(this.state.selectedEmail.email.id);
        } catch (error) {
            UI.toast(t('toast_approve_fail') + error.message, 'error');
        }
    },

    // 加载资料源
    async loadKnowledge() {
        const container = document.getElementById('mainContent');
        UI.showLoading(container);

        try {
            const sources = await API.knowledge.list();
            this.state.sources = sources;

            const emptyHtml = `
                <div class="content-header">
                    <h1>${t('knowledge_title')}</h1>
                    <button class="btn btn-primary" onclick="App.showSourceModal()">${t('knowledge_add')}</button>
                </div>
                <div class="content-body">
                    <div class="empty-state">
                        <div class="empty-state-icon">📚</div>
                        <div class="empty-state-title">${t('knowledge_empty_title')}</div>
                        <div class="empty-state-text">${t('knowledge_empty_text')}</div>
                    </div>
                </div>
            `;

            if (sources.length === 0) {
                container.innerHTML = emptyHtml;
                return;
            }

            container.innerHTML = `
                <div class="content-header">
                    <h1>${t('knowledge_title')}</h1>
                    <button class="btn btn-primary" onclick="App.showSourceModal()">${t('knowledge_add')}</button>
                </div>
                <div class="content-body">
                    <div class="source-list-container">
                        ${sources.map(source => UI.renderSourceCard(source)).join('')}
                    </div>
                </div>
            `;

        } catch (error) {
            UI.showError(container, error.message);
        }
    },

    // 显示资料源模态框
    showSourceModal(sourceId = null) {
        const modal = document.getElementById('sourceModal');
        const form = document.getElementById('sourceForm');
        const title = document.getElementById('sourceModalTitle');

        form.reset();
        document.getElementById('sourceId').value = '';

        if (sourceId) {
            title.textContent = t('source_modal_edit');
            const source = this.state.sources.find(s => s.id === sourceId);
            if (source) {
                document.getElementById('sourceId').value = source.id;
                document.getElementById('sourceTitle').value = source.title;
                document.getElementById('sourceContent').value = source.content;
                document.getElementById('sourceKeywords').value = source.keywords.join(', ');
                document.getElementById('sourceCategory').value = source.category || '';
            }
        } else {
            title.textContent = t('source_modal_add');
        }

        UI.showModal('sourceModal');
    },

    // 编辑资料源
    editSource(sourceId) {
        this.showSourceModal(sourceId);
    },

    // 删除资料源
    async deleteSource(sourceId) {
        if (!confirm(t('delete_confirm'))) return;

        try {
            await API.knowledge.delete(sourceId);
            UI.toast(t('toast_source_deleted'), 'success');
            await this.loadKnowledge();
        } catch (error) {
            UI.toast(t('toast_delete_fail') + error.message, 'error');
        }
    },

    // 绑定模态框事件
    bindModals() {
        // 资料源表单
        document.getElementById('sourceForm')?.addEventListener('submit', async (e) => {
            e.preventDefault();

            const id = document.getElementById('sourceId').value;
            const data = {
                title: document.getElementById('sourceTitle').value,
                content: document.getElementById('sourceContent').value,
                keywords: document.getElementById('sourceKeywords').value
                    .split(',')
                    .map(k => k.trim())
                    .filter(k => k),
                category: document.getElementById('sourceCategory').value || null,
            };

            try {
                if (id) {
                    await API.knowledge.update(id, data);
                    UI.toast(t('toast_source_updated'), 'success');
                } else {
                    await API.knowledge.create(data);
                    UI.toast(t('toast_source_created'), 'success');
                }
                UI.hideModal('sourceModal');
                await this.loadKnowledge();
            } catch (error) {
                UI.toast(t('toast_action_fail') + error.message, 'error');
            }
        });

        // 新建邮件表单
        document.getElementById('newEmailForm')?.addEventListener('submit', async (e) => {
            e.preventDefault();

            const data = {
                subject: document.getElementById('newEmailSubject').value,
                body: document.getElementById('newEmailBody').value,
                sender_email: document.getElementById('newEmailSender').value,
                sender_name: document.getElementById('newEmailSenderName').value || null,
            };

            try {
                await API.emails.create(data);
                UI.toast(t('toast_email_created'), 'success');
                UI.hideModal('newEmailModal');
                await this.loadInbox();
            } catch (error) {
                UI.toast(t('toast_create_fail') + error.message, 'error');
            }
        });
    },

    // 加载统计
    async loadStats() {
        const container = document.getElementById('mainContent');
        UI.showLoading(container);

        try {
            const stats = await API.stats.dashboard();
            this.state.stats = stats;

            container.innerHTML = `
                <div class="content-header">
                    <h1>${t('stats_title')}</h1>
                </div>
                <div class="content-body">
                    <div class="stats-grid">
                        ${UI.renderStatCard(stats.summary.total_emails, t('stat_total'))}
                        ${UI.renderStatCard(stats.summary.pending_emails, t('stat_pending'))}
                        ${UI.renderStatCard(stats.summary.auto_replies, t('stat_auto_replies'))}
                        ${UI.renderStatCard(stats.summary.approved_replies, t('stat_approved'))}
                        ${UI.renderStatCard(stats.summary.processing_rate + '%', t('stat_rate'))}
                        ${UI.renderStatCard(stats.knowledge_sources_count, t('stat_sources'))}
                    </div>
                </div>
            `;

        } catch (error) {
            UI.showError(container, error.message);
        }
    },
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

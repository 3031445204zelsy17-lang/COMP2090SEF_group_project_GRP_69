/**
 * Bilingual (zh/en) translation module
 *
 * Usage:
 *   t('key')         — returns translated string for current language
 *   toggleLang()     — switch language and reload page
 *   applyLang()      — update all [data-i18n] elements in current DOM
 */

const DICT = {
  // ── Navigation ──────────────────────────────────────
  app_title:           { zh: '📧 邮件系统',            en: '📧 Mail System' },
  nav_inbox:           { zh: '收件箱',                en: 'Inbox' },
  nav_sent:            { zh: '已发送',                en: 'Sent' },
  nav_knowledge:       { zh: '资料源',                en: 'Sources' },
  nav_stats:           { zh: '统计',                  en: 'Stats' },
  logout:              { zh: '退出',                  en: 'Logout' },
  user_label:          { zh: '用户',                  en: 'User' },

  // ── Common ──────────────────────────────────────────
  loading:             { zh: '加载中...',             en: 'Loading...' },
  error:               { zh: '出错了',                en: 'Error' },
  cancel:              { zh: '取消',                  en: 'Cancel' },
  save:                { zh: '保存',                  en: 'Save' },
  submit:              { zh: '提交',                  en: 'Submit' },
  delete_btn:          { zh: '删除',                  en: 'Delete' },
  edit_btn:            { zh: '编辑',                  en: 'Edit' },
  send_btn:            { zh: '发送',                  en: 'Send' },
  back:                { zh: '← 返回',               en: '← Back' },
  lang_toggle:         { zh: 'EN',                   en: '中文' },

  // ── Time formatting ─────────────────────────────────
  just_now:            { zh: '刚刚',                  en: 'just now' },
  minutes_ago:         { zh: ' 分钟前',               en: ' min ago' },
  hours_ago:           { zh: ' 小时前',               en: ' hr ago' },
  days_ago:            { zh: ' 天前',                 en: ' days ago' },

  // ── Email status ────────────────────────────────────
  status_pending:      { zh: '待处理',                en: 'Pending' },
  status_classified:   { zh: '已分类',                en: 'Classified' },
  status_replied:      { zh: '已回复',                en: 'Replied' },
  status_approved:     { zh: '已审核',                en: 'Approved' },
  status_sent:         { zh: '已发送',                en: 'Sent' },
  status_sent_check:   { zh: '✓ 已发送',              en: '✓ Sent' },
  duplicate_tag:       { zh: '重复',                  en: 'Duplicate' },
  approved_badge:      { zh: '✓ 已审核',              en: '✓ Approved' },
  pending_badge:       { zh: '待审核',                en: 'Pending' },

  // ── Inbox view ──────────────────────────────────────
  inbox_title:         { zh: '📥 收件箱',             en: '📥 Inbox' },
  inbox_empty_title:   { zh: '收件箱为空',            en: 'Inbox is empty' },
  inbox_empty_text:    { zh: '暂无待处理的邮件',       en: 'No emails to process' },
  new_email_btn:       { zh: '+ 新建邮件',            en: '+ New Email' },

  // ── Sent view ───────────────────────────────────────
  sent_title:          { zh: '📤 已发送',             en: '📤 Sent' },
  sent_empty_title:    { zh: '暂无已发送邮件',        en: 'No sent emails yet' },
  sent_empty_text:     { zh: '审核通过的回复将显示在这里', en: 'Approved replies will appear here' },
  recipient_label:     { zh: '收件人: ',              en: 'To: ' },

  // ── Email detail ────────────────────────────────────
  email_detail_title:  { zh: '邮件详情',              en: 'Email Detail' },
  sender_label:        { zh: '发件人: ',              en: 'From: ' },
  time_label:          { zh: '时间: ',                en: 'Time: ' },
  no_reply_title:      { zh: '尚未生成回复',          en: 'No reply generated yet' },
  no_reply_text:       { zh: '点击按钮让 AI 为您生成回复', en: 'Click the button to generate an AI reply' },
  generate_reply_btn:  { zh: '🤖 生成 AI 回复',       en: '🤖 Generate AI Reply' },
  reply_section:       { zh: '✉️ 回复内容',           en: '✉️ Reply Content' },
  ref_sources:         { zh: '📖 引用资料:',          en: '📖 References:' },
  ref_none:            { zh: '无',                    en: 'None' },

  // ── Chat panel ──────────────────────────────────────
  chat_header:         { zh: '💬 AI 对话编辑',        en: '💬 AI Chat Edit' },
  chat_intro:          { zh: '已为您生成回复。您可以输入指令调整，如：', en: 'Reply generated. You can adjust it with instructions like:' },
  chat_hint_en:        { zh: '• "用英文回复"',         en: '• "Reply in Chinese"' },
  chat_hint_formal:    { zh: '• "语气更正式一些"',     en: '• "Make it more formal"' },
  chat_hint_add:       { zh: '• "添加关于截止日期的信息"', en: '• "Add deadline info"' },
  chat_placeholder:    { zh: '输入指令调整回复...',    en: 'Type instruction to edit...' },
  chat_updated:        { zh: '已更新回复内容',         en: 'Reply updated' },
  chat_thinking:       { zh: '正在思考...',            en: 'Thinking...' },
  regen_btn:           { zh: '🔄 重新生成',            en: '🔄 Regenerate' },
  approve_send_btn:    { zh: '✓ 批准发送',             en: '✓ Approve & Send' },

  // ── Knowledge sources ───────────────────────────────
  knowledge_title:     { zh: '📚 资料源管理',          en: '📚 Knowledge Sources' },
  knowledge_add:       { zh: '+ 新增',                 en: '+ Add New' },
  knowledge_empty_title: { zh: '暂无资料源',           en: 'No sources yet' },
  knowledge_empty_text: { zh: '点击右上角添加资料源来指导 AI 回复', en: 'Click the button above to add sources for AI' },
  source_modal_add:    { zh: '新增资料源',             en: 'Add Source' },
  source_modal_edit:   { zh: '编辑资料源',             en: 'Edit Source' },
  delete_confirm:      { zh: '确定要删除这个资料源吗？', en: 'Delete this source?' },

  // ── Stats ───────────────────────────────────────────
  stats_title:         { zh: '📊 统计仪表盘',          en: '📊 Dashboard' },
  stat_total:          { zh: '总邮件数',               en: 'Total Emails' },
  stat_pending:        { zh: '待处理',                 en: 'Pending' },
  stat_auto_replies:   { zh: '自动回复',               en: 'Auto Replies' },
  stat_approved:       { zh: '已审核',                 en: 'Approved' },
  stat_rate:           { zh: '处理率',                 en: 'Process Rate' },
  stat_sources:        { zh: '资料源',                 en: 'Sources' },

  // ── Toast messages ──────────────────────────────────
  toast_reply_sent:       { zh: '回复已发送！',        en: 'Reply sent!' },
  toast_reply_generated:  { zh: '回复已重新生成',      en: 'Reply regenerated' },
  toast_reply_updated:    { zh: '回复已更新',          en: 'Reply updated' },
  toast_reply_approved:   { zh: '回复已审核通过',      en: 'Reply approved' },
  toast_source_deleted:   { zh: '资料源已删除',        en: 'Source deleted' },
  toast_source_updated:   { zh: '资料源已更新',        en: 'Source updated' },
  toast_source_created:   { zh: '资料源已创建',        en: 'Source created' },
  toast_email_created:    { zh: '邮件已创建',          en: 'Email created' },
  toast_generate_fail:    { zh: '生成回复失败: ',      en: 'Generate failed: ' },
  toast_send_fail:        { zh: '发送失败: ',          en: 'Send failed: ' },
  toast_regen_fail:       { zh: '重新生成失败: ',      en: 'Regenerate failed: ' },
  toast_update_fail:      { zh: '更新失败: ',          en: 'Update failed: ' },
  toast_approve_fail:     { zh: '审核失败: ',          en: 'Approve failed: ' },
  toast_delete_fail:      { zh: '删除失败: ',          en: 'Delete failed: ' },
  toast_action_fail:      { zh: '操作失败: ',          en: 'Action failed: ' },
  toast_create_fail:      { zh: '创建失败: ',          en: 'Create failed: ' },
  toast_edit_fail:        { zh: '修改失败: ',          en: 'Edit failed: ' },

  // ── New Email modal ─────────────────────────────────
  new_email_title:      { zh: '新建邮件',              en: 'New Email' },
  sender_email:         { zh: '发件人邮箱',            en: 'Sender Email' },
  sender_name:          { zh: '发件人姓名',            en: 'Sender Name' },
  email_subject:        { zh: '邮件主题',              en: 'Subject' },
  email_body:           { zh: '邮件内容',              en: 'Body' },
  ph_sender_email:      { zh: '',                      en: '' },
  ph_sender_name:       { zh: '',                      en: '' },
  ph_subject:           { zh: '',                      en: '' },
  ph_body:              { zh: '',                      en: '' },

  // ── Source form ─────────────────────────────────────
  source_title_label:   { zh: '标题',                  en: 'Title' },
  source_content_label: { zh: '内容',                  en: 'Content' },
  source_keywords_label:{ zh: '关键词（用逗号分隔）',   en: 'Keywords (comma separated)' },
  source_keywords_ph:   { zh: '例如：课程, 作业, 考试', en: 'e.g. course, homework, exam' },
  source_category_label:{ zh: '分类',                  en: 'Category' },
  cat_none:             { zh: '无',                    en: 'None' },
  cat_academic:         { zh: '学术问题',              en: 'Academic' },
  cat_administrative:   { zh: '行政事务',              en: 'Administrative' },
  cat_faq:              { zh: '常见问题',              en: 'FAQ' },

  // ── Login page ──────────────────────────────────────
  login_title:          { zh: '登录 - 自动邮件回复系统', en: 'Login - Auto Email Reply System' },
  login_heading:        { zh: '📧 自动邮件回复系统',    en: '📧 Auto Email Reply System' },
  login_subtitle:       { zh: '智能邮件处理助手',       en: 'Intelligent Email Assistant' },
  label_email:          { zh: '邮箱',                  en: 'Email' },
  label_password:       { zh: '密码',                  en: 'Password' },
  ph_email:             { zh: '请输入邮箱',            en: 'Enter email' },
  ph_password:          { zh: '请输入密码',            en: 'Enter password' },
  login_btn:            { zh: '登录',                  en: 'Login' },
  login_loading:        { zh: '登录中...',             en: 'Logging in...' },
  no_account:           { zh: '还没有账号？',           en: "Don't have an account? " },
  register_link:        { zh: '注册',                  en: 'Register' },
  label_name:           { zh: '姓名',                  en: 'Name' },
  ph_name:              { zh: '请输入姓名',            en: 'Enter name' },
  ph_reg_email:         { zh: '请输入邮箱',            en: 'Enter email' },
  ph_reg_password:      { zh: '请输入密码（至少6位）',  en: 'Enter password (min 6 chars)' },
  label_role:           { zh: '角色',                  en: 'Role' },
  role_professor:       { zh: '教授',                  en: 'Professor' },
  role_student:         { zh: '学生',                  en: 'Student' },
  register_btn:         { zh: '注册',                  en: 'Register' },
  register_loading:     { zh: '注册中...',             en: 'Registering...' },
  register_success:     { zh: '注册成功，请登录',       en: 'Registered! Please login' },
  login_fail:           { zh: '登录失败: ',            en: 'Login failed: ' },
  register_fail:        { zh: '注册失败: ',            en: 'Register failed: ' },
  has_account:          { zh: '已有账号？',             en: 'Already have an account? ' },
  login_link:           { zh: '登录',                  en: 'Login' },
  footer:               { zh: '© 2026 自动邮件回复系统 - COMP2090 课程项目', en: '© 2026 Auto Email Reply System - COMP2090 Project' },
};

// ── Language state ──────────────────────────────────────

let _lang = localStorage.getItem('lang') || 'zh';

/**
 * Get translated string by key.
 * Falls back to zh, then returns the raw key if not found.
 */
function t(key) {
  const entry = DICT[key];
  if (!entry) return key;
  return entry[_lang] !== undefined ? entry[_lang] : entry.zh;
}

/** Get current language code. */
function currentLang() {
  return _lang;
}

/**
 * Switch language and reload the page.
 * Using reload because all UI is JS-rendered —
 * after reload, init() re-renders everything with t() calls.
 */
function toggleLang() {
  _lang = _lang === 'zh' ? 'en' : 'zh';
  localStorage.setItem('lang', _lang);
  location.reload();
}

/**
 * Apply translations to static HTML elements with data-i18n attributes.
 * Called once on page load after DOM is ready.
 *
 * Supported attributes:
 *   data-i18n="key"              → sets textContent
 *   data-i18n-placeholder="key"  → sets placeholder
 */
function applyLang() {
  document.querySelectorAll('[data-i18n]').forEach(function (el) {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
    el.placeholder = t(el.dataset.i18nPlaceholder);
  });
  // Update page title if data-i18n-title is set on <html>
  var titleKey = document.documentElement.dataset.i18nTitle;
  if (titleKey) document.title = t(titleKey);
}

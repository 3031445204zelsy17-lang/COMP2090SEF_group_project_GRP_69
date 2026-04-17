# COMP2090 Task1 - 视频演示脚本 (2分30秒)

## 基本信息
- **项目**: Automatic Email Reply System（智能邮件自动回复系统）
- **PPT**: `~/Desktop/自动邮件回复系统：面向对象设计实践 (1).pdf`（共 10 页）
- **时长**: 约 2 分 30 秒
- **重点**: AI 智能回复流程 + OOP 架构（故事线讲解）

---

## PPT 页面与用途对照

| PPT 页码 | 标题 | 视频中怎么用 |
|----------|------|-------------|
| p1 | 封面 | 不展示，视频开场直接在浏览器 |
| p2 | 目录 | **跳过** |
| p3 | Executive Summary | **跳过** |
| p4 | Email Processing Pipeline | **讲解 ~15s** |
| p5 | Strategy Pattern（多态+抽象） | **讲解 ~20s** |
| p6 | Inheritance & Encapsulation | **讲解 ~20s** |
| p7 | Composition | **讲解 ~15s** |
| p8 | Technology Stack | 快速带过 ~3s |
| p9 | 总结与回顾 | 快速带过 ~5s |
| p10 | Q&A Thank You | 结束画面 |

> 实际只翻 PPT 第 4-10 页，前 3 页不翻。切到 PPT 后从第 4 页开始。

---

## 时间分配

| 阶段 | 时长 | 画面 |
|------|------|------|
| 开场 + 学生端带过 | ~15s | 浏览器 |
| 教授端：AI 回复流程 | ~40s | 浏览器 |
| 教授端：知识库 + 统计 | ~15s | 浏览器 |
| PPT p4：邮件处理管线 | ~15s | PPT 第 4 页 |
| PPT p5：多态 + 抽象 | ~20s | PPT 第 5 页 |
| PPT p6：继承 + 封装 | ~20s | PPT 第 6 页 |
| PPT p7：组合 | ~15s | PPT 第 7 页 |
| PPT p8-p10：收尾 | ~10s | PPT 第 8-10 页 |

---

## 详细脚本

### [0:00 - 0:15] 开场 + 学生端带过

**画面**: 浏览器登录页

**口述**:
> "This is our Automatic Email Reply System. It helps professors handle student emails with AI-powered classification and reply generation. Students register here and submit emails — we'll focus on the professor side."

**操作**: 指向注册页面的 "Student" 角色选项（1 秒），然后登录教授账号

---

### [0:15 - 0:55] 教授端：AI 回复流程

**操作**:
1. 登录教授账号，展示收件箱

**口述**:
> "Here's the professor inbox — emails are tagged with categories like '学术问题', '行政事务', and different statuses: Pending, Classified, and Replied."

**操作**:
2. 点击一封已生成回复的邮件

**口述**:
> "This email was auto-classified as '学术问题'. The AI generated a reply using DeepSeek, referencing relevant knowledge base entries."

**操作**:
3. 展示 AI 回复 + References 部分

**口述**:
> "The AI Chat Edit lets professors adjust replies naturally — let me ask it to respond in Chinese."

**操作**:
4. 输入 `Please reply in Chinese` → Send → 展示中文回复

**口述**:
> "Looks good — approve and send."

**操作**:
5. 点击 "✓ Approve & Send"，展示 "Reply sent!" 提示

---

### [0:55 - 1:10] 教授端：知识库 + 统计面板

**操作**:
1. 点回收件箱，切到 "📚 Sources" 页面

**口述**:
> "Behind the AI replies is a knowledge base. Professors can add, edit, and delete course materials and FAQs — these feed into the AI to generate context-aware replies."

**操作**:
2. 快速扫过知识库条目（课程大纲、作业指南、办公时间、请假流程），指向关键词标签

**操作**:
3. 切到 "📊 Stats" 页面

**口述**:
> "The Stats Dashboard gives an overview — total emails, pending count, auto-replies generated, approval rate, and knowledge sources."

**操作**:
4. 扫过统计卡片（2-3 秒），然后 Cmd+Tab 切到 PPT

---

### [1:10 - 1:25] PPT 第 4 页：邮件处理管线

**画面**: PPT 第 4 页

**口述**:
> "So what just happened behind the scenes? When an email arrives, it goes through this pipeline: classified by keywords, then a reply is generated using the selected strategy, and finally the professor reviews and approves it. This pipeline is built entirely with OOP principles — let me show you how."

---

### [1:25 - 1:45] PPT 第 5 页：多态 + 抽象（Strategy Pattern）

**口述**:
> "The reply generation step uses the **Strategy Pattern**. This slide shows our abstract base class — `ReplyStrategy` defines the interface with `generate()` as an abstract method. That's **Abstraction**.

> Then we have three concrete strategies — Auto calls DeepSeek API, Template fills predefined templates, and Manual handles professor edits. The system calls `generate()` without knowing which strategy it's using. That's **Polymorphism** — the right strategy is picked at runtime."

**操作**: 指向 PPT 左侧代码块的 `ABC` + `@abstractmethod`，再指向右侧三个策略卡片

---

### [1:45 - 2:05] PPT 第 6 页：继承 + 封装

**口述**:
> "For **Inheritance**, we have three hierarchies shown here: Users — `AbstractPerson → User → Professor / Student`. Emails — `AbstractEmail → StudentEmail / FAQEmail`. Databases — `DatabaseClient → SqliteClient / SupabaseClient`, letting us switch between local and cloud storage.

> And **Encapsulation** — the Email model keeps all attributes private with double underscores. The status field only allows valid transitions: pending → classified → replied → approved → sent. You can't skip steps."

**操作**: 先指向上方的三条继承链图，再指向下方的 `__status` 代码高亮

---

### [2:05 - 2:20] PPT 第 7 页：组合

**口述**:
> "Finally, **Composition** — the `ReplyService` brings everything together. It composes four independent components: the database client, the AI engine, the knowledge service, and the reply strategy. Each is testable and replaceable on its own. Together they form the complete pipeline you saw in the demo."

**操作**: 指向代码中的 `self._db`、`self._llm`、`self._kb`、`self._strategy`

---

### [2:20 - 2:30] PPT 第 8-10 页：收尾

**画面**: 快速翻过

**翻到第 8 页（Technology Stack），口述**:
> "The tech stack: FastAPI for the backend, DeepSeek for AI, Supabase for the database, all in Python."

**翻到第 9 页（总结），口述**:
> "To summarize: all five OOP concepts power this real-world system. For future improvements, we'd add attachment handling and better duplicate detection."

**翻到第 10 页（Thank You）**:
> "Thanks for watching!"

---

## 录前准备清单

### 浏览器
- [ ] 教授账号已登录，停在收件箱
- [ ] 有一封邮件已生成 AI 回复，准备好演示 Chat 编辑
- [ ] DeepSeek API 可用（提前测试一次）

### PPT
- [ ] PPT 打开，先翻到第 4 页，全屏准备好
- [ ] 第 1 页 "Presenter: AI Assistant" 改成你的名字
- [ ] Cmd+Tab 切换练习一次

### 系统
- [ ] 勿扰模式
- [ ] 只开浏览器 + PPT，关闭其他窗口
- [ ] 录屏软件就绪
- [ ] 麦克风测试

### 整场切换顺序
浏览器（UI 演示 ~70s）→ Cmd+Tab → PPT 第 4-10 页（~80s）→ 结束

## 关键节奏

1. **UI 只做一件事**: AI 回复 + Chat 编辑，做完立刻切 PPT
2. **PPT 从第 4 页开始**: 前 3 页（封面/目录/Summary）不翻
3. **翻页节奏**: p4(15s) → p5(20s) → p6(20s) → p7(15s) → p8-p10(10s 快速过)
4. **OOP 按故事走**: 跟着一封邮件的生命周期，自然碰到每个概念
5. **不要解释代码细节**: 指向 PPT 上的高亮部分说概念，不念代码

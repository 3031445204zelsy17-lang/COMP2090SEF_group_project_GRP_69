# COMP2090SEF Group Project - 任务记录

**项目名称：** COMP2090SEF Group Project
**课程代码：** COMP2090SEF
**开始日期：** 2026-03-06
**最后更新：** 2026-03-06

---

## 📋 项目概述

### 项目目标
开发一个自动邮件回复系统，结合 OOP 设计和数据结构/算法，帮助教授高效处理学生邮件。

### 项目组成
- **Task 1 (50%)**: OOP 应用开发 - 自动邮件回复系统
- **Task 2 (30%)**: 自学数据结构和算法 - Heap 数据结构和 Heap Sort 算法

---

## 🏗️ 项目结构

```
COMP2090SEF_group_project/
├── .gitignore                    # Git 忽略文件
├── PROJECT_LOG.md               # 本文件（任务记录）
├── Automatic Email System(oop) T1/    # Task 1 文件夹
│   ├── README.md                         # 英文项目说明
│   └── The initial code of automatic email system.py  # 初始代码
└── python Algorithms and Data Structures T2/  # Task 2 文件夹
    ├── README.md                         # 英文项目说明
    └── heap.py                          # Heap 数据结构实现
```

---

## ✅ 已完成的工作

### 2026-03-06（第一次会话）

#### 1. 项目规划和文档创建
- [x] 创建项目概览文档 (PROJECT_OVERVIEW.md)
- [x] 创建 README.md（中英文版本）
- [x] 创建 OOP_DESIGN.md（OOP 设计文档）
- [x] 创建 requirements.txt（Python 依赖）
- [x] 创建 .gitignore 文件
- [x] 创建 LICENSE 文件

#### 2. GitHub 仓库设置
- [x] 创建 GitHub 仓库（Public）
- [x] 仓库名称：`COMP2090SEF_group_project_GRP_69`
- [x] 仓库描述：`COMP2090SEF - Automatic Email Reply System with OOP and Heap/Heap Sort Algorithm`
- [x] 可见性：Public
- [x] 推送代码到 GitHub

#### 3. Task 1：OOP 应用开发
- [x] 翻译 README.md 为英文
- [x] 创建初始代码文件
- [x] 设计 OOP 类结构（抽象类、继承、多态等）

#### 4. Task 2：数据结构和算法
- [x] 选择数据结构：Heap（堆）
- [x] 选择算法：Heap Sort（堆排序）
- [x] 实现 Heap 数据结构（heap.py）
- [x] 翻译 README.md 为英文

#### 5. Git 版本控制
- [x] 初始化 Git 仓库
- [x] 首次提交：`Initial commit: COMP2090SEF Group Project`
- [x] 推送到远程仓库

---

## ⏳ 待完成的工作

### Task 1：OOP 应用开发

#### 核心类实现
- [ ] `AbstractPerson` - 人员抽象基类
- [ ] `Professor` - 教授类
- [ ] `Student` - 学生类
- [ ] `AbstractEmail` - 邮件抽象基类
- [ ] `StudentEmail` - 学生邮件类
- [ ] `FAQEmail` - FAQ 邮件类
- [ ] `Category` - 分类类
- [ ] `Reply` - 回复类
- [ ] `ReplyStrategy` - 回复策略抽象类
- [ ] `LLMReplyStrategy` - LLM 回复策略
- [ ] `TemplateReplyStrategy` - 模板回复策略
- [ ] `ManualReplyStrategy` - 手动回复策略
- [ ] `EmailService` - 邮件服务类

#### 业务逻辑
- [ ] 邮件分类功能（使用 Task 2 的算法）
- [ ] 重复邮件检测
- [ ] 自动回复生成
- [ ] LLM API 集成
- [ ] 数据库集成（MySQL/PostgreSQL）

#### 前端界面
- [ ] 管理面板（HTML/CSS/JavaScript）
- [ ] 邮件列表展示
- [ ] 分类结果查看
- [ ] 回复审核功能

#### 测试
- [ ] 单元测试（pytest）
- [ ] 集成测试
- [ ] 测试用例编写

---

### Task 2：数据结构和算法

#### Heap 数据结构
- [ ] 完善 Heap 类实现
- [ ] 添加更多方法：
  - `build_heap()`
  - `heap_sort()`
  - `heapify()`
  - `extract_min()`
  - `insert()`

#### Heap Sort 算法
- [ ] 实现 Heap Sort 算法
- [ ] 时间复杂度分析：O(n log n)
- [ ] 空间复杂度分析：O(1)
- [ ] 与其他排序算法对比

#### 集成到 Task 1
- [ ] 在 EmailService 中使用 Heap 优先级队列
- [ ] 在邮件分类中使用 Heap 算法
- [ ] 性能测试和优化

#### 学习报告
- [ ] 编写 Task 2 学习报告
- [ ] 包含时间复杂度分析
- [ ] 包含应用示例
- [ ] 包含图表和表格

---

## 📊 当前项目状态

### 完成度

| 模块 | 完成度 | 说明 |
|-----|-------|------|
| **项目规划** | 100% | 文档齐全，结构清晰 |
| **GitHub 仓库** | 100% | 已创建并推送 |
| **Task 1 代码** | 10% | 仅有初始代码 |
| **Task 2 代码** | 30% | Heap 基本实现 |
| **测试用例** | 0% | 尚未开始 |
| **项目报告** | 0% | 尚未开始 |

**总体完成度：约 20%**

---

## 🔗 GitHub 仓库信息

### 仓库详情
- **仓库地址：** https://github.com/3031445204zelsy17-lang/COMP2090SEF_group_project_GRP_69
- **仓库类型：** Public
- **主分支：** main
- **最新提交：** e1679c0
- **提交信息：** Initial commit: COMP2090SEF Group Project

### Git 命令

```bash
# 进入项目目录
cd "/Users/yifanshi/Desktop/COMP2090SEF_group_project"

# 查看状态
git status

# 查看提交历史
git log --oneline

# 拉取最新代码
git pull origin main

# 推送代码
git push origin main
```

---

## 📅 关键时间节点

| 日期 | 事件 | 状态 |
|------|------|------|
| 2月15日 | 提交组名和成员名单 | ✅ 已完成 |
| 3月8日 | 预提交（GitHub 链接） | ⚠️ 已逾期 |
| **4月12日 23:59** | **最终提交** | ⏳ 剩余约 37 天 |

---

## 🎯 下次继续的步骤

### 立即开始（优先级最高）

1. **完善 Task 1 的 OOP 类实现**
   - 从 OOP_DESIGN.md 复制类定义
   - 创建 `src/models/` 文件夹
   - 实现所有核心类

2. **完善 Task 2 的 Heap 实现**
   - 完善 `heap.py` 中的所有方法
   - 添加 Heap Sort 算法
   - 编写测试用例

3. **编写测试用例**
   - 为每个 OOP 类编写单元测试
   - 测试 Heap 数据结构
   - 测试 Heap Sort 算法

4. **编写学习报告**
   - Task 1 报告（OOP 应用）
   - Task 2 报告（Heap 和 Heap Sort）

---

## 📝 待填写信息

### 团队信息
- **组长姓名：** [待填写]
- **组长学号：** [待填写]
- **成员姓名：** [待填写]
- **成员学号：** [待填写]

### 教授信息
- **课程教授：** Dr. Jimmy S. Ren / Dr. Patrick Chan
- **教授邮箱：** [待填写]
- **GitHub 用户名：** [待填写]（用于邀请为 Collaborator）

---

## 💡 重要提醒

### Git 工作流
- 每完成一个功能，立即提交
- 提交信息使用统一格式：`feat: 描述`、`fix: 描述`、`docs: 描述`
- 定期推送到 GitHub

### OOP 设计原则
- 严格遵循封装、继承、多态、抽象
- 使用设计模式提高代码质量
- 保持代码简洁和可维护

### Task 2 集成
- 将 Heap 数据结构集成到 Task 1 的优先级管理
- 使用 Heap Sort 进行邮件排序
- 在报告中说明集成方式

---

## 📚 参考文档

### 项目文档
- `PROJECT_OVERVIEW.md` - 项目概览（在其他文件夹）
- `OOP_DESIGN.md` - OOP 设计文档（在其他文件夹）
- `README.md` - 项目说明（中英文）

### 课程要求
- COMP2090SEF Course Project Document
- 评分标准和要求

### 技术文档
- Python 官方文档
- Flask/FastAPI 文档
- GitHub 文档

---

## 🆘 遇到问题？

### 常见问题

#### 1. Git 推送失败
```bash
# 解决方案
git pull origin main
git push origin main
```

#### 2. Python 依赖安装失败
```bash
# 解决方案
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. LLM API 调用失败
- 检查 API Key 是否正确
- 检查网络连接
- 使用 Mock 数据测试

---

## 📞 联系方式

- **GitHub 仓库：** https://github.com/3031445204zelsy17-lang/COMP2090SEF_group_project_GRP_69
- **课程页面：** HKMU OLE
- **提交日期：** 2026年4月12日 23:59

---

**最后更新：** 2026-03-06
**会话记录：** 第一次会话 - 项目初始化和 GitHub 设置
**下次会话目标：** 完成核心 OOP 类实现和测试用例

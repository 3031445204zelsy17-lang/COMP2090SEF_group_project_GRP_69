# OOP 设计文档 - 自动邮件回复系统

**版本：** v1.0
**创建日期：** 2026-03-06

---

## 📋 目录

1. [设计概述](#设计概述)
2. [类图](#类图)
3. [类详细设计](#类详细设计)
4. [OOP 概念应用](#oop-概念应用)
5. [设计模式](#设计模式)
6. [数据结构选择](#数据结构选择)

---

## 设计概述

### 设计原则

本项目严格遵循面向对象编程（OOP）的四大原则：

1. **封装 (Encapsulation)** - 隐藏实现细节，暴露公共接口
2. **继承 (Inheritance)** - 通过基类实现代码复用
3. **多态 (Polymorphism)** - 通过接口实现灵活扩展
4. **抽象 (Abstraction)** - 通过抽象类定义规范

### 设计目标

- ✅ 使用所有课程中介绍的 OOP 概念
- ✅ 实现至少 3 个模块/文件
- ✅ 解决实际生活中的邮件管理问题
- ✅ 代码清晰、可维护、可扩展

---

## 类图

```
┌─────────────────────────────────────────────────────────────┐
│                        EmailSystem                          │
│  + process_email(email: Email)                              │
│  + get_category(email: Email) -> Category                  │
│  + generate_reply(email: Email) -> Reply                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────┐    │    ┌─────────────────────┐
│     AbstractPerson  │◄───┼───►│     AbstractEmail    │
│  + name: str        │    │    │  + id: str          │
│  + email: str       │    │    │  + subject: str     │
│  + send_email()     │    │    │  + body: str        │
│  + receive_email()  │    │    │  + timestamp        │
└─────────────────────┘    │    └─────────────────────┘
        ▲                 │            ▲
        │                 │            │
    ┌───┴───┐             │        ┌───┴───┐
    │       │             │        │       │
┌───────┐ ┌───────┐       │   ┌───────┐ ┌───────┐
│Professor││Student│       │   │Student │ │  FAQ  │
└───────┘ └───────┘       │   │ Email  │ │ Email │
        │                 │   └───────┘ └───────┘
        │                 │        │
        │                 │        ▼
        │                 │   ┌──────────────┐
        │                 │   │   Category    │
        │                 │   │  + id: str    │
        │                 │   │  + name: str │
        │                 │   │  + priority   │
        │                 │   └──────────────┘
        │                 │
        │                 │   ┌──────────────┐
        │                 │   │    Reply     │
        │                 │   │  + content   │
        │                 │   │  + auto      │
        │                 │   │  + approved  │
        │                 │   └──────────────┘
        │                 │
        │                 │   ┌──────────────┐
        │                 │   │ReplyStrategy │◄───┬──────┐
        │                 │   │ + generate() │    │      │
        │                 │   └──────────────┘    │      │
        │                 │          ▲            │      │
        │                 │          │            │      │
        │                 │    ┌─────┴─────┐  ┌───┴──┐  │
        │                 │    │           │  │      │  │
        │                 │ ┌───────┐ ┌───────┐│ ┌───────┐
        │                 │ │LLM    │ │Template││ │Manual│
        │                 │ │Reply  │ │Reply  ││ │Reply │
        │                 │ └───────┘ └───────┘│ └───────┘
        │                 │
        ▼                 ▼
┌──────────────────────────────────────────────────┐
│              EmailService                         │
│  + classify_email(email: Email) -> Category      │
│  + check_duplicate(email: Email) -> bool         │
│  + generate_auto_reply(email: Email) -> Reply    │
│  + send_reply(reply: Reply) -> bool              │
└──────────────────────────────────────────────────┘
```

---

## 类详细设计

### 1. AbstractPerson（抽象基类）

**职责：** 定义人员的通用属性和行为

```python
from abc import ABC, abstractmethod
from datetime import datetime

class AbstractPerson(ABC):
    """人员抽象基类"""

    def __init__(self, name: str, email: str):
        self.__name = name  # 私有属性（封装）
        self.__email = email

    @property
    def name(self) -> str:
        """getter 方法"""
        return self.__name

    @property
    def email(self) -> str:
        """getter 方法"""
        return self.__email

    @abstractmethod
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """发送邮件（抽象方法）"""
        pass

    @abstractmethod
    def receive_email(self) -> list:
        """接收邮件（抽象方法）"""
        pass
```

---

### 2. Professor（教授类）

**职责：** 继承 AbstractPerson，实现教授特定的行为

```python
class Professor(AbstractPerson):
    """教授类"""

    def __init__(self, name: str, email: str, department: str):
        super().__init__(name, email)
        self.__department = department  # 院系
        self.__inbox = []  # 收件箱

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """实现发送邮件"""
        # 实现发送逻辑
        return True

    def receive_email(self) -> list:
        """实现接收邮件"""
        return self.__inbox

    def approve_reply(self, reply: Reply) -> bool:
        """审核自动回复"""
        reply.approved = True
        return True
```

---

### 3. Student（学生类）

**职责：** 继承 AbstractPerson，实现学生特定的行为

```python
class Student(AbstractPerson):
    """学生类"""

    def __init__(self, name: str, email: str, student_id: str):
        super().__init__(name, email)
        self.__student_id = student_id  # 学号

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """实现发送邮件"""
        # 实现发送逻辑
        return True

    def receive_email(self) -> list:
        """实现接收邮件"""
        return []
```

---

### 4. AbstractEmail（抽象邮件类）

**职责：** 定义邮件的通用属性

```python
class AbstractEmail(ABC):
    """邮件抽象基类"""

    def __init__(self, id: str, subject: str, body: str, sender: AbstractPerson):
        self.__id = id
        self.__subject = subject
        self.__body = body
        self.__sender = sender
        self.__timestamp = datetime.now()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def subject(self) -> str:
        return self.__subject

    @property
    def body(self) -> str:
        return self.__body

    @property
    def sender(self) -> AbstractPerson:
        return self.__sender
```

---

### 5. StudentEmail（学生邮件类）

**职责：** 继承 AbstractEmail，实现学生邮件

```python
class StudentEmail(AbstractEmail):
    """学生邮件类"""

    def __init__(self, id: str, subject: str, body: str, sender: Student):
        super().__init__(id, subject, body, sender)
        self.__category = None  # 分类
        self.__reply = None  # 回复

    @property
    def category(self) -> Category:
        return self.__category

    @category.setter
    def category(self, value: Category):
        self.__category = value

    @property
    def reply(self) -> Reply:
        return self.__reply

    @reply.setter
    def reply(self, value: Reply):
        self.__reply = value
```

---

### 6. FAQEmail（FAQ 邮件类）

**职责：** 继承 AbstractEmail，表示 FAQ 相关邮件

```python
class FAQEmail(AbstractEmail):
    """FAQ 邮件类（重复问题）"""

    def __init__(self, id: str, subject: str, body: str, sender: Student):
        super().__init__(id, subject, body, sender)
        self.__faq_id = None  # 关联的 FAQ ID
        self.__is_duplicate = False  # 是否重复

    @property
    def faq_id(self) -> str:
        return self.__faq_id

    @faq_id.setter
    def faq_id(self, value: str):
        self.__faq_id = value

    @property
    def is_duplicate(self) -> bool:
        return self.__is_duplicate
```

---

### 7. Category（分类类）

**职责：** 表示邮件的分类

```python
class Category:
    """邮件分类类"""

    def __init__(self, id: str, name: str, priority: int):
        self.__id = id
        self.__name = name  # 分类名称
        self.__priority = priority  # 优先级 (1-10, 1 最高)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def priority(self) -> int:
        return self.__priority

    def __lt__(self, other: 'Category') -> bool:
        """重载 < 运算符（多态）"""
        return self.__priority < other.__priority
```

---

### 8. Reply（回复类）

**职责：** 表示邮件回复

```python
class Reply:
    """邮件回复类"""

    def __init__(self, content: str, auto: bool = True):
        self.__content = content  # 回复内容
        self.__auto = auto  # 是否自动回复
        self.__approved = False  # 是否已审核
        self.__timestamp = datetime.now()

    @property
    def content(self) -> str:
        return self.__content

    @property
    def auto(self) -> bool:
        return self.__auto

    @property
    def approved(self) -> bool:
        return self.__approved

    @approved.setter
    def approved(self, value: bool):
        self.__approved = value
```

---

### 9. ReplyStrategy（回复策略抽象类）

**职责：** 定义回复策略的接口（多态）

```python
from abc import ABC, abstractmethod

class ReplyStrategy(ABC):
    """回复策略抽象类"""

    @abstractmethod
    def generate(self, email: AbstractEmail) -> Reply:
        """生成回复（抽象方法）"""
        pass
```

---

### 10. LLMReplyStrategy（LLM 回复策略）

**职责：** 使用 LLM API 生成回复

```python
class LLMReplyStrategy(ReplyStrategy):
    """LLM 回复策略"""

    def __init__(self, api_key: str):
        self.__api_key = api_key

    def generate(self, email: AbstractEmail) -> Reply:
        """使用 LLM 生成回复"""
        content = self.__call_llm_api(email)
        return Reply(content, auto=True)

    def __call_llm_api(self, email: AbstractEmail) -> str:
        """调用 LLM API"""
        # 实现调用逻辑
        return "这是自动回复"
```

---

### 11. TemplateReplyStrategy（模板回复策略）

**职责：** 使用预设模板生成回复

```python
class TemplateReplyStrategy(ReplyStrategy):
    """模板回复策略"""

    def __init__(self):
        self.__templates = {
            'academic': "感谢您的学术问题，我们会尽快回复...",
            'admin': "关于行政事务，请参考以下链接...",
            'faq': "这是一个常见问题，答案如下..."
        }

    def generate(self, email: AbstractEmail) -> Reply:
        """使用模板生成回复"""
        template_type = email.category.name.lower()
        content = self.__templates.get(template_type, "谢谢您的邮件")
        return Reply(content, auto=True)
```

---

### 12. ManualReplyStrategy（手动回复策略）

**职责：** 标记需要手动回复

```python
class ManualReplyStrategy(ReplyStrategy):
    """手动回复策略"""

    def generate(self, email: AbstractEmail) -> Reply:
        """标记为需要手动回复"""
        return Reply("需要手动回复", auto=False)
```

---

### 13. EmailService（邮件服务类）

**职责：** 组合多个类，实现邮件处理的核心逻辑

```python
class EmailService:
    """邮件服务类（组合模式）"""

    def __init__(self, db_connection):
        self.__db = db_connection
        self.__categories = self.__load_categories()

    def classify_email(self, email: StudentEmail) -> Category:
        """分类邮件"""
        # 实现分类逻辑（可以使用 Task 2 的算法）
        pass

    def check_duplicate(self, email: StudentEmail) -> bool:
        """检查重复邮件（使用 Task 2 的数据结构）"""
        pass

    def generate_auto_reply(self, email: StudentEmail) -> Reply:
        """生成自动回复"""
        strategy = self.__select_strategy(email)
        return strategy.generate(email)

    def __select_strategy(self, email: StudentEmail) -> ReplyStrategy:
        """选择回复策略（多态）"""
        if email.category.priority == 1:
            return LLMReplyStrategy("api_key")
        elif email.category.name == "FAQ":
            return TemplateReplyStrategy()
        else:
            return ManualReplyStrategy()
```

---

## OOP 概念应用

### 1. 封装 (Encapsulation)

✅ **私有属性：** 使用 `__attribute` 命名
✅ **公共接口：** 通过 `@property` 提供 getter/setter
✅ **隐藏实现：** 内部方法使用 `__method` 命名

**示例：**
```python
class Professor:
    def __init__(self, name: str, email: str):
        self.__name = name  # 私有属性
        self.__email = email

    @property
    def name(self) -> str:
        return self.__name  # 通过公共接口访问
```

---

### 2. 继承 (Inheritance)

✅ **单继承：** StudentEmail 继承 AbstractEmail
✅ **多层继承：** Professor → AbstractPerson
✅ **代码复用：** 通过 `super().__init__()` 复用父类代码

**示例：**
```python
class Professor(AbstractPerson):  # 继承
    def __init__(self, name: str, email: str, department: str):
        super().__init__(name, email)  # 调用父类构造函数
        self.__department = department
```

---

### 3. 多态 (Polymorphism)

✅ **方法重载：** `Category` 类重载 `__lt__` 运算符
✅ **方法重写：** 子类重写抽象方法
✅ **策略模式：** 不同 ReplyStrategy 的 `generate()` 方法

**示例：**
```python
# 策略模式（多态）
strategies = [
    LLMReplyStrategy("key"),
    TemplateReplyStrategy(),
    ManualReplyStrategy()
]

for strategy in strategies:
    reply = strategy.generate(email)  # 同一接口，不同实现
```

---

### 4. 抽象 (Abstraction)

✅ **抽象类：** `AbstractPerson`, `AbstractEmail`
✅ **抽象方法：** `send_email()`, `receive_email()`
✅ **接口定义：** `ReplyStrategy` 定义统一接口

**示例：**
```python
class AbstractPerson(ABC):
    @abstractmethod
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """抽象方法：子类必须实现"""
        pass
```

---

### 5. 组合 (Composition)

✅ **类组合：** EmailService 组合多个服务类
✅ **对象组合：** Email 包含 Category 和 Reply
✅ **灵活设计：** 通过组合而非继承实现功能扩展

**示例：**
```python
class EmailService:
    def __init__(self, db_connection):
        self.__db = db_connection  # 组合数据库连接
        self.__classifier = Classifier()  # 组合分类器
        self.__replier = Replier()  # 组合回复生成器
```

---

## 设计模式

### 1. 策略模式 (Strategy Pattern)

**应用：** ReplyStrategy 及其子类

**优点：**
- 算法可以独立于使用它的客户端变化
- 避免使用多重条件判断

---

### 2. 工厂模式 (Factory Pattern)

**应用：** EmailFactory 创建不同类型的邮件

**优点：**
- 创建对象和使用对象分离
- 便于扩展新的邮件类型

---

### 3. 单例模式 (Singleton Pattern)

**应用：** DatabaseConnection（数据库连接）

**优点：**
- 确保只有一个数据库连接实例
- 节省资源

---

## 数据结构和技术选择

### 实际使用的技术

| 功能 | 技术 | 说明 |
|-----|------|------|
| 邮件分类 | 关键词列表匹配（Keyword Matching） | Category 类维护关键词列表，通过 `matches()` 方法计算匹配分数进行分类 |
| 重复检测 | SequenceMatcher 文本相似度 | Python 标准库 `difflib.SequenceMatcher` 计算邮件文本相似度（阈值 0.8） |
| 优先级排序 | Category 类运算符重载 | 通过 `__lt__` 运算符重载实现优先级比较，配合 Python `sorted()` 排序 |
| 知识库检索 | 加权关键词匹配 | KnowledgeSource 类的 `calculate_relevance_score` 方法，综合关键词、标题、内容的加权匹配分数 |

---

## 📝 总结

本设计完整地应用了所有 OOP 概念：

- ✅ **类和对象**
- ✅ **封装**
- ✅ **继承**
- ✅ **多态**
- ✅ **抽象**
- ✅ **组合**

同时应用了常用的设计模式：
- ✅ 策略模式
- ✅ 工厂模式
- ✅ 单例模式

设计遵循 SOLID 原则，代码清晰、可维护、可扩展。

---

**版本：** v1.0
**创建日期：** 2026-03-06

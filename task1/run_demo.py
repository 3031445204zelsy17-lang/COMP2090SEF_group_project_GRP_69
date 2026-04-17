"""Offline Demo Mode Entry Point

Run this script to start the system in demo mode with:
- SQLite database (no Supabase needed)
- Template-based replies (no DeepSeek API needed)
- Pre-loaded sample data for demonstration

Usage: python run_demo.py

Login credentials:
  Professor: professor@hkmu.edu.hk / demo123
  Student:   student@hkmu.edu.hk / demo123
"""

import asyncio
import os
import sys

# Set environment variables BEFORE any config imports
# This ensures Settings reads demo values instead of trying to connect to real services
os.environ["APP_ENV"] = "demo"
os.environ["APP_SECRET_KEY"] = "demo-secret-key-for-testing"
os.environ["DEEPSEEK_API_KEY"] = "demo-not-needed"
os.environ["SUPABASE_URL"] = "demo-not-needed"
os.environ["SUPABASE_KEY"] = "demo-not-needed"

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.db.sqlite_client import SqliteClient
from src.db.supabase_client import set_db_backend
from src.llm.template_client import TemplateLLMClient
from src.llm.deepseek_client import set_llm_backend


async def seed_demo_data(db: SqliteClient):
    """Seed the SQLite database with comprehensive demo data.

    Creates a "lived-in" system with emails in various states:
    pending, classified, replied (awaiting review), and sent.
    """
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # ==================== Users ====================

    professor = await db.create_user(
        name="Demo Professor",
        email="professor@hkmu.edu.hk",
        role="professor",
        password_hash=pwd_context.hash("demo123"),
    )

    student = await db.create_user(
        name="Demo Student",
        email="student@hkmu.edu.hk",
        role="student",
        password_hash=pwd_context.hash("demo123"),
    )

    # ==================== Categories ====================

    cat_academic = await db.create_category(
        "学术问题", 1,
        ["作业", "考试", "课程", "学分", "论文", "项目", "实验", "成绩"],
    )
    cat_admin = await db.create_category(
        "行政事务", 2,
        ["请假", "注册", "缴费", "证明", "申请", "表格", "流程", "办公室"],
    )
    cat_faq = await db.create_category(
        "常见问题", 3,
        ["时间", "地点", "联系方式", "办公时间", "截止", "提交"],
    )
    cat_other = await db.create_category("其他", 5, [])

    # ==================== Knowledge Sources ====================

    await db.create_knowledge_source(
        title="课程大纲 - COMP2090 数据结构与算法",
        content="""COMP2090SEF 数据结构、算法与问题解决

课程简介：
本课程介绍常用的数据结构和算法，培养学生的计算思维和问题解决能力。

评估方式：
- 平时作业: 30%
- 期中考试: 20%
- 期末项目: 50%

上课时间：
- 周二 14:00-16:00
- 周四 10:00-12:00

上课地点：A301 教室""",
        keywords=["COMP2090", "课程", "大纲", "数据结构", "算法"],
        category="academic",
    )

    await db.create_knowledge_source(
        title="作业提交指南",
        content="""作业提交注意事项：

1. 提交截止时间：每周五 23:59
2. 提交方式：通过 Moodle 平台提交
3. 文件格式：Python 文件 (.py) 或 Jupyter Notebook (.ipynb)
4. 命名规范：学号_姓名_作业编号

迟交政策：
- 迟交 1 天：扣除 10%
- 迟交 2 天：扣除 20%
- 迟交超过 2 天：不予评分

如有特殊情况，请提前申请延期。""",
        keywords=["作业", "提交", "截止", "Moodle", "迟交"],
        category="academic",
    )

    await db.create_knowledge_source(
        title="办公室开放时间",
        content="""教授办公室开放时间：

张教授
- 办公室：B512
- 时间：周一、周三 14:00-16:00
- 邮箱：zhang@university.edu

李教授
- 办公室：B513
- 时间：周二、周四 15:00-17:00
- 邮箱：li@university.edu

如需其他时间，请提前邮件预约。""",
        keywords=["办公时间", "教授", "预约", "办公室"],
        category="faq",
    )

    await db.create_knowledge_source(
        title="请假申请流程",
        content="""请假申请流程：

1. 填写请假申请表（可从学院网站下载）
2. 附上相关证明文件（如病假需医生证明）
3. 提交给课程负责人
4. 等待审批结果（通常 3 个工作日内）

注意事项：
- 请假超过 3 天需院长批准
- 考试期间请假需特别申请
- 病假需在 48 小时内提交申请""",
        keywords=["请假", "申请", "流程", "病假", "证明"],
        category="administrative",
    )

    # ==================== Emails (various states) ====================

    # Email 1: replied, academic — awaiting review
    email1 = await db.create_email(
        subject="关于 COMP2090 作业 3 的问题",
        body="""张教授您好，

我是 COMP2090 课程的学生。我对作业 3 中的二叉树遍历部分有些疑问。

题目要求我们实现中序遍历，但我使用递归实现后，输出结果与预期不符。
请问是否可以请您在下次课上讲解一下这个部分？

另外，作业提交截止日期是本周五 23:59 吗？

谢谢！
学生：王小明
学号：12345678""",
        sender_email="wangxm@student.university.edu",
        sender_name="王小明",
        category_id=cat_academic["id"],
    )
    await db.update_email(email1["id"], status="replied")

    # Email 2: replied, administrative — awaiting review
    email2 = await db.create_email(
        subject="请假申请 - 生病",
        body="""教授您好，

我因为感冒发烧，无法参加明天的课程。附上医生证明。

请问如何补交今天截止的作业？是否可以申请延期？

谢谢理解。
学生：李华
学号：12345679""",
        sender_email="lihua@student.university.edu",
        sender_name="李华",
        category_id=cat_admin["id"],
    )
    await db.update_email(email2["id"], status="replied")

    # Email 3: sent, FAQ — approved reply (demonstrates completed flow)
    email3 = await db.create_email(
        subject="办公时间咨询",
        body="""老师您好，

请问您的办公室开放时间是什么时候？我想去请教一些关于期末项目的问题。

谢谢！
学生：张三""",
        sender_email="zhangsan@student.university.edu",
        sender_name="张三",
        category_id=cat_faq["id"],
    )
    await db.update_email(email3["id"], status="sent")

    # Email 4: classified, academic — no reply yet
    email4 = await db.create_email(
        subject="关于课程大纲",
        body="""教授您好，

请问 COMP2090 课程的评估方式是怎样的？期末项目占比多少？

谢谢！""",
        sender_email="lisi@student.university.edu",
        sender_name="李四",
        category_id=cat_academic["id"],
    )
    await db.update_email(email4["id"], status="classified")

    # Email 5: pending — no category yet
    await db.create_email(
        subject="期中考试安排",
        body="""教授您好，

请问 COMP2090 期中考试的时间和地点是什么？考试范围包括哪些章节？

谢谢！
学生：赵六""",
        sender_email="zhaoliu@student.university.edu",
        sender_name="赵六",
    )

    # Email 6: pending — no category yet
    await db.create_email(
        subject="选课问题",
        body="""老师好，

我想问下学期选课的流程是什么？需要满足什么前置条件才能选 COMP3090？

谢谢！
学生：周七""",
        sender_email="zhouqi@student.university.edu",
        sender_name="周七",
    )

    # ==================== Pre-generated Replies ====================

    # Reply for email 1: auto-generated, not approved (pending professor review)
    await db.create_reply(
        email_id=email1["id"],
        content=(
            "Dear Student,\n\n"
            "Thank you for your inquiry about 关于 COMP2090 作业 3 的问题. "
            "Based on the course materials and lecture notes, "
            "please refer to the relevant chapters and assignment guidelines for detailed information. "
            "If you need further clarification, feel free to visit during office hours.\n\n"
            "Best regards"
        ),
        is_auto=True,
        referenced_sources=[],
    )

    # Reply for email 2: auto-generated, not approved (pending professor review)
    await db.create_reply(
        email_id=email2["id"],
        content=(
            "Dear Student,\n\n"
            "Thank you for your request regarding 请假申请 - 生病. "
            "Please visit the university administration office or check the student portal "
            "for the relevant forms and procedures. "
            "Make sure to submit all required documents before the deadline.\n\n"
            "Best regards"
        ),
        is_auto=True,
        referenced_sources=[],
    )

    # Reply for email 3: auto-generated, approved (demonstrates "sent" state)
    reply3 = await db.create_reply(
        email_id=email3["id"],
        content=(
            "Dear Student,\n\n"
            "Your question about 办公时间咨询 is a frequently asked question. "
            "You may find the answer in the course FAQ section or the student handbook. "
            "If you still need help, please do not hesitate to ask during the next class.\n\n"
            "Best regards"
        ),
        is_auto=True,
        referenced_sources=[],
    )
    await db.approve_reply(reply3["id"])

    print("Demo data seeded successfully!")
    print(f"  Users: 2 (professor + student)")
    print(f"  Categories: 4")
    print(f"  Knowledge sources: 4")
    print(f"  Emails: 6 (various states)")
    print(f"  Replies: 3 (1 approved, 2 pending review)")


def main():
    print("=" * 60)
    print("  Automatic Email Reply System - DEMO MODE")
    print("=" * 60)
    print()
    print("This mode uses:")
    print("  - SQLite database (local file, no Supabase needed)")
    print("  - Template-based replies (no DeepSeek API needed)")
    print()

    # Initialize SQLite database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_data.db")
    db = SqliteClient(db_path)

    # Swap database and LLM backends before any services are instantiated
    set_db_backend(db)
    set_llm_backend(TemplateLLMClient())

    # Initialize schema and seed data
    asyncio.run(db.init_db())
    asyncio.run(seed_demo_data(db))

    print()
    print(f"Database: {db_path}")
    print()
    print("Starting server at http://localhost:8000")
    print()
    print("Login credentials:")
    print("  Professor: professor@hkmu.edu.hk / demo123")
    print("  Student:   student@hkmu.edu.hk / demo123")
    print()
    print("API docs: http://localhost:8000/docs")
    print("=" * 60)

    # Start the FastAPI server
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()

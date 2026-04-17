# COMP2090SEF Group Project - Project Log

**Course:** COMP2090SEF Data Structures, Algorithms and Problem Solving
**Group:** 69
**Repository:** https://github.com/3031445204zelsy17-lang/COMP2090SEF_group_project_GRP_69

---

## Project Overview

An automatic email reply system that helps professors efficiently process student emails through intelligent classification and AI-powered auto-reply.

- **Task 1 (50%):** OOP Application — FastAPI backend, management panel, email classification, and auto-reply
- **Task 2 (30%):** Self-learned Data Structure & Algorithm — Heap and Heap Sort

---

## Completed Work

### Task 1: OOP Application

#### OOP Concepts Demonstrated

| Concept | Implementation |
|---------|---------------|
| Abstraction | `AbstractPerson`, `AbstractEmail` base classes with abstract methods |
| Inheritance | `AbstractPerson → User → Professor/Student`; `AbstractEmail → StudentEmail/FAQEmail`; `DatabaseClient → SqliteClient/SupabaseClient` |
| Polymorphism | Strategy pattern — `ReplyStrategy` interface with `AutoReplyStrategy`, `TemplateReplyStrategy`, `ManualReplyStrategy` |
| Encapsulation | Private attributes (`__status`, `__id`) with property accessors; status transition validation |
| Composition | `ReplyService` composes `DatabaseClient`, `DeepSeekClient`, `KnowledgeService`, and `ReplyStrategy` |

#### Features

- Email classification by category (Academic, Administrative, FAQ) using keyword matching
- AI-powered reply generation via DeepSeek API with RAG (knowledge base context)
- Conversational reply editing (professor can instruct AI to modify drafts)
- Management panel with inbox, knowledge base, and statistics dashboard
- Offline demo mode (SQLite + template replies, no API key needed)

#### Files

```
task1/
├── src/
│   ├── models/       (base, email, category, reply, user, strategies, factory, knowledge_source, email_processor)
│   ├── services/     (email_service, reply_service, classification_service, knowledge_service)
│   ├── api/          (auth, emails, replies, knowledge, stats)
│   ├── db/           (base, sqlite_client, supabase_client)
│   ├── llm/          (deepseek_client, template_client)
│   └── config/       (settings)
├── tests/            (test_email, test_category, test_reply, test_classification, test_knowledge)
├── ui/               (HTML/CSS/JS management panel)
└── run_demo.py       (Offline demo launcher)
```

### Task 2: Heap & Heap Sort

- Heap data structure implementation with `build_heap`, `heapify`, `insert`, `extract_min`
- Heap Sort algorithm with O(n log n) time complexity
- Integration into Task 1 for priority-based email sorting

---

## Team

- **Shi Yifan** (s1415343) — Task 1 OOP application, backend, frontend, AI integration
- **Jeff Shaoqi** (s1409290) — Task 2 Heap & Heap Sort, testing

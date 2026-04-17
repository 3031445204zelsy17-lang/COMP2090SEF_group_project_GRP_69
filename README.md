# Automatic Email Reply System

An intelligent email classification and auto-reply system based on OOP, helping professors efficiently process student emails.

**Course:** COMP2090SEF — Data Structures, Algorithms and Problem Solving
**Group:** 69

---

## Try the Demo (No API Key Needed)

> **Note:** Please use the offline demo mode below. It requires no API keys or internet connection.

```bash
git clone https://github.com/3031445204zelsy17-lang/COMP2090SEF_group_project_GRP_69.git
cd COMP2090SEF_group_project_GRP_69/task1
pip install -r requirements.txt
python run_demo.py
```

Then open **http://localhost:5000** in your browser.

**Login credentials:**

| Role | Email | Password |
|------|-------|----------|
| **Professor** | professor@hkmu.edu.hk | demo123 |
| Student | student@hkmu.edu.hk | demo123 |

**Demo video:** https://youtu.be/WWtY-848b3M

---

## Project Overview

- **Task 1 (50%):** OOP Application — Email classification, AI-powered auto-reply, and management panel
- **Task 2 (30%):** Self-learned Data Structure & Algorithm — Heap and Heap Sort

### Core Features

- **Email Classification** — Automatic categorization (Academic, Administrative, FAQ) with priority-based Heap sorting
- **AI Auto-Reply** — DeepSeek API with RAG context from knowledge base; professor reviews and approves
- **Management Panel** — Inbox, knowledge base editor, and statistics dashboard

---

## OOP Concepts

| Concept | Implementation |
|---------|---------------|
| **Abstraction** | `AbstractPerson`, `AbstractEmail` base classes with abstract methods |
| **Inheritance** | `AbstractPerson → Professor / Student`; `DatabaseClient → SqliteClient / SupabaseClient` |
| **Polymorphism** | Strategy pattern — `ReplyStrategy` with Auto, Template, and Manual strategies |
| **Encapsulation** | Private attributes with property accessors; validated status transitions |
| **Composition** | `ReplyService` composes Database, LLM, KnowledgeService, and ReplyStrategy |

See [OOP_DESIGN.md](./OOP_DESIGN.md) for detailed class diagrams.

---

## Repository Structure

```
├── task1/                          # Task 1: OOP Application
│   ├── src/                        #   Backend (FastAPI)
│   │   ├── models/                 #   OOP classes
│   │   ├── services/               #   Business logic
│   │   ├── api/                    #   REST API routes
│   │   ├── db/                     #   Database layer (SQLite + Supabase)
│   │   ├── llm/                    #   LLM integration (DeepSeek + Template)
│   │   └── config/                 #   Configuration
│   ├── tests/                      #   Unit tests (pytest)
│   ├── ui/                         #   Frontend (HTML/CSS/JS)
│   ├── run_demo.py                 #   Offline demo launcher
│   └── requirements.txt            #   Python dependencies
├── task2/                          # Task 2: Heap & Heap Sort
│   ├── heap sort.py
│   └── README.md
├── USER_GUIDE.md                   # Detailed setup instructions
├── OOP_DESIGN.md                   # OOP design documentation
└── PROJECT_LOG.md                  # Development log
```

---

## Testing

```bash
cd task1
pytest tests/ -v
```

---

## Team

- **Shi Yifan** (14153433)
- **Chen Rongan** (14092908)
- **Han Xiaoyu** (13798919)

---

## License

This project is for COMP2090SEF course purposes only.

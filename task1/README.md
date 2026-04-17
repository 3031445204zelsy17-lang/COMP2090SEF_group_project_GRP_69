# Task 1 — OOP Application: Automatic Email Reply System

An intelligent email classification and auto-reply system built with FastAPI, helping professors efficiently process student emails.

---

## Quick Start (Offline Demo)

No API keys or internet connection required.

```bash
cd task1
pip install -r requirements.txt
python run_demo.py
```

Then open **http://localhost:8000** in your browser.

### Login Credentials

| Role | Email | Password |
|------|-------|----------|
| **Professor** | professor@hkmu.edu.hk | demo123 |
| Student | student@hkmu.edu.hk | demo123 |

### What You Can Do

1. **Inbox** — View pre-loaded student emails, classified by category (Academic, Administrative, FAQ) and sorted by priority
2. **Auto-Reply** — Click an email to see the AI-generated reply. Use the Chat Edit box to modify it, then approve and send
3. **Knowledge Base** — View, add, edit, or delete course materials and FAQs in the Sources tab
4. **Statistics** — Check the Stats tab for email volume, reply rates, and other metrics

### Demo Video

https://youtu.be/WWtY-848b3M

---

## Core Features

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

See [OOP_DESIGN.md](../OOP_DESIGN.md) for detailed class diagrams.

---

## Full Mode (API Required)

Full mode connects to DeepSeek for AI-powered replies and Supabase for cloud database storage.

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and fill in your API key
cd src
python main.py
```

---

## Project Structure

```
task1/
├── src/                        # Backend (FastAPI)
│   ├── main.py                 #   Application entry point
│   ├── models/                 #   OOP classes
│   ├── services/               #   Business logic
│   ├── api/                    #   REST API routes
│   ├── db/                     #   Database layer (SQLite + Supabase)
│   ├── llm/                    #   LLM integration (DeepSeek + Template)
│   └── config/                 #   Configuration
├── tests/                      #   Unit tests (pytest)
├── ui/                         #   Frontend (HTML/CSS/JS)
├── run_demo.py                 #   Offline demo launcher
├── .env.example                #   Environment variable template
└── requirements.txt            #   Python dependencies
```

---

## Testing

```bash
cd task1
pytest tests/ -v
```

---

## Documentation

- [USER_GUIDE.md](../USER_GUIDE.md) — Detailed setup instructions
- [OOP_DESIGN.md](../OOP_DESIGN.md) — OOP design documentation

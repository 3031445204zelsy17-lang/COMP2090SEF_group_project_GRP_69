# COMP2090SEF Group Project — Group 69

**Course:** COMP2090SEF — Data Structures, Algorithms and Problem Solving

An intelligent email classification and auto-reply system (Task 1) with a self-learned Heap Sort implementation (Task 2).

---

## Team

- **Shi Yifan** (14153433)
- **Chen Rongan** (14092908)
- **Han Xiaoyu** (13798919)

---

## Quick Start

### Task 1 — OOP Application (Offline Demo)

No API keys or internet required:

```bash
cd task1
pip install -r requirements.txt
python run_demo.py
```

Open **http://localhost:8000** in your browser.

| Role | Email | Password |
|------|-------|----------|
| Professor | professor@hkmu.edu.hk | demo123 |
| Student | student@hkmu.edu.hk | demo123 |

### Task 2 — Heap Sort

```bash
cd "python Algorithms and Data Structures T2"
python heap_sort.py
```

Enter numbers one by one, press Enter to finish.

---

## Task Overview

### Task 1  — OOP Application

An email management system for professors with automatic classification, AI-powered reply generation, and a web-based management panel.

**Key features:**
- Email classification with priority-based sorting (Academic, Administrative, FAQ)
- AI auto-reply via DeepSeek API with RAG context from knowledge base
- Professor review and approval workflow
- Management panel with inbox, knowledge base editor, and statistics dashboard

**OOP concepts applied:** Abstraction, Inheritance, Polymorphism, Encapsulation, Composition, Strategy Pattern, Factory Pattern, Singleton Pattern

→ See [task1/README.md](./task1/README.md) for full details.

### Task 2 — Heap and Heap Sort

A Python implementation of Heap Sort using Max-Heap structure, with interactive number input and validation.

**Key features:**
- `heapify()` — O(log n) subtree adjustment
- `build_max_heap()` — O(n) heap construction
- `heap_sort()` — O(n log n) in-place ascending sort
- Interactive input with validation and error handling

→ See [python Algorithms and Data Structures T2/README.md](./python%20Algorithms%20and%20Data%20Structures%20T2/README.md) for full details.

---

## Demo Videos

- **Task 1:** https://youtu.be/WWtY-848b3M
- **Task 2:** https://youtu.be/ZKLc8llIEeA

---

## Repository Structure

```
├── task1/                                    # Task 1: OOP Application
│   ├── src/                                  #   Backend (FastAPI)
│   │   ├── models/                           #     OOP classes
│   │   ├── services/                         #     Business logic
│   │   ├── api/                              #     REST API routes
│   │   ├── db/                               #     Database (SQLite + Supabase)
│   │   ├── llm/                              #     LLM integration (DeepSeek + Template)
│   │   └── config/                           #     Configuration
│   ├── tests/                                #   Unit tests (pytest)
│   ├── ui/                                   #   Frontend (HTML/CSS/JS)
│   ├── run_demo.py                           #   Offline demo launcher
│   └── requirements.txt                      #   Python dependencies
├── python Algorithms and Data Structures T2/ # Task 2: Heap & Heap Sort
│   ├── heap sort.py                          #   Heap Sort implementation
│   └── README.md                             #   Algorithm documentation
├── OOP_DESIGN.md                             # OOP design documentation
├── USER_GUIDE.md                             # Detailed setup instructions
└── README.md                                 # This file
```

---

## License

This project is for COMP2090SEF course purposes only.

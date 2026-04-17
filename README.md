# Automatic Email Reply System

An intelligent email classification and auto-reply system based on OOP, helping professors efficiently process student emails.

**Course:** COMP2090SEF Data Structures, Algorithms and Problem Solving
**Group:** 69

---

## Project Overview

This project develops an automatic email reply system that helps professors quickly process student emails through intelligent classification and AI-powered auto-reply.

- **Task 1 (50%):** OOP Application — Email classification, auto-reply via LLM, and management panel
- **Task 2 (30%):** Self-learned Data Structure & Algorithm — Heap and Heap Sort

---

## Quick Start

### Prerequisites

- Python 3.10+
- DeepSeek / OpenAI API Key

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configuration

Copy the example environment file and fill in your API key:

```bash
cd task1
cp .env.example .env
# Edit .env with your API key
```

### Run Project

```bash
cd task1/src
python main.py
# Access management panel at http://localhost:5000
```

### Demo Mode

```bash
cd task1
python run_demo.py
```

---

## Core Features

### Email Classification
- Automatic classification by topic (Academic, Administrative, Duplicate)
- Intelligent duplicate detection
- Priority-based sorting using Heap

### Auto Reply
- LLM API integration for generating replies
- FAQ link and template support
- Professor review and modification workflow

### Management Panel
- View classification results and reply records
- Manual intervention options
- Configurable auto-reply rules

---

## Project Architecture

### Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML / CSS / JavaScript |
| Backend | Python (FastAPI) |
| Database | SQLite (demo) / Supabase (PostgreSQL) |
| AI | DeepSeek / OpenAI API |
| Algorithm | Heap & Heap Sort |

### File Structure

```
COMP2090SEF_group_project_GRP_69/
├── task1/                          # Task 1: OOP Application
│   ├── src/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── models/                 # OOP models (Email, Category, Reply, User)
│   │   ├── services/               # Business logic services
│   │   ├── api/                    # API route handlers
│   │   ├── db/                     # Database layer
│   │   ├── llm/                    # LLM integration
│   │   ├── config/                 # Configuration
│   │   └── utils/                  # Utility functions
│   ├── tests/                      # Unit tests
│   ├── ui/                         # Frontend (HTML/CSS/JS)
│   ├── docs/                       # API docs and migrations
│   ├── run_demo.py                 # Demo launcher
│   └── requirements.txt
├── task2/                          # Task 2: Heap & Heap Sort
│   ├── heap sort.py                # Heap implementation
│   └── README.md
├── Automatic Email System(oop) T1/ # Initial design files
├── python Algorithms and Data Structures T2/
├── OOP_DESIGN.md                   # OOP design documentation
├── PROJECT_OVERVIEW.md             # Project overview
└── requirements.txt
```

---

## OOP Design

This project demonstrates the following OOP concepts:

| Concept | Implementation |
|---------|---------------|
| **Class** | Email, Category, Reply, User, Professor, Student |
| **Inheritance** | AbstractPerson → Professor, Student; AbstractEmail → StudentEmail, FAQEmail |
| **Polymorphism** | Strategy pattern for reply generation (LLM, Template, Manual) |
| **Encapsulation** | Private attributes with public property accessors |
| **Abstraction** | Abstract base classes for Person and Email |
| **Composition** | Email contains Category and Reply |

See [OOP_DESIGN.md](./OOP_DESIGN.md) for detailed class diagrams and design rationale.

---

## Testing

```bash
cd task1
pytest tests/ -v
```

---

## Team

- **Shi Yifan** (s1415343)
- **Jeff Shaoqi** (s1409290)

---

## License

This project is for COMP2090SEF course purposes only.

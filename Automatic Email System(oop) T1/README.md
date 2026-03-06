# Automatic Email Reply System

An intelligent email classification and auto-reply system based on OOP, helping professors efficiently process student emails.

---

## 📖 Project Overview

This project is a course project for **COMP2090SEF Data Structures, Algorithms and Problem Solving**

- **Task 1 (50%)**: OOP Application Development

The project aims to develop an automatic email reply system that helps professors quickly process student emails through intelligent classification and AI auto-reply, saving time.

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.10+
MySQL/PostgreSQL 14+
OpenAI API Key (or other LLM API)
```

### Install Dependencies

```bash
cd /Users/yifanshi/Desktop/COMP2090_Project
pip install -r requirements.txt
```

### Run Project

```bash
# Start backend service
cd task1/src
python main.py

# Access management panel
# http://localhost:5000
```

---

## 📋 Core Features

### Email Classification
- Automatic classification by topic (Academic issues, Administrative matters, Duplicate emails)
- Intelligent identification of duplicate questions
- Automatic priority adjustment

### Auto Reply
- LLM API integration to generate appropriate auto-replies
- Support for FAQ links and fixed templates
- Professors can review and modify auto-replies

### Management Panel
- View classification results and reply records
- Manual intervention options
- Configurable auto-reply rules

---

## 🏗️ Project Architecture

### Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML/CSS/JavaScript |
| Backend | Python (Flask/FastAPI) |
| Database | MySQL/PostgreSQL |
| AI | LLM API (OpenAI/Azure) |
| Security | SSL encryption, Access control |

### File Structure

```
COMP2090_Project/
├── task1/                    # OOP Application Development
│   ├── src/
│   │   ├── models/           # Email, Category, Reply and other classes
│   │   ├── services/         # EmailService, ReplyService
│   │   ├── utils/            # Data structures and algorithms utilities
│   │   └── config.py         # Configuration management
│   ├── tests/                # Unit tests
│   └── docs/                 # API documentation
├── task2/                    # Data Structures and Algorithms
│   ├── code/                 # Trie Tree, KMP algorithm, etc.
│   └── docs/                 # Study report
└── reports/                  # Project reports
```

---

## 🎯 Development Progress

### Task 1: OOP Application Development
- [ ] Email class design
- [ ] Category class design
- [ ] Reply class design
- [ ] EmailService service class
- [ ] Database integration
- [ ] LLM API integration
- [ ] Management panel development
- [ ] Test case writing

---

## 📊 OOP Design

This project uses the following OOP concepts:

- **Class** - Email, Category, Reply, User
- **Inheritance** - User → Professor, Student
- **Polymorphism** - Different types of reply strategies
- **Encapsulation** - Private attributes and public methods
- **Abstraction** - Abstract classes and interfaces
- **Composition** - Email contains Category and Reply

For detailed design, please refer to [OOP_DESIGN.md](./OOP_DESIGN.md).

---

## 🧪 Testing

```bash
# Run tests
cd task1
pytest tests/

# Run specific test
pytest tests/test_email.py -v

# Generate coverage report
pytest tests/ --cov=src --cov-report=html
```

---

## 📄 License

This project is only for COMP2090SEF course learning purposes.

---

## 👥 Contact Information

- **Project Repository:** [https://github.com/3031445204zelsy17-lang/COMP2090SEF_group_project_GRP_69.git](https://github.com/3031445204zelsy17-lang/COMP2090SEF_group_project_GRP_69.git)
- **Course Page:** [HKMU OLE]
- **Submission Date:** March 6, 2026

---

**Last Updated:** 2026-03-06

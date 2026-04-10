# 📊 ATHINA VSM – Value Stream Mapping Tool

> Web app for generating and visualizing Value Stream Maps from team questionnaires, powered by AI.

**Live:** [vsm.devspn.tech](https://vsm.devspn.tech) · **Stack:** Django 5.1 · PostgreSQL 16 · Bootstrap 5.3 · OpenAI · Docker

---

## Quick Start (Docker)

```bash
cd app
cp .env.example .env          # edit with your values
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

The app runs at **http://localhost:8001**. Admin panel at `/admin/`.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `0` for production, `1` for development |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `POSTGRES_*` | Database credentials |
| `CSRF_TRUSTED_ORIGINS` | HTTPS origin for CSRF (e.g. `https://vsm.devspn.tech`) |

> AI configuration (API key, model, endpoint) is managed from **Admin → AI Configurations**.

---

## How to Use the App

### Option A: Questionnaire Flow (with AI)

| Step | What to do |
|------|------------|
| **1. Create a Project** | Go to **Projects** → create or select one. Projects group questionnaires and VSMs. |
| **2. Fill Questionnaires** | Inside the project, each team fills their department questionnaire with process metrics, times and pain points. |
| **3. Review Responses** | Check that enough teams have responded before generating. |
| **4. Generate VSM with AI** | Click **Generate VSM** — AI analyzes all responses and creates the map automatically. |
| **5. Save the VSM** | Review the generated map, adjust if needed, and save. |
| **6. Visualize** | Explore the interactive Value Stream Map with work times, wait times, rework loops and bottlenecks. |
| **7. Get AI Suggestions** | Project managers can click **AI Suggestions** to get Lean/Six-Sigma improvement recommendations. |
| **8. Iterate** | Collect new responses, regenerate and compare to track improvement. |

### Option B: Admin Flow (Manual)

| Step | What to do |
|------|------------|
| **1. Create Departments** | Admin → **Categories** → add departments (Developers, QA, UX, etc.) |
| **2. Create Forms** | Admin → **Sections** + **Questions** → configure questionnaire per department |
| **3. Create Projects** | Admin → **Projects** → create project with name, slug, color |
| **4. Create VSM Manually** | Admin → **Value Streams** → add steps with work/wait times, loop factors, people count |

---

## User Roles & Permissions

| Role | Can view | Can edit | Can manage |
|------|----------|----------|------------|
| **Viewer** | ✅ Projects & VSMs | ❌ | ❌ |
| **Editor** | ✅ | ✅ Fill questionnaires, edit data | ❌ |
| **Project Manager** | ✅ | ✅ | ✅ Generate VSM, AI suggestions, manage project |
| **Admin** (superuser) | ✅ | ✅ | ✅ Full access + Django Admin |

Users are assigned to projects via **Admin → Projects → Project Memberships**.

---

## Admin Panel Guide

Access at `/admin/` with a superuser account.

### Data Structure

```
📁 Project
├── 📝 FormResponse (questionnaire answers as JSON)
│   └── 🏢 Category (department) → 📂 Section → ❓ Question
├── 🗺️ ValueStream (VSM map)
│   └── ⚙️ ProcessStep (work_time, wait_time, loop_factor, people)
└── 📊 Diagram (Mermaid diagrams)
```

### Admin Sections

| Section | Purpose |
|---------|---------|
| **AI Configurations** | Set OpenAI/Azure OpenAI API key, model, and endpoint |
| **Categories** | Departments (Developers, QA, UX, Data, Agile, Management, DevOps) |
| **Sections** | Form sections A–G per category |
| **Questions** | Individual questions (text, textarea, checklist, table) |
| **Projects** | Projects with name, slug, color, and member assignments |
| **Form Responses** | Raw questionnaire answers (JSON) per project + category |
| **Value Streams** | VSM maps with AI analysis and AI suggestions |
| **Process Steps** | Individual steps in a VSM with time metrics |
| **Diagrams** | Mermaid.js diagrams attached to projects |

### Load Seed Data

```bash
docker compose exec web python manage.py load_questions    # 200+ questions in 7 departments
docker compose exec web python manage.py load_diagrams     # Mermaid diagrams
docker compose exec web python manage.py load_vsm_seed     # Demo VSM data
docker compose exec web python manage.py load_test_data    # Test data
```

---

## Features

- 🌙 **Dark mode** — toggle in navbar, respects system preference
- 🌐 **i18n** — Spanish and English
- 🤖 **AI generation** — VSM from questionnaire responses (OpenAI / Azure OpenAI)
- 💡 **AI suggestions** — Lean/Six-Sigma improvement recommendations
- 📊 **Interactive VSM** — visual map with work/wait times, loops, push/pull flow
- 🔒 **Role-based access** — viewer, editor, project manager, admin
- ❓ **Guided tutorial** — Intro.js step-by-step walkthrough
- 📋 **7 department questionnaires** — 200+ questions across A–G sections
- 📈 **Mermaid diagrams** — embedded flow diagrams with zoom/pan

---

## Questionnaire Templates (Markdown)

| # | File | Team |
|---|------|------|
| 1 | [01-developers-questionnaire.md](01-developers-questionnaire.md) | Developers |
| 2 | [02-qa-testing-questionnaire.md](02-qa-testing-questionnaire.md) | QA / Testing |
| 3 | [03-ux-design-questionnaire.md](03-ux-design-questionnaire.md) | UX / Design |
| 4 | [04-data-analytics-questionnaire.md](04-data-analytics-questionnaire.md) | Data / Analytics |
| 5 | [05-agile-questionnaire.md](05-agile-questionnaire.md) | Agile / Scrum |
| 6 | [06-management-questionnaire.md](06-management-questionnaire.md) | Management |
| 7 | [07-devops-questionnaire.md](07-devops-questionnaire.md) | DevOps / Platform |

Each questionnaire has 7 sections: **A** Team Identity · **B** Process Steps · **C** Handoffs · **D** Pain Points · **E** Tools · **F** Improvements · **G** VSM Metrics.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Django 5.1, Gunicorn |
| Database | PostgreSQL 16 |
| Frontend | Bootstrap 5.3.3, Mermaid.js 11, Intro.js 7.2, marked.js |
| AI | OpenAI / Azure OpenAI SDK |
| Static files | WhiteNoise |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions → SSH deploy |
| i18n | Django i18n (es/en) |

---

## Glossary

| Term | Definition |
|------|-----------|
| **Value Stream** | All steps from request to delivery (value-adding and non-value-adding) |
| **Lead Time** | Total time from request to delivery |
| **Process Time** | Actual working time (excluding waiting) |
| **Wait Time** | Time a work item sits idle |
| **Bottleneck** | A constraint limiting overall throughput |
| **Rework / Loop** | Redoing work due to defects or unclear requirements |
| **%C&A** | % Complete & Accurate — work usable without rework |

---

*ATHINA LOT1 · DevSecOps Team · Value Stream Mapping Tool*

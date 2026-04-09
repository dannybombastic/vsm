# Value Stream Mapping (VSM) Initiative — ATHINA Project

## Purpose

This initiative aims to **map the complete delivery value stream** across all teams in the ATHINA project. By understanding the steps, handoffs, pain points, and dependencies each team faces, we can identify bottlenecks, eliminate waste, and improve our end-to-end delivery capability.

As the DevOps lead, I will consolidate all team responses into a unified Value Stream Map to drive continuous improvement across the organization.

## Delivery Chain Overview

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  End Client  │────▶│  Management  │────▶│    Agile /   │────▶│  Delivery    │
│  (External)  │     │  (Business)  │     │  Scrum Team  │     │  Teams       │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                 │
                                                ┌────────────────┼────────────────┐
                                                │                │                │
                                           ┌────▼───┐       ┌────▼───┐       ┌────▼───┐
                                           │  Dev   │       │  QA /  │       │  UX /  │
                                           │  Team  │       │ Testing│       │ Design │
                                           └────┬───┘       └────┬───┘       └────┬───┘
                                           ┌────▼────┐      ┌────▼────┐           │
                                           │ Data /  │      │ DevOps /│           │
                                           │Analytics│      │Platform │           │
                                           └────┬────┘      └────┬────┘           │
                                                │                │                │
                                                │                │                │
                                                └────────────────┼────────────────┘
                                                                 │
                                                           ┌─────▼─────┐
                                                           │  Felipe   │
                                                           │(Tech Lead)│
                                                           └─────┬─────┘
                                                                 │
                                                           ┌─────▼─────┐
                                                           │ Management│
                                                           │ (Review)  │
                                                           └─────┬─────┘
                                                                 │
                                                           ┌─────▼─────┐
                                                           │End Client │
                                                           └───────────┘
```

### Client-Supplier Relationships

| Team | Their Client (who they deliver to) | Their Supplier (who gives them work) |
|------|-----------------------------------|--------------------------------------|
| **Management** | Business Stakeholders / End Client | All delivery teams (status, demos, releases) |
| **Agile / Scrum** | All delivery teams (refined backlog) | Management (priorities), End Users (feedback) |
| **Developers** | Felipe (Tech Lead) | Agile (refined stories), UX (designs), QA (defects) |
| **QA / Testing** | Developers (quality gates), Management (release confidence) | Developers (testable builds), Agile (acceptance criteria) |
| **UX / Design** | Developers (implementable designs), Business (user experience) | Business/Management (requirements), End Users (feedback) |
| **Data / Analytics** | Business/Management (insights, reports) | Developers (data pipelines), Business (data requirements) |
| **DevOps / Platform** | All delivery teams (pipelines, environments, infrastructure) | Developers (pipeline requirements), Management (provisioning requests), Security (compliance) |

## Questionnaires

Each team has a dedicated questionnaire to fill out. All forms follow the same 6-section structure:

| # | Questionnaire | Target Team |
|---|---------------|-------------|
| 1 | [01-developers-questionnaire.md](01-developers-questionnaire.md) | Developer Team |
| 2 | [02-qa-testing-questionnaire.md](02-qa-testing-questionnaire.md) | QA / Testing Team |
| 3 | [03-ux-design-questionnaire.md](03-ux-design-questionnaire.md) | UX / Design Team |
| 4 | [04-data-analytics-questionnaire.md](04-data-analytics-questionnaire.md) | Data / Analytics Team |
| 5 | [05-agile-questionnaire.md](05-agile-questionnaire.md) | Agile / Scrum Team |
| 6 | [06-management-questionnaire.md](06-management-questionnaire.md) | Management Team |
| 7 | [07-devops-questionnaire.md](07-devops-questionnaire.md) | DevOps / Platform Team |

### Questionnaire Structure (same for all teams)

Each form has 6 sections:

| Section | Focus |
|---------|-------|
| **A — Team Identity** | Role definition, client, supplier |
| **B — Process Steps** | Ordered steps per work item type (Feature, Bug Fix, Other) |
| **C — Handoffs & Dependencies** | Who gives you work, who receives your output |
| **D — Pain Points & Waste** | Blockers, rework, waiting, unclear requirements |
| **E — Tools & Systems** | What tools are used at each step |
| **F — Improvement Ideas** | What would make delivery faster or better |

## How to Fill Out Your Questionnaire

1. **Open your team's questionnaire** from the table above
2. **Fill in each section** honestly and completely — there are no wrong answers
3. **Be specific** — instead of "deployment is slow", say "deploying to UAT takes 2 days because we wait for environment availability"
4. **Think about all work item types** — features, bug fixes, and any other deliverable
5. **Include every step** — even small ones like "wait for approval" or "send a Teams message"
6. **Note pain points** — anything that causes delay, rework, confusion, or frustration
7. **Submit** your completed form via a Pull Request or by sharing the filled document

> **Tip**: Walk through a recent real example (a feature you delivered or a bug you fixed) as you fill out the form. Concrete examples produce the best insights.

## Timeline

| Phase | Activity | Owner |
|-------|----------|-------|
| **Week 1** | Distribute questionnaires to all teams | DevOps Lead |
| **Week 2** | Teams fill out their questionnaires | All Teams |
| **Week 3** | Consolidate responses into unified VSM | DevOps Lead |
| **Week 4** | Present findings and improvement proposals | DevOps Lead + All Teams |

## What Happens After

Once all questionnaires are collected, the DevOps lead will:

1. **Build the unified Value Stream Map** using the [aggregation template](vsm-aggregation-template.md)
2. **Identify bottlenecks** — steps where work piles up or waits
3. **Map handoff friction** — transitions between teams that cause delays or rework
4. **Catalog pain points** — grouped by theme and impact
5. **Propose improvements** — prioritized by impact and feasibility
6. **Present to all teams** — collaborative review and action planning

## Glossary

| Term | Definition |
|------|-----------|
| **Value Stream** | The sequence of all steps (value-adding and non-value-adding) required to deliver a product or service from request to delivery |
| **Handoff** | The point where work transfers from one person or team to another |
| **Lead Time** | Total elapsed time from when work is requested to when it is delivered |
| **Process Time** | The actual time spent working on a task (excluding waiting) |
| **Wait Time** | Time a work item spends idle, waiting for the next step |
| **Waste (Muda)** | Any activity that consumes resources but creates no value for the customer |
| **Bottleneck** | A constraint that limits the throughput of the entire system |
| **WIP (Work in Progress)** | The number of items being worked on simultaneously |
| **%C&A (% Complete & Accurate)** | The percentage of work received from upstream that is usable without rework |
| **Rework** | Having to redo work due to defects, unclear requirements, or missed requirements |
| **Shift-Left** | Moving activities (testing, security, feedback) earlier in the process |

## ATHINA Pipeline Reference

For context, our current CI/CD pipeline follows these stages:

```
Code Commit → Maven Build → Unit Tests → SonarQube Analysis → Docker Build
    → Qualys Security Scan → Push to ACR → Container App Deploy (Blue-Green)
    → Smoke Tests → Environment Promotion (dev → test → uat → acc → prd)
```

### Environments
- **Development** (dev) — West Europe
- **Testing** (test) — North Europe
- **UAT** (uat) — North Europe
- **Acceptance** (acc) — West Europe
- **Production** (prd) — West Europe

---

*This VSM initiative is led by the DevSecOps team as part of continuous improvement for the ATHINA project.*

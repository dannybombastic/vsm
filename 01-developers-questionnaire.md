# Value Stream Mapping Questionnaire — Developer Team

> **Target**: All developers in the ATHINA project
> **Objective**: Map the steps you follow to deliver your work, identify pain points, and find improvement opportunities
> **Instructions**: Fill in each section as completely as possible. Use a recent real example to guide your answers.

---

## Section A — Team Identity

**A1. Your name / team:**

```
Answer:
```

**A2. Your primary role (e.g., Backend Developer, Frontend Developer, Full-Stack):**

```
Answer:
```

**A3. Who is your primary client? (Who receives and depends on your work output?)**

```
Answer:
Example: Felipe (Tech Lead) who integrates and validates our deliverables
```

**A4. Who is your primary supplier? (Who provides you with the inputs you need to start your work?)**

```
Answer:
Example: Agile team (refined user stories), UX team (designs), QA (defect reports)
```

**A5. How many people are on your team?**

```
Answer:
```

---

## Section B — Process Steps

For each work item type below, list **every step** you go through from the moment you receive the work until you consider it "done". Include small steps like waiting for reviews, sending messages, or switching tools.

### B1. Feature Delivery

> Think of a recent feature you delivered. Walk through every step from receiving the story to having it deployed.

| Step # | Step Description | Who does it | What triggers this step | What is the output |
|--------|-----------------|-------------|------------------------|--------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |
| 9 | | | | |
| 10 | | | | |

**B1a. Which of these steps do you feel add the most value?**

```
Answer:
```

**B1b. Which steps feel like waste or unnecessary overhead?**

```
Answer:
```

### B2. Bug Fix Lifecycle

> Think of a recent bug you fixed. Walk through every step from receiving the report to having the fix in production.

| Step # | Step Description | Who does it | What triggers this step | What is the output |
|--------|-----------------|-------------|------------------------|--------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |

**B2a. What is the typical difference between a critical bug fix and a normal bug fix in terms of steps?**

```
Answer:
```

### B3. Other Work Items (Tech Debt, Spikes, Documentation)

| Step # | Step Description | Who does it | What triggers this step | What is the output |
|--------|-----------------|-------------|------------------------|--------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

---

## Section C — Handoffs & Dependencies

**C1. List every team or person you receive work from, and what you receive:**

| From (Team/Person) | What do you receive? | How is it delivered? (e.g., Jira ticket, Teams message, email, meeting) | Is the information usually complete and clear? (Yes/No/Sometimes) |
|--------------------|---------------------|------------------------------------------------------------------------|------------------------------------------------------------------|
| | | | |
| | | | |
| | | | |
| | | | |

**C2. List every team or person you hand work off to, and what you deliver:**

| To (Team/Person) | What do you deliver? | How is it delivered? | Is there a clear "definition of done" for this handoff? (Yes/No) |
|-------------------|---------------------|---------------------|----------------------------------------------------------------|
| | | | |
| | | | |
| | | | |
| | | | |

**C3. Are there any handoffs that frequently cause delays or confusion? Describe them:**

```
Answer:
```

**C4. Do you depend on other teams or external parties to unblock your work? If so, who and how often?**

```
Answer:
```

---

## Section D — Pain Points & Waste

**D1. What are your top 3 biggest frustrations or blockers in your delivery process?**

```
1.
2.
3.
```

**D2. Where do you experience the most waiting? (e.g., waiting for code reviews, environment availability, approvals, test results)**

```
Answer:
```

**D3. How often do you have to rework something you already completed? What are the typical causes?**

```
Answer:
Example: "About 20% of PRs need rework after code review because requirements were ambiguous"
```

**D4. Are there manual steps in your process that you feel should be automated?**

```
Answer:
```

**D5. Do you experience context switching? How many tasks or projects do you work on simultaneously?**

```
Answer:
```

**D6. Code Review specific — how long does it typically take for a PR to be reviewed? Are there bottlenecks?**

```
Answer:
```

**D7. Build & Deploy specific — do you experience issues with any of these pipeline stages?**

| Pipeline Stage | Issues? (Yes/No) | Describe if Yes |
|---------------|-------------------|-----------------|
| Maven Build | | |
| Unit Tests | | |
| SonarQube Analysis | | |
| Docker Build | | |
| Qualys Security Scan | | |
| Push to ACR | | |
| Container App Deployment | | |
| Smoke Tests | | |
| Environment Promotion (dev→test→uat→acc→prd) | | |

**D8. Environment specific — do you have issues with any development/testing environments?**

```
Answer:
```

---

## Section E — Tools & Systems

**E1. List all tools and systems you use in your daily delivery work:**

| Tool / System | What you use it for | Satisfaction (1-5, where 5 = excellent) | Pain points with this tool |
|---------------|--------------------|-----------------------------------------|---------------------------|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

**E2. Do you have to switch between many tools to complete a single task? Which task requires the most tool-switching?**

```
Answer:
```

**E3. Are there tools you wish you had, or tools you think should be replaced?**

```
Answer:
```

---

## Section F — Improvement Ideas

**F1. If you could change ONE thing about the delivery process, what would it be?**

```
Answer:
```

**F2. What improvement would have the biggest impact on your team's delivery speed?**

```
Answer:
```

**F3. What improvement would have the biggest impact on your team's delivery quality?**

```
Answer:
```

**F4. Are there practices from previous projects or companies that you think would work well here?**

```
Answer:
```

**F5. Any other comments, observations, or suggestions?**

```
Answer:
```

---

> **Thank you for completing this questionnaire!** Your input is essential to building an accurate Value Stream Map and identifying real improvements. Please submit your completed form to the DevOps Lead.

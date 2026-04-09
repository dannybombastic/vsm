# Value Stream Mapping Questionnaire — Data / Analytics Team

> **Target**: All data engineers, data analysts, and BI specialists in the ATHINA project
> **Objective**: Map the steps you follow to deliver data work (pipelines, reports, analytics), identify pain points, and find improvement opportunities
> **Instructions**: Fill in each section as completely as possible. Use a recent real example to guide your answers.

---

## Section A — Team Identity

**A1. Your name / team:**

```
Answer:
```

**A2. Your primary role (e.g., Data Engineer, Data Analyst, BI Developer, Data Scientist):**

```
Answer:
```

**A3. Who is your primary client? (Who receives and depends on your data work?)**

```
Answer:
Example: Business/Management (dashboards, reports, insights), Developers (data models, APIs)
```

**A4. Who is your primary supplier? (Who provides you with the inputs you need to start your work?)**

```
Answer:
Example: Developers (data pipelines, application data), Business (data requirements, KPI definitions), Management (reporting priorities)
```

**A5. How many people are on your team?**

```
Answer:
```

---

## Section B — Process Steps

For each work item type below, list **every step** you go through from receiving the request to delivering the final output.

### B1. Data Pipeline / ETL Development

> Think of a recent data pipeline or ETL job you developed. Walk through every step from requirement to production deployment.

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

**B1a. Which of these steps add the most value?**

```
Answer:
```

**B1b. Which steps feel like waste or unnecessary overhead?**

```
Answer:
```

### B2. Report / Dashboard Creation or Modification

> Walk through the steps for creating or modifying a report/dashboard for stakeholders.

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

### B3. Ad-Hoc Analysis / Data Investigation

> Walk through the steps for handling an ad-hoc data request or investigation.

| Step # | Step Description | Who does it | What triggers this step | What is the output |
|--------|-----------------|-------------|------------------------|--------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

### B4. Data Quality Issue Resolution

> Walk through the steps when a data quality problem is reported or discovered.

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

| From (Team/Person) | What do you receive? | How is it delivered? (e.g., ticket, meeting, email, Teams) | Is the information usually complete and clear? (Yes/No/Sometimes) |
|--------------------|---------------------|----------------------------------------------------------|------------------------------------------------------------------|
| | | | |
| | | | |
| | | | |
| | | | |

**C2. List every team or person you hand work off to, and what you deliver:**

| To (Team/Person) | What do you deliver? | How is it delivered? (e.g., dashboard link, data export, API endpoint, pipeline) | Is there a clear "definition of done" for this handoff? (Yes/No) |
|-------------------|---------------------|---------------------------------------------------------------------------------|----------------------------------------------------------------|
| | | | |
| | | | |
| | | | |

**C3. Are there any handoffs that frequently cause delays or confusion? Describe them:**

```
Answer:
```

**C4. How do you coordinate with developers when data models or schemas change?**

```
Answer:
```

**C5. How do business stakeholders communicate data requirements to you? Is this process effective?**

```
Answer:
```

---

## Section D — Pain Points & Waste

**D1. What are your top 3 biggest frustrations or blockers in your data delivery process?**

```
1.
2.
3.
```

**D2. Where do you experience the most waiting? (e.g., waiting for data access, environment provisioning, stakeholder clarification, schema changes)**

```
Answer:
```

**D3. How often do you have to rework a deliverable? What are the typical causes?**

```
Answer:
```

**D4. Data infrastructure specific — do you experience issues with any of these?**

| Area | Issues? (Yes/No) | Describe if Yes |
|------|-------------------|-----------------|
| PostgreSQL Flexible Server (database access, performance) | | |
| Azure Synapse Analytics (workspace, queries, performance) | | |
| Azure AI Search (indexing, search quality) | | |
| Azure Purview / Data Governance | | |
| Data pipeline reliability (job failures, retries) | | |
| Data freshness / latency (is data up-to-date enough?) | | |
| Cross-environment data access (dev/test/uat/prd) | | |
| Data security / access control | | |
| Storage accounts (data lake, blob storage) | | |

**D5. Data quality specific:**

| Area | Issues? (Yes/No) | Describe if Yes |
|------|-------------------|-----------------|
| Source data quality from applications | | |
| Data validation / monitoring | | |
| Schema evolution and versioning | | |
| Missing or incomplete data | | |
| Data documentation / catalog | | |

**D6. Do you have visibility into upstream application changes that affect your data pipelines?**

```
Answer:
```

---

## Section E — Tools & Systems

**E1. List all tools and systems you use in your daily data work:**

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

**E3. Are there data tools or capabilities you wish you had?**

```
Answer:
```

---

## Section F — Improvement Ideas

**F1. If you could change ONE thing about the data delivery process, what would it be?**

```
Answer:
```

**F2. What improvement would have the biggest impact on data delivery speed?**

```
Answer:
```

**F3. What improvement would have the biggest impact on data quality?**

```
Answer:
```

**F4. How could the collaboration between Data and Development teams be improved?**

```
Answer:
```

**F5. How could data requirements gathering from business stakeholders be improved?**

```
Answer:
```

**F6. Are there data practices from previous projects or companies that you think would work well here?**

```
Answer:
```

**F7. Any other comments, observations, or suggestions?**

```
Answer:
```

---

> **Thank you for completing this questionnaire!** Your input is essential to building an accurate Value Stream Map and identifying real improvements. Please submit your completed form to the DevOps Lead.

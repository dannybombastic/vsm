# Value Stream Mapping Questionnaire — DevOps / Platform Team

> **Target**: All DevOps engineers, SREs, and platform engineers in the ATHINA project
> **Objective**: Map the steps you follow to build, maintain, and operate the CI/CD pipelines, infrastructure, and platform services that enable all delivery teams. Identify pain points and find improvement opportunities.
> **Instructions**: Fill in each section as completely as possible. Use a recent real example to guide your answers.

---

## Section A — Team Identity

**A1. Your name / team:**

```
Answer:
```

**A2. Your primary role (e.g., DevOps Engineer, SRE, Platform Engineer, Infrastructure Engineer):**

```
Answer:
```

**A3. Who is your primary client? (Who depends on your work output?)**

```
Answer:
Example: All delivery teams (Developers, QA, Data) — they depend on pipelines, environments, and infrastructure to deliver their work
```

**A4. Who is your primary supplier? (Who provides you with the inputs you need to start your work?)**

```
Answer:
Example: Developers (pipeline requirements, Dockerfiles, deployment configs), Management (environment provisioning requests), Security (compliance requirements)
```

**A5. How many people are on your team?**

```
Answer:
```

---

## Section B — Process Steps

For each work item type below, list **every step** you go through from receiving the request to completing the work. Include waiting, coordination, and approval steps.

### B1. CI/CD Pipeline — Build or Modify a Pipeline

> Think of a recent pipeline you created or modified. Walk through every step from request to production-ready pipeline.

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

### B2. Infrastructure Change — Provision or Modify Infrastructure

> Think of a recent infrastructure change (new environment, new service, scaling, network change). Walk through every step.

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

### B3. Incident / Production Issue Response

> Walk through the steps when a production issue or incident is reported that requires DevOps involvement.

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

### B4. Environment Promotion (dev → test → uat → acc → prd)

> Walk through the steps for promoting a release across environments.

| Step # | Step Description | Who does it | What triggers this step | What is the output |
|--------|-----------------|-------------|------------------------|--------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |

### B5. Security & Compliance Tasks

> Walk through the steps for security-related work (secret rotation, vulnerability remediation, access management, compliance checks).

| Step # | Step Description | Who does it | What triggers this step | What is the output |
|--------|-----------------|-------------|------------------------|--------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |

---

## Section C — Handoffs & Dependencies

**C1. List every team or person you receive work from, and what you receive:**

| From (Team/Person) | What do you receive? | How is it delivered? (e.g., ticket, Teams message, email, pipeline failure alert) | Is the information usually complete and clear? (Yes/No/Sometimes) |
|--------------------|---------------------|---------------------------------------------------------------------------------|------------------------------------------------------------------|
| | | | |
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
| | | | |

**C3. Are there any handoffs that frequently cause delays or confusion? Describe them:**

```
Answer:
```

**C4. How do delivery teams request DevOps support? Is this process effective?**

```
Answer:
```

**C5. How do you communicate platform changes, outages, or maintenance windows to other teams?**

```
Answer:
```

---

## Section D — Pain Points & Waste

**D1. What are your top 3 biggest frustrations or blockers in your DevOps work?**

```
1.
2.
3.
```

**D2. Where do you experience the most waiting? (e.g., waiting for approvals, access grants, vendor support, stakeholder decisions)**

```
Answer:
```

**D3. How often do you have to rework something you already completed? What are the typical causes?**

```
Answer:
```

**D4. CI/CD Pipeline specific — do you experience issues with any of these?**

| Area | Issues? (Yes/No) | Describe if Yes |
|------|-------------------|-----------------|
| Pipeline reliability (flaky builds, random failures) | | |
| Pipeline execution speed (build/deploy times) | | |
| Pipeline maintenance burden (YAML complexity, duplication) | | |
| Self-hosted agent pool availability and performance | | |
| Maven build and artifact feed issues | | |
| Docker build issues (caching, image size, layers) | | |
| SonarQube integration (scan times, false positives) | | |
| Qualys security scanning (scan times, false positives) | | |
| ACR push/pull performance | | |
| Container App deployment (blue-green, revision management) | | |
| Smoke test reliability (Playwright tests) | | |
| Environment promotion process (manual steps, approvals) | | |

**D5. Infrastructure specific — do you experience issues with any of these?**

| Area | Issues? (Yes/No) | Describe if Yes |
|------|-------------------|-----------------|
| Terraform state management | | |
| Azure resource provisioning delays | | |
| Cross-environment configuration drift | | |
| Network / Private Endpoint configuration | | |
| Key Vault / secret management | | |
| App Configuration management | | |
| PostgreSQL Flexible Server administration | | |
| Container Apps environment management | | |
| Application Gateway configuration | | |
| Cost management and resource optimization | | |
| Azure subscription / RBAC management | | |
| Service Principal / Managed Identity management | | |

**D6. Operations specific — do you experience issues with any of these?**

| Area | Issues? (Yes/No) | Describe if Yes |
|------|-------------------|-----------------|
| Monitoring and alerting coverage | | |
| Incident detection speed (how fast do you know something is wrong?) | | |
| Incident resolution process | | |
| Backup and disaster recovery procedures | | |
| Resource automation (start/stop schedules) | | |
| Log management and troubleshooting | | |
| On-call / out-of-hours support | | |

**D7. How much of your time is spent on reactive/unplanned work vs. planned improvements?**

```
Answer:
Example: "70% reactive (firefighting, urgent requests), 30% planned improvements"
```

**D8. Are there manual processes that should be automated but aren't yet?**

```
Answer:
```

**D9. Do you experience "toil" — repetitive manual work that could be eliminated?**

```
Answer:
```

---

## Section E — Tools & Systems

**E1. List all tools and systems you use in your daily DevOps work:**

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
| | | | |
| | | | |

**E2. Do you have to switch between many tools to complete a single task? Which task requires the most tool-switching?**

```
Answer:
```

**E3. Are there DevOps tools or capabilities you wish you had?**

```
Answer:
```

**E4. How do you manage Infrastructure as Code? Are the current practices effective?**

```
Answer:
```

---

## Section F — Improvement Ideas

**F1. If you could change ONE thing about the DevOps/platform delivery process, what would it be?**

```
Answer:
```

**F2. What improvement would have the biggest impact on delivery team velocity? (Making other teams faster)**

```
Answer:
```

**F3. What improvement would have the biggest impact on platform reliability?**

```
Answer:
```

**F4. What improvement would reduce the most toil or manual work?**

```
Answer:
```

**F5. How could the collaboration between DevOps and delivery teams be improved?**

```
Answer:
```

**F6. What security or compliance improvements should be prioritized?**

```
Answer:
```

**F7. Are there DevOps practices from previous projects or companies that you think would work well here?**

```
Answer:
```

**F8. Any other comments, observations, or suggestions?**

```
Answer:
```

---

> **Thank you for completing this questionnaire!** Your input is essential to building an accurate Value Stream Map and identifying real improvements. Please submit your completed form to the DevOps Lead.

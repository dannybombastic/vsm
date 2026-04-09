# Value Stream Mapping Questionnaire — QA / Testing Team

> **Target**: All QA engineers and testers in the ATHINA project
> **Objective**: Map the steps you follow to validate and assure quality of deliverables, identify pain points, and find improvement opportunities
> **Instructions**: Fill in each section as completely as possible. Use a recent real example to guide your answers.

---

## Section A — Team Identity

**A1. Your name / team:**

```
Answer:
```

**A2. Your primary role (e.g., QA Engineer, Test Automation Engineer, Manual Tester):**

```
Answer:
```

**A3. Who is your primary client? (Who depends on your quality assurance work?)**

```
Answer:
Example: Developers (quality gates and feedback), Management (release confidence and go/no-go decisions)
```

**A4. Who is your primary supplier? (Who provides you with the inputs you need to start testing?)**

```
Answer:
Example: Developers (testable builds), Agile team (acceptance criteria and test scenarios)
```

**A5. How many people are on your team?**

```
Answer:
```

---

## Section B — Process Steps

For each work item type below, list **every step** you go through from the moment you receive work to validate until you consider it "done". Include waiting, coordination, and communication steps.

### B1. Feature Testing

> Think of a recent feature you tested. Walk through every step from receiving the testable build/story to sign-off.

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

**B1a. Which of these steps add the most value to quality assurance?**

```
Answer:
```

**B1b. Which steps feel like waste or unnecessary overhead?**

```
Answer:
```

### B2. Bug Verification & Regression

> Walk through the steps when a developer delivers a bug fix for you to verify.

| Step # | Step Description | Who does it | What triggers this step | What is the output |
|--------|-----------------|-------------|------------------------|--------------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |

**B2a. How do you decide when regression testing is needed vs. targeted verification?**

```
Answer:
```

### B3. Test Planning & Preparation

> Walk through the steps you take to prepare for testing before a sprint or release.

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

| From (Team/Person) | What do you receive? | How is it delivered? (e.g., ticket status change, Teams message, build notification) | Is the information usually complete and clear? (Yes/No/Sometimes) |
|--------------------|---------------------|------------------------------------------------------------------------------------|------------------------------------------------------------------|
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

**C4. How do you communicate test results to other teams? Is this process effective?**

```
Answer:
```

**C5. When you find a defect, describe the process from discovery to resolution:**

```
Answer:
```

---

## Section D — Pain Points & Waste

**D1. What are your top 3 biggest frustrations or blockers in your testing process?**

```
1.
2.
3.
```

**D2. Where do you experience the most waiting? (e.g., waiting for builds, test environments, test data, developer fixes)**

```
Answer:
```

**D3. How often do you have to re-test something due to incomplete fixes or changing requirements?**

```
Answer:
```

**D4. Test Environment specific — do you experience issues with any of these?**

| Area | Issues? (Yes/No) | Describe if Yes |
|------|-------------------|-----------------|
| Environment availability | | |
| Environment configuration (does it match production?) | | |
| Test data availability | | |
| Test data quality / freshness | | |
| Shared environments (conflicts with other testers) | | |
| Database state / seeding | | |
| External service dependencies / mocks | | |

**D5. Test Automation specific:**

| Area | Issues? (Yes/No) | Describe if Yes |
|------|-------------------|-----------------|
| Test automation coverage sufficient? | | |
| Automated tests reliable (not flaky)? | | |
| Smoke test pipeline (Playwright) works well? | | |
| Test maintenance burden manageable? | | |
| CI/CD integration smooth? | | |

**D6. How often do you discover defects that could have been caught earlier (e.g., by unit tests, code review, or clearer requirements)?**

```
Answer:
```

**D7. Do you have enough visibility into what developers are working on and when builds will be ready for testing?**

```
Answer:
```

---

## Section E — Tools & Systems

**E1. List all tools and systems you use in your daily testing work:**

| Tool / System | What you use it for | Satisfaction (1-5, where 5 = excellent) | Pain points with this tool |
|---------------|--------------------|-----------------------------------------|---------------------------|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

**E2. Do you have to switch between many tools to complete a single testing task? Which task requires the most tool-switching?**

```
Answer:
```

**E3. Are there testing tools or capabilities you wish you had?**

```
Answer:
```

---

## Section F — Improvement Ideas

**F1. If you could change ONE thing about the testing/QA process, what would it be?**

```
Answer:
```

**F2. What improvement would have the biggest impact on test execution speed?**

```
Answer:
```

**F3. What improvement would have the biggest impact on defect detection? (Catching bugs earlier)**

```
Answer:
```

**F4. How could the handoff between developers and QA be improved?**

```
Answer:
```

**F5. Are there testing practices from previous projects or companies that you think would work well here?**

```
Answer:
```

**F6. Any other comments, observations, or suggestions?**

```
Answer:
```

---

> **Thank you for completing this questionnaire!** Your input is essential to building an accurate Value Stream Map and identifying real improvements. Please submit your completed form to the DevOps Lead.

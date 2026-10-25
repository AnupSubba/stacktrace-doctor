# Requirements

## Problem

Java developers lose time decoding long stack traces. The real cause is often buried several
"Caused by" levels deep, search results are noisy, and general chatbots answer confidently
without sources.

## Solution

A focused tool that finds the real cause, explains it in plain English, suggests a fix, and
shows the documentation it relied on.

## Users

- Junior and mid-level Java / Spring Boot developers
- Support engineers triaging production logs
- Students learning Spring

## User stories

| ID  | Story | Acceptance criteria |
|-----|-------|---------------------|
| US1 | As a developer, I paste a stack trace and get the root cause in plain English. | Deepest cause identified correctly on ≥80% of the evaluation set; answer in under 10 s |
| US2 | I see a suggested fix, with a code or config snippet when relevant. | Ordered fix steps; snippet shown in a code block |
| US3 | I see which documentation the answer used. | 1–5 source links; every link comes from the retrieved documents, never invented (enforced in code) |
| US4 | I see a confidence level. | high / medium / low; "low" when the docs don't cover the error |
| US5 | I can try the app without my own logs. | A dropdown with at least 5 sample traces |
| US6 | I'm told clearly when my input isn't a stack trace. | Friendly message; no LLM call made |

## Non-functional requirements

| Area | Requirement |
|------|-------------|
| Performance | Median answer under 10 s |
| Privacy | No accounts, nothing stored server-side; users asked to remove secrets and customer data |
| Security | API keys only in secrets, never in code or Git history; input capped at 20,000 characters |
| Cost | $0: free tiers only; per-session limit and caching protect the quota |
| Usability | Works on mobile; one text box, one button |

## Scope

**In scope (v1):** Spring Boot, Spring Framework, Spring Data JPA / Hibernate, Spring Security,
HikariCP and common core Java exceptions.

**Out of scope (v1):** log files over 1 MB, other languages, IDE plugins, user accounts.

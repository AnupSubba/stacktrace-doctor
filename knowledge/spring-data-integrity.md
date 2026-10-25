---
title: Constraint violation on insert or update (DataIntegrityViolationException)
error: org.springframework.dao.DataIntegrityViolationException
frameworks: [Spring Data, Spring Framework, Hibernate]
source: https://docs.spring.io/spring-framework/reference/data-access.html
---
## What it means
The database rejected a write because it breaks a constraint: unique key, NOT NULL, foreign key or column length.

## Common causes
- Inserting a duplicate value into a unique column (e.g. email).
- A required field is null.
- Deleting a parent row that still has children (foreign key).
- A string longer than the column allows.

## Fixes
1. Read the nested cause: it names the constraint that failed.
2. Validate input before saving (Bean Validation: @NotNull, @Size, @Email) and return a 400/409 instead of a 500.
3. For unique values, check existence first or handle the exception and return 409 Conflict.

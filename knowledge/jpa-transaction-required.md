---
title: No EntityManager with actual transaction available (TransactionRequiredException)
error: jakarta.persistence.TransactionRequiredException
frameworks: [JPA, Spring Framework, Spring Data]
source: https://docs.spring.io/spring-framework/reference/data-access/transaction.html
---
## What it means
A write operation (persist, merge, remove, or a @Modifying query) ran without an active transaction.

## Common causes
- Missing @Transactional on the service method.
- @Transactional on a private method, or called from another method in the same class (self-invocation bypasses the proxy).
- A @Modifying repository query called outside a transaction.

## Fixes
1. Put @Transactional on the public service method that performs the write.
2. Avoid self-invocation: move the transactional method to another bean.
3. Add @Transactional together with @Modifying for update/delete queries.

---
title: Row was updated or deleted by another transaction (ObjectOptimisticLockingFailureException)
error: org.springframework.orm.ObjectOptimisticLockingFailureException
frameworks: [Spring Data, Hibernate, JPA]
source: https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html
---
## What it means
The entity has a @Version field and another transaction changed the same row after you read it, so your update was rejected
to avoid overwriting their change (a "lost update").

## Common causes
- Two users or two threads updating the same record at the same time.
- Re-saving a stale entity or DTO that carries an old version number.

## Fixes
1. Treat it as a normal conflict: reload the entity and retry, or return 409 Conflict to the client.
2. Keep transactions short so conflicts are rare.
3. For hot rows (counters, stock), consider pessimistic locking or an atomic UPDATE statement.

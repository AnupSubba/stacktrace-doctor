---
title: Connection is not available, request timed out (HikariCP)
error: java.sql.SQLTransientConnectionException
frameworks: [HikariCP, Spring Boot]
source: https://github.com/brettwooldridge/HikariCP
---
## What it means
HikariCP could not hand out a database connection within connectionTimeout (30 seconds by default):
"HikariPool-1 - Connection is not available, request timed out after 30000ms".

## Common causes
- All connections are busy: long transactions, slow queries, or slow external calls (HTTP, LLM APIs) made inside @Transactional.
- Connection leaks: connections opened manually and never closed.
- The pool is too small for the number of concurrent requests, or the database is unreachable.

## Fixes
1. Keep transactions short; never call external services inside a transaction.
2. Turn on leak detection: spring.datasource.hikari.leak-detection-threshold=2000 (milliseconds).
3. Size the pool deliberately (spring.datasource.hikari.maximum-pool-size) and check database max connections.

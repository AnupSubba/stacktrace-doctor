---
title: Table or column does not exist (SQLGrammarException)
error: org.hibernate.exception.SQLGrammarException
frameworks: [Hibernate, JPA, Spring Data]
source: https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html
---
## What it means
The database rejected the SQL Hibernate generated, usually because a table or column doesn't exist
(PostgreSQL: relation "orders" does not exist / column "order_date" does not exist).
Spring often wraps it as InvalidDataAccessResourceUsageException.

## Common causes
- The schema was never created or migrated (Flyway/Liquibase not run).
- Naming mismatch: Spring Boot converts camelCase fields to snake_case columns by default.
- Wrong schema or database in the connection URL.
- A reserved word used as a table name (e.g. user, order).

## Fixes
1. Run your migrations, or check spring.jpa.hibernate.ddl-auto for local development only.
2. Align names with @Table(name = ...) and @Column(name = ...).
3. Check the datasource URL and default schema; quote or rename reserved-word tables.

---
title: Failed to configure a DataSource (DataSourceBeanCreationException)
error: org.springframework.boot.autoconfigure.jdbc.DataSourceProperties$DataSourceBeanCreationException
frameworks: [Spring Boot]
source: https://docs.spring.io/spring-boot/reference/data/sql.html
---
## What it means
Spring Boot tried to auto-configure a DataSource but could not work out how to connect:
"Failed to configure a DataSource: 'url' attribute is not specified and no embedded datasource could be configured".

## Common causes
- spring.datasource.url is missing, misspelt or defined under the wrong profile.
- The JDBC driver dependency (e.g. org.postgresql:postgresql) is not on the classpath.
- A JPA starter was added to a project that doesn't need a database.

## Fixes
1. Set spring.datasource.url, username and password for the active profile.
2. Add the JDBC driver dependency for your database.
3. If no database is needed, remove spring-boot-starter-data-jpa (or exclude DataSourceAutoConfiguration).

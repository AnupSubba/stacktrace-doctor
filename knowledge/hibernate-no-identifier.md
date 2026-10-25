---
title: No identifier specified for entity (AnnotationException)
error: org.hibernate.AnnotationException
frameworks: [Hibernate, JPA]
source: https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html
---
## What it means
An @Entity class has no field marked as its primary key, so Hibernate cannot map it.

## Common causes
- Missing @Id on the identifier field.
- @Id imported from the wrong package (org.springframework.data.annotation.Id instead of jakarta.persistence.Id).

## Fixes
1. Add @Id (jakarta.persistence.Id) and usually @GeneratedValue(strategy = GenerationType.IDENTITY or SEQUENCE).
2. Check imports: JPA entities must use jakarta.persistence annotations (javax.persistence before Spring Boot 3).

---
title: Could not initialize proxy - no Session (LazyInitializationException)
error: org.hibernate.LazyInitializationException
frameworks: [Hibernate, Spring Data, JPA]
source: https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html
---
## What it means
A lazy relationship was accessed after the Hibernate session (transaction) had closed, so Hibernate could not load it.

## Common causes
- Accessing a @OneToMany / @ManyToOne(fetch = LAZY) field in a controller, a mapper or the JSON serializer.
- spring.jpa.open-in-view=false (a good setting) without fetching what the response needs.

## Fixes
1. Fetch what you need in the query: JOIN FETCH in JPQL, or @EntityGraph on the repository method.
2. Map entities to DTOs inside the @Transactional service method.
3. Don't switch everything to FetchType.EAGER: it causes N+1 queries and over-fetching.

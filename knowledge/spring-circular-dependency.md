---
title: The dependencies of some of the beans form a cycle (BeanCurrentlyInCreationException)
error: org.springframework.beans.factory.BeanCurrentlyInCreationException
frameworks: [Spring Framework, Spring Boot]
source: https://docs.spring.io/spring-framework/reference/core/beans.html
---
## What it means
Bean A needs bean B and bean B (directly or indirectly) needs bean A, so Spring cannot finish creating either.
Since Spring Boot 2.6, circular references are prohibited by default and start-up fails with "The dependencies of some of the beans in the application context form a cycle".

## Common causes
- Two services calling each other, usually a sign that responsibilities are mixed.
- A configuration class that injects a bean it also defines.

## Fixes
1. Refactor: move the shared logic into a third bean that both depend on.
2. Use application events (ApplicationEventPublisher) instead of a direct call in one direction.
3. As a last resort, inject one side lazily with @Lazy or ObjectProvider.
4. Avoid spring.main.allow-circular-references=true as a permanent fix.

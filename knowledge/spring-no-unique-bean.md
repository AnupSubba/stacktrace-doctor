---
title: Expected single matching bean but found 2 (NoUniqueBeanDefinitionException)
error: org.springframework.beans.factory.NoUniqueBeanDefinitionException
frameworks: [Spring Framework, Spring Boot]
source: https://docs.spring.io/spring-framework/reference/core/beans.html
---
## What it means
Spring found more than one bean that matches the type being injected and cannot decide which one to use.

## Common causes
- Two implementations of the same interface (e.g. EmailNotifier and SmsNotifier both implement Notifier).
- A library auto-configures a bean of the same type as one you defined (e.g. two DataSource or ObjectMapper beans).

## Fixes
1. Mark the default implementation with @Primary.
2. Use @Qualifier("beanName") at the injection point.
3. Inject all of them as List<Notifier> or Map<String, Notifier> when you really need several.

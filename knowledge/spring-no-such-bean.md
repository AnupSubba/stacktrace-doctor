---
title: No qualifying bean of type (NoSuchBeanDefinitionException)
error: org.springframework.beans.factory.NoSuchBeanDefinitionException
frameworks: [Spring Framework, Spring Boot]
source: https://docs.spring.io/spring-framework/reference/core/beans.html
---
## What it means
Spring was asked to inject a bean of some type, but no bean of that type exists in the application context.
It usually appears as the "Caused by" of an UnsatisfiedDependencyException while the application starts.

## Common causes
- The class is missing @Service, @Component, @Repository or @Configuration + @Bean.
- The class is in a package outside the component scan (not under the @SpringBootApplication package).
- The bean is conditional (@Profile, @ConditionalOnProperty) and the condition is false.
- You inject the implementation class while only an interface proxy exists, or vice versa.

## Fixes
1. Add the right stereotype annotation, or declare an @Bean method in a @Configuration class.
2. Move the class under the main application package, or add @ComponentScan / @EnableJpaRepositories for that package.
3. Check active profiles and conditional properties.
4. Inject the interface type rather than the concrete class.

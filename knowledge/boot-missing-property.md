---
title: Could not resolve placeholder (missing configuration property)
error: org.springframework.util.PlaceholderResolutionException, java.lang.IllegalArgumentException
frameworks: [Spring Framework, Spring Boot]
source: https://docs.spring.io/spring-boot/reference/features/external-config.html
---
## What it means
A @Value("${some.property}") or a placeholder in configuration refers to a property that is not defined anywhere.
The message reads: Could not resolve placeholder 'some.property' in value "${some.property}".
Spring Framework 6.2+ reports it as PlaceholderResolutionException; older versions as IllegalArgumentException.

## Common causes
- The property is missing from application.properties / application.yml for the active profile.
- An environment variable expected in production is not set.
- A typo in the property name, or wrong YAML nesting.

## Fixes
1. Define the property, or provide a default: @Value("${some.property:default}").
2. Prefer @ConfigurationProperties with validation (@Validated) so missing values fail with a clear message.
3. Check which profile is active (spring.profiles.active) and which files are loaded.

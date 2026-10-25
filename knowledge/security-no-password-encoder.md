---
title: There is no PasswordEncoder mapped for the id "null"
error: java.lang.IllegalArgumentException
frameworks: [Spring Security]
source: https://docs.spring.io/spring-security/reference/features/authentication/password-storage.html
---
## What it means
Spring Security's DelegatingPasswordEncoder expects stored passwords to start with an id such as {bcrypt} or {noop}.
A password without a prefix can't be matched to an encoder: "There is no PasswordEncoder mapped for the id \"null\"".

## Common causes
- Plain-text or legacy hashed passwords stored without a {id} prefix.
- In-memory users defined with plain passwords in tests or demos.

## Fixes
1. Store passwords encoded with a prefix, e.g. PasswordEncoderFactories.createDelegatingPasswordEncoder().encode(raw).
2. Or define a single encoder bean (e.g. BCryptPasswordEncoder) if all passwords use the same algorithm.
3. Never use {noop} (plain text) outside local demos.

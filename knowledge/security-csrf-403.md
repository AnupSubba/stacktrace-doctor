---
title: 403 Forbidden on POST/PUT/DELETE (CSRF protection)
error: org.springframework.security.web.csrf.InvalidCsrfTokenException
frameworks: [Spring Security]
source: https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html
---
## What it means
Spring Security's CSRF protection rejected a state-changing request (POST, PUT, PATCH, DELETE) because it had no valid CSRF token.
GET requests work, which makes this confusing; often there is no stack trace at all, just a 403.

## Common causes
- A REST client or JavaScript app sends POST without the CSRF token.
- Testing with Postman or curl against an app with default security.

## Fixes
1. For browser apps using session cookies: send the token (e.g. CookieCsrfTokenRepository + the X-XSRF-TOKEN header).
2. For stateless APIs authenticated with tokens (JWT, OAuth2) and no cookies, disabling CSRF can be appropriate: http.csrf(csrf -> csrf.disable()).
3. Turn on DEBUG logging for org.springframework.security to see the exact reason.

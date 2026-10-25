---
title: Required request parameter is not present (MissingServletRequestParameterException, 400)
error: org.springframework.web.bind.MissingServletRequestParameterException
frameworks: [Spring Framework, Spring Boot]
source: https://docs.spring.io/spring-framework/reference/web/webmvc.html
---
## What it means
A @RequestParam marked as required (the default) was not in the request, so Spring returned 400 Bad Request.

## Common causes
- The client forgot the query parameter (?page=1).
- The parameter name differs between client and server.
- Since Spring 6.1, parameter names come from the -parameters compiler flag; without it, @RequestParam needs an explicit name.

## Fixes
1. Send the parameter, or make it optional: @RequestParam(required = false) or defaultValue = "1".
2. Name it explicitly: @RequestParam("page") int page.
3. Make sure the build keeps parameter names (Spring Boot's Maven/Gradle plugins configure -parameters).

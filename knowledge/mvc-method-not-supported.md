---
title: Request method not supported (HttpRequestMethodNotSupportedException, 405)
error: org.springframework.web.HttpRequestMethodNotSupportedException
frameworks: [Spring Framework, Spring Boot]
source: https://docs.spring.io/spring-framework/reference/web/webmvc.html
---
## What it means
A request arrived with an HTTP method (e.g. POST) that the matching URL doesn't support; Spring returns 405 Method Not Allowed.

## Common causes
- The client calls POST but the controller only has @GetMapping for that path (or the reverse).
- A typo in the path sends the request to a different mapping.
- HTML forms only send GET and POST.

## Fixes
1. Match the client's method to the controller mapping (@PostMapping, @PutMapping, ...).
2. Check the exact path and any class-level @RequestMapping prefix.
3. Read the Allow response header: it lists the supported methods.

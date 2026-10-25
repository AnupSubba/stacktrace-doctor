---
title: JSON parse error (HttpMessageNotReadableException, 400)
error: org.springframework.http.converter.HttpMessageNotReadableException
frameworks: [Spring Framework, Jackson]
source: https://docs.spring.io/spring-framework/reference/web/webmvc.html
---
## What it means
Spring could not convert the request body into the @RequestBody object, so it returned 400 Bad Request.
The message usually starts with "JSON parse error" or "Required request body is missing".

## Common causes
- Invalid JSON (trailing comma, single quotes, unquoted keys).
- A type mismatch: text sent for a number, or a wrong date format.
- An empty body for a required @RequestBody.
- Missing Content-Type: application/json header.

## Fixes
1. Validate the JSON the client sends; the message points to the line and column.
2. Match field types and date formats (@JsonFormat, or ISO-8601 strings for java.time types).
3. Send Content-Type: application/json, and use @RequestBody(required = false) only when the body is optional.

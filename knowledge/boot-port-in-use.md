---
title: Port 8080 was already in use (PortInUseException)
error: org.springframework.boot.web.server.PortInUseException
frameworks: [Spring Boot, Tomcat]
source: https://docs.spring.io/spring-boot/how-to/webserver.html
---
## What it means
The embedded web server could not bind to its port because another process is already listening on it.
Spring Boot reports "Web server failed to start. Port 8080 was already in use."

## Common causes
- Another instance of the same app is still running (often from the IDE).
- Another application uses the same port.

## Fixes
1. Stop the other process (find it with `lsof -i :8080` on macOS/Linux or `netstat -ano | findstr :8080` on Windows).
2. Or change the port: server.port=8081 (or server.port=0 for a random port in tests).

---
title: Invalid application.yml (SnakeYAML ScannerException / ParserException)
error: org.yaml.snakeyaml.scanner.ScannerException
frameworks: [Spring Boot, SnakeYAML]
source: https://docs.spring.io/spring-boot/reference/features/external-config.html
---
## What it means
Spring Boot could not read application.yml because the YAML syntax is invalid, for example
"mapping values are not allowed here" or "found character '\t' that cannot start any token".

## Common causes
- Tabs instead of spaces for indentation.
- Wrong indentation level, or a missing space after a colon (key:value instead of key: value).
- Unquoted values containing special characters such as : or #.

## Fixes
1. Use spaces only (2 per level) and check the line number in the message.
2. Quote values with special characters.
3. Validate the file with your IDE's YAML support before starting the app.

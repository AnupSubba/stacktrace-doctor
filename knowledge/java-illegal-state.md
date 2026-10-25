---
title: IllegalStateException
error: java.lang.IllegalStateException
frameworks: [Java, Spring Framework]
source: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/IllegalStateException.html
---
## What it means
A method was called at a time when the object is not in the right state for it. The message usually explains which state.
In Spring tests, "Failed to load ApplicationContext" is an IllegalStateException whose real reason is in the "Caused by" lines below it.

## Common causes
- Using a resource after it was closed or before it was initialised.
- Spring test contexts failing to start (look at the deepest cause).
- Streams reused after a terminal operation ("stream has already been operated upon or closed").

## Fixes
1. Always read the deepest "Caused by": it's usually the actual problem.
2. Check object lifecycles: initialise before use, don't reuse closed resources or consumed streams.

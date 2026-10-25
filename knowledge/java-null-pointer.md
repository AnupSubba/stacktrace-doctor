---
title: NullPointerException
error: java.lang.NullPointerException
frameworks: [Java]
source: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/NullPointerException.html
---
## What it means
Code used a null reference as if it pointed to an object: calling a method, reading a field, unboxing, or indexing an array.
Since Java 14, "helpful NullPointerExceptions" name exactly what was null, e.g. Cannot invoke "String.length()" because "name" is null.

## Common causes
- A repository or map lookup returned null (no record found).
- A field was never initialised, or a Spring bean was created with new instead of being injected.
- Unboxing a null Integer or Long into int or long.

## Fixes
1. Read the message: it names the variable or expression that was null; then check the first "at" line from your own package.
2. Handle "not found" explicitly: Optional, orElseThrow with a meaningful exception, or a 404 response.
3. Prefer constructor injection and final fields so dependencies can't be null.

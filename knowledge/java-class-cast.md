---
title: ClassCastException
error: java.lang.ClassCastException
frameworks: [Java]
source: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ClassCastException.html
---
## What it means
Code tried to cast an object to a type it isn't, e.g. class java.lang.Integer cannot be cast to class java.lang.Long.

## Common causes
- Raw or loosely typed collections (List, Map<String, Object>) holding unexpected types.
- Native SQL query results (numbers may be BigInteger, BigDecimal, Integer or Long depending on the driver).
- JSON deserialised into Map<String, Object> (numbers become Integer, Double...).
- The same class loaded by two class loaders (dev tools restart): "X cannot be cast to X".

## Fixes
1. Use generics and typed DTOs instead of Object and raw types.
2. Convert numbers safely: ((Number) value).longValue().
3. Check instanceof (or use pattern matching) before casting.

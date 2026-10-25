---
title: NumberFormatException
error: java.lang.NumberFormatException
frameworks: [Java]
source: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/NumberFormatException.html
---
## What it means
A string could not be converted to a number: For input string: "abc" (or "", or "12.5" for an int).

## Common causes
- Parsing user input, request parameters or CSV values without validation.
- Empty strings or extra spaces.
- Decimal values parsed as integers, or numbers too large for int.

## Fixes
1. Validate and trim input before parsing; return 400 for invalid client input.
2. Use the right type (Long, BigDecimal) for the value range and format.
3. In Spring, bind parameters to numeric types and let validation report errors.

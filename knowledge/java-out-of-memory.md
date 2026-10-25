---
title: OutOfMemoryError: Java heap space
error: java.lang.OutOfMemoryError
frameworks: [Java]
source: https://docs.oracle.com/en/java/javase/21/troubleshoot/
---
## What it means
The JVM could not allocate an object because the heap is full even after garbage collection.
Other variants: "Metaspace" (too many classes), "Direct buffer memory", "unable to create native thread".

## Common causes
- Loading too much data at once (findAll() on a large table, reading a whole file into memory).
- A memory leak: growing static collections or caches, ThreadLocals not cleared, listeners never removed.
- The heap is simply too small for the workload or the container memory limit.

## Fixes
1. Capture evidence: -XX:+HeapDumpOnOutOfMemoryError, then analyse the dump (Eclipse MAT, VisualVM).
2. Stream or paginate large data; use bounded caches (e.g. Caffeine with maximumSize).
3. Size the heap for the container (-XX:MaxRAMPercentage) only after ruling out a leak.

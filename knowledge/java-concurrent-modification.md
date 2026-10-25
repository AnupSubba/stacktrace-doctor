---
title: ConcurrentModificationException
error: java.util.ConcurrentModificationException
frameworks: [Java]
source: https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ConcurrentModificationException.html
---
## What it means
A collection was modified while it was being iterated, so the fail-fast iterator stopped.
It can happen in a single thread, not only with concurrency.

## Common causes
- Calling list.remove(...) inside a for-each loop over the same list.
- Another thread modifying a shared ArrayList or HashMap.

## Fixes
1. Remove with the iterator (iterator.remove()) or use list.removeIf(condition).
2. Collect changes first, then apply them after the loop.
3. For shared data across threads, use ConcurrentHashMap, CopyOnWriteArrayList or proper locking.

---
name: test-rules
description: Test-suite conventions and network boundaries.
globs:
  - "tests/**"
  - "evals/**"
---
# Test and Eval Rules

## Unit Tests
- Unit tests must be deterministic and offline.
- Use fixtures or fakes for model, embedding, database, and network behavior.

## Evals
- Add focused eval cases for behavior changes that affect retrieval or generation.
- Store expected citation ids or expected evidence text explicitly.
- Include eval diffs in PR notes when eval outputs change.

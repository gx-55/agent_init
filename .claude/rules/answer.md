---
name: answer-rules
description: Conventions for answer generation, prompts, schemas, and citations.
globs:
  - "services/answer/**"
  - "tests/answer/**"
---
# Answer Generation Rules

## Prompts
- Edit only the current prompt version unless the user explicitly asks for a migration.
- Keep old prompt versions frozen for regression comparisons.

## Structured Output
- Validate LLM outputs with typed schemas before returning them.
- Do not pass raw provider responses across service boundaries.

## Citations
- Answers must cite only ids present in the retrieval context.
- Unsupported claims should be removed or marked as insufficient evidence.

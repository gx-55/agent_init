---
name: new-rag-eval
description: Add a new RAG or citation evaluation case, wire it into the eval harness, run the focused case, and summarize the result. Use when the user asks to add an eval, cover a regression, or verify citation behavior.
---

# New RAG Eval

## Inputs

Gather the query, expected citation ids or expected evidence text, and optional production trace id.

## Steps

1. Read the local eval template if one exists.
2. Create a kebab-case case file in the citation eval suite.
3. Run the smallest focused eval command available.
4. Summarize pass/fail, citation grounding, unsupported claims, and latency outliers.
5. If failure is expected today, add a short note to the case file.

## Boundaries

- Do not edit unrelated eval suites.
- Do not open a PR from this skill.
- Do not introduce network calls into unit tests.

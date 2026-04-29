# claude-initiate
<!-- Keep this root memory short. It is loaded at every session start. -->
Reusable bootstrap workspace for Claude/Codex agent configuration stacks.

## Layout
<!-- Replace these paths with the directories that matter in this repo. -->
- `services/retrieval/`  - chunking, embedding, reranker, citation packing
- `services/answer/`     - prompt templates, generator node, guardrails
- `shared/`              - schemas, tracing, settings
- `evals/`               - golden sets, runners, scoring

## Build & test
<!-- Keep commands exact. Delete commands that do not work in this repo. -->
- Install:           `uv sync`
- Unit tests:        `uv run pytest -q`
- Eval harness:      `uv run python -m evals.run --suite citations`
- Lint + types:      `uv run ruff format . && uv run mypy .`

## Canonical conventions
<!-- Write behavioral rules, not aspirations. -->
- The canonical answer prompt lives at `services/answer/prompts/v4.md`.
  Do not edit frozen prompt versions unless updating regression snapshots.
- All LLM outputs must be validated with typed schemas. No raw dict returns
  from generator nodes.
- Retrieval results must carry stable citation ids. Answer generation must
  emit citations using those exact ids.

## Guardrails
<!-- These lines should prevent common agent mistakes. Tune aggressively. -->
- Never bump a model version string without updating its eval snapshot in
  the same commit.
- Never introduce network calls inside unit tests. Use fixtures and fakes.
- Prefer editing existing modules over adding new top-level packages.
- If a change touches `services/retrieval/`, read `.claude/rules/retrieval.md`
  before planning.
- Keep functions focused. Split by responsibility when behavior branches.

## Before opening a PR
<!-- Replace with the checks your team actually requires. -->
- Run the relevant tests or evals and include the result in the PR body.
- Update `CHANGELOG.md` under `## Unreleased` when user-facing behavior changes.
- Use the PR readiness subagent in `.claude/agents/pr-checklist.md`.

---
name: retrieval-rules
description: Conventions for retrieval code. Loaded only for matching paths.
globs:
  - "services/retrieval/**"
  - "tests/retrieval/**"
---
# Retrieval Service Rules

## Chunking
- Use the project canonical chunker for all document ingest.
- Document chunk-size or overlap changes in an ADR or eval note.

## Reranker
- Implement the existing reranker interface. Do not parallel it.
- Cap reranking input size. Reranker latency is usually an SLO risk.

## Citations
- Every returned chunk must carry a stable citation id.
- Use the shared citation helper. Do not hand-roll citation ids.
- If citation id semantics change, update answer citation packing in the same diff.

## Tests
- Retrieval unit tests must not hit embedding or search APIs.
- Gate integration tests behind an explicit marker.

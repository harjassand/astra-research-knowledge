# W03 implementation report — deterministic agent catalog and graph

Implemented the requested builder and generated indexes:

- `outputs/ASTRA_KNOWLEDGE/tools/build_agent_catalog.py`
- `outputs/ASTRA_KNOWLEDGE/indexes/agent_catalog.json`
- `outputs/ASTRA_KNOWLEDGE/indexes/agent_graph.json`
- `outputs/ASTRA_KNOWLEDGE/indexes/agent_topics/*.json`

The catalog has 186 claims. Each entry stores the exact on-disk card SHA-256, title/status/topics, local card and `knowledge.py read` pointers, existing card/read web page pointers, and the original `depends_on` and `scoped_dependencies` records without reinterpreting them. Interface and failure fields include only verbatim labeled card lines; absent structured fields are `UNKNOWN`. The builder checks each card hash against the SQLite docs row, so stale/mismatched card snapshots fail closed.

The graph contains 1,639 source edges and four normalized kinds while retaining each raw relation and source. Mapping: `supported_by` → `provenance`; `links_to_not_logical_dependency` → `navigation`; literal `requires`/`requires_*` → `explicit_requirement`; all other labels → `scoped_relation`. Provenance has `never_proof_by_itself`, navigation has `forbidden`, requirements have `obligation_only`, and other scoped relations have `forbidden_unless_manually_interpreted`. Thus the builder does not treat source citation, topical navigation, or conceptual relations as proof composition. Graph endpoints are materialized as claim, dependency, evidence, or explicit unresolved-reference nodes; this snapshot had zero unresolved endpoint references.

Freshness metadata records schema version, builder SHA-256, SHA-256 for claims/edges/dependencies/documents/SQLite inputs, and a stable aggregate card-manifest digest. Per-card SHA is also recorded on catalog rows. Topic shards contain compact routing metadata and pointers, not repeated claim statements.

Validation performed by the builder and independent assertions:

- 186 cards found, each card SHA matches SQLite and its local card page exists.
- All 535 read-web pointers resolve; all 186 card-web pointers resolve.
- All graph endpoints and scoped dependency IDs resolve; zero unresolved graph references.
- Edge totals: 535 provenance, 868 navigation, 47 explicit requirements, 189 scoped relations (sum 1,639).
- Ten topic shards generated.
- Independent assertions confirmed navigation composition is forbidden and quoted fields are either literal line lists or `UNKNOWN`.
- Rebuilding twice produced byte-identical catalog, graph, and topic shard outputs.

Run from the workspace root with:

```sh
python3 outputs/ASTRA_KNOWLEDGE/tools/build_agent_catalog.py
```

No existing scientific source, card, or database was edited. The workspace directory is not a Git repository, so a Git status/diff could not be used to enumerate modifications; the builder writes only its named catalog, graph, and topic shard outputs.

# Repository map

Start with [00_START_HERE.txt](00_START_HERE.txt) and [current retrieval](knowledge/README.md).

| Location | Purpose |
| --- | --- |
| `knowledge/current/` | Generated current records, packets, search projections, inventory and coverage |
| `knowledge/retrieve.py` | Public local retrieval facade |
| `knowledge/units/`, `knowledge/reviews/`, `knowledge/transfers/` | Versioned reusable units, scoped review and supported transfers |
| `cards/`, `frontier/`, `indexes/`, `agent/SEMANTIC_NOTICES.d/` | Scientific authoring authorities, status, corrections and historical access editions |
| `research/`, `updates/`, `evidence/` | Preserved source artifacts and provenance |
| `literature/` | Historical extracted lemma atlas, included in current retrieval |
| `technology/` | Scoped technology records and handoffs |
| `state/` | Published checkpoints and continuation protocol |
| `plugins/astra-research/` | Optional read-only search/fetch plugin |
| `web/`, `exports/`, dated access manifests | Historical exports; use their recorded revision |

The compiler reads existing scientific authorities and generates one normalized current representation. [knowledge/INTAKE.md](knowledge/INTAKE.md) specifies that process. Edit authoring inputs, then build and check when scientific inputs or retrieval architecture change; generated files are not edited by hand.

The Pages site is a bounded projection of a named Git revision. Its publication metadata binds that view to its corpus input version. Original sources and older interfaces remain in Git. The local optional neural ranking runtime is documented separately from portable reading in [knowledge/README.md](knowledge/README.md).

[history/README.md](history/README.md) distinguishes older inventories and retired evaluation tooling from current access. Historical instructions do not control a new task. Source identity, scoped review, proof validity, physical validation and practical value retain their own evidence.

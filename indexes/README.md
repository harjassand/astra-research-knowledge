# Authoring indexes and historical projections

Current search, packets and inventory live in [knowledge/current/](../knowledge/current/), accessed through [knowledge/retrieve.py](../knowledge/README.md).

`claims.jsonl` and `agent_catalog.json` are pinned baselines. Their `.d/` directories supply later authoring shards; `query_aliases.d/` supplies routing vocabulary. Use the [intake contract](../knowledge/INTAKE.md) when changing those inputs.

Dated validation receipts, graph indexes and `history/` describe the versions that produced them. They are not a second current inventory or a scientific acceptance decision. Source indexes retain exact paths and provenance; follow the selected current packet to the governing bytes.

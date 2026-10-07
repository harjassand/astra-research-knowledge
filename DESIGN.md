# Why this structure

This is a workload-dependent design, not a proven universal optimum. It minimizes routine ingestion while keeping exact evidence recoverable. The unit of knowledge is a scoped result with a stable source identifier, a typed information interface, dependencies, costs and failure domain. Topics provide navigation; archived objects preserve byte identity; local search produces bounded evidence packets.

OpenAI's [GPT-6 Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) recommends minimal routing and reading documentation when the task needs it. That supports a small entry point rather than compulsory whole-project reading. OpenAI's [citation guidance](https://developers.openai.com/api/docs/guides/citation-formatting) supports stable identifiers and explicit source units. Its [file search guide](https://developers.openai.com/api/docs/guides/tools-file-search) documents the token/latency versus retrieval-quality tradeoff when limiting results. This repository implements a local interface; it does not configure paid hosted retrieval or require an API key.

[Anthropic's context-engineering article](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) describes lightweight references, retrieval as needed and persistent notes. [Lost in the Middle](https://arxiv.org/abs/2307.03172) supplies evidence of position-sensitive use of long contexts in the models it studied; it does not measure today's Astra or prove a particular budget optimal. [SQLite FTS5](https://sqlite.org/fts5.html) supplies the offline full-text engine. These are design inputs; retrieval fixture checks here verify routing and budgets, not Astra learning quality.

## Storage and context are separate

`evidence/objects` contains unique exact original files. `indexes/files.jsonl` maps every included original path to its object, so distinct histories remain distinguishable and exact duplicates occupy one copy. Git history, bytecode/cache directories and Finder metadata are excluded with reasons. Runtime dependencies remain archived for reproduction, but do not pollute default scientific search.

`01_CORE.txt` is the initial scientific map. L cards are curated statements from the current report, with precise source paths and explicit unresolved dependencies. P cards preserve previous mathematical records. W cards are selected report extracts and expressly do not replace full proofs. Topic routers, typed support/dependency links, the complete family assessment ledger and source metadata enable further reading without loading giant indexes into a prompt.

Local FTS/BM25 uses document context and favors cards/current proofs. This is lexical retrieval with curated routing; it has no semantic embedding service and no claim of perfect recall. Historical evidence is available with `--history`. Markdown links are recorded as navigation edges, never automatically promoted to logical prerequisites. Proof claims and reported check status remain attached to their provenance stream.

## Learning and continuation

The folder extends accessible inference-time knowledge. Persisting a result does not change model weights, establish mastery, make a supplied oracle cheap or validate a proof. `state/reading_queue.json` starts unread; the agent can record reading, reconstruction and review separately. `state/representations.jsonl` holds reusable abstractions with contracts, guarantees, costs, failure domains and source IDs. Re-ingestion can use `state/ACTIVE_CONTEXT.txt` and a new task-specific packet instead of a transcript dump.

Local execution, the read-only HTTP interface and static HTML/text pages expose the same underlying source IDs. The static export is prepared for web hosting, while actual remote access requires a chosen reachable host. Raw archived instructions/scripts are inert source data; the new small AGENTS.md controls this knowledge folder subject to the current user's request.

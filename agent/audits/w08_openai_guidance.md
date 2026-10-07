# W08 — OpenAI guidance for Astra research context

Date checked: 2026-10-08. Target: GPT-6 Astra (`gpt-6-astra`), as requested.

## Official sources retrieved

- [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) — Astra-specific Codex guidance on concise skill descriptions, progressive disclosure, removing unnecessary always-read instructions, and defining completion/persistence.
- [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra) — Astra behavior and current prompting practices. It says Astra can follow longer instructions but may be more sensitive to instructions present in context; conflicting or unclear skill guidance can make it pause. Audit accessible guidance and make instruction priority explicit.
- [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) — relevant context can be added through retrieval (including file search); context windows are token-bounded; provide precise task logic and data.
- [Compaction](https://developers.openai.com/api/docs/guides/compaction) — API-level compaction reduces long-running conversation context while preserving state needed for later turns. Compaction is a context-management mechanism, not a substitute for an auditable external evidence store.
- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — define the task objective and metrics, use representative/hard cases and expert labels, prefer pairwise/classification/scoring where appropriate, and continuously grow evaluations from observed failures. For document Q&A, evaluate context precision/recall as well as answer quality.
- [GPT-6 Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra) — identifies a 1,050,000-token context window and 128,000-token maximum output. These are API model specifications, not a recommendation to fill the window or a guarantee about long-context retrieval quality.

## Supported recommendations for this research corpus

1. Keep the first-read entry short and route to topic-specific evidence. The Astra-specific guidance explicitly recommends progressive disclosure because every loaded skill/document consumes context and irrelevant instructions can constrain behavior. Do not force a full-corpus read for every research question.
2. Retrieve scoped theorem/result records together with interface, assumptions, dependencies, costs, failure domain, and source provenance. This is a corpus-specific design choice consistent with OpenAI's general recommendation to provide relevant context and constrain answers to selected resources; OpenAI does not prescribe this exact schema.
3. Keep historical instructions and archived material clearly marked as source data, and make instruction precedence unambiguous. This follows Astra guidance about sensitivity to context and conflicts among skills/files.
4. For long-running API conversations, use documented Responses compaction when useful, while retaining external state/evidence identifiers and loading a fresh task-specific packet. The public compaction docs describe API behavior; they do not establish that arbitrary summaries preserve every research detail.
5. Evaluate the retrieval system separately from mathematical correctness. Build held-out questions with expected source IDs, required assumptions, and known counterexamples; score source recall/precision and whether answers preserve scope/status. Expert adjudication is needed for proof validity and novelty. A successful retrieval fixture is not a proof check.
6. Treat context-window capacity as a hard input/output resource ceiling, not a target budget. Test packet sizes and retrieval quality on the actual task distribution instead of assuming larger prompts improve performance.

## Canonical entry inspection and alignment

Inspected `outputs/ASTRA_KNOWLEDGE/exports/ASTRA_BRIEF.txt`, `outputs/ASTRA_KNOWLEDGE/DESIGN.md`, `outputs/ASTRA_KNOWLEDGE/AGENTS.md`, and the `00_START_HERE.txt`/`01_CORE.txt` entry pointers after completing official-doc retrieval.

The current design already uses a compact scientific brief, topic routers, task-sized retrieval packets, stable result/source identifiers, and explicit distinctions among reported, reconstructed, finite-checked, and externally verified claims. Its own design states the corpus is workload-dependent rather than a proven universal optimum, and that fixture checks test routing/budgets rather than Astra learning quality. Those are useful, well-scoped claims and align with the official guidance above.

No code change is indicated by the public guidance. For the system audit, record the following as validation targets rather than implementation assumptions: (a) held-out retrieval recall/precision by topic and query type; (b) packet token cost versus omission/error rate; (c) whether compaction/continuation preserves required provenance and unresolved gates; and (d) confusion rates between source-reported, internally reconstructed, and externally verified statuses. The inspected canonical brief reports no Astra-specific retrieval-quality evaluation, so that performance remains unestablished here.

## Limits of public documentation

The official pages provide model-facing prompt/context guidance and API compaction/RAG/evaluation patterns. They do not verify private Astra tokenizer details, latent-language/hidden-state capabilities, or an optimal external research-context encoding. I found no public official claim supporting such mechanisms; none is assumed here. The model page's context specification also does not establish long-context accuracy or mathematical proof capability.

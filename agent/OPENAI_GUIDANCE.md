# Official guidance consulted for this architecture

Checked 10 October 2026. The dated recent guidance below is within the requested 10 August–10 October window. Continuously maintained documentation has no publication date established by this audit; retrieval recency is not publication recency.

OpenAI's 11 September article recommends small routers, task-dependent disclosure and removing redundant instructions, while accounting for different models using repository guidance. Astra already follows this pattern; this implementation improves the missing access paths and keeps detailed protocols optional. This is an architectural inference, not a measured discovery benefit. [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

The September changelog records releases of GPT-6 Astra, Sol and Luna and new API orchestration capabilities. It establishes recent product changes, not capabilities automatically available to an ordinary ChatGPT conversation. [OpenAI API changelog](https://developers.openai.com/api/docs/changelog).

Current model guidance describes lean instructions, calibrated checking and explicit delegation in a capable harness. This repository keeps mathematical contracts and role-specific handoffs readable across the user's Astra, Sol and Luna conversations; it does not set their model or reasoning effort. [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra).

| Architectural provision | Ordinary web conversation | Local coding agent | API application |
|---|---|---|---|
| Static concept routes, dossiers, exact proof ranges | Fetch through available GitHub/web tools | Read files or CLI | Can fetch same files |
| Durable cross-chat state | Retrieve published checkpoints; draft handoff | Validate, append and publish through Git | Application must implement publication |
| Context selection | Agent chooses relevant files | Agent or bounded packet CLI | Application may choose files/tools |
| Model/effort, persisted reasoning, tool search, compaction, caching | Product-controlled; repository cannot configure | Harness-dependent; repository cannot force settings | Application-controlled when supported |
| Subagent coordination | Requires available product tools or explicit independent handoffs | Harness can delegate distinct work | Requires supported application orchestration |

API compaction returns an opaque continuation object; tool search dynamically loads tool definitions. Neither is a portable repository memory format or a synchronization service. Static mathematical checkpoints remain inspectable and source-pinned regardless of the product's context handling. [Compaction](https://developers.openai.com/api/docs/guides/compaction), [Tool search](https://developers.openai.com/api/docs/guides/tools-tool-search).

No paid service, model call, embedding pipeline, model comparison or research-discovery experiment was introduced. Static byte sizes and software fixtures establish structure only; model-specific performance and scientific effectiveness remain unmeasured.

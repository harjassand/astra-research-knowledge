# Astra research access: 20-worker investigation

Twenty GPT-6 Luna workers audited this external research corpus. The implemented result is a smaller task-first reading interface, safer source access, and explicit obligations for proposed mathematical connections. This does not establish better theorem discovery by Astra, an optimal encoding, external correctness, novelty, or learned model weights. All 186 scientific cards and the original evidence remain unchanged.

## Implemented reading structure

Start with `00_START_HERE.txt`; `01_CORE.txt` is now optional broad orientation. The bootstrap sends an agent to task-relevant metadata, cards, scoped contrasting cases, and decisive source proofs. It does not require reading the whole scientific map or loading the roughly 138,416-o200k-token card collection.

Local access uses `tools/knowledge.py route` for metadata and `packet` for ordinary bounded retrieval. Search citations now open their owning source and chunk range; invalid ranges fail explicitly; read byte limits include line labels; stopword padding no longer changes alias eligibility. Packet text has an optional exact UTF-8 byte ceiling in addition to its existing meter. A JSON wrapper, other prompt content, and tool protocol overhead are outside the packet-text budget.

The optional `tools/bundle.py` admits whole cards, explicit card requirements, and scoped contrasts; it never silently truncates a card. Omitted cards/requirements remain explicit. A bundle does not assert dependency closure or proof certification. Tight budgets can exclude a decisive card: expand the budget or read its source separately. Ordinary packets remain the default because the small fixture below did not show that whole-card bundles dominate ordinary retrieval.

Web access uses `agent/topics.txt`, ten small metadata TSV topic routes, exact `cards/<ID>.txt`, and cited `web/pages/<source-ID>.html`. Raw GitHub URLs can replace `main` with one commit SHA to avoid mixed revisions. `agent/manifest.json` records exact navigation/card hashes. The static GitHub edition has no Python/SQLite service or full cold corpus. `agent/local-tools/` preserves tool source copies; using these requires placing them in the separate full local snapshot. Source availability is still explicit in the existing source maps; previously absent linked proofs have not appeared by inference.

`indexes/agent_catalog.json` contains source pointers, statuses, hashes, and preserved dependency records. Its literal-label parser uses `UNKNOWN` when it does not extract a field; that does not mean the theorem lacks the assumption. `indexes/agent_graph.json` distinguishes 535 provenance, 868 navigation, 47 explicit-requirement, and 189 scoped-relation edges. Requirements create obligations; none of these automatically certifies a premise or permits proof composition.

Seven scoped blocker records cover phase/herald limits, copy-ladder/classicality limits, EPR-star parity, Born curvature, energy contracts, complete-block covers, and exact-oracle/noisy acquisition. They are routing aids with source anchors, not generic impossibility claims. `agent/CONTRACTS.txt` makes symbol and cost mismatches explicit.

`mechanisms/bridge_candidates.json` preserves three source-anchored hypotheses and three rejected transfers. The candidates concern posterior-volume memory converses, relative counting within a restricted passive Gaussian class, and a restricted count-algebra classical-output reconstruction. Each names its interface, charged acquisition, missing lemma, reciprocal restrictions and falsifier. They remain MODEL_HYPOTHESIS / NOT_THEOREM. Session and bridge templates retain source revision, reading depth, exact spans, unresolved assumptions, comparators, and next checks; no fake learned state was initialized.

## Measured results

All token figures use tiktoken 0.14.0 `o200k_base`, an estimate rather than a verified Astra tokenizer. Current bootstrap: 419 local tokens or 278 static-web tokens; see `manifest.json` for its hash-bound counts. The old mandatory local start-plus-core was 5,988 tokens; the old static pair was 5,837. The new core is optional and preserved byte-for-byte. AGENTS instruction overhead is counted separately in validation; it is not included in those bootstrap figures.

A frozen development fixture contains 12 queries with 18 manually source-anchored mandatory card/span requirements. The retrievers receive only the queries, not gold IDs or spans. The engineering team knew the corpus; this is not a blind, held-out Astra capability experiment. Its hash is `4a08b020aa1d9455efc0eccae2f9be3705008832c0093407e20cdec2418ebd35`. The same corpus, maximum 6,000 UTF-8 bytes and 1,500 o200k tokens apply to every packet, including framing.

| System | Required cards | Entire required spans | Mean tokens | Mean bytes |
|---|---:|---:|---:|---:|
| Preserved original packet | 14/18 | 14/18 | 1,352.25 | 5,341.33 |
| Flat lexical BM25 passages | 13/18 | 8/18 | 1,426.00 | 5,859.17 |
| Updated ordinary packet | 14/18 | 14/18 | 1,352.25 | 5,341.33 |
| Optional whole-card contrast bundle | 13/18 | 13/18 | 1,115.42 | 4,350.50 |

All 48 final packets satisfy both ceilings. The ordinary packet shows no recall regression on this fixture; this does not establish improved recall on unfamiliar queries. The bundle trades one required span for roughly 18% fewer mean tokens here. Do not turn that tradeoff into a universal efficiency claim. Answer correctness, interface-transfer reasoning, hypothesis quality, novelty and theorem discovery were not graded by this retrieval fixture; no Astra calls were made for it.

The original baseline implementation was preserved before edits at SHA-256 `7c8258fc879938dfefab9d1aff20d9aff6878163cf26c9a8424ebb6c691f0ee9`. A preliminary mislabeled run accidentally used the edited live script; it is quarantined as `intermediate_updated_results.json`, explicitly NOT the original baseline. The reported baseline was rerun from the preserved implementation. Scientific corpus inputs and retrieval-code hashes are separately recorded. Results, exact packets, hashes, evaluator and adapter are under `agent/evaluation/`; replay currently requires the full local workspace layout and tokenizer dependency paths recorded in the scripts.

A three-snippet compression probe found 296 tokens for the existing dense originals, versus 312 for TSV, 318 for ordinary prose, 322 for compact labeled text, and 341 for JSONL. This is a limited sample, not a global optimum or Astra inference-quality evaluation. No evidence justified replacing mathematical statements with an invented private language. Metadata structure is added for selective access; original mathematical text is retained.

## Remaining capability experiment

The next decision requires Astra on unfamiliar, prospectively frozen tasks: compare this interface with a flat manifest plus search over the identical evidence, with equal context, time, tool, feedback and model settings. Score source recovery, preservation of interfaces/costs, valid transfers, falsifiable hypotheses, and independently checked final artifacts. Count acquisition, failed search, checking and maintenance. Maintain disjoint development and test tasks and preserve complete traces. A blinded expert or executable checker must assess the consequential mathematics. Worker agreement and format tests cannot replace that experiment.

Twenty Luna workers performed the design audits and selected implementation followups. Worker token usage, aggregate inference cost and an end-to-end Astra trial were not measured. No paid hosted embedding, retrieval pipeline or separate API evaluation was provisioned. Proposals for a transactional ingestion rewrite, automatically completed theorem contracts, and model-specific semantic retrieval remain unimplemented rather than being described as acquired capability.

The provenance audit found earlier `VALIDATION.json` snapshots that cover fewer cards. Those historical records remain recoverable and do not validate this release; `indexes/AGENT_ACCESS_VALIDATION.json` names current navigation checks. A constrained web reader reported older unpinned content during its audit; current publication is checked separately against exact commit-pinned raw bytes. Cache observations are not accepted as proof of remote source drift.

The design follows OpenAI's [Astra progressive-disclosure guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra). OpenAI's [agent-evaluation guidance](https://developers.openai.com/api/docs/guides/agent-evals) supports repeatable datasets and traces; its [accuracy guide](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy) separates retrieval failure from model inference failure. These support the workflow choices, not claims of measured research gains.

## Audit inventory

The twenty design reports are in `agent/audits/`: navigation; retrieval; graph; card schema; compression; notation; web; official guidance; evaluation; connections; counterexamples; continuation state; provenance; context allocation; intake; costs; frozen benchmark; adversarial transfers; portable interface; architecture synthesis. Implementation/check reports are additional artifacts. They remain internal model-assisted analyses. Original scientific proof and historical-priority statuses are unchanged.

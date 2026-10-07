# W17 frozen retrieval and transfer benchmark

Frozen before repository optimization on 2026-10-08 (Australia/Brisbane). The benchmark has 12 manually annotated queries over the current `outputs/ASTRA_KNOWLEDGE` corpus. Gold labels point to card IDs and inclusive 1-based line spans. They are source-location judgments only; retrieval scoring does not validate mathematics, priority, or external correctness.

## Tasks

| ID | Task type | Gold cards |
|---|---|---|
| W17-01 | exact_scope_retrieval | L01-cyclic-grid |
| W17-02 | positive_plus_blocker_pair | N46-compact-quantum-classicality, N61-broadcast-copy-ladder |
| W17-03 | external_prerequisite | L02-commuting-repetition |
| W17-04 | version_import_correction | N71-spectral-passive-loss, N74-spectral-loss-sharpness-limits |
| W17-05 | multi_hop_transfer | L08-logconcave-transport, N28-transfer-controls |
| W17-06 | missing_lemma_discovery | N75-covariance-kls-plateau, N28-transfer-controls |
| W17-07 | exact_scope_retrieval | L03-all-field-nine-fourths |
| W17-08 | positive_plus_blocker_pair | L03-all-field-nine-fourths, L04-block-cover-obstruction |
| W17-09 | exact_scope_retrieval | L05-finite-global-rank |
| W17-10 | scope_and_interface_retrieval | L06-relative-field |
| W17-11 | cross_card_interface_correction | N25-acquisition-interface-tests, L01-cyclic-grid |
| W17-12 | missing_prerequisite_and_acquisition_gap | L09-egyptian-supply |

The query text, exact gold spans, and task-specific answer requirements are in the adjacent JSON. The 12 tasks cover exact scope retrieval; two positive/blocker pairs; an external prerequisite; version/import correction; multi-hop transfer; missing-lemma discovery; and acquisition/interface distinctions.

## Frozen evaluation protocol

Run each query with a maximum of 6000 UTF-8 bytes and 1500 model tokens, stopping at whichever constraint is reached first. Count the complete serialized packet, including header and trailer. Report actual packet bytes and tokens per query and their means. Record the exact tokenizer and version (prefer `o200k_base`); if tokenization is unavailable, report tokens as unavailable rather than substituting byte counts.

The primary metric is mandatory card coverage: per-query fraction of mandatory card IDs retrieved, plus micro- and macro-averages over the 12 queries. Also report exact-span coverage: whether retrieved text intersects each annotated inclusive line span. As a secondary source-grounded measure, score the task's answer requirements against the cited spans. Do not score mathematical truth, novelty, or external validation.

The standard equal-information-budget baseline is generic lexical BM25 over all card text, with no curated alias routing or query-specific preselection. Pack top-ranked passages under the same byte and token ceilings. Freeze the BM25 implementation, tokenizer, analyzer, and card-ID tie-break in the run record. Compare systems at identical ceilings and report realized packet sizes. Keep gold IDs and spans out of query inputs and retrieval-visible metadata until packets are frozen.

## Gold annotation boundary

Every gold span refers to the current corpus card itself, so line numbering is directly reproducible with `nl -ba`. For example, the three-line scope in `L03-all-field-nine-fourths` is lines 3–4, with evidence pointers at lines 6–10. The card status fields and caveats remain part of the evidence; no card claim is promoted by its inclusion here.

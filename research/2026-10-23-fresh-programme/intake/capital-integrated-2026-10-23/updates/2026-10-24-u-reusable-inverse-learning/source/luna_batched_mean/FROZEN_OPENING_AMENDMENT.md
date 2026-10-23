# Frozen opening amendment and authorized run

This file preserves the initial opening at `PUBLIC_REPLAY_CHALLENGE_FROZEN.md` and records the specific authorized corrections made before implementation.

1. The task stream is eight tasks with sixteen posterior outputs per task. The next count uses the last of the sixteen outputs. The earlier opening's “one posterior draw per task” wording is superseded; no earlier bytes were edited.
2. Each quadtree node uses the smallest coordinate hull of its grid centers. This makes a singleton cell exactly the grid center and tightens non-singleton domains relative to geometric cell edges.
3. Proposal-cell and within-cell choices use exact lazy-CDF and `randbelow` draws; threshold comparisons extend the same lazy uniform until each rational comparison is resolved. Refinement occurs only after the actual uniform is certified to lie in the current likelihood uncertainty interval. The original selected cell's `U_old` stays pinned through refinement.
4. The authorized comparators are a retained OS* point-rejection method and an exact full-grid posterior/CDF cache. All replay the same lead-generated count sequence, with separate bit tapes and cost ledgers. The full-grid method pays for all 256 exact recurrence evaluations and caches posterior weights/CDFs by observed count.
5. All latent random seeds are in `private_evaluator_seed_manifest_DO_NOT_PASS_TO_LEARNER.json`. They are not part of the learner inputs or public replay. Public replay uses only the visible code, exact events, and consumed bit tapes. Float arithmetic is used only for elapsed-time measurement.

The fixture is synthetic and finite. A deterministic PRNG transcript is a reproducibility fixture, not an empirical demonstration of ideal iid sampling; exact-law reasoning remains conditional on independent fair bits. The run is not a favorable-regime sweep or a practical-cost superiority claim.

The first executable output is preserved unchanged under `v1_superseded/`. The current run applies ordinary-cost fixes: task-start normalizer certificates, OS* reuse of paid points when they later become singleton nodes, eviction of obsolete active-tree CDF caches, explicit integer work for lazy comparisons, and lead-first public replay before the full-grid table is opened.

# Separate independent review: exhaustive open-loop comparator

PASS after two scoped receiving/resource repairs. This does not amend the accepted feedback manifest or its receipt. It is a conditional consumer of the already received polynomial feedback certificate, not another source/provenance verifier or a claim of superior learning performance.

## Final source binding

All ten entries of `FREEZE_MANIFEST.json` were independently checked. Manifest SHA-256: `8b5ce9bfff7cd2124dd53b998a86a32ff06d11b2d2b7e9b60a677ef4b1a6311d`.

- Proof `PROOF_AND_SCOPE.md`: `037182fdd3b527694936c787e2ebce3b61b16cffedefd332fc97c1c2b7c62556`.
- Enumerator `exhaustive_openloop.py`: `2ad053bc4e3466fb1d4ddaa1c9ec2a901d8a4215b86e2ed6e689b2890099efff`.
- Full result: `2c88ca9f312fc136b01008f0d2d30b1d4cc2a87342bc56e604f9d681eb4b5d28`.
- Harness `check_exhaustive.py`: `f204dfc7e38f8a9786a01f1550db34093ab8faba449de3aa7b72f86715a241b7`.
- Harness result: `9e221cb32e1b74ca5bc2e7114377a474097a33315669806d1833039245888d16`.

The entire proof and code were read. Both final run() functions were independently rerun without writing author artifacts: all 16,777,216 words and all 557 exact backend checks passed, with every non-timing result field matching the frozen records.

## Arithmetic proof

The retained nonnegative integer rows have sum D=240,000,000. Starting from the indicator reward scaled by S=2^32, each floor update stays in [0,S]. Every row product and every partial sum is nonnegative and at most D*S<2^64, so uint64 multiplication/accumulation does not wrap. The divisor is also representable. This is not relying on floating-point BLAS accuracy.

For stochastic B=M/D, the approximate vector is componentwise below the exact value and loses less than 1/S per update. Sup-norm contraction therefore bounds its total deficit by L/S. The maximum grid value over all words is below the exact maximum, and that exact maximum is at most the maximum grid value plus L/S. No precision assumption about the identity of the maximizing word is needed.

The binary frontier visits every word once. Splitting at prefix depth four only batches this full tree. Bit ordering of the reported maximizing word agrees with the backward-value products; its reversal is the physical chronological action list. The maximizing grid word is independently replayed with unbounded integers/rationals. The small harness checks every word through length eight, checks the one-sided interval width, rejects an unsafe uint64 precision and checks absence of a cross-horizon gap.

The current interface is the two-action, original indicator-task fixture with a point initial coarse block, not an arbitrary MDP parser. Trusted artifact consumption is explicit. General distributions or different tasks would require their own receiving and value calculation.

## Common-event consequence

Every global open-loop action is a special case of the admitted block-Markov action family. On the SAME previously received polynomial event, the error E bounds both the selected feedback policy and every open-loop word. Thus

    true feedback - best true open loop
       >= coarse feedback - coarse open-loop upper bound - 2E.

No old single-action norm event or second confidence allocation is used. The interval is for expected terminal reward; there is no guarantee for each random rollout or a posterior interpretation conditional on PASS.

For the same 24-step task the retained open-loop optimum is at most approximately .3773533191997558, while the learned feedback policy has coarse value approximately .6244843518542954. Using the exact rational E from the polynomial receiver gives a true gap lower bound approximately .21832641998609595. Exact rational output defines this claim; decimal displays do not improve it. A randomized open-loop choice is a convex combination of fixed words and cannot exceed their maximum expected value.

This is a concrete action-information distinction: the feedback policy uses realized state labels and the retained block map. An open-loop word does not. Ordinary coarse-MDP planning with the same certificate achieves the same feedback policy. The gap is not an exclusive compiler advantage or a learning/sample-complexity lower bound.

## Repairs preserved rather than erased

1. Original source `8eda8e0e...` emitted a purported same-horizon gap even for short backend-test lengths, using the fixed 24-step feedback value. I flagged this; the author reported an independently contemporaneous fix. Current code emits null gap fields unless the requested length equals the recorded horizon. The old bytes are preserved under `historical_pre_horizon_scope/`. The genuine length-24 bound was unaffected.
2. Source `19d00c48...` used `(front@M.T)//D` while its peak-array bound charged only one temporary. I flagged that the matmul input and newly allocated division output may coexist. Current code explicitly divides the matmul temporary in place, assigns it, then deletes it. The old source and result are preserved under `historical_pre_peak_memory/`. Current bulk-array accounting includes old frontier, new frontier and one explicit temporary, and explicitly excludes small retained arrays, Python objects and internal library scratch. It is not a complete process-RSS bound.

The exhaustive route pays 536,870,880 coarse integer scalar products; it is exponential enumeration, not an efficient general open-loop optimizer. No new source observations were used, and the earlier acquisition/retained-state/sensor-interface costs remain. No historical novelty or end-to-end practical advantage is inferred.

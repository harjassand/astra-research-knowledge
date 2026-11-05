# Independent distance-21 circuit feasibility audit

**Correctness: PASS. Target decision: INCONCLUSIVE.**

The fixed 10,000-trial run produced seven accepts. Its exact outward 99.9% modeled failure interval is **[5.591279015181958e−13, 8.565926177314925e−12]**, including the complete circuit-conversion and dyadic-rounding total-variation budget. This straddles the predeclared target 1e−12, so it neither certifies meeting the target nor establishes that the target is missed. The sample size was not extended.

## Independent checks

- Source comparison confirms the same distance-13 algorithm and integer checker, with only the announced input filename, default count, seed and output changes. All precommitted source and frozen-input hashes match.
- All **6,774,016 folded-state inequalities**, **1,937,884 transitions**, and 105,844 scalar-state inequalities pass independent arbitrary-precision verification. The exact contraction bound is 16/17. Actual intermediate arithmetic needs at most 122 bits, so uint128 is safe on this input.
- The exact normalizer is 5516128755926106386249697631 / 1329227995784915872903807060280344576, approximately 4.149874042239687e−9.
- Independent forward propagation checked all **197,924 Pauli generators** from **73,583 original noise channels**, all **26,461 merged probability brackets** and gauge identities, plus 100 separate stabilizer simulations. The projected law contains 4,840 selected detectors and L0.
- Fixed-seed replay reproduced every category: seven accepts, 2,833 nonsimple paths, 95 negative-score rejections, 260 fold rejections, 4,438 nonfailures, 2,366 other witnesses and one null outcome.
- Every one of the **6,811 decoder calls** was checked for zero residual syndrome and original L0 parity. There were 2,373 logical failures before canonical-witness rejection. Mean steps 26.7093, maximum steps 54 and maximum true score 78 all match.
- Reverse exact binomial sums independently certify the CP endpoints. The conversion budget was recomputed directly from every rounded probability and original enclosure, not copied from the producer summary.

## Resource accounting

The original host timestamps show 258.37 seconds from precommit to the completed pilot resource record, below the 20-minute budget. The largest observed RSS was 438,888 KiB, approximately 428.6 MiB, below 2 GiB.

The original acquisition recorded only internal function time. A separately monitored complete acquisition subprocess was therefore repeated and reproduced the frozen graph byte-for-byte. Adding that 15.541-second acquisition replay to the original table, certificate and pilot subprocess stages gives **93.465 seconds of separately measured complete stage work**. This is not a single uninterrupted benchmark or a speed claim. See `resource_addendum.json` for the exact stage measurements.

## Scope and remaining assumptions

The result concerns the specified 21-round, distance-21 Z-basis logical-memory circuit at exact rational p=1/1000, one selected detector sector plus L0, and the fixed integer-cost minimum-weight decoder. It is not a hardware reliability bound or a claim about both logical sectors or a correlation-aware decoder. Ideal independent random bits and the decoder's exact minimum-weight contract remain explicit assumptions.

The graph conversion error budget targets exact rational circuit p. It does not silently include the distinct binary64-parameter Stim sampling law. No new algorithm, favorable general scaling, or superiority over a matched optimized circuit-level splitting method is established by this pilot.

## Files

- `check_certificate.py` and `certificate_audit_results.json`: full independent certificate verification.
- `audit_d21_projection.py` and `d21_projection_results.json`: independent circuit projection checks.
- `verify_pilot.py` and `pilot_audit_results.json`: source equivalence, exact confidence, event checks and full deterministic replay.
- `resource_addendum.json`: complete subprocess resource readback and repeated acquisition hash verification.

The main sampler hash is 995e935ff7086e2f64d65a76e049e85b68ee8920ebb72158d70deabbd84195f7. The input graph hash is 34da7d8ec1a79176a7e5262baa69fafa49d0742639e92a76e5ccaf249107b493. The table hash is faa644147d8a9c0048cf0c896e210c92903d05c19cb142a28446246d36459f8f.

Run scripts with the pinned Python/scientific-library environment used in the main package. The original-host timestamp measurement is historical metadata; timestamps on copied files are not a new benchmark.

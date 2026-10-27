# Exact conditional photon-affinity reader

`photon_certificate.py` streams fixed-N two-channel paired bright/dark blocks,
validates rational photon codes, clips WHOLE blocks, computes eight exact
empirical means/unbiased variances and conservative rational confidence/bias
bounds, then returns a rational maximum-cycle-affinity lower bound or UNKNOWN.
It closes the reviewed operation's missing record-to-certificate interface.
It acquires no instrument, source qualification, physical records, IID law or
calibration, and claims no statistical/solver advantage.

## Use

Existing Python3 and its standard library only; no new packages.

    python3 photon_certificate.py YOUR_RECORDS.jsonl -o conditional_result.json

For stdin use `-`. See FORMAT.md and header.example.json. One JSONL header
freezes N>=2, both cutoffs, external per-record conditional count-mean ceilings,
TOTAL-dataset failure budgets, coding error eta, and analysis-frequency/gate/
capture/coder/precommitment references. It is followed by exactly N numbered
blocks, each with bright_a,bright_b,dark records for both channels. Every
count equals the explicit phasor-list length; every rational [re,im] has
re²+im²<=1. No timestamp sine/cosine or other transcendental is evaluated.

The reader waits for EOF. Missing/extra/blank/reordered/malformed/nonfinite/
count-mismatched input gives INVALID_INPUT, exit2, with no bound. JSON binary
floats and duplicate keys are rejected. A valid file gives exit0, with either
CONDITIONAL_LOWER_BOUND or UNKNOWN. The iterator API accepts only bytes/text
lines: None cannot masquerade as EOF. If EITHER channel's block count exceeds
its cutoff, ALL8 coordinates become0; the block stays in N and every event is
still validated and billed. Count equals cutoff is retained.

Results retain header, hashes, exact sums/squared sums, empirical moments,
tail/bias/root receipts, guards and failure sum. `affinity_squared_lower` is
36*rlo_squared/(1-rlo_squared), a rational. `affinity_lower` is a LOWER rational
square root. Confidence logarithms/roots are conservative UPPER enclosures.
The proof uses pi>3. Observed maxima are diagnostic only, never acquired caps.
ARITHMETIC.md explains the finite rounding chain.

## Conditional meaning

All source/readout promises remain SUPPLIED: stationary finite-state irreducible
bidirectional all-even Markov dynamics; real nonnegative emissions; passive
COMMON gate before separate fixed causal responses; deterministic repeated dark
background; qualified complete capture/reset or charged tail bounds; conditional
independent Poisson readout; acquired conditional photon-mean ceilings; fixed
qualified coding; independent a,b,d records and IID stationary blocks, or paid
preparation/coupling guarantees. Finite counts do not verify those promises.

Every alpha_other_total value must ALREADY bound a TOTAL DATASET failure.
Per-record failures must first be accumulated externally; all capture,
preparation, coupling, coding/readout and other failures must be included or
supplied as exact promises. The example's1/100 statistical+1/200 preparation+
1/200 coupling gives49/50 conditional confidence (98%), not99%.

Frequency/gate/coder/N/cutoffs must actually predate the data. A header/hash
fixes one execution, not historical precommitment, protection from repeated
post-data reruns, device authentication or physical qualification. All outputs
explicitly retain physical qualification=False and this caveat. They describe
maximum microscopic simple-cycle LOG RATE RATIO, not entropy-production rate.
Reservoir entropy per traversal additionally needs supplied local detailed
balance. UNKNOWN is not evidence of equilibrium. rlo_squared>=1 is UNKNOWN/
inconsistent geometry, never a clipped spectacular finite estimate.

## Verification and review

    python3 photon_certificate.py NONPHYSICAL_TINY.jsonl -o NONPHYSICAL_TINY_RESULT.json
    python3 -m unittest -v test_reader.py
    python3 replay.py

Every generated fixture/result is explicitly NONPHYSICAL_SOFTWARE_TEST. No
IID/Poisson/Markov/physical cap or clock validity is claimed. The deterministic
positive branch fixture exercises arithmetic ONLY; its positive number is not
an observed affinity or statistical success. Tests cover independent8-coordinate
hand aggregation, variance/clipping, conjugation/phase cancellation, malformed
clipped records, fixed-N/EOF, budget scope, exact root/log bounds, independent
Poisson tails, positive transport and UNKNOWN guards. No random records are
generated. A supplied physical-data stream is not automatically qualified.

The governing notes were whole-read at their final reviewed hashes; see
GOVERNING_MATH.json. Root separately completed independent final code/arithmetic
acceptance at SHA256911c9888e11d858fefa66f0c36c903faa7f9e371fe925ff237d90490675965c9:
literal stats/whole clipping;13 malformed CLI and3API cases; independent exact
Poisson enclosures;28sqrt/5log bounds; exact geometry/conjugation; full NONPHYSICAL
positive branch. Root found the intermediate None/EOF bug; a unique sentinel
and Unicode validation fixed it, and all regressions pass. Source deltas and
review receipts preserve this history. This is completed internal correctness
review at its actual conditional scope, not physical qualification or a demand
for another default audit.

The reader preserves the established empirical-Bernstein, source sector/cycle
and ordinary mean-calibration credit. It invents no new inequality or priority
claim. The strongest ordinary comparator receives the same records, envelopes,
calibration and mixing information and may use the SAME clipping/empirical-
Bernstein operation. Numeric population-power planning is separate from this
observed-record inference interface and is not an inference input.

## Costs

Inputs cost2N bright+N dark TWO-CHANNEL records:3N gated records,6N channel
records. ALL photons are processed, including clipped blocks. Source gaps,
stationary preparation, gating, full response/tail capture, dark acquisition,
cap/coder/detector calibration and physical-failure qualification remain
external costs; none was acquired or timed here.

Software performs O(events+N) rational operations for validation/features/16
accumulators, plus O(K1+K2) Taylor operations and exact integer square roots.
These are not unit-bit-cost or polynomial-in-binary-N/K guarantees. Memory is
one full JSONL block plus16 fractions, whose bits may grow with TOTAL input
encoding for varying denominators. It is not constant memory in bits; a common
fixed coding grid is more economical. Large encodings face runtime resource
limits. Tail arithmetic is linear in cutoffs, not their bit length.

The log upper ceil(log2(32/alpha_stat)) is intentionally conservative (e>2).
Thus this exact reader does not inherit the population planner's unrounded
power/sample figures or any matched-power advantage. Exact rounding costs no
extra failure probability but can reduce power. Selected fresh-process times
are NONPHYSICAL software receipts only. Total research/setup/source-reading
and physical acquisition costs remain uninstrumented; no full-cycle advantage
is inferred. Byte hashes establish identity, not physical truth.

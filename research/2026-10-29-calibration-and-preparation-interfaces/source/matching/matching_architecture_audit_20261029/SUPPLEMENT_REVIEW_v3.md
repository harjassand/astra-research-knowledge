# Independent review of sharpness and implementation/comparator supplements
2026-10-29. Accepted at stated scope. Sources EXACT_PARTIAL_SWAP_SHARPNESS_v2.md and COMPARATOR_AND_RESOURCE_SCOPE_v3.md in matching_survival_20261029.

The exact partial-swap proof is identical in substance to the independently accepted root derivation in RATE_REVIEW.md. Its formulas and endpoint n=4,t=pi/2 are correct. It strengthens the earlier small-angle existence argument without changing the all-CPTP inequality or claiming subcode-factor sharpness.

The two-logical-basis comparator is correct. I independently opened Zeng–Zhou–Liu https://arxiv.org/html/1911.06855 and read equations21–23: the g-MUB test gap is (g-1)/g, giving coefficient2 for two bases. Computational and full Hadamard-product bases are mutually unbiased in dimension2^k. Full-Clifford preparation is unnecessary for this weaker constant-factor comparator. The physical encoder and decoder remain necessary in this implementation.

The displayed pair circuit produces (|01>-|10>)/sqrt2 and its Bell-readout result is11. Per pair it uses two CNOTs and four single-qubit gates across preparation/readout, so n CNOTs and2n single-qubit gates for n/2 pairs are correct, before frame rotations/routing. The nearest-neighbour permutation upper bound and depth use ordinary adjacent sorting and retain the labelled source boundary; they are compatible with the separately reviewed quadratic lower bound. These are ideal gate counts, not noise-tolerant or physical timing guarantees.

Historical novelty, superior total cost and generic unknown-noise recovery are explicitly not established. No correction required to these supplements.

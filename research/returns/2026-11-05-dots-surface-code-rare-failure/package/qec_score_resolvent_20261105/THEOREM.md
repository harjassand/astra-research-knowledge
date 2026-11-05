# A finite score-folded cover for canonical QEC witnesses

## Scope

This is an exact rational importance sampler for one fixed, independently specified circuit-noise/decoder model. It is not a new hardware acquisition, a general polynomial-time logical-error estimator, or a claim of superiority over optimized splitting methods. The canonical-witness construction and its possible exponential overlap cost remain. The operation below removes most of the additional exponential-tilt normalization loss on the acquired distance-13 circuit graph.

## Inputs and retained witnesses

The graph has independent edge faults with probabilities q_e, positive integer decoder costs c_e, and designated left/right rough boundaries. A deterministic minimum-cost decoder returns C(E). On a logical failure, a fixed breadth-first rule selects one simple left-to-right path P in E XOR C(E).

Minimum-cost optimality gives S(P,E)=sum_{e in P} c_e(2E_e-1) >= 0. The proof compares C(E) with C(E) XOR P. A consecutive pair of clean path edges belongs to C(E). If a strictly cheaper direct triangle edge connects its endpoints, toggling that triangle would lower C's cost. Thus excluding such clean-clean pairs preserves every canonical witness. This necessary restriction is inherited from the independently audited circuit construction; it is not a sufficient failure test.

## The finite lift

An automaton state a records an oriented edge and its fault bit b. Its increment is delta_a=c_e(2b-1), and its tilted weight is w_a=P(E_e=b)2^{delta_a}. Immediate backtracking is disallowed; transitions terminate at any rough-boundary leaf. The optional clean-triangle restriction is imposed.

Fix an integer modulus N. The additional state r is the accumulated score modulo N, in {0,...,N-1}. A right-boundary terminal has weight t(a,r)=2^{-r}; other terminals have weight zero. Let T_N be the positive continuation matrix, with transition weight w_j and updated residue r+delta_j modulo N.

Any finite nonnegative rational array H satisfying H >= t+T_N H is sufficient. It need not be an exact inverse or fixed point. Define the rational initial normalizer

Z = sum_{a beginning at a left boundary} w_a H(a,delta_a mod N).

Choose that initial state with probability w_a H/Z. At a live state, use continuation probabilities w_j H(j,r+delta_j)/H(a,r), terminal probability t(a,r)/H(a,r), and reject with the remaining probability. All probabilities are nonnegative by the verified inequality. States with H=0 have zero incoming selected mass and are never divided by zero.

Keep the actual integer score S, not merely its residue. Reject immediately if a vertex repeats. At a right terminal, reject S<0; otherwise accept an additional fair-bit coin of probability 2^{-(S-r)}. Here S-r is a nonnegative multiple of N.

## Exact path law

Before the final coin, telescoping cancels all H factors. A completed path with marked fault bits has mass

    product_e P(E_e=b_e) * 2^{S-r} / Z.

The terminal coin cancels the factor 2^{S-r} exactly on every nonnegative-score path. Negative scores, including aliases near N-1, contribute zero. Thus every retained simple marked path has mass product_e P(E_e=b_e)/Z, with no aliasing bias. Rational supersolution slack is a null outcome, not an approximation error.

Sample all off-path faults independently from their original q_e, run the fixed decoder, and accept only when the sampled path equals its canonical witness. For each failing E exactly one accepted path is left, and every failure's canonical path was retained. Therefore the final Bernoulli success probability is exactly P_q(failure)/Z. No path-length truncation or tail correction occurs. Immediate repeated-vertex rejection bounds every path trial by the number of graph vertices.

## Integer certificate

The executed input probabilities are rounded to dyadics with denominator 2^64. The exact sum of edge rounding errors plus the original circuit-conversion enclosure gives a total-variation error bound below 8.791e-17. This is added to the final physical-model interval, not silently discarded.

At costs 4/5, all tilted edge weights have common denominator 2^69. H is represented by integers U on the grid 2^-52. A floating resolvent only proposes U. The C++ checker verifies every folded inequality using unsigned 128-bit integer arithmetic, with overflow checks. It also verifies an integer scalar vector W >= 1+T W. The largest W is 17, so this supplies a strict contraction certificate independently of the numerical solver.

If the initial rounded table has maximal upward grid defect d, replace U by U+dW. Since W-TW >= 1, this repairs every row. The checker re-verifies all rows after repair. The executed N=64 table required d=1. Right-boundary 2^-r is rounded upward only when checking the table; the sampler uses its exact unrounded value.

The exact normalizer is

2818187113480842400929869436333 / 1329227995784915872903807060280344576

or approximately 2.1201683401324154e-6. All sampling choices use integer comparisons, including background Bernoulli draws. Python's seeded PRNG is an implementation; exact iid confidence statements assume ideal independent random bits.

## Costs and limits

The N=64 table has 24,340 automaton states, 64 residues, 420,444 allowed state transitions and 12,462,080 raw table bytes. Every path trial has a deterministic finite graph-size bound, followed by at most one decoder invocation. Actual setup, memory and production work are recorded separately.

The score fold does not remove non-simple-walk waste, nonfailure proposals or canonical-witness multiplicity. In particular it does not invalidate the serial-diamond exponential acceptance counterexample in the independent scaling audit. The present result is a complete finite-instance operation, not an all-distance FPRAS.

## Closest prior mechanisms

Exponential tilting, Markov-additive-process importance sampling, Doob transforms and positive supersolution proposals are established techniques. Relevant general literature includes Collamore, Annals of Applied Probability 12 (2002), 382–421, on Markov-additive ruin importance sampling; Karp–Luby union sampling and ALOE (https://arxiv.org/abs/1710.06965) on witness overlap; and Bravyi–Vargo splitting for QEC rare events (https://arxiv.org/abs/1308.6270). The present tested join is the small finite score quotient plus an exact terminal rejection correction and integer supersolution for this acquired circuit graph. No first-use or universal novelty claim is made without a fuller literature review.

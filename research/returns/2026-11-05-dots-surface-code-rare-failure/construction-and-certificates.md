# Canonical witnesses, the exact score-folded sampler and certificates

The [main result](README.md) targets a fixed noise law, graph and minimum-cost decoder. The [final theorem](package/qec_score_resolvent_20261105/THEOREM.md), [initial witness theorem](package/canonical_qec_witness_20261105/THEOREM_AND_SCOPE.md) and [completed independent audit](package/qec_score_resolvent_audit_20261105/AUDIT.md) supply the proof.

## A computable failure cover

Let `E` be the error pattern and `C(E)` the fixed minimum-cost correction. A deterministic breadth-first rule selects one simple left-to-right logical path `P` from a failure residual `E XOR C(E)`. Comparing the correction with its symmetric difference along `P` gives

\[
S(P,E)=\sum_{e\in P}c_e(2E_e-1)\ge0.
\]

If two consecutive path edges are clean, they lie in the correction. A strictly cheaper triangle shortcut would improve it, so those marked transitions can be excluded. Equal-cost shortcuts must remain under deterministic ties. This condition retains all canonical failure witnesses; it is not a sufficient failure test.

Sample a path cover, mark its fault bits, draw ordinary off-path faults and run the actual fixed decoder. Accept only when the sampled path is the error configuration's single canonical witness. That replaces a potentially difficult multiplicity count by one computable indicator. Canonical union sampling and rare-event importance sampling are established principles; the contribution is this tractable geometric cover and exact implementation for the specified QEC target.

## A finite score quotient with exact correction

An automaton state records an oriented edge and its fault bit, with increment `delta=c_e(2b-1)` and tilted weight `w=Pr(E_e=b) 2^delta`. The additional state is accumulated score modulo `N`. Immediate backtracking is forbidden, boundary leaves terminate, and the strict triangle rule is imposed.

For nonnegative transition matrix `T_N` and right-terminal weight `t=2^(-r)`, any finite nonnegative rational table `H>=t+T_N H` suffices. Initial mass is `w H/Z`; continuation and terminal probabilities use ratios of neighboring `H` values. Unused probability is an explicit null rejection. Zero-table states have no selected incoming mass.

The sampler retains the **true** integer score `S`, as well as residue `r`. It immediately rejects repeated vertices, rejects terminal `S<0`, and otherwise accepts a fair-bit terminal coin with probability `2^(-(S-r))`. Telescoping cancels all table factors and the coin cancels the score-folding factor, leaving marked-path mass `Pr(path bits)/Z`. Off-path noise and canonical acceptance therefore give

\[
\Pr(\text{one accepted trial})=\Pr_q(\text{failure})/Z.
\]

There is no aliasing approximation or omitted long-path tail. Every canonical path is simple; immediate repeat rejection gives a deterministic finite graph-size trial bound. Supersolution slack changes efficiency rather than the identity. A separate scalar certificate `W>=1+T W`, with maximum `W=17`, supplies a strict contraction check independently of floating solver diagnostics.

## Exact certificate and production confidence

The modulus-64 production table has 24,340 oriented-edge/fault-bit states, 1,557,760 folded states, 420,444 transitions and 12,462,080 raw table bytes. A floating resolvent proposes the table; integer inequalities decide validity. The original C++ checker uses checked 128-bit arithmetic. The independent Python checker reconstructs transitions from the graph and verifies all inequalities with arbitrary-precision integers. An upward grid-defect repair via `W` is rechecked after application. The sampler uses the exact terminal coin even where certificate construction rounded terminal values upward.

The exact normalizer is

\[
Z=\frac{2818187113480842400929869436333}
{1329227995784915872903807060280344576}
\simeq2.1201683401\times10^{-6}.
\]

The [certificate audit receipt](package/qec_score_resolvent_audit_20261105/certificate_audit_results.json) retains all-row verification. The [finite exact audit](package/qec_score_resolvent_audit_20261105/finite_exact_results.json) tests cyclic graphs, null slack, negative and multi-period scores, triangle pruning and deliberately incorrect rounded terminal coins. Exact enumeration recovers the independently computed target in all valid variants and detects the biased variant.

Fixed-sample binomial confidence endpoints use exact outward integer tail inequalities. Floating beta quantiles only propose endpoints; exact verification or bisection determines validity. The independent audit includes adversarial invalid quantile proposals.

The [production audit](package/qec_score_resolvent_audit_20261105/production_audit_results.json) reproduces all 100,000 fixed-seed categories and inspects all 84,073 decoder calls for zero residual detector syndrome and original logical-observable parity, rather than only a gauged cut. It reproduces the exact normalizer, interval fractions and conversion expansion. This is a completed supplied internal audit, not a new Capital replay.

## Exact circuit marginal and the model boundary

The [projection audit](package/canonical_qec_circuit_audit_20261105/AUDIT.md) proves a complete one-basis-plus-logical marginal factorization for uniform depolarizing channels and independent declared flips. Independent Bernoulli factors on all nonzero effect-image vectors reproduce the channel's Fourier coefficients. This preserves the projected correlations; replacing correlated qubit faults by independent marginal flips would be invalid. Arbitrary nonuniform Pauli channels do not automatically admit this factorization.

Original rational conversion enclosures plus dyadic edge rounding produce the complete TV budget below `8.791e-17`, included on both sides of the final interval. That budget belongs to exact rational circuit `p=1/1000`. A simulator with literal binary64 noise parameters is a distinct law, and its floating detector-error-model agreement is diagnostic rather than the source of the tiny certificate.

Binary tables, `.npz` traces, scripts and certificates are preserved byte-for-byte without loading numerical arrays or executing the research programs in this publication.

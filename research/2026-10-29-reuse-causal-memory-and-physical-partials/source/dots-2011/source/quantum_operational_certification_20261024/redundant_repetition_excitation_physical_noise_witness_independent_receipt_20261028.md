# Independent receiving: physical bit flips supply repetition-patch excitation

2026-10-28 18:14 UTC. **PASS, scoped corollary** for `redundant_repetition_excitation_physical_noise_witness_20261028.md`, SHA256 `55736dd9aa480457eeacf8598374a308c94d5cd2f133d0afb337c33e38207f56`. No author or received source was modified by this review.

## Accepted derivation

The ordinary repetition isometry followed by three independent physical X flips decomposes exactly, INCLUDING logical off-diagonal matrix units, into two abstract logical Pauli branches under the reversible majority/syndrome unitary. Each physical pattern is uniquely either a weight-at-most-one syndrome representative e_g or its complement 111 XOR e_g. Consequently the two positive gauge blocks are exactly the diagonal GI/GX stated in the source. A fixed arbitrary three-qubit output mixer V merely conjugates the common logical algebra; it preserves width-three locality, spectra and all CP-order comparisons.

For 0<p<1/2, GI-GX>=0 coordinatewise. The Bell-block POVM argument therefore makes ideal majority/syndrome extraction, after undoing the unknown mixer for the informed oracle, optimal among ALL full-CPTP logical receivers. Its loss is `3p²-2p³`. The CP X contrast is the total gauge block, while the Z contrast is GI-GX; its minimum relative contrast is exactly `1-2p`, attained on the weight-one syndrome sectors. The output marginal and smallest signed gaps are exactly

    r=p(1-p)/2,
    gamma=p(1-p)(1-2p)/2.

These are actual physical-noise-generated excitation scales, not free gauge-preparation controls. The full-support example therefore instantiates the acquired-gap theorem using only the declared ordinary source/readout interface.

The supplied coarse margin remains essential: the source correctly requires a trusted rational `kappa0<=1-2p`, for example from p<=p_max<1/2. Actual p and excitation are not supplied, and the fine direct-gap guard can adapt to the true gamma, but this does not eliminate the coarse kappa0 cost. The finer inverse-epsilon rate is only the parent's instance-sensitive capped acceptance guarantee, not a universal acceptance statement or a practical-budget claim.

After successful operator certification, a changed gauge occupation is licensed by the parent fixed-algebra theorem, not by an assertion that independent bit flips generate every coherent gauge state. More general future maps still need the explicit fixed-U/source-family and current dominance promises. The source's p->0 and p->1/2 limitations are correctly stated: nearly noiseless current-gauge recovery may be easy even while all-gauge completion is hard to certify, and a vanishing Z contrast invalidates the acquisition margin.

## Independent exact evidence

`redundant_repetition_excitation_physical_noise_independent_check_20261028.py/json` uses a separate direct physical-Kraus construction rather than the author's Bell-block assembly. It checks four different rational p values with two nontrivial exactly rational ENTANGLING output mixers V. For all 32 logical matrix-unit cases, 2,048 complex rational output entries exactly equal the asserted GI/GX subsystem model. Exact inverse-majority reduction yields `(1-ell*)E+ell*XEX` on every coherent matrix unit. It also verifies unitary mixers, anticommuting width-three generators, floors, signed gaps, all syndrome CP-order inequalities and a supplied class margin distinct from actual p.

The author's six-level exact check was read and its source/check bindings reverified; this review did not rerun or overwrite its output. The independent script uses zero source samples and zero RNG draws. There is no production learner, source tomography run, hardware invocation, noisy gate benchmark or external priority claim.

The companion JSON binds this corollary source, author evidence, independent evidence, the acquired-patch main theorem and its exact main receiving files. This is a narrow physical-instantiation corollary, not a substitute for the parent's confidence/abstention and implementation ledger.

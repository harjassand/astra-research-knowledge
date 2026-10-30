# Primary comparison check: no all-rate transfer theorem located

Internal focused search, 2026-10-30. This is not an exhaustive literature nonexistence claim.

## Decisive primary-source checks

1. Campos, Bruno, Fu, Del Vecchio, Williams, *Comparison Theorems for Stochastic Chemical Reaction Networks*, https://arxiv.org/pdf/2302.03091 . Theorem 3.5, page 12 of PDF (printed page 12/section starts on printed 11), assumes BOTH chains irreducible and positive recurrent before comparing their stationary distributions. It also requires the preorder/coupling hypotheses of Theorem 3.1. Thus this theorem cannot establish recurrence merely from bounded ratios to a balanced reference. Their infinite-state examples establish recurrence separately through explicit Foster-Lyapunov functions in SI Section S.1. The comparison is stochastic ordering of increasing/decreasing sets, not an entrywise factorial-density estimate.

2. Thiede, Van Koten, Weare, *Sharp entrywise perturbation bounds for Markov chains*, https://arxiv.org/pdf/1410.1431 . Finite state space throughout. Theorem 3 and Corollary 2 bound log stationary-density changes using entrywise perturbations divided by Q_ij(S), a probability of hitting j before returning to i or being killed in an auxiliary substochastic chain S. Theorem 4 proves these sensitivity coefficients essentially sharp. Applying this on growing chemical truncations requires new uniform quantitative control of those probabilities and of the sum over perturbed entries. Multiplicative rate comparability alone does not supply that control.

3. Solan and Vieille, *Perturbed Markov chains*, J. Appl. Prob. 40 (2003), 107–122, author PDF https://www.math.tau.ac.il/~eilons/result14.pdf , also https://arxiv.org/abs/math/0306248 . The paper explicitly concerns finite-state discrete-time chains. Its relative-perturbation/graph-theoretic framework is not itself a countably infinite recurrence-preservation theorem.

4. Cappelletti and Wiuf, *Product-form Poisson-like distributions and complex balanced reaction systems*, https://arxiv.org/abs/1507.02195 . Establishes the structural product-form/complex-balance connection and a stochastic deficiency-zero theorem; it does not license arbitrary changes of rate constants outside complex balance while retaining a factorial comparison envelope.

## Exact elementary finite-state bound and why it does not finish the task

If two N-state irreducible CTMC generators satisfy M^−1≤q'(x,y)/q(x,y)≤M on common off-diagonal support, the directed matrix-tree formula gives

    M^−(N−1)≤tau'_r/tau_r≤M^(N−1),
    M^−2(N−1)≤pi'_r/pi_r≤M^2(N−1).

This follows by multiplying N−1 edge factors in each tree and then normalizing; no perturbative smallness is needed. For an n-radius d-dimensional truncation N=O(n^d), however, its exponential loss is exp[O(n^d)], not the desired exp[O(n)]. For d≥2 it can overwhelm factorial decay exp[−Theta(n log n)]. Worse, naive deletion/reflection of edges from a nonreversible complex-balanced reference need not preserve its restricted stationary distribution. Chemical truncations must address this separately.

## Conclusion

The sought theorem was not found. The strongest directly checked SCRN comparison theorem assumes the very recurrence needed here. Existing generic finite-state estimates expose an additional global hitting/geometry problem rather than remove it. A genuine chemical result would need to use the fixed finite translated reaction-cycle structure, not only a factorial reference distribution and uniform multiplicative rate bounds. The accompanying explicit counterexample proves this last distinction is substantive.

# Native excursion entropy completion: targeted primary-source comparison

Date: 2026-10-29. Author: Astra child branch `controlled_realization_frontier`.

## Finding and scope

The strongest primary sources inspected establish event-law entropy estimators, equality conditions within a given hidden network, and constrained minimization over hidden models. They do not, in the passages and constructions inspected, establish the proposed matching realization theorem over arbitrary finite hidden dimensions and arbitrary hidden parity. This is a bounded collision check, not a priority determination.

The prospective addition is specific: an entropy-controlled finite continuous-time Markov completion of a native port-excursion record, in a stated approximation topology, with physical reversal fixing the resolved ports, exact port clocks and total mean, and no prior bound on hidden dimension or rates. The event-law KL lower bound, phase-type approximation, and the idea of minimizing hidden entropy are established ingredients. Their combination becomes a substantive theorem only after the matching realization, boundary convention, and convergence obligations are proved.

Use stationary flux densities `K_ij(t)` per unit physical time and direct port fluxes `d_ij`. The established observable expression is

\[
\sigma_{\rm event}
=\sum_{ij}\int_0^\infty K_{ij}(t)
 \log\frac{K_{ij}(t)}{K_{ji}(t)}\,dt
+\sum_{i\ne j}d_{ij}\log\frac{d_{ij}}{d_{ji}}.
\]

An unnormalized excursion measure requires the corresponding common stationary normalization. The candidate theorem concerns the infimum in a weighted-L1 **closure**, not exact realization of every continuous density by one finite CTMC.

## Decisive primary comparisons

### 1. Ehrich 2021: full-record fitting, with hidden-state count fixed

[Jannik Ehrich, *Tightest bound on hidden entropy production from partially observed dynamics*, J. Stat. Mech. 2021, 083214](https://arxiv.org/pdf/2105.08803), DOI 10.1088/1742-5468/ac150e. Read v2, especially §4 and §5, manuscript pp. 13 and 18.

The discrete-time fitting construction assumes that the correct number of hidden states is known. It retains the complete observed jump statistics, rather than only a few moments. In §5, Ehrich explicitly asks whether admitting more hidden states and cycles can lower the fitted bound all the way to time-series irreversibility. A continuous-time extension is suggested, not proved there.

The proposed completion addresses a related question, but it enlarges the class in two material ways: arbitrary hidden parity and approximation rather than exact preservation. It must not be presented as resolving Ehrich's ordinary-reversal, exact-realization problem. The primary antecedent is unusually close because the question itself is explicit.

Receipt: `turn580view2`; additional inspected passage `turn575view0`.

### 2. van der Meer, Ertel and Seifert 2022: the observable entropy and fixed-model saturation

[Jann van der Meer, Benjamin Ertel and Udo Seifert, *Thermodynamic Inference in Partially Accessible Markov Networks: A Unifying Perspective from Transition-Based Waiting Time Distributions*, Phys. Rev. X 12, 031025](https://arxiv.org/pdf/2203.12020), DOI 10.1103/PhysRevX.12.031025. Read v2, especially §V B and its four rules.

The paper obtains a waiting-time estimator as semi-Markov entropy production. Its topology rules characterize equality within the underlying ordinary Markov network. Removing the observed edges and leaving a topologically trivial hidden network gives saturation. A duration-dependent forward/reverse ratio implies a hidden driven cycle and a strict underestimate in that network. The converse implication can fail under special symmetries.

These statements do not construct a different hidden model approaching the observable entropy. In particular, the prospective paired-parity realization changes the permitted microscopic reversal class. It is compatible with the cited strictness result because it is outside that ordinary-reversal equality criterion.

Receipt: `turn575view3`; primary source `turn571view3`.

### 3. Degünther, van der Meer and Seifert 2024: Markovian snippets and the odd-variable boundary

[Julius Degünther, Jann van der Meer and Udo Seifert, *Fluctuating Entropy Production on the Coarse-Grained Level: Inference and Localization of Irreversibility*, Phys. Rev. Research 6, 023175](https://arxiv.org/pdf/2309.07665), DOI 10.1103/PhysRevResearch.6.023175. Read the 2023 preprint, equations (8), (28)–(31), §IV A–C and Appendix A.

Their physical snippet entropy uses the final event probability `P(J)` in the system boundary, not `P(Theta J)`. Their odd-variable examples explain why the latter substitution can create a nonzero system-entropy change on a closed physical trajectory and spoil additivity. They establish a conditional coarse-graining relation and entropy inference; the inspected sections do not give a universal minimal-entropy hidden completion.

This is a direct constraint on the new theorem's formulation. A stationary law need not be parity invariant. Physical additive entropy and KL against the stationary parity-reversed path law then differ by a preparation boundary, although their long-time rates agree. Section 3 below derives that distinction for the proposed channels.

Receipt: `turn580view1`; earlier primary passage `turn575view1`.

### 4. Ertel, van der Meer and Seifert 2022: thermodynamic consistency restricts Markov embeddings

[Benjamin Ertel, Jann van der Meer and Udo Seifert, *Operationally Accessible Uncertainty Relations for Thermodynamically Consistent Semi-Markov Processes*, Phys. Rev. E 105, 044113](https://arxiv.org/pdf/2111.13113), DOI 10.1103/PhysRevE.105.044113. Read §IV B, §VI and Appendix C of v2.

The paper explicitly distinguishes mathematical Markov approximation of singular waiting laws from its thermodynamically consistent state-lumping class. Its Markov-based uncertainty relation rules out some semi-Markov processes from that class, despite the availability of mathematical Markov approximations. The construction and proof use ordinary Markov-network entropy and a specific lumping interface.

This is a consequential comparator, not an obstruction to arbitrary hidden parity. The new result must explain why its allowed reversal mechanism and information interface differ. Calling every phase-type approximation thermodynamically equivalent would miss the issue this source isolates.

Receipt: `turn576view0`, especially manuscript p. 6; Appendix C inspected in `turn575view2`.

### 5. Aldous and Shepp 1987: Erlang approximation is old, with a sharp state cost

[David Aldous and Larry Shepp, *The Least Variable Phase Type Distribution Is Erlang*, Communications in Statistics—Stochastic Models 3, 467–473](https://escholarship.org/content/qt7w51x4rb/qt7w51x4rb.pdf), DOI 10.1080/15326348708807067. Read original pp. 467–468 from page images, not the repository's misordered author metadata.

The abstract already describes Erlang phases as a method for approximating arbitrary semi-Markov processes by Markov processes. The paper proves that an absorption time using `n` transient phases satisfies `Var(T)/(E T)^2 >= 1/n`, with equality for an Erlang chain with equal rates.

Thus phase approximation is a conventional ingredient, and increasing time concentration has a concrete state cost. For an Erlang duration of mean `tau` and relative standard deviation `eta`, at least order `eta^-2` phases are needed within this class; the equal phase rate is `n/tau`. The completion theorem does not give a bounded-clock or bounded-memory physical implementation for free.

Receipt: `turn580view3`, `turn580view4`; source `turn579view1`.

### 6. Nitzan, Ghosal and Bisker 2023: strongest equally informed constrained optimization

[Eden Nitzan, Aishani Ghosal and Gili Bisker, *Universal bounds on entropy production inferred from observed statistics*, Phys. Rev. Research 5, 043251](https://doi.org/10.1103/PhysRevResearch.5.043251). Primary preprint: [arXiv:2212.01783](https://arxiv.org/pdf/2212.01783).

The full-record optimization is stated for hidden systems with the same hypothesized topology. It then replaces equality of waiting-time functions by a hierarchy of moment constraints suitable for numerical optimization. The conclusion explicitly leaves universality of a simpler hidden topology unresolved. The ordinary stationary flux entropy is the objective.

Given actual topology, dimension, or parity information, this optimization can provide stronger bounds than the unrestricted completion value. The proposed theorem would explain what remains when those structural restrictions are absent; it would not outperform an equally informed optimizer that is allowed to use genuine additional structure.

Receipt: `turn579view0`, equations (16)–(18); conclusion `turn580view0`; published full-text search receipt `turn577search0`.

## Boundary and channel calculation

The following is an independent algebraic check, not a claim extracted from the literature and not a review of the entire completion proof.

Let `Q` be a finite irreducible row generator with strictly positive stationary law `pi`, and let `Theta` be a permutation involution. Write

\[
Q^*=\Pi^{-1}Q^T\Pi,\qquad
R=\Theta Q^*\Theta,\qquad
\pi^\Theta_x=\pi_{\Theta x}.
\]

`R` is the generator of the stationary path reversed in time and then transformed by `Theta`; its stationary law is `pi^Theta`. For finite relative entropy, set

\[
\sigma_\Theta
=\sum_x\pi_x\left[
\sum_{y\ne x}q_{xy}\log\frac{q_{xy}}{r_{xy}}
+\lambda_R(x)-\lambda_Q(x)\right].
\]

The KL chain rule for the initial state and conditional jump path gives the exact finite-horizon identity

\[
D(P^\pi_{Q,[0,T]}\Vert \mathcal R_\Theta P^\pi_{Q,[0,T]})
=D(\pi\Vert\pi^\Theta)+T\sigma_\Theta.
\tag{1}
\]

No parity-invariance assumption was used. With `pi != pi^Theta`, omitting the first term in (1) is incorrect.

For the conventional additive physical entropy, use the system boundary
`log pi(X_0)/pi(X_T)` and the conditional path ratio against the same generator evaluated on the physical reversed trajectory. The difference between that functional and the stationary path log-likelihood ratio is
`log pi(X_T)/pi(Theta X_T)`. Its stationary expectation is `D(pi || pi^Theta)`. Thus the mean additive entropy is `T sigma_Theta`, while the full stationary path KL is (1). Equivalently, substituting

\[
r_{xy}=\frac{\pi_{\Theta y}}{\pi_{\Theta x}}
q_{\Theta y,\Theta x}
\]

in the rate formula produces a stationary gradient term whose mean is zero. Physical thermodynamic interpretation still requires the declared reversal and an appropriate local detailed-balance model; (1) is an exact probabilistic identity.

Now consider a channel `c : i -> j` with stationary throughput `a_c`, `m_c` phases, and phase rate `gamma_c`. Its reverse partner `bar(c) : j -> i` has throughput `b_c = a_bar(c)` and the same phase count and phase rate. Let parity swap the channels and reverse phase order, fixing ports. With port mass `w_i`, use entry rate `a_c/w_i`, phase and exit rates `gamma_c`, and stationary phase masses `a_c/gamma_c`.

The parity-reversed adjoint has entry rate `b_c/w_i` and unchanged interior and exit rates. The global port flux-balance constraint makes the port escape rates agree; all hidden escape rates agree by paired clocks. Therefore

\[
\sigma_\Theta
=\sum_c a_c\log\frac{a_c}{a_{\bar c}}
+\sum_{i\ne j}d_{ij}\log\frac{d_{ij}}{d_{ji}},
\tag{2}
\]

when all masses and fluxes use one normalized stationary convention. Each interior rate contribution vanishes. The preparation term is nevertheless generally positive:

\[
D(\pi\Vert\pi^\Theta)
=\sum_c \frac{m_ca_c}{\gamma_c}
\log\frac{a_c}{a_{\bar c}}.
\tag{3}
\]

Ports contribute zero because parity fixes them. Equations (2) and (3) separate sustained entropy per unit time from the asymmetric stationary hidden occupation. They do not eliminate either resource by relabelling it.

For a completed port-to-port excursion, the entry and exit conditional likelihood ratios multiply to
`a_c w_j / (a_bar(c) w_i)`. Adding the physical system boundary `log(w_i/w_j)` yields `log(a_c/a_bar(c))`, exactly the channel contribution. This directly verifies the native snippet convention.

## What the completion proof must establish

The only new theorem candidate is a matching upper construction and a closure statement. A defensible proof should make the following obligations explicit.

1. **Native normalization and clocks.** Use port masses, direct fluxes, total excursion masses and their balance equations. Preserving these preserves observed departure rates. Exact total hidden mean is an additional constraint, not a consequence of unweighted L1 convergence.
2. **Paired kernels.** For each common duration component `b`, use the same duration kernel for `i -> j` and `j -> i`, with separate coefficients. The microscopic rate is the discrete component KL. This is the useful parity mechanism.
3. **An actual weighted-L1 density approximation.** Point masses at histogram centers approximated by excessively narrow Erlang kernels can leave spikes and gaps; weak convergence alone is insufficient. A conventional route is common-rate Erlangization, where bin width is `1/lambda` and the `k`th bin uses shape `k+1`. Its width is larger than the mesh while both tend to zero. Truncate the weighted tail carefully. A common dilation tending to one can repair total mean without disturbing masses, pairing, or component entropy.
4. **Entropy convergence, not continuity by assertion.** Histogram KL increases to the record KL under a suitable refining common partition. Smoothing cannot increase this component KL. If the smoothed kernels converge in the stated topology, lower semicontinuity supplies the opposite limiting inequality. This sandwich is the proper way to establish entropy convergence, including the infinite-entropy case.
5. **What is free in the model class.** Hidden dimension, phase rates and the choice of hidden physical parity vary with accuracy. The result gives an infimum over that class. It does not assert exact finite realization, bounded hidden clocks, finite-sample acquisition of an arbitrary density, or a manufactured physical device.

The lower bound remains ordinary data processing at the correctly defined native record. The strongest equally informed unrestricted method is therefore direct evaluation or estimation of the event-law relative entropy. The prospective theorem would certify its completeness for the declared realization class, rather than provide a faster numerical estimator. Actual structural restrictions can strengthen it and must be retained when present.

## Retrieval scope and unresolved points

The source check was intentionally limited to the closest hidden-model optimization, Markovian-event, semi-Markov consistency and phase-approximation papers. No primary passage proving the proposed arbitrary-parity matching completion was found. No comprehensive novelty claim is justified by this search.

A PMC request for the 2024 PNAS paper *General theory for localizing the where and when of entropy production meets single-molecule experiments* encountered an access interstitial; no claim here relies on that inaccessible text. A 2026 large-deviation paper surfaced, but its abstract concerned empirical semi-Markov fluctuations rather than completion, and no theorem from it is used. No physical observations, preparations or device operations were performed for this review.

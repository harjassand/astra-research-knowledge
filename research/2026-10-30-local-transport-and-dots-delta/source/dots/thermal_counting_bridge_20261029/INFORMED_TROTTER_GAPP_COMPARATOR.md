# Equally informed Trotter/GapP comparator using the SAME counting premise

2026-10-29. Focused primary-source comparison by the thermal-proof worker. This note does not independently audit the adaptive-cap sparsifier constants; that is assigned separately. It does not establish historical priority of the final combined consequence.

## Verdict

**No advantage over an equally informed standard Trotter/GapP approach equipped with the same new fixed-width counting algorithm has been demonstrated.** The thermal and signed-counting parts of the current construction can be reconstructed by combining established quantitative machinery, with careful representation/precision bookkeeping. The new counting theorem is an imported premise shared by both approaches, not a contribution of this reduction.

This is compatible with the combined conditional consequence being worthwhile to state and verify. It is not evidence that the consequence was previously published verbatim. The useful contribution presently supported is an explicit, audited, parameter-preserving composition, including where naive reductions lose the subexponential-in-volume claim.

## 1. What the directly read primary Trotter paper does and does not say

**Childs, Su, Tran, Wiebe, Zhu, _A Theory of Trotter Error_, arXiv:1912.08854v3 (enhanced version of PRX 11, 011020, 2021).**

https://arxiv.org/pdf/1912.08854

Relevant locations: Theorem 8 and Appendix A Eqs. (169)–(170); Theorem 11, Eq. (54); Section 4.3, Lemma 14 and Eqs. (104)–(105); Appendix E, Eq. (221) and its following bound.

The paper supplies exact additive, exponentiated, and multiplicative error representations. Its displayed general imaginary-time estimate contains `exp(2 t Upsilon sum_gamma ||H_gamma||)`. Its local-Hamiltonian commutator analysis already exploits support growth and induced/local norm. **The displayed general theorem alone does not give our volume-uniform step count:** keeping that extensive exponential bounded normally takes step size of order `1/L`. Merely citing commutator scaling while dropping the exponential would be incorrect. However, a knowledgeable comparator is allowed to specialize the exact representation using local imaginary-time estimates, rather than remain trapped by this generic bound.

## 2. Established local-strength ingredient resolves that specialization

**Kuwahara, Mori, Saito, _Floquet-Magnus Theory and Generic Transient Dynamics in Periodically Driven Many-Body Quantum Systems_, arXiv:1508.05797v3 (2016), Appendix B, Lemma 3, Eq. (B2), specialization Eq. (B6).**

https://arxiv.org/pdf/1508.05797

The lemma treats distinct few-body generators with their individual local-strength bounds. For a k-site operator, its nested-commutator bound supplies a factor `p!` times the pth power of the local energy scale. Applied to a colored, piecewise-constant pulse sequence, Dyson simplex integration cancels this factorial. This is exactly the governing ingredient of `PHYSICS_LOCAL_STRENGTH_THEOREM.md`; it is not newly discovered here.

**Arad, Kuwahara, Landau, _Connecting global and local energy distributions in quantum spin models on a lattice_, arXiv:1406.3898v3, Lemma 3.1 and proof, is related direct imaginary-time precedent.**

https://arxiv.org/pdf/1406.3898

That lemma controls short imaginary-time conjugation through local strength and support, not raw volume. Its conventions differ from ours, so our explicit constants are proved rather than silently quoted from it.

### Explicit synthesis, not a claimed verbatim published theorem

For layer maxima `J_j`, define `K=k sum_j J_j`, and total term norm `L=sum_e ||h_e||`. The standard coefficient bound followed by the Hermitian-even-part estimate, singular-value Gronwall, and operator-monotone logarithm yields

\[
\|\log P(\delta)+\delta H\|
\le\frac{2LK^2\delta^3}{3(1-K^2\delta^2)}.
\]

These final algebraic steps are written out in our proof. They are a transparent specialization/composition of known methods, not evidence of a new locality principle. Their correctness matters: an extensive additive norm bound or an unjustified BCH truncation would not replace them.

## 3. Signed path sums and tensor expectations are established counting machinery

**Fortnow and Rogers, _Complexity Limitations on Quantum Computation_, arXiv:cs/9811023, Section 2.4, Theorem 2.2; Section 3, Lemma 3.2 and proof.**

https://arxiv.org/pdf/cs/9811023

Theorem 2.2 gives GapP closure under exponential sums and polynomial products. Lemma 3.2 clears rational transition denominators and represents path sums by GapP functions. Its formal statement concerns quantum Turing machines, not our nonunitary tensor network; applying the same integer-path-sum mechanism here is an explicit extension of the proof technique, not a literal application of the quantum-machine theorem.

**Schuch, Wolf, Verstraete, Cirac, _The computational complexity of PEPS_, arXiv:quant-ph/0611050v2 (PRL 98, 140506, 2007), Section IV.**

https://arxiv.org/pdf/quant-ph/0611050

Section IV covers normalization, unnormalized and normalized expectations, and general complex tensor contraction through counting. Its path-integral argument explicitly handles signed contributions; positivity of individual tensor entries is unnecessary. The paper does not provide our precise linear-size, bit-budgeted 3-CNF resource theorem. That size accounting must still be checked, rather than inferred from generic polynomial-time reducibility.

### Parameter-preserving implementation available to the same informed comparator

For `G` bounded-locality gates with `B`-bit Gaussian-integer numerators, use local wire segments, magnitude selectors, a phase accumulator, and a Boolean comparison circuit. This needs `O_k(G B+n)` Boolean variables/gates. Deterministic ancillas have unique extensions under standard gate-to-3-CNF encoding. Two counts recover the real signed sum exactly. This is a resource-aware implementation of the established GapP approach; it does not eliminate cancellation by approximation or require stoquasticity.

Generic statements such as “the contraction is in GapP” only promise polynomial overhead, which is insufficient to transfer a `2^{o(N)}` algorithm to `2^{o(n)}`. The linear-in-gates-and-bits accounting is therefore important, but no separation from a comparator allowed the same routine encoding has been demonstrated.

## 4. Rational rounding and resources of the informed comparator

The comparator can round each positive local exponential to a Hermitian positive dyadic matrix `G_e`, then define `h'_e=-(2/delta)logG_e`. The standard integral formula for the operator logarithm bounds `||h'_e-h_e||` locally. Summing those local perturbations controls free-energy density. This avoids demanding gate error `1/n` merely because there are many gates. It is a useful precision arrangement, but no independent priority claim for this arrangement is established here.

With fixed bounded graph degree and fixed density accuracy, `r,B=O(1)`, hence `G,N=O(n)`. Both the current construction and this informed baseline then obtain the same conditional sparse-counting runtime.

For the **same separately verified adaptive sparsification output**, with fixed `k,g`, the target density parameter `tau` gives

\[
q=O(n\tau^{-2}),\quad K=O(k^2g),\quad \beta=\Theta(\tau^{-1}),\quad
r=O(\tau^{-3/2}),\quad B=O(\log(2/\tau)).
\]

Therefore both approaches have

\[
G=O(n\tau^{-7/2}),\qquad
N=O(n\tau^{-7/2}\log(2/\tau)),\qquad \#\text{clauses}=O(N).
\]

Equipped with the same imported sparse-#3SAT runtime `2^{O(N/sqrt(log N))}`, both obtain, for `tau=(log n)^{-a}` up to rounding,

\[
2^{O\left(n(\log n)^{(7a-1)/2}\log\log n\right)},
\]

which is subexponential in `n` for `a<1/7`. For bounded graph degree without the sparsification cost, the same bookkeeping instead has `N=O(n tau^{-3/2} log(2/tau))`, hence the corresponding sufficient range `a<1/3`.

The dense bounded-local-strength consequence depends on obtaining the sparse approximant with the required `cJ_s` and perturbation bounds. This note does not claim that an existing paper states the adaptive cap verbatim or that a fixed, coarser cap suffices. The separate cap proof must be credited as an explicitly checked resource arrangement atop standard sampling/concentration ideas.

## 5. Witness and measurement-access consequences do not create a separation

Once `P>0` is explicitly represented, `sigma=P^r/Tr(P^r)` is a valid mixed state. Counting local insertions gives exact rational expectations under the rounded representation. An energy evaluated on a valid state is automatically an upper bound on the ground energy, independently of whether a randomized sparsification event succeeded.

If `A=-(r/beta)logP` satisfies `||A-H||<=n tau`, the ordinary Gibbs variational/entropy bound gives

\[
\operatorname{Tr}(H\sigma)-E_0(H)
\le2n\tau+n\log d/\beta.
\]

Thus the same informed counting comparator also obtains the current variational witness guarantee. Positive conditional probabilities obtained from local/projective insertions can be sampled sequentially by exact-rational Bernoulli routines. This remains classical expected-time access to specified product-measurement statistics, not physical preparation, trace-distance approximation to a ground state, or generic efficient Gibbs sampling. None of these witness consequences establishes an advantage over the same counting-enabled baseline.

## Recommended claim boundary

Safe: **“An explicit quantitative reduction from bounded-local-strength quantum energy-density approximation and associated variational-state queries to sparse exact counting, with audited precision and size, yields the stated conditional runtime.”**

Not supported: a new sign-problem solution independent of exact counting; a new fundamental imaginary-time locality theorem; a demonstrated advance over equally informed Trotter/GapP methods supplied the same counting premise; or established historical novelty of the full composition.

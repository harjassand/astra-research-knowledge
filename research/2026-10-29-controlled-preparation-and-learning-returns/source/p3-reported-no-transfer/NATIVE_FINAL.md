**I obtained a stronger construction and a matching quantitative principle: negativity and relative likelihood jointly control the attainable entropy advantage.** The construction maintains a fixed gap after **10% local signal depolarization**, at every positive negativity budget. The accompanying bound explains why that gap disappears when the hypotheses’ relative likelihood is bounded.

The proofs and constructions are complete as local working results; they have not received independent review.

## 1. A mechanism that preserves the gap

I reused the completed qubit measurement pair and changed the hypothesis construction. The first hypothesis is now a **faithful product state**; the vacuum-coupled state enters the second argument of relative entropy.

Then I give the two preparations different probabilities of occupying an orthogonal reference branch:
\[
\alpha_a=a\alpha\oplus(1-a)\tau,\qquad
\beta_w=w\beta\oplus(1-w)\tau.
\]

For the comparison gap
\[
\Delta(\rho,\sigma)
=D(P\rho\Vert P\sigma)-D(Q\rho\Vert Q\sigma),
\]
with the reference retained, this gives
\[
\Delta(\alpha_a,\beta_w)=a\,\Delta(\alpha,\beta),
\qquad
\mathcal N(\alpha_a)=0,\qquad
\mathcal N(\beta_w)=w\,\mathcal N(\beta).
\]

The classical divergence between the flag probabilities appears equally in both measurement comparisons and cancels. **The gap is weighted by \(a\); the negativity is weighted by \(w\).**

With \(a=3/4\), the explicit construction after 10% local signal noise has the rigorously enclosed gap
\[
0.002512352
<
\Delta
<
0.002512353
\quad\text{nats},
\]
so it exceeds \(1/500\) nat independently of \(w\).

For every \(\nu>0\), choosing \(0<w\le 2\nu\) meets the negativity budget. The states remain faithful on a **qubit signal and five-dimensional reference**. Choosing \(w\le1/k\) also gives every specified finite level of ordinary reference extendibility. A dense extension still has matrix order \(2\cdot5^k\).

Both signal marginals agree; **the reference marginals differ**. Both preparations undergo the same local noise channel. The earlier equal-reference witness loses its reversal at this 10% noise level, so its scope has not been silently enlarged.

This construction requires separate control of the two hypothesis preparations. A common channel acting on an unknown input preserves its existing relative-likelihood bound and cannot create the arbitrarily large flag ratio \(a/w\).

## 2. A general bound, independent of reference size

Suppose the measurement or channel pair is ordered on all PPT input pairs. Bound the hypotheses’ relative likelihood by
\[
\kappa^{-1}\sigma\preceq\rho\preceq\kappa\sigma,
\]
and suppose each negativity is at most \(\nu\). I derived
\[
\boxed{\;
\Delta(\rho,\sigma)\le 2d\nu\,h(\kappa),
\qquad
h(\kappa)=
\min\!\left\{
\kappa-1+\log\kappa,\,
\frac{2(\kappa-1)^2}{\kappa+1}
\right\},
\;}
\]
where \(d\) is the signal dimension. **The reference dimension does not appear.**

The central operation is one common positive correction:
\[
C=d\,\Pi_A\!\left[(\rho^{T_A})_-+(\sigma^{T_A})_-\right].
\]
Here \(\Pi_A\) removes off-diagonal signal blocks. Adding \(C\) to both hypotheses and renormalizing makes both PPT, at correction trace at most \(2d\nu\). A logarithm-remainder estimate bounds how much relative entropy this common addition can remove.

This also produces a physical obstruction: one common **separable-state replacement channel**, with replacement probability at most
\[
\frac{2d\nu}{1+2d\nu},
\]
makes both hypotheses PPT. Thus a small-negativity advantage cannot survive *every* preparation-noise direction of that strength. The specified local signal noise has a different contract.

Equal reference marginals plus fixed local depolarization supply a dimension-independent \(\kappa\). Under that contract, the advantage must vanish linearly with \(\nu\). A separate noisy equal-marginal family achieves a positive constant times \(\nu\), showing that the linear dependence cannot uniformly be improved to \(o(\nu)\).

### Matching joint dependence

For the fixed qubit measurement pair at 10% local noise, let \(G(\nu,\kappa)\) be the largest gap over all finite references satisfying those budgets. For \(0<\nu\le1/4\) and \(\kappa\ge8000\), the construction and upper bound give
\[
\frac{\min\{1,\nu\kappa\}}{1\,200\,000}
\;\le\;
G(\nu,\kappa)
\;\le\;
8\min\{1,\nu\kappa\}.
\]

The constants are conservative. The substantive result is the **matching dependence on \(\nu\kappa\)**: an expanding likelihood range can compensate for decreasing negativity. The lower construction needs only reference dimension five; the upper bound allows arbitrary finite references. This scaling statement is restricted to the displayed parameter range.

## 3. The fixed entropy gap has a real acquisition cost

Replacing the denominator’s rare active component by a product state changes the entire preparation by trace distance at most \(w\) and removes the gap.

Distinguishing those two preparation models with success at least \(2/3\), even using collective quantum measurements, requires
\[
n\ge \frac{1}{3w}
\]
supplied copies. Because \(w\) can be arbitrarily small beneath any fixed positive negativity cap, that cap and local noise alone provide **no uniform finite-copy verification guarantee** for this fixed-gap promise.

There is an additional exact distinction: for sufficiently small \(w\), the optimal equal-prior single-copy discrimination test uses only the flag and has **identical success probability for both measurements**, despite their fixed relative-entropy gap.

The construction therefore pays for its advantage through reference likelihood, preparation precision, and verification time. A fixed global white-noise floor closes this particular escape route and restores a vanishing-gap bound.

## Proofs and checks

The finite constructions passed **36 exact rational matrix and logarithm-interval checks**. The general bounds have analytic proofs.

- :chatgpt-content-reference{index="2"}[COMMON_REPAIR_AND_ASYMMETRIC_FLAGS.tex](producer-workspace/COMMON_REPAIR_AND_ASYMMETRIC_FLAGS.tex)
- :chatgpt-content-reference{index="3"}[noise_resource_checks.py](producer-workspace/noise_resource_checks.py) and :chatgpt-content-reference{index="4"}[noise_resource_results.json](producer-workspace/noise_resource_results.json). The script reuses the preserved rational backend.

The foundations remain conventional operator concavity, relative entropy, and entanglement robustness. I checked the existing robustness framework and close work on common replacement and information fragility; historical priority for the present combination remains unresolved. :chatgpt-content-reference{index="0"}

The previous assets remain intact. N972 and N677 are credited as inherited machinery; N675 and its accepted dependencies remain accepted without reopening validation. **General fixed-gap decision or hardness results remain open, and the existing no-cutoff deduction remains SLD-specific.** The advance here is a quantitative account of which additional statistical and preparation resources are needed to turn a small-negativity entropy advantage into reliable inference.

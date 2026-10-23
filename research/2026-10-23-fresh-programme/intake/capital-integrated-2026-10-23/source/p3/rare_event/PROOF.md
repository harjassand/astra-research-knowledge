# Product-innovation relative-moment certificate

Research collaborator: `/root/rare_event_primitive`, fresh Astra P3, 23 October 2026.

## Status

The statement below is proved directly. It is a tensorization of a classical
scalar Kantorovich-type moment inequality. It is **not claimed historically new**.
It supplies a potentially useful verification interface for the parent branch's
forced-survival / Feynman–Kac computation. It does not itself invent an importance
sampler or establish a practical speedup over conditional Monte Carlo.

The Astra corpus was entered through `00_START_HERE.txt` at revision
`e606bfc587c76bdcae8b8fa3ec33e721efa2fbac`. Selective reads included dossiers
N486–N493 and the complete indexed BN research-note proof range
`frontier/proof_ranges/2185aeb7b8dabaac5b26910c.txt` (source hash
`3724e9edad63df08248b0f7f01b7eed95ac188ed12a30a1a281eb38012f46b69`).
The literal old source path `updates/BN/package/RESEARCH_NOTE.md` returned 404;
the indexed proof-range route resolved. No inherited theorem is required below.

## 1. Operational interface

Let `U_1,...,U_n` be independent innovations with known product law. Let
`W=f(U_1,...,U_n)>0` be an evaluable weight. We want its mean `p=E W` with
relative error. The weight may have a known very small multiplicative scale,
which does not affect the following certificate.

Assume verified constants `c_i>=0` such that, for every coordinate `i` and
every pair of inputs differing only at that coordinate,

    |log f(u)-log f(u')| <= c_i.

Essential suprema suffice, with the usual product-measure interpretation.
The certificate does not contain `p`, the committor, or statewise continuation
probabilities. It does require proof of the global coordinate influence bounds.
Checking those by enumerating all inputs would reintroduce the original problem;
the useful route is a compact analytic bound from the simulator's structure.

## 2. Sharp theorem

Define

    K = product_i cosh(c_i/2)^2.

Then

    E W^2 / (E W)^2 <= K <= exp((1/4) sum_i c_i^2).

Consequently `Var(W)/p^2 <= K-1`.

### Scalar lemma

For a positive random variable `l<=Z<=u`,

    E Z^2 / (E Z)^2 <= (l+u)^2/(4lu).

Proof: `(Z-l)(Z-u)<=0` implies
`E Z^2 <= (l+u)m-lu`, where `m=E Z`. Dividing by `m^2` and maximizing over
`m in [l,u]` gives the maximum at `m=2lu/(l+u)` and value
`(l+u)^2/(4lu)`. For `u/l=e^c` this is `cosh(c/2)^2`.
Equality is attained by `P(Z=u)=l/(l+u)` and `P(Z=l)=u/(l+u)`.

### Tensorization proof

Condition on all coordinates except `U_n`. The scalar lemma gives

    E_n f^2 <= K_n (E_n f)^2.

Set `g=E_n f`. Integration over `U_n` preserves every other coordinate ratio
bound: if inputs to `g` differ only in coordinate `i<n`, then
`g(u)<=e^(c_i) g(u')` and conversely. Independence is what lets the same
conditional integration measure be used for the two values.
Inductively,

    E f^2 <= K_n E g^2 <= product_i K_i (E f)^2.

Finally `log cosh x <= x^2/2`, proved by differentiating and using
`tanh x <= x` for `x>=0`, yields the exponential bound.

### Sharpness

Choose independent Bernoulli variables with

    P(U_i=1)=1/(1+exp(c_i)),
    W=product_i exp(c_i U_i).

Each scalar inequality is exact and the product attains `K`. Hence no uniformly
smaller bound can be valid using only the numbers `c_i` and independence. For
small `c_i`, `log K=(1/4)sum c_i^2+O(sum c_i^4)`, so the coefficient `1/4` is
also asymptotically optimal for this information contract.

The sharpness example is an exactly soluble validation case, not evidence of
algorithmic superiority; its mean factorizes analytically.

## 3. Obtaining influences from a contractive simulator

Suppose

    X_t = Phi_t(X_(t-1), U_t),
    log W = constant + sum_(t=1)^H g_t(X_t),

where `Phi_t` is `rho_t`-Lipschitz in state under a fixed norm, `g_t` is
`lambda_t`-Lipschitz in that same norm, and changing only `U_i` at a fixed
previous state changes `Phi_i` by at most `d_i`.

A common-randomness coupling gives

    c_i = d_i sum_(t=i)^H lambda_t product_(k=i+1)^t rho_k.

This follows by induction on the propagated state perturbation and summing
the resulting changes in the log weight. No distributional mixing theorem or
committor is needed. If `rho_t<=rho<1`, `lambda_t<=lambda`, and `d_i<=d`, then

    c_i <= d lambda/(1-rho),
    log K <= H d^2 lambda^2 / (4(1-rho)^2).

This is a sufficient bound. Sharper componentwise Jacobian or sparse influence
propagation can be substituted when verified.

**Scope:** fixed nonzero heterogeneity does not give uniform-in-H sample cost.
The worst-case bound still grows exponentially in `H lambda^2/(1-rho)^2`.
Rarity can be arbitrarily severe through the known constant scale without
altering `K`; the fluctuation/influence budget remains the decisive quantity.

## 4. Probability interpretation

For a model that must survive H stages, let `a_t(X_t) in (0,1]` be the known
probability of surviving stage t, and let the `X_t` trajectory have its known
survival-conditional dynamics driven by independent innovations. Force
survival in the simulator and return

    W = product_t a_t(X_t).

Then `E W` is the original full-survival probability by conditioning. The
representation itself is established conditional Monte Carlo / Feynman–Kac
normalizing-constant estimation. The proposed additional operation is a
verified relative-moment certificate computed from the log-weight influences.

This does not cover an arbitrary rare terminal event: a hard terminal
indicator gives zero weights and can make the log influences infinite.
One must either acquire a success-preserving proposal or use another argument.
Physical-time rates, model calibration, and measured acquisition cost remain
separate obligations.

## 5. Finite-sample inference and precision

For relative tolerance epsilon and certified relative variance `v=K-1`, take
`n=max(1,ceil(4v/epsilon^2))` independent weights per group. Each group mean
has relative error exceeding epsilon with probability at most 1/4 by
Chebyshev. Taking the median of an odd number J of independent group means
gives failure probability at most

    sum_(j=(J+1)/2)^J binom(J,j) (1/4)^j (3/4)^(J-j).

This is the already-established median-of-means argument also used by BN.
The resulting sample requirement is `O((1+v/epsilon^2)log(1/alpha))`.
All simulator calls and certificate acquisition must be charged.

Very small weights must be handled with a known scale or log arithmetic.
Floating-point evaluation is not automatically a formal confidence guarantee.
If every computed weight obeys a proved uniform multiplicative enclosure
`exp(-delta)W <= W_hat <= exp(delta)W`, then every positive sample mean and
median obeys the same enclosure. Combine that deterministic error with the
statistical interval. Without such an enclosure, label the implementation
floating and the statistical theorem exact-model only.

## 6. Exact counterexample if innovations are correlated

Let all `U_i=B` for one Bernoulli variable, set `r>1`, and `W=r^(sum_i U_i)`.
As a function on the full cube, the coordinate log oscillations are `log r`.
Choose `P(B=1)=1/(1+r^n)`. The true relative second moment is

    (1+r^n)^2/(4r^n),

whereas incorrectly treating the inputs as independent predicts

    ((1+r)^2/(4r))^n.

The first can be exponentially larger. The independent-innovation
representation and its influence proof therefore must be audited, particularly
when a persistent latent environment is reused across many simulated times.

## 7. Baselines and claim boundary

Required equal-information controls include the same conditional Monte Carlo
estimator without certification, randomized quasi-Monte Carlo, antithetic
paths when symmetry exists, and a particle/Feynman–Kac normalizing-constant
estimator. Deterministic dynamic programming or quadrature should be used
where the effective state is small. The certified estimator cannot claim
new variance reduction relative to identical conditional Monte Carlo.

Pointwise deterministic probability envelopes may be exponentially wider
than a small influence budget suggests: `sum c_i` can scale like sqrt(H)
while `sum c_i^2=O(1)`. That contrasts two information summaries, but does
not alone prove lower bounds against all equally informed deterministic or
randomized algorithms.

## 8. Closest sources checked

- Blanchet, Glynn, Leder (2012), *On Lyapunov Inequalities and Subsolutions
  for Efficient Importance Sampling*: DOI 10.1145/2331140.2331141;
  author page https://web.stanford.edu/~glynn/papers/2012/BlanchetGLeder12.html.
  Establishes the mature Lyapunov/subsolution context; abstract inspected.
- Hartmann, Joester, Schuette, Sikorski, Weber (2026), *Importance sampling of
  unbounded random stopping times: computing committor functions and exit rates
  without reweighting*, https://arxiv.org/abs/2601.01489. Abstract inspected;
  unbounded stopping-time issue is already explicitly studied.
- Cesar and Rogers, *Bounding, Concentrating, and Truncating: Unifying Privacy
  Loss Composition for Data Analytics*, https://arxiv.org/abs/2004.07223v3.
  Its bounded-range-to-concentrated-divergence result is a close mathematical
  predecessor to the exponential `sum c_i^2/4` bound at order two.
- Dong, Durfee, Rogers, *Optimal Differential Privacy Composition for
  Exponential Mechanisms and the Cost of Adaptivity*,
  https://arxiv.org/abs/1909.13830v2. Abstract inspected; bounded-range
  composition is established machinery.
- Rogers and Steinke's author exposition, 12 July 2021,
  https://differentialprivacy.org/exponential-mechanism-bounded-range/,
  Theorem 5 and proof were inspected. It explicitly proves eta-bounded-range
  implies eta^2/8 concentrated DP, hence order-two divergence at most eta^2/4.
  This warns against claiming the basic exponential bound as new.
- Harrison and Manurangsi, *Exact zCDP Characterizations for Fundamental
  Differentially Private Mechanisms*, https://arxiv.org/abs/2510.25746v1.
  Abstract inspected; contains tight bounded-range characterizations.
  HTML retrieval failed and its precise theorem was not inspected.

Literature coverage is selective. Historical novelty of this precise
tensorized statement/application remains UNKNOWN.

## 9. Parked alternative: abstract-state Bellman certificates

An earlier candidate used pointwise enclosures of aggregate transition vectors
on a small partition, then robust reachability and second-moment Bellman
inequalities. This would remove concrete-state enumeration conditional on
cheap analytic envelopes, but overlaps established formal abstraction and
robust MDP methods. Worse, its reachability brackets can already answer the
probability task. It was deprioritized in favor of the innovation certificate,
which does not contain a continuation-probability table.


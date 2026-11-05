# IID canonical-witness estimation for a specified QEC graph model

Status: implemented, exact small-instance audit passed, useful finite-size regime observed. Independent matched-baseline and scaling audits are included. They establish limits but not a strongest-method speedup. This is not a general polynomial-time simulator, a new decoder, or a hardware-reliability certificate.

## 1. Explicit acquired interface

Input is a finite unweighted decoding graph. Internal vertices carry parity checks; left and right rough-boundary vertices are leaves and unchecked. An independent Bernoulli(p) fault sits on each graph edge, with rational0<p<=1/2. The target decoder deterministically returns a minimum-cardinality edge set C with the observed internal syndrome. A failure means odd parity of E XOR C on the left-boundary cut.

The standard unrotated planar surface-code instance has distance d in the modeled Z direction, N=2d^2-2d+1 physical edges, and d(d-1) internal checks. Only independent Z noise and ideal checks are modeled. No calibration data or quantum device is needed or claimed.

A second implemented graph stacks T layers, adds independent time-like syndrome-error edges between adjacent layers, and leaves the spatial rough boundaries at every time. This is T data-error rounds with T-1 noisy syndrome observations and perfect initial/final syndrome closure. It is a phenomenological noise model, not circuit depolarizing noise. Correlated/hyperedge faults, a joint X/Z failure target, arbitrary nonminimum-weight decoders, and hardware data require separate derivations.

The implementation uses the already installed PyMatching library with unit weights and physical-edge fault IDs. Its minimum-weight contract is an explicit software assumption. Independent checks compare its outputs to exhaustive/alternative exact optimization on finite instances. No reserved evaluation data was opened.

## 2. Canonical fault-rich witness

Let R=E XOR C(E). Internal degrees of R are even. Odd left-cut parity implies R contains a simple left-to-right path. Fix a deterministic selector, implemented as breadth-first search with fixed source/edge ordering, and call its selected path w(E).

For any such path P, C XOR P has the same internal syndrome. Minimum weight gives

|C| <= |C XOR P| = |C|+|P|-2|C intersect P|.

Because P lies in E XOR C, the E and C indicators on P are complementary. Therefore at least ceil(|P|/2) edges of P are faulty. This is a cover of every decoder failure, not an assumption that arbitrary fault-rich paths necessarily cause failure.

## 3. Implicit walk envelope and exact IID trial

For length l, let c_l count all oriented nonbacktracking walks from the left leaves to the right leaves, terminating on arrival. Vertices may repeat in this proposal cover. Let

t_l = Pr[Binomial(l,p) >= ceil(l/2)].

For a finite length cap M, define Z_M=sum_(l<=M)c_l t_l. Directed-edge dynamic programming counts c_l and samples a walk of any specified length exactly. It neither lists all walks nor assumes they are self-avoiding.

One trial:

1. Draw length l with probability c_l t_l/Z_M and a uniform such nonbacktracking walk P.
2. If P repeats a vertex, reject.
3. Otherwise draw independent edge noise conditioned on at least ceil(l/2) faults on P. Draw its fault count by the exact truncated-binomial law, choose a uniform subset of that size, and draw all other edge faults independently.
4. Decode. Reject if there is no failure or P is not exactly w(E). Otherwise output Y=1.

For each valid simple P, its joint proposal with a compatible error E has mass

(t_l/Z_M) * (Pr_p(E)/t_l) = Pr_p(E)/Z_M.

Exactly one path survives the canonical-selector test for any failure whose selected path has length<=M. Thus

Pr[Y=1] = Pr_p[failure and |w(E)|<=M]/Z_M.

The Y trials are iid Bernoulli under independent ideal random bits. No conditioned Markov chain, mixing claim, failure-oracle approximation, or witness-multiplicity count is used.

This canonical-cover acceptance identity is established importance-sampling machinery, not a new invention here. Karp–Luby–Madras1989 provides the general cover-weighted unique-representative construction: https://www.math.cmu.edu/~af1p/Teaching/MCC17/Papers/KLM.pdf . Laumanns–Zenklusen's path-reliability estimator is a particularly close implicit-path predecessor: https://arxiv.org/abs/0707.3231 . The candidate specialized join is the complete MWPM residual-path cover, nonbacktracking implicit envelope, and controlled long-witness remainder for this QEC target.

## 4. Exact long-witness remainder

Let S be the number of left boundary leaves, and let Delta be the maximum internal degree. Each leaf has one outgoing edge. Then c_l <= S(Delta-1)^(l-1).

For0<p<=1/2, Chernoff gives t_l <= r^l with r=2sqrt(p(1-p)). Any rational upper bound rbar>=r with eta=(Delta-1)rbar<1 yields

B_M = [S/(Delta-1)] eta^(M+1)/(1-eta).

By the witness cover and a union bound,

Z_M theta <= P_failure <= Z_M theta+B_M,

where theta=Pr[Y=1]. If M is at least the number of internal vertices plus1, every possible simple witness is included and the remainder is exactly zero, without a small-p convergence assumption.

The program constructs rbar by an integer square-root comparison on a fixed rational grid and evaluates B_M as a Fraction. The old prototype lacked an explicit p<=1/2 domain guard; the guard is now present. The reported p=.001 runs were in domain throughout.

## 5. Arithmetic and confidence

For p=a/b, every t_l has integer numerator A_l and denominator b^l. Length weights use the common denominator b^M, so they are integers c_l A_l b^(M-l). All categorical draws use exact integer rejection, as do truncated-binomial counts and uniform subsets.

The optimized ordinary-noise step takes uniform16-bit words, rejects values at or above floor(65536/b)*b, and reduces the surviving words modulo b. Comparing residues with a gives exact Bernoulli(a/b) coins under uniform independent source bits. The seeded Python PRNG is a reproducibility implementation, not proof of ideal randomness.

A fixed number n of proposals gives a binomial count X. The two-sided Clopper-Pearson interval uses alpha=.001. Its endpoints are rounded outward to a20-bit dyadic grid using exact integer comparisons of binomial CDF numerators with alpha/2. The final endpoints are exact rational Z_M times those bounds, with B_M added to the upper endpoint. Printed decimal intervals are summaries; exact fractions are stored.

This controls sampling uncertainty and the explicit length remainder within the stated model. It does not validate the physical noise assumptions or remove the trusted-library/ideal-randomness assumptions. Multiple separately reported99.9% intervals do not automatically form a99.9% joint assertion; use a union bound or a new allocation if combining them.

## 6. Cost and limitations

Directed-edge DP stores O(M|E|) integers. Counts have O(M log(Delta)) bits; probability numerators also pay O(M log b) bits. Arithmetic cost is not unit-cost when these integers become large. A trial uses one sampled walk, independent graph-edge coins, one decoder call, and one graph search. Actual wall time includes setup, all rejected proposals, and exact confidence calculations.

Efficiency is governed by Z_M/P_failure, not the tiny absolute failure rate alone. No uniform inverse-polynomial acceptance claim is made. An independent serial-diamond graph gives an exponentially bad family even at small fixed p. Its modeled Z-logical path length grows, while its dual distance stays2; it is a valid obstruction to a general graph theorem, not yet a theorem about the usual square surface-code family.

The ordinary2D screen at p=.001 found acceptance31.9%,31.2%,24.4%,19.6%,11.0% for d=5,9,17,25,41 with1000 proposals each. These are exploratory acceptance/time diagnostics, not confidence-certified rate estimates. They do not prove asymptotic polynomial scaling or behavior near threshold.

## 7. Strong comparison required

- Bravyi–Vargo2013 splitting and Bennett-ratio simulation already reach rare logical-error regimes: https://arxiv.org/abs/1308.6270 .
- Mayer et al. circuit-level splitting already report rates below1e-20, while identifying confidence/convergence limitations: https://arxiv.org/abs/2509.13678 . The present model is less general; a numerical rate below1e-20 is not itself an advantage.
- Haruna et al.2026 locally balanced single-flip/cluster-exchange MCMC is the current same-code-capacity comparator: https://arxiv.org/abs/2610.35498 . Its pinned source was inspected, and an independent implementation of the published kernel/BAR mathematics was tested on the matched input. The upstream package was not executed, so no upstream runtime claim is made.
- Fail Fast provides QEC-specific min-weight logical/restriction sampling and exact onset counts, plus multi-seeded splitting: https://arxiv.org/abs/2511.15177 , especially Section4.3. Those are essential prior art, although a lowest-weight coefficient or an extrapolation is not the same as the full finite-p failure probability with an explicit remainder.
- Generic fault-weight stratification and uniform global-noise tilting are useful but insufficient sole baselines.

The potentially useful distinction is complete finite-p IID confidence from a tractable implicit witness cover in a measured practical regime. No novelty, speed superiority over the strongest matched code, or civilization-changing consequence is claimed before that comparison and audit conclude.

# Independent review: full thermal clock weights at fixed couplings

29 October 2026. **ACCEPTED at the classical full-weight/acquisition/sampling scope stated below.** This is an independent analytic reconstruction, not a second implementation or a finite-clock replay. The exact reviewed inputs are copied and hashed in `REVIEW_INPUTS.json`. The main input is `FULL_THERMAL_WEIGHTS.md`, SHA256 `9a34fd8cb580b08f9bd727266232a8663606911dcede215e27b97d61037064cf`.

The earlier positive clock initializer, its rational-coin/streaming supplement, and the supplied KT and cylinder estimates are retained at their accepted scopes. I checked the cylinder construction and the new use of its estimates, rather than inferring a spatial-support bound from the old syndrome-incidence bound. I found no mathematical obstruction to this new classical bridge. The conditional preparation of the FULL noncommuting clock Gibbs state is a separate operation under B's review; this note does not accept it by composition.

## 1. Exact target and fixed parameters

Write

`H(eta,S)=sum_i Q_i + lambda sum_e eta_e V_e(S)`.

There are `m` clocks of fixed dimension `L`, each native hopping label has support at most `q`, and at most `d_hop` native labels touch any clock. Syndrome signs remain free commuting involutions until final evaluation. Every symbol in a hopping term is carried by a clock in its native support. The prefix-gauge construction supplies these facts; an arbitrary weakly interacting Hamiltonian is not admitted here.

At fixed `lambda>0`, `Delta=1/(4 lambda^L)`, and `beta=4 ln B0`, the required classical energy is

`F_beta(S)=-beta^(-1) log Tr_clock exp[-beta Delta H(1,S)]`.

This trace includes every clock level. Replacing it by `Delta E(S)` would in general give the wrong marginal at fixed couplings as `m` grows. The present proof retains the full trace and uses its ground energy only to bound its connected corrections. All geometric, KT, cooling, and weighted-cylinder gates must hold for the chosen fixed parameters. No practical values of those constants have been acquired.

Use distinct names for `d_hop` and the degree of the enlarged history graph. The former pays `|A|<=d_hop |B_A|`; the latter pays connected-set enumeration and polymer mixing. Taking a fixed maximum of them is harmless, but substituting a graph degree for native label incidence without justification is not.

## 2. Why the weighted cylinder estimate really retains amplitudes

At a fixed slab length `delta in [delta0,2 delta0]`, the exact-label Dyson expansion lives in the commutative coefficient algebra

`l1(N^E) tensor l1(Z2^checks)`.

For a prescribed native-label multiplicity `(n_e)`, time interleavings and the time-simplex factorial give the absolute majorant `product_e a_e^(n_e)/n_e!`, with `a_e=delta |lambda| exp(2q delta)`. This statement is before evaluation of the amplitude variables and before merging check parities. Summing positive multiplicities therefore proves the same slab bound in the enlarged algebra. Evaluation of amplitudes, restriction to an amplitude support, and projection to a parity are contractions of its coefficient l1 norm. Products have norm at most the product of norms.

The frozen bad-spacetime-set convention explicitly includes ALL native clock cells of every active label, even if a particular matrix element leaves a spectator clock in its vacuum. Consequently a label present in a cluster has its full native support in that cluster's spatial projection. This detail pays the later containment `B_A subset B_C`; retaining only actually excited cells would not do so.

Set `A_h=2+ln(1/h)`. The ordinary rooted KP bound applied with activity weight `exp(A_h |B|)` gives

`sum_(C containing x) ||Phi_C||_l1 exp(A_h mass(C)) <= Bstar`.

The additional label algebra costs no hidden local-basis factor: the positive Dyson majorant already sums its unmerged coefficients. Intermediate activity matrices need not be Hermitian, and signed/complex scalar clusters are never sampled as positive quantum states.

## 3. Coefficient-wise pressure identification and the order of limits

Fix FINITE `m`, the chosen slab `delta`, and real amplitudes in an open box about zero contained in the KT/KP domain. For every assignment of the free signs, the finite-clock Hamiltonian is Hermitian and its KT ground state remains simple. The infinite-time line pressure is an absolutely convergent analytic series in the amplitudes, as is the KT energy.

For this fixed spatial system, take cylinders with `M'` time layers and the SAME slab `delta`. The temporal lifting argument cancels every logarithmic cluster of mass `<M'/2`; the remaining absolute sum divided by `M'` tends to zero. The elementary finite-dimensional spectral limit then gives

`p_infinity(eta,S)=-delta E(eta,S)`

on the real amplitude box for each sign assignment. Character inversion in the finite free-sign algebra and the multivariate analytic identity theorem give equality of the unmerged amplitude/parity coefficients. Absolute convergence extends the equality to the physical amplitude evaluation `eta_e=1`. Equivalently one may choose a strictly smaller coupling gate to put that evaluation inside the analytic domain.

This fixes `m` FIRST. It neither exchanges the spatial and zero-temperature limits nor assumes convergence of a merely formal pressure. The estimates are uniform in `m` only after this finite-system identification. The physical cylinder uses `M=floor(beta Delta/delta0)` and `delta=beta Delta/M`; the auxiliary sequence used to identify its line pressure is permitted to keep this particular `delta` fixed.

For the cylinder-minus-line remainder, every surviving cluster has mass at least `M/2`. If `B_C` is its connected spatial projection, then

`h^(-|B_C|) <= exp[(A_h-2) mass(C)]`.

The two unspent exponential units give `exp[-2 mass(C)]<=exp(-M)`. There are `M` possible cylinder time roots for a fixed spatial clock and at most the same `M` times a line-orbit root bound. Thus the new weighted estimate is exactly

`sup_i sum_(thermal terms rooted spatially at i) ||coefficient||_l1 h^(-|B_C|) <= 2 M Bstar exp(-M)`.

An orbit may be counted by more than one time-zero root; this is an upper bound, so overcounting is safe. Small clusters have no winding and no nontrivial temporal stabilizer; their exact cancellation uses the full multi-polymer mass and the inherited ordered-tuple/Ursell convention.

For complex intermediate coefficients, take the REAL PART OF EACH COEFFICIENT after the analytic construction. That contracts the absolute norm and preserves the real physical function. Taking the pointwise real part as a function of complex amplitudes is not the analytic operation being used.

## 4. Connected hopping increments and the global tail

For any retained connected hop set `A`, use the COMMON finite clock set `B_A=union_(e in A) supp(e)` when evaluating every `F_C`, `C subset A`. Keep the onsite penalties of all clocks in `B_A`, including those unused by a particular subset `C`. The remaining clocks give a known sign-independent free-clock factor. This convention makes factorization literal; dropping different outside factors in different subset evaluations would require tracking their scalar cancellation instead.

In an absolutely convergent amplitude series, Boolean inclusion-exclusion

`eta_A^F = sum_(C subset A) (-1)^(|A|-|C|) F_C`

keeps precisely those monomials whose set of DISTINCT hopping labels is `A`. If `A` has disconnected overlap components, the restricted Hamiltonian is a sum on disjoint clock factors, its full trace is a product, and its log is additive as a function of the signs. The mixed increment is zero even if some formal signs are shared between factors.

For connected `A`, its declared support `B_A` is connected and contains every associated parity variable. Each coefficient inherited from a thermal cluster has `B_A subset B_C`. Replacing the cluster support by this smaller declared support only lowers its `h` weight. Grouping coefficients within this same `A` cannot increase l1. Merging equal parities across different distant declarations is not used.

After subtracting the ACTUAL nominal order-`L` monomials, the ground estimate plus the thermal estimate therefore give

`sup_i sum_(b: i in B_b) |r_b| h^(-|B_b|) <= Gamma`

with

`Gamma=C_h lambda + (2 M Bstar/beta) exp(-M)`.

All native labels of `A` touch `B_A`, so `|A|<=d_hop |B_A|`. Omitting `|A|>K` leaves only `|B_A|>K/d_hop`, and hence

`sup_S |F_beta(S)-F_beta,K(S)-scalar| <= m Gamma h^(K/d_hop)`.

This is an absolute GLOBAL energy error. Choose `K>=L` for consistency with the inherited leading-term subtraction and then `K=O(log(m/epsilon))`. No time-orbit evaluation or infinite-volume pressure value appears in that acquisition algorithm.

The full and truncated normalized classical laws have l1 distance at most `2 beta e_K` by the ordinary Gibbs interpolation bound. Their scalar offsets cancel from normalization. Free-sign expansions remain valid after restricting to the physically admissible syndrome set and its redundant check relations.

## 5. Finite full-trace acquisition needs no spectral separation

See `FULL_TRACE_ACQUISITION.md` for the explicit algorithm and an optional rational parameter prescription. There are `m C^K` connected sets, `2^K` subsets and at most `2^(qK)` formal sign evaluations per set. Each local matrix has dimension `D<=L^(qK)` and rational Hermitian entries for dyadic `lambda`; its norm is at most `qK+|lambda|K`.

Exact rational inertia brackets the ENTIRE ordered eigenvalue multiset to a chosen common absolute width. Degenerate eigenvalues can share intervals. A complex-to-real embedding repeats every eigenvalue twice, and its multiplicity counts must be halved correctly. Neither minimum spacing between levels nor a full-clock gap is needed for this full-trace task.

For matched eigenvalues differing by at most `eta`, the two log traces differ by at most `t eta`. Thus the free energies differ by at most `Delta eta`. Subtracting a lowest-eigenvalue interval and computing a bounded log-sum-exp is stable. Terms below a certified cutoff may be enclosed by their total multiplicity times the largest omitted exponential. Large `t` increases the required bit precision only logarithmically; it does not require a Taylor sum of length `t`.

Allocating each local free-energy evaluation accuracy `epsilon/[poly(m) exp(O(K))]` pays every subset sum, Fourier sum, retained bond and subsequent rounding. Because `K=O(log(m/epsilon))`, matrix dimension, number of evaluations, and bit precision give polynomial work in `m,1/epsilon`, with fixed, potentially prohibitive exponents and parameter constants. This is an analytic algorithm, not an executed all-family compiler.

## 6. What follows and what does not

With `Gamma<=1/(16 beta)`, `v_b=exp(2 beta |r_b|)-1<=4 beta |r_b|` gives the same positive-bond activity gate as in the already reviewed growing-penalty initializer. Downward rational rounding and charging unresolved-sign omissions preserve it. Its exact-coverage activities, common denominator, streamed connected-set enumeration, rational categorical coins, count-metric mixing, and one total timeout cap are unchanged. The acquired classical law is now the CORRECT full Gibbs syndrome marginal at FIXED couplings.

This is a meaningful improvement over conditioning onto all clock ground fibers: that older approximation has an extensive thermal-population debt at fixed penalty. The new bridge removes that debt from the classical marginal and supplies its coefficients without an infinite-time oracle. The contour/KP and hard-core-polymer methods remain established ordinary tools; no generic algorithmic or historical novelty follows from this review.

A full noncommuting Gibbs initializer additionally needs a separate uniform-cost operation preparing the conditional full clock state for the CLASSICAL syndrome supplied by this sampler. A classical marginal alone does not prepare that state. No claim is accepted here about B's still-separate operation, microscopic Davies noise, constant-precision physical couplings, noisy gates, autonomous initialization, useful thresholds, practical advantage, or a general low-temperature quantum Gibbs algorithm.

**Review outcome:** the full-weight expansion, fixed-parameter admission, global truncation, and expected polynomial classical bit-cost bridge are accepted at these exact supplied-model scopes. The combined quantum initializer must retain the independent conditional-state-preparation gate.

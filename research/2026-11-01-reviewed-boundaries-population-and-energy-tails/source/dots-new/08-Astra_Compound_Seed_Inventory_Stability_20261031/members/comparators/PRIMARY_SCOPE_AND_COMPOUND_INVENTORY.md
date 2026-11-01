# One-port conservative four-species network: primary scope and exact obstructions

Status: independent mathematical comparator note, 31 October 2026. This is **not a proof of recurrence** for the non-complex-balanced fixture, and not an exhaustive novelty determination. Earlier accepted packages are unchanged.

## 1. Useful result first

For the raw reversible network

```
0 <-> A;
A+B <-> C+D;
2A <-> C+D;
A+C <-> C+D;
A+D <-> C+D,
```

no actually inspected general theorem below directly supplies positive recurrence or all stationary exponential moments at the fixture with every rate one except `C+D -> A+C`, whose rate is two. Some potentially relevant older full texts are inaccessible under the standing access restrictions, so this is a **bounded scope result**, not a claim that the network or family is new.

The compound inventory `R=A+min(C,D)` has internally invariant **positivity**, not a conserved numerical value. It identifies the true internally inactive face `R=0`. Nevertheless the first-core up-event probability is bounded away from zero along an explicit large-count sequence, even starting with `A=1`. Thus the earlier common-seed single-core `O(1/N)` argument does not transfer. Moreover **every positive normlike one-step geometric-Foster candidate depending only on `(A,N)` fails**, including nonseparable candidates. This representation obstruction holds even at a complex-balanced parameter point and therefore is not itself evidence of a recurrence novelty.

## 2. Task-first source ledger and comparison limits

The existing local source ledgers were read first: `stochastic_boundary_construction_20261031/SOURCE_SCOPE.md`, `stochastic_boundary_continuation_delivery_20261031/PRIOR_SOURCE_SCOPE.md`, `stochastic_adaptive_mass_20261031/SOURCE_SCOPE.md`, and the continuation `COMPARISON_AND_SCOPE.md`. They preserve prior governing Astra repository retrieval at revision `51ce47ce39f976517d60e2f87bbe280b651f6056`; its restricted constructions are not a general weak-reversibility theorem.

### Actually accessible primary statements inspected in this pass

* **Anderson–Cappelletti–Kim, JAP (2020)**: the publisher abstract states a binary, single-linkage theorem with a pure multiple of every species among the complexes, proved using an n-step embedded chain. Here the full graph has two linkage classes and lacks pure B, C, D complexes. Only the abstract, not the full proof, was inspected. [Primary publisher abstract](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/stochastically-modeled-weakly-reversible-reaction-networks-with-a-single-linkage-class/5E9F7DAE999525F8D4A3392F80B3F0C9).

* **Agazzi–Laurence, Bulk stability (2026)**: the actual full HTML concerns planar/two-species systems. Theorem 4.1 establishes stopped bulk drift; Corollary 4.3 requires additional compatible boundary estimates for recurrence. It neither supplies a four-species theorem nor closes the inactive faces here. [Primary full text](https://arxiv.org/html/2610.31550v1).

* **Chuang Xu, Exponential ergodicity of first order endotactic stochastic reaction systems (2026)**: actual Section 4, condition SUB and Theorem 4.1 require a first-order endotactic subsystem, a strictly negative positive-weight linear drift, a sublinear residual, and a common closed communicating class. The only first-order subsystem here is `0 <-> A`, which fixes B,C,D; its communicating classes are not the full irreducible class. Independently, the pure-B ray rules out the resulting positive linear Foster inequality, as proved below. This excludes that theorem's stated route, not every higher-order method. [Primary full text](https://arxiv.org/html/2601.00176v1).

* **Laurence–Robert, Scaling Methods for Stochastic Chemical Reaction Networks**, actual v3 full text: Theorem 3 gives an ordinary random-stopping Foster criterion: one must acquire an integrable stopping time and negative expected energy change relative to its expected duration. Their triangular recurrence example in Section 3/Proposition 7 is two-species, not a theorem for this four-species fixture. This is a strong conventional comparator for future multiscale work, but the stopping rule and drift remain work to be done. [Primary full text](https://arxiv.org/html/2310.01949v3).

* **Anderson–Cappelletti–Fan–Kim, New path method (2025)**: the accessible publisher abstract presents a spectral-gap method for an already ergodic CTMC, including complex-balanced and additional examples. It does not automatically provide the missing recurrence premise for this non-complex-balanced fixture. Full theorem hypotheses were not inspected. [Primary publisher abstract](https://epubs.siam.org/doi/10.1137/24M1665933).

* **Anderson–Kim (2018), Some network conditions**: the actual arXiv abstract confirms binary tier-based criteria, but does not state enough hypotheses to decide every relevant theorem. The historically denied Wisconsin full text was not fetched or bypassed. [Primary abstract](https://arxiv.org/abs/1710.11263).

* **Anderson–Cappelletti–Kim–Nguyen (2020), Tier structure**: the actual arXiv abstract reports stochastic recurrence results for a subclass of strongly endotactic systems, and explicitly separates the deterministic and stochastic implications. The present full graph is not strongly endotactic by the total-count normal below. A complete exclusion of every theorem in that paper would require its actual hypotheses, not only this abstract. [Primary abstract](https://arxiv.org/abs/1808.05328).

### Prior inspected result, current unavailable attempt

Kriebel's *Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks*, v1.2.4 (August 2026), was previously inspected and reconstructed in this branch. Its full single-linkage scope does not directly cover this two-linkage open network. Stability of the finite conserved internal fibers does not alone imply stability after opening the port. The [author-hosted source](https://aleckriebel.com/research/positive-recurrence-bimolecular-reaction-networks/paper-v1.2.4.pdf) was unavailable via the tool on this pass; no retry or alternate transfer was attempted. This paragraph relies on the recorded prior inspection, not a new full-text fetch.

The ConStRAINeD two-species weak-reversibility result remains an in-preparation announcement with no inspected manuscript, and is not a four-species certificate.

### Access limitations, not silently resolved

The AIMS HTML attempt for Anderson–Kim's 2023 mixing-time paper timed out (400); it was not retried or replaced by a PDF transfer. A guessed arXiv HTML version for the path-method paper returned 404 and was not retried at another version. Previously denied/gated Wisconsin, ScienceDirect, PMC/Hoessly, eScholarship429 and DOI-failed targets were not fetched. Search results automatically displayed some double-full/all-outflow snippets, but those are **not substituted for inspected complete theorems**. They therefore do not support an exhaustive prior-art exclusion. In particular, do not report “no existing theorem applies” without this qualification.

## 3. Raw architecture and complex balance

The seven complexes are `0,A,AB,CD,2A,AC,AD`. The full graph has two linkage classes, the internal stoichiometric span has rank three, and adding the port gives full rank four. Hence deficiency is `7-2-4=1`. The binary internals conserve total count `N`, and their common support intersection is empty.

For `w=(1,1,1,1)`, all maximal source complexes are binary and every reaction from them has zero w-increment. Yet w is not orthogonal to the full stoichiometric space, because of `0 -> A`. The required strict inward reaction at a maximal source is absent. Thus the full graph is not strongly endotactic.

For each `X in {B,C,D}` the reversible enabled path

```
0 -> A -> 2A -> C+D -> A+X -> X
```

uses only the displayed network. Translation by arbitrary nonnegative surplus preserves enabling. Concatenating these paths and the direct A path shows that every lattice state communicates with zero: the full state space is one closed irreducible class.

At the fixture rates, complex balance would force concentrations `(a,b,c,d)>0` to satisfy `a=1` from the core, `ab=cd` from leaf AB, `a^2=cd` from leaf 2A, `ac=2cd` from leaf AC, and `ad=cd` from leaf AD. Thus `c=1`, `d=1/2`, but also `cd=1`, a contradiction. At the all-unit-rate point, `(1,1,1,1)` is detailed balanced; the ordinary product-Poisson construction already establishes stability and all exponential moments there.

At pure B counts, a positive linear function `v·x` has generator `lambda v_A>0`. The corresponding positive exponential-linear function also has strictly positive quotient. These basic Foster templates cannot establish a geometric drift on this irreducible class.

## 4. Compound positivity, not a common-seed time change

Put `R=A+min(C,D)`. Its internal increments are

| Channel | Delta R |
|---|---:|
| AB -> CD | 0 |
| CD -> AB | 0 |
| 2A -> CD | -1 |
| CD -> 2A | +1 |
| AC -> CD | -1 + 1_(D<C) |
| AD -> CD | -1 + 1_(C<D) |
| CD -> AC | 1 - 1_(D<=C) |
| CD -> AD | 1 - 1_(C<=D) |

Only three forward channels can decrease R. For `2A -> CD`, enabling already gives `R>=2`. If `AC -> CD` is enabled at `R=1`, necessarily `A=1,C>=1,D=0`, making its increment zero; the AD case is symmetric. Thus **no internal reaction sends R>=1 to R=0**.

`R=0` exactly means `A=0` with either C=0 or D=0. All internals are then disabled. If `R>0` and `N>=2`, at least one internal reaction is enabled. The sole small exception is the state A=1,N=1. Consequently A=0 itself is not the inactive face: CD-bearing states can move internally. Time change by R produces death hazard `mu A/R`, not a constant independent exponential clock. Any use of the old common-A theorem would need a genuinely new argument.

## 5. Exact first-core obstruction

At `(A,B,C,D)=(0,n,1,1)`, the four CD departures have total rate 5, independently of n. Immigration is rate lambda. Therefore

`P(first event is immigration) = lambda/(lambda+5)`.

This event is included in a first-core up event, so the latter cannot be uniformly `O(1/N)`. Starting instead at `(1,n,0,0)`, the AB forward reaction has rate `alpha n`, while the core competition is lambda+mu. It reaches `(0,n-1,1,1)`. Hence

`p_up >= alpha n/(alpha n+lambda+mu) * lambda/(lambda+5)`.

For the fixture this converges to `1/6`. The lower bound also rules out a bare first-core `t^N` contraction at sufficiently large t, since its expected ratio is at least `t p_up`. This does **not** imply transience or absence of exponential stationary moments; it diagnoses the wrong sampling scale.

## 6. Aggregate (A,N) one-step geometric Foster no-go

This argument holds for every positive choice of rates on the displayed graph. Let alpha be the AB->CD rate. Suppose a positive normlike function `V(x)=F(A,N)` satisfies a global inequality

`LV <= -epsilon V + C`, with `C>=0`.

A finite-exception geometric Foster inequality implies such an inequality after increasing C. Reducing epsilon if needed, assume `0<epsilon<min(lambda,lambda+mu)`. Write

`u_n=F(0,n)`, `v_n=F(1,n)`, `rho=1-epsilon/lambda in (0,1)`.

At `(0,n-1,0,0)`, only immigration acts, so

`v_n <= rho u_(n-1) + C/lambda`.  (1)

At `(1,n-1,0,0)`, the only internal channel is AB->CD, of rate `alpha(n-1)`, and its destination has A=0,N=n. Discarding the positive core destination terms yields

`LV >= alpha(n-1)u_n - [alpha(n-1)+lambda+mu]v_n`.

Combining with the asserted upper bound gives

`u_n <= [1+(lambda+mu-epsilon)/(alpha(n-1))]v_n + C/[alpha(n-1)]`.  (2)

The product of the bracket in (2) with rho tends to rho<1. Equations (1)-(2) thus imply, for all large n, `u_n <= rho' u_(n-1)+M` for fixed rho'<1 and finite M. Iteration bounds u_n, contradicting normlikeness along the pure-B ray. All comparison states belong to the same closed class by Section 3.

This excludes arbitrary nonseparable positive normlike F(A,N), not only separable `t^N H(A)`. It excludes neither joint-composition corrections, random/sampled-time drift, additive alternative criteria, nor product-form arguments. In particular, it holds at the already solved complex-balanced all-unit-rate point.

## 7. Additional radial-template warning

For the same fixture family let `a` be the rate of `2A -> CD`. If `2a(t-1)>lambda`, no positive normlike `t^N g_R` can have physical one-step geometric Foster drift. The large pure-B states at R=0 force `g_0>t g_1`; the A=1 states then force `g_2<g_1/t`. At A=2 with large B, AB->CD leaves R fixed, core death has nonnegative g-contribution, and after discarding the positive immigration destination,

`LV/t^N >= 2a(g_1-g_2)-lambda g_2 > [2a(1-1/t)-lambda/t]g_1 > 0`.

This proves the claimed obstruction without addressing a vanishing composition-dependent corrector. It gives no verdict on the separate still-editing inventory/corrector construction.

## 8. Evidence scope

`exact_comparator_checks.py` and its JSON output independently verify finite raw graph/rank/paths, rational rate relations, exact inventory increments over a finite grid, and the first-core lower bounds. The ordinary proofs above, not the finite tests, establish the infinite-ray obstructions and inventory invariance. No simulation, stationary-fiber oracle, infinite-tail numerical inference, remote write, or upload was used.

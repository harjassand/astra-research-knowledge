# Independent review: bounded-oscillation killed fibers and the homogeneous family

2026-10-30. Reviewer: `producer-workspace/review_chemical_global_foster`.

## Verdict

**PASS for the root conditional lemma and the author's corrected V2 homogeneous-family application.** For every sufficiently large conserved population N, the stated hypotheses genuinely give uniform clearing survival

`sup_x P_x(tau_clear>t) <= M exp(-lambda N^(m-1)t)`

and mean clearing time `O(N^(1-m))`, without mixing, stationary averaging, or irreducibility of the conservative state chain. The application earns its all-face boundary premise from actual stochastic mass-action rates, including zero and disabled coordinates.

The initial application's small-N wording required correction: a shell with some active states can also contain an inactive nonclearing class. The author accepted the explicit counterexample below and saved a separate V2. The root subsequently added catalyst/scope clarifications; those additions were reread and are included in the pinned input below. The earlier whole-network receipt was not changed.

This is **not** a full-process recurrence theorem or novelty clearance. The killed-semigroup implication and the upgrade from a uniform mean hitting-time bound to an exponential tail are ordinary machinery. The substantive application-specific work is the uniform all-face drift and its bounded shell oscillation. No conclusion about interior mixing follows.

## Exact reviewed inputs

The following byte-identical input copies are retained under `inputs/` in this receipt directory; their original locations are recorded here.

| Input | SHA-256 |
|---|---|
| `producer-workspace/BOUNDED_OSCILLATION_KILLED_FIBER_LEMMA.md` | `54c99591bb09060d38fdc215ff7a544bf1eb1f525edbaf91f4e0df70448dd0dd` |
| `producer-workspace/UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME_V2.md` | `bf2dfd46e12d16bb6f18ab2f8471c152a9243f08b5bcd57e9e3fb670fd60339a` |
| Same live directory, `HOMOGENEOUS_FAST_BOUNDARY_LIMIT.md` | `35f2b30f25403a2a9a4854fa386215a468924b6fec5e5bd96831c4a91db5078d` |
| `producer-workspace/FRACTIONAL_FACTORIAL_BULK.md` | `439964f8c9c5fa3dd8cc0c6166b450b52a4b51519476ad35e168d2d3ff11b1ba` |

The initial application `UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME.md`, SHA-256 `e69b10c97b53a7d98d2219c0adce38957a6ee5640a60c8db22a69da5b491cd04`, is retained separately as history, not as the corrected small-N statement.

The earlier whole-network review remains at `producer-workspace/INDEPENDENT_WHOLE_PROOF_REVIEW.md`, SHA-256 `7bd2ab1c58495998f58149663e38c11af89d9abfe3ba17e1c0f5d18f914ed8b9`. I rechecked that hash; this new review neither replaces nor enlarges its network scope.

## 1. Root conditional lemma: complete proof and conventions

Fix N>=1 above the hypothesis threshold. Q_N is a conservative finite-state jump generator acting on column functions by

`Q_N f(x)=sum_y q_N(x,y)[f(y)-f(x)]`.

All rates are finite. Let k_N(x)>=0 be the total rate of the actual event at which the process is stopped. The killed generator on the surviving fiber is
`K_N=Q_N-diag(k_N)`; the test function is assigned value zero at the cemetery. This convention is essential: the killing contribution is `-k_N f`, not merely a subtraction from the running cost.

For a positive V_N, the termwise inequality `log u<=u-1` gives

`Q_N log V_N <= Q_N V_N/V_N`.

Subtracting a shell-dependent constant does not change Q_N log V_N because Q_N1=0. Set

```
W_N=log V_N-min_x log V_N,
f_N=1+W_N/N,
M=1+C_0.
```

Then `1<=f_N<=M`. Outside C_N, assumptions 2 and k_N>=0 imply

`K_N f_N <= -c_0 N^(m-1)`.

Inside C_N, assumptions 3 and 4 imply

`K_N f_N <= C_1 N^(m-1)-c_1 N^m`.

For N>=`max(1,2 max(C_1,0)/c_1)`, the latter is at most `-(c_1/2)N^m`, hence at most `-(c_1/2)N^(m-1)`. Consequently, with

`lambda=min(c_0,c_1/2)/M>0`,

one has the **multiplicative** inequality

`K_N f_N <= -lambda N^(m-1) f_N`

throughout the fiber. Thus the source's additive negative estimate does indeed imply the claimed multiplicative estimate; no unmentioned lower bound on f_N is being used in the wrong direction.

Let `T_t=exp(tK_N)`, a positive substochastic semigroup. Since

`d/dt [exp(lambda N^(m-1)t) T_t f_N]
 =exp(lambda N^(m-1)t) T_t (K_N+lambda N^(m-1)I)f_N <=0`,

we get `T_t f_N<=exp(-lambda N^(m-1)t)f_N`. Positivity and `1<=f_N` then give

```
P_x(tau_clear>t)=T_t1(x)
 <=T_tf_N(x)
 <=M exp(-lambda N^(m-1)t).
```

Integration proves `sup_x E_x tau_clear<=M/[lambda N^(m-1)]`. Finite state and finite rates justify the semigroup and differentiations directly. Conservative irreducibility is nowhere needed. Indeed the proved strict killed inequality itself excludes a closed nonclearing class at these N.

### Catalyst and control conventions

If a **fixed positive** factor a_B multiplies both Q_N and k_N, its killed generator is a_B K_N, so replace t by a_B t. The mean bound is divided by a_B. For a_B=0, survival is one and the displayed bound with zero exponent is only vacuous; there is no finite-mean conclusion. For `(B)_q` with nonnegative integer B and fixed integer q>=1, positivity means B>=q. The q=0 convention gives factor one.

B must remain fixed before the event being studied, or the conclusion must instead be expressed through an operational clock or a positive lower bound on the varying factor. Immigration, activation, changing-N transitions, or changing-B transitions cannot be silently placed inside this conservative Q_N.

If the same f_N and constants work for every allowed instantaneous row in a bounded coefficient family, the corresponding exponential supermartingale proves the same estimate for predictable/adapted time-dependent choices. Fixed-N rates are then uniformly bounded, so there is no switching explosion. No stationary policy, invariant distribution, or optimizer is needed. This is a survival statement, not a stationary recurrence assertion for a nonhomogeneous process.

## 2. Factorial oscillation and interior upper bound

For `V_N=exp(sum_i b_i x_i) product_i(x_i!)^alpha` with `sum_i x_i=N`, write

`log V_N=alpha log N! -alpha log multinomial(N;x)+sum_i b_i x_i`.

The multinomial coefficient lies in `[1,d^N]`; the linear term lies between `N min_i b_i` and `N max_i b_i`. Therefore

`osc(log V_N)<=N[alpha log d+max_i b_i-min_i b_i]`.

The additive `alpha log N!`, of size N log N, cancels on a fixed fiber. Bounding absolute log V_N instead would introduce an avoidable logarithmic loss. The convention `0!=1` makes V_N positive at every boundary state.

On an interior region `x_i>=epsilon N`, every bounded conservative reaction increment nu satisfies

`log V_N(x+nu)-log V_N(x)=sum_i b_i nu_i +alpha sum_i nu_i log N+O(1)=O(1)`.

Here finite-product factorial formulas make the error uniform once N is large compared with the fixed increments and 1/epsilon; `sum_i nu_i=0` cancels log N. If all source orders are at most m and coefficients are uniformly bounded, the total rate is O(N^m), giving `|Q_N log V_N|<=C N^m` on that interior. This verifies the root lemma's assumption 3 for the stated chemical family. The author's weaker global `CN^m log(N+1)` estimate is also correct and sufficient for its own proof, but not necessary on the interior.

## 3. The actual homogeneous family earns all-face negativity

The reviewed family has k>=2 species, one fixed finite strongly connected graph of composition complexes, every source and target of total order m>=2, every pure complex mX_i present, and positive rate constants. Killing is `c(A)_m`, c>0. These are substantial structural restrictions, not consequences of general weak reversibility.

### 3.1 Uniform stochastic boundary limit

For fixed nonnegative integers a,b, define for integer n>=0

```
h_ab(n)=(n)_a [(n+b-a)!/n!]^alpha  if n>=a,
h_ab(n)=0                          otherwise.
```

When a=b=0 the factor is exactly one. Otherwise `p=(1-alpha)a+alpha b>0`. Fixed-shift factorial estimates give `h_ab(n)=n^p[1+O(1/n)]` for large n. On `0<=n<=N`, the large-n error is bounded by `C max(1,N^(p-1))`, and the bounded-n remainder is O(1). Thus

`sup_(0<=n<=N) |N^-p h_ab(n)-(n/N)^p|<=C N^-min(p,1)`.

Disabled sources n<a are included: n is then bounded and the comparison monomial is O(N^-p). Invalid factorials are never evaluated on that branch.

For a conservative reaction y->y', the exponents sum to m. Every normalized coordinate factor is uniformly bounded, so expanding a finite product proves that its actual factorial gain, divided by N^m, converges uniformly over all integer compositions to
`t^((1-alpha)y+alpha y')`, with t=x/N. The loss converges uniformly to t^y. Therefore

`L_N V_N/(N^m V_N) -> E_alpha(t)
 =sum_e k_e[t^((1-alpha)y+alpha y')-t^y]`

uniformly on the entire discrete simplex, including zero, bounded, and disabled coordinates. A fixed compact positive coefficient box preserves the same uniform estimate.

### 3.2 The source graph on a face is genuinely killed

At a boundary point t, let U consist of complexes supported on the positive coordinates of t. U is nonempty because it contains a pure complex for a positive coordinate, and proper because a missing coordinate's pure complex is absent. If a source lies outside U, both its limiting gain and loss vanish because 0<alpha<1. If a source lies in U but its target does not, its gain vanishes and its loss is negative. The remaining expression is exactly the killed finite-complex energy on U.

Strong connectivity means every complex of U reaches an edge exiting U; the graph restricted to U therefore satisfies the path-to-killing premise. The finite killed-graph lemma gives one sufficiently small alpha with strict negativity on the closed normalized simplex. There are only finitely many such supports/faces, so one alpha works for all.

For coefficient-box uniformity, the small-alpha contradiction proof also allows a convergent coefficient sequence: positive terms divided by alpha stay bounded uniformly; a support-to-complement edge has a coefficient bounded away from zero and contributes a negative term divided by alpha tending to minus infinity. This proves a uniform small-alpha interval. At fixed admissible alpha, compactness of coefficients and normalized simplex supplies a common strict margin.

The normalization does not vanish on faces. Indeed

`S(t)=sum_y t^y >=sum_i t_i^m >=k^(1-m)>0`.

The author's weaker lower bound k^-m is sufficient. Therefore the normalized killed-energy margin yields an absolute negative bound for E_alpha on the whole simplex boundary. Uniform continuity extends it to `min_i t_i<=epsilon` for some `0<epsilon<1/k`. Uniform stochastic convergence then gives

`L_N V_N/V_N<=-cN^m`

throughout that boundary neighborhood for every sufficiently large N and every coefficient choice in the fixed box. No supported subgraph or boundary cylinder is omitted.

## 4. Interior entrance and clearing

Set

```
U_N=log V_N-alpha log N!+alpha N log k,
K_N^interior={x:min_i x_i>epsilon N}.
```

Then `0<=U_N<=alpha N log k`, and outside the interior, `L_N U_N<=-cN^m`. Stopping the finite chain at its interior entrance and at time T gives

`cN^m E_x(T wedge tau_interior)<=U_N(x)<=alpha N log k`.

Letting T grow proves `sup_x E_x tau_interior<=C N^(1-m)`. This does not assume that the entrance time is finite in advance, nor that the entire conservative shell is irreducible. It proves each large-N conservative class reaches the interior.

On the interior, A>=epsilon N, hence for sufficiently large N,
`c(A)_m>=c' N^m`. Combining the preceding boundary inequality, oscillation bound, and interior upper bound with Section 1 gives the exponential clearing-survival estimate and mean bound uniformly over all compositions. In particular the actual application supplies every structural premise of the root lemma; it is not merely a conditional restatement.

These constants may depend on the fixed graph, species count, order, and coefficient bounds. No effective small-alpha threshold, algorithmic efficiency, or dimension-uniform constant is established. The exponent's formula is valid in arbitrary fixed composition dimension, which is a different claim.

## 5. Small-N correction and explicit counterexample

Take the degree-two graph `2A <-> 2C`, with positive rates, and kill at rate `c(A)_2`. It is strongly connected and contains every pure complex. At N=2, states `(2,0)` and `(0,2)` are active, but `(1,1)` enables neither fast reaction and has zero killing rate. Thus `P_(1,1)(tau_clear>t)=1` and its mean clearing time is infinite. Merely calling that N-shell active is not enough.

The corrected V2 properly restricts the finite-small-N extension to **active states or their components**, meaning states enabling a source complex. From such a state x, choose y<=x. A complex path from y to mA gives the enabled physical path

`x-y+y_0, x-y+y_1, ..., x-y+mA`.

The leftover vector x-y is fixed and nonnegative, so every step is valid. At the final state killing is positive. Every conservative successor of an active state is active, since the target complex is itself a source in the strongly connected graph. Thus the finite active set contains no closed nonclearing class. Standard finite-chain path bounds give finite clearing time from each of its states, uniformly also over a compact positive coefficient box. Constants can be enlarged over the finitely many small-N active states under consideration.

For all `N>k(m-1)`, pigeonhole guarantees at least one coordinate is >=m, so a pure source is enabled at every state. This supplies an explicit activity threshold, though the analytic large-N threshold may be larger. Small-N interior entrance is not automatically included: an active class can clear without ever entering the chosen interior. V2 extends the clearing statement only, as required.

The catalyst correction is also explicit in V2: `(B)_q=0` at B<q gives no finite clearing-time claim. These corrections leave the all-sufficiently-large-N theorem unchanged.

## 6. Ordinary comparator and scope of possible novelty

The implication `Kf<=-lambda f`, `1<=f<=M` -> uniform exponential survival is the elementary positive killed-semigroup/Lyapunov comparison proved in Section 1. No new spectral or mixing theorem is required.

There is also a stronger baseline comparison against overclaiming the tail upgrade: any already-proved uniform mean absorption bound T_N gives an exponential tail of the same order by Markov's inequality and repeated worst-case conditioning. At intervals 2T_N, the conditional chance of surviving another interval is at most 1/2, so

`sup_x P_x(tau>t)<=2 exp[-(log 2)t/(2T_N)]`.

This applies to killing by adjoining the absorbing cemetery and does not need conservative irreducibility. It is explicitly presented, with a slightly sharper continuous-time choice, in [Aldous–Fill, *Reversible Markov Chains and Random Walks on Graphs*, §2.4.3, equation (2.20)](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch2.S4.html). Consequently exponential survival at order N^(m-1) is not a qualitatively new conclusion once a uniform `O(N^(1-m))` mean clearing bound is available. The bounded supersolution supplies a particularly direct common-control certificate and explicit prefactor, not a new general exponentialization principle.

What this review actually verifies is the construction of that uniform mean/survival scale from actual all-face mass-action drift and O(N) entropy oscillation for the stated homogeneous strongly connected pure-complex family. Whether this exact structural combination is already known is **unverified**. Deterministic permanence, general recurrence, and the old pointwise Green-kernel failures are not silently imported or altered.

The `N^-9/4` special-chain clearing estimate in the earlier three-species proof remains sharper than this generic cubic `N^-2` bound. This review does not replace load-bearing tail summations in any whole-process proof: competing births, changes of N/B, residual threshold defects, and global boundary matching still require their own actual stopped-process estimates.

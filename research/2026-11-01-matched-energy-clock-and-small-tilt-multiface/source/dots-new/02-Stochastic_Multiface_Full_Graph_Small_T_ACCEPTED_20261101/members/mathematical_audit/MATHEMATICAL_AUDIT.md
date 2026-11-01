# Independent adversarial mathematical audit — complete small-tilt multiface theorem

## Verdict and binding

**PASS, scoped to the mathematical theorem.** The complete full-hub-graph construction proves positive recurrence and one acquired nonzero exponential total-count moment for the stated square-free reversible binary one-port architecture with positive rational rates. There is no graph restriction. No substantive mathematical defect or repair was found in the audited proof.

This is **not executable constructor / raw receiver / serialized DAG admission**. No author code is a premise of this verdict. It is not a claim of every prescribed tilt, arbitrary weak reversibility, practical tail constants, historical novelty, or source-process clearance. The prior aggregate and detour acceptances do not establish this theorem; the new inequalities were independently checked.

Two immutable input snapshots are distinguished:

* `THEOREM_INPUT.md`: initial requested theorem, SHA256 `1bb095387e1efe086117f6be61cffe4563d49efbdacb6309be864979aa2284f7`.
* `THEOREM_CONSERVATIVE_DELTA_INPUT.md`: author’s current theorem, SHA256 `dc96226443a99ee0a8541f03cce5af28ff735a95c6855053d223cf87d5001327`.

An exact diff shows **one line changed**: the last-copy threshold uses the explicit lower bound `dA=1/[8(3M+1)^2] <= D_(2M)` instead of the exact rational `D_(2M)`. The new threshold is conservative. Both mathematical statements pass. The delta also avoids expanding `q^(3M)` merely to acquire that threshold, which matters for enormous rate ratios. The original source changed after handoff, not in this audit; the original snapshot remains separately bound. All audit work is local, pure mathematics; no external source retrieval was used.

## 1. Source grouping and every signed resource jump

For an independent set I, every hub is of exactly one of three types: I--Near, Far--Far, or outside I with a Near endpoint. There is no I--I hub. The first two selected types have resource weight `2M+2`; the third is charged, not omitted. Every forward arm with its satellite in I goes from weight `2M` to weight at least `2M+2`, even when that satellite is not an endpoint of the target hub.

At a selected hub, amplification has resource increment `2M-2 >= M`. The only adverse reverse arms have target satellite in I and increment −2. All other reverse arms have nonnegative increment. Since `q^M >= 2` and

`q^2-1 <= 5/(2M),  M >= 12s/b`,

the favorable amplification gap minus every adverse outgoing rate is at least `b/2-5b/24 = 7b/24 > b/4`.

Here is the missing expanded convexity argument, independently derived. For one grouped source put `P(u)=sum k(u^(-Delta)-1)`. Each integer-power term is convex on positive u: its exponent is either nonpositive or at least one. Since `P(1)=0`, convexity puts P below its endpoint chord on `[1,q]`. The gap at q therefore gives `P(u) <= -gap*(u-1)/(q-1)`. Setting `u=1/z` and using `u-1 >= 1-z`, then integrating against `z^(j+M-1)`, yields exactly the stated −g D and −h D terms. This handles all simultaneous outgoing rates; it is not a single-reaction approximation.

For every signed resource jump, `|Delta| <= 4M+4`. The elementary power sum gives

`|z^Delta-1|/(1-z) <= (4M+4) q^(4M+4) < (4M+4) 3^6`

because M≥2 and `(1+1/M)^M<3`. Unselected amplification/arms cost at most `Cstep*(a+kmax) A(U+1)D`. Unselected hub sources cost at most `Cstep*s Qbad D`. These include quadratic forward propensities and unrestricted reverse redistributions.

True death changes J by **−2M**, not by a one-step surrogate. Its positive difference satisfies

`Z_(j-2M)-Z_j <= 2M q^(2M) D_j < 18M D_j`.

The factor `mu A/t` only decreases this bound, and the remaining tilted death baseline is nonpositive. Immigration is bounded using monotonicity, `t Z_(j+2M)-Z_j <= (t-1) Z_j`. Thus inequality (1) is valid for the actual generator, including last-copy death. None of these arguments needs a favorable birth head.

## 2. Uniform profile bounds and subset elimination

The integral representation is exact. Its lower-bound integration interval `[1-1/(j+M+1),1]` really lies in `[1/q,1]`; the integrand’s power is at least 1/4 there. Integration of `(1-z)` gives the displayed `1/[8(j+M+1)^2]`. The upper bound follows by extending the interval to `[0,1]`. Combining `U<=J<=WU` yields (2) without requiring U>0.

For each fixed I, define the large subset only as an analysis partition. It never changes the actual weights or function being differentiated. If it is nonempty, its large coordinate pays `CA A(U+1)D` with one quarter of the arm capture. For a bad hub meeting Near(I_large), choose one adjacent large vertex. Its other endpoint is outside I, so its product is at most `x_v U <= x_i x_v/T`. At most E bad hubs charge any chosen cross hub. This proves the stated quarter-budget, including overlapping hubs.

Every bad hub not charged in that way has both endpoints Far(I_large). If I_large=I, none remain. Otherwise the receiver is a **strictly smaller** independent set J. Its outside count satisfies `U_J+1 <= (B+1)(U_I+1)`, and the independently checked profile bounds imply `D_I <= R D_J`. This is a valid uniform comparison even at wildly separated scales.

If I_large is empty, `N+1 <= (B+1)(U_I+1)`. The entire positive remainder is therefore bounded by the global A and Q terms in (3); no inactive face is thrown away. One may retain −3r_I/4 by discarding only the extra negative quarter.

For each receiving J there are fewer than `2^n` strict supersets; each has `w_I <= w_J/K`. The chosen K makes their aggregate transferred cost at most `w_J r_J/4`. Consequently the global −S/2 inequality follows. It is a sum of fixed smooth count functions, not an invalid maximum/minimum generator rule.

## 3. Constructive activation cover, expanded independently

A concrete prefix algorithm is in `independent_math_checks.py`. Sort positive counts descending and take the prefix preceding the first successive ratio ≤eta; if there is no such gap, take all positive entries. For a list of at most n entries with total L, the prefix minimum is at least `eta^(n-1)L/n`; its omitted mass is at most `n eta` times that minimum.

When A≤gamma N, satellite mass is at least N/2, so the first prefix minimum is at least hh N. An edge inside that prefix supplies the stated two-heavy-endpoint alternative. Otherwise the prefix is independent and its outside mass U is at most `3delta/8` times its minimum, hence at most delta times that minimum.

If activation fails, the combined terms `AF+Qcross` bound the prefix minimum times `A+NearMass`. Thus `A+NearMass < epsC delta U`, and FarMass>U/2. Run the same prefix procedure on Far. Its minimum is at least hh U. An edge inside this new prefix would contribute at least `hh^2 U^2` to Qfar, contradicting failure because epsC<hh². Adding the new prefix therefore preserves independence. The remaining outside count is at most `delta*min_new/4 + epsC*delta*U <= 3delta*min_new/8`. Old prefix coordinates are larger than the new minimum. Each failure adds at least one vertex; after at most n stages the process terminates. Zero coordinates are never an obstacle because the Far total is positive when an enlargement is needed.

For an active face alternative, U cannot be zero: U=0 places all satellite support in an independent set and has A=0, hence Q=0. Integer counts then give U≥1, and (2) gives `S>=min(g,h)*d*epsC/4`. The coefficient w_I≥1 is sufficient. There is no claim that one preselected face works uniformly.

## 4. Small tilt, baseline, and the inactive-state join

All quantities through P, RA, RQ and sstar precede eps. Cbirth also precedes eps. Choosing eps only after these weights gives the genuine uniform bound `eps*Cbirth <= sstar/16`. e, H, and Nstar are acquired subsequently. No head height determines a weight which in turn determines that same head; there is no circular fixed-point choice.

For `B0=1-e A/(N+1)`, exact death changes the angular ratio by `(N+1-A)/[N(N+1)]`. Its positive tilted contribution is at most e mu, including A=1. Its negative baseline is at least `(1-e)D A`. Forward internal channels cost at most `e(2a+kmax)A`; reverse amplifications give `-2eb Q/(N+1)`, and all reverse arms help. Immigration’s angular change is nonpositive. The selected e proves (5), with `e mu <= mu^2 eps/4`.

For Z0={A=0,Q=0}, every internal source is disabled. Every internal target has either positive A or a populated hub, so **no internal transition can enter Z0**. Immigration leaves Z0, and monotonicity of every profile gives exact drift at most `lambda[eps(1+P)-H]=-lambda` there.

The only adverse entrance is a genuine death from A=1 with independent satellite support. For N≥2, the nonempty support itself is an enumerated face: J=2M, F=N−1, and `S >= g(N-1)D_(2M)`. Its weight is at least one. This pays the entire `mu H/t` indicator cost with S/4 at the stated threshold. The conservative dA replacement only strengthens this condition. There are no ignored entrance channels or seed-only excursion arguments.

The remaining Nstar conditions absorb RA into one quarter of the linear A death and RQ into one half of the Q capture. They give (6). The cover then gives either −3sstar/16 or at most −1; inactive states give −lambda. The weaker common nu in (7) is valid. Finite head states, including N=0 or the A-only last-copy event, are intentionally paid by the head constant rather than claimed to satisfy tail drift.

## 5. Global process and head constant

`3/4 <= h <= Htot` makes `Wfun=t^N h` normlike. Dividing the uniform additive negative drift by Htot gives the claimed multiplicative drift. On N<Nstar the total jump rate is bounded by `lambda+mu Nstar+Srate Nstar^2`; destination total count increases by at most one. The given CF also covers `zeta Wfun`, with a conservative extra power of t. No jump or factor of t is missing.

The only upward total-count channel is constant-rate immigration. A Poisson domination makes all finite-time paths stay within a finite random sublevel and gives finite exponential moments, while rates are bounded on each finite sublevel. This yields nonexplosion and legitimizes localized Dynkin/integrating-factor receiving. The moment bound provides tight occupation averages. Irreducibility is independently justified by the reversible singleton path through any actual arm of each satellite, followed by nonnegative translations. The invariant probability is therefore unique and the chain positive recurrent. Fatou applied to occupation averages gives the stated stationary exponential moment.

The proof does not assert that the resulting tilt is useful numerically. In the seven finite audit fixtures, acquired head integers already require 252–848 bits; no `t^(Nstar+1)` or profile at such a head was expanded. A symbolic expression is not a practically evaluated tail bound. Budget refusal must remain UNKNOWN_COMPUTATION in any eventual executable receiver.

## 6. Independent finite evidence and reproduction

`independent_math_checks.py` imports **no author code**. It uses exact integers/Fractions, recomputes the theorem’s constants, constructs actual channels, evaluates actual source/death/birth transitions, implements the selector, and checks hierarchy assignments at the acquired enormous T. It includes triangles, paths, a triangle plus an edge, an isolated satellite, unequal rational rates, and sparse arms (one arm per satellite, including nonincident target hubs). Full proof acceptance rests on the uniform derivations above, not extrapolation from tests.

The canonical results are `INDEPENDENT_CHECKS.json`; measured elapsed time is separate in `CHECK_STDOUT.json`. Reproduce from a copied audit directory with assertions enabled:

```
PYTHONDONTWRITEBYTECODE=1 python independent_math_checks.py
```

The exact result file is deterministic; runtime is not promised identical. The tests intentionally do not attempt actual global-tail pointwise powers at astronomical thresholds. This is a mathematical audit supplement, **not** a raw-network admission API or independent serialized proof receiver. The author’s newly supplied constructor can be reviewed separately against the frozen conservative theorem.

No denied or pending action blocks this mathematical verdict. No frozen theorem was edited by this auditor.

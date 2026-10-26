# ASTRA Pro3 — Ordered-response completion, mixed interventions, and calibration gauges

26 October 2026. Original constructive continuation in the temporary Pro3 role. All exact source-family statements below are conditional on the **declared** observation and regularity interfaces. The mathematics of scalar Lipschitz extensions, finite hyperplane arrangements, and linear programming is classical; the source-to-future-operation compilation is a new implemented combination in this programme. No historical priority, hardware implementation, independent physical regularity acquisition, or superiority over an equally informed retainer is claimed.

## 1. The acquisition problem and the main change of mechanism

Old experiments expose scalar forward readings of `F(t,x)=m x+A(t,x)` at chosen exact inputs and known times. The true residual `A` is **unknown**. The scientific contract supplies rational constants `a,v>=0` and assumes

`|A(t,x)-A(s,y)| <= a*|x-y|+v*|t-s|` for **every** pair of points.

A native reading `Yhat_i` at `(t_i,x_i)` is only warranted to satisfy `|Yhat_i-F(t_i,x_i)|<=eta_i`; errors can be arbitrarily correlated. Retain the interval

`A(t_i,x_i) in [Yhat_i-m*x_i-eta_i, Yhat_i-m*x_i+eta_i]`.

**After acquisition**, a controller can change the feedback gain, the source time, the network topology, the source-input mixing and the requested state functional. The learner has no native inverse, derivative, network-equilibrium or transpose oracle.

The previous general vector-valued mixed-feedback Pro3 solver used recursive box exclusion. The present construction establishes a broad **scalar-source** subclass in which even mixed feedback and multiple unforeseen inputs have an **exact finite polyhedral consistency representation**. The assumption that scalar residuals map a scalar physical input to a scalar response is central: the result must not be promoted to the Euclidean vector-valued setting, where ordering is unavailable.

## 2. The complete scalar noisy-history theorem

Let `D((t,x),(s,y))=a*|x-y|+v*|t-s|` (a possibly degenerate metric if `a=0` or `v=0`). For finitely many points `z_i=(t_i,x_i)`, specify interval obligations `[l_i,u_i]`. They can all be realized by **one globally defined** residual satisfying the contract if and only if, for every ordered pair,

`l_i - u_j <= D(z_i,z_j)`.                                                (1)

**Necessity** follows from `l_i <= A(z_i) <= A(z_j)+D(z_i,z_j) <=u_j+D(z_i,z_j)`. For sufficiency, define the explicit lower extension

`A_*(z)=max_i {l_i-D(z,z_i)}`.                                             (2)

Each term is 1-Lipschitz relative to `D`; their finite maximum is also 1-Lipschitz. At `z_j` it is at least `l_j`. Every term is at most `u_j` by (1), so `A_*(z_j)<=u_j`. Thus (2) is a **witness source**, not only an uncertainty inequality. The proof also accommodates repeated locations, correlated bounded errors and times after the observation window.

This resolves an important distinction with prior Pro3 vector observations: **pairwise scalar interval consistency is jointly sufficient here**, whereas generic vector-valued noisy completion can fail joint consistency despite passing pairwise tests. The conclusions do not contradict one another because the output-space contracts differ.

## 3. The ordered-response procedure theorem

Fix `q` unknown future state variables `z in R^q`. A later experimental operation may specify finitely many *virtual source evaluations* at known times with

`input_j = s_j(z)`, `output_j = r_j(z)`,

where `s_j`, `r_j` are **known affine functions of z**. For old sites the inputs and interval outputs are constant; for future virtual evaluations their output obligation is the singleton `r_j(z)`.

By (1), a state portfolio is compatible with one true source if and only if

`l_i(z)-u_j(z) <= a*|s_i(z)-s_j(z)|+v*|t_i-t_j|` for all i,j.           (3)

Partition state space by the finitely many hyperplanes `s_i(z)=s_j(z)`. On each closed ordering cell, every absolute value in (3) has a fixed sign; (3) and the cell's ordering inequalities are **affine rational halfspaces**. Therefore the complete portfolio-consistency set is a **finite union of rational polyhedra**. If bounded, the extreme value of *any later linear observable* `c^T z` is obtained exactly by rational LP on each nonempty cell. Every attained extremum admits a globally defined source witness (2).

The theorem is exact even for **signed interconnections** and for portfolios whose source evaluation locations are not themselves measured state coordinates. It is not polynomial-time in the number of states: order-cell enumeration can grow factorially, and rational arithmetic can grow expensive.

Two special consequence classes:

**A. Mixed-feedback, changing-time inverse queries.** A future load and controller obey `p_j=(m-K_j)z_j+A(t_j,z_j)`. Thus `s_j=z_j` and `r_j=p_j-(m-K_j)z_j`. When `m-K_j>a`, every permissible source has one and only one equilibrium for that query. A previous anchor `(t0,x0,Yhat0,eta0)` implies

`|z_j| <= (|p_j-(Yhat0-m*x0)|+a*|x0|+v*|t_j-t0|+eta0)/(m-K_j-a)`. (4)

This supplies the finite bounding rectangle for the exact 2-state polygon implementation.

**B. Newly wired networks sharing a latent scalar source.** For `z in R^q`, allow the future equations

`m*z_j+A(t_j,L_j z+c_j)=p_j`.                                       (5)

Signed coefficients in `L` are permitted. If `m>a*||L||_infinity` and `c=0`, the map `z -> (p-A(t,Lz))/m` is a global contraction in infinity norm. Every admissible source has a **unique** network equilibrium. From any old anchor `(t0,x0,r0 +- eta0)` a common state box obeys

`||z||_infinity <= max_j(|p_j|+|r0|+eta0+a*|x0|+v*|t_j-t0|)/(m-a*||L||_infinity)`. (6)

The code implements (5) for `q=2`, `c=0`, with both positive and negative couplings. All extremal portfolios receive a single McShane source witness; no fictitious independence between the two virtual residual evaluations is introduced.

**Why the procedure is complete, not just sound:** the virtual finite nodes satisfying (3) extend by (2); that source has exactly the prescribed virtual outputs. Under (4) or the contraction in (5), those states are the unique outcomes of the stipulated later operation.

## 4. Correlated calibration is a different observation contract

Suppose the native sensor adds one common, unknown bias `b in [b_-,b_+]` plus individual bounded errors `e_i`:

`Yhat_i=F(t_i,x_i)+b+e_i`, `|e_i|<=eta_i`.

The retained residual band is now `[Yhat_i-m*x_i-b-eta_i,Yhat_i-m*x_i-b+eta_i]`. On every ordering cell, the complete joint consistency constraints are **linear in `(z,b)`**. For one common scalar nuisance, write inequalities `h(z)+beta*b<=c`; a positive-beta row and a negative-beta row give a necessary and sufficient projected inequality after dividing by their positive magnitudes and adding. Rows independent of `b` are carried unchanged. This is ordinary exact Fourier–Motzkin elimination; the implementation then optimizes over two state variables using rational vertices. For a higher-dimensional shared linear calibration nuisance, polyhedral projection/LP applies, with potentially worse complexity.

A source witness for any feasible `(z,b)` again uses (2). This establishes sharp source-family bounds, accounting for **one shared sensor bias rather than fabricated independent biases**.

A useful negative control: in four near-coincident mixed-feedback questions, the common-bias treatment did **not** improve the error radius compared with independent inflation by the same worst-case bias magnitude. That is a real failure of the stronger representation to help those tasks; no improvement is claimed.

## 5. Actually executed acquisition and future operations

All demonstrations use exact rational synthetic sources and **charge every native observation**. A separate source-aware checker, never the learner, chooses test loads that are known to have valid responses. The source contract is proved from the fixture definition by bounding its absolute-value slopes, but is supplied to the learner without the formula.

**Nonlinear time-dependent source:** `A(t,x)=|x-1/5|/5-|x+1/7|/7+t/20`; take `m=3`, public `a=1/2`, `v=1/10`. The total spatial Lipschitz constant of this actual residual is at most `1/5+1/7=12/35 <1/2`, with temporal constant `1/20<1/10`. Four native noisy scalar forward readings (errors bounded by `1/1000`) are taken at two times and four positions.

**Changed feedback and times.** Six unseen two-equilibrium contrast tasks, with varied gains and times, were certified with **zero** further learner calls. The sharp worst-case radii were:

| Task | Separate-equilibrium radius | Joint exact radius | Improvement |
|---|---:|---:|---:|
| 1 | 0.075377 | 0.017250 | 4.37x |
| 2 | 0.108730 | 0.023651 | 4.60x |
| 3 | 0.055293 | 0.021843 | 2.53x |
| 4 | 0.158165 | 0.031135 | 5.08x |
| 5 | 0.091499 | 0.027549 | 3.32x |
| 6 | 0.086257 | 0.021864 | 3.95x |

The separate-equilibrium comparator optimizes each equilibrium with the same old history and source contract, but discards the constraint tying the **two future outcomes to the same source**. An equally informed conventional retainer that keeps the joint consistency family can use the present LP and tie it. The first suite checked 133,380 rational pairwise line intersections while exploring ordering cells, excluding the additional independent tasks.

**Newly connected networks.** The same four readings supported four later signed/cooperative two-state network structures, at new times, and three future observables per network (12 tests, zero later native calls). The state-difference task bounds were:

| Network | Joint radius | Dropping the future-future source constraint | Width reduction |
|---|---:|---:|---:|
| Signed L1 | 0.010880 | 0.100344 | 9.22x |
| Signed L2 | 0.026045 | 0.121138 | 4.65x |
| Cooperative L3 | 0.051401 | 0.100724 | 1.96x |
| Signed L4 | 0.002251 | 0.055546 | 24.67x |

Here the independent-future construction is a **valid relaxation**, not a claimed globally attainable or optimal independent physical model. All 12 reference outcomes lie in the actual sharp intervals, and exact McShane sources attain the upper and lower extremal states. Four tested source wiring matrices and all later loads are in the JSON results; both signs of coupling occur. There were 22,230 exact candidate line intersections per two-state task in this suite.

**Deliberate impossibility control.** Duplicate historical inputs at the same time with contradictory, nonoverlapping output intervals are rejected as `INCONSISTENT`, even when other readings seem plausible. No source family or future answer is issued.

## 6. A persistent calibration-gauge information obstruction

A separate exact construction uses `m=4`, public `a=1/10`, no time drift, and two old biased reports `Yhat(0)=0`, `Yhat(10)=40` with zero individual noise. The common bias satisfies `|b|<=1/2`.

For **every** `b in [-1/2,1/2]`, the genuinely different physical source

`F_b(x)=4x-b`

and the instrument with additive bias `+b` produce the **same report**

`Y_b(x)=F_b(x)+b=4x`

at **every possible input**. This is a full adaptive-transcript indistinguishability construction, not a finite-sample or weak-excitation example.

For future physical feedback gains `K1=2`, `K2=1`, new loads `p1=1/10`, `p2=597/20`, and physical responses `p_j=F_b(x_j)-K_j*x_j`, the equilibrium difference is

`x1-x2 = p1/2-p2/3 + b*(1/2-1/3)`.

The unavoidable worst-case error radius for any method restricted to the **same uncalibrated sensor**, after arbitrarily many readings, is therefore `B*|1/2-1/3|=1/12 ~=0.0833333`. The exact broader Lipschitz consistency family has radius `0.10186757`. Treating the common bias independently at each old site gives the weaker radius `0.41815467` (4.10x larger). One additional physical-source reading at `x=5` through the same biased instrument leaves the exact sharp radius **unchanged**. An **external exact calibration of b** would reduce the sharp radius to `0.00417479`; that external sensor privilege must be paid separately and is not obtainable simply by issuing another ordinary forward call.

This distinguishes *more of the same measurements* from an experiment that genuinely breaks the source/instrument gauge. It is a decisive procedure-selection fact, though the common-additive-gauge argument itself is elementary.

## 7. Code, certificate mechanism, actual costs, and verification

The four standard-library Python scientific programmes are:

- `mixed_temporal_exact.py`: exact rational ordering and source-extremal compiler, six mixed-feedback/noisy/time-varying tasks and an inconsistent-history control.
- `mixed_calibration_exact.py`: one shared unknown calibration offset, exact Fourier–Motzkin elimination, four informative negative controls.
- `shared_network_order_compiler.py`: four changed signed/cooperative network structures, 12 later task bounds, contraction and extremal source checks.
- `calibration_gauge_limit.py`: an actual full-adaptive-transcript indistinguishability family, a repeated-source-reading control, and a separately charged external-calibration comparison.

Every polyhedral extremum is computed by enumerating the intersections of rational halfspace boundaries inside an explicitly derived bounded rectangle. Each feasible candidate is checked against all source/order constraints; the complete geometric enumeration proves no missing optimum. A constructed McShane extension realizes both extremal states as one source. This exact method is appropriate for two unknown states, **not** a general scalable rational LP solver.

`verify_results.py` independently checks saved rational outcomes and repeat-executes all four scripts from a fresh temporary directory, comparing every result file's SHA-256. All four clean replays passed byte-for-byte, with suite runtimes recorded in `independent_replay_results.json`. The scientific tests include 23 task portfolios (6 mixed-feedback, 4 shared-bias, 12 network observables, one separate gauge task). This is reproducibility of the *software* and mathematical controls, not formal verification of the complete proofs.

The reported acquisition costs are four initial scalar native source calls for the first three suites and two initial scalar calls for the gauge source; the latter evaluates a hypothetical third call separately. All later task inferences use **zero** native source calls. Experiment-cost comparisons do not hide source-aware reference checks or software enumeration. The JSON contains the exact rational loads, true checker states, compatible source extremizers, widths, order-cell counts and investigated candidate intersections.

## 8. Actual boundaries and strongest next attacks

1. **Physical contracts are supplied, not acquired.** No finite collection of readings of an otherwise unrestricted smooth physical system proves the global spatial/temporal Lipschitz constants: a smooth bump supported away from all sampled spacetime points can preserve every previous reading and violate the bound. This is a fundamental missing-warrant obstruction, not a compiler bug.
2. The exact polyhedral mechanism relies on **scalar** residuals and affine future evaluation/input expressions. In vector physical inputs and responses, ordering does not resolve Euclidean norms; the earlier fixed-feedback convex SOCP and mixed-feedback box methods remain distinct.
3. The identity of the scalar residual source **across experimental modules and future times** is assumed. A shared latent physical mechanism, but not its actual form, is part of the source contract. Independent different sources must not be collapsed.
4. No finite input-history size bound or polynomial-time scaling is established. The order cells can grow factorially; source evaluation and full future network LPs may be prohibitively expensive.
5. A detector’s common bias can be an **irreducible gauge** even if its reported entire source graph is measured; a different measurement interface or operation definition is required to resolve it.
6. Same-information retaining algorithms can adopt the identical exact consistency representation and tie every guarantee. Dropping joint constraints is intentionally a weaker baseline; the results establish the value of retained correlations, not privileged algorithmic access.
7. The next mathematical opportunity is a **contract-weakening branch**: compile inverse operations from order/monotonicity observations without any quantitative upper Lipschitz ceiling, then compare what remains usable and what new sensors are necessary. A still harder physical opportunity is to warrant source regularity with independently testable instrumentation rather than assuming it.

## Prior primary evidence and mathematical antecedents

- This extension was developed after inspecting the governing prior Pro3 note `ASTRA_PRO3_JOINT_INVERSE_SECTOR_TRANSFER.md`, especially its complete common-feedback theorem, its scalar mixed-feedback counterexample, and its rational box-search limitations. That note and the earlier uploads remain separate historical evidence; no old sandbox path was reused as a new artifact.
- Scalar Lipschitz extension by the maximum-of-cones formula is classical McShane–Whitney theory. See Valentin Gutev, *On real-valued functions of Lipschitz type*, *Expositiones Mathematicae* 43 (2025), DOI: https://doi.org/10.1016/j.exmath.2025.125701, for a modern exposition.
- Exact rational polyhedral optimization, Fourier–Motzkin elimination, Banach contraction and source indistinguishability are standard component principles. No priority search supports claiming them new.

## 9. Executed second attack: order-only acquisition, with no upper Lipschitz ceiling

After completing the mixed-feedback and calibration studies, I tested a **different, weaker physical contract** rather than continuing to refine the same fixture. The source is now stationary and scalar,

`F(x)=m*x+A(x)`, `m>0`,

where `A` is **continuous and nondecreasing**, but its slope and any upper Lipschitz constant are completely unspecified. Future gains obey `K<m`, so `x -> (m-K)*x+A(x)` is strictly increasing and globally surjective. There is a unique response to every later scalar load.

Let historical residual observations be exact `(x_i,r_i=A(x_i))`, sorted by input (the same argument extends to interval outputs if their isotonic consistency constraints are checked). A requested future load `p` under gain `K` at an unknown equilibrium `x` must satisfy `r=p-(m-K)*x`. On a particular open interval between consecutive old locations, a compatible nondecreasing source exists if and only if

`max{r_i:x_i<x} <= r <= min{r_i:x_i>x}`.                           (7)

The inequality holds with the obvious one-sided conventions outside the observed range. At an **exactly coincident** location, `r` must instead match that site's true reading. These constraints are linear in `x` on each ordered interval. Their infimum and supremum across intervals form the sharp possible response range over the stated class. To prove sufficiency, select a permissible `x`, insert the new `(x,r)` into the ordered dataset and join consecutive points by straight segments, extending the residual constantly outside its extreme observation locations. This constructs a global continuous nondecreasing residual. Because no upper slope bound is supplied, solutions can approach an old location with an increasingly steep short segment; a reported endpoint may be a sharp infimum/supremum without itself being realized by a continuous source. The implementation distinguishes its `SHARP_INF_SUP` claim from an attained maximum.

**Actual native acquisition.** I used `m=2` and a synthetic, nonpolynomial monotone piecewise-linear residual

`A(x)=max(0,x+1/2)/9 + max(0,x-1/3)/7`,

with four exact native readings at `-1,0,1,2`. After those readings, eight new loads and feedback gains were specified. Their sharp absolute-error radii, respectively, were

`0.01389, 0.06878, 0.04127, 0.06349, 0.08466, 0.04127, 0.05635, 0.10317`.

All eight source-aware answers were enclosed with **zero later learner source calls**. The code also explicitly inserts virtual readings near both reported extrema and checks that a continuous piecewise-linear monotone source can interpolate them. One additional *charged* forward experiment at the midpoint of a chosen retained interval narrowed its sharp radius from `0.06878307` to `0.02898295` (about 2.37x). No derivative, potential, upper stiffness or global Lipschitz constant was used.

This is a scientifically meaningful trade: **quantitative precision transfers are possible without a quantitative upper-regularity contract**, but they require a different stationarity and monotonicity promise. If time drift is unconstrained, old measurements need not bound later response; if monotonicity is not physically justified, the enclosure is invalid. The result is classical isotonic interpolation/optimal recovery connected to the existing reusable source-to-operation interface, not a new general identification theorem.

The executable control and saved data are `monotone_weak_contract.py` and `monotone_weak_contract_results.json`; the clean replay verifier covers this fifth investigation as well.

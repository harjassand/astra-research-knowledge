# Independent review: strict-power clearing by short-time production

2026-10-30. Reviewer: `producer-workspace/review_chemical_global_foster`.

## Verdict

**PASS for `STRICT_POWER_FAST_CLEARING_V2.md`, with the catalyst convention below.** Its uniform short-time production estimate, falling-factorial error, martingale control, independent killing coupling, and block restart are valid for the stated fixed-coefficient homogeneous family. No prior recurrence, factorial-boundary mean bound, or mixing theorem is needed.

There is a stronger conclusion, fully proved below. If the constructed deterministic production exponent is L>=1, set

```
delta = 1/(mL+1),       beta = m-1+delta.
```

Then, uniformly over every initial composition on all sufficiently large N-shells,

```
E_x tau_clear <= C N^(-beta),
P_x(tau_clear>t) <= 2 exp(-c N^beta t).
```

Thus the draft's safe exponent `1/[4(mL+1)]` can be increased to the critical exponent `1/(mL+1)`. A fixed large block multiplier, not a diverging hazard within a unit-multiplier block, provides the requisite constant probability of clearing. For m=3 and L=1 this recovers `N^(-9/4)`.

This is a killed conservative-fiber theorem, not a general weakly reversible recurrence theorem or a mixing claim. Coefficients are fixed in time and state, although constants are uniform when their fixed values range over a specified positive compact box. Arbitrary state-dependent controls are not approved by this argument. Exact-result novelty is unverified; quantitative fluid approximation and uniform-block iteration are established methodology.

## Reviewed sources and preservation

Source directory: `producer-workspace/chemical_joint_shell_20261030`.

| File | SHA-256 |
|---|---|
| `STRICT_POWER_FAST_CLEARING_V2.md` | `99da4993b135ece91efe5d689d066e5985a2cd46aafff1d4c73c33ce551313dd` |
| `UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME_V2.md` | `bf2dfd46e12d16bb6f18ab2f8471c152a9243f08b5bcd57e9e3fb670fd60339a` |
| Historical initial strict-power draft | `dae538e087b0f22e55c60ccc47c07655ed4518acd8e47d3ada2d18292520e1c6` |

Byte-identical copies are retained in `inputs/`. The second file supplies the **family contract and finite-N scope**, not a load-bearing absorption estimate: the strict-power proof below is independent of its fractional-factorial argument.

Earlier whole-v1 receipt remains unchanged at `producer-workspace/INDEPENDENT_WHOLE_PROOF_REVIEW.md`, SHA-256 `7bd2ab1c58495998f58149663e38c11af89d9abfe3ba17e1c0f5d18f914ed8b9`. The separate bounded-oscillation/all-face review is `producer-workspace/INDEPENDENT_REVIEW.md`, SHA-256 `f455b3db03682055a345fe3d66dfb8440b0cf4f25050bb705bed1ae3d84b5853`.

## 1. Exact assumptions

There are d>=2 composition species, total population N. Every fast source and target complex has the same order m>=2. The finite complex graph is strongly connected and contains every pure complex mX_i. Each fast reaction has fixed positive mass-action coefficient; these coefficients may range over a prescribed compact positive box when taking uniform constants. Killing is the actual distinguished event with rate `c_A(A)_m`, where c_A>0 is fixed (or bounded in its own positive compact interval).

The fast generator before killing acts on the finite N-shell. Its total rates are finite, and it preserves N. Conservative irreducibility at state level is not assumed: residue classes and other disconnected classes are allowed. The common catalyst factor, if present, is removed until Section 6.

## 2. Uniform deterministic production really follows from the graph

Write the normalized mass-action vector field as

`b(z)=sum_(y->y') k_(y,y') z^y (y'-y)`

on the closed unit simplex. It is polynomial and uniformly Lipschitz there. Conservation makes the sum of coordinates constant. At z_j=0, every negative contribution to b_j vanishes, so the simplex is invariant.

For any coordinate j, every consuming source has y_j>=1. Since all simplex coordinates lie in [0,1], `z^y<=z_j` for such a source. Thus the total negative contribution is bounded below by `-C z_j`, with C uniform over the coefficient box.

For any initial point choose a species i with `z_i(0)>=1/d`. The differential inequality `z_i'>=-Cz_i` yields

`z_i(t)>=(1/d)exp(-Ct)>=(1/d)exp(-C)` for `0<=t<=1`.

Fix once and for all a complex path from mX_i to mA. Scan its edges, keeping the set of species already assigned lower bounds `z_l(t)>=a_l t^(L_l)` for the full time interval `(0,1]`. Start with species i, exponent zero. Whenever a product introduces a species j absent from this accumulated support, the current source has y_j=0 and the edge has positive net production of j. Every species in that source already has a lower bound, because the source is the preceding complex on the path. Therefore

`z_j'(t)>=a t^r-Cz_j(t)`, where `r=sum_l y_l L_l`.

Variation of constants gives the explicit bound

`z_j(t)>=a exp(-C)t^(r+1)/(r+1)` on `(0,1]`.

All previously derived bounds remain valid: each was a global differential inequality for the same full ODE, including all consumption through the common `-Cz_l` bound. This is not an assertion that the actual trajectory follows the selected complex path, and no reaction-path probability is substituted for an ODE estimate.

The scan eventually assigns A, since the terminal complex is mA. If i=A, its constant lower bound also bounds a positive multiple of t^L for any L>=1. Taking the largest exponent and smallest positive constant over the finitely many possible initially dominant species gives

`z_A(t)>=a_0 t^L`, `0<t<=1`,

uniformly over **all** initial simplex points and over the coefficient box. The recursion uses only positive coefficient lower bounds and a common consumption upper bound, so uniformity is genuine.

The integer exponent can be bounded explicitly. Whenever a new species is introduced, `L_new<=m L_max+1`. There are at most d-1 introductions after the initial species. Hence one may take

`1<=L<=(m^(d-1)-1)/(m-1)`

after replacing smaller exponents by the worst one. A particular graph may admit much smaller L. Constants remain graph- and coefficient-dependent. No claim that this L is optimal is made.

## 3. Uniform finite-N fluid error, including disabled sources

Let X be the **unkilled** fast chain, and define

`Y_N(u)=X(N^(1-m)u)/N`.

Its jump for edge e is `nu_e/N`, and its rescaled rate is `N^(1-m) k_e (NY_N)_(y_e)`. Consequently its drift is

`b_N(z)=sum_e k_e nu_e N^-m (Nz)_(y_e)`

on the lattice simplex. Fixed-degree falling-factorial polynomial expansion gives

`sup_lattice |b_N(z)-b(z)|<=C/N`.

This estimate includes disabled sources: at integer counts below the source multiplicity, the falling factorial is exactly zero because its product has a zero factor. Polynomial expansion is still valid; no false division by a small source monomial occurs.

The rescaled total jump rate is at most CN, and every jump has magnitude at most C/N. The compensated vector martingale therefore has predictable quadratic-variation trace at most `Cu/N` and

`E sup_(u<=T)|M_N(u)|^2<=CT/N`, `0<T<=1`.

This is Doob's inequality, with finite dimension absorbed in C. The chain is finite and nonexplosive for each fixed N before killing, so no stopping-at-explosion circularity enters.

Let z solve the ODE with initial point exactly x/N. Its error obeys

`sup_(u<=T)|Y_N(u)-z(u)| <= exp(KT)[sup_(u<=T)|M_N(u)|+CT/N]`.

Squaring, taking expectations, and applying Markov's inequality gives

`P(sup_(u<=T)|Y_N(u)-z(u)|>eta)
 <=C[T/N+T^2/N^2]/eta^2`.                                      (F)

All constants are independent of the initial composition and N, and uniform over the fixed coefficient box. In particular (F) is valid on shrinking time intervals and with shrinking tolerances; it is a quantitative estimate, not an appeal to an unquantified fluid-limit theorem.

For the source's choice `epsilon=1/[4(mL+1)]`, `T=N^-epsilon`, and `eta=(a_0/2)(T/2)^L`, its asserted exponent

`kappa=1-epsilon(2L-1)>epsilon`

is correct. The deterministic drift-error term has strictly faster decay. Its original safe-exponent proof therefore passes as written.

## 4. Independent hazard coupling and the critical exponent

Set `delta=1/(mL+1)` and choose a fixed constant R>=1, to be specified. Take

```
T_N=R N^-delta,
eta_N=(a_0/2)(T_N/2)^L,
t_N=N^(1-m) T_N=R N^(1-m-delta).
```

For sufficiently large N, T_N<=1. On the good event in (F), for every u in `[T_N/2,T_N]`,

`Y_(N,A)(u)>=a_1 T_N^L`, where `a_1=a_0/2^(L+1)>0`.

Furthermore,

`N T_N^L=R^L N^(1-L/(mL+1)) -> infinity`.

Thus A is eventually at least 2m throughout that interval, and `(A)_m>=2^-m A^m` there. This checks the actual factorial killing rate rather than replacing it by A^m at bounded A.

Construct clearing by an independent unit exponential variable E and the cumulative hazard of the unkilled path:

`tau=inf{t: integral_0^t c_A(A(s))_m ds >= E}`.

Up to tau this is exactly the CTMC with the additional clearing channel. Conditional on the fast path, survival is the exponential of minus its cumulative hazard. On the good event the hazard by physical time t_N is at least

```
c_H N^(1-m) T_N (N T_N^L)^m
 =c_H N T_N^(mL+1)
 =c_H R^(mL+1),
```

with c_H>0 uniform in the initial state and coefficient box.

Meanwhile (F) gives

```
P(bad) <= C_R N^-kappa_* + C_R N^-[2-delta(2L-2)],
kappa_* = 1-delta(2L-1)
         = [(m-2)L+2]/(mL+1) > 0.
```

The second exponent exceeds kappa_* by `1+delta`. Choose R once so that `exp(-c_H R^(mL+1))<=1/4`. Then choose N sufficiently large that the fluid-error probability is <=1/4. This yields the uniform one-block bound

`sup_x P_x(tau>t_N)<=1/2`.                                (B)

At the critical exponent the good-event hazard need not diverge with N. A sufficiently large fixed R supplies the constant clearing probability, while the error probability still vanishes. This is why the sharper exponent is permitted.

## 5. Restart establishes its own finiteness

The model has fixed coefficients, and (B) holds for every state on the same N-shell. On survival at a block boundary the residual state remains in that shell; exponential memorylessness and the Markov property give

`P_x(tau>j t_N)<=2^-j` for integers j>=0.

Integrating the piecewise constant bound gives

`E_x tau<=t_N sum_(j>=0)2^-j=2t_N`.

For arbitrary t>=0,

`P_x(tau>t)<=2^-floor(t/t_N)
 <=2 exp[-(log 2)t/t_N]`.

This proves the verdict with `C=2R` and `c=(log 2)/R`. It also proves tau finite almost surely. There is no prior mean bound inside this argument; the use of the same uniform short-time estimate after each restart is not circular. The unkilled chain, not an assumed recurrent full network, is the process used to establish the estimate.

For the original cubic fast chain, each initially pure non-A species immediately has a fast edge producing A, so L=1. Then `beta=3-1+1/(3+1)=9/4`, exactly the earlier special-chain clearing exponent. This equality is a mathematical consequence of the production bound, not a claim of optimality over all possible processes.

## 6. Catalyst, genuine competition, and finite-state exceptions

A fixed positive factor a_B multiplying both fast and clearing rates divides all times by a_B and multiplies the exponential-survival rate by a_B. For `(B)_q`, require B>=q when q>=1. If q=0 the factor is one. If a_B=0 there is no finite clearing claim.

Before the first genuinely competing connector birth, N and B are fixed. Suppose its total rate is at most `C(1+NB)` along the fiber. Couple its hazard independently with the fast and clearing clocks. Removing the birth channel until its first event, or using the exact competing-hazard formula, gives

```
P(birth before clearing)
 <= E integral_0^(tau_clear) rate_birth(X_s) ds
 <= C(1+NB) N^(1-m-delta)/(B)_q.
```

This is an actual first-event comparison, not an equilibrium average. The bound can of course be capped at one. For B>=max(q,1), fixed q, the falling-factorial comparison yields the simpler

`O(N^(2-m-delta) B^(1-q))`.

The source's final simplification assumes B>=1; this is automatic in its intended connector family q>m>=2. If q=0 and B=0 are allowed as an optional catalyst convention, retain the unsimplified expression: the simplified expression would incorrectly give zero despite immigration. This qualification does not affect the clearing theorem.

Small N is not automatically covered. The preserved counterexample is `2A<->2C`, N=2, x=(1,1), with killing `(A)_2`: the state is inactive and never clears, even though other states of its shell are active. Only source-enabled states/classes can be included by a separate finite-state access argument. For N>d(m-1), a pure source is enabled everywhere; the analytic threshold can be larger.

Conservative state-level irreducibility is unnecessary throughout. Arbitrary state-dependent fast coefficients, however, would remove the fixed polynomial Lipschitz ODE used in (F). The compact **constant-coefficient** uniformity must not be silently upgraded to arbitrary controls.

## 7. What the strict power supplies downstream—and what it does not

For cubic m=3, competition of order NB against a shared resource factor has N-exponent `-1-delta`. Thus the scalar sum `sum_n n^(-1-delta)` is finite. If an actual no-birth descent lowers N by m per clearing and maintains B>=S, this bound supplies a uniform `O(S^(1-q))` total birth-interruption risk before a fixed finite head. The sum of the mean clearing times is also finite. These conditional statements follow by positive summation and uniformity over each clearing's output composition; they do not themselves specify a full residual trace.

For m=2, the same crude birth-risk sum has exponent `-delta` and need not converge; additional resource growth or another argument would be required. No general-order tail closure is inferred from the power gain alone.

In every case, the full connector process still requires actual output/return accounting, low-resource phases, threshold leakage, and global matching. This review neither solves those obligations nor assumes a closed finite corner.

## 8. Primary methodological comparators

The martingale-plus-Gronwall estimate is established quantitative fluid-approximation machinery: [Darling–Norris, *Differential equation approximations for Markov chains*, arXiv:0710.3269v2, §4.1 and Theorem 4.1](https://arxiv.org/pdf/0710.3269). Their §4.2/Theorem 4.2 provides stronger exponential-error estimates under suitable hypotheses. The L2 estimate proved here is sufficient; using a shrinking time interval does not make the underlying approximation principle new.

Uniform block restart is likewise ordinary Markov-chain machinery, as illustrated by [Aldous–Fill, §2.4.3](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch2.S4.html). The preceding proof does not depend on citation for validity: every estimate needed for this family has been derived explicitly.

The actual contribution established by this review is a uniform finite-graph production exponent, its compatibility with stochastic errors down to the critical startup scale, and an actual clearing-hazard bound for the stated family. Whether the precise family theorem or equivalent argument already appears in the literature remains unverified. No external publication or experimental chemistry/biology was performed.

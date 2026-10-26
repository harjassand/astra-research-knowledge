# ASTRA Pro3 — Exact port-quotient learning and active-interface invention

27 October 2026. Constructive mathematical and executable research continuation of `ACQUIRED_POSITIVE_OPERATIONS(1).md` and `ACQUIRED_LATENT_MIXED_CONTROLLER_THEOREM.md`.

**Scope.** The underlying source is a fixed real symmetric positive-definite response operator. The original full-vector action and any later boundary-clamp/reaction action are **distinct, explicitly charged instrument interfaces**. Linearity, symmetry, a global spectral contract, noiselessness where used, and the ability to configure specified known positive rank-one shunts are supplied, not learned from finite observations. These are mathematical/software controls, not physical experiments. The specific classical ingredients are operator intervals, Schur complements/shorting, inverse order, positive contractions, Sherman–Morrison, polarization, and minimax indistinguishability. No historical-priority or exclusive algorithmic advantage is asserted.

## 1. Exact transfer theorem: eliminating unknown internal ports preserves the *whole* Loewner interval

Let `0 < L <= S <= U` in Loewner order, where every matrix in `[L,U]` is genuinely allowed by the retained record. Let `P` be a full-row-rank `d×n` rational matrix defining an experimentally accessible boundary constraint `P x=z`. When the interior of quadratic energy `x^T S x/2` equilibrates, the boundary energy is `z^T R_P(S) z/2` with

`R_P(S)=(P S^(-1) P^T)^(-1)`.

**Exact image theorem.**

`{R_P(S): L<=S<=U} = [ R_P(L), R_P(U) ]`.

This is equality of sets of **matrices**, not just inequalities for individual quadratic forms. In particular, every interior reduced matrix is realized by a compatible *full* positive-definite source.

**Constructive proof without irrational square roots.** Inversion reverses Loewner order and is a bijection from `[L,U]` onto `[U^(-1),L^(-1)]`. Write `D=L^(-1)-U^(-1)>=0`, `Z0=P U^(-1)P^T`, `M=P D P^T`. A desired reduced `R` lies in the asserted right-hand interval iff its inverse `Z=R^(-1)` lies in `[Z0,Z0+M]`; set `E=Z-Z0`, so `0<=E<=M`.

If `M` is nonsingular, define the rational matrix

`X=D P^T M^(-1) E M^(-1)P D`, `Q=U^(-1)+X`, `S=Q^(-1)`.

Then `P Q P^T=Z`, `0<=X<=D`, and hence `L<=S<=U` with `R_P(S)=R`. The inequality `X<=D` follows by writing `D=D^(1/2)D^(1/2)`: the middle multiplier is a positive contraction, because `0<=E<=M=PD P^T`. For singular `M` the same argument holds with the Moore–Penrose pseudoinverse `M†`, since `E` has range contained in `range M`. Rational pseudoinverses remain rational. This constructs a *source witness* for any rational proposed boundary operator, not merely a fitted response.

An alternative description uses the elementary fact that compressing a PSD operator interval `0<=X<=D` by a fixed linear map is **surjective** onto `0<=PXP^T<=PDP^T`. Composition with two inversion order isomorphisms proves the result.

**Exact query complexity in the new interface.** Let `Δ_R=R_P(U)-R_P(L)`. Then

`rank(Δ_R)=rank( P(L^(-1)-U^(-1))P^T ) =: r_P`.

Once this exact reduced interval has been acquired, `r_P` new full-vector **boundary** actions `q -> R q` suffice to identify the entire reduced matrix, by querying a rational basis of the range of `Δ_R`. They are necessary for deterministic, uniformly exact, possibly adaptive methods over the whole interval: after fewer queries along a central transcript there exists a nonzero uncertainty direction `w` orthogonal to all queried inputs, and small PSD-compatible perturbations `±εww^T` give the same entire transcript. This is a query theorem for the supplied full boundary-vector interface, **not** a scalar-sensor lower bound and **not** a theorem about an additional microscopic source restriction.

Thus the relevant dimension for future operations is the *interface-visible uncertainty rank*, which may be much smaller than the underlying source dimension or its original uncertainty rank.

## 2. Actual rank-two source and new boundary instrument

The established exact source class is `I<=S<=3I`. One **historical native full-vector** observation at `e0` returned `S e0=(2,1,0,0)`. Positivity of `I-(S-2I)^2` forces `S e1=(1,2,0,0)` and complete decoupling of the first two coordinates. Thus the exact admissible source family is

```
S=[ [2,1,0,0],
    [1,2,0,0],
    [0,0,*,*],
    [0,0,*,*] ],     I2 <= lower-right block <= 3 I2.
```

The actual checker chose the hidden block `[[2,1/4],[1/4,5/2]]`, and this was **not supplied to the learner**. Retained full-source uncertainty has rank two (three free symmetric coefficients).

Now provide a genuinely different future boundary instrument: it can impose `P x=z` and read the boundary force, for

`P = [[1,0,1,0],[0,0,1,1]]`.

The acquired reduced endpoints are

`R_L=[[6/7,-3/7],[-3/7,5/7]]`,
`R_U=[[6/5,-3/5],[-3/5,9/5]]`.

The interface-visible difference has rank two. Fifteen distinct rational interior targets were constructed in inverse-compressed coordinates; all admitted exact *full four-port* source lifts with the original historical reading unchanged. No microscopic source information was imported into the learner to produce these lifts.

**New native boundary observation.** The instrument queried `q=(1,0)` and returned

`Rq = (12/11,-27/44)`. 

Writing `R=[[a,b],[b,c]]`, the complete new reduced family has fixed `a=12/11`, `b=-27/44`, and

`303/352 <= c <= 633/352`.

The interval is exact by the two generalized Schur inequalities, and both endpoints have explicit original-source lifts. One measured boundary column reduces the remaining uncertainty rank from two to one; a second exact boundary-vector action `(0,1)` identifies `c` and the entire reduced response. This is a *later* interface (one historical four-scalar action plus one charged two-scalar boundary action), not a claim that a new interface came for free.

### Later mixed controllers: exact one-source range

After the boundary measurement, two late controllers are supplied: `K0=0` and the nonsymmetric `K1=[[0,1],[-1,0]]`; their task outputs are `e1^T(R-Kj)^(-1)e1` (indexing reduced ports from zero). Let `f0(c),f1(c)` denote these responses, and consider the *unforeseen* weighted contrast `f=f0-(133225/35721)f1`. Its derivative has precisely one critical point inside the admissible interval, at `c=117/88`, where the minimum is attained. Exact rational extrema:

`joint-source range = [-11264/11907, -87040/130977]`.

If one instead combines separately tight controller ranges while discarding the common source, the larger interval is

`[-7778560/4060287, 4357376/11918907]`.

The sharp width ratio is `182927/22568 ≈ 8.10559`. Source witnesses exist at every required interior and boundary extremum. Both controllers are mathematical forward predictions via rational inversion; **neither controller was physically run**. A fully informed ordinary retaining algorithm can tie all these results.

## 3. Noise correction: a false exact collapse and a sharp scalar repair

If the reduced instrument reports both coordinates of `Rq` with deterministic coordinatewise error at most `η`, it is **unsound** to freeze `a,b` at their displayed centres and claim the exact rank-one interval above.

For a reported pair `(a0,b0)` with `|a-a0|<=η`, `|b-b0|<=η`, and reduced endpoints `L_R,U_R`, every compatible unobserved diagonal `c` obeys

`c >= (L_R)22 + (b-(L_R)12)^2/(a-(L_R)11)`,
`c <= (U_R)22 - ((U_R)12-b)^2/((U_R)11-a)`

when the displayed denominators are positive. The unconstrained sharp lower candidate uses the **largest** allowed `a` and `b` closest to `(L_R)12`. The sharp upper candidate uses the **smallest** allowed `a` and `b` closest to `(U_R)12`. If their complete Loewner inequalities check, the candidates give attained exact minima/maxima and full-source witnesses. Otherwise the executable returns `UNKNOWN` rather than silently declaring sharpness.

For the experiment above, both endpoints are jointly feasible for noise widths `η=0, 1/1000, 1/200, 1/100`. At `η=1/1000` the identified `c` radius rises from `0.46875` to about `0.46997526`. These are sharp intervals for **this one scalar task**, not a claim that the entire noisy source family is a Loewner interval. The full-source lifting formula produces indistinguishable source witnesses at the endpoints.

A separate control constructs `R_true±(1/1000)I`, both fully source-realizable and both compatible with the same reported first column, while their unmeasured action differs. Hence genuine source uncertainty remains after a noisy observation even if a numerical routine prints a nearly saturated central estimate.

## 4. Changed mechanism: one accessible scalar port plus *reconfigurable* known shunts

A more physically consequential action is possible. Suppose the original accessible boundary is just `x0`; its unchanged scalar reaction cannot detect *any* coefficient of the hidden `r×r` block `T`, no matter how many times that same static experiment is repeated. The first two forced original coordinates have block `B=[[2,1],[1,2]]`, and the hidden block is `T` with `I<=T<=3I`.

Now suppose the native instrument can add a **known rank-one positive shunt**

`J_v = λ(e0-v)(e0-v)^T`, with `v` supported in the hidden block,

then clamp the single boundary port at unit displacement and read just **one scalar reaction**. The scalar source result is

`r_λ(v)=R0 + λ/(1+λ v^T T^(-1)v)`, with `R0=3/2`.

This identity follows exactly by minimizing the known quadratic energy in the hidden coordinates, or by Sherman–Morrison. It makes the one-port instrument a programmable quadratic-form sensor:

`v^T T^(-1)v = 1/(r_λ(v)-R0)-1/λ`.

For `λ=1`, query the `r` standard hidden directions `v_i=e_i`, then all `r(r−1)/2` pair sums `v_ij=e_i+e_j`. Recover `H=T^(-1)` by

`H_ii=q(e_i)`, `H_ij=[q(e_i+e_j)-q(e_i)-q(e_j)]/2`, then `T=H^(-1)`.

This is an **actual change of native experiment**: the new shunts must be genuinely configurable and each altered one-port reaction incurs one scalar experiment. It is not valid to produce `r_λ(v)` by mathematical postprocessing of unavailable source data. Rank-one shunt synthesis could have substantial hardware cost; no device or such native interface has been demonstrated physically.

**Optimal scalar-call theorem.** Exactly `r(r+1)/2` such measurements are sufficient and necessary to identify every interior compatible `T` under arbitrary deterministic adaptive strategies through this particular scalar shunt interface. Each report is an invertible transform of the *one* linear functional `v^T H v` of the `r(r+1)/2` unknown symmetric coefficients of `H`. After fewer probes, an adversary can choose a nonzero symmetric `Δ` annihilated by all probed forms and two sufficiently small perturbations `H0±εΔ` about an interior reference. Their complete adaptive transcripts agree, although their unknown response laws differ. Inversion maps their matrices back to valid distinct sources. This is an interface-specific dimension lower bound; a richer full-vector port instrument may use fewer calls.

**Executed synthetic controls:** hidden port counts `r=2,3,5` required respectively `3,6,15` scalar boundary readings, returning respectively `3,6,15` scalars. Every acquired inverse coefficient and the recovered hidden `T` matched the source-aware exact checker. Each control then executed one subsequently specified skew-coupled controller equilibrium with zero additional native calls. For `r=2`, two sources with different inverse off-diagonals produce precisely the same first two readings, while the third pair-sum reading distinguishes them.

### Noisy extension

For any one shunt report `y` with `|y-r(v)|<=η`, set `d=y-R0`. When `d>η`, the exact scalar quadratic form is enclosed by

`1/(d+η)-1/λ <= v^T T^(-1)v <= 1/(d-η)-1/λ`.

These outer intervals can be polarized into an outer matrix bound; if `||Hhat−H||<=δ<1/3` follows from exact arithmetic and `I<=T<=3I`, then

`||Hhat^(-1)-T|| <= 9δ/(1−3δ)`.

In the executed r=2 control with nonzero adversarial perturbations bounded by `η=1/1000`, the certified inverse-matrix error was `1529/250000 = 0.006116`, leading to a conservative recovered-stiffness error bound `13761/245413 ≈ 0.05607`. The true source lay inside the bound. This is *not* the minimax noise floor and not an exact noisy consistency set.

### Joint falsification of a falsely shared law

Three separate scalar readings can each individually obey the `[I,3I]` source contract yet **cannot** all arise from a single shared source. The executable set the first two inverse quadratic responses to `40/79` and `32/79`, and a reported pair-sum quadratic response to `19/10` (within its individual allowed `[2/3,2]`). These imply

`Hbad=[[40/79,781/1580],[781/1580,32/79]]`,

whose determinant is the strictly negative rational `−97961/2496400`. Every reading separately has a spectral-compatible source witness; together they violate positive definiteness. The procedure rejects the record instead of fitting a false hidden physical mechanism.

## 5. Why independently complete boundary descriptions still lose information

Exact interval transfer concerns **one chosen boundary interface at a time**. It does not mean that two separately exact reduced operator intervals can be chosen independently while keeping the same underlying physical source.

For `I2<=S<=3I2`, let one scalar boundary vector be `p=e1`, and another `q=(3/5,4/5)`. Each separate scalar effective stiffness ranges exactly over `[1,3]`. But the pair `(R_p,R_q)=(1,3)` is **jointly impossible**: `R_p=1` forces `S^(-1)p=p`, while `R_q=3` forces `S^(-1)q=q/3`; symmetric matrices cannot have nonorthogonal eigenvectors at distinct eigenvalues. More quantitatively, conditioned on `R_p=1`, the sharp upper bound becomes `R_q<=75/43`, attained by `S=diag(1,3)`, not the independently permitted `3`.

The proper joint compiler retains one common `S` (or its low-rank latent matrix) across multiple boundary choices and controllers. The independent intervals are safe only as **outer** portfolios. This is a real limit to fixed-width summary composition, not a defect of numerical precision.

## 6. Scientific judgement and honest comparison

**What is actually acquired?** A spectral-contract-qualified entire four-port source family from one saturated exact reading; exact reduced two-port response families for newly specified boundary maps; a reduced response column from a later *charged* boundary experiment; and, when reconfigurable shunts are genuinely available, scalar quadratic forms that reconstruct a hidden response block without direct access to its ports. Retained products include exact rational matrices, source-realization witnesses and task-dependent information budgets.

**Later transfer:** boundary energy and reaction under unseen port constraints; inverse/feedback tasks at one reduced interface; exact entire-boundary identification after the calculated number of added boundary actions; and formerly unobservable hidden inverse-response reconstruction via configured shunts, supporting new later linear controller responses. Cross-interface exactness requires carrying the common latent source, not replacing it by independent endpoint intervals.

**What must be supplied?** Fixed real linear symmetric PD source, initial spectral contract and exact saturated old reading where used, actual boundary-clamping and reaction sensors, allowed positive rank-one hardware shunts and their known strengths, or explicitly widened uncertainty under bounded noise. No absence-of-signal argument infers such physical contracts.

**Cost/comparators:** The full-information route can identify an r-port unknown symmetric block in r additional **full-vector** native queries if the hidden ports are accessible. The proposed reconfigured one-port route uses `r(r+1)/2` separate **scalar** readings and configured shunt changes. Their physical cost/bandwidth trade-off depends on real instrumentation. The previous historical full-vector call is *not forgiven*. An equally informed classical system-identification, Kron-reduction or set-membership retainer can use the very same mathematical procedures and tie all results. The correct scientific gain is an explicitly compilable, source-preserving **new operation interface**, not an exclusive architecture or known lifetime advantage.

**Remaining research frontier:** Actual physical feasibility and cost of reconfigurable shunts; source stability during repeated changed configurations; robust shared-parameter inference for jointly noisy reconfigurable readings; simultaneous exact preservation across multiple different boundary maps; and evidence-driven acquisition of the underlying spectral/linearity contracts. There is no new physical law or demonstrated apparatus.

### Executable evidence

- `acquired_port_quotient.py` → `acquired_port_quotient_results.json`: exact matrix-interval surjection and rational lifts; interface rank theorem controls; one native boundary observation; mixed-controller exact extrema; separate-interface impossibility; noisy false-collapse witnesses.
- `noisy_port_warrant.py` → `noisy_port_warrant_results.json`: four noise budgets, sharp unmeasured response bounds, individually verified full-source lifts.
- `reconfigurable_single_port_acquisition.py` → `reconfigurable_single_port_results.json`: native r=2,3,5 scalar instrument acquisitions, matching rank lower-bound pair, safe noisy polarisation, joint incompatible-record falsifier.
- `independent_verify.py` independently reconstructs primary identities, witnesses, and metadata; `clean_replay.py` separately executes research scripts and verifies byte-for-byte JSON output. All executable claims must be restricted to tests actually passing the verifier.

### Classical literature

- Anderson, *Shorted Operators*, SIAM Journal on Applied Mathematics 20 (1971), 520–525, https://doi.org/10.1137/0120053.
- Butler and Morley, *A Note on the Shorted Operator*, SIAM Journal on Matrix Analysis and Applications 9 (1988), 147–155, https://doi.org/10.1137/0609011.
- Sherman–Morrison formula, polarization and matrix inversion are classical; no separate priority claim.

# Independent receipt: actual weighted source-time storage

**Decision: PASS WITH EXPLICIT SCOPE CONVENTIONS.** No algebraic repair is required in either frozen source. The received result is a finite-size, stopped occupation/capture/source certificate for the actual twelve-channel rate-2 chain. The coefficient tradeoff genuinely permits the specified `E/B <= 1/5` gate without a separate `A <= εN` premise for this drift estimate. This is not admission, cone survival, weighted imbalance control, clock acquisition, clearance, recurrence, or mixing.

Reviewer: `review_weighted_source_storage`. Date: 2026-11-01. No helper, external source, installation, hardware action, or publication was used. Morrey work was not resumed.

## 1. Frozen sources and decision basis

The principal sources are:

* `WEIGHTED_SOURCE_TIME.md`, SHA-256 `849b4af64f65788d374b42da1e8b16d717314b62e5d6671c1d620a0bbda9c5b8`;
* `STORAGE_COEFFICIENT_TRADEOFF.md`, SHA-256 `a79b2fcbcd369130e3648eb5a05b7eeec205bdd65ec184901f9910bb9ce14242`.

The parent model is `TASK_OBSERVABLE_CORRECTOR.md`, SHA-256 `02e55555d845f7f3060e23500cb36934fbfd4709eb8755c9b1ebf2cfa7002a94`. All seven source/model/check files are copied and hashed in `SOURCE_SNAPSHOT_FREEZE.json`; no author freeze was present for the weighted continuation at the start of this review. The source files were not edited. Existing parent-component review is provenance only: the arguments below independently audit the weighted continuation.

Ordinary reasoning below is the decision basis. `independent_exact_audit.py` separately reconstructs reactions from reactant/product stoichiometry, checks formal finite-step identities and exact rational cases, and is only supplementary. Both author programs were replayed in a separate directory; their JSON outputs agree byte-for-byte with their frozen source outputs.

## 2. Model and one-step domain

Counts are nonnegative integers. All twelve channels are retained, with rates `1,A,a2,AC,a2,AD,a2,AE,AE,2CD,CD,AB`, where `a2=A(A-1)`. Their A increments are all ±1; `|ΔL|<=1` and `|ΔE|<=1`. Thus `|Δl|<=1/T`, `|Δe|<=κ=T^-3`. Inactive channels must not be treated as actual endpoint jumps.

For a current state satisfying the padded cone, every point on every active straight jump segment has

`l_segment >= l-1/T >= g(e+κ)^2 >= g e_segment^2`,

`l_segment <= l+1/T <= H(e-κ)^2 <= H e_segment^2`.

The last comparisons use positive e. The lower e condition guarantees `e_segment>=e0-κ>=1` in the fixed-3 source. This verifies padding, including crossing endpoints; it does not guarantee that the endpoint remains in the **padded** pre-stop domain. B and any A count gates are pre-stop conditions, not terminal claims.

The weighted estimates themselves need only the specified current-state inequalities and positive exit E, not padded cone invariance. In the addendum, `E>=m>=8` already gives `E_exit>=7`; its stated `e0>κ` is another sufficient positivity condition. Any proposed example `m=ceil(T^3 e0)` must still satisfy `m>=8` (or `>=100` for the numerical gate).

## 3. Exact finite increments and the fixed coefficient 3

Write `φ=e^-p`, `ψ=e^(1-p)/(p-1)`, and `K=a2(A-1)+2CD(A+1)`. Directly summing the channels gives

`GA=1-A-3a2+A(C+D)+3CD-AB`,

`G(Aφ)=φ GA+K d_+φ+2A^2 E d_-φ`,

`G(T^3ψ)=-(a2+2CD)α_++2AE α_-`.

The second identity is an exact endpoint product rule. In particular the two backward-E channels contribute `(A+1)AE d_-φ+(A-1)AE d_-φ=2A^2E d_-φ`; the signs are not obtained by replacing E with a deterministic trajectory. Integer counts ensure `K>=0`: at A=0 or 1 its falling-factorial part is zero, and at A>=2 it is nonnegative.

Let `r=1/E=κ/e<=1/(4p)`, with real p>1. Forward integration bounds `-d_+φ<=pφ/E`. Backward integration gives

`d_-φ <= (pφ/E)(1-r)^(-p-1) <= 2pφ/E`,

because Bernoulli's inequality yields `(1-r)^(p+1)>=1-(p+1)r>=1/2`. Similarly `(1+r)^(-p)>=1-pr>=3/4`, hence `3φ/4<=α_+<=φ`; and `(1-r)^(-p)<=4/3<=2`, hence `φ<=α_-<=2φ`. These are genuine finite-step bounds for all real p>1, not only the integer p in the exact tests.

For `W=Aφ+3T^3ψ`, discard the nonpositive `-Aφ`, `-3a2φ`, `K d_+φ`, and `-3a2α_+`. The remaining CD coefficient is `3φ-6α_+<=-3φ/2`; the backward weight/storage costs are at most `4pA^2φ+12AEφ`. Therefore

`GW <= φ[1-AB+A(C+D)+4pA^2+12AE]-(3/2)CDφ`.

If `C+D+4pA+12E<=B/2` holds at every pre-stop state, this is at most `φ-(AB/2)φ-CDφ`. There is an unused `-(1/2)CDφ` margin. The sufficient parameter condition is valid since `C+D<=2L<=2Hν^2N`, `A<=εN`, `E<=νN`, and `B>=cN`.

**Gate convention:** the literal statewise absorption gate is not a consequence of its truth at entrance alone. Either its sufficient parameter condition holds on the entire stopped domain, or failure of the literal gate must be included in the physical stop. This is the operative reading of the source's statewise premise; no propagation of it is received here.

## 4. Exact p=2 coefficient tradeoff

For p=2, direct finite algebra gives

`α_+/φ=E/(E+1)`, `α_-/φ=E/(E-1)`,

`E d_-φ/φ=D(E)=E(2E-1)/(E-1)^2`.

The first ratio increases with E; the second and D decrease for E>1. Explicitly `D'(E)=(1-3E)/(E-1)^3<0`, and

`5/2-D(E)=(E^2-8E+5)/(2(E-1)^2)>=0` for integer E>=8.

Thus the specified a,b,d are valid at every pre-stop E>=m, including m=8. Rewriting the exact A drift as

`GA=1+2A-5A^2+2AL+3CD-AB`

retains the needed negative quadratic coefficient. With `W_k=Aφ+kT^3/e`, the exact generator has the same product terms with 3 replaced by k. After the nonpositive forward terms are discarded it is bounded by

`φ{1+A[2+2L+2kbE-B]+(2d-5)A^2}-(2ka-3)CDφ`.

Hence `σ=2ka-3>0`, `θ in (0,1)`, and `2+2L+2kbE<=(1-θ)B` give exactly

`GW_k<=φ-θABφ-σCDφ`.

No separate A cap has entered; only the count identity `A<=L` will be used in jump/bracket estimates. At finite m, `k>3/2` **alone is insufficient**: one must have `k>(3/2)(1+1/m)`, exactly as the addendum states. The finite `2/N` term in its sufficient parameter gate cannot be dropped.

For `k=8/5,m=100,θ=1/10`, the constants are exactly `σ=17/101`, `b=100/99`, `d=19900/9801`. Under the stipulated ratio gates and B>=100,

`(2+2L+2kbE)/B <= 1/50+1/5+64/99=4289/4950<9/10`.

There are actual admissible lattice states: `(A,B,C,D,E)=(30,1000,70,70,200)` has `L/B=1/10`, `E/B=1/5`, and E>=100. This demonstrates nonvacuity of the algebraic gate, not dynamic reachability. A growing-cone example is also possible with `T=10,N=100000`, state `(3000,100000,7000,7000,20000)`, `e0=2,c=1,ν=1/5,g=2,H=3`: the padded L/E cone and the sufficient tradeoff parameter gate both hold. No separate A cap is needed for this example's tradeoff estimate.

## 5. Jumps and compensated bracket

For the eight E-preserving channels, `ΔW=±φ`. The four E-changing channels give, in order `2A→AE,CD→AE,AE→2A,AE→CD`,

`-φ+(A-1)d_+φ-kα_+`,
` φ+(A+1)d_+φ-kα_+`,
` φ+(A+1)d_-φ+kα_-`,
`-φ+(A-1)d_-φ+kα_-`.

These include crossing jumps. The scalar bounds above give `|ΔW_p|<=[7+2p(A+1)/E]φ` for fixed 3. For p=2 they give `|ΔW_k|<=[1+kb+d(A+1)/E]φ`; here `d>=2` and b>=1 dominate the forward increment as well. The cone gives `A/E<=L/E<=Hν`, while `1/E<=κ/e0` or `1/m`. Thus the stated J and deterministic j are valid.

Every reaction changes A by ±1, so the sum of all rates equals the A bracket. For fixed 3, absorption implies `3A+C+D+2E<=B/2`; using `a2<=A^2` and B>=1 gives the claimed looser bound `q_A<=1+3AB+3CD`. Therefore `q_W<=J_p^2 φ^2(1+3AB+3CD)`. In particular the actual AB↔CD contribution is exactly `(AB+CD)φ^2`.

For the tradeoff, exact summation gives

`q_A=1+AB+3CD+A^2-2A+2AL+2AE <=1+AB+3CD+A(3L+2E)`.

The last inequality uses A<=L and A>=0. Since kb>3/2,

`3L+2E <= (3/2)(2L+2kbE) <= (3/2)(1-θ)B`.

This proves the stated `C_B=1+(3/2)(1-θ)` bound. Separate admitted ratios yield `C_B=1+3r_L+2r_E`. At the numerical gate this is `17/10`, hence `C_Q=max(17,303/17)=303/17`. No upper B bound is used.

## 6. Positive storage, localization, and the actual probability bound

Both storages are nonnegative at every admitted state and actual exit endpoint with positive E. There is no subtraction of a terminal quantity of unknown sign. Total molecule count increases only through rate-one immigration and otherwise stays constant or decreases. On a bounded time interval it is bounded by initial count plus the immigrant count; all reaction rates are then bounded by a polynomial in that finite count. This proves nonexplosion and supplies ordinary localization/integrability. It does not say the reaction counts are conditionally Poisson after the path-dependent intensity has been observed.

With the actual compensated jump martingale M, the drift inequalities imply

`W(t∧τ)+Q(t∧τ) <= W(0)+∫_0^(t∧τ)φ ds+M(t∧τ)`.

Taking stopped expectations, localizing and applying Fatou gives `E Q<=W(0)+STφ0` for a fixed admitted initial state. For random entrance states the statement is conditional on the entrance sigma-field (or one takes expectation of the right side). The source/capture/fast-A expectation bounds follow immediately from the actual integrands and B>=cN.

The integral Q is continuous, so stopping at its first hit of Qbar creates no overshoot. At that hit before or at the physical horizon, nonnegative W forces `M>=Qbar-D=x`. Before the additional stop,

`<M><=J^2φ0[STφ0+C_Q Qbar]`,

where fixed 3 uses `C_Q=6`. This follows from `φ^2<=φ0φ` and, respectively, `3AB+3CD<=6(AB/2+CD)` or `C_B AB+3CD<=C_Q(θAB+σCD)`.

For jump size at most j, the standard jump exponential-supermartingale estimate, derived from `exp(u)-1-u <= u^2/[2(1-u/3)]` for 0<=u<3, gives

`P(sup M>=x, <M><=v)<=exp[-x^2/(2(v+jx/3))]`.

This directly proves the sources' one-sided bound, without factor two. It uses predictable intensities of the actual chain, not a frozen-fiber law or conditional-Poisson assumption. Using a hitting event including equality with the terminal horizon removes any tie convention; the printed strict-before event is weaker and still yields the asserted non-strict occupation ceilings.

## 7. Uniform scaling and size conditions actually received

For fixed p>=2, the initial upper cone gives

`D_p<=HT e0^(2-p)+[3T^3/(p-1)]e0^(1-p)+ST e0^-p`.

For 1<p<2, `A/E<=Hν` gives the alternative bound printed in the source. For fixed 3, with T>=1 and all admission constants fixed, p>1 fixed and e0 bounded below as required, a deterministic `D_p<=K T^3` follows. Therefore expected fast-A occupation is at most `2K T^-2/c`, and at `Qbar=2K T^3` the good-event bound is `4K T^-2/c`; source occupation is at most `2K T^3`. These claims are about the entire **stopped** growing e-range.

For the tradeoff, set `K=H+k/e0+S/e0^2`. Then `D_k<=KT^3` for T>=1. A convenient deterministic ceiling gives expected occupation at most `K T^-2/(θc)`, good-event occupation at most `2K T^-2/(θc)`, and source occupation at most `2KT^3/σ`. Uniform constants require c and e0 bounded away from zero, bounded H,S,k, and θ,σ bounded away from zero. With fixed m=100 the numerical gate has such constants. If k tends to 3/2 or θ tends to zero with T, these uniform conclusions do not follow without separately controlling the resulting constants.

For the choice `Qbar=2D`, an order-T^3 exponent additionally requires `D` of order T^3 and bounded deterministic J,φ0 and bracket coefficients. This is explicitly qualified in the fixed-3 source. At entrances with e of order T^2, actual D can instead have order T, so the same adaptive threshold need not have a T^3 exponent. A deterministic ceiling `Dbar=KT^3` with `Qbar=2Dbar`, `x>=Dbar`, and the corresponding bracket does give an order-T^3 exponent under the fixed-constant assumptions. Do not mix the actual D, its ceiling, and the lower martingale margin inconsistently.

For p>=2, `e^-p<=e0^(2-p)e^-2` holds pathwise before the stop, so one p=2 budget controls all such weighted integrals on the same good event. The constants may depend on p; there is no uniform-in-p bound asserted without controlling `e0^(2-p)`.

Finite-size restrictions remain literal: the fixed-3 bounds need `T^-3/e0<=1/(4p)`, `e0-T^-3>=1`, nonempty admitted state and `e0<=νT^2`; the addendum needs its m/σ/θ/positivity restrictions and full parameter gate including `2/N`. These are not asymptotic decorations.

## 8. Defects, conventions, and exclusions

No blocking algebraic or stochastic-calculus defect was found. `DEFECTS_AND_QUALIFICATIONS.json` records the nonblocking receiving conventions: admitted entrance; pointwise gate or its exit; actual exit endpoints; conditional random-entrance interpretation; uniform constants; correct variance/margin with a deterministic ceiling. The existing proof is received only under these explicit premises.

This audit pays actual weighted AB and CD compensators and fast-A occupation. It does not pay any physical/domain exit, prove the process reaches an admissible entrance or the moderate ratios, bound the weighted imbalance integral, or turn the result into a clearance/clock/global theorem. In particular `Z^2` may be of order L^2 on the admitted cone. The claimed source-time occupation is not a substitute for that missing imbalance bound.

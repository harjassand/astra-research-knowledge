# Exact independent receipt: actual inverse-cubic progress

Reviewed source: `../ACTUAL_INVERSE_CUBIC_PROGRESS.md`, SHA-256 `d0a69858857cb54b2127fd7b79204bc9f0f2529eaae67040ba052dbd24d62719`.

**PASS, conditional actual stopped-domain time budget. No repair required.** The full-generator identities, integer/source inequalities, finite-jump Taylor bound, scalar constant, globally positive extension, stopped expectation, target/admission union, and entrance scaling are correct. This is not admission, target reachability without an admission receiver, a clearance theorem, a CLT, or a computational complexity/CDF claim.

## 1. Literal twelve-channel check

Use coordinate order `(A,B,C,D,E)`. The twelve rates, in the source's reaction order, are

`1,A,A(A-1),AC,A(A-1),AD,A(A-1),AE,AE,2CD,CD,AB`.

For `U=E-A/2`, the respective marks are

`-1/2,+1/2,+1/2,-1/2,+1/2,-1/2,+3/2,-3/2,-1/2,+1/2,-1/2,+1/2`.

Summing rates times marks and squared marks gives exactly the displayed `GU` and `q_U`. The sole coefficient-two channel is `CD->AE`; all three `2A` rates use the falling factorial. In particular the `AE->2A` and `AE->CD` marks are `-3/2` and `-1/2`: both E-consuming channels are retained. `U` and `E` are not assumed monotone.

## 2. Geometry and drift certificate

Write `L=A+(C+D)/2`, `Z=C-D`. Then

`CD=(L-A)²-Z²/4>=81L²/100-L²/400=323L²/400>=4L²/5`.

This uses `0<=A<=L/10` and `|Z|<=L/10`, not a supplied equilibrium. Hence `AL<=L²/10<=CD/8`. Rewriting the exact drift in terms of `L` gives the useful nonnegative-slack identity

`GU-AB/10-CD/4`
` = [(5/2)A²-2A]+2A(B/5-E)+A²+(CD/8-AL)+(CD-4)/8`.

Each term is nonnegative on the admitted count domain. The first term is nonnegative for every integer `A>=0`; the last uses `CD>=4`. Thus `GU>=AB/10+CD/4>0`.

The integer assumption matters: `(5/2)A²-2A` is not nonnegative for all real `A>=0`. The source applies it only to actual integer counts, correctly.

## 3. Bracket certificate

The stated gates imply `A<=B/100`, `C+D<=B/5`, and `E<=B/5`. The exact bracket comparison can be certified by

`(83/100)AB+(13/16)CD-q_U`
` = (CD-4)/16 + A(B-100)/400`
`   +(11A/4)(B/100-A+1)`
`   +(A/4)(B/5-C-D)+(5A/2)(B/5-E)`.

Every term is nonnegative. The final comparison follows from

`9(AB/10+CD/4)-[(83/100)AB+(13/16)CD]`
` = (7/100)AB+(23/16)CD>=0`.

Consequently `q_U<=9GU` for this same actual generator and pre-stop domain. No conditional martingale or favorable-history substitution occurs.

## 4. Every finite jump and the inverse-cubic drift

For `f(u)=u^-3`, `f'(u)=-3u^-4`, `f''(u)=12u^-5`. At an admitted state `u>=100`, every actual mark has `|h|<=3/2`; every point of its segment is at least `u-3/2>=98.5`. Taylor's theorem therefore gives

`f(u+h)-f(u)<=-3h/u^4+6h²/(u-3/2)^5`.

The independent checker additionally verifies this inequality for **all** `u>=100` and each of the four possible mark values `h in {-3/2,-1/2,1/2,3/2}` by exact algebra: after writing `u=100+z`, each rational gap has a positive denominator and a numerator with nonnegative polynomial coefficients for `z>=0`. This is not merely a finite grid check.

Summing over all twelve channels gives

`Gf<=-3GU/u^4+6q_U/(u-3/2)^5`
`   <=(GU/u^4)[-3+54u^4/(u-3/2)^5]`.

The scalar ratio `54u^4/(u-3/2)^5` is decreasing for `u>3/2`, since its logarithmic derivative is `-(u+6)/(u(u-3/2))<0`. At `u=100` its exact value is

`172800000000/296709280757<1`.

Equivalently the source's integer comparison has positive margin

`50*197^5-27*200^5=6195464037850`.

Because `GU>0`, this proves `Gf<=-2GU/u^4`. Next, every sign in the deterministic comparison chain is correct:

`Gf<=-CD/(2u^4)<=-(2/5)L²/E^4<=-1/(10N²)`.

The first inequality uses `GU>=CD/4`, the second uses `0<u<=E` and `CD>=4L²/5`, and the last uses `R=E²/(NL)<=2`. Denominators are nonzero on the admitted domain: `u>=100` implies `E>0`, and `CD>=4` implies `L>0`.

## 5. Extension and actual stopped duration

The extension `Psi=10N²/max(U,50)^3` is globally positive and bounded by `10N²/50³`, including states with negative `U`. Its possible nonsmoothness at `U=50` is irrelevant: every admitted state and every one-step segment has `U>=98.5`. Therefore the finite-jump generator calculations are unchanged and `GPsi<=-1` before the actual stop.

Assume a fixed finite initial state in the admitted domain, a declared actual target stopping time `tau_E`, and the first other failure time `sigma_adm` containing every required gate. Put `sigma=tau_E wedge sigma_adm`.

There is no hidden explosion issue in applying localized Dynkin. All internal reactions conserve total particle number, while immigration has unit rate and true death lowers that number. On every finite horizon, total count is bounded pathwise by its initial value plus the unit-rate immigration Poisson count. This bound has every finite polynomial moment; the twelve rates are at most quadratic in total count. It therefore gives both nonexplosion and the finite-horizon integrability needed for the bounded observable and its stopped generator.

For finite `t`, localized Dynkin and the drift inequality give

`0<=E[Psi(X_{sigma wedge t})]<=Psi(x)-E[sigma wedge t]`.

Letting `t` increase to infinity yields `E[sigma]<=Psi(x)` and in particular `sigma<infinity` almost surely. This conclusion concerns target **or admission failure**, not target alone. For `d>0`, Markov's inequality gives `P(sigma>d)<=Psi(x)/d`.

The actual event inclusion is

`{tau_E>d} subset {sigma>d} union {sigma_adm<=min(tau_E,d)}`.

Thus a separately received admission-failure bound gives exactly the source's target tail inequality. Simultaneous adverse exits, including at the deadline, lie in the second event. No independence is needed. Exit states are globally evaluated, never reset or deleted.

## 6. Entrance scaling and its extra hypotheses

For `T=N^(1/5)`, actual entrance `E=e0 T³`, and `U>=.99E`,

`Psi(x)<=[10/(.99³)]T/e0³<11T/e0³`.

The exact integer check is `11*99³-10*100³=673289>0`. With `d=epsilon T`, the stopped-duration contribution is therefore at most `11/(epsilon e0³)`, as stated.

The sufficient lower-ratio condition is also correct: `R>=1/2` gives `L<=2E²/N`, hence `A/(2E)<=L/(20E)<=E/(10N)<=1/100` when `A<=L/10` and `E<=N/10`. This proves `U>=.99E`.

It does not follow from the basic upper-`R` gate alone. For example `(A,B,C,D,E)=(400,40000,3600,3600,1000)` with reference `N=48600` satisfies every basic pre-stop gate, yet `U/E=0.8`. The source explicitly warns of this scope distinction, correctly.

## Scope and outcome

No repair was found necessary. The receipt accepts a conditional physical-time-to-target-or-failure component only. Acquiring the cone, imbalance/A caps, count margins, admission probability, macro-target exit-state handoff, and final removal-time continuation remain separate operations. Earlier accepted files and the reviewed source were not changed.

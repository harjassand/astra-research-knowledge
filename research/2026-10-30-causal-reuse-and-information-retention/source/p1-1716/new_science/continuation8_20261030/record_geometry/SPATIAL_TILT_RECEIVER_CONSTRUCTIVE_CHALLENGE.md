# Constructive challenge of the corrected spatial-tilt receiver

30 October 2026. This note checks the root proposal communicated in this round, not an unseen final root manuscript. It supplies the ratio-continuity and weak-PDE arguments needed for that proposal. No further numerical fixture is used.

## 1. Interface inherited from the actual-current correction

Use the shared-bit ring with fixed `0<=alpha<1`, `c=s/2`, actual uniform canonical reference, initial density ceiling `exp(O(N))`, interior conserved mass, and clock window

\[
N\gamma_N\to\infty,\qquad \gamma_N/N\to0.
\tag{1}
\]

The companion `INVERSE_ACTIVITY_AND_WEIGHTED_CORRECTOR.md` proves that, for every smooth deterministic current test `H`, the actual weighted current is exponentially equivalent at speed `N` to

\[
K_H(N^2t)/N^2+c\int_0^tS_H(\eta_{N^2v})dv,
\quad S_H=\sum_iH_i\delta_i,
\tag{2}
\]

where `K_H` has native increments `d_H=H_i delta_i-alpha u F_H`, compensator `cS_H`, and `F_H=A_H/A`. The result also holds under arbitrary predictable native weak tilts bounded by `K/N`, with unchanged clock. Fixed `alpha<1` is needed by the inverse-activity proof; it is not uniform as native ellipticity vanishes.

For fixed smooth bounded `E(t,x)`, define the mathematical comparison law

\[
r_i^E=r_i\exp[d_E/N],
\qquad d_E=E_i\delta_i-\alpha uF_E.
\tag{3}
\]

Since `|F_E|<=||E||`, this is a permitted bounded weak tilt. Its density process need not be reversible and `d_E` need not be antisymmetric under an individual native exchange. Neither property is required for the likelihood transfer or martingale drift expansion. No actual actuator supplying (3) is assumed.

The actual and comparison processes start from the same warranted microscopic initial law. The initial ceiling is used for superexponential estimates only; it does not transfer a finite-action lower probability from a different initializer.

## 2. The exact drift and its error

Under (3), the process called `K_H` in (2) is a martingale plus drift

\[
\sum_i r_i(e^{d_E/N}-1)d_H
=\frac1N\sum_i r_i d_Hd_E+O_{E,H}(N^{-1}).
\tag{4}
\]

The last error follows from bounded `d_H,d_E`, total native rate `O(N)`, and a second-order Taylor remainder. All these are physical finite-state bounds, uniform in configuration and the bit.

The exact covariance algebra is

\[
\sum_i r_i d_Hd_E
=c\left[A_{HE}-\alpha^2\frac{A_HA_E}{A}\right]
+c\alpha u[S_{HE}-F_ES_H-F_HS_E].
\tag{5}
\]

For smooth tests the last bracket is uniformly `O(1)`, by discrete summation by parts. It is divided by `N` in (4), so no additional phase estimate is needed for it.

The tilted martingale part of the normalized current has bracket `O(1/N)` and bounded vanishing jumps. Thus only occupation replacement of the first line in (5) remains.

## 3. The quotient in the covariance is Lipschitz at zero activity

This is a useful stronger observation than a denominator cutoff. For bounds `L_H,L_E`, let

\[
\mathcal C=\{(a,b,e):a\ge0,\ |b|\le L_Ha,\ |e|\le L_Ea\}.
\]

On this convex cone define

\[
\Phi(a,b,e)=\begin{cases}be/a,&a>0,\\0,&a=0.\end{cases}
\tag{6}
\]

It is globally Lipschitz on the cone. Away from zero its partial derivatives have absolute bounds `L_H L_E`, `L_E`, and `L_H`; the line segment between two cone points stays in the cone. Continuity at its vertex follows from `|Phi|<=L_H L_E a`. Hence

\[
|\Phi(a,b,e)-\Phi(a',b',e')|
\le L_HL_E|a-a'|+L_E|b-b'|+L_H|e-e'|.
\tag{7}
\]

Use `a=A/N`, `b=A_H/N`, `e=A_E/N`. Their occupation replacements converge in time `L1` to `2C_rho`, `2B_H`, `2B_E`, where

\[
C_\rho=\int\chi(\rho),\qquad B_H=\int\chi(\rho)H.
\]

The admissibility cone holds both microscopically and after replacement. Equation (7) therefore gives convergence in time `L1` of the nonlocal covariance term, with zero convention if `C_rho=0`:

\[
\frac{A_HA_E}{AN}\longrightarrow
2\frac{B_HB_E}{C_\rho}.
\tag{8}
\]

This step does not require a lower bound on the activity or on `C_rho`. Under each finite-energy limiting density path, `C_rho>0` for almost every time anyway, by the connectedness and `H^1` argument in the companion inverse-activity proof.

One may formulate the receiving proof with fixed spatial mollifiers first. Occupation replacement supplies the time `L1` errors, and (7) transfers them to the nonlinear covariance without changing the order of limits. It would be incorrect to infer (8) merely from a typical canonical mean of `A`.

## 4. Identified PDE and the needed energy class

Equations (2), (4), (5), and (8) identify every subsequential density/current limit as

\[
j=-c\partial_x\rho+s\chi(\rho)[E-\alpha^2\bar E_\rho(t)],
\qquad
\partial_t\rho+\partial_xj=0,
\tag{9}
\]

where

\[
\bar E_\rho(t)=\frac{\int\chi(\rho_t)E_t}{C_{\rho_t}}
\tag{10}
\]

at times with positive denominator. It can be set to zero on the remaining null set. Always `|bar E_rho|<=||E||_infinity`.

The companion density exponential tightness and finite-test energy estimate transfer to (3) by `E Z_E^2<=exp(C_E N T)`. Thus the receiving limit has `rho in L2([0,T],H1)` and `0<=rho<=1`. The forcing in (9) is bounded, so `rho_t` belongs to `L2([0,T],H^{-1})`. This is the usual energy class in which the following comparison and difference tests are legitimate. Existence of a subsequential weak solution comes from this actual stochastic tightness argument; it need not be supplied by an unproved nonlocal PDE existence assertion.

## 5. Positivity for the flat interior initializer

For the root full-action receiver, take the actual limiting initial profile `rho_0=m in (0,1)`. More generally assume `delta_0<=rho_0<=1-delta_0`. Treat the bounded measurable scalar `bar E_rho(t)` in a given weak solution as a prescribed time coefficient. The spatial derivative of the effective field is exactly `partial_x E`; no derivative of `bar E_rho` is taken.

Let `L=||partial_x E||_infinity` and `v(t)=delta_0 exp(-sLt)`. The spatially constant `v` is a subsolution because

\[
v'=-sLv\le-s\chi(v)\partial_xE.
\tag{11}
\]

The symmetric function `1-v` is a supersolution. Weak comparison follows by applying the positive-part energy test to the difference from a sub/supersolution: the flux is Lipschitz in `rho`, diffusion is the fixed positive constant `c`, and the spatial derivative of its prescribed field is bounded. The sign of the subsolution defect is the one in (11); a Gronwall estimate controls the Lipschitz flux term. Consequently

\[
\delta_T\le\rho_t(x)\le1-\delta_T,
\qquad \delta_T=\delta_0e^{-sLT}>0,
\tag{12}
\]

almost everywhere on the interval. This argument is not a maximum-principle assertion for an arbitrary rough density-dependent field: the nonlocal term is spatially constant, which is the essential simplification.

If the initial profile touches zero or one, (11) supplies no positive constant. The full-action receiver may simply retain its flat interior start. A stronger initial-profile theorem would require an explicit positive-time regularization argument.

## 6. Uniqueness of the weak receiver

Let `rho` and `tilde rho` solve (9) with the same flat interior initializer. By (12), both denominators in (10) are at least `C_0=delta_T(1-delta_T)`. Since `chi` is Lipschitz with constant one,

\[
|\bar E_\rho-\bar E_{\widetilde\rho}|
\le\frac{2\|E\|_\infty}{C_0}\|\rho-\widetilde\rho\|_{L1}
\le\frac{2\|E\|_\infty}{C_0}\|\rho-\widetilde\rho\|_{L2}.
\tag{13}
\]

The flux map `F(rho)=chi(rho)(E-alpha^2 bar E_rho)` is therefore Lipschitz from this subset of `L2` into `L2`, with a finite constant `C_(E,alpha,delta_T)`. For `w=rho-tilde rho`, the energy identity gives

\[
\frac12\frac d{dt}\|w\|_2^2
\le-\frac c2\|\partial_xw\|_2^2
+\frac{s^2 C_{E,\alpha,\delta_T}^2}{2c}\|w\|_2^2.
\tag{14}
\]

The weak energy regularity above justifies this test and the common initial trace. Gronwall proves uniqueness. Therefore the actual comparison process converges in probability to the uniquely identified deterministic solution of (9), together with its full integrated current. Current tightness uses the proved weighted-current replacement and the exact ring bound `||W_t^N||_TV<=|Q_N(t)|+1`, as in the accepted round7 argument.

This closes the proposed corrected-tilt LLN for a fixed smooth deterministic `E` and a flat interior initial profile, conditional on the companion weighted-current proof. The proof does not require the tilted generator to be reversible, a tilted invariant law, or a uniform microscopic activity lower bound.

## 7. The inverse field and action checks

For a smooth desired path with `rho` bounded away from zero and one, continuity, and initial profile `m`, put `A=j+c rho_x` and `C=int chi(rho)`. The field

\[
E=\frac{A}{s\chi(\rho)}
+\frac{\alpha^2}{1-\alpha^2}\frac{\int j}{sC}
\tag{15}
\]

satisfies (9), because `int A=int j` and
`int chi E=(int j)/[s(1-alpha^2)]`. The fixed-`alpha<1` restriction is essential.

The exact log likelihood is expressed by the base martingale `K_E` and its quadratic compensator. In the limit it is

\[
\int jE-c\int\rho E_x
-\frac s2\int\left[\chi(\rho)E^2
-\alpha^2\frac{(\int\chi(\rho)E)^2}{C}\right]dt,
\tag{16}
\]

with space integration in the first two terms. The sign of the heat term is as displayed: integration by parts turns the linear part into `int (j+c rho_x)E`. Substitution of (15) gives the proposed action

\[
\frac1{2s}\int_0^T\left\{
\int\frac{(j+c\rho_x)^2}{\chi(\rho)}
+\frac{\alpha^2}{1-\alpha^2}\frac{(\int j)^2}{C}\right\}dt.
\tag{17}
\]

The extra term is jointly convex in `(rho,j)`: `x^2/y` is convex and nonincreasing in positive `y`, while `C_rho` is concave in `rho`. Spatial convolution preserves `int j` and increases `C_rho`; time convolution uses the same perspective convexity. Mixing with the flat path and past-only time smoothing therefore has the same cost-lowering properties as in the accepted round7 local action, once its exact topology and initial trace are carried over.

These observations validate the proposed receiving mechanism and its action algebra. They are not a hash-pinned review of the future root full-LDP manuscript. That manuscript must still state the finite-test upper-bound passage, exponential tightness, its smooth approximation, and the initial-law quantifiers explicitly. A randomly initialized canonical density ensemble has an additional static initial cost for a full spatial LDP; the fixed-profile theorem cannot silently be transferred to it.

## 8. Remaining boundary

There is no identified receiver gap in the positive-clock proposal at the stated interface. The zero-external-clock receiver and the singular full spatial action at `alpha=1` remain unproved. The primary mathematical techniques remain conventional martingale, exclusion replacement, and parabolic energy arguments. The candidate addition is the actual event-memory physical supplier and the explicit geometry it gives in this particular family, with priority unresolved.

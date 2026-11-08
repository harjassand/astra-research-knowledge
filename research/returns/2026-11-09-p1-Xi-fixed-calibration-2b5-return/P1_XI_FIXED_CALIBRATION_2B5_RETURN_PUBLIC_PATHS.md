# P1 Xi completed return

Source: https://chatgpt.com/c/6af0e2d0-1db8-83ec-9610-24dde8eedecf
Model at dispatch: GPT-6 standard, Extra High. Turn: 2b531b24-7b54-484e-9cd3-4a4e2f1ebb2d; response: 674219ad-ed39-4f19-8233-cd7b394737f7. Completion: 2026-11-08T22:56:53.517Z. No producer ZIP visible.

Capture note: the source reader limited the raw response to 20,000 characters. The final section below is transcribed from the visible rendered response; its original Markdown/LaTeX source was unavailable. Text preceding that section is the source-reader response.

## Actual prompt

Resolve a NEW FULL robustness question using the accepted8EB+BCA deterministic fluid controller: can one nominal polynomial-resource programme work at a FIXED relative calibration tolerance, independent of K and viscosity? Both previous full constructions stand at their stated scopes under the correctness assumption; no reproof or independent-verification assignment. You own all methods, representations, source order and framing.

On unit T3 keep EXACTLY
 partial_t u+P[(u.dot.grad)u]=nu*Delta u+P[(b_actual(t,x).dot.grad)u],
 divu=0, meanu=0.
For EVERY rational nu>0,K>=1 output ONE deterministic nominal programme consisting of finitely many DISJOINT pulse intervals, scalar nonnegative rational-polynomial C2 envelopes f_l(t) supported on those intervals, nonzero integer frequencies p_l and nonzero rational vectors a_l with a_l.dot.p_l=0. The nominal field is sum_l f_l(t)*a_l*cos(2*pi*p_l.dot.x).

Fix rho0=1/1024. The SAME programme must succeed for EVERY STATIC calibration choice, unknown to the compiler,
 b_actual=sum_l f_l(t)*theta_l*(a_l+e_l)*cos(2*pi*p_l.dot.x+phi_l),
 1-rho0<=theta_l<=1+rho0,
 e_l.dot.p_l=0, |e_l|2<=rho0*|a_l|2,
 phi_l arbitrary in[0,2*pi).
The errors may be independent between pulses but remain constant during each pulse. No feedback, measurements, stochastic success event or knowledge/oracle/encoding of these unknown real parameters is supplied. Exact frequency indices and envelope timing are part of this stated model; arbitrary time-dependent/spatial hardware errors are not assumed covered.

For EVERY smooth mean-zero divergence-free u0 with ||u0||H3<=K and EVERY admissible calibration, require unique GLOBAL strong evolution, classical for positive time, and common rational M,T with
 sup_(t>=0)||u(t)||H3<=M, ||u(T)||H1<=nu/4,
 b_actual=0 outside[0,T].
Use ||v||Hs^2=sum_k(1+4*pi^2|k|^2)^s|v_hat(k)|^2. No increased viscosity/damping, per-profile/per-calibration programme or exceptional initial states.

Retain the FULL polynomial resource contract. For COMPLETE input length B and S=2+K+nu+nu^-1, fixed computable absolute C,d must bound synthesis/certification BIT work, nominal description/coefficient/breakpoint heights, pulse/mode counts and degrees by C(B+1)^d; and T,M,frequencies, inverse nonzero piece durations, actual-field sup||b||W3infinity, sup||partial_t b||W2infinity and integral_0^T(||b||W3infinity^2+||partial_t b||W2infinity^2)dt by C*S^d, UNIFORMLY over calibration. All finite arithmetic/precision/actuation/output costs paid. No PDE/regularity/real oracle or uncertified search. A full negative must address this model, not only your current single shear or small-critical-norm proof route. Practical hardware advantage is not presumed.

Accepted capital, credited once:
*8EB full all-initial native-velocity controller: exact Leray Fourier ladders, both Jacobi polarisations with root bonds1 and |k.dot.m|/(|k||m|), quantitative return-amplitude decay/finite-frequency error, H3-tail control and critical Fourier entry. Small F_-1<nu/4 gives global unforced continuation.
*BCA actual new polynomial closure: derivative directions parallel to a and perpendicular to both a,p commute with the shear; only the p-direction yields a strictly lower triangular four-group H3 hierarchy, including viscous dissipation and nonlinear energy commutators. Nilpotence replaces exponential Gronwall by L=(1+2^24*s*A*(1+P1)^3)^3, paying the full nonlinear short pulse and all polynomial resources. Its explicit C=2^(10^8),d=50000 are valid coarse bounds, not practical values.
*Lei-Lin1203.2699v1 Thm1.1/Section2 is prior R3 critical-Fourier small-data machinery; your matched torus/H3 estimate stands. Earlier stochastic-velocity/per-initial and vorticity/measure-exceptional source contracts are unchanged, not stronger robust deterministic premises.

ROOT-checked scope warning, not a full negative: your generic single-shear vectors use m=(1,Q,Q^2), a_3=Q^3-Q. The transverse perturbation e=(0,Q*a_3,-a_3) has e.dot.m=0, |e|/|a|<=2/Q^3, and (a+e).e3=0. It leaves the k=e3 mode unmixed, so the current spectral-evacuation proof is not automatically stable at fixed relative tolerance. That invariant shear datum itself is globally regular; this does NOT refute the requested full controller.

Optional ROOT opening only: a fixed finite family of integer orthogonal pairs can cover every direction k with BOTH normalized |k.dot.m| and |k.dot.a|>=1/4; coordinate pairs cover directions with two large components, while (e_i+e_j,e_i-e_j) cover near-axis directions. This margin survives rho0 perturbations, but composing evacuations without low-frequency return/cost blowup is unconstructed. You may discard the family, the proof route and this intuition.

Pursue FULL resolution persistently. A tolerance shrinking with S, per-calibration tuning, another exactly calibrated controller or a conditional composition lemma is not the fixed-tolerance theorem.

you may use all subagents avaible
All inherited source/access/transfer/resource holds apply to every subagent, including unknown identities. EVERY failed original/transfer, including NSF10314785, OpenAI Uniform-Permanence tree, Dots/Golding-Henderson/Serre/CarloAlberto/root2410.23225v3/TR26-272/2610.00548v2/d-nb.info990289982 governingSection5 and all others, remains HELD: no retry/raw/PDF/mirror/alternate/identifying recovery/held-source injection. No attachments, extra principal/model/worker/resource/account/spending, Sol or Dots action.

## Available user-visible activity

Worked for 16m 33s

Completed hierarchical Fourier control construction and global contraction proof

I’ve found a possible way around the single-shear calibration failure: use nine fixed shear directions. Every low Fourier mode has at least one shear with a quantitative mixing margin that survives the 1/1024 perturbation.

The composition challenge is controlling modes already moved to high frequencies. I’m using a decomposition into a frequency-diagonal return operator and a small off-diagonal remainder, with each successive shear frequency chosen large enough to absorb the previous stage’s H³ bound. This avoids assuming the pulses commute.

Analyzed — Python:
```python
h=1
vals=[]
for j in range(1,10):
    n=max(16,h+11)
    ell=30+9*n
    hn=h+ell
    d=5*hn+3
    vals.append((j,h,n,ell,hn,d))
    h=hn
vals
```
Result:
```
[(1, 1, 16, 174, 175, 878), (2, 175, 186, 1704, 1879, 9398), (3, 1879, 1890, 17040, 18919, 94598), (4, 18919, 18930, 170400, 189319, 946598), (5, 189319, 189330, 1704000, 1893319, 9466598), (6, 1893319, 1893330, 17040000, 18933319, 94666598), (7, 18933319, 18933330, 170400000, 189333319, 946666598), (8, 189333319, 189333330, 1704000000, 1893333319, 9466666598), (9, 1893333319, 1893333330, 17040000000, 18933333319, 94666666598)]
```
Audited the construction
Audited pulse construction

Analyzed — Python:
```python
j,hp,n,ell,h,d=vals[-1]
maxexp = 20+max(d+6*n,3*d+4*n)
j,h,n,d,maxexp,10+d+3*n,10+2*d+2*n
```
Result: (9, 18933333319, 1893333330, 94666666598, 291573333134, 100346666598, 193119999866)

Checked controllability estimates and construction
Computed shear-stage exponent recurrence and verified Fourier resource bounds

## Response, source text through section 8

# Fixed-tolerance robustness: a nine-shear construction

**The strengthened robustness problem admits a positive construction, conditional on the accepted 8EB and BCA results.** The new ingredient is a finite family of shear directions combined with a Fourier decomposition that controls what later pulses do to frequencies evacuated by earlier pulses.

The calibration tolerance remains exactly

\[
\boxed{\rho_0=\frac1{1024}}
\]

for every viscosity, initial-data radius and pulse. It is not reduced as \(K/\nu\) grows.

The construction uses nine disjoint pulses, each containing one rational-trigonometric spatial mode and one nonnegative degree-six rational-polynomial envelope. No calibration parameters enter the synthesis algorithm.

## 1\. Nine directions robustly cover every Fourier mode

Let \(e_1,e_2,e_3\) denote the standard coordinate vectors. Fix the following nine nominal pairs \((m,a)\), where the physical frequency will be \(p=Nm\)\.

Six coordinate pairs

\[
(m,a)=(e_i,e_j),\qquad i\ne j.
\]

Three diagonal pairs

\[
(m,a)=(e_i+e_j,e_i-e_j),\qquad i<j.
\]

Every pair satisfies \(a\cdot m=0\), and

\[
1\le |a|_2,|m|_2\le\sqrt2,\qquad |a|_1\le2.
\]

**Direction-cover lemma.** For every \(k\in\mathbb Z^3\setminus\{0\}\), at least one of these pairs satisfies

\[
\boxed{
\frac{|a\cdot k|}{|a|_2|k|_2}\ge\frac14,
\qquad
\frac{|m\cdot k|}{|m|_2|k|_2}\ge\frac14.
}
\tag{1}
\]

To prove it, suppose first that two coordinates of \(k\) have magnitude at least \(|k|_2/4\)\. Choose the corresponding coordinate pair.

Otherwise, one coordinate has magnitude at least \(\sqrt{7/8}|k|_2\), while either other coordinate has magnitude below \(|k|_2/4\)\. A diagonal pair using the dominant coordinate then has both normalized dot products at least

\[
\frac{\sqrt{7/8}-1/4}{\sqrt2}>\frac14.
\]

This covers every nonzero real direction, not just integer directions.

Now take any admissible calibration

\[
\widetilde a=\theta(a+e),\qquad
|e|_2\le\rho_0|a|_2,\quad
e\cdot m=0,\quad
1-\rho_0\le\theta\le1+\rho_0.
\]

For a pair satisfying (1),

\[
\begin{aligned}
|\widetilde a\cdot k|
&\ge(1-\rho_0)
\left(|a\cdot k|-\rho_0|a|_2|k|_2\right)\\
&\ge(1-\rho_0)(1/4-\rho_0)|a|_2|k|_2\\
&>\frac{|k|_2}{5}.
\end{aligned}
\tag{2}
\]

The second dot product in (1) is unchanged. Consequently, the two Jacobi polarizations of this calibrated shear satisfy

\[
\tau_1=1,\qquad
\tau_2=\frac{|m\cdot k|}{|m|_2|k|_2}\ge\frac14.
\]

In particular,

\[
\tau_j^2\ge r,\qquad r=\frac1{32}.
\tag{3}
\]

These are absolute margins independent of \(K,\nu,k\), and the calibration.

## 2\. Arbitrary phases do not destroy the central mixing estimate

For one calibrated shear

\[
\widetilde v(x)=\widetilde a
\cos(2\pi Nm\cdot x+\phi),
\]

the exact Leray Fourier evolution starting at frequency \(k\) remains on

\[
k+jNm,\qquad j\in\mathbb Z.
\]

Its nearest-neighbour coefficients acquire phase factors \(e^{i\phi}\) and \(e^{-i\phi}\)\. The transformation of ladder coefficients

\[
w_j\longmapsto e^{-ij\phi}w_j
\]

removes those factors. Crucially, the central coefficient \(j=0\) is unchanged.

Thus the calibrated central-return estimate is independent of \(\phi\)\.

Using the accepted 8EB return-amplitude bound with the fixed spectral margin (3), a sufficiently large *polynomial* shear time \(s=s(\varepsilon)\) gives central-return norm at most \(\varepsilon/4\)\. A sufficiently large polynomial frequency multiplier \(N=N(R,s,\varepsilon)\) makes the finite-frequency Leray-projector error at most another \(\varepsilon/4\)\.

For every low frequency \(|k|_2\le R\) covered by that shear, the resulting exact central-return matrix \(C_\ell(k)\) therefore satisfies

\[
\boxed{\|C_\ell(k)\|_{\mathrm{op}}\le\varepsilon.}
\tag{4}
\]

For every other frequency and every other calibration, unitarity always supplies

\[
\boxed{\|C_\ell(k)\|_{\mathrm{op}}\le1.}
\tag{5}
\]

This is sufficient even when the nine central-return matrices do not commute. For each low \(k\), at least one factor in

\[
C_9(k)C_8(k)\cdots C_1(k)
\]

has norm at most \(\varepsilon\), while all other factors have norm at most one. Therefore

\[
\boxed{
\|C_9(k)\cdots C_1(k)\|_{\mathrm{op}}\le\varepsilon,
\qquad 0<|k|_2\le R.
}
\tag{6}
\]

## 3\. Preventing high-frequency return under later pulses

Central contraction alone is insufficient. An earlier shear creates high Fourier frequencies, and a subsequent shear might transfer some of those back to low frequencies.

The missing estimate is obtained by decomposing each exact inviscid shear propagator into

\[
\boxed{U_\ell=C_\ell+\mathcal R_\ell,}
\tag{7}
\]

where \(C_\ell\) is the frequency-diagonal central-return operator and \(\mathcal R_\ell\) contains all nonzero ladder shifts.

For a pure input Fourier mode \(k\), the calibrated ladder generator has norm bounded by \(C|k|_2\), independently of its spatial frequency multiplier \(N\)\. Nearest-neighbour propagation and the Dyson expansion imply

\[
\sum_{j\in\mathbb Z}|w_j(s)|
\le
C\sqrt{1+s|k|_2}\,|\widehat f(k)|.
\tag{8}
\]

This follows by retaining \(O(1+s|k|_2)\) ladder sites, applying Cauchy–Schwarz and \(L^2\)\-unitarity there, and bounding the remaining sites by the factorial tail of the Dyson series. All constants are uniform over the stated calibration set.

For \(|k|_2\le|p_\ell|_2/2\), every nonzero ladder shift has frequency at least \(|p_\ell|_2/2\)\. For larger input \(k\), the initial \(H^3\) Fourier tail controls the entire ladder.

The lattice estimates

\[
\sum_k(1+|k|_2)^{1/2}|\widehat f(k)|
\le C\|f\|_{H^3},
\]

\[
\sum_{|k|_2>P/2}
(1+|k|_2)^{1/2}|\widehat f(k)|
\le\frac{C}{P}\|f\|_{H^3}
\]

therefore yield the uniform off-diagonal bound

\[
\boxed{
F_{-1}(\mathcal R_\ell f)
\le
\frac{2^{24}(1+s)}{|p_\ell|_2}\|f\|_{H^3}.
}
\tag{9}
\]

Here

\[
F_{-1}(f)=\sum_{k\ne0}\frac{|\widehat f(k)|}{2\pi|k|_2}.
\]

Unlike a support-truncation argument, (9) applies to the entire infinite Fourier series of every \(H^3\) datum. It also accounts for resonant high-input frequencies whose shifted ladder could reach a low frequency.

Because \(C_\ell\) is frequency-diagonal and contractive,

\[
F_{-1}(C_\ell f)\le F_{-1}(f).
\]

Consequently, choosing the frequency multipliers successively large relative to the *previous* \(H^3\) bound lets the nine shears compose without either commuting assumptions or an uncontrolled accumulation of returned low-frequency mass.

## 4\. The complete deterministic compiler

Fix the absolute rational/integer constants

\[
J=9,\qquad C_*=2^{40},\qquad r=\frac1{32}.
\]

Given rational \(\nu>0\) and \(K\ge1\), compute

\[
\boxed{
R=\left\lceil C_*\left(1+\frac K\nu\right)\right\rceil,
\qquad
\varepsilon=\min\left\{\frac1{16},\frac{\nu}{C_*K}\right\},
}
\tag{10}
\]

and the common integer inviscid shear time

\[
\boxed{
s=\left\lceil C_*r^{-7}\varepsilon^{-5}\right\rceil.
}
\tag{11}
\]

Fix any predetermined ordering of the nine pairs in Section 1. The ordering does not depend on the input or the calibration.

Initialize

\[
K_0=K,\qquad t_0=0.
\]

For \(\ell=1,\ldots,9\), perform the following fixed sequence of exact rational computations.

First calculate

\[
\boxed{
N_\ell=
\left\lceil
C_*\left(
1+\frac{s(R+1)^2}{\varepsilon}
+\frac{J(1+s)K_{\ell-1}}{\nu}
\right)
\right\rceil,
}
\tag{12}
\]

and set

\[
p_\ell=N_\ell m_\ell,\qquad
P_\ell=\sum_{i=1}^3|p_{\ell,i}|.
\]

The polynomial \(H^3\) amplification allowance is

\[
\boxed{
L_\ell=
\left(1+2^{30}s(1+P_\ell)^3\right)^3.
}
\tag{13}
\]

Define the rational stage bounds

\[
K_\ell=8L_\ell K_{\ell-1},
\qquad
E_\ell=\nu K_\ell+C_*K_\ell^2.
\tag{14}
\]

Then compute

\[
\boxed{
D_\ell=
\left\lceil C_*
\left(
1+L_\ell^2K_{\ell-1}
+\frac{J^3K_\ell E_\ell^2}{\nu^3}
\right)\right\rceil,
\qquad
\delta_\ell=D_\ell^{-1}.
}
\tag{15}
\]

Define the active interval and the next stage endpoint by

\[
I_\ell=[t_{\ell-1},t_{\ell-1}+\delta_\ell],
\qquad
t_\ell=t_{\ell-1}+2\delta_\ell.
\]

Thus there is a strictly positive gap of duration \(\delta_\ell\) after every active pulse. All active intervals are disjoint, including at their endpoints.

Let

\[
h(z)=140z^3(1-z)^3.
\]

The nominal envelope is

\[
\boxed{
f_\ell(t)=
\begin{cases}
sD_\ell h\!\left(D_\ell(t-t_{\ell-1})\right),
&t\in I_\ell,\\
0,&t\notin I_\ell.
\end{cases}}
\tag{16}
\]

The nominal control is therefore exactly

\[
\boxed{
b_{\rm nominal}(t,x)
=
\sum_{\ell=1}^{9}
f_\ell(t)a_\ell\cos(2\pi p_\ell\cdot x).
}
\tag{17}
\]

Each envelope is nonnegative, rational-polynomial, degree six, and globally \(C^2\)\. Every frequency is a nonzero integer vector, and \(a_\ell\cdot p_\ell=0\)\.

Finally output

\[
\boxed{
M=2^{1000}K_9
}
\tag{18}
\]

and

\[
\boxed{
T=t_9+\frac{1+64K^2M/\nu^3}{\nu}.
}
\tag{19}
\]

Both outputs are rational. All nominal pulses finish strictly before \(T\)\.

## 5\. The nine calibrated inviscid stages have a uniform contraction

For each pulse, define its calibrated spatial vector field

\[
\widetilde v_\ell(x)=
\theta_\ell(a_\ell+e_\ell)
\cos(2\pi p_\ell\cdot x+\phi_\ell),
\]

and the corresponding Leray-projected operator

\[
\mathcal A_\ell w=P[(\widetilde v_\ell\cdot\nabla)w].
\]

Let

\[
U_\ell=\exp(s\mathcal A_\ell)
\]

denote its inviscid linear propagator.

The calibration constraints imply

\[
\theta_\ell(a_\ell+e_\ell)\cdot p_\ell=0,
\qquad
\left|\theta_\ell(a_\ell+e_\ell)\right|_1<4.
\tag{20}
\]

Thus the frequency-ladder and polynomial \(H^3\) estimates apply with constants independent of the unknown parameters.

For a good pair and \(0<|k|_2\le R\), (2) gives a ladder coupling of magnitude at least \(|k|_2/5\), while (3) gives \(\tau_j^2\ge1/32\)\.

The quantitative 8EB spectral estimate, using \(s\) from (11), bounds the limiting central return by \(\varepsilon/4\)\. The finite-\(N_\ell\) projector error is bounded by

\[
\frac{2^{16}s(R+1)^2}{N_\ell}
\le\frac{\varepsilon}{4}.
\]

Consequently the calibrated central matrices have the contraction property (4).

Meanwhile, from (9) and (12), for every \(f\) with \(\|f\|_{H^3}\le K_{\ell-1}\),

\[
\begin{aligned}
F_{-1}((U_\ell-C_\ell)f)
&\le
\frac{2^{24}(1+s)K_{\ell-1}}{N_\ell}\\
&\le\frac{\nu}{2^{16}J}\\
&<\frac{\nu}{256J}.
\end{aligned}
\tag{21}
\]

This is where the successive frequency choice matters. The \(\ell\)\-th frequency is selected using the previous \(H^3\) bound \(K_{\ell-1}\), which is already known to the compiler.

There is no dependence on a future frequency or an unknown actual calibration.

## 6\. Every physical pulse and gap remains strongly regular

Let \(u_{\ell-1}\) denote the physical state at time \(t_{\ell-1}\)\. Assume inductively

\[
\|u_{\ell-1}\|_{H^3}\le K_{\ell-1}.
\]

On the active interval, rescale time by \(t=t_{\ell-1}+\delta_\ell\tau\)\. The exact physical equation becomes

\[
\partial_\tau u
=
s h(\tau)\mathcal A_\ell u
+\delta_\ell\nu\Delta u
-\delta_\ell P[(u\cdot\nabla)u].
\tag{22}
\]

The accepted BCA triangular derivative hierarchy applies to the actual calibrated shear: its direction is still perpendicular to \(p_\ell\), and the bound (20) controls its amplitude.

The factor \(L_\ell\) from (13) dominates the calibrated polynomial \(H^3\) amplification. Since (15) guarantees the required small pulse duration, the BCA bootstrap gives

\[
\sup_{t\in I_\ell}\|u(t)\|_{H^3}
\le4L_\ell K_{\ell-1}
=\frac{K_\ell}{2}.
\tag{23}
\]

During the following gap, the equation is unforced. The local \(H^3\) inequality

\[
\frac{d}{dt}\|u\|_{H^3}
\le2^{20}\|u\|_{H^3}^2
\]

and the same choice of \(\delta_\ell\) imply

\[
\sup_{t\in[t_{\ell-1}+\delta_\ell,t_\ell]}
\|u(t)\|_{H^3}\le K_\ell.
\]

Thus

\[
\boxed{
\sup_{t_{\ell-1}\le t\le t_\ell}
\|u(t)\|_{H^3}\le K_\ell.
}
\tag{24}
\]

By induction, the physical equation has a unique strong solution throughout all nine pulses and their gaps, for every calibration and every initial state in the specified \(H^3\) ball.

### Physical-to-inviscid discrepancy

Compare the physical stage output \(u_\ell=u(t_\ell)\) with \(U_\ell u_{\ell-1}\)\.

The calibrated inviscid shear has

\[
\|U_\ell u_{\ell-1}\|_{H^3}
\le2L_\ell K_{\ell-1}
=\frac{K_\ell}{4}.
\]

The physical equation and the inviscid equation differ during the active interval only by the original viscosity and the Navier–Stokes nonlinearity, each multiplied by \(\delta_\ell\) in rescaled time. Since the inviscid propagator is \(L^2\)\-unitary, Duhamel's formula yields an \(L^2\) discrepancy at most \(\delta_\ell E_\ell\)\.

The following unforced gap contributes at most another \(\delta_\ell E_\ell\)\.

Therefore, writing

\[
r_\ell=u_\ell-U_\ell u_{\ell-1},
\]

we obtain

\[
\|r_\ell\|_2\le2\delta_\ell E_\ell,
\qquad
\|r_\ell\|_{H^3}\le2K_\ell.
\]

Interpolation gives

\[
\begin{aligned}
F_{-1}(r_\ell)
&\le\|r_\ell\|_{H^1}\\
&\le(2\delta_\ell E_\ell)^{2/3}
(2K_\ell)^{1/3}.
\end{aligned}
\tag{25}
\]

To check the stated error budget explicitly, put

\[
x_\ell=\frac{J^3K_\ell E_\ell^2}{\nu^3}.
\]

Equation (15) gives \(D_\ell\ge C_*(1+x_\ell)\), so \((1+x_\ell)^2\ge4x_\ell\) implies

\[
8K_\ell\delta_\ell^2E_\ell^2
\le\frac{2\nu^3}{C_*^2J^3}.
\]

Taking cube roots in (25),

\[
\boxed{
F_{-1}(r_\ell)\le\frac{\nu}{256J}.
}
\tag{26}
\]

The physical error and the off-diagonal ladder error are therefore both paid from the same fixed, rationally certified budget.

## 7\. Simultaneous stabilization for all initial states and calibrations

At each completed physical stage,

\[
\begin{aligned}
u_\ell
&=U_\ell u_{\ell-1}+r_\ell\\
&=C_\ell u_{\ell-1}+g_\ell,
\end{aligned}
\]

where

\[
g_\ell=(U_\ell-C_\ell)u_{\ell-1}+r_\ell.
\]

By (21) and (26),

\[
F_{-1}(g_\ell)\le\frac{\nu}{128J}.
\tag{27}
\]

Iterating this identity gives the exact decomposition

\[
u_9=
C_9C_8\cdots C_1u_0+
\sum_{\ell=1}^{9}
C_9\cdots C_{\ell+1}g_\ell.
\tag{28}
\]

Every \(C_\ell\) is contractive in \(F_{-1}\)\. Therefore the second term contributes at most

\[
\sum_{\ell=1}^{9}F_{-1}(g_\ell)
\le\frac{\nu}{128}.
\tag{29}
\]

For the first term, split \(u_0\) into frequencies \(|k|_2\le R\) and \(|k|_2>R\)\.

The nine-direction cover and (6) give

\[
F_{-1}(C_9\cdots C_1u_{0,\le R})
\le\varepsilon F_{-1}(u_{0,\le R})
\le\varepsilon K.
\]

For the original high-frequency tail, Fourier Cauchy–Schwarz gives

\[
F_{-1}(u_{0,>R})
\le\frac{2^{20}K}{R^2}.
\]

Using (10), both of these terms are below \(\nu/1024\)\.

Combining them with (29),

\[
\begin{aligned}
F_{-1}(u(t_9))
&\le
\varepsilon K+\frac{2^{20}K}{R^2}
+\frac{\nu}{128}\\
&<\frac{\nu}{32}.
\end{aligned}
\]

Hence, uniformly over the complete initial class and every admissible independent calibration,

\[
\boxed{
F_{-1}(u(t_9))<\frac{\nu}{4}.
}
\tag{30}
\]

This is the decisive simultaneous-control statement. No common stochastic event, continuity-net argument, or per-calibration tuning is needed.

### Global continuation

For \(t\ge t_9\), the actual control is zero. The accepted torus critical-Fourier-norm continuation estimate therefore gives global strong evolution and

\[
\int_{t_9}^{\infty}F_1(u(t))\,dt\le\frac13.
\]

The \(H^3\) commutator estimate yields

\[
\sup_{t\ge t_9}\|u(t)\|_{H^3}
\le2^{1000}\|u(t_9)\|_{H^3}
\le M.
\]

Together with (24),

\[
\boxed{
\sup_{t\ge0}\|u(t)\|_{H^3}\le M.
}
\tag{31}
\]

The strong solution is unique and classical for positive time.

Finally, throughout the controlled and uncontrolled evolution, the original viscosity satisfies the exact energy identity

\[
\frac12\frac{d}{dt}\|u\|_2^2+
\nu\|\nabla u\|_2^2=0.
\]

Thus

\[
\|u(t)\|_2\le\frac K{1+\nu t}.
\]

Interpolating with (31),

\[
\|u(t)\|_{H^1}^3
\le\frac{K^2M}{(1+\nu t)^2}.
\]

At the rational time (19),

\[
\boxed{
\|u(T)\|_{H^1}\le\frac{\nu}{4}.
}
\tag{32}
\]

The same \(M,T\) apply simultaneously to all initial states and calibrations.

## 8\. Full polynomial physical-resource audit

The unknown calibration does not affect the nominal description length or synthesis computations. It affects physical actuation only through the uniformly bounded amplitude in (20).

Because there are only nine pulses, the resource exponents can be propagated explicitly.

Recall

\[
S=2+K+\nu+\nu^{-1}.
\]

The initial parameter definitions imply, with absolute computable prefactors,

\[
R=O(S^2),\qquad
\varepsilon^{-1}=O(S^2),\qquad
s=O(S^{10}).
\]

Define the integer exponent sequence

\[
h_0=1,
\qquad
n_\ell=\max\{16,h_{\ell-1}+11\},
\]

\[
h_\ell=h_{\ell-1}+30+9n_\ell.
\tag{33}
\]

Direct substitution in (12)–(15) then establishes

\[
N_\ell,\ P_\ell=O(S^{n_\ell}),
\]

\[
K_\ell=O(S^{h_\ell}),
\qquad
D_\ell=O(S^{5h_\ell+3}).
\]

These bounds have fixed computable prefactors, not input-dependent ones.

After nine stages,

\[
n_9=1{,}893{,}333{,}330,
\]

\[
h_9=18{,}933{,}333{,}319,
\]

and

\[
5h_9+3=94{,}666{,}666{,}598.
\]

### Actual-field actuation

On pulse \(\ell\),

\[
\|b_{\rm actual}\|_{W^{3,\infty}}
\le C_1sD_\ell(1+P_\ell)^3,
\]

\[
\|\partial_t b_{\rm actual}\|_{W^{2,\infty}}
\le C_1sD_\ell^2(1+P_\ell)^2.
\]

Here \(C_1\) is absolute and does not depend on the phase, amplitude error or direction error.

The pulse duration is \(D_\ell^{-1}\), so its integrated actuation is at most

\[
C_1s^2
\left[
D_\ell(1+P_\ell)^6+
D_\ell^3(1+P_\ell)^4
\right].
\tag{34}
\]

Since the pulses are disjoint, their integrated costs add without cross terms.

Substituting (33) yields the following conservative powers.

| Physical quantity | Polynomial bound |
|--------|--------|
| Maximum spatial frequency | \(CS^{1{,}893{,}333{,}330}\) |
| Global \(H^3\) bound \(M\) | \(CS^{18{,}933{,}333{,}319}\) |
| Terminal time \(T\) | \(CS^{18{,}933{,}333{,}325}\) |
| Maximum reciprocal pulse/gap duration | \(CS^{94{,}666{,}666{,}598}\) |
| Actual \(\sup_t\\|b\\|_{W^{3,\infty}}\) | \(CS^{100{,}346{,}666{,}598}\) |
| Actual \(\sup_t\\|\partial_t b\\|_{W^{2,\infty}}\) | \(CS^{193{,}119{,}999{,}866}\) |
| Total integrated actuation | \(CS^{291{,}573{,}333{,}134}\) |

The final zero-control interval has duration

\[
T-t_9=\frac{1+64K^2M/\nu^3}{\nu},
\]

whose reciprocal is at most \(\nu\le S\)\. Thus the inverse-duration requirement also covers every nonzero gap and the final unforced interval.

Every exponent in the table is below \(10^{12}\)\.

### Description heights and bit work

The nominal programme contains exactly nine active envelopes and nine spatial cosine modes, with maximum polynomial degree six. Every frequency index and every \(a_\ell\) is integer.

All time breakpoints are rational sums of the form

\[
t_\ell=2\sum_{j=1}^{\ell}D_j^{-1}.
\]

Expanding each shifted envelope \(h(D_\ell(t-t_{\ell-1}))\) gives rational coefficients whose numerator and denominator bit lengths are \(O(B+1)\), with fixed absolute computable constants.

Indeed, the compiler performs a fixed number of integer and rational operations, fixed-power exponentiations, exact comparisons and ceilings. The rational heights may have very large constant multipliers, but the number of stages is nine and the exponentiation degrees are fixed. They therefore remain linear in the complete binary input length \(B\)\.

Using schoolbook exact integer arithmetic, the entire synthesis and input-dependent certification can be bounded by

\[
C(B+1)^3
\]

bit operations for a sufficiently large absolute computable \(C\)\.

The certification uses only the fixed direction-cover lemma, the accepted quantitative spectral and \(H^3\) estimates, and rational comparisons from the compiler formulas. It does not evaluate an unknown solution or any unknown calibration parameter.

A single deliberately coarse pair of common resource constants is

\[
\boxed{
C=2^{10^{15}},\qquad d=10^{12}.
}
\]

The nine-step exponent recurrence above bounds every numerical power by \(S^d\)\. Propagating the fixed numerical prefactors in (10)–(19), (21) and (25)–(34) fits inside the displayed \(C\)\. The same constants dominate all binary heights, output lengths and synthesis work.

This is a mathematical polynomial-resource guarantee; the constants are not intended as practical engineering specifications.



## Final section, rendered-text capture

## 9. Result

Positive robustness theorem at the stipulated accepted scope

**Theorem.** Assume the accepted 8EB quantitative velocity-ladder mixing theorem and BCA polynomial H³ pulse estimates. For the fixed relative calibration tolerance ρ₀ = 1/1024, the algorithm (10)–(19) produces one nominal nine-pulse programme satisfying the entire stated robustness contract for every rational ν > 0 and K ≥ 1.

For every admissible static calibration, including arbitrary independent phase shifts and transverse amplitude errors, and every smooth mean-zero divergence-free u₀ with ‖u₀‖H³ ≤ K, the actual equation has a unique global strong solution, classical for positive time, with

supₜ≥₀ ‖u(t)‖H³ ≤ M, ‖u(T)‖H¹ ≤ ν/4.

All specified synthesis, encoding, timing, frequency, amplitude, derivative and integrated-actuation resources satisfy the required fixed-degree polynomial bounds, uniformly over the calibration set.

The result is stronger than merely showing that a sufficiently accurate implementation of the original single shear succeeds. It tolerates a fixed nonvanishing relative calibration error because the nine directions provide redundant mixing coverage, and the diagonal/off-diagonal Fourier decomposition prevents uncontrolled accumulation of low-frequency returns.

It does not cover arbitrary time-varying calibration errors or incorrect spatial frequency indices; those are outside the stated model. The proof remains conditional precisely on the two previously accepted constructions, rather than constituting independent verification of them.

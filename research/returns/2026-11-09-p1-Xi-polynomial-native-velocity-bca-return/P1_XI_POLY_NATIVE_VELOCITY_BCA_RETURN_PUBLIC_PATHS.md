# P1 Xi completed return

Source: https://chatgpt.com/c/6af0e2d0-1db8-83ec-9610-24dde8eedecf
Model at dispatch: GPT-6 standard, Extra High. Turn: bca946bb-8c54-439b-99b4-378b5ca508be; response: 28427cfc-d072-4c94-940b-8d2519421979. Completion: 2026-11-08 22:20:50 UTC. No producer ZIP visible.

## Actual prompt

Resolve a NEW FULL resource question using your8EB native-velocity controller as accepted capital: can uniform deterministic stabilization be achieved with POLYNOMIAL physical resources and POLYNOMIAL synthesis bit work? Your full finite-computable construction stands at its stated scope, assuming its proof is correct; this is not a request to reprove or independently verify it. You own all methods, representations, source order and framing.

On unit T^3 use EXACTLY
 partial_t u+P[(u.dot.grad)u]=nu*Delta u+P[(b(t,x).dot.grad)u],
 divu=0, meanu=0,
with the canonical Leray projection. For EVERY rational nu>0,K>=1, ONE uniform deterministic algorithm must output rational T>0, M, and divergence-free spatially finite rational-trigonometric b, time piecewise rational-polynomial/globally C2/zero outside[0,T], so EVERY smooth mean-zero divergence-free u0 with ||u0||H3<=K has unique GLOBAL strong evolution, classical for positive time, with
 sup_(t>=0)||u(t)||H3<=M,  ||u(T)||H1<=nu/4.
Use ||v||Hs^2=sum_k(1+4*pi^2|k|^2)^s|v_hat(k)|^2. The SAME programme works for the ENTIRE initial class; the native unforced small-data guarantee at nu/4 stands.

NEW indispensable resource contract: fixed computable absolute C,d, independent of input, such that with S=2+K+nu+nu^-1 and COMPLETE binary length B,
 * total deterministic synthesis/certification BIT work, output description length, coefficient/breakpoint binary heights, number of pieces/modes and polynomial degrees <=C(B+1)^d;
 * T, M, maximum spatial frequency, reciprocal of every nonzero time-piece duration, sup_t||b||W3infinity, sup_t||partial_t b||W2infinity and
   integral_0^T(||b||W3infinity^2+||partial_t b||W2infinity^2)dt <=C*S^d.
Charge ALL construction, arithmetic, numerical accuracy, actuation and output costs; constants/exponents must be computable. Polynomial in numeric S is distinct from polynomial in B. No PDE/regularity/real oracle, uncertified search, per-profile controller, increased viscosity/damping, feedback, white noise or exceptional initial states. A full negative must address this full resource model under a precisely justified assumption, not failure of your shear or a Gronwall bound. Practical hardware/energy advantage is not presumed.

Accepted8EB operation, credited once: explicit rational generic a,m with a.dot.m=0 and no small-mode resonances; single shear v=a cos(2*pi*N*m.dot.x). Its exact Leray Fourier ladders have two limiting Jacobi polarisations with central bond strengths1 and |k.dot.m|/(|k||m|). Quantitative return-amplitude decay, finite-N projector Duhamel error and uniform H3-ball tail estimates give small F_-1=sum_(k!=0)|u_hat(k)|/(2*pi|k|) after an inviscid shear. A sufficiently short rational pulse controls the physical nonlinear/viscous discrepancy, and F_-1<nu/4 gives global unforced continuation. Your finite bit programme, explicit H3/T/actuation and C2 bump stand. Its Q0=2^(2H) short-pulse estimates have double-exponential numeric magnitudes and exponential output bit bounds; they DO NOT meet the new contract.

Existing small-critical-Fourier-norm machinery is credited: Lei-Lin1203.2699v1 https://arxiv.org/pdf/1203.2699v1 Thm1.1/Section2, read by ROOT, is on R3; your torus Fourier-sum/H3 continuation calculation supplies the matched finite-periodic scope. Agresti2607.15140v4 and FHHLN2004.07528v3 retain their already supplied stochastic/per-initial and vorticity/measure-exceptional scopes; no stronger deterministic theorem is imported.

Optional ROOT idea only: a.dot.k is conserved along the shear ladder, while nearest-neighbour hops have bounded block norms; weighted ladder moments may give polynomial H3 growth even with diagonal viscous killing, replacing the exponential derivative bound. Whether that can pay the nonlinear pulse and ALL resource bounds is not supplied; you may discard it and the shear route.

Pursue FULL resolution persistently and independently. Another finite-but-exponential controller or a conditional linear estimate is not the polynomial-resource theorem.

you may use all subagents avaible
All inherited source/access/transfer/resource holds apply to every subagent, including unknown identities. EVERY failed original/transfer, including NSF10314785, OpenAI Uniform-Permanence tree, Dots/Golding-Henderson/Serre/CarloAlberto/root2410.23225v3/TR26-272/2610.00548v2 and all others, stays HELD: no retry/raw/PDF/mirror/alternate/identifying recovery/held-source injection. No attachments, extra principal/model/worker/resource/account/spending, Sol or Dots action.

## Available user-visible activity

Worked for 16m 30s

Finalized controlled pulse via nonlinear estimates and bootstrap closure

The polynomial-resource question appears to turn on one estimate: whether the linear Leray-projected shear can be bounded in H³ by a polynomial rather than an exponential. I’ll use derivatives parallel and transverse to the shear to test a triangular energy estimate, then account for the nonlinear pulse error and every output/resource bound.

Bounded shear dynamics and verified nonlinear pulse growth estimates
Bounded the construction
Searched 9 websites
Constructed an explicit certified stabilizing protocol

The triangular estimate closes the nonlinear pulse with a rational duration 1/D, where D is polynomial in S. The remaining calculation is an explicit resource audit: frequency, amplitude, time derivative, integrated actuation, coefficient heights, and synthesis bit complexity.

Bounded the construction

Analysis paused — Python:

```python
from fractions import Fraction
import sympy as sp
z=sp.symbols('z')
h=140*z**3*(1-z)**3
print(sp.integrate(h,(z,0,1)))
print([(sp.diff(h,z,j).subs(z,0), sp.diff(h,z,j).subs(z,1)) for j in range(3)])
v = {'R':2,'Q':2,'A':14,'rinv':12,'epsinv':2,'s':94,'N':114,'p':118}
v['L']=3*(v['s']+v['A']+3*v['p'])
v['M0']=v['L']+1
v['E0']=2*v['M0']
v['D']=v['M0']+2*v['E0']+3
v['bW3']=v['s']+v['D']+v['A']+3*v['p']
v['btW2']=v['s']+2*v['D']+v['A']+2*v['p']
v['I']=2*v['s']+3*v['D']+2*v['A']+4*v['p']
v['bcoef']=v['s']+7*v['D']+v['A']
v
```

## Complete response

# Resolution: polynomial-resource deterministic stabilization

**Under the stipulated acceptance of the 8EB velocity-shear construction, the polynomial-resource question has a positive resolution.**

The same single-mode Leray-projected shear can be used. The necessary improvement is to replace the exponential \(H^3\) estimate during the control pulse with a polynomial estimate exploiting the shear's directional structure.

The resulting construction has\:

- One prescribed divergence-free spatial cosine mode.
- One active time interval, with a degree-six polynomial envelope.
- Uniform global strong solvability for every admissible initial velocity.
- Terminal \(H^1\) norm at most \(\nu/4\)\.
- Physical resources polynomial in \(S=2+K+\nu+\nu^{-1}\)\.
- Deterministic synthesis using polynomial bit work in the complete input length \(B\)\.

The qualification is precise: this establishes the new resource theorem **conditional on the previously accepted 8EB uniform inviscid-shear estimate**\. It does not require an additional stochastic theorem or a PDE-computation oracle.

## 1\. The missing polynomial \(H^3\) estimate

Let

\[
v(x)=a\cos(2\pi p\cdot x),\qquad a\cdot p=0,
\]

and define the native velocity operator

\[
\mathcal A w=P[(v\cdot\nabla)w].
\]

Consider the rescaled controlled equation

\[
\partial_\tau u
=s h(\tau)\mathcal A u
+\delta\nu\Delta u
-\delta P[(u\cdot\nabla)u],
\qquad 0\le\tau\le1,
\]

where \(h\ge0\) and \(\int_0^1h=1\)\.

The usual isotropic Sobolev estimate gives an exponential bound involving the shear's frequency and amplitude. That estimate is valid but unnecessarily expensive.

### A triangular derivative hierarchy

Choose an orthonormal basis

\[
e_1=\frac a{|a|},\qquad
e_2=\frac p{|p|},\qquad
e_3=e_1\times e_2,
\]

and write \(D_i=e_i\cdot\nabla\)\.

Because \(a\cdot p=0\), the coefficient \(\cos(2\pi p\cdot x)\) is constant in the \(e_1\) and \(e_3\) directions. Since constant derivatives commute with the Leray projection,

\[
\boxed{
[D_1,\mathcal A]=[D_3,\mathcal A]=0.
}
\]

Only the \(D_2\) derivatives produce commutators. For \(D^\alpha=D_1^{\alpha_1}D_2^{\alpha_2}D_3^{\alpha_3}\),

\[
[D^\alpha,\mathcal A]u
=
\sum_{\ell=1}^{\alpha_2}
\binom{\alpha_2}{\ell}
P\left[
(D_2^\ell\cos(2\pi p\cdot x))
(a\cdot\nabla)
D_1^{\alpha_1}D_2^{\alpha_2-\ell}D_3^{\alpha_3}u
\right].
\]

The crucial observation is that **every commutator reduces the number of \(D_2\) derivatives**\. Although it may introduce another \(D_1\) derivative, it never raises the total derivative order above three.

This produces a strictly triangular hierarchy of four derivative groups.

### Exact \(H^3\) grouping

Set

\[
c_\alpha=\binom3{|\alpha|}\frac{|\alpha|!}{\alpha_1!\alpha_2!\alpha_3!},
\]

and for \(j=0,1,2,3\), define

\[
E_j(\tau)^2
=
\sum_{\substack{|\alpha|\le3\\\alpha_2=j}}
c_\alpha\|D^\alpha u(\tau)\|_2^2.
\]

By the multinomial theorem and orthonormality,

\[
\|u\|_{H^3}^2=\sum_{j=0}^3E_j^2.
\]

Consequently, with \(E=\sum_{j=0}^3E_j\),

\[
\|u\|_{H^3}\le E\le2\|u\|_{H^3}.
\]

The linear shear is skew-adjoint in \(L^2\) on divergence-free fields. The viscosity contributes a nonpositive term to every differentiated energy estimate.

For the Navier–Stokes nonlinearity, the leading differentiated transport term also cancels\:

\[
\langle D^\alpha u,P[u\cdot\nabla D^\alpha u]\rangle=0.
\]

Only product commutators remain. For \(|\alpha|\le3\), Fourier convolution estimates give the uniform bound

\[
\left|
\left\langle D^\alpha u,
D^\alpha P[(u\cdot\nabla)u]\right\rangle
\right|
\le C_0\|D^\alpha u\|_2\|u\|_{H^3}^2,
\qquad C_0=2^{20}.
\]

Here the estimate is on the energy pairing, not on the full \(H^3\) norm of the nonlinear term. This distinction avoids a derivative loss.

Writing \(A=|a_1|+|a_2|+|a_3|\) and \(P_1=\sum_i|p_i|\), the commutator expansion therefore gives

\[
\boxed{
E_j'(\tau)\le
\gamma h(\tau)\sum_{i<j}E_i(\tau)
+\delta C_0E(\tau)^2,
}
\]

with the explicit rational/integer coefficient

\[
\gamma=2^{20}sA(1+P_1)^3.
\]

### Polynomial growth rather than exponential growth

Let \(J\) be the \(4\times4\) strictly lower triangular matrix with \(J_{ji}=1\) for \(i<j\)\. Then

\[
J^4=0.
\]

The homogeneous derivative hierarchy is bounded by

\[
e^{\gamma J\int_0^\tau h}
=
I+\gamma HJ+\frac{\gamma^2H^2J^2}{2}
+\frac{\gamma^3H^3J^3}{6},
\qquad 0\le H\le1.
\]

There is no exponential series beyond the third power.

Define

\[
\boxed{
L=\left(1+2^{24}sA(1+P_1)^3\right)^3.
}
\]

The matrix estimate yields

\[
\boxed{
E(\tau)\le
L\left(
2K+4\delta C_0\int_0^\tau E(r)^2\,dr
\right).
}
\]

If

\[
\delta\le\frac{1}{32C_0L^2K},
\]

a bootstrap gives

\[
\boxed{
\sup_{0\le\tau\le1}\|u(\tau)\|_{H^3}
\le4LK.
}
\]

For the inviscid linear shear, where the \(\delta\)\-terms vanish, the sharper bound is

\[
\boxed{
\sup_{0\le\tau\le1}\|w(\tau)\|_{H^3}
\le2LK.
}
\]

These estimates are uniform over the full initial \(H^3\) ball and, critically, \(L\) is a fixed-degree polynomial in the shear's numerical parameters.

This removes the exponential \(Q_0=2^{2H}\) factor responsible for the previous construction's excessive physical and binary resources.

## 2\. Explicit polynomial-resource synthesis algorithm

We retain the accepted 8EB quantitative inviscid-shear construction, but replace its pulse-duration, \(H^3\), and terminal-time parameters.

Every computation below uses rational or integer arithmetic.

### Step A. Construct the mixing shear

Fix

\[
C_*=2^{30}.
\]

Compute

\[
R=\left\lceil100C_*\left(1+\frac K\nu\right)\right\rceil,
\qquad
\varepsilon_*=
\min\left\{\frac14,\frac{\nu}{100C_*K}\right\}.
\]

Define the integer vectors

\[
Q=10(R+1),\qquad
m=(1,Q,Q^2),
\]

\[
n=(1,Q^3,Q^6),\qquad
a=m\times n.
\]

Set

\[
A=|a_1|+|a_2|+|a_3|,
\qquad
r=\frac{1}{R^2(1+Q^2+Q^4)}.
\]

Compute

\[
s=\left\lceil10^9r^{-7}\varepsilon_*^{-5}\right\rceil
\]

and

\[
N=\left\lceil
100C_*
\left(
1+R+
\frac{sAR^2}{\varepsilon_*}
+\frac{K(1+sA)}{\nu}
\right)
\right\rceil.
\]

Finally put

\[
p=Nm,\qquad P_1=|p_1|+|p_2|+|p_3|,
\]

\[
v(x)=a\cos(2\pi p\cdot x).
\]

The accepted 8EB Fourier-ladder theorem supplies the uniform estimate

\[
\boxed{
F_{-1}\bigl(e^{s\mathcal A}u_0\bigr)
\le\frac{3\nu}{100}
\quad\text{for every }\|u_0\|_{H^3}\le K,
}
\tag{1}
\]

where

\[
\mathcal A=P[(v\cdot\nabla)\,\cdot\,],
\qquad
F_{-1}(f)=\sum_{k\ne0}
\frac{|\widehat f(k)|}{2\pi|k|}.
\]

This is the single inherited analytic result. The polynomial resource argument does not assume any additional regularity or stability theorem.

### Step B. Compute a polynomial pulse duration

Using \(A,P_1,s\), compute

\[
L=\left(1+2^{24}sA(1+P_1)^3\right)^3.
\]

Set

\[
M_0=4LK,\qquad
E_0=\nu M_0+2^{20}M_0^2.
\]

Define the positive integer

\[
\boxed{
D=
\left\lceil
2^{30}
\left(
1+L^2K+\frac{M_0E_0^2}{\nu^3}
\right)
\right\rceil,
}
\tag{2}
\]

and

\[
\delta=\frac1D.
\]

Unlike the previous construction, no exponential of a shear-dependent quantity appears in \(D\)\.

### Step C. Output the physical controller

Let

\[
h(z)=140z^3(1-z)^3,\qquad 0\le z\le1.
\]

Define

\[
\boxed{
b(t,x)=
\begin{cases}
sD\,h(Dt)\,a\cos(2\pi p\cdot x),
&0\le t\le\delta,\\[2mm]
0,&t<0\text{ or }t>\delta.
\end{cases}
}
\tag{3}
\]

The polynomial \(h\) satisfies

\[
\int_0^1h(z)\,dz=1,
\]

and

\[
h^{(j)}(0)=h^{(j)}(1)=0,\qquad j=0,1,2.
\]

Thus \(b\) is globally \(C^2\) in time. It is divergence-free because \(a\cdot p=0\)\.

It has one real spatial cosine mode and degree six in time. Its nonzero time-polynomial coefficients are explicitly

\[
140s\,a\left(
D^4t^3-3D^5t^4+3D^6t^5-D^7t^6
\right).
\]

All coefficients are integers.

### Step D. Output the global bound and terminal time

Set

\[
\boxed{M=2^{1000}M_0}
\tag{4}
\]

and

\[
\boxed{
T=\delta+\frac{1+64K^2M/\nu^3}{\nu}.
}
\tag{5}
\]

Both are positive rationals. The controller is already zero for every \(t\ge\delta\), so in particular it is zero for \(t\ge T\)\.

The algorithm is now completely specified.

## 3\. The physical pulse satisfies the required approximation estimate

We must prove that the polynomial \(D\) in (2) makes the actual nonlinear, viscous trajectory sufficiently close to the inviscid shear trajectory.

Let \(u(t)\) denote the physical solution and put

\[
U(\tau)=u(\delta\tau),\qquad 0\le\tau\le1.
\]

Then

\[
\partial_\tau U
=s h(\tau)\mathcal A U
+\delta\nu\Delta U
-\delta P[(U\cdot\nabla)U].
\]

The triangular estimate from Section 1 applies because

\[
D\ge2^{30}L^2K
>
32\cdot2^{20}L^2K.
\]

Therefore

\[
\sup_{0\le\tau\le1}\|U(\tau)\|_{H^3}\le M_0.
\tag{6}
\]

This estimate also closes the standard \(H^3\) continuation argument, proving existence and uniqueness through the entire control pulse.

Let \(W\) satisfy

\[
\partial_\tau W=s h(\tau)\mathcal A W,\qquad W(0)=u_0.
\]

Because \(h\) integrates to one,

\[
W(1)=e^{s\mathcal A}u_0,
\]

and the linear triangular estimate gives

\[
\sup_{0\le\tau\le1}\|W(\tau)\|_{H^3}\le2LK\le M_0.
\tag{7}
\]

The propagator generated by \(s h(\tau)\mathcal A\) is unitary on divergence-free \(L^2\)\. Duhamel's formula therefore gives

\[
\begin{aligned}
\|U(1)-W(1)\|_2
&\le\delta\int_0^1
\left(
\nu\|\Delta U\|_2+
\|P[(U\cdot\nabla)U]\|_2
\right)d\tau\\
&\le\delta E_0.
\end{aligned}
\tag{8}
\]

Also,

\[
\|U(1)-W(1)\|_{H^3}\le2M_0.
\]

Sobolev interpolation yields

\[
\|U(1)-W(1)\|_{H^1}
\le
(\delta E_0)^{2/3}(2M_0)^{1/3}.
\tag{9}
\]

For mean-zero fields, Fourier Cauchy–Schwarz and the elementary lattice estimate

\[
\sum_{k\ne0}|k|^{-4}\le52
\]

give

\[
F_{-1}(f)\le\|f\|_{H^1}.
\]

The choice of \(D\) ensures

\[
2M_0\delta^2E_0^2\le\frac{\nu^3}{512}.
\]

Cubing (9) consequently establishes

\[
\boxed{
F_{-1}(U(1)-W(1))\le\frac{\nu}{8}.
}
\tag{10}
\]

Combining (1) and (10),

\[
\begin{aligned}
F_{-1}(u(\delta))
&\le F_{-1}(W(1))
+F_{-1}(U(1)-W(1))\\
&\le\frac{3\nu}{100}+\frac{\nu}{8}\\
&<\frac{\nu}{4}.
\end{aligned}
\]

Thus

\[
\boxed{
\sup_{\|u_0\|_{H^3}\le K}
F_{-1}(u(\delta;u_0))
<\frac{\nu}{4}.
}
\tag{11}
\]

No initial-dependent quantities appear in \(D,b\), or any parameter used in this argument.

## 4\. Global regularity and terminal \(H^1\) control

After \(t=\delta\), the controller vanishes.

The established torus critical-Fourier-norm estimate gives

\[
\frac{d}{dt}F_{-1}(u)
+\bigl(\nu-F_{-1}(u)\bigr)F_1(u)\le0.
\]

By (11),

\[
F_{-1}(u(t))\le\frac{\nu}{4},
\qquad t\ge\delta,
\]

and

\[
\int_\delta^\infty F_1(u(t))\,dt\le\frac13.
\]

The standard \(H^3\) Fourier commutator estimate then yields

\[
\|u(t)\|_{H^3}
\le
M_0\exp\left(
1000\int_\delta^t F_1(u(r))\,dr
\right)
\le2^{1000}M_0=M.
\]

Together with (6),

\[
\boxed{
\sup_{t\ge0}\|u(t)\|_{H^3}\le M.
}
\tag{12}
\]

The continuation criterion gives global uniqueness and strong solvability. The positive viscosity and smooth spatial coefficients give the required classical regularity for positive time.

For the terminal estimate, divergence-freeness of both \(u\) and \(b\) gives the native energy identity

\[
\frac12\frac{d}{dt}\|u\|_2^2+
\nu\|\nabla u\|_2^2=0.
\]

Hence

\[
\|u(t)\|_2\le K e^{-4\pi^2\nu t}
\le\frac K{1+\nu t}.
\]

Interpolating with (12),

\[
\|u(t)\|_{H^1}^3
\le
\|u(t)\|_2^2\|u(t)\|_{H^3}
\le
\frac{K^2M}{(1+\nu t)^2}.
\]

Let \(Z=64K^2M/\nu^3\)\. The selected time satisfies \(1+\nu T\ge1+Z\)\. Therefore,

\[
\|u(T)\|_{H^1}^3
\le
\frac{\nu^3}{64}
\frac{Z}{(1+Z)^2}
\le\frac{\nu^3}{64}.
\]

It follows that

\[
\boxed{
\|u(T)\|_{H^1}\le\frac{\nu}{4}.
}
\tag{13}
\]

The required terminal condition is proved.

## 5\. Complete physical-resource audit

The remaining question is whether every output resource is polynomial in the numerical parameter

\[
S=2+K+\nu+\nu^{-1}.
\]

It is.

For clarity, the following are conservative upper bounds on powers of \(S\)\. Every row has an absolute computable multiplicative constant.

| Quantity | Upper bound |
|--------|--------|
| Low-frequency cutoff \(R\) | \(CS^2\) |
| Shear integer-vector magnitude \(A\) | \(CS^{14}\) |
| Inverse resonance parameter \(r^{-1}\) | \(CS^{12}\) |
| Inverse tolerance \(\varepsilon_*^{-1}\) | \(CS^2\) |
| Mixing duration \(s\) | \(CS^{94}\) |
| Frequency multiplier \(N\) | \(CS^{114}\) |
| Maximum spatial frequency \(P_1\) | \(CS^{118}\) |
| Polynomial shear factor \(L\) | \(CS^{1386}\) |
| Pulse \(H^3\) bound \(M_0\) | \(CS^{1387}\) |
| Error constant \(E_0\) | \(CS^{2774}\) |
| Reciprocal pulse duration \(D\) | \(CS^{6938}\) |
| Global \(H^3\) bound \(M\) | \(CS^{1387}\) |
| Terminal time \(T\) | \(CS^{1393}\) |

These follow by substituting the defining expressions successively. For example,

\[
R=O(S^2),\quad Q=O(S^2),\quad A=O(S^{14}),
\]

\[
r^{-1}=O(S^{12}),
\quad s=O\bigl(S^{7\cdot12+5\cdot2}\bigr)=O(S^{94}),
\]

\[
N=O(S^{114}),\quad P_1=O(S^{118}),
\]

and therefore

\[
L=O\left(
(S^{94}S^{14}S^{354})^3
\right)=O(S^{1386}).
\]

All later resource exponents follow from the displayed rational formulas.

### Peak amplitudes and integrated actuation

Because \(h,h'\) are fixed degree-six and degree-five polynomials respectively, their sup norms have absolute bounds.

The controller (3) therefore satisfies

\[
\|b\|_{L^\infty_tW^{3,\infty}_x}
\le
C sDA(1+P_1)^3
\le CS^{7400},
\]

and

\[
\|\partial_t b\|_{L^\infty_tW^{2,\infty}_x}
\le
C sD^2A(1+P_1)^2
\le CS^{14220}.
\]

Since the active pulse has duration \(\delta=1/D\),

\[
\begin{aligned}
&\int_0^T
\left(
\|b\|_{W^{3,\infty}}^2+
\|\partial_t b\|_{W^{2,\infty}}^2
\right)dt\\
&\qquad\le
C s^2A^2
\left[
D(1+P_1)^6+
D^3(1+P_1)^4
\right]\\
&\qquad\le
\boxed{CS^{21502}}.
\end{aligned}
\tag{14}
\]

Both nonzero time pieces satisfy the reciprocal-duration requirement\:

\[
\delta^{-1}=D\le CS^{6938}
\]

and

\[
(T-\delta)^{-1}
=
\frac{\nu}{1+64K^2M/\nu^3}
\le\nu\le S.
\]

The finite actuation and every requested physical magnitude are therefore polynomial in \(S\)\.

## 6\. Binary heights, output length and deterministic bit work

The polynomial physical bounds alone do not establish polynomial synthesis bit work. Both must be checked.

In this construction, the arithmetic operations have a particularly simple structure. All powers appearing in the synthesis are fixed integer powers. All comparisons are between rationals. There are no adaptive precision loops, matrix diagonalizations, optimization problems, spectral evaluations or PDE solves.

The largest time-polynomial coefficients have magnitude bounded by

\[
420sAD^7\le CS^{48674}.
\]

Because the input length is \(B\),

\[
S\le2^{B+3}
\]

for a conservative binary-encoding bound. Thus

\[
\log_2(420sAD^7)=O(B).
\]

For the intermediate rational coefficients, the numerator and denominator heights are also \(O(B)\)\: only a fixed number of rational additions, multiplications, divisions and fixed-power operations occur, starting from \(B\)\-bit inputs.

There are exactly two nonzero-duration pieces within \([0,T]\), at most two complex Fourier modes representing the single real cosine, and maximum time-polynomial degree six. The full output description therefore has \(O(B)\) bits, with absolute computable constants.

A schoolbook exact-rational implementation, including integer ceilings, comparisons, fraction normalization and verification of the output parameter inequalities, admits the conservative bounds

\[
\boxed{
\text{synthesis and certification bit work}
\le C(B+1)^3,
}
\]

\[
\boxed{
\text{output description length and all binary heights}
\le C(B+1).
}
\]

The analytic spectral and continuation estimates are uniform theorems used in the proof, not numerical subroutines invoked on unknown solutions.

For a single common exponent covering every contractual resource, an intentionally loose explicit choice is

\[
\boxed{
d=50{,}000,\qquad C=2^{10^8}.
}
\]

The displayed resource exponents, fixed arithmetic operation count, and rational coefficient formulas give the required bounds with these absolute computable constants. No efficiency optimization is needed for the theorem.

## 7\. Verification of the nonlinear commutator constant

One technical point is worth making explicit because the proof depends on a polynomial rather than exponential bound.

Set

\[
W_k=(1+4\pi^2|k|^2)^{1/2}.
\]

Counting integer lattice points in cubic shells gives

\[
\sum_{k\ne0}|k|^{-4}
\le26\sum_{j=1}^\infty j^{-2}\le52.
\]

Consequently,

\[
\sum_{k\in\mathbb Z^3}W_k^{-4}<2,
\]

and

\[
\sum_{k\ne0}
\frac{(2\pi|k|)^2}{W_k^6}<1.
\]

The second inequality controls a first derivative of \(u\) in Fourier \(\ell^1\) by \(\|u\|_{H^3}\)\.

For the only potentially troublesome differentiated product, involving two second derivatives, let

\[
A_k=W_k^3|\widehat u(k)|.
\]

Each second-derivative Fourier coefficient is bounded by \(W_k^{-1}A_k\)\. For fixed \(k\), Cauchy–Schwarz gives

\[
\begin{aligned}
\left(
\sum_{\ell+h=k}
W_\ell^{-1}W_h^{-1}A_\ell A_h
\right)^2
&\le
\left(
\sum_{\ell+h=k}W_\ell^{-2}W_h^{-2}
\right)
\left(
\sum_{\ell+h=k}A_\ell^2A_h^2
\right)\\
&\le2\sum_{\ell+h=k}A_\ell^2A_h^2.
\end{aligned}
\]

Summing over \(k\) gives a product \(L^2\) bound of \(\sqrt2\|u\|_{H^3}^2\)\.

All terms in the differentiated nonlinear commutators have derivative distributions \((1,3)\), \((2,2)\), or \((3,1)\), or strictly lower orders. The preceding estimates control each distribution uniformly, including under any orthonormal change of derivative directions.

Accounting for vector components, Leibniz coefficients and the finite derivative groupings fits inside \(C_0=2^{20}\)\.

This completes the constant-level justification for the nonlinear term in the triangular hierarchy; no assumption about higher Sobolev norms of the initial data was introduced.

## 8\. Final theorem and scope

(Positive conditional resolution)

**Theorem.** Assume the accepted 8EB uniform inviscid velocity-shear estimate (1). Then the deterministic algorithm (2)–(5), together with the shear synthesis in Step A, satisfies the full polynomial-resource stabilization contract for every rational \(\nu>0\), \(K\ge1\), and every smooth mean-zero divergence-free initial condition satisfying \(\|u_0\|_{H^3}\le K\)\.

Specifically,

\[
\boxed{
\sup_{t\ge0}\|u(t)\|_{H^3}\le M,\qquad
\|u(T)\|_{H^1}\le\nu/4,
}
\]

with one common controller for the entire initial class, while all synthesis, encoding and physical-resource bounds satisfy the required polynomial inequalities.

The principal new ingredient is the nilpotent derivative hierarchy

\[
[D_1,\mathcal A]=[D_3,\mathcal A]=0,
\qquad
[D_2^j,\mathcal A]
\text{ involves only lower }D_2\text{-orders}.
\]

It converts shear-dependent exponential Sobolev growth into a fixed-degree polynomial. That permits a polynomially short nonlinear pulse while keeping the original viscosity and the native Leray-projected velocity equation.

The result does not prove or independently certify the inherited 8EB mixing theorem. **Within the question's explicit acceptance of that theorem, however, the previous double-exponential resource obstruction is eliminated, and the strengthened polynomial-resource contract follows.**

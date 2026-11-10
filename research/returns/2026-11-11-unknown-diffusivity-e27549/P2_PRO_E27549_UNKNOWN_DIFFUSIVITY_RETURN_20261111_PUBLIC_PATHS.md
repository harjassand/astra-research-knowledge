# P2 completed return — unknown diffusivity ensemble

Chat: https://chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677  
Model shown: Pro. User turn: ad0e9595-f5b8-48a0-b6d6-ad0ac8712ecd. Final: e27549be-a93c-5a78-9054-4958f45207c1.  
Prompt source: `work/astra-renewed-pro-programmes-20261103/P2_FULL_UNKNOWN_DIFFUSIVITY_ENSEMBLE_MHD_COMPILER_PRO_20261111.txt` (SHA-256 `2f6bc37b9910bfd6fcc5d5767f8a71b504713b45b1e86426b0e9587f5ae4fd0a`; the approved posted version omitted one terminal LF).

Capture: complete final copied through the response's UI Copy control as Markdown; the native reader exposed only a 20,000-character prefix. No literal database-byte identity is claimed. Current activity history was virtualized; the visible pre-completion excerpt below is all preserved from that view. No original ZIP was visible; none is included.

## Visible activity excerpt

The visible continuation of a paragraph began: “constant viscosity. This preserves the supplied two-stage target synthesis; no parameter sampling or estimation is needed.” The displayed activity lines were:

- Checked conjugation order
- Finalizing resource bounds
- Clarified parameter identities and checked weak-solution scope
- Checked viscosity residuals
- Checked global reset stability
- Prepared H12 fixed-order data
- Checked bit-length bounds and truncated target coefficients
- Alternative constructions finished
- Refined rational coefficient handling
- Checked coefficient bit complexity and prepared finite Fourier storage
- Checked coefficient bounds and uniformized viscosity terms
- Verified Fourier-multiplier commutation
- Bounded rational quadrature perturbations
- Refined affine-word constants and wrote inverse affine group
- Checked uniform strong-solution bounds
- Defined compiler constant A
- Derived explicit A and physical-bit bounds
- Rounded amplitudes and constants
- Finalized computable compiler details
- Selected explicit constants and reviewed proof order
- Specified rational reset program and initial H1 bound
- Bounded affine writer error

Earlier visible activity addressed making carrier forces independent of unknown parameters, accumulated return errors in coupled erasure and target writing, and obstructions to a shared schedule across the parameter rectangle. The activity panel showed three subagents used; their current final panels were not available in this capture.

## Complete UI-copied final

**Yes, under the concrete quantitative constructions supplied in the question.** The viscosity-dependent carrier compensation can be removed while preserving polynomial costs and the common-input quantifier.

In fact, the compiler can ignore \(\nu_+\) and \(\rho_+\) when constructing the force. It can produce one force that works throughout a slightly larger rectangle
\[
[\underline\nu,1]\times[\underline\rho,1],
\]
where \(\underline\nu,\underline\rho\) are rational lower bounds computed from \(\nu_-,\rho_-\).

The new ingredients are:

1. **Spatial averaging of the viscosity-dependent affine drift of the erasing word.**
2. **An exact-return analysis reference for the supplied parameter-independent magnetic-stirring pulse.**
3. **A viscosity-independent version of the fixed-depth lowering step.**
4. **Exact affine cancellation in the target writer’s forward/inverse shear loops.**

The averaging in the first step is over **spatial translations**, never over parameter samples. No value of either actual diffusivity is estimated or evaluated by the compiler.

Below is the construction and the resource argument. I use the quantitative primitives stipulated in the question, including their effective constants and concrete shear-word representations. This is additional machinery beyond Nersesyan’s qualitative framework, whose quantifier order permits choosing the control after fixing the viscosity. [arxiv.org](https://arxiv.org/pdf/1403.5369v2?utm_source=chatgpt.com)

---

# 1. Parameters used by the compiler

Define
\[
n_\nu=\left\lceil\nu_-^{-1}\right\rceil,\qquad
n_\rho=\left\lceil\rho_-^{-1}\right\rceil,
\]
and
\[
\nu_0=n_\nu^{-1},\qquad
\rho_0=n_\rho^{-1},\qquad
\mu_0=\min(\nu_0,\rho_0).
\]
Then
\[
\frac{\nu_-}{2}\le\nu_0\le\nu_-,
\qquad
\frac{\rho_-}{2}\le\rho_0\le\rho_-.
\]
Thus every admissible actual pair satisfies
\[
\nu_0\le\nu\le1,\qquad \rho_0\le\rho\le1.                         \tag{1.1}
\]

Similarly, put
\[
M_0=\lceil M\rceil,\qquad
\tau_0=\left\lceil\tau^{-1}\right\rceil^{-1},\qquad
\epsilon_0=\left\lceil\epsilon^{-1}\right\rceil^{-1}.
\]
The numerical construction can use these coarse bounds. The exact input \(\tau\) is retained to place the final endpoint at precisely \(\tau\).

Set
\[
X=2+M_0+n_\nu+n_\rho+\lceil\tau^{-1}\rceil+\lceil\epsilon^{-1}\rceil.
\]
There is a fixed numerical constant \(C\) with
\[
X\le CR.                                                        \tag{1.2}
\]

All control choices below use these quantities, the target encoding, and fixed precomputed data. Positive powers of an actual diffusivity are bounded using \(1\); reciprocal powers and coercivity estimates use \(\nu_0,\rho_0\).

Write
\[
\mathcal B(v,w)=P[(v\cdot\nabla)w],\qquad
L_Fv=\mathcal B(F,v)+\mathcal B(v,F),
\]
\[
C_Fb=(F\cdot\nabla)b-(b\cdot\nabla)F.
\]

Parameter-dependent functions introduced below are **analysis references**. They are not evaluated by the compiler and are not additional applied velocities or forces.

---

# 2. A viscosity-independent erasing word

Simply omitting \(-\nu\Delta w\) from a carrier force is not, by itself, a small-error argument. For a scalar shear amplitude,
\[
x'+\lambda x=f,
\]
one has
\[
x(h)-x(0)+\lambda\int_0^h x(t)\,dt=\int_0^h f(t)\,dt.
\]
A nonzero prescribed displacement and small endpoint velocity cannot both be made independent of \(\lambda\) by an arbitrary single short pulse.

The erasing word needs a cancellation at the level of its complete affine action.

## 2.1 Exact affine action of one shear leg

For a one-coordinate shear
\[
F=e_i\phi(x_j),\qquad i\ne j,
\]
we have
\[
\mathcal B(F,F)=0,\qquad L_F\Delta F=0.                           \tag{2.1}
\]

Let
\[
w(t)=c(t)F,\qquad a(t)=\int_{t_0}^t c(s)\,ds,
\]
and emit the parameter-independent force
\[
f=w_t.
\]

Consider the reference equation
\[
v_t+L_wv=\nu\Delta w.
\]
Equation (2.1) gives its exact solution
\[
v(t)=e^{-a(t)L_F}v(t_0)+\nu a(t)\Delta F.
\]
A shear leg of signed impulse \(a\) therefore acts by the affine map
\[
\boxed{
\mathcal A_F^\nu(a)v=e^{-aL_F}v+\nu a\Delta F.
}                                                               \tag{2.2}
\]

This formula is exact and independent of physical compression. It concerns the physical Euler linearized generator \(L_F\).

## 2.2 Affine bias of the supplied contracting word

Fix the concrete finite shear word from the accepted construction. In its linear-impulse representation, write
\[
W(s)=E_m(s)\cdots E_1(s),\qquad
E_j(s)=e^{-c_jsL_{F_j}},
\]
where all \(c_j,F_j\) are fixed and effectively given.

The supplied estimates are
\[
W(s)=e^{s^4D}+O_{H^m\to H^m}(s^5),                              \tag{2.3}
\]
on the required fixed Sobolev orders, with \(D\) a Fourier multiplier having the stated negative symmetric part. The underlying transport of the word is exactly the identity.

Replacing each shear leg by its affine map (2.2), the complete word acts as
\[
v\longmapsto W(s)v+\nu b(s),                                    \tag{2.4}
\]
where
\[
b(s)=
\sum_j c_js\,E_m(s)\cdots E_{j+1}(s)\Delta F_j.
\]

Let \(K_{\rm cat}\) bound the coordinate sizes of the fixed catalogue’s wavevectors. Then
\[
b(s)=s b_1+s^2b_2+s^3b_3+s^4b_4+O_{H^m}(s^5),                 \tag{2.5}
\]
where each \(b_j\) is a mean-zero solenoidal Fourier polynomial supported in
\[
|k|_\infty\le jK_{\rm cat}.                                     \tag{2.6}
\]

There is no operator-norm differentiability assumption about a transport group here. To obtain (2.5), differentiate the fixed products on the fixed smooth vectors \(\Delta F_j\), paying the finitely many additional derivatives. Each application of \(L_F\) adds at most one catalogue frequency. Mean zero is preserved by \(L_F\).

All Taylor coefficients, support bounds and remainder constants are effectively bounded in fixed precomputation.

## 2.3 Fixed positive rational spatial quadrature

We construct a fixed finite quadrature annihilating every nonzero Fourier mode in
\[
|k|_\infty\le4K_{\rm cat}.
\]

For completeness, it can be made exactly rational in sine/cosine coordinates.

Let \(K=4K_{\rm cat}\), \(n=2K+1\). Approximate the \(n\)-th roots of unity by rational unit-circle points
\[
z_j=\frac{1-t_j^2+2it_j}{1+t_j^2},\qquad t_j\in\mathbb Q,
\]
within
\[
\frac1{100n^2K}.
\]
Form the real Fourier matrix with rows
\[
1,\quad \operatorname{Re}z_j^k,\quad \operatorname{Im}z_j^k,
\qquad 1\le k\le K.
\]
It is a quantitatively small perturbation of the real discrete Fourier matrix. Rational Gaussian elimination gives positive rational weights satisfying
\[
\sum_j\omega_j=1,\qquad
\sum_j\omega_j z_j^k=0\quad(1\le |k|\le K).
\]

Tensor this quadrature over three coordinates and clear denominators. We obtain finitely many spatial translations \(\theta_\ell\) and positive integer multiplicities \(m_\ell\) such that
\[
\sum_\ell m_\ell T_{\theta_\ell}q=0                              \tag{2.7}
\]
for every mean-zero Fourier polynomial supported in the box above.

The translations need not be represented by rational angles. Their unit-circle coordinates are rational, so every integer Fourier phase has rational real and imaginary parts. Translated fields therefore remain ordinary rational combinations of the fixed sine/cosine partners.

This entire quadrature, including its possibly enormous integer multiplicities, is fixed precomputation.

## 2.4 The new contracting word

Concatenate the translated words with these multiplicities.

Translation commutes with \(D\), so each translated linear word still has leading term \(e^{s^4D}\). Equation (2.7) cancels the direct affine coefficients through order four.

The composition does not recreate lower-order affine terms: a completed linear word differs from \(I\) by \(O(s^4)\), and an affine bias is \(O(s)\), so their cross contribution is \(O(s^5)\).

The resulting fixed superword has
\[
\boxed{
\overline W(s)=e^{J_0s^4D}+O_{H^m\to H^m}(s^5),
\qquad
\overline b(s)=O_{H^m}(s^5),
}                                                               \tag{2.8}
\]
where \(J_0=\sum_\ell m_\ell\) is fixed.

Its underlying transport is still exactly the identity.

Let \(a_\nu\) be the continuous affine correction along \(n\) repeated superwords:
\[
(a_\nu)_t+L_wa_\nu=\nu\Delta w,\qquad a_\nu(0)=0.
\]
Stable repetition gives, uniformly for \(0<\nu\le1\),
\[
\sup_t\|a_\nu(t)\|_{H^m}
\le C(s+ns^5)e^{Cns^5},                                        \tag{2.9}
\]
and
\[
\|a_\nu(\delta)\|_{H^m}
\le Cns^5e^{Cns^5}.                                             \tag{2.10}
\]

Thus the force \(w_t\), which contains no viscosity, has the same useful contracting word together with a uniformly controllable affine correction.

## 2.5 Explicit polynomial word parameters

For an incoming velocity bound \(K\ge1\), desired \(L^2\) accuracy \(e\le1\), and allowed partial affine size \(r\le1\), choose
\[
\gamma=\frac{e}{C(K+1)},\qquad
q_a=\min(\gamma,r,\mu_0),
\]
\[
T_a=C\gamma^{-4},\qquad
s=\min\left(s_0,\frac{q_a}{C(T_a+1)}\right),
\qquad
n=\left\lceil T_a/s^4\right\rceil.                              \tag{2.11}
\]
Here \(C,s_0\) are fixed effective constants, with fixed safety margins.

These choices give
\[
\|\overline W(s)^n\|_{H^1\to L^2}\le\gamma,
\]
\[
\sup_t\|a_\nu(t)\|_{H^6}\le \min(r,\mu_0)/100,
\qquad
\|a_\nu(\delta)\|_{H^6}\le e/100.                                \tag{2.12}
\]

For example, direct substitution gives
\[
n\le C\left(
\gamma^{-24}
+\gamma^{-20}r^{-4}
+\gamma^{-20}\mu_0^{-4}
\right).                                                       \tag{2.13}
\]
There is no variable exponent.

Run this word in a prescribed rational time \(\delta\), using the rational quadratic velocity pulse \(6z(1-z)\) on each leg. The emitted force is its derivative. Consequently,
\[
\sup_t\|w_t\|_{W^{1,\infty}}
\le C s n^2\delta^{-2}.                                         \tag{2.14}
\]
All spatial constants and the superword length are fixed and included in \(C\).

## 2.6 The coupled reset estimate survives

Use the reference \(w+a_\nu\), but retain the interaction coordinates generated by \(w\). The exact smooth residual is
\[
\boxed{
f-\bigl[(w+a_\nu)_t-\nu\Delta(w+a_\nu)
       +\mathcal B(w+a_\nu,w+a_\nu)\bigr]
=
\nu\Delta a_\nu-\mathcal B(a_\nu,a_\nu),
\quad f=w_t.
}                                                               \tag{2.15}
\]
The large cross term \(L_wa_\nu\) cancels exactly.

The additional velocity and induction operators are \(L_{a_\nu}\) and \(C_{a_\nu}\). Their coefficients are small by (2.12). Their bounds use only the fixed Sobolev constants and \(\mu_0\).

The accepted coupled reset energy argument therefore applies with \(\nu_0,\rho_0\) as lower coercivity bounds. Its separate velocity estimate retains the Lorentz contribution
\[
C\nu_0^{-1}\rho_0^{-1/2}K_\star^4\delta^{1/2}.                  \tag{2.16}
\]

One concrete reset schedule is
\[
\sigma=
\min\left\{\frac{d_{\rm bud}}4,\,
c\mu_0^7r_0^8K_\star^{-20}\right\},
\]
\[
e=c\nu_0r_0\sigma,
\]
\[
\delta=
\min\left\{\frac{d_{\rm bud}}4,\,
c\mu_0^3r^4e^4K_\star^{-12}\right\}.                              \tag{2.17}
\]
Run the new word in time \(\delta\), then use zero force for time \(\sigma\).

The affine endpoint is included in the \(e\)-budget. Heat smoothing uses
\[
\|u(\delta+\sigma)\|_{H^1}
\le
C\frac{\|u(\delta)\|_2}{\sqrt{\nu_0\sigma}}
+C\nu_0^{-7/8}\sigma^{1/8}K_\star^2.                             \tag{2.18}
\]
Thus the same prescribed reset makes the velocity \(H^1\)-small for every actual pair.

For the first reset, use the accepted initial-ball version, replacing its viscosities in lower bounds by \(\nu_0,\rho_0\). The magnetic endpoint remains bounded by a fixed multiple of \(M_0+1\), independently of the reset accuracy.

---

# 3. Exact-return references for the magnetic stirring pulse

Use the supplied polynomial
\[
r(z)=3z^2-20z^3+45z^4-42z^5+14z^6.
\]
The emitted force is
\[
\boxed{
f(t)=A h^{-2}r''(t/h)F,
}                                                               \tag{3.1}
\]
where
\[
r''(z)=6-120z+540z^2-840z^3+420z^4.
\]
It is rational and has degree four.

For an arbitrary actual viscosity, let \(x_\lambda\) and
\(\alpha_\lambda=\int x_\lambda\) be the supplied scalar Stokes solution, where
\[
\lambda=\nu\kappa^2,\qquad 0<\lambda\le49.
\]
These functions are used only in the proof.

The supplied endpoint estimates are approximate. We convert them into an **exact-return reference with a small smooth residual**.

Put
\[
b=\alpha_\lambda(h),\qquad d=x_\lambda(h),
\]
and define
\[
\phi(z)=3z^2-2z,\qquad \psi(z)=3z^2-2z^3,
\]
\[
q_\lambda(t)=d\,\phi(t/h)+\frac bh\,\psi'(t/h).
\]
Because
\[
\phi(0)=0,\quad \phi(1)=1,\quad \int_0^1\phi=0,
\]
and
\[
\psi(0)=0,\quad\psi(1)=1,\quad
\psi'(0)=\psi'(1)=0,
\]
the corrected amplitude
\[
\bar x_\lambda=x_\lambda-q_\lambda
\]
satisfies
\[
\boxed{
\bar x_\lambda(0)=\bar x_\lambda(h)=0,
\qquad
\int_0^h\bar x_\lambda(t)\,dt=0.
}                                                               \tag{3.2}
\]

Hence both the Euler and induction propagators of the reference carrier
\[
\bar w_\nu(t)=\bar x_\lambda(t)F
\]
return exactly to the identity.

The actual output remains (3.1). Its difference from the force required by this reference is
\[
q_\lambda'+\lambda q_\lambda.
\]
Using the supplied endpoint bounds,
\[
\boxed{
\|q_\lambda'+\lambda q_\lambda\|_\infty
\le C|A|\,49^3 h
}                                                               \tag{3.3}
\]
for \(49h\le1\).

This residual is uniformly small as \(h\) decreases. It is included in the local mechanical error estimate during the stirring phase. It need not be forced below a later, \(h\)-dependent global tolerance.

The corrected displacement satisfies
\[
\|\bar\alpha_\lambda-Ar(\cdot/h)\|_\infty
\le C|A|\,49h.                                                   \tag{3.4}
\]
After reducing one fixed upper bound on \(h\),
\[
\int_0^1\bar\alpha_\lambda(hz)^2\,dz
\ge \frac{3A^2}{40040}.                                         \tag{3.5}
\]

## Uniform scalar magnetic average

The corrected profile is linear in \(A\). All fundamental shears have the same eigenvalue \(\lambda=\nu\kappa^2\). Therefore the two signs, sine/cosine pair and three cyclic orientations use the same scalar profile.

The full conjugated diffusion average is exactly
\[
\boxed{
\overline A_{\nu,\rho}
=
\rho\left[
1+\frac{\kappa^2a^2}{6}
\int_0^1\bar r_{\lambda,h}(z)^2\,dz
\right]\Delta,
\qquad
\bar r_{\lambda,h}(z)=\frac{\bar\alpha_\lambda(hz)}a.
}                                                               \tag{3.6}
\]
There is a fixed rational \(\gamma_*>0\), for instance a sufficiently small power of two, such that its mean-zero heat gap is at least
\[
g=\gamma_*\rho_0a^2.                                             \tag{3.7}
\]

The averaged operator varies with the actual parameters. Its lower gap, coefficient bounds, ellipticity and fixed-order smoothing bounds are uniform. Those bounds, rather than a parameter evaluation, determine the schedule.

---

# 4. Fixed-depth lowering without viscosity-dependent coefficients

At one lowering step, let
\[
\zeta(t)=b(t)\xi
\]
be the usual zero-integral cubic velocity excursion. The output is now
\[
\boxed{f_{\rm low}=\zeta_t+g_0.}                                 \tag{4.1}
\]
There is no \(-\nu\Delta\zeta\) term.

For each actual viscosity, define only in the proof
\[
(\theta_\nu)_t
=
\nu\Delta\zeta-\mathcal B(\zeta,\zeta)-g_1,
\qquad \theta_\nu(0)=0.                                         \tag{4.2}
\]
Use
\[
u=\zeta+\theta_\nu+Qz,\qquad B=\mathcal M b,
\]
where \(Q,\mathcal M\) are generated by the scalar carrier \(\zeta\).

The new viscous primitive is especially simple:
\[
\int_{t_I}^t\nu\Delta\zeta(s)\,ds
=
\nu\Delta\xi\int_{t_I}^t b(s)\,ds.                               \tag{4.3}
\]
It returns exactly to zero at every complete carrier cell.

If the carrier amplitude is \(A\), cell width is \(\ell\), and the quadratic cell-average mismatch is at most \(\delta_0\), then
\[
\sup_t\|\theta_\nu(t)\|_{H^k}
\le C\left[\delta_0+\ell(A^2+A)\right],                          \tag{4.4}
\]
uniformly for \(\nu\le1\). The potentially dangerous term obeys
\[
\|L_\zeta\theta_\nu\|_{H^s}
\le CA\left[\delta_0+\ell(A^2+A)\right].                          \tag{4.5}
\]

The amplitude is chosen from a desired average quadratic force, so it does not increase when \(\ell\) is reduced. The accepted noncircular tolerance choice therefore still makes every residual and conjugation defect polynomially small.

The large, unknown derivative \((\theta_\nu)_t\) cancels exactly in the transformed equation. It is never output.

The signed quadratic certificates are unchanged. In particular, opposite quadratic signs use the distinct carriers \(a+b\) and \(a-b\), rather than an invalid attempt to reverse a square by changing its overall sign.

The magnetic transformed equation remains
\[
b_t
=
\rho\mathcal M^{-1}\Delta\mathcal M b
-
C_{\mathcal M^{-1}\theta_\nu+\mathcal M^{-1}Qz}b
+\mathcal M^{-1}h_B.                                             \tag{4.6}
\]
No additive magnetic control appears.

All diffusion and bilinear commutator estimates from the accepted lowering proof remain valid. Their upper bounds use \(1\), and their coercivity thresholds use \(\nu_0,\rho_0\).

The lowering depth is the fixed depth of the enlarged erasing catalogue. Outer interval endpoints are preserved exactly.

---

# 5. The target writer has exact affine cancellation

This step does not require an additional spatial averaging grid or additional algebraic depth.

From (2.2),
\[
\mathcal A_F^\nu(a)v=Q_F(a)v+\nu a\Delta F,
\qquad Q_F(a)=e^{-aL_F}.
\]
Since \(Q_F(a)\Delta F=\Delta F\),
\[
\mathcal A_F^\nu(a)\mathcal A_F^\nu(b)
=\mathcal A_F^\nu(a+b),
\qquad
\bigl(\mathcal A_F^\nu(a)\bigr)^{-1}
=\mathcal A_F^\nu(-a).                                          \tag{5.1}
\]

Let a forward shear word have affine map
\[
\mathcal A^\nu z=Sz+\nu d.
\]
If \(\mathcal T_g z=z+g\), then
\[
\boxed{
\mathcal A^\nu\mathcal T_g(\mathcal A^\nu)^{-1}z
=z+Sg.
}                                                               \tag{5.2}
\]
The viscosity-dependent shift cancels exactly.

This is where the assumption that the unknown viscosity is constant in time is used.

## 5.1 A two-shear Bessel leaf

For
\[
S=Q_G(b)Q_F(a),
\]
use the chronological sequence
\[
G(-b),\quad F(-a),\quad \text{seed }g,\quad F(a),\quad G(b).        \tag{5.3}
\]
The reference endpoint is exactly \(z+Sg\) for every constant \(\nu\).

For a carrier leg of duration \(\ell\), use
\[
q(z)=6z(1-z),
\]
\[
w(t)=\frac a\ell q\!\left(\frac{t-t_0}{\ell}\right)F,
\qquad
\boxed{
f(t)=w_t
=\frac a{\ell^2}q'\!\left(\frac{t-t_0}{\ell}\right)F.
}                                                               \tag{5.4}
\]
During the seed interval, set \(w=0\) and emit
\[
\boxed{
f(t)=\frac1\ell q\!\left(\frac{t-t_0}{\ell}\right)g.
}                                                               \tag{5.5}
\]

Every accepted two-shear Bessel leaf can be put in this literal forward/inverse form. Its homogeneous Euler and magnetic propagators both return exactly to \(I\).

Round phase fields and seed coefficients before constructing a leaf, and reuse the identical rounded shear on its inverse leg. The identities above remain exact for any rational sine/cosine combination with the same shear orientation.

## 5.2 Uniform nonlinear MHD estimate for the leaf

For the actual parameter, define the reference
\[
u_*=w+v_\nu,\qquad B_*=0,
\]
where
\[
(v_\nu)_t+L_wv_\nu=\nu\Delta w+f_{\rm seed}.
\]
Equation (5.2) gives its prescribed endpoint independently of \(\nu\).

If \(K_m(A)\) bounds the partial shear propagators and inverses for
\[
A=1+|a|+|b|,
\]
then
\[
\sup_t\|v_\nu(t)\|_{H^m}
\le
K_m(A)^2\left(
\|z\|_{H^m}+\|g\|_{H^m}+CA
\right).                                                       \tag{5.6}
\]
This is polynomial and independent of the compressed duration.

The sole smooth reference residual is
\[
\boxed{
\nu\Delta v_\nu-\mathcal B(v_\nu,v_\nu).
}                                                               \tag{5.7}
\]
All large carrier terms have cancelled.

Removing the carrier propagators from the actual pair error gives
\[
E'
+P^{-1}\bigl(\|\widetilde e\|_{H^2}^2
            +\|\widetilde b\|_{H^2}^2\bigr)
\le P(E+E^3+1+\eta^2),                                         \tag{5.8}
\]
where \(P\) is a fixed computable polynomial in the known smooth envelopes, the impulses and \(\mu_0^{-1}\).

For a suitably short rational duration \(h\),
\[
E_{\rm out}^{1/2}
\le
(1+Ph)E_{\rm in}^{1/2}
+P\sqrt h(1+\eta).                                               \tag{5.9}
\]
At the endpoint, the interaction-coordinate norm is the physical pair norm because both return maps are exactly \(I\).

No operator-norm assertion that diffusion is close to \(I\) on the \(H^1\) ball is used.

## 5.3 Quadratic holds

The quadratic holds already have parameter-independent force: it is zero.

For a desired dose \(-\lambda\mathcal B(\xi,\xi)\), translate to \(z+\alpha\xi\), hold for time \(h\), and translate back, with \(h\alpha^2\) approximating \(\lambda\).

During the hold use the reference
\[
(v_\nu)_t+L_{\alpha\xi}v_\nu
=
\nu\alpha\Delta\xi-\alpha^2\mathcal B(\xi,\xi).
\]
Its integrated transport parameter is
\[
h|\alpha|=\sqrt{\lambda h}.
\]
The viscosity term contributes at most a fixed polynomial times \(\sqrt h\), uniformly for \(\nu\le1\). The remaining reference residual again has form (5.7).

Thus the supplied two-stage quadratic synthesis is retained. There is no frequency-dependent extra depth, and no \(h\alpha^4\) estimate is needed.

---

# 6. Uniform joint erasure and one common schedule

The preceding modifications fit the coupled stability proof of the accepted MHD construction with uniform constants.

Here is an explicit parameter order.

Choose fixed effective constants \(C_*,c_*>0\), with the usual fixed safety margins, and set
\[
q=c_*X^{-10},\qquad K_0=C_*(M_0+1).
\]
Choose
\[
a=
\left\lceil
\frac{C_*K_0}{\gamma_*\rho_0\tau_0q}
\right\rceil,
\qquad
g=\gamma_*\rho_0a^2.                                             \tag{6.1}
\]

Let
\[
\Gamma=C_*(2+a+\nu_0^{-1}+\rho_0^{-1})^{d_*}                     \tag{6.2}
\]
dominate all fixed-order coefficient, inverse ellipticity, local energy and smoothing bounds. Both \(C_*,d_*\) are fixed precomputation outputs.

Set
\[
T=\min\left\{\frac{\tau_0}{100},
             \frac1{100\Gamma},
             \frac1{100g}\right\},
\qquad
\mathcal J=\frac{100\Gamma}{T^2},                                \tag{6.3}
\]
\[
r=\frac{q}{100\Gamma\mathcal J K_0},
\qquad
r_0=\frac{r}{100\Gamma^2},
\qquad
K_\star=100\Gamma K_0,                                          \tag{6.4}
\]
\[
\beta=\min\left\{\frac1{1000},
                 \frac{gT}{10^6\Gamma^8}\right\}.                \tag{6.5}
\]

Take the magnetic excursion duration to be the rational minimum
\[
h=\min\left\{
\frac{T}{1000},
\frac{gT^2}{10^6\Gamma^8},
\left(\frac{r}{10^6\Gamma^8K_0^2}\right)^8,
h_{\rm fixed},
\frac1{C_*a}
\right\},                                                       \tag{6.6}
\]
where the fixed \(h_{\rm fixed}\) and the last cap ensure the regime of Section 3 and a corrected-reference residual at most a reserved fixed fraction of one.

After each magnetic excursion, insert the uniform reset (2.17), with its total duration bounded by \(\beta h\).

These choices are triangular. The magnetic coefficient envelope does not depend on the number or compression of the reset word: the word’s underlying maps return exactly, and its partial maps have fixed bounds.

## 6.1 Operator-norm contraction, uniformly in the rectangle

On a short macro interval, the two-sided smoothing telescope from the accepted construction gives, for every actual pair,
\[
\|U_{\nu,\rho}-e^{T_b\overline A_{\nu,\rho}}\|_{H^1\to H^1}
\le
C\Gamma^8\left(\frac{\ell}{T_b}+\beta\right),                    \tag{6.7}
\]
where \(\ell\) is the actual microcycle duration and \(T_b\) is an integer number of microcycles with
\[
T/2\le T_b\le T.
\]

The estimate uses only uniform spatial coefficient bounds and coercivity. It uses no time derivative of the fast coefficient schedule and no derivative with respect to \(\nu\) or \(\rho\).

Equations (6.5)–(6.6), together with the uniform heat gap (3.7), give
\[
\|U_{\nu,\rho}\|_{H^1\to H^1}
\le1-\frac{gT_b}{16}                                             \tag{6.8}
\]
with room reserved for lowering errors.

Repeat the macro
\[
n_b=\left\lceil\frac{256K_0}{qgT_b}\right\rceil                  \tag{6.9}
\]
times. Its homogeneous magnetic endpoint is then at most \(q/(16K_0)\) in \(H^1\)-operator norm.

The total magnetic-erasure time satisfies
\[
n_bT_b\le \frac{256K_0}{qg}+T.
\]
The amplitude choice (6.1), with its fixed safety constant, places this within a small fixed fraction of \(\tau_0\).

## 6.2 Closing the Lorentz–induction estimates

During a stirring phase the corrected reference has a mechanical residual bounded by a fixed constant. The local coupled energy estimate and the separate velocity estimate give
\[
\sup_{I_h}\|u-\bar w_\nu\|_{H^1}
\le \Gamma r_0+\Gamma K_\star^2h^{1/4}<r/8.                     \tag{6.10}
\]
The following uniform reset restores the entrance level \(r_0\).

During a reset, the affine correction of Section 2 is included in the velocity perturbation. Its partial norm is below the allocated fraction of \(r\). Thus the same bound on the actual perturbation velocity holds through the complete schedule.

For the magnetic interaction coordinate \(b\),
\[
\|\mathcal M^{-1}C_v(\mathcal M b)\|_{H^{-3/4}}
\le \Gamma\|v\|_{H^1}\|b\|_{H^1}.
\]
Uniform forward bounds and smoothing give a kernel whose integral is at most \(\mathcal J\). The global Duhamel estimate is therefore
\[
\sup_t\|b(t)\|_{H^1}
\le
4K_0+
\Gamma\mathcal J
\left(r\sup_t\|b(t)\|_{H^1}+\eta_{\rm eff}\right).                \tag{6.11}
\]

Choose
\[
\eta_0=
\min\left\{
1,\frac{q}{100\Gamma\mathcal J},c_*\mu_0q
\right\}.                                                       \tag{6.12}
\]
Equations (6.4) and (6.11) close the magnetic bootstrap for every actual pair. This magnetic bound supplies the Lorentz budget used in the velocity estimates, so the argument is coupled.

The first reset brings the initial velocity down to \(r_0\), leaving magnetic \(H^1\) norm at most \(K_0\). The final reset and magnetic contraction then give
\[
\boxed{\|(u,B)\|_{\mathcal H^1}\le q.}                            \tag{6.13}
\]

All forces in this joint eraser are shared across the entire parameter rectangle.

## 6.3 Lowering the nominal force

The nominal joint eraser uses one fixed enlarged catalogue. Apply Section 4 at its fixed depth.

Choose the lowering tolerance after the nominal schedule is fixed, below the finite list of:

- viscous and resistive coercivity margins;
- the macro gap \(gT_b\);
- reset endpoint tolerances;
- the small-velocity margin;
- the final \(q\)-budget.

Their reciprocals are polynomial in the numerical parameters already selected. The signed-scale perturbation estimate for the magnetic propagator preserves (6.8), and the coupled energy estimates preserve (6.10)–(6.13).

The physical output after lowering uses exactly the twelve prescribed fields.

---

# 7. Arbitrary variable targets and the exact final time

Truncate at
\[
N=\left\lceil\frac{16M_0}{\epsilon_0}\right\rceil.
\]
The \(H^1\) promise gives
\[
\|V-V_N\|_2\le M_0/N\le\epsilon_0/16.                            \tag{7.1}
\]

Canonicalize and coalesce retained modes exactly. Round their coefficients with a prescribed \(H^1\) error budget, preserving solenoidality with the rational projector
\[
P_k=I-\frac{k\otimes k}{|k|^2}.
\]
Obtain a target \(\widetilde V_N\) with
\[
\|V-\widetilde V_N\|_2\le\epsilon_0/8.                           \tag{7.2}
\]

The accepted Bessel and depth-two quadratic compiler supplies the finite algebraic program for \(\widetilde V_N\). Implement each leaf by Section 5.

The ordering remains noncircular:

1. choose the finite algebraic certificates;
2. choose hold durations and carrier amplitudes through the fixed two levels;
3. choose Bessel directional accuracy and rational phase fields;
4. count the leaves;
5. choose their durations from the uniform estimate (5.9).

Shortening a leaf does not change its phase catalogue or seed direction.

Allocate the errors so that the total multiplicative pair amplification is at most two and the total additive error is at most \(\epsilon_0/4\). From an entrance pair \(H^1\) norm at most \(2q\), the writer then gives
\[
\|(u_{\rm out}-\widetilde V_N,B_{\rm out})\|_{\mathcal H^1}
\le4q+\epsilon_0/4.                                             \tag{7.3}
\]

Its duration is chosen at most \(\tau_0/4\).

Between the joint eraser and the writer, insert zero force for the remaining time. Since \(q\ll\mu_0\) and \(\eta\le c_*\mu_0q\), the small-data MHD energy estimate keeps the pair within \(2q\) during this wait.

Place the writer so that its endpoint is exactly the input time \(\tau\). The waiting length is a known nonnegative rational number.

Combining (7.2) and (7.3),
\[
\begin{aligned}
\|(u(\tau)-V,B(\tau))\|_{\mathcal H^0}
&\le
\|(u(\tau)-\widetilde V_N,B(\tau))\|_{\mathcal H^1}
+\|\widetilde V_N-V\|_2\\
&\le4q+\epsilon_0/4+\epsilon_0/8\\
&<\epsilon.
\end{aligned}                                                    \tag{7.4}
\]

Take the output disturbance tolerance to be a fixed reserved fraction of \(\eta_0\), allowing the inherited rational approximation budgets.

---

# 8. Every Leray–Hopf realization and every real parameter pair

Fix an arbitrary
\[
(\nu,\rho)\in[\nu_0,1]\times[\rho_0,1],
\]
an arbitrary admitted initial pair, and an arbitrary admitted disturbance pair.

For this actual data, construct the physical local strong MHD solution. The estimates above are uniform a priori bounds and permit continuation through the complete prescribed schedule:
\[
(u,B)\in
L^\infty(0,\tau;H^1)\cap L^2(0,\tau;H^2).                        \tag{8.1}
\]

Weak–strong uniqueness in the original equations identifies every energy-admissible Leray–Hopf realization with this strong solution. The disturbances cancel in that comparison because they are the same actual disturbances on both sides.

Its qualitative Gronwall factor does not select the disturbance tolerance: polynomial robustness has already been proved directly for the actual strong solution.

The strong solution has a continuous \(L^2\) trace. Therefore (7.4) holds for the specified one-sided total-energy trace.

The force and \(\eta\) were fixed before this arbitrary parameter pair was chosen. Since every estimate used the same bounds (1.1), the conclusion is simultaneous over the entire rectangle, including irrational parameter values. No finite parameter sampling, parameter-continuity cover or selection of controls is involved.

---

# 9. Polynomial numerical and binary resources

The modifications require recomputing the resource bounds; the known-parameter exponent is not reused without accounting for the new operations.

## 9.1 Numerical ledger

All numerical design variables are obtained by a fixed sequence of sums, products, fixed powers, rational minima and ceilings.

The new costs are explicitly polynomial:

- The affine eraser has the count bound (2.13) and force bound (2.14).
- Magnetic stirring uses degree-four force of size \(Ca h^{-2}\).
- Its additional pulse caps have reciprocal bounded by a fixed polynomial in \(a\).
- The lowering correction adds the term \(A\ell\) to the existing \(A^2\ell\) bound; its depth remains fixed.
- Target leaves retain their fixed two-shear structure, with the additional reference envelope (5.6), which is polynomial in the impulses.
- The target’s quadratic depth remains two.
- The number of retained target modes and all certificate and Bessel counts are polynomial in \(N,M_0,\epsilon_0^{-1}\), hence in \(R\).

Repeated words reuse the same parameters. Their stability is controlled by \(ns^5\), not by exponentiating their total absolute strain. Completed target leaves return exactly, so their polynomial partial-propagator bounds are not multiplied once per leaf.

These facts yield a computable polynomial
\[
E_{\rm phys}(R)
\]
bounding
\[
\eta^{-1},\qquad \sup_t\|f(t)\|_{W^{1,\infty}}.
\]
Because \(\tau\le1\), the same envelope bounds the force integral.

No numerical bound uses the raw denominator heights of the input target. Those heights affect arithmetic costs only.

## 9.2 Binary ledger

The implementation maintains a separate bit-height bound.

- Input parameter intervals are read exactly; only their coarse lower bounds enter numerical control design.
- Large input wavevectors are compared directly with \(N^2\) and discarded when appropriate.
- Retained equal modes are coalesced before using numerical coefficient bounds.
- Tiny target coefficients are rounded with absolute error budgets and are never inverted merely because they are nonzero.
- Root, Bessel and trigonometric calculations use controlled dyadic precision.
- Rational phase fields are rounded once and reused on inverse legs.
- Repeated knots are computed from integer indices and stored rational interval lengths.
- The parameter formulas and the lowering recursion have fixed depth.
- Ordinary time-polynomial expansion is charged explicitly.

Thus polynomially many arithmetic operations are accompanied by polynomial bounds on operand lengths. This is not inferred solely from numerical magnitudes.

The final time-polynomial degree is at most four. All coefficients are ordinary rationals.

These rules produce a computable polynomial
\[
E_{\rm bit}(L+R)
\]
for bit operations, working-memory bits, output bits, interval count and individual numerator/denominator bit lengths.

## 9.3 Fixed precomputation and the actual \(A,p\)

The precomputation is finite and input-independent:

1. Run the accepted fixed-family, word and saturation precomputation.
2. Construct the rational spatial quadrature of Section 2.
3. Form the translated superword and compute its fixed Taylor and Sobolev bounds.
4. Add the explicit pulse-correction bounds from the fixed polynomials \(r,\phi,\psi\).
5. Add the affine-palindrome and modified-lowering bounds.
6. Propagate numerical and binary majorants through the compiler.

All new constants arise from finite Fourier coefficient bounds, finite differentiation, rational linear algebra, the supplied effective propagator estimates, and elementary inequalities. There is no spectral, norm or PDE oracle.

Let
\[
p=\max\{1,\deg E_{\rm phys},\deg E_{\rm bit}\}.
\]
After substituting the fixed comparison \(X\le CR\), compute the coefficient sums of both nonnegative-coefficient envelopes. Include the recorded fixed precomputation cost and table sizes.

An integer \(A\) above these quantities, with a fixed explicit allowance for computing \(A,p\) themselves, gives
\[
\boxed{
\begin{gathered}
\text{compiler bit operations, memory bits, output bits, interval count,}\\
\text{degrees and individual rational bit lengths}
\le A(L+R)^p,
\\[2mm]
\eta^{-1},\quad
\sup_{0\le t\le\tau}\|f(t)\|_{W^{1,\infty}},\quad
\int_0^\tau\|f(t)\|_{W^{1,\infty}}\,dt
\le AR^p.
\end{gathered}}                                                  \tag{9.1}
\]

This specifies fixed computable integers \(A,p\), including the full fixed preprocessing. Their computation is performed before any variable input is read.

---

# 10. What the compiler actually emits

The parameter-independent force formulas are:

| Operation | Emitted mechanical force |
|---|---|
| Uniform erasing word | \(w_t\) |
| Magnetic stirring excursion | \(A h^{-2}r''(t/h)F\) |
| One lowering step | \(\zeta_t+g_0\) |
| Target shear-conjugation leaf | \(w_t+f_{\rm seed}\) |
| Quadratic hold or waiting interval | \(0\) |

After fixed-depth lowering, every force lies in the span of the twelve stated fundamental mechanical fields.

The actual \(\nu,\rho\) occur only in the proof references and the equations being estimated. They do not occur in the emitted coefficients, the selected clock, the target catalogue, or the disturbance tolerance.

Therefore, from the accepted constructions, this yields **one total deterministic polynomial compiler with the full continuum-parameter, common-initial-ball, robust all-weak contract posed in the question**.

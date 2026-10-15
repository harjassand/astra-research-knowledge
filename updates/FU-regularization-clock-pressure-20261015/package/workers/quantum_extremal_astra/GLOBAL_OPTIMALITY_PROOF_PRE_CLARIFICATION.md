# Candidate sharp Pauli regularization theorem — independent derivation

**Status, 2026-10-15:** internally derived candidate theorem, ready for independent mathematical audit. The decimal and finite LP checks are diagnostics. The argument below is an analytic dual certificate; its validity does not rely on those checks. No historical novelty claim is made.

**Scope:** normalized Pauli matrices, all three coordinates, a positive scalar noise probability law, and the exact identity

\[
\widehat M(t)=\widehat\nu(t)e^{i t\cdot\sigma}\qquad(t\in\mathbb R^3).
\]

The noise is centered and radial and has every exponential moment. The measurement is a positive normalized qubit POVM. The variance is \(\operatorname{Cov}(\nu)=vI_3\).

## 1. Statement and constants

Let \(h_0(s)=1\) for \(0\le s\le2\). For \(s>2\), extend it by the delay equation

\[
2(s-1)h_0'(s)+h_0(s)+h_0(s-2)=0.                 \tag{1}
\]

Equivalently, including \(s=2\),

\[
2(s-1)h_0(s)=\int_{s-2}^{s}h_0(u)\,du.         \tag{2}
\]

Put

\[
K=\int_1^\infty h_0(s)\,ds,
\qquad c=(4K+2)^{-1},
\qquad v_*={23\over9}-{2c\over9}.              \tag{3}
\]

**Candidate theorem.** Every law in the stated scope has \(v\ge v_*\), and equality is attained by

\[
\nu(ds,d\omega)=2cs h_0(s)\,ds\,{d\Omega(\omega)\over4\pi},
\]

with the positive POVM

\[
M(dr,dn)=q(r)\,dr\,{I+n\cdot\sigma\over4\pi}\,d\Omega(n),
\quad
q(r)=cr\bigl[h_0(r-1)+h_0(r+1)\bigr]\mathbf1_{r\ge1}.
                                                               \tag{4}
\]

Numerical quadrature gives

\[
K\simeq2.0497559609679565,
\quad c\simeq0.09804859909224145,
\quad v_*\simeq2.533766977979502.
\]

The exact definition is (1)–(3), not these decimals. Equality is achieved by a probability density singular like \(1/|x|\) at the origin. A smooth-density restriction would therefore require a separate attainment discussion. Smooth approximations achieve variances decreasing to \(v_*\).

## 2. Exact radial positivity reduction

First suppose scalar noise and POVM have been smoothed by an independent centered isotropic Gaussian. Let \(g(x)\) be the one-coordinate noise density. Radial scalar positivity implies

\[
g(x)=\int_{|x|}^\infty h(s)\,ds,
\qquad h(s)=-g'(s)\ge0\quad(s>0).
\]

For a radial noise density \(p(|z|)\), \(h(s)=2\pi s p(s)\). The radial noise-radius law is \(2sh(s)ds\); hence

\[
2\int_0^\infty sh(s)ds=1,
\qquad v={2\over3}\int_0^\infty s^3h(s)ds.      \tag{5}
\]

Covariance of the Fourier identity under rotations implies a polar POVM representation

\[
M(dr,dn)=[q(r)I+b(r)n\cdot\sigma]dr\,{d\Omega(n)\over4\pi},
\qquad q\ge|b|.
\]

The complete one-direction spectral-plus-noise identity, rather than only a coordinate moment condition, gives

\[
\begin{aligned}
\int_r^\infty {q(u)\over2u}\,du
 &=\tfrac12[g(r-1)+g(r+1)],\\
r\int_r^\infty {b(u)\over2u^2}\,du
 &=\tfrac12[g(r-1)-g(r+1)].
\end{aligned}                                                    \tag{6}
\]

Define

\[
\Delta_h(r)=\int_{|r-1|}^{r+1}h(s)ds.
\]

Differentiating (6) yields

\[
\begin{aligned}
A_h(r):=q(r)-b(r)&=2r h(r+1)-\Delta_h(r)\ge0\quad(r>0),\\
B_h(r):=q(r)+b(r)&=\Delta_h(r)-2r h(1-r)\ge0\quad(0<r<1).
\end{aligned}                                                    \tag{7}
\]

For \(r\ge1\), the second expression is instead
\(q+b=\Delta_h(r)+2r h(r-1)\ge0\), automatic from scalar positivity. Thus (5) and (7), with \(h\ge0\), are exactly the relevant radial inequalities. In particular, positivity of the operator-valued measure alone has not replaced positivity of \(\nu\).

## 3. Positive renewal construction and all exponential moments

Equation (1) has a unique continuous, piecewise smooth method-of-steps solution. Its integral invariant is (2). It stays strictly positive: at a hypothetical first zero above 2, (2) equates zero to an integral of previously strictly positive values. Consequently (1) shows that it decreases for \(s>2\).

For \(s\ge4\), monotonicity in (2) gives

\[
0<h_0(s)\le {h_0(s-2)\over s-1}.
\]

Iterating gives factorial decay on successive intervals of length 2. In particular, every integral \(\int e^{as}s^j h_0(s)ds\) is finite for every finite \(a\) and integer \(j\ge0\). This proves every exponential moment, not merely finite-window positivity.

For \(0<r<1\), \(h_0(1-r)=h_0(1+r)=1\) and \(\Delta_{h_0}(r)=2r\), so both expressions in (7) vanish. For \(r\ge1\), equation (2) with \(s=r+1\) makes \(A_{h_0}(r)=0\). Thus the POVM is rank one and has no radial mass below 1, exactly as in (4).

Write \(H(r)=h_0(1+r)\), and \(M_j=\int_0^\infty r^jH(r)dr\). The renewal equation becomes

\[
2rH(r)=\int_{\max(0,r-2)}^rH(u)du+G(r),
\quad G(r)=\begin{cases}r&0\le r\le1,\\2-r&1\le r\le2,\\0&r>2.\end{cases}
                                                                  \tag{8}
\]

Integrating against powers of \(r\), justified by the factorial tail, gives

\[
M_0=K,\quad M_1=K+\tfrac12,
\quad M_2=2K+1,
\quad M_3=\tfrac{16}3K+\tfrac{31}{12}.
\]

Therefore

\[
2\int_0^\infty sh_0(s)ds=4K+2,
\qquad
\int_0^\infty s^3h_0(s)ds={46\over3}K+{22\over3}.
\]

These establish normalization and (3). Also, for \(1\le r\le2\), (1) gives \(H(r)=2/\sqrt r-1\). Consequently

\[
K>\int_0^1 1\,dr+\int_1^2(2/\sqrt r-1)dr
  =4\sqrt2-4>\tfrac32,
\qquad 0<c<\tfrac18.                          \tag{9}
\]

To verify the full transform identity of the explicit construction, set \(g(x)=c\int_{|x|}^\infty h_0\). The scalar density in (4) equals
\(-r[g'(r-1)+g'(r+1)]\). The vector density obtained by differentiating the second formula in (6) equals the same \(q\), by (2) and the plateau below 2. Integrating back from infinity proves (6). Rotational covariance gives this identity for every unit direction; its Fourier transform is precisely \(\widehat\nu(t)e^{it\cdot\sigma}\) for every \(t\in\mathbb R^3\).

## 4. The positive adjoint kernel

Define for \(t\ge0\)

\[
d(t)=\exp\!\left[-\frac12\int_0^2{1-e^{-tu}\over u}du\right],
\]

and for \(r>0\)

\[
\ell(r)=\frac12\int_0^\infty e^{-rt}d(t)^{-1}dt.                 \tag{10}
\]

Every derivative exists and \(\ell\) is completely monotone. Integration by parts using

\[
(d^{-1})'(t)={1-e^{-2t}\over2t}d(t)^{-1}
\]

gives the exact adjoint renewal identity

\[
2r\ell(r)-\int_r^{r+2}\ell(u)du=1,
\qquad 2r\ell'(r)+3\ell(r)=\ell(r+2).           \tag{11}
\]

The boundary at infinity in this integration by parts vanishes for every \(r>0\); the boundary at zero is \(d(0)^{-1}=1\).

For \(t>0\),

\[
d(t)^{-1}=e^{\gamma/2}\sqrt{2t}\exp[\tfrac12 E_1(2t)].
\]

Let \(Q=\sqrt{2\pi}e^{\gamma/2}\). As \(r\downarrow0\),

\[
\ell(r)={Q\over4r^{3/2}}+O(1).
\tag{12}
\]

The remainder is bounded because \(d(t)^{-1}-e^{\gamma/2}\sqrt{2t}\) is integrable in \(t\): it is bounded at zero and decreases exponentially times a power at infinity.

For later bounds, \((\log d^{-1})'\le1\) and also \((\log d^{-1})'\le1/(2t)\). Therefore \(d(t)^{-1}\le e\) for \(0\le t\le1\), and \(d(t)^{-1}\le e\sqrt t\) for \(t\ge1\). In particular

\[
-\ell'(1)
 =\tfrac12\int_0^\infty t e^{-t}d(t)^{-1}dt
 \le {e\over2}\left(1+\Gamma(5/2)\right)
 ={e\over2}\left(1+{3\sqrt\pi\over4}\right)<{16\over5}.          \tag{13}
\]

The final strict numerical inequality can, for example, be checked with rational bounds \(e<2.72\), \(\pi<22/7\); it is not based on quadrature of \(\ell\).

Set

\[
w(s)=\int_{1-s}^{1+s}\ell(u)du\quad(0\le s<1).
\]

The constant in (3) satisfies

\[
K=\int_0^1w(s)ds.                              \tag{14}
\]

For completeness: let \(\mathcal H(t)=\int e^{-tr}H(r)dr\). Transforming (8) gives
\((\mathcal H/d)'=-\widehat G/(2d)\), with
\(\widehat G(t)=(1-e^{-t})^2/t^2\). Since \(H(0)=1\), \(\mathcal H(t)/d(t)\to0\) as \(t\to\infty\). Thus

\[
K={1\over2}\int_0^\infty{(1-e^{-t})^2\over t^2d(t)}dt.
\]

Tonelli's theorem applied to (10) and the interval defining \(w\) identifies this with (14). All integrands in this calculation are nonnegative.

## 5. Explicit dual multipliers

Define

\[
\begin{aligned}
f(s)&=s(1-s^2)-c[s+w(s)]\quad(0<s<1),\\
F(r)&=\int_0^r f(1-u)du\quad(0<r<1),\\
\kappa&=3v_*={23\over3}-{2c\over3},\\
P(r)&={r^2\over2}+2r+{2\over3}+{c\over3}+{4c\over3}\ell(r).
\end{aligned}
\]

By (3) and (14), \(\int_0^1 f=1/4-c(1/2+K)=0\), so \(F(0)=F(1)=0\). Now set

\[
U(r)=\begin{cases}P(r)+F(r)/(3r^2)&0<r<1,\\P(r)&r\ge1,\end{cases}
\]

\[
V(r)={2r f(1-r)-F(r)\over3r^2}\quad(0<r<1).
\tag{15}
\]

### 5.1 Positivity of U

Put \(J(r)=\int_{2-r}^{2+r}\ell(u)du\). By (11),

\[
w(1-r)=2r\ell(r)-1-J(r),
\]

so

\[
f(1-r)=r(2+c-3r+r^2)-2cr\ell(r)+cJ(r).          \tag{16}
\]

Using the differential identity in (11) gives

\[
{d\over dr}\bigl[F(r)+4cr^2\ell(r)\bigr]
 =r(2+c-3r+r^2)+cJ(r)+2cr\ell(r+2)>0
\quad(0<r<1).                                  \tag{17}
\]

The quantity in brackets tends to zero at zero by (12), since
\(F(r)=-cQ\sqrt r+O(r^2)\). Hence it is positive. Substituting into (15) proves \(U(r)>0\), including on \((0,1)\). For \(r\ge1\), positivity is immediate from \(P\).

### 5.2 Positivity of V

Let \(G_*(r)=F(r)-2rf(1-r)\). It tends to zero at both endpoints 0 and 1. Differentiating (16), and using (11), gives

\[
{G_*'(r)\over r}
 =-6-3c+15r-7r^2
  -c\left[{J(r)\over r}+2\ell(2-r)\right].       \tag{18}
\]

Let \(M_1^\ell=-\ell'(1)\). Complete monotonicity and
\(J(r)/r=\int_{-1}^1\ell(2+rt)dt\) imply

\[
{d\over dr}\left[{J(r)\over r}+2\ell(2-r)\right]
 =\int_{-1}^1t\ell'(2+rt)dt-2\ell'(2-r)
 \le\tfrac52M_1^\ell.
\]

Indeed, the integral over \(t>0\) is nonpositive; the integral over \([-1,0]\) is at most \(M_1^\ell/2\); and the last term is at most \(2M_1^\ell\), since all arguments are at least 1. Combining (9) and (13),

\[
{d\over dr}\left({G_*'(r)\over r}\right)
\ge15-14r-\tfrac52cM_1^\ell
>1-\tfrac52\cdot\tfrac18\cdot\tfrac{16}5=0.
\tag{19}
\]

Thus \(G_*'(r)/r\) is strictly increasing. Since \(G_*\) has value zero at both endpoints, it follows that \(G_*<0\) throughout \((0,1)\): the derivative has exactly one sign change, from negative to positive. Therefore \(V(r)>0\).

The apparent singularities at zero in (15) cancel. From (16)–(18),

\[
U(0+)=V(0+)=1+{c\over2}+{2c\over3}\ell(2)>0.
\]

Also \(U\) is continuous at 1, \(V(1-)=0\), and \(U(r)=O(1+r^2)\) at infinity.

## 6. Exact adjoint identity and the variance bound

For any nonnegative smooth \(h\) satisfying (5) and finite \(\int s^3h\), the dual multipliers obey

\[
\boxed{
\int_0^\infty (s^3-\kappa s)h(s)ds
 =\int_0^\infty U(r)A_h(r)dr
  +\int_0^1V(r)B_h(r)dr.
}                                                               \tag{20}
\]

Here is an explicit algebraic verification, avoiding an unrecorded boundary cancellation. From (11), direct integration of the polynomial part of \(P\) gives

\[
2rP(r)-\int_r^{r+2}P(u)du=(r+1)^3-\kappa(r+1).
\tag{21}
\]

Put \(\psi(r)=F(r)/(3r^2)\) for \(r<1\). Then

\[
V=3\psi+2r\psi',\quad \psi(1)=0,
\quad \int_r^1(V-\psi)du=-2r\psi(r).
\tag{22}
\]

After Tonelli/Fubini expansion, the coefficient of \(h(s)\) on the right of (20) is

\[
2(s-1)U(s-1)\mathbf1_{s>1}
-\int_{|s-1|}^{s+1}U(r)dr
+\mathbf1_{s<2}\int_{|s-1|}^1V(r)dr
-2(1-s)V(1-s)\mathbf1_{s<1}.
\tag{23}
\]

For \(s\ge2\), (21) immediately gives \(s^3-\kappa s\). For \(1<s<2\), the terms involving \(\psi,V\) cancel by (22), and (21) again applies. For \(0<s<1\), put \(r=1-s\). The \(\psi,V\) correction equals
\(-2r(\psi+V)=-(4/3)f(s)\). Meanwhile direct polynomial integration gives

\[
-\int_{1-s}^{1+s}P(u)du-(s^3-\kappa s)={4\over3}f(s).
\]

This proves (20) on the remaining interval. Values at the isolated dividing points do not affect the smooth-density integral.

All expanded integrals are absolutely finite: \(U\) is bounded at zero and grows at most quadratically, \(V\) is bounded, and the interval \([|s-1|,s+1]\) has length \(2\min(s,1)\). Thus the necessary bounds are controlled by \(\int(s+s^3)h\). No assumption about pointwise decay of arbitrary admissible \(h\) has entered the dual calculation.

Positivity of (7) and of (15) makes the right side of (20) nonnegative. Using (5),

\[
v={2\over3}\int s^3h\ge {2\over3}\kappa\int sh
={\kappa\over3}=v_*.
\]

For \(h=ch_0\), both terms in (20) vanish, by Section 3. Thus the bound is attained.

## 7. Extension beyond smooth scalar densities

Given any radial positive scalar law \(\nu\) in the stated scope and its positive POVM \(M\), convolve both with the same centered isotropic Gaussian of covariance \(\epsilon I_3\). Then

\[
\nu_\epsilon=\nu*\gamma_\epsilon\ge0,
\qquad M_\epsilon=M*\gamma_\epsilon\ge0,
\qquad
\widehat M_\epsilon=\widehat\nu_\epsilon e^{it\cdot\sigma}.
\]

Both acquire smooth densities; radial covariance is preserved; and the scalar noise covariance becomes \((v+\epsilon)I_3\). The preceding proof applies and gives \(v+\epsilon\ge v_*\). Letting \(\epsilon\downarrow0\) gives the desired bound for arbitrary radial scalar probability measures, including singular ones. This is a bound-extension argument; it does not assert that Gaussian smoothing retains equality.

In fact the lower-bound proof only uses finite scalar variance, not every exponential moment. To extend the claim explicitly to that larger class, one uses the standard positive-characteristic-function fact that the finite second derivative at zero of the positive scalar trace characteristic function determines its finite second moment. The all-exponential-moment scope already requested is sufficient and avoids needing that additional formulation.

A rotation average also shows that \(\operatorname{tr}\operatorname{Cov}(\nu)/3\ge v_*\) for arbitrary centered scalar noise laws satisfying the exact Pauli identity: average \(\nu\) under SO(3) and conjugate/rotate \(M\) by the corresponding spin representation. The common Pauli factor survives, positivity survives, and the averaged covariance is \(\operatorname{tr}\operatorname{Cov}(\nu)I_3/3\). This corollary concerns average noise variance; it does not assert an isotropic matrix lower bound for the original anisotropic law.

## 8. Costs, information comparison, and what remains unclaimed

Implementation of (4) is the ordinary covariant spin measurement followed by state-independent radial randomization. Since \(R\ge1\), the direction is recovered exactly as \(n=X/|X|\). Thus this experiment and the ordinary covariant spin measurement are exactly Blackwell equivalent. The optimized radius supplies an exact scalar-convolution representation, not additional quantum information.

For a unit direction, the raw second moment is \(v_*+1\simeq3.533766978\), versus 3 for the usual unbiased report \(3n\). The ratio is about 1.177922326. The radial optimum therefore remains worse for the raw linear estimator, although direction-based decoders retain the usual covariant-measurement information.

The analytic renewal definition does not itself certify a finite-bit sampler, hardware synthesis, or gate-error budget. No efficient sampling or physical implementation advantage is claimed. No historical priority review of this extremal theorem has been completed. Uniqueness of the extremizer among all nonsmooth measures is not claimed here; sharp value and attainment are the stated theorem.

## 9. Numerical provenance and failures

`extremal_numerics.py` and `extremal_numerics.json` preserve the independent exploration before root comparison. The full radial discretized LP converged toward the candidate at grid spacings 0.08, 0.04, 0.02, 0.01. It enforces finitely many constraints and truncates the tail at 16; it is not a proof or certified lower bound. The analytic certificate above supersedes that evidence for sharpness if the proof survives independent audit.

An initial numerical run failed at the endpoint of a one-parameter family because its normalization tended to zero; the endpoint was replaced by its Dickman limit. One near-endpoint adaptive quadrature emitted a slow-convergence warning. Neither calculation is used in the theorem, and the warning is not interpreted as a certified bound.

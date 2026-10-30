# L14 scalar Hessian gate: exact quartic bound, failed cubic bridge

## Scope and source

The targeted claim is the (U=0) compatible scalar inequality (17) in the pinned N901 proof source:

\[
\kappa\left\langle
\psi_{xy}(\psi_{xy}^2+\sigma^2\psi_{xx}^2)\right\rangle^2
\le 4\sigma^2\langle\psi_{xx}^2\rangle
\left\langle J_r\!\begin{pmatrix}
\psi_{xy}&\psi_{yy}\\-\sigma\psi_{xx}&-\sigma\psi_{xy}
\end{pmatrix}\right\rangle,
\quad \sigma=r+1,\quad \kappa=\frac{r(r+2)}3,\quad r>0.
\]

The original source is `updates/GD-joint-structured-genesis-20261016/package/derived/workers/gd_positivity_frontier/PROOF.md`, lines 349–377. It explicitly labels (17) OPEN at lines 372–377. The unchanged polynomial is defined there at lines 24–29:

\[
J_r(F)=\alpha(u+v-2j)^2+\beta u^2+j^2+ruj,
\quad \alpha=\frac{3r}{8(r+2)},\quad \beta=\frac{r(r-1)}6,
\]
where (F=\begin{pmatrix}a&b\\c&d\end{pmatrix}), (u=a^2+c^2), (v=b^2+d^2), (j=ad-bc).

## Surviving pointwise quartic estimate

Set (p=\psi_{xx}), (q=\psi_{xy}), (w=\psi_{yy}), and

\[
X=\sigma p,\qquad Y=w,\qquad Z=q,\qquad
\lambda=\frac{\kappa}{4\sigma^2}=\frac{r(r+2)}{12(r+1)^2}.
\]

For the compatible matrix (V=\begin{pmatrix}Z&Y\\-X&-\sigma Z\end{pmatrix}), exact expansion gives

\[
D:=J_r(V)-\lambda Z^2(Y+\sigma X)^2=A+B Z^2+C Z^4,
\]

with

\[
A=J_r\!\begin{pmatrix}0&Y\\-X&0\end{pmatrix},
\]
\[
B=-\frac{Y(r+2)}{12(r+1)^2}
\left[X(18r^3+50r^2+44r+12)-Y(9r^3+18r^2+8r)\right],
\]
\[
C=\frac{(r+2)(9r^3+36r^2+40r+12)}{24}>0.
\]

The source's exact Gram decomposition gives (A\ge0). Explicitly, with (t=(2r+1)/3), (w_0=ab+cd), (z=(u,v,j)^T), and

\[
M_r=\begin{pmatrix}
t^2&1/3&2t\\
1/3&1&-2\\
2t&-2&16/3+1/\alpha
\end{pmatrix},
\qquad
J_r(F)=\alpha z^TM_rz+\frac{4\alpha}{3}w_0^2,
\]

the three leading principal minors of (M_r) are (t^2), (4r(r+1)/9), and (16(r+1)/27), all positive for (r>0). This identity and all minors are independently re-expanded and checked over exact SymPy polynomials by `exact_certificate.py`.

For the remaining sign branch, define (A_x=18r^3+50r^2+44r+12>0), (B_y=9r^3+18r^2+8r>0). If (B<0), then (Y(A_xX-B_yY)>0), which implies (XY>0). Exact factorization gives

\[
4AC-B^2=\frac{r((r+1)X+Y)^2}{144(r+1)^4}S_r(X,Y),
\]

where

\[
\begin{aligned}
S_r={}&36r^7X^2+r^6(144XY+252X^2)+r^5(54Y^2+972XY+709X^2)\\
&+r^4(360Y^2+2566XY+1050X^2)+r^3(881Y^2+3410XY+889X^2)\\
&+r^2(1004Y^2+2408XY+432X^2)+r(536Y^2+856XY+112X^2)\\
&+108Y^2+120XY+12X^2.
\end{aligned}
\]

Every coefficient is positive, and (XY>0) in this branch, so (S_r>0) and (4AC-B^2\ge0). Completing the square in (Z^2\ge0) proves (D\ge0). If (B\ge0), then (D\ge A\ge0) directly. Thus, for every (r>0) and every real (X,Y,Z),

\[
\boxed{J_r(V)\ge\frac{\kappa}{4\sigma^2}Z^2(Y+\sigma X)^2.}
\]

The exact algebra/check receipt is `EXACT_CHECKS.json`; its status is `PASS` for the polynomial identities, source Gram identity, and Gram minors. This estimate is pointwise and does not itself use Hessian compatibility.

## Failed bridge to (17)

The scalar cubic in (17), in the variables above, is

\[
C_{17}=\left\langle Z(Z^2+X^2)\right\rangle.
\]

The pointwise estimate would combine with Cauchy if one had

\[
C_{17}=\frac1\sigma\left\langle XZ(Y+\sigma X)\right\rangle
=\left\langle pq(w+\sigma^2p)\right\rangle.
\]

That equality was an error. The asserted required null-Lagrangian identity
\(\langle q^3\rangle=\langle pqw\rangle\) is false. On the normalized square torus, take the smooth compatible potential
\[
\psi(x,y)=\cos x+\cos y+\cos(x+y).
\]
Then (p=-\cos x-\cos(x+y)), (q=-\cos(x+y)), and (w=-\cos y-\cos(x+y)), with
\[
\langle q^3\rangle=0,\qquad \langle p^2q\rangle=0,\qquad \langle pqw\rangle=-\frac14.
\]
Consequently the claimed bridge fails (for every (\sigma)); the pointwise quartic estimate controls a different cubic moment. No proof of (17) follows from this route.

## Numerical screen and status

The exploratory direct finite-Fourier optimization evaluates the original compatible ratio
\[
\Gamma_r=\frac{\kappa C_{17}^2}{4\sigma^2\langle p^2\rangle\langle J_r(V)\rangle}
\]
using smooth finite Fourier potentials, not independent Hessian jets. Previously saved screens are in `search_K2_*.json` and `search_K3_r1.json`. A fresh run at (r=0.1), (K=3), (80\times80) grid, seed 31021, and 700 gradient iterations per start reached a console best (\Gamma\approx0.1363523) (start index 25). It was interrupted before the output JSON was written; the coefficient vector was not captured, so this is only a partial search receipt, not a reproducible witness. No compatible counterexample was found in these screens. They do not prove the inequality.

**Disposition:** the pointwise quartic estimate is proved exactly; the cubic-identity route is refuted by the smooth example above; no genuine-compatible counterexample to (17) was found. Equation (17) remains OPEN on the evidence in this worker task. The general-(U) question is outside this result and remains separate.

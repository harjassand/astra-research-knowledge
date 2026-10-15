# Independent sharp rank-one convexity reconstruction

Date: 2026-10-15. This workstream derived the family threshold from the defining polynomial without reading `workers/moving_kernel_genesis`. After that derivation was reported, the parent supplied a candidate four-coefficient theorem; Section 6 independently recomputes its necessary conditions and audits its reduction to the sharp family. These are explicit mathematical arguments with exact symbolic algebra receipts. External mathematical review and historical priority remain unresolved.

## 1. Exact result and scope

For real parameters define

\[
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
u=a^2+c^2,\quad v=b^2+d^2,\quad j=ad-bc,
\]
\[
H=(u+v-2j)^2=((a-d)^2+(b+c)^2)^2,
\qquad
F_{\alpha,r}=\alpha H+\frac{r(r-1)}6u^2+j^2+ruj.
\]

**Theorem.** For every pair of real numbers \((\alpha,r)\), the polynomial \(F_{\alpha,r}\) is rank-one convex on all of \(\mathbb R^{2\times2}\) if and only if

\[
\boxed{r\in(-\infty,-2)\cup[0,\infty),\qquad
\alpha\ge\alpha_*(r):=\frac{3r}{8(r+2)}.}
\]

For \(-2\le r<0\), no finite value of \(\alpha\) works. For the supplied interval \([-21/8,-5/2]\), the sharp pointwise floor increases from \(63/40\) to \(15/8\). Therefore the sharp **uniform** floor over that interval is \(15/8\).

This characterizes rank-one convexity, not quasiconvexity. The supplied compatible-heat certificate establishes quasiconvexity for this interval when \(\alpha\ge3-3/16000=47997/16000\). In the gap

\[
\alpha_*(r)\le\alpha<47997/16000,
\]

quasiconvexity remains **UNKNOWN** in this workstream. Below \(\alpha_*(r)\), the necessary rank-one condition fails, so quasiconvexity fails as well. The broader rank-one theorem supplies no new compatible-heat certificate.

## 2. Reduction to a universal acoustic form

The invariants \(u,v,j\), and hence \(F\), are invariant under left multiplication by a proper rotation. Given \(p\ne0\), choose \(R\in SO(2)\) with \(Rp=|p|e_1\). Then

\[
D^2F(A)[p\otimes\xi,p\otimes\xi]
=|p|^2D^2F(RA)[e_1\otimes\xi,e_1\otimes\xi].
\]

The zero vector \(p\) is harmless. Thus it suffices to treat every \(A\) and every \(\xi=(n,m)\), without normalizing or discretizing \(\xi\).

Put \(x=a-d\), \(y=b+c\). The independent coordinates are \((a,c,x,y)\); conversely \(b=y-c\), \(d=a-x\). Along \(e_1\otimes(n,m)\), their velocities are \((n,0,n,m)\). Also

\[
j=a^2+c^2-ax-cy,\qquad j'=(a-x)n-cm,\qquad j''=0.
\]

Direct differentiation gives the acoustic quadratic form

\[
\begin{split}
Q_{\alpha,r}:={}&D^2F_{\alpha,r}(A)
[e_1\otimes(n,m),e_1\otimes(n,m)]\\
={}&4\alpha\big[(x^2+y^2)(n^2+m^2)+2(nx+my)^2\big]\\
&+\frac23r(r-1)n^2(3a^2+c^2)
+2\big((a-x)n-cm\big)^2\\
&+r\big[2n^2(a^2+c^2-ax-cy)
+4an\big((a-x)n-cm\big)\big].
\end{split}
\]

Since the integrand is smooth, nonnegativity of this form for all backgrounds and directions is equivalent to convexity on every rank-one line: the second derivative of every such line restriction is nonnegative everywhere. This is the classical Legendre–Hadamard characterization, not a numerical criterion.

## 3. Sharp necessity and excluded parameters

For every real \(r\), take

\[
A_r=\begin{pmatrix}0&2r+1\\3&0\end{pmatrix},
\qquad P=e_{11}.
\]

Direct substitution, with no limiting argument, gives

\[
D^2F_{\alpha,r}(A_r)[P,P]
=16(r+2)^2\alpha-6r(r+2).
\]

When \(r\ne-2\), this is

\[
\boxed{16(r+2)^2\big(\alpha-\alpha_*(r)\big).}
\]

Consequently no smaller \(\alpha\) can be rank-one convex, including at \(r=0\).

For \(-2<r<0\), choose instead

\[
A=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad P=e_{11}.
\]

Here \(x=y=0\), and the acoustic value is \(2r(r+2)/3<0\), independently of \(\alpha\).

At \(r=-2\), the polynomial is \(\alpha H+(u-j)^2\). For any real \(\alpha\), choose

\[
A_\alpha=\begin{pmatrix}0&\alpha+2\\-\alpha-1&0\end{pmatrix},
\qquad P=e_{11}.
\]

Then \(b+c=1\), and \(D^2F_{\alpha,-2}(A_\alpha)[P,P]=-4\). This covers the otherwise singular endpoint exactly.

## 4. Acoustic positive-semidefinite factor and sufficiency

Assume \(r<-2\) or \(r>0\). Define the four bilinear expressions

\[
\begin{aligned}
L_1&=2(r+1)^2na-2(r+1)mc-(3r+2)nx,\\
L_2&=2(r+1)(r+2)nc-3mx-3(r+1)ny,\\
L_3&=(2r+1)nx+3(r+1)my,\\
L_4&=mx.
\end{aligned}
\]

The exact acoustic factorization is

\[
\begin{split}
\boxed{Q_{\alpha,r}={}}&
\frac{L_1^2}{2(r+1)^2}
+\frac{rL_2^2}{6(r+1)^2(r+2)}
+\frac{rL_3^2}{2(r+1)^2(r+2)}
+\frac{3r^2L_4^2}{2(r+1)^2}\\
&+4\big(\alpha-\alpha_*(r)\big)
\big[(x^2+y^2)(n^2+m^2)+2(nx+my)^2\big].
\end{split}
\]

Every coefficient of a square is positive in the stated parameter ranges. The last line is nonnegative exactly when \(\alpha\ge\alpha_*(r)\). No coefficient divides by \(n\) or \(m\), so this one identity treats both coordinate directions, all zero directions, and all backgrounds. It proves the required universal nonnegativity, and Section 3 proves sharpness.

Equivalently, write \(z=(a,c,x,y)^T\), let \(L\) be the matrix whose rows are the coefficients of the four \(L_i\), and set

\[
W=\operatorname{diag}\left(
\frac1{2(r+1)^2},
\frac r{6(r+1)^2(r+2)},
\frac r{2(r+1)^2(r+2)},
\frac{3r^2}{2(r+1)^2}\right).
\]

The acoustic matrix at the floor is exactly \(L^TWL\). The certificate JSON stores this factor and its nonnegative \(\alpha\)-slack matrix.

For \(r=0\), \(F_{\alpha,0}=\alpha H+j^2\). The quartic \(H\) is convex, being the fourth power of the Euclidean norm of a linear image of \(A\), and \(j^2\) is convex along rank-one lines because \(j\) is affine on those lines. Thus \(\alpha\ge0\) suffices; the previous witness proves necessity. This case is also polyconvex and quasiconvex.

### How the sharp factor arises

For \(n\ne0\), first eliminate \((a,c)\) by a Schur complement. Their acoustic block \(P\) has

\[
\det P=\frac43n^4r(r+2)(r+1)^2>0,
\qquad P_{11}=2n^2(r+1)^2>0.
\]

The remaining two-by-two form is \(T_\alpha=\alpha B-K\), where

\[
B=4\begin{pmatrix}m^2+3n^2&2mn\\2mn&3m^2+n^2\end{pmatrix},
\]
\[
K=\frac r{2(r+2)}
\begin{pmatrix}
\dfrac{3m^2+(5r+4)(r+2)n^2}{(r+1)^2}&\dfrac{3mn}{r+1}\\
\dfrac{3mn}{r+1}&3n^2
\end{pmatrix}.
\]

At \(m=0\), the lower diagonal entry is \(4n^2(\alpha-\alpha_*)\), exposing the necessary floor. At that exact floor,

\[
\boxed{T_{\alpha_*}=\frac r{2(r+2)}
\left[ww^T+
\begin{pmatrix}\dfrac{3r(r+2)m^2}{(r+1)^2}&0\\0&0\end{pmatrix}\right],
\quad w=\binom{(2r+1)n/(r+1)}{3m}.}
\]

This proves the all-directions bound directly. Completing the preceding two squares and clearing their directional denominators yields the four-square identity above.

## 5. Consequences for the supplied interval

The derivative \(\alpha_*'(r)=3/[4(r+2)^2]\) is positive. The endpoint floors are exactly

\[
\alpha_*(-21/8)=63/40,\qquad
\alpha_*(-5/2)=15/8.
\]

Therefore \(\alpha\ge15/8\) is necessary and sufficient for every family member throughout the whole closed interval to be rank-one convex. Necessity uses its right endpoint and the explicit witness; sufficiency uses the universal identity.

At \(r=-8/3\), the floor is \(3/2\). In particular the source's failed selected heat-Gram continuation at \(\alpha=3,r=-8/3\) occurs inside the rank-one convex region. That failure cannot imply failure of rank-one convexity or quasiconvexity; it concerns that particular continuation.

## 6. Independent audit of the full four-coefficient cone

Consider

\[
G_{\alpha,\beta,\gamma,\delta}
=\alpha H+\beta u^2+\gamma j^2+\delta uj.
\]

The exact characterization, proposed by the other workstream and independently audited here, is

\[
\boxed{G\text{ is rank-one convex}\iff
\begin{pmatrix}6\beta+\delta&\delta\\\delta&\gamma\end{pmatrix}\succeq0,
\qquad
\begin{pmatrix}8\alpha&\delta\\\delta&2\beta+\delta\end{pmatrix}\succeq0.}
\]

**First necessity.** For arbitrary real \(k,t\), put

\[
A_t=\begin{pmatrix}1&-kt\\kt&1\end{pmatrix},\qquad
P_t=e_1\otimes(t,1).
\]

The full exact acoustic value is

\[
\begin{split}
D^2G(A_t)[P_t,P_t]
={}&2t^2\big[(6\beta+\delta)-2\delta(k-1)+\gamma(k-1)^2\big]\\
&+2(2\beta+\delta)k^2t^4.
\end{split}
\]

Nonnegativity for all \(t\), followed by \(t\to0\), forces the first bracket to be nonnegative for every \(k\). This is exactly positivity of the first displayed matrix, after changing the sign of the second coordinate. It includes \(\gamma=0\): then \(\delta=0\) and \(\beta\ge0\) are forced.

**Second necessity.** For arbitrary real \(c,y\), choose

\[
A=\begin{pmatrix}0&y-c\\c&0\end{pmatrix},\qquad P=e_{11}.
\]

Then

\[
D^2G(A)[P,P]
=2(2\beta+\delta)c^2-2\delta cy+4\alpha y^2.
\]

Its matrix in the order \((y,c)\) is
\(\left(\begin{smallmatrix}4\alpha&-\delta\\-\delta&2(2\beta+\delta)\end{smallmatrix}\right)\), a congruence of the second displayed matrix by \(\operatorname{diag}(1/\sqrt2,-\sqrt2)\). Thus that matrix is necessary, including its singular cases.

**Sufficiency when \(\delta\ne0\).** Write

\[
s=2\beta+\delta,\qquad t=6\beta+\delta.
\]

The two matrix conditions force \(s,t,\alpha,\gamma>0\). Set

\[
\rho=t/\delta=1+6\beta/\delta,\qquad
\lambda=\delta^2/t=\delta/\rho>0.
\]

If \(\delta>0\), then \(\rho>0\). If \(\delta<0\), then
\(\rho+2=3s/\delta<0\), so \(\rho<-2\). The independently proved sharp theorem therefore applies. Direct comparison of the four coefficients gives the identity

\[
\boxed{G=
\lambda F_{\alpha_*(\rho),\rho}
+(\gamma-\lambda)j^2
+\left(\alpha-\frac{\delta^2}{8s}\right)H.}
\]

Indeed \(\lambda\rho=\delta\),
\(\lambda\rho(\rho-1)/6=\beta\), and
\(\lambda\alpha_*(\rho)=\delta^2/(8s)\).
The first matrix gives \(\gamma-\lambda\ge0\), and the second gives
\(\alpha-\delta^2/(8s)\ge0\). Every summand is rank-one convex.

**All remaining boundary cases.** If \(\delta=0\), the conditions reduce to \(\alpha,\beta,\gamma\ge0\). Then \(G\) is a nonnegative sum of convex \(H,u^2\) and polyconvex \(j^2\), so is polyconvex. If any of \(s,t,\alpha,\gamma\) vanishes under the matrix conditions, their corresponding determinant inequality forces \(\delta=0\), reducing to this case. Thus no division by a possibly zero quantity is hidden in the theorem. Equalities of either determinant with \(\delta\ne0\) are permitted by the decomposition.

This establishes the full four-dimensional rank-one convex cone. Quasiconvexity over that entire cone remains **UNKNOWN**. The family proof and this reduction establish neither a general heat certificate nor a general Morrey implication.

## 7. Historical comparison and verification

Dacorogna–Marcellini's 1988 paper already uses the Legendre–Hadamard Hessian condition to prove rank-one convexity of a planar quartic. The present operation—reduce the rank-one Hessian to a quadratic form and prove it positive—is classical. The exact threshold and factorization here are deductions for the supplied anisotropic polynomial; no historical priority is asserted. [Primary paper, pp. 78–80](https://www.mat.univie.ac.at/~stefanelli/cv/paper5.pdf).

Bruno–Pasqualotto's Theorem 2 proves equivalence of rank-one convexity and quasiconvexity for quartic polynomials invariant under both left and right proper rotations. Its Appendix A determines that invariant cone by two acoustic PSD blocks and proves quasiconvexity using an exact-two-form correction along heat flow. The present family is generally only left invariant: at \(\operatorname{diag}(1,0)\), its value is \(\alpha+r(r-1)/6\), whereas after a right quarter turn the value is \(\alpha\). For the requested negative interval these differ, so that theorem's symmetry hypothesis fails. The acoustic sum of squares here addresses a smaller class of jets than a compatible-heat certificate. [Primary preprint, Theorem 2 and Appendix A](https://arxiv.org/html/2608.06367v1).

The exact verifier starts from the polynomial in \((a,b,c,d)\), computes its Hessian, and checks the coordinate change, matrix factor, Schur complement, necessary witnesses, excluded parameter witnesses, endpoint values, four-coefficient acoustic identities, decomposition, and singular cases. No numerical grid, optimizer, floating-point eigenvalue, or other worker's files is used.

Run from this directory:

```sh
../../.venv/bin/python verify.py
```

The generated `VERIFICATION.json` is an algebraic receipt. It does not replace mathematical sign arguments, external review, or a quasiconvexity certificate. Source inputs were read only from `sources/astra_compatible_heat_result`; the supplied source certificate was not regenerated or modified in this workstream.

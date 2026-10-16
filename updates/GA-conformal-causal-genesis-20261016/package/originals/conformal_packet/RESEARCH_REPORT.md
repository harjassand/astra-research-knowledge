# Cubic compatibility at the positive conformal contact

Research date: 16 October 2026, Australia/Brisbane.
Repository inspected: `harjassand/astra-research-knowledge`, main commit
`3dde9ce74d829a93388e64032d27351b36dd2221`.

**Status.** This investigation does not prove the sharp positive-core quasiconvexity inequality and does not produce a compatible negative Jensen field. It derives an exact classification of cubic functionals controlled by the degenerate conformal operator, an explicit nonlocal cubic identity with a quantitative bound, a conditional exclusion of nonconcentrating near-kernel loss, and exact counterexamples to two stronger proposed shortcuts. The proofs use classical interpolation, Hodge decomposition, integration by parts, and heat smoothing. Historical originality of the precise classification and identity is not established. The finite verifier checks algebra and specified compatible fields, not the analytic interpolation theorem or an all-gradient sharp inequality.

## 1. The unchanged target and reconstruction

For
\[
 A=\begin{pmatrix}a&b\\c&d\end{pmatrix},\quad
 u=a^2+c^2,\quad v=b^2+d^2,\quad j=ad-bc,
\]
let
\[
 H=(u+v-2j)^2,
 \qquad J_r=\frac{3r}{8(r+2)}H+\frac{r(r-1)}6u^2+j^2+ruj,
 \qquad r>0.
\]
All coefficients of this integrand are retained. No finite-distortion completion is constructed or used to promote its fixed-coefficient status.

Write a compatible gradient as
\[
 A=D\phi=\begin{pmatrix}f_x&f_y\\g_x&g_y\end{pmatrix},
 \qquad a=f_x,\ b=f_y,\ c=g_x,\ d=g_y.
\]
Unless specified otherwise, averages are normalized on the square torus
\(\mathbb T^2=(\mathbb R/2\pi\mathbb Z)^2\). The proofs first concern smooth periodic maps and then pass to the stated Sobolev classes by convolution and strong convergence. A zero-boundary map on a bounded planar domain may be extended by zero to a surrounding square and treated periodically. The inequalities have the correct homogeneous scaling to remove the size of that square.

Set
\[
 \sigma=r+1,\qquad \kappa=\frac{r(r+2)}3,\qquad
 q=\sigma a+d,\qquad
 U_r=2a q-(r+2)a^2+r c^2-2bc.
\]
Direct expansion, with \(\langle\det D\phi\rangle=0\), gives
\[
 \langle J_r(sI+D\phi)-J_r(sI)\rangle
 =A_r+sC_r+s^2Q_r,                                     \tag{1}
\]
where
\[
 A_r=\langle J_r(D\phi)\rangle,
 \quad Q_r=\langle q^2+\kappa c^2\rangle,
\]
\[
 \boxed{C_r=\langle qU_r-\kappa a(a^2+c^2)\rangle.}       \tag{2}
\]
Equivalently, if \(t=(2r+1)/3\), the cubic density is
\[
 DJ_r(A):I=r(d+ta)(a^2+c^2)+2j((r+1)a+d).
\]
The raw quadratic Taylor coefficient is \(q^2+\kappa c^2+(r+2)j\).

For \(r=1\), \(\sigma=2,\kappa=1\), and
\[
 C_1=\langle a^3+5a^2d-4abc+ac^2+2ad^2-2bcd+c^2d\rangle.
\]
The required inequality remains
\[
 \boxed{C_r^2\le4A_rQ_r.}                               \tag{3}
\]
For a fixed map, minimizing (1) in \(s\) gives \(s_*=-C_r/(2Q_r)\) and gap
\(A_r-C_r^2/(4Q_r)\) when \(Q_r>0\). When \(Q_r=0\), compatibility forces
\(a=c=d=0\), leaving a pure shear and \(C_r=0\).
Proving (3) for all maps establishes all scalar conformal backgrounds. By left rotation invariance, it also establishes their output rotations. It would not by itself establish every nonscalar full-rank background.

### What was rechecked

The incoming calibration package's verifier was executed with Python optimization disabled: all 24 groups passed. The incoming sharp-frontier verifier was similarly executed: all 10 groups passed. Logs and archive hashes are retained.

The new verifier independently reconstructs, from \(J_r\), the conformal expansion, positive-branch acoustic Schur complement, Gram-difference calibration identity, full arbitrary-background calibration polynomial identity and its rational positive minors. Thus the new argument does not rely merely on previous report labels.

For the acoustic calculation, left rotations reduce the rank-one direction to
\(e_1\otimes(1,z)\). With
\[
 (a,b,c,d)=\tfrac12(P+X,Y-Q,Y+Q,P-X),
\]
the conformal block is
\[
 A_c=\begin{pmatrix}
 (r+1)^2/2&-z(r+1)/2\\
 -z(r+1)/2&(3z^2+r(r+2))/6
 \end{pmatrix},
 \quad \det A_c=\frac{r(r+1)^2(r+2)}{12}>0.
\]
Put \(\alpha=3r/[8(r+2)]\),
\(b_r=r(5r+4)/[24(r+1)^2]\), \(c_r'=\alpha/(r+1)^2\).
The Schur complement is
\[
 4\begin{pmatrix}
 (\alpha-c_r')z^2+3(\alpha-b_r)&(2\alpha-\alpha/(r+1))z\\
 (2\alpha-\alpha/(r+1))z&3\alpha z^2
 \end{pmatrix}.
\]
Its determinant is \(48\alpha(\alpha-c_r')z^4\), and
\[
 \alpha-c_r'>0,\qquad
 \alpha-b_r=\frac{r(2r+1)^2}{24(r+1)^2(r+2)}>0.
\]
This is an independent rank-one-convexity proof for every \(r>0\). The missing input direction follows by continuity.

The inherited pointwise-support obstruction at \(I\) also rechecks. Its forced determinant slope is \(r+2\), and at
\(V=s\operatorname{diag}(1,-r-1)\) the residual is
\[
 -\frac{r(r+2)}3s^3+
 \left[\frac{3r}{8(r+2)}(r+2)^4+\frac{(r+2)(r+3)}6\right]s^4.
\]
Its negative cubic does not produce a compatible zero-boundary perturbation. It rules out the ordinary pointwise minor support at that background, not quasiconvexity.

## 2. An exact classification of cubic compensation

This section is independent of the particular quartic.

For fixed \(\sigma>0\), define
\[
 T_\sigma\phi=(\sigma f_x+g_y,\ g_x)=(q,c).
\]
Its symbol on the two potentials is, apart from a factor \(i\),
\[
 \begin{pmatrix}\sigma\xi_x&\xi_y\\0&\xi_x\end{pmatrix}.
\]
The rank is two when \(\xi_x\ne0\), and one at a nonzero vertical covector. It is not a constant-rank operator. In particular, a uniform linear estimate controlling the full gradient by \(T_\sigma\phi\) is unavailable; the exact kernel includes \((f(y),0)\).

### Theorem 1: the cubic selection rule

Let \(P(a,b,c,d)\) be a real homogeneous cubic. The following are equivalent.

1. There is a finite constant \(K\) such that, for every smooth periodic \(\phi\),
\[
 |\langle P(D\phi)\rangle|
 \le K\|T_\sigma\phi\|_2\|D\phi\|_4^2.                 \tag{4}
\]
2. There is a finite, not necessarily the same, constant \(K'\) such that
\[
 \|P(D\phi)\|_1
 \le K'\|T_\sigma\phi\|_2\|D\phi\|_4^2.               \tag{5}
\]
3. The polynomial restriction
\[
 \boxed{P(a,b,0,-\sigma a)\text{ is divisible by }a^2.}   \tag{6}
\]

Equivalently, the coefficients of \(b^3\) and \(ab^2\) in that restriction vanish. These are two independent linear conditions, defining an 18-dimensional subspace of the 20-dimensional space of homogeneous cubics in four variables.

The theorem identifies **finiteness**, not the optimal constants in (4) or (5). In particular the optimal signed and absolute constants need not agree. It is not a sharp quasiconvexity theorem.

### 2.1 The analytic interpolation input, with proof

For \(1<p_0,p_1<\infty\), put
\(1/t=(1/p_0+1/p_1)/2\). On a square torus,
\[
 \|\psi_{xy}\|_t
 \le C_{p_0,p_1}\|\psi_{xx}\|_{p_0}^{1/2}
                       \|\psi_{yy}\|_{p_1}^{1/2}.        \tag{7}
\]
This is a classical mixed-derivative interpolation estimate. The proof is included to make the exact input and endpoints clear.

First take a trigonometric polynomial. Remove its modes on the two coordinate frequency axes; those modes contribute nothing to \(\psi_{xy}\). This projection has uniformly bounded norm on every finite \(L^p\), because it is a composition of identity minus a conditional expectation. On the remaining modes define
\[
 F(z)=e^{(z-1/2)^2}|D_x|^{2(1-z)}|D_y|^{2z}\psi,
 \qquad0\le\Re z\le1.
\]
On \(\Re z=0\), the imaginary factors are products of the one-dimensional multipliers \(|n|^{it}\), acting on \(\psi_{xx}\). On \(\Re z=1\), they act on \(\psi_{yy}\). The one-dimensional Marcinkiewicz multiplier bound applies because the variation of \(n^{it}\) on every dyadic interval is bounded by a constant times \(|t|\). Applying it in each coordinate and using Fubini gives at most polynomial growth in \(|\Im z|\); the Gaussian factor makes the boundary bounds uniform. The vector-valued three-lines/complex-interpolation inequality between \(L^{p_0}\) and \(L^{p_1}\) yields
\[
 \||D_x||D_y|\psi\|_t
 \le C\|\psi_{xx}\|_{p_0}^{1/2}\|\psi_{yy}\|_{p_1}^{1/2}.
\]
Two bounded periodic Hilbert transforms convert the left-hand side to the mixed derivative. This proves (7). If either endpoint norm is zero, the off-axis part is zero. Frequency approximation gives the general estimate wherever the two endpoint derivatives are in their stated spaces. No endpoint \(p=1\) or \(p=\infty\) is used.

This proof uses established harmonic-analysis results, not a new sharp multiplier estimate. The finite symbolic verifier does not verify these analytic theorems.

### 2.2 Nonlinear control of the transverse derivative

The required specialization of (7) is
\[
 \|\psi_{xy}\|_{8/3}^2
 \le C\|\psi_{xx}\|_2\|\psi_{yy}\|_4.                  \tag{8}
\]
Take the periodic Hodge decomposition, after removing irrelevant means,
\[
 (\sigma f,g)=\nabla\chi+(\psi_y,-\psi_x),\qquad
 \Delta\chi=q.
\]
It gives the exact identities
\[
 \sigma a=\chi_{xx}+\psi_{xy},\qquad
 \sigma b=\chi_{xy}+\psi_{yy},\qquad
 c=\chi_{xy}-\psi_{xx}.                                 \tag{9}
\]
The second derivatives of \(\chi\) are the usual bounded second-order Riesz multipliers applied to \(q\). Hence
\[
 \|\psi_{xx}\|_2\le C\|q\|_2+\|c\|_2,
 \qquad
 \|\psi_{yy}\|_4\le C_\sigma\|D\phi\|_4.
\]
By (8),
\[
 \|\psi_{xy}\|_{8/3}^2
 \le C_\sigma\|T_\sigma\phi\|_2\|D\phi\|_4.
\]
Also ordinary Lebesgue interpolation gives
\[
 \|\chi_{xx}\|_{8/3}^2
 \le\|\chi_{xx}\|_2\|\chi_{xx}\|_4
 \le C_\sigma\|T_\sigma\phi\|_2\|D\phi\|_4.
\]
Together with (9),
\[
 \boxed{\|a\|_{8/3}^2
 \le C_\sigma\|T_\sigma\phi\|_2\|D\phi\|_4.}           \tag{10}
\]
This is a nonlinear estimate: two powers of the missing derivative are controlled by one power of the defect and one power of the full gradient norm. It is not a false linear Korn estimate across a rank drop.

### 2.3 Sufficiency of the selection rule

In the linear coordinates \((a,b,c,q)\), condition (6) is exactly the ability to write
\[
 P=qP_2+cR_2+a^2(\lambda a+\mu b),                     \tag{11}
\]
where \(P_2,R_2\) are homogeneous quadratics. The first two terms have absolute \(L^1\) bounds by \(L^2\)-\(L^4\)-\(L^4\) Hölder. The last terms satisfy
\[
 \|a^2a\|_1\le\|a\|_{8/3}^2\|a\|_4,
 \qquad
 \|a^2b\|_1\le\|a\|_{8/3}^2\|b\|_4.
\]
Use (10). This proves (5), and (5) immediately implies (4). Strong convolution approximation gives the result for periodic \(W^{1,4}\) maps. Zero extension into a surrounding square gives the zero-boundary version on bounded domains, with the same scale-invariant form.

### 2.4 Necessity: actual compatible oscillations

The coefficient of \(b^3\) must vanish. Take \(g=0\),
\(f(y)=\sin y+\tfrac12\sin2y\). Then \(T_\sigma\phi=0\), while
\(\langle b^3\rangle=3/4\).

To test \(ab^2\), set
\[
 \psi(x,y)=-\cos(x+y)-\cos y-\tfrac12\cos(x+2y).
\]
For every positive integer \(N\), define the genuinely periodic compatible map
\[
 f_N(x,y)=N^{-1}\psi_y(x,Ny),\qquad
 g_N(x,y)=-\sigma N^{-2}\psi_x(x,Ny).
\]
Then
\[
 a_N=N^{-1}\psi_{xy},\quad b_N=\psi_{yy},\quad
 c_N=-\sigma N^{-2}\psi_{xx},\quad d_N=-\sigma a_N,
 \quad q_N=0,                                          \tag{12}
\]
where the derivatives on the right are evaluated at \((x,Ny)\).
Exact trigonometric integration gives
\[
 \langle\psi_{xy}\psi_{yy}^2\rangle=\frac32,
 \qquad\langle\psi_{xx}^2\rangle=\frac58.
\]
Thus
\[
 \langle a_Nb_N^2\rangle=\frac{3}{2N},\qquad
 \|T_\sigma\phi_N\|_2=\frac{\sigma}{N^2}\sqrt{\frac58},
 \quad\sup_N\|D\phi_N\|_4<\infty.                      \tag{13}
\]
Once the \(b^3\) coefficient is zero, every other cubic term except \(ab^2\) has order \(N^{-2}\) or smaller on (12). A nonzero \(ab^2\) coefficient therefore contradicts (4). This completes both necessity and sufficiency.

Merely vanishing on the exact pure-shear kernel is insufficient: \(ab^2\) vanishes there and still fails the estimate. The first transverse jet is load-bearing.

The same construction shows that the power of the defect in (10) cannot be uniformly improved: \(\|a_N\|_{8/3}^2\) and \(\|T_\sigma\phi_N\|_2\) both scale as \(N^{-2}\), while the full gradient norm stays bounded and nonzero.

### 2.5 Optional exponent extension

The same proof works for every \(s>2\) and \(1/p+2/s=1\). In (7) take endpoints \(p,s\), so the intermediate exponent satisfies \(2/t+1/s=1\). The conclusion is
\[
 \|a\|_t^2\le C_{\sigma,p,s}\|T_\sigma\phi\|_p\|D\phi\|_s,
\]
and the same algebraic criterion (6) characterizes bounded cubic estimates
\(\|P(D\phi)\|_1\le K\|T_\sigma\phi\|_p\|D\phi\|_s^2\).
The first theorem and applications use only \((p,s)=(2,4)\). No endpoint estimate is asserted.

## 3. Application to the target: an explicit cubic operation

The target cubic (2), restricted to the formal defect plane \(q=c=0\), is
\[
 \boxed{C_r(a,b,0,-(r+1)a)=-\kappa a^3.}               \tag{14}
\]
It obeys the selection rule and in fact vanishes to third rather than just second transverse order. Thus its cubic coupling has a genuine compatible bound for every fixed \(r>0\).

Finiteness of some bound for this particular cubic was already compatible with the prior finite-completion theorem and pointwise positivity of \(J_r\). It is not, by itself, the new sharp advance. The new information is the exact operator-specific cubic selection rule and the explicit representation below. Neither identifies the constant required by (3).

### Theorem 2: horizontal-heat cubic resolvent

Let \(P_t=e^{t\partial_x^2}\), and write \(a_t=P_ta\), etc. Then for every smooth periodic compatible map and every \(\sigma>0\),
\[
 \boxed{
 \langle a^3\rangle=
 \frac6\sigma\int_0^\infty
 \langle a_ta_{t,x}q_{t,x}-a_tb_{t,x}c_{t,x}\rangle\,dt.
 }                                                       \tag{15}
\]
This identity does not require monotonicity of \(\int J_r\). Horizontal heat is used to resolve a cubic functional, not to decrease the target variational energy.

**Proof.** Compatibility gives \(a_y=b_x\), \(q_x=\sigma a_x+c_y\). Therefore
\[
 a a_xq_x-a b_xc_x-\sigma a a_x^2
 =a(a_xc_y-a_yc_x)
 =\det D(a^2/2,c).
\]
Its integral is zero. Also
\[
 \frac d{dt}\langle a_t^3\rangle=-6\langle a_ta_{t,x}^2\rangle.
\]
The horizontal mean of \(a=f_x\) is zero, so \(a_t\to0\). Integrating in time proves (15). The displayed estimates below give absolute time-integrability of its paired integrals and justify limiting Sobolev approximations.

### An explicit quantitative estimate

For every \(\theta>0\), define
\[
 K_\theta(a,b)=\frac{1+\theta}{12}a^4+
                 \frac12a^2b^2+\frac1{3\theta}b^4.
\]
For arbitrary \(X,Y\),
\[
 \begin{split}
 &D^2K_\theta(a,b)[(X,Y),(X,Y)]-a^2(X^2+Y^2)\\
 &\quad=(\sqrt\theta\,aX+2bY/\sqrt\theta)^2+b^2X^2\ge0.
 \end{split}                                           \tag{16}
\]
Hence horizontal heat integration gives
\[
 \int_0^\infty\langle a_t^2(a_{t,x}^2+b_{t,x}^2)\rangle dt
 \le\langle K_\theta(a,b)\rangle.
\]
The terminal energy is nonnegative and can be discarded. In addition,
\[
 \int_0^\infty\langle q_{t,x}^2+c_{t,x}^2\rangle dt
 \le\frac12\langle q^2+c^2\rangle.
\]
Cauchy--Schwarz in space and time, applied to (15), gives
\[
 |\langle a^3\rangle|^2
 \le\frac{18}{\sigma^2}\langle q^2+c^2\rangle
                         \langle K_\theta(a,b)\rangle.
\]
Optimizing the single positive scalar \(\theta\) gives
\[
 \boxed{
 |\langle a^3\rangle|^2\le
 \frac{18}{\sigma^2}\langle q^2+c^2\rangle
 \left[
 \frac{\langle a^4\rangle}{12}
 +\frac{\langle a^2b^2\rangle}{2}
 +\frac{\sqrt{\langle a^4\rangle\langle b^4\rangle}}3
 \right].}                                             \tag{17}
\]
If one of the fourth moments is zero, the bound follows by a one-sided limit in \(\theta\). It holds for the full periodic \(W^{1,4}\) class by strong approximation. The heat integral itself may equivalently be interpreted through smooth approximation; it is not an algorithm requiring pointwise Hessians of a rough map.

The explicit constant in (17) is not claimed sharp. Substituting triangle estimates for the other terms of (2) does not yield (3).

## 4. A precise nonconcentration consequence

Fix \(r>0\). Suppose \(D\phi_n\) is bounded in \(L^4\), its fourth powers are uniformly integrable, and \(Q_r(\phi_n)\to0\). Then
\[
 \boxed{\frac{C_r(\phi_n)}{\sqrt{Q_r(\phi_n)}}\to0}       \tag{18}
\]
along the indices with nonzero denominator.

Indeed, \(q_n,c_n\to0\) in \(L^2\). The determinant-null identity implies
\[
 \sigma\langle a_n^2\rangle
 =\langle a_nq_n-b_nc_n\rangle\to0.
\]
Thus \(a_n,d_n,c_n\to0\) in measure. Uniform integrability of their fourth powers implies their strong \(L^4\) convergence to zero. In (2), the quadratic factors paired with \(q_n,c_n\) then tend to zero in \(L^2\). Finally, either (10) times \(\|a_n\|_4\), or the optimized estimate (17), gives
\(|\langle a_n^3\rangle|/\sqrt{Q_r}\to0\).

In particular, after normalization \(A_r=1\), such a nonconcentrating near-kernel sequence has cubic ratio \(C_r^2/(4A_rQ_r)\to0\). For a fixed positive \(r\), the needed pointwise coercivity of \(J_r\) follows from the verified incoming calibration at \(B=0,k=2/3\). At \(r=1\) one may instead use directly
\[
 J_1\ge\frac{5-\sqrt{13}}{16}|A|^4,
\]
which follows by writing \(8J_1=x^2+y^2+4z^2+2xz\), with
\(x=u-v,y=2w,z=2j\) and \(x^2+y^2+z^2=|A|^4\).

**The uniform-integrability assumption cannot simply be deleted.** Let \(\phi\) be any smooth compact compatible map with \(C_r\ne0\). Concentrate it by
\[
 \phi_\varepsilon(x)=\varepsilon^{1/2}
        \phi((x-x_0)/\varepsilon).
\]
Then
\[
 A_r(\phi_\varepsilon)=A_r(\phi),\quad
 Q_r(\phi_\varepsilon)=\varepsilon Q_r(\phi),\quad
 C_r(\phi_\varepsilon)=\varepsilon^{1/2}C_r(\phi).
\]
Its cubic ratio is unchanged. Such a datum with nonzero cubic is easily obtained from a scalar-row compact map with an asymmetric \(x\)-derivative profile and \(g=0\). Smooth approximation preserves a nonzero cubic integral.

Thus concentration is not ruled out, and (18) is not an all-gradient proof. It isolates an exact mechanism that any near-kernel sharp analysis must retain.

## 5. Why the obvious sharp norm estimate fails

The resolvent (15) also gives an explicit bilinear stress. For horizontal Fourier frequencies \(p,\ell\), output \(k=p+\ell\), and
\(D=k^2+p^2+\ell^2\), define
\[
 \widehat{T_1(a,a)}_k=
 \sum_{p+\ell=k}\frac{3k^2}{D}\widehat a_p\widehat a_\ell,
\]
\[
 \widehat{T_2(a,b)}_k=
 \sum_{p+\ell=k}\frac{-6k\ell}{D}\widehat a_p\widehat b_\ell.
\]
The zero-over-zero multiplier is defined as zero; the vertical coordinate remains a physical variable. Exact heat integration gives
\[
 \langle a^3\rangle=\sigma^{-1}\langle qT_1+cT_2\rangle.
\]
For \(r=1\), set
\[
 S_1=2a q-3a^2+c^2-2bc-\tfrac12T_1,
 \qquad S_2=-ac-\tfrac12T_2.
\]
Subtract the global mean of \(S_1\) and the horizontal mean of \(S_2\), which pair to zero with \(q,c\). Then
\[
 C_1=\langle qS_1+cS_2\rangle.                          \tag{19}
\]
The tempting sufficient condition
\[
 \langle S_1^2+S_2^2\rangle\le4A_1                    \tag{20}
\]
is **false**, even for an explicitly compatible smooth map with zero cubic integral.

Let
\[
 F(y)=\frac{(1+\cos y)^8}{256},\qquad
 f(x,y)=\frac14\sin(4x)F(y),\qquad g=0.
\]
More generally use \(f=n^{-1}\sin(nx)F(y)\). Then
\[
 a=F\cos nx,\quad b=F'\sin(nx)/n,\quad c=d=0,
\]
\[
 T_1=F^2\cos2nx,\qquad T_2=-FF'\sin2nx/n,
\]
\[
 S_1=(F^2-\langle F^2\rangle)/2,
 \qquad S_2=FF'\sin2nx/(2n).
\]
Consequently
\[
 \begin{split}
 \langle|S|^2\rangle-4A_1
 =\frac1{16}\left[
 \langle F^4\rangle-4\langle F^2\rangle^2
                   -\frac3{n^4}\langle(F')^4\rangle
 \right].
 \end{split}
\]
At \(n=4\), the exact value is
\[
 \boxed{\frac{159381921467360331}{147573952589676412928}>0.} \tag{21}
\]
The stress ratio is approximately 1.05496633. Meanwhile \(C_1=\langle a^3\rangle=0\), and its Jensen polynomial is \(A_1+s^2Q_1>0\) for a nonzero map.

This is not a negative-energy counterexample. It excludes the sharp contraction of this particular, fully specified stress representation, including its natural mean projections. It does not exclude all nonlocal stresses, nonlinear selection, or a different allocation of resonant terms. It explains why retaining the cubic pairing and its cancellations can be essential before applying a norm inequality.

## 6. Genuine multimode interaction exceeds the one-wave constant

For a one-phase gradient \(D\phi=R h'\), with \(R=v\otimes\xi\) rank one, normalize the generic nonzero coordinates by
\(R=(1,t;s,st)\). Then
\[
 J_1(R)=\frac{(1+s^2)^2(1+t^2)^2}{8},
 \quad C_1(R)=(1+s^2)(1+st),
 \quad Q_1(R)=(2+st)^2+s^2.
\]
The exact identity
\[
 (1+t^2)((2+st)^2+s^2)-4(1+st)^2
 =((1-t^2)s-2t)^2
\]
and scalar Hölder give
\[
 \boxed{\frac{C_1(\phi)^2}{4A_1(\phi)Q_1(\phi)}\le\frac12}
\]
for every one-phase periodic map, with the remaining coordinate cases obtained by continuity. This is not a valid universal bound for interacting gradients.

`EXACT_RESONANCE_FIXTURE.json` supplies a continuous periodic piecewise-affine map on a 12 by 12 nodal grid, with rational nodal values of denominator 20 and physical coordinate scale 25/2 in the x direction. Each square is split along its lower-left to upper-right diagonal. This defines an actual compatible map, not an independently prescribed gradient law. The equal-area triangle integrals are checked with exact fractions.

The exact normalized quantities are
\[
 A_1=\frac{14054717889}{640000},\quad
 C_1=\frac{282507}{80},\quad Q_1=\frac{16569}{80},
\]
\[
 \langle D\phi\rangle=0,\qquad\langle\det D\phi\rangle=0,
\]
\[
 \boxed{\frac{C_1^2}{4A_1Q_1}
 =\frac{17735601122000}{25874735633649}
 \approx0.685440862976>\frac23>\frac12.}                \tag{22}
\]
Its fully optimized scalar conformal background is
\(s_*=-94169/11046\), and its optimized Jensen gap is strictly positive:
\[
 A_1-C_1^2/(4Q_1)=\frac{8139134511649}{1178240000}>0.
\]
The rational aspect ratio permits exact periodic tiling into a square, followed by isotropic rescaling. Thus the example also transfers to the standard square-torus class. Smoothing transfers a strict violation of the false one-wave bound to smooth compatible gradients.

This fixture is included to defeat an insufficient reduction to one-phase estimates. It is not evidence of non-quasiconvexity. The searched unrounded Fourier candidate reached approximately 0.7217, but only (22) is promoted as an exact lower-bound witness here.

## 7. Searches, failures, and evidence limits

At the unchanged \(J_1\) coefficients, 26 completed signed cubic-ratio local searches were run: 10 Fourier searches at bandwidth 3, eight at bandwidth 7, and eight periodic P1 searches on a 12 by 12 grid. No ratio above one was obtained. Six additional absolute-cubic exploratory searches also found no violation, but absolute-value quadrature is not polynomially exact and these are not rigorous bounds.

The Fourier grids contain 4m+1 points per direction, enough for exact quartic averages of a bandwidth-m trigonometric polynomial in exact arithmetic. Floating calculation and local optimization remain heuristic. The P1 search is compatible by construction. The best P1 candidate was independently coarsened to rational nodal data and rechecked exactly, producing (22).

Several canonical bilinear stress estimates were attacked rather than assumed: horizontal-heat, angle-adapted, physically aligned, and frequency-projected variants. Numerical failures are retained as exploratory data. Only the closed-form compatible carrier (21) is promoted as an analytic counterexample to its specified sharp stress contraction. High-aspect ratio overflows and NaN outputs in median/max-frequency variants are recorded as failed implementations, not mathematical evidence.

Selected finite output-frequency-only Riesz multiplier ansatzes of angular degrees 2, 4, and 6 have inconsistent exact sampled-triad identity systems. Their scripts and rank receipts are retained. This says only that those declared finite ansatzes cannot represent the cubic identity. It neither rules out general Fourier operations nor supplies a quasiconvexity obstruction, and it is not a premise of Theorem 1 or 2.

The correct next mathematical task is not another local optimizer or another finite supporting-plane expansion. It is to establish, or refute with a compatible field, the optimal signed cubic estimate (3), retaining resonant cancellations and concentration rather than replacing them by the disproved contraction (20).

## 8. Prior mathematics and concurrent-source boundaries

**Classical analytic tools.** The mixed-derivative lemma uses complex interpolation, periodic imaginary-power multiplier bounds and Hilbert transforms. The Hodge decomposition and second-order Riesz estimates are standard. The heat identity uses an exact Jacobian and semigroup differentiation. None of these general tools is claimed as invented here. The specific cubic criterion (6), its application to the conformal defect, and the explicit resolvent/budget pair are derived in this investigation; their historical originality has not been established.

Müller's published *Quasiconvexity is not invariant under transposition* relates a cubic compensated-compactness phenomenon to a differential constraint whose rank varies. That predecessor prevents presenting cubic compensation beyond constant rank as a new subject. Only its primary published abstract and repository record were inspected here; a complete priority comparison with its proof and the broader trilinear literature remains outstanding.

Guerra--Raiţă's systematic null-Lagrangian/Hardy-space theory explicitly assumes constant rank. Their separate necessity result explains a limitation of corresponding linear Lp estimates. The symbol of \(T_\sigma\) is not constant rank, so their constant-rank conclusions are not directly imported as a proof of (10). This does not mean they or related work cannot imply an equivalent specialized inequality; such priority has not been cleared.

Bruno--Pasqualotto's quartic result has both left and right rotational invariance, while the positive sharp cores generally have only left rotational invariance. Their heat/exact-form method is inherited capital. The use of horizontal smoothing in (15) does not assert monotonicity of the target energy and does not circumvent their scope merely by renaming the flow.

The pinned N877 result concerns finite completion along H, not the unchanged quartic. It is not used as a proof of (3). N874 already contains the general all-background moment/Schur reformulation; (1) is its conformal specialization, rederived here, not a new general reduction.

Pedregal's arXiv:1905.06571v5 claims a general planar implication. The prior archive has a scoped permitted-mold objection to its nonempty-image step. This investigation does not adopt the manuscript's global claim and does not claim a new independent audit of its entire proof. Neither a claimed resolution nor an objection to one proof route decides (3).

Primary source URLs and actual reading scopes appear in `SOURCES.json`. No absent external endorsement or historical-priority clearance is inferred from these comparisons.

## 9. Exact remaining obligation and reproducibility

For a fixed r define
\[
 \Gamma_r=\sup_{\phi\text{ compatible},\,A_rQ_r>0}
                 \frac{C_r^2}{4A_rQ_r}.
\]
Conformal-background quasiconvexity is exactly \(\Gamma_r\le1\). The new classification proves a finite compatible estimate but does not locate this sharp threshold. The preceding finite-completion result already implies some finite bound for this target: at scalar conformal backgrounds H(sI+A)=H(A), so a QC completion yields C_r^2<=4(A_r+lambda< H(Dphi) >)Q_r, and pointwise coercivity of J_r absorbs the added H into a fixed multiple of A_r. It does not supply the optimal signed constant. The new classification concerns all homogeneous cubics and is not a claim that finite boundedness for this particular target was previously unavailable.

The exact lower bound (22) shows \(\Gamma_1>2/3\). No upper bound of one or a rigorous lower bound greater than one was obtained. The all-background positive family and general planar Morrey implication remain unresolved in this investigation.

The strongest next construction should use (15) or a different compatible representation while preserving cancellations that the separate stress norm loses. It must handle concentration, which exactly preserves the ratio, and cannot rely on a forbidden pointwise minor support at I. An extension from conformal to arbitrary full-rank backgrounds would require a further all-background argument even after (3) is proved.

To replay the exact algebra and fixtures:

```sh
python verify_compatibility.py
```

The script uses explicit runtime checks, not Python `assert`, and does not import an optimizer or discovery state. It checks 21 finite algebraic groups and writes `VERIFICATION_RECEIPT.json`. The analytic interpolation/Hodge, time-integration, density, and uniform-integrability proofs are written above and are not machine-formalized by that receipt. Input replays, archive hashes, exploratory scripts/data, failed cases, and the exact compatible fixture are retained. External mathematical review remains required.

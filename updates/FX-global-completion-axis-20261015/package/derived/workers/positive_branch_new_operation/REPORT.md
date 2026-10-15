# Sharp positive branch: nonlocal projection and Burkholder operations

15 October 2026. Independent worker derivation. Historical priority is not
cleared; analytic arguments have not received external or formal review.

**Result:** the sharp positive-branch quasiconvexity problem remains
**UNKNOWN**. Two genuinely different proposed operations have rigorous
obstructions here. First, scalar-potential constrained projection can
strictly increase the energy on smooth compatible periodic maps, including
an explicit positive gradient-cap example. Second, positive superpositions
of invertibly transformed quartic Burkholder integrands cannot produce the
sharp generators. Neither statement is a quasiconvexity counterexample.

No new heat matrix, local two-form, SOS certificate, or unconstrained matrix
Young measure is used. Only the designated source report and designated
previous obstruction reports were read; no concurrent worker result is a
premise.

## 1. Exact input and notation

For a real matrix $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$, set

\[
u=a^2+c^2,\qquad j=ad-bc,\qquad
H=((a-d)^2+(b+c)^2)^2.
\]

The sharp generator under investigation is

\[
J_r(A)=\alpha H+\beta u^2+j^2+ruj,
\quad \alpha=\frac{3r}{8(r+2)},\quad
\beta=\frac{r(r-1)}6,\quad r>0.
\]

The inherited input states rank-one convexity, invariant extremality and
non-polyconvexity. The following projection obstruction does not require
those assertions. The moment reduction uses rank-one convexity only to
infer positivity of a constant-coefficient quadratic gradient functional.

All periodic averages below are normalized averages on

\[
Q=(\mathbb R/(2\pi\mathbb Z))^2.
\]

## 2. The scalar projection operation and its correct scope

The preliminary primary paper [Agazzi et al., arXiv:2609.28311v1](https://arxiv.org/html/2609.28311v1)
uses $L^2$-projection of a scalar potential onto a convex gradient
constraint. Its load-bearing scalar steps were reconstructed: closure of
the feasible set follows from the common Lipschitz bound and bounded means;
the Hilbert projection inequality holds; a support-function bump rules out
an interior constrained gradient wherever the residual potential is
nonzero; translations of the projected potential give a nonnegative
gradient cross term. The paper's later implications to all Burkholder
integrands and the sharp Beurling norm are not premises here.

Concretely, let $u(x)=p\cdot x+\eta(x)$, $p\in K$, and let $\zeta$
project $\eta$ onto potentials with $p+D\zeta\in K$. Write
$w=p\cdot x+\zeta$. The relevant conclusions are

\[
Dw=Du\ \text{or}\ Dw\in\partial K\quad\text{a.e.},
\qquad
\langle Dw\cdot(Du-Dw)\rangle\ge0.
\tag{2.1}
\]

A useful consequence is contraction of every convex radial scalar
Dirichlet energy for a ball $K=\overline B_\rho$. If
$\Psi(z)=\psi(|z|)$, then on the set where $Du-Dw\ne0$,

\[
D\Psi(Dw)=\frac{\psi'(\rho)}\rho Dw.
\]

Convexity and (2.1) therefore give

\[
\langle\Psi(Du)-\Psi(Dw)\rangle
\ge\frac{\psi'(\rho)}\rho
\langle Dw\cdot(Du-Dw)\rangle\ge0.
\tag{2.2}
\]

The same argument works for an ellipsoid and a matching constant positive
quadratic metric, using translations in arbitrary spatial directions.
This scalar fact supplies no monotonicity for a vector energy containing
coupled determinant terms.

## 3. Compatible failure of scalar-component projection, for every r>0

Put

\[
P=r-4\alpha=\frac{r(2r+1)}{2(r+2)},\qquad
Q_0=-4\alpha=-\frac{3r}{2(r+2)},
\]

and define smooth periodic scalar functions

\[
\psi=\sin x+\sin y,
\qquad
\phi=-2\cos x\cos y(P\sin x-Q_0\sin y).
\]

Consider the compatible vector map

\[
v_\varepsilon=(\varepsilon\phi,\psi),\qquad
E_r(\varepsilon)=\langle J_r(Dv_\varepsilon)\rangle.
\]

Projecting the first scalar potential onto constants gives

\[
v_\varepsilon\longmapsto (0,\psi),
\tag{3.1}
\]

because $\phi$ has mean zero. This is precisely scalar-potential
$L^2$-projection with the closed convex gradient constraint $K=\{0\}$.
Both input and output are actual compatible periodic gradients.

Here is a direct first-variation proof that the operation raises the
energy. At $\varepsilon=0$, put $c=\psi_x$, $d=\psi_y$, and

\[
\kappa=r c^2-4\alpha(c^2+d^2).
\]

Expanding the defining polynomial gives

\[
E'_r(0)=\langle\kappa(\phi_x\psi_y-\phi_y\psi_x)\rangle
=-\langle\phi(\kappa_x\psi_y-\kappa_y\psi_x)\rangle.
\]

The displayed construction is exactly
$\phi=\kappa_x\psi_y-\kappa_y\psi_x$. Consequently

\[
E'_r(0)=-\langle\phi^2\rangle
=-\frac{P^2+Q_0^2}{4}
=-\frac{r^2(2r^2+2r+5)}{8(r+2)^2}<0.
\tag{3.2}
\]

There is also an explicit universal rational small parameter. Exact
trigonometric integration gives

\[
E_r(\varepsilon)=C_0-\delta\varepsilon
+C_2\varepsilon^2+C_3\varepsilon^3+C_4\varepsilon^4,
\tag{3.3}
\]

where

\[
\begin{aligned}
C_0&=\frac{r(2r^2+2r+11)}{32(r+2)},\\
\delta&=\frac{r^2(2r^2+2r+5)}{8(r+2)^2},\\
C_2&=\frac{r^2(64r^5+128r^4+1224r^3+932r^2+2569r+1320)}{384(r+2)^3},\\
C_3&=\frac{3r^4(2r+1)(8r^2+26r+29)}{64(r+2)^4},\\
C_4&=\frac{3r^5(512r^6+1536r^5+2824r^4+3088r^3+6174r^2+4886r+7305)}{4096(r+2)^5}.
\end{aligned}
\]

Every displayed coefficient is strictly positive for $r>0$. Set

\[
S=C_2+C_3+C_4,\qquad
\varepsilon_r=\frac{\delta C_0}
{2[\delta^2+C_0(S+\delta)]}.
\tag{3.4}
\]

Then

\[
0<\varepsilon_r<\tfrac12,\qquad
\varepsilon_r\le\frac{\delta}{2(S+\delta)},\qquad
\varepsilon_r\le\frac{C_0}{2\delta}.
\]

Using (3.3) gives the rigorous bounds

\[
\boxed{\frac{C_0}{2}\le E_r(\varepsilon_r)
\le C_0-\frac{\delta\varepsilon_r}{2}<C_0.}
\tag{3.5}
\]

Thus the projection strictly increases a strictly positive energy, for
every $r>0$. The arithmetic does not construct negative Jensen energy.

### An explicit positive-radius constraint

At $r=1$, the construction simplifies to

\[
\phi=-(\sin x+\sin y)\cos x\cos y,
\qquad \varepsilon=\tfrac1{10}.
\]

Its exact energy polynomial is

\[
E_1(\varepsilon)=
\frac{325\varepsilon^4+448\varepsilon^3+2464\varepsilon^2
-512\varepsilon+640}{4096}.
\]

Therefore

\[
E_1(0)=\frac5{32},\quad
E_1(1/10)=\frac{1227841}{8192000},\quad
\Delta=E_1(0)-E_1(1/10)=\frac{52159}{8192000}>0.
\tag{3.6}
\]

The obstruction persists for the nondegenerate closed disk

\[
K=\overline B_\rho,
\qquad \rho=\frac{\Delta}{26}=\frac{52159}{212992000}>0.
\tag{3.7}
\]

Indeed let $w$ be *any* periodic scalar potential with $|Dw|\le\rho$
a.e. and keep the second component $\psi$. The $L^2$-projection is
one such potential. With $(p,q)=Dw$, $(c,d)=D\psi$, write

\[
A_0=\begin{pmatrix}0&0\\c&d\end{pmatrix},\quad
R=\begin{pmatrix}p&q\\0&0\end{pmatrix}.
\]

Here $|c|,|d|\le1$, $|R|\le\rho<1$. The distortion vector changes
by $(p,q)$. Hence

\[
\frac18|H(A_0+R)-H(A_0)|
\le\frac12(\sqrt2+\rho)^3\rho\le\frac{125}{16}\rho.
\]

Also $|j|\le\sqrt2\rho$, $j^2\le2\rho$, and
$|u j|\le2\sqrt2\rho\le3\rho$. Since $\beta=0$,

\[
|J_1(A_0+R)-J_1(A_0)|
\le\frac{205}{16}\rho<13\rho.
\]

It follows that every feasible projected output satisfies

\[
\langle J_1(D(w,\psi))\rangle
\ge E_1(0)-13\rho
=E_1(1/10)+\frac{52159}{16384000}.
\tag{3.8}
\]

This is a rigorous compatible energy gap for an actual positive-radius
gradient constraint. An explicit formula for the projected potential is
unnecessary because the bound holds for every feasible output.

**Scope:** arbitrary scalar-component constrained projection is not
universally $J_r$-energy decreasing. A coupled vector projection, a
background-specific choice used in a different support inequality, or an
operation which compensates by other terms is not excluded. The correct
scalar projection lemma itself is not refuted.

## 4. Burkholder positive superpositions have the wrong contact type

Define the standard quartic Burkholder expression using the operator norm

\[
\mathcal B_4(A)=\|A\|_{\rm op}^4-2\det A\,\|A\|_{\rm op}^2.
\]

The following elementary fact does not use its asserted quasiconvexity.

**Strict relative-shear lemma.** If $A$ is invertible, $R\ne0$ is rank
one, and $\operatorname{tr}(A^{-1}R)=0$, then

\[
\liminf_{t\to0}
\frac{\mathcal B_4(A+tR)+\mathcal B_4(A-tR)-2\mathcal B_4(A)}{t^2}>0.
\tag{4.1}
\]

The limit can be $+\infty$. Each symmetric difference is nonnegative.

Proof: the determinant is exactly constant on the whole line, because
$\det R=0$ and its linear derivative vanishes. Write its value as $j$
and put $\lambda(t)=\|A+tR\|_{\rm op}^2$. The latter is convex as a
supremum of squared norms of linear functions. The function
$h_j(\lambda)=\lambda^2-2j\lambda$ is convex and nondecreasing for
$\lambda\ge|j|$. This proves the nonnegative symmetric-difference claim.

For strictness, use a signed singular-value frame

\[
A=\operatorname{diag}(x,kx),\quad x>0,\quad -1<k<1,\quad k\ne0,
\qquad
R=\begin{pmatrix}a&b\\c&-ka\end{pmatrix}.
\]

Rank one gives $bc=-ka^2$. Implicit differentiation of

\[
|A+tR|_F^2=\lambda(t)+\frac{j^2}{\lambda(t)}
\]

at $\lambda(0)=x^2$ yields

\[
\frac{d^2}{dt^2}\mathcal B_4(A+tR)\bigg|_{t=0}
=\frac{4x^2}{1+k}
\big[(3+2k-3k^2)a^2+b^2+c^2\big].
\tag{4.2}
\]

For $0<k<1$, the bracket equals

\[
(3+4k-3k^2)a^2+(b+c)^2,
\]

where $3+4k-3k^2\ge3$. For $-1<k<0$, it equals

\[
3(1-k^2)a^2+(b-c)^2.
\]

Each is strictly positive for a nonzero rank-one $R$ with the stated
constraint. At the positive conformal endpoint $k=1$, write
$\rho_R=|R|_F^2>0$. Then $j=x^2$ and
$|A+tR|_F^2=2x^2+\rho_Rt^2$. Direct expansion gives second variation
$2x^2\rho_R>0$. At $k=-1$ the symmetric difference is
$8x^3\sqrt{\rho_R}|t|+O(t^2)$, giving $+\infty$ in (4.1).
Proper left and right rotations preserve the norm, determinant and trace
constraint, so these cases cover every invertible $A$.

Now the sharp generators have the exact flat shear

\[
J_r(I+t e_{12})=J_r(I)+\alpha t^4.
\tag{4.3}
\]

For any invertible real $T,S$, the transformed Burkholder term

\[
G_{T,S}(A)=\mathcal B_4(TAS)
\]

has at $I,e_{12}$ the relative trace

\[
\operatorname{tr}((TS)^{-1}T e_{12}S)
=\operatorname{tr}(S^{-1}e_{12}S)=0.
\]

Thus every such nonzero transformed term has strictly positive quadratic
shear variation, whereas (4.3) has zero quadratic shear variation.

It follows that there is no identity

\[
J_r(A)=Q(A)+\int\mathcal B_4(T_\theta A S_\theta)\,d\mu(\theta)
\tag{4.4}
\]

with $Q$ rank-one convex, positive measure $\mu$ giving nonzero mass
to invertible transforms, and absolute integrability of the displayed
terms near $I,I\pm t e_{12}$. Divide the symmetric differences by
$t^2$: all integrands and the $Q$ contribution are nonnegative;
Fatou's lemma and (4.1) contradict the zero limit from (4.3). This covers
finite positive sums as well as well-defined positive superpositions.

If $T$ or $S$ is singular, its transformed expression is the convex
function $\|TAS\|_F^4$, because the transformed matrix has rank at most
one. Therefore allowing singular transforms only adds convex summands.
In particular, with a polyconvex $Q$, (4.4) is impossible even allowing
singular terms, using the inherited non-polyconvexity of $J_r$.

This obstruction remains valid **even if** the preliminary source's full
Burkholder quasiconvexity theorem is accepted. It does not exclude signed
representations, nonintegrable renormalizations, coefficient limits with
escaping transforms, other separating functions, or more elaborate uses
of the scalar projection operation.

## 5. A precise nonlocal theorem which would settle the sharp fibre

Let $V=D\varphi$ be an arbitrary smooth mean-zero compatible periodic
gradient, vectorize matrices in row-major order, and define

\[
A_V=\langle J_r(V)\rangle,\qquad
c_V=\langle DJ_r(V)\rangle,\qquad
K_V=\tfrac12\langle D^2J_r(V)\rangle.
\tag{5.1}
\]

Quartic homogeneity and symmetry of the fourth-order coefficient tensor
give the exact all-background identity

\[
\langle J_r(B+V)-J_r(B)\rangle
=A_V+c_V\cdot B+B^T K_V B.
\tag{5.2}
\]

The omitted linear-in-$V$ term integrates to zero. Rank-one convexity
implies $K_V\succeq0$, since for every fixed $B$,

\[
B^T K_V B=\tfrac12\langle D^2J_r(B)[D\varphi,D\varphi]\rangle\ge0.
\]

The last inequality follows by Fourier decomposition into rank-one modes
for the constant-coefficient Hessian at $B$. Consequently all-background
quasiconvexity is **equivalent** to the nonlocal inequality

\[
\boxed{c_V\in\operatorname{range}K_V,
\qquad c_V^T K_V^\dagger c_V\le4A_V}
\quad\text{for every compatible periodic }V.
\tag{5.3}
\]

Equivalently the moment matrix

\[
\begin{pmatrix}A_V&c_V^T/2\\c_V/2&K_V\end{pmatrix}\succeq0
\tag{5.4}
\]

must hold for all those gradients. This is an exact reformulation, not a
new proof of the desired inequality. It exposes the missing nonlocal
mixed cubic-to-quadratic estimate and eliminates affine-background
optimization from any counterexample construction.

Here the periodic formulation is equivalent to the usual domain
formulation: a compactly supported perturbation extends periodically in
a containing cell, and a periodic perturbation can be placed in larger
cells with a boundary cutoff whose contribution divided by volume tends
to zero. Quartic growth and bounded smooth gradients justify the cutoff
limit; density then handles the $W^{1,4}$ version.

If $c_V$ lies in the range, the best background is
$B=-K_V^\dagger c_V/2$. A rigorous negative Schur complement gives an
actual compatible Jensen violation. If the range condition fails, a
background in a null direction gives arbitrarily negative gaps. Local
heat cone separation supplies neither witness.

For three waves

\[
\varphi=p\sin(k\cdot x)+q\sin(l\cdot x)+s\sin((k+l)\cdot x),
\]

put $X=p\otimes k$, $Y=q\otimes l$, $Z=s\otimes(k+l)$, and let
$\mathsf T$ be the symmetric quartic tensor of $J_r$. Exact phase
averages give

\[
\begin{aligned}
A_V&=\tfrac38[J_r(X)+J_r(Y)+J_r(Z)]
+\tfrac32\sum_{U<W}\mathsf T(U,U,W,W),\\
c_V&=6\mathsf T(\,\cdot\,,X,Y,Z),\\
K_V&=3\sum_{U\in\{X,Y,Z\}}\mathsf T(\,\cdot\,,\,\cdot\,,U,U).
\end{aligned}
\tag{5.5}
\]

The coefficient identities for $k=e_1,l=e_2$, all six real amplitudes,
and every $r$ were checked exactly by independent Laurent-polynomial
constant-term extraction. General covectors use the same phase averages
when $k,l$ are independent. Rational independent covectors can be
rescaled to integer frequencies, giving a periodic compatible map on a
rectangle.

The saved search is a failed construction attempt: the fixed-covector
search ran 36 BFGS starts at each of

\[
r\in\{1/10,1/2,1,2,4,10,100\}
\]

without finding a negative affine-minimized gap. Some optimizations
terminated with precision-loss messages and some limit configurations
were singular. This supplies no bound valid for all amplitudes and no
evidence upgrading UNKNOWN. Numerical backgrounds are evaluated in the
actual quadratic polynomial after regularization; exact certification
would still be required for any negative candidate.

A second search allowed both independent spatial covectors to vary and
minimized the ratio of the all-background gap to the zero-background
energy. It used 24 starts at each of the same seven parameters. The best
reported relative gaps were approximately

\[
0.52449,\quad0.60208,\quad0.66771,\quad0.73531,
\quad0.76970,\quad0.79766,\quad0.81943.
\]

No negative candidate was found. Every best run reported precision loss;
several approached extremely unbalanced covector scales. These are
optimizer outputs, not certified minima, lower bounds or sharp constants.

## 6. A direct compatibility falsifier for an unsafe shortcut

The constrained projection acts on **potentials**, not by pointwise
clipping of their gradient vectors. For example, let
$u=\sin x\sin y$ and clip $Du$ radially to radius $1/2$. At
$(x,y)=(\pi/6,\pi/3)$, the original norm is $\sqrt{10}/4>1/2$, and
the clipped vector field has curl

\[
\partial_x\widetilde u_y-\partial_y\widetilde u_x
=\frac{2\sqrt3}{5\sqrt{10}}\ne0.
\]

Hence it is not a gradient even locally there. This shortcut cannot
replace the scalar-potential projection in a compatibility proof.

## 7. What remains and what is reproducible

The surviving sharp target is (5.3), or a different all-background
operation controlling its mixed cubic term. Independent scalar row
projection loses the coupled determinant information; standard positive
Burkholder representation has strictly positive curvature at the wrong
contact type. A useful next construction would have to couple scalar
potentials, use a separating function with a trace-free invertible
acoustic contact, or prove (5.3) directly. None has been achieved here.

Run

```
R/.venv/bin/python R/workers/positive_branch_new_operation/verify_new_operation.py
```

with $R$ the parent research directory. It uses SymPy only and checks
the exact shear identities, positivity decompositions, all-parameter
projection-energy coefficients, the rational positive-cap gap, the
clipping curl, and symbolic three-wave moments. Analytic projection
existence, the Fatou argument and the universal Fourier/Jensen passage
are written proofs, not formally verified code.

`PROJECTION_COUNTEREXAMPLE.json` stores the reproducible projection map,
coefficient formula and exact gaps. `EXACT_VERIFICATION.json` records the
actual completed checks. `explore_three_wave.py` and discovery JSONs keep
the failed numerical construction separate from proved statements.

No source package, worktree file, Git state or external application was
modified. **QC of $J_r$, r>0: UNKNOWN.**

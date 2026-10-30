# Exposed quasiconvex rays from the anisotropic acoustic zeros

All cones in this note consist of **real homogeneous quartic polynomials on
all real 2 by 2 matrices**. Extremality is in the full 35-dimensional space,
without any imposed invariance or restriction on a competitor's coefficients.

Put

\[
 F_u=T^2+4(r(u)-1)q^2+4\beta(u)qX,\quad
 \beta(u)=\frac{1-3u^2}{1+3u^2},\quad
 r(u)=4-\frac{12u}{1+3u^2}.
\]

Here \(T=|A|^2\), \(q=\det A\), and

\[
 X=a^2+c^2-b^2-d^2,\qquad Y=2(ab+cd),\qquad Z=2q.
\]

**Theorem.** For every real \(0<u<1/3\), \(F_u\) spans an exposed ray of the
full cone of rank-one-convex homogeneous quartics. Whenever \(F_u\) is
quasiconvex, the same functional exposes its ray in the full quasiconvex cone.

In particular, both supplied seeds are exposed quasiconvex rays: the

- \(u=1/6\) seed \(F_{11/13,28/13}\);
- \(u=1/30\) seed \(F_{299/301,1084/301}\).

The latter is non-polyconvex by the supplied unrestricted minor-support
contradiction. More generally, the **entire already certified interval**

\[
 |u-1/30|<2^{-206}
\]

is an arc of non-polyconvex exposed quasiconvex rays. The interval and its
quasiconvexity are inherited from `ARC_PROOF.txt`; the unrestricted exposed-ray
statement is established here. No quasiconvexity of the rest of the curved
boundary is inferred.

## 1. The full rank-one-convex cone has a useful PSD representation

If \(G\) is a homogeneous quartic, symmetry of its four-linear polarization
gives

\[
 D^2G(A)[R,R]=D^2G(R)[A,A]. \tag{1}
\]

Consequently \(G\) is rank-one convex if and only if the ordinary 4 by 4
matrix \(H_G(R)=D^2G(R)\) is positive semidefinite for **every rank-one** \(R\).
This is an unrestricted assertion about \(G\). It is not the 6 by 6
compatible-Hessian heat density, and does not assume a closed angular
correction exists for a competitor.

For completeness, rank-one convexity of the whole stated \(F_u\) arc can
also be checked directly. After positive homogeneous rescaling, align a
nonzero rank-one matrix to \(E_{11}\) by a left rotation and a right rotation. The transformed anisotropic term is

\[
4\beta q(cX+sY),\qquad c^2+s^2=1.
\]

At \(E_{11}\), its Hessian divided by 4 is

\[
 \begin{pmatrix}
 3&0&0&3\beta c\\
 0&1&-\beta c&2\beta s\\
 0&-\beta c&1&0\\
 3\beta c&2\beta s&0&2r-1
 \end{pmatrix}. \tag{2}
\]

Take the Schur complement of its upper block \(\operatorname{diag}(3,1)\). Its first diagonal entry is

\[
 1-\beta^2c^2>0,
\]

and, with \(z=c^2\) and \(z_*=(r-1)/(3\beta^2)\), its determinant is

\[
 2r-1-4\beta^2+2\beta^2(1-r)z+3\beta^4z^2
       =3\beta^4(z-z_*)^2. \tag{3}
\]

The equality follows from the specified \(\beta(u),r(u)\). Writing

\[
 B=1-3u^2,\quad H=1+3u^2,\quad M=1-4u+3u^2,
 \quad D=3u^2-3u+1,
\]

we have \(z_*=MH/B^2\) and \(B^2-MH=4uD>0\), so

\[
 0<z_*<1\qquad(0<u<1/3).
\]

Thus (2) is PSD at all rank-one directions, with exactly four projective
domain directions at which its determinant vanishes. Equation (1) proves
rank-one convexity directly.

## 2. An explicit positive exposing functional

The general operation is elementary but useful: if a finite collection of
acoustic kernel equations $H_G(R_j)K_j=0$ has only the one-dimensional
solution space spanned by a rank-one-convex quartic $F$, then the positive
linear functional $\sum_j K_j^{\mathsf T}H_G(R_j)K_j$ exposes its ray.
This follows from PSD matrix kernels and (1). It is a criterion for
extremality, not a completeness criterion for heat certificates. The
following construction applies it to the actual inherited acoustic zeros.

Use the exact acoustic data in the supplied `ARC_PROOF.txt`. For

\[
 R_t=\begin{pmatrix}1&t\\0&0\end{pmatrix},
 \qquad m_u(t)=B^2(1-t^2)^2-MH(1+t^2)^2,
\]

define the four-vector

\[
\begin{split}
 K_0&=-B[u(1-t^2)+Ht^2](1+t^2),\\
 K_1&=Bt[H-u(1-t^2)](1+t^2),\\
 K_2&=B^2t(1-t^2)-uHt(1+t^2)^2,\\
 K_3&=B^2t^2(1-t^2)+uH(1+t^2)^2.
\end{split} \tag{4}
\]

The leading coefficient of \(m_u\) is \(4uD>0\). Its monic form is

\[
 t^4-C(u)t^2+1,\qquad
 C(u)-2=\frac{(u-1)(3u-1)H}{uD}>0. \tag{5}
\]

Hence its four roots are real and simple. At every such root \(K\ne0\),
since \(K_0=-B[u+(H-u)t^2](1+t^2)<0\).

Direct exact polynomial reduction gives

\[
 H_{F_u}(R_t)K(t,u)=0\pmod {m_u}. \tag{6}
\]

The calculation below independently reconstructs (6) as part of its full
35-column calculation. It also checks the generic determinant identity

\[
 \det H_{F_u}(R_t)=\frac{2304}{H^4}m_u(t)^2. \tag{7}
\]

Let \(O_\theta\) denote a proper output rotation, acting on both matrices
and their four-vector representations. Define the linear functional

\[
 \mathcal L_u(G)=
 \sum_{m_u(t)=0}\frac1{2\pi}\int_0^{2\pi}
 (O_\theta K)^\mathsf T
 H_G(O_\theta R_t)(O_\theta K)\,d\theta. \tag{8}
\]

By (1), each integrand is nonnegative for every rank-one-convex quartic

\[
 \mathcal L_u(G)\ge0.
\]

Equation (6) and the left invariance of \(F_u\) give

\[
 \mathcal L_u(F_u)=0.
\]

This functional is not zero: it is positive on \(T^2\). If

\[
 G\text{ is rank-one convex},\qquad\mathcal L_u(G)=0,
\]

continuity and nonnegativity force every integrand to vanish. For a PSD
matrix, a vanishing quadratic value implies its full vector kernel equation.
Thus

\[
 H_G(O_\theta R_t)(O_\theta K)=0
\]

for every output angle and every root of \(m_u\). These are the equations
that make the exposed face one-dimensional.

The integral in (8) is a finite exact operation. Its integrand is a
homogeneous quartic in \((\cos\theta,\sin\theta)\). Its mean uses only the
moments \(3/8,1/8,3/8\) for the even monomials of degree four. Equivalently,
four angles \(0,\pi/4,\pi/2,3\pi/4\) give exact quadrature. Summing over the
four roots is the trace in the degree-four root algebra. Therefore (8) has
rational coefficients whenever \(u\) is rational. At \(u=1/30\) its literal
primitive integer coefficient vector is supplied in
`acoustic_face_result.json` and reconstructed by `verify_extreme.py`.

## 3. The exact full-space rank calculation

Write a general homogeneous quartic as

\[
 G=\sum_{i+j+k+l=4}g_{ijkl}a^ib^jc^kd^l.
\]

There are 35 independent coefficients. Use the unnormalized rotation

\[
 O_s=\begin{pmatrix}1&-s\\s&1\end{pmatrix}.
\]

It is a positive scalar times a proper rotation. After reducing (4) in

\[
 \mathbb Q(u)[t]/(m_u)
\]

and clearing its nonzero denominator \(uD\), form

\[
 H_G(O_sR_t)O_sK\pmod {m_u}. \tag{9}
\]

It has four components, degree at most 3 in \(s\), and degree at most 3 in \(t\).

The 64 coefficient equations are a \(64\times35\) rational matrix \(E(u)\).
Since \(m_u\) has four distinct real roots, the full acoustic kernel
equations imply exactly these coefficient equations. All its rational
denominators divide \(uD\), which never vanishes on the interval.

At \(u=1/30\), the monic acoustic polynomial and a primitive integer kernel
representative are particularly small:

\[
 m=t^4-\frac{83981}{2710}t^2+1,
\]

\[
 K=\begin{pmatrix}
 761510-25254181t^2\\
 761510t+1655520t^3\\
 810290t-1710280t^3\\
 810290-23400039t^2
 \end{pmatrix}. \tag{10}
\]

The standard-library verifier reconstructs every column, verifies an exact
nonzero \(34\times34\) determinant, and verifies \(E(1/30)F_{1/30}=0\).
Thus its rank is 34 and its nullspace is precisely the span of \(F_{1/30}\).
This finite seed result uses no symbolic package, optimizer, numerical
eigenvalue test, or imported producer code.

For the whole parameter interval, `generic_face.py` computes the same
minor symbolically over \(\mathbb Q[u]\), after nonzero row denominator
clearing. Its exact factorization is in `generic_face_result.json`.
Initially that one minor failed at four interior algebraic parameter values.
Those are not rank obstructions: `curve_rank.py` eliminates them using
different exact minors.

More explicitly, the only irreducible determinant factors with roots in

\[
 0<u<1/3
\]

are the following. Each has one root in this interval, as checked by exact
Sturm root counts.

| Irreducible factor \(p(u)\) | prime | root modulo prime | rank of \(uD E(u)\) there |
|---|---:|---:|---:|
| \(3u^2-6u+1\) | 101 | 14 | 34 |
| \(9u^4-12u^3+3u^2-4u+1\) | 103 | 7 | 34 |
| \(18u^4-45u^3+36u^2-15u+2\) | 101 | 33 | 34 |
| \(135u^6-594u^5+927u^4-732u^3+309u^2-66u+5\) | 107 | 3 | 34 |

These are exact divisibility witnesses, not parameter sampling evidence.
If all 34-minors vanished at a characteristic-zero root of an irreducible \(p\),
then \(p\) would divide every minor of the integer polynomial matrix \(uDE(u)\).
Reduction modulo a prime would then force rank below 34 at every modular
root of \(p\). The exhibited ranks contradict this. The saved data contain
the independent row and column indices for each witness.

Every other irreducible factor of the first minor has no root in the open
interval. The first minor handles all remaining parameters. Finally,

\[
 E(u)F_u=0
\]

is checked as a generic rational-function identity, with the coefficient of \(a^4\)
in \(F_u\) equal to 1. This gives rank at most 34 at every parameter. Hence

\[
 \operatorname{rank}E(u)=34\quad\text{for every }0<u<1/3. \tag{11}
\]

## 4. Exposed rays and a failed ordinary propagation mechanism

If \(G\) is rank-one convex and \(\mathcal L_u(G)=0\), equations (9)--(11) give \(G=\lambda F_u\). A
homogeneous rank-one-convex quartic is nonnegative at \(E_{11}\), and

\[
 F_u(E_{11})=1,
\]

so \(\lambda\ge0\). Thus (8) exposes precisely the ray \(\mathbb R_{\ge0}F_u\), proving the theorem. Since quasiconvexity implies
rank-one convexity, the same exposing functional works in the quasiconvex
cone whenever the ray belongs to that cone.

At the non-polyconvex seed and its certified arc, an immediate consequence
is that **no nonzero polyconvex homogeneous quartic can be subtracted while
retaining rank-one convexity**. Otherwise

\[
 F_u=G+P,\quad G\text{ rank-one convex},\quad
 P\ne0\text{ polyconvex}
\]

would force \(P\) to be a positive multiple of the non-polyconvex \(F_u\).
This rules out arbitrary polyconvex quartic summands, not a chosen polynomial
minor-lift ansatz.

There is also an exact obstruction to extending the known invariant
classification by ordinary transformations and conic mixing. If a quartic \(Q\)
is invariant under both left and right proper rotations, those rotations
act transitively on rank-one matrices of fixed norm. Consequently its
Hessian is singular at every nonzero rank-one matrix, or at none of them.
An invertible pullback \(A\mapsto LAR\) preserves that all-or-none property.
But \(F_u\) has both kinds: (7) is nonzero at \(t=0\), and zero at the four
real acoustic directions. Therefore \(F_u\) is not proportional to any such
pullback of any invariant quartic.

Since \(F_u\) is an extreme rank-one-convex ray, any exact finite conic
decomposition into rank-one-convex quartics would require each nonzero
summand to be proportional to \(F_u\). Therefore the non-polyconvex
quasiconvex arc cannot be obtained by mixing polyconvex quartics and linear
pullbacks of the classified invariant quartics. Singular left or right
pullbacks of an invariant rank-one-convex quartic are convex: on rank-one
matrices an invariant quartic equals \(a|A|^4\) with \(a\ge0\). They give no
exception. No claim about limits of unbounded or degenerating conic
decompositions is made.

This is the substantive obstruction to that ordinary propagation attack.
The new opening is structural: the angular certificate reaches exposed
quasiconvex rays unavailable through those exact decompositions. It is not
a counterexample to rank-one convexity implying quasiconvexity.

## 5. Inputs, checks, and remaining obligation

The governing supplied inputs were `FACTS.txt`, `PROOF.txt`,
`ARC_PROOF.txt`, `seed_299_301.json`, and `receive_boundary.py` in the shared
angular case directory. The literal B1 receiver was executed successfully:
it rebuilt the actual primitive and density, verified all 6,321 positive
coefficient matrices, and checked the unrestricted non-polyconvex support
gap \(34938784681/901552190\). These inherited quasiconvexity and
non-polyconvexity claims are not replaced by the rank calculation.

The already cited primary paper
[Bruno--Pasqualotto, arXiv:2608.06367v1](https://arxiv.org/html/2608.06367v1)
was read. Its Theorem 2 and Appendix A concern quartics invariant under
both left and right rotations; the nonexistence result in Section 4
compares against that actual scope. The paper's heat/exact-form method is
ancestry, rather than a classification of this anisotropic family.

Reproduce the finite seed theorem with:

```sh
python3 verify_extreme.py
```

Reproduce the whole-curve arithmetic proof, using SymPy, with:

```sh
python3 acoustic_face.py
python3 generic_face.py
python3 curve_rank.py
```

The generic determinant computation took about 100 seconds in the local
runtime. The independent standard-library seed verification took about
0.02 seconds. These are costs of these concrete calculations, not general
complexity claims. Scientific code and exact coefficient data are all in
this assigned directory.

The central unresolved obligation remains quasiconvexity on the rest of
the curved boundary (or a genuine quasiconvexity counterexample), including
the acquisition/completeness of an admissible closed correction. Extremality
does not supply that correction or imply quasiconvexity. The whole quartic
classification, gradient Young-measure rigidity, and any quantitative strong
quasiconvexity modulus are not established here. The supplied B0
polyconvexity question is also left at its supplied scope. Historical
priority of the exposed-ray theorem has not been established.

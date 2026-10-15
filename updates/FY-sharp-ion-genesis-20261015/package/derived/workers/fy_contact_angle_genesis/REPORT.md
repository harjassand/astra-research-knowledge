# Exact finite-H completion for every finite nonzero contact angle

15 October 2026. Original internal derivation by `fy_contact_angle_genesis`.
Status: analytic theorem with 363 passing exact assertions in the accompanying
verification receipt. External correctness, formal verification, and historical
originality remain UNKNOWN. The new content is the complete generic-angle
projection and its boundary exclusions. Sufficiency uses the pinned N873
degenerate-flat analytic mechanism; that mechanism is credited rather than
presented as a new discovery.

Pinned read-only checkout:
`/Users/harjas/Documents/ChatGPT/ultra/work/astra-sharp-ion-20261015`,
`b32943eeb62d0d79929a9e572a344219a785ebf9`.
Only this worker directory was written. No current other-worker artifacts were
read; no source, checkout, or Git content was edited. The unavailable incoming
ZIP is not a premise.

## 1. Exact theorem

Let V be the nine-dimensional real space of left-SO(2)-invariant homogeneous
quartics on real 2-by-2 matrices. Throughout this theorem, fix a real
`t != 0`, finite. First use the equivalent contact normal form

\[
 R_t=\begin{pmatrix}t&0\\1&0\end{pmatrix}
     =(t,1)\otimes e_1,\qquad B=I.
\]

For `A=[[a,b],[c,d]]`, put

\[
u=a^2+c^2,\quad v=b^2+d^2,\quad w=ab+cd,\quad j=ad-bc,
\]
\[
H=((a-d)^2+(b+c)^2)^2,\quad n=1+t^2,
\quad L_t=t w-j+v,
\quad B_t=v\left(j-\frac{2L_t}{n}\right).
\]

**Contact-span theorem.** If F is rank-one convex and
`D^2F(I)[R_t,R_t]=0`, then it has the unique form

\[
 F=\alpha H+G,\qquad G=kL_t^2+\ell B_t+m v^2. \tag{1}
\]

Every polynomial (1) has the indicated contact, even without rank-one
convexity. The converse span claim does require rank-one convexity or
quasiconvexity in addition to the contact equality.

Set

\[
A_0=2m-\ell,\quad B_0=2m+\ell,
\quad \Delta=k n^2 A_0B_0-\ell^2(t^2B_0+3A_0). \tag{2}
\]

**Exact projection theorem.** For every real triple `(k,ell,m)`, the following
are equivalent:

1. Some finite real alpha makes (1) rank-one convex on all real matrices.
2. Some finite real alpha makes (1) quasiconvex at every real affine background.
3. Either

\[
 k=\ell=0,\quad m\ge0, \tag{3a}
\]

or

\[
 m>|\ell|/2,\qquad \Delta>0. \tag{3b}
\]

Condition (3b) automatically implies `k>0`. In (3a), every `alpha>=0`
works by ordinary convexity. In (3b), every sufficiently large nonnegative
alpha works, with an exact coefficient specified below.

The quasiconvexity quantifiers are every bounded planar Lipschitz domain
Omega, every B in `R^(2x2)`, and every `phi in W_0^(1,4)(Omega;R^2)`.
The periodic inequality also holds. This is an equality of the projections
after deleting alpha; it does not identify the least alpha or equate the
unprojected ROC and QC cones.

### Return to the requested contact `(I,e1 tensor(t,1))`

Let

\[
 U_t=\frac1{\sqrt n}\begin{pmatrix}t&1\\1&-t\end{pmatrix}.
\]

It is orthogonal, symmetric, and has determinant -1. It fixes I by
conjugation and sends `e1 tensor(t,1)` to R_t. If the requested polynomial
is F, apply the theorem to `F_t(A)=F(U_t^T A U_t)`. Orthogonal conjugation
preserves left-SO(2) invariance, H, rank-one convexity, and the full QC test
contract: use `phi_t(x)=U_t phi(U_t^T x)` and the orthogonally transformed
domain. Although U_t contains a square root, the entries of
`U_t A U_t^T` are rational functions of rational t, with denominator n.
No irrational input oracle is needed in the rational compiler.

## 2. Stationarity gives exactly the four-dimensional span

Use the invariant basis

`u^2, uv, v^2, uw, vw, w^2, uj, vj, wj`

and write its coefficients `f0,...,f8`. Its independence follows either
from direct polynomial coefficients or the Hermitian representation on
`(z^2,zy,y^2)` for column coordinates `z=a+ic, y=b+id`.

For a rank-one-convex C2 polynomial,

\[
h_F(B,p,q)=\tfrac12D^2F(B)[p\otimes q,p\otimes q]\ge0.
\]

At its zero `(I,(t,1),e1)`, every first derivative in B,p,q vanishes.
Exact elimination gives five independent linear equations:

\[
f_0+f_6/4=0,\qquad f_1+3f_6/2+f_8/(2t)=0,\qquad f_3=0,
\]
\[
f_4-\frac{2t}{t^2+3}f_6+\frac{2t}{t^2+3}f_7
       +\frac{n}{t^2+3}f_8=0,
\qquad f_5-f_6+\frac{t^2-1}{2t}f_8=0. \tag{4}
\]

The coefficient columns of `H,L_t^2,B_t,v^2` in this basis are

\[
\begin{pmatrix}
1&0&0&0\\
6&1&0&0\\
1&1&-2/n&1\\
0&0&0&0\\
0&2t&-2t/n&0\\
-4&t^2-1&0&0\\
-4&0&0&0\\
-4&-2&(t^2+3)/n&0\\
0&-2t&0&0
\end{pmatrix}. \tag{5}
\]

They are independent for t nonzero and span the kernel of (4). In particular,

\[
\alpha=-f_6/4,\quad k=-f_8/(2t),\quad
\ell=\frac n{t^2+3}(f_7+4\alpha+2k),\quad
m=f_2-\alpha-k+2\ell/n. \tag{6}
\]

Contact equality alone is weaker. For example,
`u^2-((6t^2+2)/n)uv` has the displayed contact but its background a
derivative of h is `12t^2+4`, which is nonzero. It is not rank-one convex
and is outside (1).

Quasiconvexity supplies the same necessity: the quadratic second variation
and cutoff plane waves imply the Legendre-Hadamard inequality, hence
nonnegativity of h. This is the standard necessary direction, not any
unproved planar ROC-to-QC implication.

## 3. The forced quadratic support and all weak cases

For an arbitrary increment X with entries again `(a,b,c,d)`, introduce

\[
x=-a+t(b+c)+d=DL_t(I)[X].
\]

Direct Taylor expansion gives the exact identity

\[
\tfrac12D^2G(I)[X,X]-3\ell\det X
=Q(X)
=k x^2+\frac{2\ell}{n}(tb-3d)x+A_0b^2+3B_0d^2. \tag{7}
\]

The multiplier `lambda=3ell` is forced if a PSD determinant support exists.
Indeed R_t is a rank-one contact, so a PSD support must annihilate R_t;
polarizing against all E in (7) forces this multiplier uniquely.
Thus lambda-finding, an open service for the full-space compiler, is absent
on this contact stratum.

On rank-one X the determinant term vanishes. For arbitrary `(x,b,d)` with
`td-b != 0`, choose

\[
c=\frac{xd-tbd-d^2}{td-b},\qquad a=t(b+c)+d-x. \tag{8}
\]

Then `det X=0`. This dense set of triples shows that the acoustic
inequality at I forces Q to be nonnegative on every triple. Equivalently,

\[
C=\begin{pmatrix}
k&\ell t/n&-3\ell/n\\
\ell t/n&A_0&0\\
-3\ell/n&0&3B_0
\end{pmatrix}\succeq0,\qquad \det C=3\Delta/n^2. \tag{9}
\]

All weak cases are now explicit:

* If `ell=0`, (9) is equivalent to `k>=0,m>=0`.
* If `ell!=0`, its nonzero off-diagonal entries and `t!=0` force
  `A_0>0,B_0>0`; Schur complementation then makes (9) equivalent to
  `Delta>=0`.

For the second assertion, a zero diagonal in a PSD matrix has a zero row.
Here the first off-diagonal entry rules out `A_0=0`, and the second rules
out `B_0=0`. These arguments cover all rank deficiencies, not merely a
generic open subset of the weak cone.

## 4. Every non-convex singular boundary is impossible

The completion H has zero Hessian and zero cubic tensor at I. Consequently
it cannot change any first background derivative of an acoustic zero there.

### 4.1 `ell!=0`, `Delta=0`

Assume the weak conditions, so `A_0,B_0>0` and

\[
k=\frac{\ell^2(t^2B_0+3A_0)}{n^2A_0B_0}. \tag{10}
\]

Besides R_t, the quadratic kernel contains the exactly rank-one matrix

\[
Z=\begin{pmatrix}
-\dfrac{B_0t^2+A_0}{2A_0n}&-\dfrac{\ell t}{A_0n}\\
\dfrac{B_0t^2+A_0}{2tB_0n}&\dfrac{\ell}{B_0n}
\end{pmatrix}
=\frac{(-tB_0,A_0)\otimes(B_0t^2+A_0,2\ell t)}
       {2tA_0B_0n}. \tag{11}
\]

It is nonzero, has `x(Z)=1`, and satisfies `Q(Z)=det Z=0`.
It is independent of R_t. In fact, the full kernel plane is parametrized by
`x` and `c` with

\[
b=-\frac{\ell t}{nA_0}x,\quad d=\frac{\ell}{nB_0}x,
\]

and its determinant has nonzero mixed coefficient

\[
td-b=\frac{4\ell tm}{nA_0B_0}x. \tag{12}
\]

Thus the determinant quadric meets this kernel plane in two distinct
rank-one lines. Formula (11) is its second line.

Write

\[
P=mB_0^2t^2+A_0^2(2\ell+m),
\]
\[
S=B_0^3t^4+2(4m-3\ell)A_0B_0t^2+3A_0^3. \tag{13}
\]

The complete background gradient of the half-acoustic polynomial at this
second contact is the exact identity

\[
g:=D_B h_G(I;Z)
=\frac{\ell^3t}{A_0^3B_0^2n^3}
       (-4tP,S,S,4tP). \tag{14}
\]

This vector is never zero in the allowed boundary region. If `ell>0`,
then `m>0` and `P>0`. If `ell<0`, all three coefficients of S as a
polynomial in `t^2` are positive, so `S>0`. This is the decisive sign
argument; no numerical search or unproved flatness necessity is used.

For each proposed finite alpha, take `E=-g` and put
`T_alpha=h_(G+alpha H)(E;Z)`. Since h is quadratic in its background,

\[
h_{G+\alpha H}(I+\epsilon E;Z)
=-|g|^2\epsilon+T_\alpha\epsilon^2.
\]

The explicit positive choice

\[
\epsilon=\min\left(\frac12,
              \frac{|g|^2}{2(|T_\alpha|+1)}\right) \tag{15}
\]

makes this strictly negative. Therefore no finite alpha gives rank-one
convexity, and hence none gives quasiconvexity.

### 4.2 `ell=m=0`, `k>0`

Here `G=kL_t^2`, and Q has rank one. Take

\[
Z_0=(1,-t)\otimes e_2=\begin{pmatrix}0&1\\0&-t\end{pmatrix}.
\]

Then `det Z_0=0`, `x(Z_0)=0`, and `L_t(Z_0)=n`. Thus

\[
h_G(I;Z_0)=0,\qquad
D_Bh_G(I;Z_0)=2kn(-1,t,t,1)\ne0. \tag{16}
\]

The same exact witness construction (15) excludes every finite alpha.

### 4.3 Exhaustion

If `ell=0,k=0,m>=0`, G is `m v^2`, an ordinary convex quartic.
If `ell=0,k>0,m>0`, C is positive definite and is in (3b).
The remaining weak case is (16). If `ell!=0`, the weak cone consists
exactly of its positive-definite interior and boundary (10), already
settled. Outside the weak cone (7)--(9) already violate a necessary
acoustic inequality. This exhausts every real coefficient triple.

## 5. Analytic completion, all backgrounds and test functions

In (3b), C is positive definite, and (7) has kernel exactly `span{R_t}`.
Background stationarity at the original contact gives

\[
T(I,R_t,R_t,E)=0\quad\hbox{for every }E,
\]

where `G(X)=T(X,X,X,X)` is the symmetric polarization. Hence the exact
kernel-pair flatness predicate of the pinned N873 compiler holds.
The reduction to a one-dimensional rank-one kernel is why its sufficient
predicate becomes necessary for finite completion on this generic stratum.

For completeness, here is the analytic absorption argument actually used.
Let M be the sum of absolute expanded coefficients of G, which bounds the
four-linear norm of T. Let `kappa>0` be a lower bound for Q on its kernel
orthogonal complement. Set `S_3(U,V,W)=T(I,U,V,W)` and `J0=sqrt(2)M`.
For `X=Z+Y`, where `Z in ker Q` and `Y perpendicular ker Q`, flatness gives

\[
|S_3(E,X,X)|\le3J0|E||X||Y|,
\qquad |S_3(X,X,X)|\le4J0|X||Y|^2. \tag{17}
\]

Rotate the target to write any affine background as `B=sI+E`, with
`s>=0` and E anticonformal. Left invariance preserves the test contract.
Then `|CB|^2=2|E|^2` for `CA=(a-d,b+c)`. Expand the entire quartic Taylor
remainder, integrate, and remove the constant-coefficient determinant term
using `integral det Dphi=0`. Applying Young's inequality to (17) gives

\[
\begin{split}
\int [G(B+X)-G(B)-DG(B):X]\ge{}&
\frac\kappa2s^2\int|Y|^2
-(2592M^2/\kappa+8M)|E|^2\int|X|^2\\
&-(512M^2/\kappa+3M)\int|X|^4,
\qquad X=D\phi. \tag{18}
\end{split}
\]

There is no higher-order remainder. The mixed quadratic term costs
`kappa s^2|Y|^2/4 +1296J0^2|E|^2|X|^2/kappa`; the conformal cubic costs
`kappa s^2|Y|^2/4 +256J0^2|X|^4/kappa`. The other terms cost
`8M|E|^2|X|^2+3M|X|^4`. These are the pinned compiler's conservative
Taylor/Young constants, included to specify the exact dependency.

For H, its Bregman remainder satisfies

\[
H(B+X)-H(B)-DH(B):X
\ge|CB|^2|CX|^2+|CX|^4/5,
\]

and separately is at least `|CX|^4/3`. Both follow by completing squares
in `|x+y|^4-|x|^4-4|x|^2 x.y`.
For compactly supported gradients, the exact L2 identity and a classical
nonsharp Cauchy-Riemann L4 estimate give

\[
\int|CX|^2=\int|X|^2,\qquad
\int|X|^4\le(625/4)\int|CX|^4. \tag{19}
\]

The latter uses only the standard finite complex Beurling bound
`||B||_4<=sqrt(24)`, as in pinned N873; no sharp-norm conjecture is used.
Any finite classical L4 bound suffices for the existential theorem.
Combining (18)--(19), every

\[
\alpha\ge\alpha_*:=401296\frac{M^2}{\kappa}+\frac{9391}{4}M \tag{20}
\]

gives the full QC inequality. The linear terms integrate to zero.
Smooth zero-boundary tests extend by strong W^(1,4) density and quartic
growth. For periodic tests, tile a large square and cut off in its boundary
layer; bulk area is quadratic in the tile count while boundary error is
linear, so division by area gives the periodic inequality. Smooth
approximation extends that statement to periodic W^(1,4) maps.

An additional `nu H`, `nu>=0`, supplies the uniform numerical margin

\[
\int_\Omega[F(B+D\phi)-F(B)]
\ge\frac{4\nu}{1875}\int_\Omega|D\phi|^4
\quad\hbox{if }\alpha\ge\alpha_*+\nu. \tag{21}
\]

This proves the sufficient direction analytically, not by a finite grid.

### Exact rational coefficient

Put

\[
J=\begin{pmatrix}-1&t&t&1\\0&1&0&0\\0&0&0&1\end{pmatrix},
\qquad Q_4=J^TCJ.
\]

In (3b), Q_4 has three positive eigenvalues and one zero eigenvalue. Let
e2 and e3 be its second and third elementary symmetric functions, computed
as sums of principal minors. The rational number

\[
\kappa=e_3(Q_4)/e_2(Q_4)
=\left(\sum_{i=1}^3\lambda_i^{-1}\right)^{-1}>0 \tag{22}
\]

is at most the smallest positive eigenvalue. One check is
`e3(Q_4)=3Delta/n`. Formulae (20),(22) and expanded M are a fixed exact
compiler; no eigenvalue approximation or supplied lambda is hidden.

### A necessary coefficient blowup, rather than only a large sufficient bound

Fix `t=1, ell=m=1, k=1/2+eta`, with `eta>0`. Here `Delta=12eta`, so the
theorem admits a QC completion for every positive eta. Take the fixed
rank-one direction and anticonformal background increment

\[
Z=\begin{pmatrix}-1&-1/2\\1/3&1/6\end{pmatrix},\qquad
E=\begin{pmatrix}2/3&-1/2\\-1/2&-2/3\end{pmatrix}.
\]

The exact half-acoustic polynomial on the affine line of backgrounds is

\[
h_{G_\eta+\alpha H}(I+sE;Z)
=\eta-\frac{5(18\eta+5)}{18}s
+\left[\frac{25(68\eta+25)}{648}+\frac{1250}{81}\alpha\right]s^2.
\]

Nonnegativity for every real s forces its discriminant to be nonpositive.
Thus **every** ROC completion, and hence every QC completion, satisfies

\[
\boxed{\alpha\ge\frac1{32\eta}+\frac{13}{80}+\frac{47}{200}\eta.} \tag{25}
\]

The divergence is therefore intrinsic. The sufficient formula (20) also
grows at most as a constant times `1/eta` on this family near zero, because
M stays bounded and `e3=18eta` while e2 tends to a positive rank-two value.
This establishes the order of the required coefficient blowup, without
identifying its sharp leading constant or least-alpha threshold. It also
exhibits a nonclosed projected cone: the completed coefficients converge
to an excluded boundary triple.

## 6. The exceptional limits are checked, not silently included

### Trace-free `t=0`

Our necessary quadratic identity still makes sense, but the generic
boundary exclusion does not. At t=0,

\[
G=k j^2+(-2k+3\ell)vj+(k-2\ell+m)v^2,
\]

\[
C_0=\begin{pmatrix}k&0&-3\ell\\0&2m-\ell&0\\-3\ell&0&3(2m+\ell)\end{pmatrix}.
\]

For the inherited sharp family, after the 90-degree orthogonal conjugation
that exchanges u and v, take

\[
k=1,\qquad \ell=(r+2)/3,\qquad m=(r+1)(r+2)/6. \tag{23}
\]

This gives exactly
`j^2+r vj+r(r-1)v^2/6`. For `r(r+2)>0`, C_0 is PSD of rank two:

\[
A_0=r(r+2)/3>0,\quad B_0=(r+2)^2/3>0,
\quad kB_0=3\ell^2.
\]

Its kernel is `span{e21,diag(-(r+1),1)}`. On that plane,

\[
\det(s e21+z\operatorname{diag}(-(r+1),1))=-(r+1)z^2.
\]

Since `r<-2` or `r>0`, there is exactly one rank-one line, counted with
double intersection multiplicity. The second line (11) has coalesced into
it. The inherited heat proof admits QC completion on this sharp boundary;
the generic theorem explicitly excludes t=0 and does not contradict it.
The kernel-pair flatness compiler fails here: on the diagonal kernel vector,
the cubic tensor is `-r(r+2)/12`, exactly as in N873 after conjugation.

### Nonshear `|t| -> infinity`

Fix `(K,E,M)` in the nonshear notation and set
`k_t=K/t^2, ell_t=E, m_t=M`. Then

\[
k_tL_t^2+E B_t+M v^2\longrightarrow K w^2+E vj+M v^2,
\]

and

\[
\frac{\Delta_t}{t^2}\longrightarrow
(2M+E)\,[K(2M-E)-E^2]. \tag{24}
\]

The limiting strict conditions are precisely the nonshear N873 conditions
`K>0, E+2M>0, 2KM-KE-E^2>0`. The two generic rank-one kernel lines can
coalesce in this limit; the separate nonshear boundary proof remains
needed. No uniform alpha bound across either singular limit is asserted.

## 7. Classical comparison and scientific scope

Iwaniec--Kristensen, *A construction of quasiconvex functions* (2005),
printed pp.77--80, Theorem 3.1 and Lemma 4.1, were acquired from the
[publisher PDF](https://www.rivmat.unipr.it/fulltext/2005-4s/pdf/03.pdf)
and visually inspected. Their completion theorem assumes a positive
uniform Legendre-Hadamard lower bound proportional to `|B|^(p-2)|R|^2`.
Every polynomial in this report retains an acoustic zero at nonzero I,
so that hypothesis fails. Their elliptic-operator strong-QC lemma and
Taylor/Young method are the classical ancestors of the sufficiency proof.
The new necessity is the explicit second rank-one contact and its
nonzero background derivative; strict completion alone does not classify
this projected boundary.

Bruno--Pasqualotto's August 2026
[primary preprint, Theorem 2](https://arxiv.org/html/2608.06367v1)
states ROC iff QC for quartics invariant under both left and right
rotations. That is a three-dimensional isotropic space, while this theorem
assumes left invariance only and classifies existence after H completion.
The intersection of their isotropic space with this generic stationary
space is exactly `span{H}` (checked algebraically in the verifier).
Thus their stated symmetry theorem does not cover the nontrivial members
of this stratum. Its scientific acceptance is not inferred from the
preprint's availability, and it is not a premise of this proof.

No matching exact generic-angle projected boundary theorem was acquired
in this bounded comparison. That is not a historical-originality claim.

## 8. Costs, artifacts, and unfinished obligations

For rational t and rational coefficients, exact stationary admission,
parameter extraction (6), the inequalities (3), principal minors (22),
M, alpha_*, and the reserve margin all use matrices of order at most four
and polynomials of at most 35 monomials. With fixed dimension, the
numerator/denominator bit sizes are O(N) and total exact bit work is
polynomial in total input bit length N. Precision of t and coefficients is
charged. This does not solve acquisition of the polynomial or contact.
For arbitrary real inputs, the theorem is mathematical, not a numerical
oracle claim.

The script rejects t=0 rather than misapplying the generic criterion.
A finite sufficient alpha is conservative; its magnitude and the loss of
conditioning near the boundary are proof costs, not practical performance.
No least-alpha result, full eight-dimensional projection classification,
formal Lean proof, external correctness certificate, physical device,
novelty claim, or publication is asserted.

Required next checks: independently audit the full analytic argument,
especially the boundary gradient (14), weak-case exhaustion, and the
orthogonal transfer to the requested contact. Exact verification only
checks its recorded algebraic scope. The sharp alpha threshold and a
complete treatment of arbitrary nonconformal invertible backgrounds as
contact normalizations remain outside this theorem.

The executed verifier passed 363 assertions, including the four entries of
the boundary gradient (14), rank-one factorizations, every decision branch,
instantiated boundary witnesses at `alpha=12345/7`, both singular limits,
the necessary blowup (25), and rejection of rounded or nonfinite input. These finite checks certify
the recorded algebra, while Sections 2--5 supply the universal argument.

Companion artifacts: `verify.py` (exact identities and limit checks),
`classify.py` (exact rational admission/completion and boundary witnesses),
`verification.json`, and `RECEIPT.json`.

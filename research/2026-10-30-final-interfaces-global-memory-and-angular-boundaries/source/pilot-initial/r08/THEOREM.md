# Exposed anisotropic rays in the full quartic rank-one-convex cone

Let \(\mathcal R_4\) be the cone of all real homogeneous quartic
polynomials on \(\mathbb R^{2\times2}\) which are rank-one convex.
The summands in this cone are not required to have any invariance.
Write

\[
 T=|A|^2,\quad q=\det A,\quad X=a^2+c^2-b^2-d^2,
\]
\[
 H=1+3\tau^2,\quad B=1-3\tau^2,\qquad
 F_\tau=T^2+4(3-12\tau/H)q^2+4(B/H)qX.
\]

## Result

For every \(0<\tau<1/3\), the ray \(\mathbb R_+F_\tau\) is an
**exposed extreme ray of the full cone \(\mathcal R_4\)**. In particular,
if \(F_\tau=G_1+\cdots+G_N\) and all \(G_i\) are homogeneous quartic
rank-one-convex polynomials, every \(G_i\) is a nonnegative scalar
multiple of \(F_\tau\).

Consequently the two supplied quasiconvex seeds, at \(\tau=1/6\) and
\(\tau=1/30\), are also exposed extreme rays of the cone of all
homogeneous quartic quasiconvex polynomials. Using the supplied local
continuation theorem at its accepted scope, **every member of its
\(2^{-206}\) arc about \(1/30\) is a non-polyconvex exposed extreme
quasiconvex quartic**.

None of the open-branch \(F_\tau\) is an invertible left/right linear
pullback, or a transpose pullback, of a birotationally invariant quartic.
At the non-polyconvex certified parameters this excludes every finite
nonnegative decomposition into polyconvex homogeneous quartics and
linear pullbacks of the published birotational rank-one-convex quartics.

This is a cone-geometry result. It does not prove quasiconvexity on the
uncertified part of the branch, classify arbitrary quartics, prove
rigidity of general gradient Young measures, or establish a uniform
strong-quasiconvexity modulus. Historical priority is not assessed.

## 1. Rank-one convexity and its exact acoustic zeros

For any homogeneous quartic \(G\), polarization gives

\[
 D^2G(A)[R,R]=D^2G(R)[A,A].
\]

Thus \(G\in\mathcal R_4\) if and only if the ordinary matrix
\(D^2G(R)\) is positive semidefinite at every rank-one matrix \(R\).
This special quartic identity is the reason a finite acoustic-zero
calculation can constrain all 35 coefficients of a possible summand.

Left rotational invariance of \(F_\tau\) reduces the rank-one test to
\(R=e_1\otimes(1,t)\), with the missing vertical domain direction
obtained by continuity. Put \(S=1+t^2\), \(J_t=1-t^2\). In the orthonormal
basis \((1,t)/\sqrt S,(-t,1)/\sqrt S\) in each output row, its Hessian
divided by four has the block matrix

\[
 \begin{pmatrix} A_0&B_0\\B_0^T&D_0\end{pmatrix},\qquad
 A_0=\operatorname{diag}(3S,S),
\]
\[
 B_0=(B/H)\begin{pmatrix}0&3J_t\\-J_t&-4t\end{pmatrix},\qquad
 D_0=\operatorname{diag}(S,(2r-1)S),\quad r=4-12\tau/H.
\]

For its Schur complement \(P=D_0-B_0^TA_0^{-1}B_0\), direct calculation
gives

\[
 P_{11}=\frac{4(t^2+3\tau^2)(3t^2\tau^2+1)}{S H^2}>0,
 \qquad
 \det P=\frac{3m(t,\tau)^2}{S^2H^4},
\]
\[
 m(t,\tau)=B^2(1-t^2)^2-(1-4\tau+3\tau^2)H(1+t^2)^2.
\]

Therefore \(F_\tau\) is rank-one convex. For \(0<\tau<1/3\),
\((1-4\tau+3\tau^2)H>0\), while

\[
 B^2-(1-4\tau+3\tau^2)H
 =4\tau(3\tau^2-3\tau+1)>0.
\]

It follows that \(m\) has four distinct real roots. At each such root
the Hessian has a one-dimensional kernel. A polynomial representative,
from the supplied acoustic construction, is

\[
\begin{aligned}
 K_0&=-B[\tau(1-t^2)+Ht^2](1+t^2),\\
 K_1&=Bt[H-\tau(1-t^2)](1+t^2),\\
 K_2&=B^2t(1-t^2)-\tau Ht(1+t^2)^2,\\
 K_3&=B^2t^2(1-t^2)+\tau H(1+t^2)^2.
\end{aligned}
\]

The exact identity \(D^2F_\tau(R)K=0\pmod m\) is verified in the code.
The first component of \(K\) is strictly negative at every real root,
so these are actual nonzero vectors.

For \(u=(x,y)\), define

\[
 R_u=u\otimes(1,t),\qquad
 K_u=(xK_0-yK_2,\ xK_1-yK_3,\ yK_0+xK_2,\ yK_1+xK_3).
\]

Homogeneity and output rotation give the same acoustic-zero identity for
\(R_u,K_u\), without imposing any invariance on a possible summand.

## 2. The summand face has dimension one

Suppose \(F_\tau=G+\widetilde G\), with both summands in \(\mathcal R_4\).
At any of the preceding rank-one \(R_u\), both Hessians are positive
semidefinite. Since their sum kills \(K_u\), each kills it separately:

\[
 D^2G(R_u)K_u=0 \quad\text{at every root of }m.
\]

Let \(G\) have arbitrary real coefficients in the 35 monomials
\(a^ib^jc^kd^{4-i-j-k}\). Each component of this vector equation is
cubic in \((x,y)\). Reduce its coefficients in \(t\) modulo the monic
quartic \(m\), and set all four remainder coefficients to zero. This is
an explicit \(64\times35\) rational-function matrix \(L_\tau\).

The supplied scripts construct this matrix directly by differentiating
the 35 monomials. They verify \(L_\tau F_\tau=0\) identically and certify
\(\operatorname{rank}L_\tau=34\) throughout \(0<\tau<1/3\) by exact
polynomial minors and root exclusion. The literal rational matrices for
the two seeds and their one-dimensional nullspaces are in
`face_1_6.json` and `face_1_30.json`.

The two useful minors are specified in `generic_face_result.json` and
`generic_face_exception_result.json`. After clearing the listed row
denominators, their polynomial determinants have greatest common divisor,
up to a nonzero constant,

\[
 \tau^9(3\tau^2-1)^{52}(3\tau^2+1)^9
 (3\tau^2-3\tau+1)^9(3\tau^2-2\tau+1)^3.
\]

This has no zero in the open interval; nor do the row denominators. Thus
the two exact minors cover the entire interval. The first minor alone
does fail: one degree-ten factor has a single interior zero, approximately
\(0.2012225253\). Merely asserting its generic nonvanishing would have
left a gap. Reversing pivot order retains the same unwanted factor. The
replacement minor, proposed by row pivoting there and then computed
entirely exactly, removes that factor from the common zero set. Its
numerical row proposal is not a sign or nonvanishing premise.

It follows that \(G=cF_\tau\). Since \(F_\tau(E_{11})=1\), a negative
multiple fails rank-one convexity on the line \(sE_{11}\); hence \(c\ge0\).
The same argument applies to every summand, and to quasiconvex summands
because quasiconvexity implies rank-one convexity.

## 3. An explicit exposing functional

Let \(\mathcal U=\{(1,0),(0,1),(1,1),(1,-1)\}\), and let \(t_j\) be the
four roots of \(m\). Define the linear functional

\[
 \ell_\tau(G)=\sum_{j=1}^4\ \sum_{u\in\mathcal U}
 K_u(t_j)^T D^2G(R_u(t_j))K_u(t_j).
\]

Every term is nonnegative on \(\mathcal R_4\), and
\(\ell_\tau(F_\tau)=0\). If \(\ell_\tau(G)=0\), positivity kills every
individual vector. A homogeneous cubic in \((x,y)\) which vanishes at
the four projectively distinct members of \(\mathcal U\) vanishes
identically. Four distinct roots then kill the remainder modulo \(m\).
Therefore \(L_\tau G=0\), proving

\[
 \{G\in\mathcal R_4:\ell_\tau(G)=0\}=\mathbb R_+F_\tau.
\]

This proves exposedness, not just extremality. It also makes the
functional explicitly rational in \(\tau\): write the monic zero
polynomial as \(t^4-Ct^2+1\). The root sum of a reduced scalar
\(p_0+p_1t+p_2t^2+p_3t^3\) is simply \(4p_0+2Cp_2\).
`expose_seeds.py` uses this trace formula and supplies primitive integer
coefficient vectors in `exposing_1_6.json` and `exposing_1_30.json`.
No numerical root evaluations are premises of these functionals.

## 4. Why the ordinary invariant construction does not generate these rays

Consider infinitesimal left/right changes of variables
\(\delta A=UA+AV\), with eight unrestricted real entries in \(U,V\).
The coefficient matrix for \(DF_\tau(A):\delta A=0\) has rank six.
Its exact \(6\times6\) minor is

\[
 16384(3\tau^2-1)^2(3\tau^2+1)^4\ne0
 \qquad(0<\tau<1/3).
\]

Its two-dimensional kernel consists of output rotation and the trivial
representation kernel \((U,V)=(-I,I)\). Thus the effective continuous
left/right stabilizer has dimension one.

A birotationally invariant quartic has independent left and right
rotation generators, in addition to that trivial representation kernel:
its corresponding dimension is at least three. An invertible left/right
pullback conjugates stabilizers and preserves dimension; transposition
interchanges the two sides. The dimensions are incompatible. This rules
out exact equivalence under all such transformations, not just an
orthogonal-coordinate comparison.

Now take a certified non-polyconvex \(F_\tau\). In a nonnegative finite
decomposition into polyconvex quartics and transformed birotational
rank-one-convex quartics, every summand is rank-one convex. Extremality
would make every nonzero summand proportional to \(F_\tau\). A
polyconvex summand is excluded by its non-polyconvexity, and an invariant
pullback is excluded by the stabilizer calculation. Hence such a
decomposition does not exist. This does not rule out unrelated direct
proofs or limits outside the asserted finite-decomposition scope.

## 5. A finite microstructure test for every attempted subtraction

The exposing functional gives more than a dimension count. Let
\(G\in\mathcal R_4\) be nonzero and not proportional to \(F_\tau\).
Then \(\ell_\tau(G)>0\), so at least one of its 16 explicit acoustic
evaluations satisfies

\[
 c=D^2G(R)[K,K]>0,\qquad D^2F_\tau(R)[K,K]=0.
\]

For every \(\varepsilon>0\), put \(W=F_\tau-\varepsilon G\).
Polarization gives

\[
 D^2W(K)[R,R]=-\varepsilon c<0.
\]

Thus no positive amount of any different rank-one-convex homogeneous
quartic can be removed while retaining rank-one convexity, hence neither
quasiconvexity. This supplies a precise obstruction to the natural attack
of extracting an ordinary convex/polyconvex piece from the certified ray.

It also gives an actual discriminating gradient field. Write
\(R=u\otimes v\), use a periodic cell with \(v\cdot x\) as its first
periodic coordinate, and take

\[
 \phi(x)=\delta u\sin(v\cdot x),\qquad
 D\phi=\delta R\cos(v\cdot x).
\]

Its exact mean energy gap at the base \(K\) is

\[
 \fint W(K+D\phi)-W(K)
 =-\frac{\varepsilon c\delta^2}{4}
    +\frac{3W(R)\delta^4}{8}.
\]

If \(W(R)>0\), choose
\(0<\delta^2<2\varepsilon c/[3W(R)]\); if \(W(R)\le0\), any
\(\delta>0\) works. The gap is strictly negative. This is a periodic
quasiconvexity violation for the *subtracted* energy; the usual cutoff in
many tiled cells gives compactly supported tests. It is not a violation
for the accepted seed. The 16-pair search and the amplitude choice are
finite and use exactly the same acoustic information as the proof.

This does not exclude strong quasiconvexity estimates formulated with an
increment such as \(|D\phi|^4\); subtracting a quartic of the full matrix
argument is a different assertion.

`corrugation.py` executes this test for the seed at \(\tau=1/30\),
\(G=T^2\), and \(\varepsilon=1/100\). It normalizes \(K_0=1\) and
verifies the line coefficients exactly modulo
\(t^4-(83981/2710)t^2+1\). Its positive acoustic cost is

\[
 c_G=\frac{43216979806}{6203295121}t^2
      +\frac{2049200640851}{31016475605}>0.
\]

At the smaller positive root, the displayed numerical illustration has
\(t\approx0.1797300083\), \(\delta^2\approx0.2094585676\), and mean
energy gap \(\approx-0.01735709319\). The negative sign for all four real
roots follows from the exact formula, not those decimals. The literal
algebraic fixture is `corrugation_data.json`.

## Governing inputs and remaining obligation

The quasiconvexity, origin regularity, orientation transport, unrestricted
non-polyconvexity at \(1/30\), and explicit local arc are inherited from
the supplied
[PROOF.txt](producer-workspace/PROOF.txt),
[ARC_PROOF.txt](producer-workspace/ARC_PROOF.txt),
and literal case certificates.
This tranche adds the full 35-coefficient face calculation, its exposing
functional, and the transformation/decomposition obstruction. It does
not replace the acquired closed primitive with a pointwise selection
oracle.

The ordinary competitor is the birotational classification in Bruno and
Pasqualotto, *Quasiconvexity for the Dacorogna–Marcellini Energy*,
[Theorem 2 and Appendix A](https://arxiv.org/html/2608.06367v1), together
with invertible input/output changes, nonnegative sums, and polyconvex
additions. That primary source was read for the scope of its invariance
assumption. The exact obstruction above is a new derivation here, not a
claim of historical priority.

The consequential unresolved obligation is still to certify
quasiconvexity or find an actual gradient-field violation on the rest of
the extreme curved branch. Interpolation of other homogeneous quartic
rank-one-convex generators cannot provide its individual members.

## Exact replay

From this research directory, run:

```sh
python3 verify_findings.py --full-minors
python3 corrugation.py
```

The verifier uses Python and SymPy and reconstructs the Hessian, all
acoustic constraints, both full polynomial determinants, their common
zero exclusion, the seed exposing functionals, and the stabilizer.
The optional NumPy calculation in `generic_face.py --pivot-exception`
only regenerates a proposal for the replacement row indices; it is not
used in the exact replay. This is an internally checked finite algebraic
proof, with the quasiconvexity inputs retained at their supplied scope.

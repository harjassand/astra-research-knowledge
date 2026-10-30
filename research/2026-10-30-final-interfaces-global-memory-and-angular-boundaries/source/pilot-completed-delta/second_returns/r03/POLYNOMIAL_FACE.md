# A complete exposed face of nonhomogeneous quartic energies

The permitted partner result exposes the angular seed ray among all 35
homogeneous quartic coefficients. The earlier rigidity result makes each
certified seed strictly quasiconvex. Their interface admits a further
classification: **all globally rank-one-convex lower-degree extensions of
that exposed ray can be determined exactly**.

Let \(\mathcal P_{\leq4}\) be the 70-dimensional real vector space of
polynomials of degree at most four in \(A=(a,b,c,d)\). Let
\(\mathcal R_{\leq4}\) and \(\mathcal Q_{\leq4}\) be its rank-one-convex
and quasiconvex cones, with both properties on all real matrices. Affine
polynomials and scalar multiples of the determinant are lineality.
Write \(p_j\) for a homogeneous
degree-\(j\) part. Retain

\[
 F_\tau=T^2+4(3-12\tau/H)q^2+4(B/H)qX,\quad
 H=1+3\tau^2,\quad B=1-3\tau^2,
 \qquad 0<\tau<1/3.
\]

Here \(T=|A|^2\), \(q=\det A\), and
\(X=a^2+c^2-b^2-d^2\). Let \(\ell_\tau\) be the partner's actual
16-acoustic-evaluation functional exposing \(\mathbb R_+F_\tau\) in the
full homogeneous quartic rank-one-convex cone. Set

\[
 \Lambda_\tau(p)=\ell_\tau(p_4),\qquad
 \mathscr F_\tau=
 \{p\in\mathcal R_{\leq4}:\Lambda_\tau(p)=0\}.                 \tag{1}
\]

## Result

**Theorem.** For every \(0<\tau<1/3\), \(\mathscr F_\tau\) is an exposed
face of \(\mathcal R_{\leq4}\), has dimension 20, and consists exactly of

\[
 p(A)=cF_\tau(A+V)+Q(A)+L(A)+d,\qquad c>0,                     \tag{2}
\]

where \(V\in\mathbb R^{2\times2}\), \(Q\) is a homogeneous rank-one-convex
quadratic, \(L\) is linear, and \(d\) is constant, together with
\(p=Q+L+d\) when \(p_4=0\). For \(c>0\) all the parameters in (2) are
unique. No symmetry is imposed on \(p\), its cubic part, or \(Q\).

Whenever \(F_\tau\) is quasiconvex, the face is common to the two cones:

\[
 \mathscr F_\tau
 =\{p\in\mathcal Q_{\leq4}:\Lambda_\tau(p)=0\}.                 \tag{3}
\]

At both supplied seeds, \(\tau=1/6,1/30\), and on precisely the already
certified \(|\tau-1/30|<2^{-206}\) arc, every member of (2) is **strictly
quasiconvex** for nontrivial \(W^{1,4}_0\) affine-boundary perturbations.
At \(1/30\) and throughout that inherited arc, every member with \(c>0\)
is also **not polyconvex**, regardless of the finite quadratic addition.
No polyconvexity conclusion is added at \(1/6\).

For an uncertified branch parameter, the normal form (2) classifies
rank-one convexity. It does not infer quasiconvexity of \(F_\tau\).

## 1. The exposed homogeneous face supplies the leading part

If \(p\in\mathcal R_{\leq4}\), then

\[
 D^2p_4(A)[R,R]
   =\lim_{s\to\infty}s^{-2}D^2p(sA)[R,R]\geq0
 \qquad(\operatorname{rank}R=1).
\]

Consequently \(p_4\) is rank-one convex and
\(\Lambda_\tau(p)\geq0\). The partner's full 35-coefficient exposed-face
theorem implies that equality forces

\[
 p_4=cF_\tau,\qquad c\geq0.                                  \tag{4}
\]

This establishes that (1) is an exposed face, rather than a symmetry
restricted slice. The functional is a positive sum of actual Hessian
evaluations at real acoustic pairs. Its seed integer coefficient vectors
are explicit in the permitted snapshot. Both of the partner's generic
34-by-34 determinant identities, their common-zero exclusion, seed
exposers and stabilizer were replayed locally with its unchanged
`verify_findings.py --full-minors`; no producer or external service was
consulted.

The partner's exposing calculation also defeats the ordinary attempt to
deduce a modulus by subtracting a different homogeneous convex quartic:
\(\ell_\tau(G)>0\) for every rank-one-convex \(G\) not proportional to
\(F_\tau\), hence \(F_\tau-\epsilon G\) is not rank-one convex for any
\(\epsilon>0\). This does not settle the earlier increment bound involving
\(|D\varphi|^4\). The successful change of mechanism here is to classify
lower-degree additions rather than assume an extractable quartic margin.

## 2. A new exact cubic rigidity calculation

Take the same acoustic data as in the governing construction and the
permitted exposed-face proof. Write

\[
 m(t,\tau)=B^2(1-t^2)^2-(1-4\tau+3\tau^2)H(1+t^2)^2.
\]

It has four distinct real roots for \(0<\tau<1/3\). Put
\(R_u=u\otimes(1,t)\), and use

\[
\begin{split}
 K_0&=-B[\tau(1-t^2)+Ht^2](1+t^2),\\
 K_1&=Bt[H-\tau(1-t^2)](1+t^2),\\
 K_2&=B^2t(1-t^2)-\tau Ht(1+t^2)^2,\\
 K_3&=B^2t^2(1-t^2)+\tau H(1+t^2)^2,
\end{split}
\]

with
\(K_u=(xK_0-yK_2,xK_1-yK_3,yK_0+xK_2,yK_1+xK_3)\) for
\(u=(x,y)\). These are real nonzero acoustic pairs:

\[
 D^2F_\tau(R_u)K_u=0\pmod m.
\]

Suppose (4) holds with \(c>0\), and write \(C=p_3\), \(Q_2=p_2\).
Quartic polarization and cubic polarization give, at each real root,

\[
 D^2p(sK_u)[R_u,R_u]
       =2s\,\nabla C(R_u)\cdot K_u+2Q_2(R_u).                  \tag{5}
\]

Global rank-one convexity demands nonnegativity for **both signs and all
magnitudes of \(s\)**. Therefore

\[
 \nabla C(R_u)\cdot K_u=0.                                   \tag{6}
\]

This operation is not a choice of a correction or a relaxation oracle.
It is an unavoidable linear constraint on the acquired polynomial's
cubic coefficients. A finite quadratic stiffness cannot offset a
nonzero linear drift in (5) on all real matrices.

Write \(C\) in all 20 cubic monomials. Reduce (6) modulo the monic
quartic \(m\), and equate the four \(t\)-coefficients for each of the
four homogeneous \((x,y)\)-cubic coefficients. This is a new
\(16\times20\) rational-function matrix \(L^{(3)}_\tau\). Equivalently,
one may use the four output vectors \((1,0),(0,1),(1,1),(1,-1)\) and the
four real roots: these are the same 16 acoustic pairs as the exposer.

The exact script constructs this matrix directly from all cubic
monomials. Its first 16 columns have a nonzero determinant after the
listed positive/nonzero row denominator clearings. The determinant is

\[
\begin{split}
 62208\,&\tau^{10}(3\tau^2-1)^{32}(3\tau^2+1)^8
 (3\tau^2-3\tau+1)^{10}(3\tau^2-2\tau+1)^4\\
 &\quad\times
 (9\tau^4-18\tau^3+18\tau^2-6\tau+1)^4.                       \tag{7}
\end{split}
\]

There is no unhandled exceptional parameter. For the only higher-degree
factor,

\[
 9\tau^4-18\tau^3+18\tau^2-6\tau+1
 =(3\tau^2-3\tau+1)^2+3\tau^2>0.
\]

The other factors and all row denominators are nonzero on the whole
open interval. The data lists every denominator and the exact minor.
Thus \(\operatorname{rank}L^{(3)}_\tau=16\) everywhere on that interval.

The four cubics \(\partial_aF_\tau,\ldots,\partial_dF_\tau\) lie in its
kernel since

\[
 \nabla(DF_\tau:V)(R_u)\cdot K_u
    =V\cdot D^2F_\tau(R_u)K_u=0.
\]

They are independent. The coefficient minor using the cubic monomials
\(a^2d,a^2c,a^2b,a^3\) has determinant

\[
 \frac{12288\tau^2(3\tau^2-3\tau+1)^2}{(1+3\tau^2)^4}\ne0.       \tag{8}
\]

The four-dimensional kernel is consequently **exactly** the translation
space. It follows that

\[
 C(A)=c\,DF_\tau(A):V                                        \tag{9}
\]

for a unique \(V\). No other cubic can be repaired by any quadratic or
affine additions while retaining global rank-one convexity.

## 3. Completion by translation leaves precisely a quadratic problem

Subtract \(cF_\tau(A+V)\) from \(p\). Equations (4) and (9) cancel its
quartic and cubic terms, leaving a uniquely determined
\(Q(A)+L(A)+d\). At the base \(A=-V\),

\[
 D^2p(-V)[R,R]=2Q(R)
\]

because the Hessian of a homogeneous quartic vanishes at zero. Thus
\(Q(R)\geq0\) for every rank-one \(R\). Conversely, a translated
rank-one-convex \(F_\tau\), a rank-one-convex quadratic, and affine terms
have a rank-one-convex sum. This proves (2) for \(c>0\).

If \(p_4=0\), nonnegativity of \(D^2p(sA)[R,R]\) for all real \(s\)
forces \(D^2p_3(A)[R,R]=0\). The coordinate rank-one directions imply
\(\partial_{aa}p_3=\partial_{bb}p_3=\partial_{cc}p_3=
\partial_{dd}p_3=0\), leaving only the multi-affine cubics
\(abc,abd,acd,bcd\). The rank-one directions \((1,1,0,0)\) and
\((0,0,1,1)\) kill their mixed derivatives and hence all four coefficients.
Therefore \(p_3=0\), and precisely the quadratic case remains.

The face's linear span has dimension \(1+4+10+5=20\): the quartic ray,
four translation cubics, ten quadratic coefficients and five affine
coefficients. Taking \(c>0\) and a strictly rank-one-positive quadratic
remainder gives relative interior in this span, so this is its actual
dimension, not only an upper bound.

## 4. Quasiconvexity and equality on the entire face

For homogeneous quadratics, rank-one convexity and quasiconvexity
coincide by the ordinary Fourier argument. On a torus, the gradient
coefficient at frequency \(k\ne0\) is
\(i\widehat\varphi(k)\otimes k\); its real and imaginary parts are rank
one. The quadratic energy is the sum of the corresponding nonnegative
acoustic quadratic forms. Also,

\[
 \int[Q(M+D\varphi)-Q(M)]=\int Q(D\varphi)\geq0.                \tag{10}
\]

Periodizing a zero extension proves the same assertion for Dirichlet
tests. This familiar quadratic theorem is the strongest ordinary
competitor after the forced translation; no new certificate acquisition
is being hidden in the residual problem.

If \(F_\tau\) is quasiconvex, (2) and (10) prove that every member of the
rank-one-convex face is quasiconvex. The reverse containment in (3)
follows from quasiconvexity implying rank-one convexity.

At each of the already certified parameters, the earlier finite-plane
heat-rigidity theorem gives strict quasiconvexity of \(F_\tau\) for all
nontrivial \(W^{1,4}_0\) tests. The exact energy identity for (2) is

\[
\begin{split}
 \int[p(M+D\varphi)-p(M)]
  ={}&c\int[F_\tau(M+V+D\varphi)-F_\tau(M+V)]\\
     &+\int Q(D\varphi)>0.                                  \tag{11}
\end{split}
\]

Thus the **whole positive-quartic part of this 20-dimensional exposed
face** has a unique affine minimizer for every affine Dirichlet boundary
condition. The assertion remains valid if the quadratic is indefinite
as an ordinary form; its precise rank-one condition, not ordinary
positive definiteness, is the requirement.

The residual condition is an ordinary exact quadratic test, rather than
an assumed quasiconvexity oracle. For rational coefficients, form the
\(2\times2\) acoustic matrix of \(Q(v\otimes(1,t))\) in \(v\). Its entries
have degree at most two in \(t\). Check its diagonal quadratics and
determinant quartic for nonnegativity on the real line, together with the
vertical direction. Univariate exact real-root isolation supplies a
finite decision procedure. The fixtures use explicit factorizations so
that no root-isolation result is inferred from numerical samples.

There is also a sharp conditional statement on the uncertified branch.
If a member with \(c>0\) is quasiconvex, then
\(s^{-4}p(sA)\to cF_\tau(A)\) as \(s\to\infty\). Taking this limit in
each fixed bounded-gradient quasiconvexity test proves that \(F_\tau\)
is quasiconvex. Therefore on every branch parameter either:

- \(F_\tau\) is quasiconvex and the entire 20-dimensional face is common
  to the two cones; or
- \(F_\tau\) fails quasiconvexity and the quasiconvex intersection of this
  rank-one-convex face consists only of its 15-dimensional quadratic and
  affine part.

This is a proved dichotomy. It does not choose its outcome at any
uncertified parameter.

## 5. Finite lower-degree terms cannot restore polyconvexity

At \(\tau=1/30\), retain the governing unrestricted minor-support cuts
at \(A_0=\operatorname{diag}(36,35)\),
\(R_+=\left(\begin{smallmatrix}0&55\\-4&0\end{smallmatrix}\right)\),
and \(R_-=\operatorname{diag}(1,-2)\). Their exact incompatible bounds are

\[
 U=\frac{917884501}{33110},\qquad
 L=\frac{227527416931}{8195929},\qquad
 g=L-U=\frac{34938784681}{901552190}>0.                        \tag{12}
\]

For a general quartic polynomial \(p\), a minor support at a base requires
\(a-b^2/(4e)-\lambda\det R\geq0\), where \(a,b,e\) are its second,
third and fourth line coefficients in \(p(A+sR)\), and \(e>0\). This
is just minimization over real \(s\) after dividing the support remainder
by \(s^2\); it is not restricted to homogeneous quartics.

For (2), evaluate the two cuts at the actual base
\(A=\rho A_0-V\). The resulting upper and lower bounds on the scalar
minor support are

\[
 c\rho^2U+\frac{Q(R_+)}{\det R_+},\qquad
 c\rho^2L+\frac{Q(R_-)}{\det R_-},
\]

respectively. Their lower-minus-upper gap is

\[
 c\rho^2g+
 \frac{Q(R_-)}{\det R_-}-\frac{Q(R_+)}{\det R_+}.              \tag{13}
\]

It is strictly positive for all sufficiently large finite \(\rho\).
Thus no quadratic or affine addition repairs polyconvexity for any
member with \(c>0\). The same proof works on the inherited arc, whose
same two cuts retain a strictly positive gap. The required base may
grow with the quadratic coefficients; this is explicitly an all-real-
matrix theorem, without a bounded-strain claim.

## 6. A substantive failed repair and an exact gradient-field witness

The natural alternative to the constrained cubic classification is to
allow an arbitrary cubic and stabilize it with a very large ordinary
quadratic. This fails globally, even for a single monomial:

\[
 p_\nu(A)=F_{1/30}(A)+a^3+\nu|A|^2,\qquad \nu\geq0.           \tag{14}
\]

Use the smaller positive root of
\(2710t^4-83981t^2+2710=0\), let
\(R=e_1\otimes(1,t)\), and normalize the actual acoustic vector to
\(\widehat K_0=1\). The executable fixture gives every component of
\(\widehat K\) as a polynomial modulo the monic acoustic quartic. Then
\(\nabla(a^3)(R)\cdot\widehat K=3\), so take the base

\[
 A=s\widehat K,\qquad s=-\frac{\nu(1+t^2)+1}{3}.              \tag{15}
\]

Exact division verifies that the quadratic line coefficient of
\(p_\nu(A+zR)\) is \(-1\), while its fourth coefficient is
\((1+t^2)^2\). On a periodic parallelogram with reciprocal direction
\(\xi=(1,t)\), take
\(\varphi(x)=\delta e_1\sin(\xi\cdot x)\), with
\(\delta^2=(1+t^2)^{-2}\). Odd terms average to zero, giving exactly

\[
 \fint[p_\nu(A+D\varphi)-p_\nu(A)]
       =-\frac{1}{8(1+t^2)^2}<0.                            \tag{16}
\]

This is a genuine gradient-field violation for **every finite quadratic
stiffness** \(\nu\), not just a certificate-family obstruction. Its base
gradient grows linearly with \(\nu\); the argument does not assume a
uniform bounded operating range. Standard cutoff in many cells gives
compactly supported violations.

More generally, if a cubic fails (6), one of the same 16 acoustic scores
\(\eta=\nabla C(R)\cdot K\) is nonzero. For arbitrary quadratic part
\(Q_2\), the finite base
\(sK\) with \(s=-(Q_2(R)+1)/\eta\) makes the second line coefficient
\(-1\). If the leading quartic is \(cF_\tau\), choose
\(\delta^2=1/(cF_\tau(R))\). The sinusoidal mean gap is then
\(-1/(8cF_\tau(R))<0\). Thus the linear classification has a finite,
equally informed discriminating test whenever its cubic condition fails.

## 7. An admissible nonhomogeneous, non-polyconvex fixture

The other executable fixture uses

\[
\begin{split}
 p(A)&=2F_{1/30}(A+V)+Q(A)+a+2b-3c+4d+5,\\
 V&=(1/2,-1/3,2/5,-3/7),\qquad Q=T-3q.
\end{split}
\]

The normal-form extraction recovers \(V\) and \(Q\) exactly from the
polynomial coefficients. \(Q\) is indefinite as a form on all matrices:
the eigenvalues of its coefficient matrix are \(-1/2,5/2\), each twice.
On rank-one matrices it is precisely \(|v|^2|\xi|^2\), hence is an
ordinary quasiconvex quadratic. For zero-boundary tests its determinant
part integrates to zero, and the exact gap is

\[
 2\operatorname{gap}_{F_{1/30}}(M+V,\varphi)
            +\int|D\varphi|^2.
\]

The source's two unrestricted minor-support cuts already contradict
polyconvexity at \(A_0-V\), with exact gap
\(2005882867/32783716>0\); no asymptotic base is needed in this fixture.
The ordinary quadratic addition alone explains its extra quadratic
coercivity. The new conclusion is that the normal form exhausts all
globally admissible lower-degree extensions of this exposed quartic ray.

## 8. A general exposedness-lifting principle for quartics

There is a general theorem behind the individual-generator consequence;
its shortest proof needs no acoustic calculation. Let

\[
 \mathcal N=\{L(A)+d+\lambda\det A\}
\]

be the six-dimensional null-Lagrangian space. This is precisely the
lineality of \(\mathcal R_{\leq4}\) (and of the quasiconvex cone).
Indeed, if both \(p\) and \(-p\) are rank-one convex, its second derivative
vanishes along every rank-one direction. The four coordinate directions
make it multi-affine; the four row/column pair directions kill all terms
except affine terms, \(ad\), and \(bc\). The all-ones rank-one direction
forces their coefficients to be opposite. The executable rank test uses
these nine actual rank-one directions, producing a \(135\times70\)
matrix of rank 64 with kernel exactly \(1,a,b,c,d,q\).

**General lifting theorem.** Let \(F\) generate an exposed ray of either
the homogeneous quartic rank-one-convex cone or the homogeneous quartic
quasiconvex cone, with exposing functional \(\ell\). In the corresponding
cone of all polynomials of degree at most four, for every fixed \(V\),

\[
 J_V(p)=\ell(p_4)+\Delta_Ap(-V)
\]

exposes exactly \(\mathbb R_+F(\,\cdot+V)+\mathcal N\). Hence translation
lifts the homogeneous exposed ray to an exposed extreme ray in the full
polynomial cone modulo null Lagrangians.

**Proof.** In either cone the leading part \(p_4\) belongs to the
corresponding homogeneous cone, by scaling. The matrix-space Laplacian
is a sum of four second derivatives along rank-one coordinate directions,
so is nonnegative. Both summands of \(J_V\) are therefore nonnegative.
Translate to \(V=0\). If \(J_0(p)=0\), exposedness gives \(p_4=cF\).
At the base zero, rank-one convexity makes \(p_2\) rank-one convex and
\(\Delta p_2=0\). The zero-trace quadratic argument below gives
\(p_2=\lambda q\). Then for every \(A\) and rank-one \(R\),

\[
 D^2p(sA)[R,R]
   =cs^2D^2F(A)[R,R]+sD^2p_3(A)[R,R]\geq0
       \quad\text{for all real }s.
\]

The coefficient of \(s\) must vanish; a cubic rank-one-affine polynomial
in this \(2\times2\) space is zero, as proved in Section 3. Thus
\(p=cF+N\). Conversely these polynomials all annul the functional and
belong to the relevant cone. Translation preserves the null-Lagrangian
space and the leading part, proving the claim for every \(V\).
\(\square\)

The same argument also lifts an extreme ray without an exposer: in a
decomposition of \(F\), homogeneous extremality first forces each leading
part to be a nonnegative multiple of \(F\); nonnegative Hessian traces at
zero sum to zero, forcing every quadratic part to be a null Lagrangian
and every cubic part to vanish. Conversely any homogeneous decomposition
or exposing-functional restriction is inherited from the full polynomial
quotient. Thus extremality, and separately exposed extremality, are
equivalent in the homogeneous quartic cone and for any translated
generator in the degree-at-most-four quotient cone. This statement holds
for each of the ROC and QC cones separately.

This is stronger and simpler for the individual translated ray than
assuming the family-specific 16-by-20 calculation. That calculation is
needed to classify the *whole* 20-dimensional leading-part face, where
the quadratic trace need not vanish. The lifting theorem applies to any
exposed homogeneous quartic ray in either of the two planar cones.

For a prescribed matrix translation \(V\), define the explicit linear
functional on the full polynomial space

\[
 J_{\tau,V}(p)=\ell_\tau(p_4)+\Delta_Ap(-V).                  \tag{17}
\]

Both terms are nonnegative on \(\mathcal R_{\leq4}\): the first by the
leading-part argument, and the second because each coordinate matrix
direction is rank one. No energy or test-field averaging is hidden in
this matrix-space Laplacian evaluation.

An exact polynomial identity is

\[
 \Delta_AF_\tau(A)=8(r(\tau)+2)|A|^2,\qquad
 r(\tau)=4-12\tau/(1+3\tau^2)>1.                            \tag{18}
\]

In particular the anisotropic term \(qX\) is harmonic in matrix space.
Within the classified angular face, if \(J_{\tau,V}(p)=0\), the first
term gives the normal form with some
translation \(W\). The second becomes

\[
 8c(r+2)|W-V|^2+\Delta_AQ=0.                               \tag{19}
\]

Every summand is nonnegative. For \(c>0\), (19) forces \(W=V\) and
\(\Delta Q=0\). For a rank-one-convex quadratic, zero trace forces
\(Q=\lambda q\): all four coordinate values are nonnegative and sum
to zero, so vanish; nonnegativity on each row/column rank-one plane
kills its four corresponding mixed coefficients; nonnegativity on
general rank-one matrices makes its remaining \(ad,bc\) coefficients
opposite. The \(c=0\) case gives precisely the same null space.
Conversely all \(cF_\tau(A+V)+N(A)\), \(c\geq0\), \(N\in\mathcal N\),
annihilate (17). Thus

\[
 \{p\in\mathcal R_{\leq4}:J_{\tau,V}(p)=0\}
       =\mathbb R_+F_\tau(\,\cdot+V)+\mathcal N.              \tag{20}
\]

This is a seven-dimensional exposed face in the full 70-coefficient
space, or an **exposed extreme ray in the 64-dimensional quotient by
null Lagrangians**. At each certified parameter it is the same exposed
ray in the quasiconvex quotient cone. Its positive members are strictly
quasiconvex by the earlier rigidity theorem; at \(1/30\) and on the
inherited arc they are non-polyconvex by the preceding support cuts.

In particular a decomposition of a translated seed into arbitrary
rank-one-convex polynomials of degree at most four cannot create a
different summand after quotienting by null Lagrangians. This extends
the partner's obstruction beyond homogeneous summands: applying (17) to
each summand forces it to be a nonnegative multiple of the same
translated quartic plus a null Lagrangian. It does not exclude unrelated
non-polynomial or higher-degree constructions.

## 9. Scope and artifacts

This classifies a complete common exposed face in the 70-coefficient
polynomial problem at the certified parameters. It does not classify
quartic leading parts outside the partner's exposed ray. The full curved
branch still requires an actual heat certificate or a gradient-field
counterexample for its uncertified \(F_\tau\). The first tranche's uniform
\(L^4\) increment modulus and equality gradient-Young-measure questions
at the pure seed also remain open. Exposedness does not convert strict
quasiconvexity into that modulus, and adding an ordinary quadratic does
not settle it for the original homogeneous seed. Historical priority is
not assessed.

New files are confined to `runs/r03/phase2`; first-return artifacts and
the permitted partner snapshot were left unchanged. This tranche used
only local files and local exact computation.

Run, in this directory:

```sh
python3 cubic_rigidity.py
python3 verify_polynomial_face.py
```

The first reconstructs the generic \(16\times20\) matrix, its full
polynomial minor, denominator exclusions, the translation minor, and
both seed ranks; it writes `cubic_rigidity_data.json`. The second checks
the interface with the actual seed exposer/face, the recovered normal
form, the indefinite quadratic, the unrestricted non-polyconvex cuts,
and the exact negative sinusoidal gap for the failed cubic repair; it
writes `polynomial_face_results.json`. These scripts require SymPy.

Governing sources read locally were the case `PROOF.txt`,
`ARC_PROOF.txt` and exact acoustic/seed data; the retained
`runs/r03/RIGIDITY.md`; and only the specifically permitted partner
snapshot `first_returns/r08/THEOREM.md`, its face/exposer/stabilizer
scripts, exact JSONs, and full replay verifier. Its full determinant
replay succeeded. No quasiconvexity beyond the supplied seeds/arc was
obtained by parameter sampling or inferred from the exposedness proof.

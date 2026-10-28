# Independent acceptance of a strict-ROC common-class separator

Root independently accepts the exact finite-class separation described below.
The evidence is both the exact replay in `independent_common.py` and the
analytic argument here. The checker uses SymPy's QQ polynomial engine; it
imports none of the acquisition model, author verifier, interface arrays or
numerical nullspaces. `INDEPENDENT_COMMON_REPLAY.json` records its 2.51-second
completed replay. No true non-polyconvexity or non-quasiconvexity follows.

Let A=[[a,b],[c,d]], u=a²+c², v=b²+d², w=ab+cd and q=ad−bc.
Use the basis (u²,v²,uv,w²,uw,vw,qu,qv,qw). The exact target is

    p=(55220381/10^10, 55220381/10^10, 114430029/625000000,
       −801761987/5000000000, 0, 0,
       297124543/10^10, −148562271/5000000000, 0).

The common certificate SHA256 is
`2e812506ed588ec86ea9736a831df69f5eecd8c5d282f226e73e31656360e7b9`;
the strict-ROC certificate SHA256 is
`9ab66589e89d79379216348ab26de1faba54dd4af96b3f9d62f8564cce7f9413`.

## The classes and the separation argument

Class P1 consists of homogeneous quartics G for which some homogeneous
quadratic k(A) makes

    |X|² [G(A+X)−G(A)−DG(A):X−k(A)detX]

an SOS. Its squares use the complete 60-feature vector consisting of all
A_i X_j X_k (j≤k) and all X_i X_j X_k (i≤j≤k). Vanishing at X=0 and
homogeneity give this feature space without imposing rotational symmetry.
It is a sufficient polyconvexity class. It is not all polyconvex quartics.

For a second quartic H put B1=(y0,y1,y3,y4), B2=(y1,y2,y4,y5), the two
derivatives of the planar gradient A, and

    D_H(A,y)=D²H(A)[B1,B1]+D²H(A)[B2,B2].

Class H consists of those H for which D_H, up to the pullback of a closed
quadratic two-form on R4, is an SOS in the complete 24-feature vector
(A_i y_j). The integral of that pullback vanishes: closed polynomial forms
on R4 are exact, pullback commutes with the exterior derivative, and the
integral of an exact form on the periodic domain is zero. This is the
named componentwise-heat sufficient certificate class. General flows,
nonquadratic forms and non-SOS nonnegative dissipation are outside it.

The PC functional is defined on all 658 monomials in products of its
60 features. Its moment matrix is strictly positive definite, with all
60 LDL pivots reconstructed and positive over QQ. It annihilates all ten
|X|² A_i A_j detX selector directions. Thus its value on the weighted
Bregman divergence of any G in P1 is nonnegative.

The heat functional is defined on all 210 A²y² monomials. Its 24-by-24
moment matrix likewise has 24 independently reconstructed positive pivots.
The verifier constructs ALL 60 quadratic two-forms and their exterior
derivatives directly. The derivative map has rank 15, hence closed-space
dimension 45. For every basis form omega, the functional on its pullback
equals eta applied to d(omega), where eta is the certificate's exact
16-component vector. Consequently it annihilates every closed form,
without trusting a numerically acquired nullspace basis. Its value on
D_H is nonnegative whenever H belongs to the heat class.

The two induced functionals on the nine-dimensional energy space agree
exactly. Call that shared functional g. For the target,

    g(F)=−28689295580537827/3025000000000000000000 < 0.

If F=G+H with G in P1 and H in the heat class, linearity would give
g(F)=g(G)+g(H)≥0, a contradiction. Also
g(q²)=11272198019/605000000000>0; allowing an additional nonnegative q²
term does not repair the contradiction (and that term is already in P1).

The component quartics need not initially be invariant. Average each
certificate over the compact left-output SO(2) action. The target is
invariant, norm and determinant of X are invariant, each complete feature
space is a finite representation, and averaged Gram matrices remain PSD.
For the heat class, the identity diffusion commutes with this averaging;
closedness is preserved by pullback. Therefore an arbitrary decomposition
would yield one into invariant quartics, where g applies. The invariant
quartics are spanned by the displayed nine polynomials: quadratic
expressions in u,v,w,q with the sole relation uv=w²+q². The common
separator therefore excludes such arbitrary-component decompositions,
not only decompositions that were assumed invariant in advance.

This argument DOES NOT average a simultaneously unknown energy and an
unknown diffusion tensor. That dependence is bilinear. An extension to
more general flows needs its own argument or certificate.

## Global strict rank-one convexity

The checker differentiates the literal quartic, forms its acoustic
8-by-8 matrix for rank-one directions e1 tensor (s,t), adds the supplied
skew block, and checks equality of all polynomial coefficients. The
skew block contributes zero to that rank-one test. All eight pivots of
Q−I/200000 are exactly positive, so

    D²F(A)[e1 tensor (s,t),e1 tensor (s,t)]
        ≥ |A|² (s²+t²)/200000.

Left-output SO(2) invariance transports an arbitrary output vector to e1,
with its norm retained. Thus the inequality holds for every rank-one
direction xi tensor eta, with right-hand side
|A|² |xi|² |eta|²/200000. Integrating along each affine rank-one line
establishes global rank-one convexity; the degeneracy at A=0 is harmless.

The sum of entrywise l1 norms of the nine acoustic coefficient matrices is
132. The exact shared dual normal has l1 norm 1837667307831/605000000000.
Consequently the entire coefficient sup-norm box of radius 1/52800000
remains strictly ROC and outside the same sum of certificate classes.
The bound follows from perturbing the acoustic matrix by operator norm
at most 132 times the radius and the pairing by the normal's l1 norm
times the radius. It concerns the full nine-dimensional invariant family;
no 35-dimensional openness claim is made here.

## An exact symmetric target for the next attack

Set L=−M=118849817/4000000000, leaving the other seven coefficients
unchanged. Each coefficient changes by at most 1/20000000000, inside the
proved box. Root additionally reconstructed its exact acoustic matrix
and eight positive LDL pivots after subtracting I/400000. Its common
pairing is

    −57378591155518971/6050000000000000000000 < 0.

`EXACT_SYMMETRIC_TARGET.json` contains those exact data. Symbolic
substitution confirms invariance under column swap and under simultaneous
reflection of the second output row and second input column. Those
symmetries make wider flow and true-PC questions better posed; they do
not answer either question.

The author's single pure norm-level2 acquisition had a negative numerical
margin. That is retained only as a failed positive acquisition. Root has
not accepted an exact level2 exclusion, a universal support obstruction,
a true non-PC witness, or a compatible-gradient Jensen violation.

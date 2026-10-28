# Independent substantive review: even-Hopf strict ROC / non-PC separation

**Disposition: ACCEPTED at the exact mathematical scope below.**

The literal energy

    F=(u+v)^2+(252/25)q^2+(99/25)q(u-v)

is strictly rank-one convex on all real 2x2 matrices and is genuinely not
polyconvex. Both statements persist in the stated full six-dimensional
symmetric-K entry box of radius 1/1000000. The aligned-family ROC
classification in Section 5 is also accepted, including its endpoint
degeneracies. Quasiconvexity remains UNKNOWN.

I whole-read the producer's `hopf/PROOF.md`, `verify_opposite_cuts.py`,
`EXACT_SEPARATION_REPLAY.json`, and the numerical acquisition scripts.
The companion `verify_independently.py` imports no producer code and does
not run its verifier. It reconstructs the symbolic Hessian directly from
the literal quartic, while separately evaluating the finite Jensen witness
using Python Fraction arithmetic. Its output is `REPLAY.json`.

## 1. Continuum acoustic proof reconstructed from the literal quartic

Let beta=99/100, r=88/25. First, exact expansion verifies

    F=h^T K h,
    K=[[1,0,beta],[0,1,0],[beta,0,r]],
    h=(u-v,2w,2q).

K is positive definite because r-beta^2=25399/10000>0. The Hessian
reciprocity D2F(A)[R,R]=D2F(R)[A,A] is checked as a polynomial identity
in eight independent real entries, and also follows from the symmetric
quartic tensor.

For any nonzero rank-one R, a left row rotation and scaling put it into
R=e1 tensor (cos phi,sin phi), |R|=1. Left row SO(2) rotations preserve
u,v,w,q and the Frobenius norm. This reduction covers both signs and all
rank-one matrices, not a sampled set of directions.

For an arbitrary perturbation with coordinates (a,b,c,d) in the associated
rotated column frame, direct differentiation gives the half-Hessian form

    6a^2+2b^2+2c^2+(4r-2)d^2
       +12beta cos(2phi) a d
       -4beta cos(2phi) b c
       -8beta sin(2phi) b d.                         (1)

The independent replay verifies (1) by substituting the rotation into the
literal Hessian and reducing the exact polynomial modulo
cos(phi)^2+sin(phi)^2=1. Permuting the middle coordinates yields exactly
the producer's matrix (3).

After eliminating a and c with leading diagonal block diag(6,2), its
Schur complement is 2N with

    N11=1-beta^2 s,
    N22=2r-1-3beta^2 s,
    N12=-2beta sin(2phi),       s=cos(2phi)^2.

Thus N11>=199/10000 and

    detN=3beta^4 s^2+2beta^2(1-r)s+2r-1-4beta^2.

Its vertex 2800/3267 lies in (0,1), and its exact global minimum on the
interval is 7/2500. This is a full continuum positivity argument.

For the explicit quantitative margin, traceN<=176/25, so
lambda_min(N)>=detN/traceN>=7/17600. The triangular completion has
off-diagonal operator norm at most beta<1; its inverse norm is at most
1+beta<2. Combining with the block minimum 2*(7/17600) and dividing by
the squared inverse bound gives the valid half-Hessian lower bound

    (1/2)D2F(R)[A,A]>=(7/35200)|A|^2|R|^2.           (2)

Homogeneity and reciprocity extend (2) to every A and every rank-one R;
zero A or R is included with equality. The claim uses this weighted
quartic notion of uniform strictness, not a positive Hessian lower bound
at the zero matrix independent of |A|.

## 2. Genuine support failure and its limiting cut

Independently expanding F(R+tA) at A=diag(36,35), Rplus=[[0,55],[-4,0]],
Rminus=diag(1,-2) reproduces all five coefficients in each displayed
expansion. The Schur values give exactly

    upper=14923057/550,
    lower=12087326489/445400,
    lower-upper=25999623/4899400>0.

The implication PC=>scalar minor support is sound: a convex representative
finite on the graph is finite on its convex hull, which is all R5 by the
explicit two-graph average. A subgradient exists. Differentiation only
along the smooth minors graph fixes its entry coefficient and produces
the unrestricted scalar support inequality.

Dividing that inequality for X=tR by t^2 and minimizing the remaining
quadratic is a necessary condition. A minimizing t=0 in the positive
cut is legitimate by a limit from nonzero t. There is no claim that a
zero increment itself provides a strict finite violation. The reversed
interval endpoints exclude every scalar selector, rather than one
polynomial or SOS class.

## 3. Direct actual three-atom witness

The stated positive weights are checked to sum exactly to one. The
literal rational increments are separately checked to have zero weighted
mean and zero weighted determinant. Direct evaluation at B_i=A+X_i then
gives

    sum lambda_i B_i=A,
    sum lambda_i detB_i=1260=detA,
    sum lambda_i F(B_i)-F(A)
      =-13534664264487807/296890944920312500<0.        (3)

This calculation uses the actual matrices and positive weights. It is
independent of the support theory, limiting cut, spectral search, and any
pseudo-moment relaxation. Jensen in the five minor coordinates contradicts
(3) for every convex lift, even without any differentiability assumption.

The algebraic recipe for lambda2 is also correct. Expanding the determinant
of the weighted mean and using lambda0+lambda1+lambda2=1 reduces the
minor-balance condition to

    lambda1 detX1+lambda2 detX2
       -lambda1 lambda2 det(X1-X2)=0,

which the displayed formula enforces. Positivity is checked for this
specific witness; it is not assumed for arbitrary inputs to the recipe.

## 4. Full-six box checked without alignment assumptions

For the three literal Hopf matrices H_i, the independent symbolic replay
checks H_i^2=I and H_i H_j+H_j H_i=0 for distinct i,j. Therefore H_i R are
pairwise orthogonal with common length |R|. For b_i=A^T H_i R this proves
|b|<=|A||R|. It also checks exactly

    (1/2)D2(h^TEh)(R)[A,A]
       =2h(A)^TEh(R)+4b^TEb.

Together with |h(A)|=|A|^2 and ||E||op<=3epsilon for a symmetric 3x3
entry box, the claimed perturbation bound 18epsilon |A|^2|R|^2 follows.
Subtracting it from (2) leaves

    7/35200-18/1000000=3979/22000000>0.

The witness's full 3x3 Hopf moment-difference matrix is reconstructed from
the actual atoms. Its entry-l1 norm is exactly

    236878462368814585323/59378188984062500.

Bounding the six-entry perturbation by the sum over all nine entries is
correct: off-diagonal terms are counted twice in both the trace pairing
and the norm. The perturbed Jensen defect is at most

    -2470054390528746814677/59378188984062500000000<0.

Hence the six independent entries may all change simultaneously, including
the previously zero off-diagonal entries. No symmetry retaining the
original alignment is required beyond the even-Hopf representation itself.

## 5. Aligned-family ROC boundary

For b=|beta|<1, N11>0 on [0,1], and detN>=0 is exactly

    r>=max_s [1+3b^2s+4b^2(1-s)/(1-b^2s)]/2.

The derivative has sign
3/2-2(1-b^2)/(1-b^2s)^2, after removing its nonnegative b^2 factor.
It is nonpositive throughout for 0<=b<=1/2, and has the stated single
interior maximizer for 1/2<b<1. Substitution gives the two branches in the
producer's formula. At b=0 it directly gives r>=1/2. At b=1,

    detN=(s-1)(3s-(2r-5)),

and positivity for every s in [0,1] requires and suffices that r>=4;
the s=1 diagonal case is then PSD. For b>1, N11(1)<0 excludes ROC.
All endpoint conditions and both necessity and sufficiency are covered.

## 6. Disposition boundaries and minor exposition point

The mathematical separation, explicit uniform margin, full-six box,
unrestricted support conflict, finite rational witness, and aligned ROC
classification are accepted. No material proof gap was found.

Section 6's phase-elimination expression is acquisition exposition and is
not needed for any of those conclusions: the final cuts and witness were
reconstructed independently. The producer was asked to state its unit
A,R normalization explicitly in that expression, since the displayed m
removes the |A| scaling. This is a minor clarification rather than a
qualification on the accepted theorem.

This review does not certify a numerical search as exhaustive, assess
historical priority, or establish a practical acquisition advantage. The
finite measure in (3) is not proved to be a laminate, a compatible gradient,
or a gradient Young measure. No failure of quasiconvexity follows. The
earlier rational-selector target remains a different, already PC/QC energy.

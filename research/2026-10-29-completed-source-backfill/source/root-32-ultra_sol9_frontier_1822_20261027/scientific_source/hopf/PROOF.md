# A strictly rank-one convex, non-polyconvex quartic in the even Hopf sector

This is an internally reconstructed exact result. Sections1–5 have a
completed independent substantive review with disposition **ACCEPTED**:
`../selector_opening/independent_hopf_review/REVIEW.md`. The reviewer
reconstructed the literal Hessian and finite Jensen measure without
importing producer code. The additional phase geometry and infinite
family are separate extensions and are not included in that disposition
unless explicitly added to its scope. The accepted theorem refutes ROC
implies PC in the six-parameter even Hopf sector.
It does not establish failure of quasiconvexity, world priority, or a physical
technology. The earlier rational-selector target remains positively resolved.

For every real matrix A=[[a,b],[c,d]], write

    u=a²+c², v=b²+d², w=ab+cd, q=ad−bc,
    T=u+v, x=u−v, y=2w, z=2q,  T²=x²+y²+z².

Consider the rational homogeneous quartic

    F(A)=T²+(252/25)q²+(99/25)q(u−v)
        =x²+y²+(99/50)xz+(88/25)z².                 (1)

Its even Hopf matrix is

    K=[[1,0,99/100],[0,1,0],[99/100,0,88/25]].

**Theorem.** F is strictly rank-one convex on all real 2 by 2 matrices and
is not polyconvex. The same two properties hold for every real symmetric
K' whose six independent entries differ from K by at most 1/1000000.
The latter statement uses F'(A)=h(A)^T K' h(A), with no retained alignment.

## 1. Exact continuum rank-one convexity

Put beta=99/100 and r=88/25. Quartic polarization gives

    D²F(A)[R,R]=D²F(R)[A,A].                         (2)

Thus it suffices to prove the full Hessian positive definite at every
nonzero rank-one R. Left row rotations and positive scaling reduce R to
a unit real spinor. Its Hopf vector is e=(cos theta,sin theta,0). In the
Hopf frame (e,(-sin theta,cos theta,0),e3), K has coefficients

    k=n=1, l=0, m=beta cos theta, p=−beta sin theta, r=r.

Direct differentiation in the corresponding orthonormal real perturbation
frame gives H=one half of D²F(R):

    H = [[6,0,0,6m],
         [0,2,−2m,0],
         [0,−2m,2,4p],
         [6m,0,4p,4r−2]].                            (3)

The leading block is D=diag(6,2). Its Schur complement is 2N, where

    N11=1−beta² s,
    N22=2r−1−3beta² s,
    N12=−2beta sin theta,
    det N=3beta⁴ s²+2beta²(1−r)s+2r−1−4beta²,
    s=cos² theta in [0,1].                          (4)

Here N11>=199/10000>0. The determinant's vertex is s=2800/3267,
strictly inside [0,1], and its exact minimum is 7/2500>0. Therefore N,
H, and the literal full Hessian at every unit rank-one R are positive
definite. Equation (2) proves strict ROC, with a uniform positive margin.

For an explicit margin, trace N<=2r=176/25, so N>=(7/17600)I.
Writing H as the congruence of diag(D,2N) by a block triangular matrix,
the off-diagonal block D^{-1}C=[[0,m],[-m,0]] has norm <=beta<1.
The inverse triangular factor consequently has norm <2. Hence

    (1/2)D²F(R)[A,A] >=(7/35200)|A|²|R|²             (5)

for every A and every rank-one R, by homogeneity and (2).

Also K is positive definite: its 1,3 principal block has determinant
r−beta²=25399/10000>0. Thus F(A)>0 for every A!=0.

## 2. No scalar minor support at one base point

For any quartic F, set

    T_F(R)=(1/2)D²F(R)−DF(R)DF(R)^T/(4F(R)).

A polyconvex F admits at every A a scalar k_A such that

    F(A+X)−F(A)−DF(A):X−k_A detX >=0 for every X.      (6)

For completeness, any convex lift finite on the minors graph is finite
on all R5: (B,s) is the average of the graph points at B+Y and B−Y if
detY=s−detB. A finite convex function has a subgradient. Differentiating
its touching support on the graph fixes the entry coefficient to
DF(A)−k_A cofA and gives (6).

Quartic polarization and minimization over real t in X=tR show (6)
requires

    A^T T_F(R)A−k_A detR >=0 for every R!=0.          (7)

Use the three small integer matrices

    A=diag(36,35),
    Rplus=[[0,55],[-4,0]], det Rplus=220,
    Rminus=diag(1,−2), det Rminus=−2.

Literal univariate expansion of F(R+tA) gives, in increasing t powers,

    Rplus: (35570561/5, 0, 29846114/5, 0, 113563553/5),
    Rminus:(2227/25, −10691/25, −1344076/25,
            −5883073/25, 113563553/5).

If these coefficients are c0,c1,c2,..., then

    A^T T_F(R)A=c2−c1²/(4c0).

The positive-determinant cut therefore requires

    k_A <=14923057/550,

while the negative-determinant cut requires

    k_A >=12087326489/445400.

The latter lower bound exceeds the former upper bound by

    25999623/4899400 >0.                             (8)

There is no scalar support at this A. This excludes unrestricted
polyconvexity, without a polynomial, continuity, degree, or SOS premise.
The zero minimizing scale in the Rplus cut is a valid limiting necessary
condition from (6); the next section supplies an entirely finite witness.

## 3. An exact three-atom minors-Jensen violation

At A=diag(36,35), take increments

    X0=[[-264/28745, −63481/114980],
        [5771/143725, 528/28745]],
    X1=[[0,11/20],[-1/25,0]],
    X2=diag(12/5,−24/5),

with positive weights

    (lambda0,lambda1,lambda2)=(5749/11542,1/2,11/5771).

They sum to one, sum lambda_i X_i=0, and sum lambda_i detX_i=0.
Consequently the matrices B_i=A+X_i have mean A and mean determinant
detA. Nevertheless exact literal evaluation gives

    sum lambda_i F(B_i)−F(A)
       =−13534664264487807/296890944920312500
       <−.0455.                                    (9)

Convex Jensen applied to any lift in (B,detB) contradicts (9). This is
a direct finite non-PC certificate, independent of differentiability of
a lift, the support reduction, or the Hopf eigenvalue geometry.

The weights were constructed rather than obtained by a moment relaxation.
For arbitrary rational X1,X2 and lambda1, put

    lambda2=lambda1 detX1/
      [−detX2+lambda1 det(X1−X2)],
    lambda0=1−lambda1−lambda2,
    X0=−(lambda1 X1+lambda2 X2)/lambda0.

Whenever all three weights are positive this enforces both required means.
Here lambda1=1/2 and the displayed X1,X2 give exactly the stated data.

## 4. A six-dimensional open separation, with an explicit box

Let C=sum lambda_i h(B_i)h(B_i)^T−h(A)h(A)^T. The exact verifier records
all nine rational entries. Their entry l1 norm is

    sum_ij |Cij|=236878462368814585323/59378188984062500.

For any symmetric E whose six independent entries obey |Eij|<=epsilon,
the change in (9) is bounded above by epsilon sum_ij |Cij|. At
epsilon=1/1000000, its resulting upper bound is still strictly negative,
as recorded exactly in EXACT_SEPARATION_REPLAY.json.

The Hessian perturbation satisfies

    |(1/2)D²(h^TEh)(R)[A,A]| <=6 ||E|| |A|²|R|²
                               <=18epsilon |A|²|R|².

Indeed h(A) has norm |A|², the Hopf polar vector b_i=A^TH_iR has
norm <=|A||R|, and the Hessian is 2h(A)^TEh(R)+4b^TEb.
Combine this with (5). The perturbed half-Hessian margin is at least

    7/35200−18/1000000=3979/22000000>0.              (10)

Thus every member of this full six-entry box is strictly ROC and non-PC.

## 5. Exact rank-one-convexity classification of the aligned family

For the normalized two-parameter family

    F_(beta,r)=x²+y²+2beta xz+r z²,

ROC holds exactly when |beta|<=1 and r>=R(|beta|), where

    R(b)=1/2+2b²                    for 0<=b<=1/2,
    R(b)=4−2 sqrt(3(1−b²))         for 1/2<=b<=1.

For |beta|>1, N11 at s=1 is negative. For b<1, positivity reduces to

    r >= max_(0<=s<=1)
       [1+3b²s+4b²(1−s)/(1−b²s)]/2.

Its derivative has the sign of
3/2−2(1−b²)/(1−b²s)². The maximizer is s=0 for b<=1/2 and is
[1−(2/sqrt3)sqrt(1−b²)]/b² otherwise, giving the formulas above.
At b=1 direct substitution yields detN=3(s−1)(s−(2r−5)/3), so
positivity on [0,1] holds precisely for r>=4. These statements also
include b=0, r=1/2 and all endpoint degeneracies.

The actual PC boundary of this whole family is not yet classified here.
The exact example and box settle the requested ROC-to-PC implication
negatively without needing that stronger classification.

## 6. Acquisition, ordinary comparator, and limits

The first attack eliminated the relative complex phase in the exact
global support matrix, with both A and R normalized to unit norm. With
sigma(n) the smallest eigenvalue of the
Schur complement of K along a unit Hopf vector n, and
v(n)=Kn−sigma(n)n, the minimized support value is
2[sigma(n)+m dot v(n)], m=h(A). For general nonzero A,R this normalized
value is multiplied by |A|²|R|². Arbitrary support selectors on unit A are
therefore equivalent to one scalar satisfying

    |m dot v(n)−k(m)n3/4|<=sigma(n) for every unit n.

ROC controls its equator. Opposite-height pairs give a selector-free
four-angular-variable separation search. A deterministic 70-matrix
diagnostic screen found the beta=.99 slice above; its full search and
local optimizations took 5.18 seconds on this host. The screen is not
a proof. A .052-second phase reconstruction acquired rounded rational
cuts. Small integer replacements produced the exact two cuts and the
three-atom witness. Standard-library rational replay took approximately
.002 seconds. These are measured local acquisition/replay costs, not
complexity or practical-advantage bounds.

All claims here concern global mathematical ROC and PC. The three-atom
measure matches the five minors but has not been realized by compatible
gradients or shown to be a gradient Young measure. Quasiconvexity is
UNKNOWN. A finite minors-Jensen violation does not refute QC.

Primary-literature comparison and historical priority checking are in
LITERATURE.md; absence of a match in a bounded search establishes no
world-priority claim.

The independent exact family in ALIGNED_FAMILY.md further supplies, for
every rational m>=197, a positive rational quartic in the same aligned
slice which is strictly ROC and fails PC at the identity matrix. Its
ordinary scalar support cuts are rational and its entire parameter
range has an analytic sign proof, verified symbolically in
verify_aligned_family.py. This is not a full PC boundary classification.

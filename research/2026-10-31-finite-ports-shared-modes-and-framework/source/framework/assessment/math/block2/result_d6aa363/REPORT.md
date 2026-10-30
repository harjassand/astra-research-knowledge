# A global polyconvex support construction for every exceptional cubic

The whole exceptional ROC/QC question remains open. This continuation establishes a positive result for **all four exceptional cubic coefficients** with an explicit quadratic threshold, and an exact complete answer for every isotropic lower quadratic when the exceptional coefficient matrix has rank at most one. It also proves that a nonempty interval of the remaining conformal-mode ROC family is non-polyconvex. The latter is not a QC separation.

Use the earned coordinates and normalization

    x=(a+d,c-b), y=(a-d,c+b), N(x,y)=|x|^2-|y|^2=4 det A,
    eta(y)=(y1^2-y2^2,2y1y2),
    P_(M,nu)=F0+x·M eta(y)+nu(|x|^2+|y|^2),
    F0=3F_(1/3)=2|x|^2|y|^2+|y|^4.

All thresholds below refer to P=3p, as in the shared capsule. They therefore preserve the original task's leading coefficient and quantifiers after division by three.

## Main positive theorem

For every real 2 by 2 matrix M,

    nu >= ||M||_F^2/8                                      (1)

implies that P_(M,nu) is polyconvex and hence QC. This includes weak equality in (1). The construction is a global explicit polynomial minor-support selector, proved by an exact rational sum of squares; it is not an oracle or an assumed compatible pointwise minimizer.

The earned sharp ROC threshold is

    nu_ROC=(2 sigma1(M)^2+sigma2(M)^2)/16.                  (2)

Consequently, if rank M<=1, then

    P_(M,nu) is ROC  iff QC  iff polyconvex
                       iff nu>=||M||_F^2/8.               (3)

Thus (3) completely resolves this nontranslation isotropic subfamily at its actual lower-quadratic boundary. For example,

    F0+x1(y1^2-y2^2)+(1/8)(|x|^2+|y|^2)

is globally polyconvex at its sharp ROC boundary. In the task's original normalization it is

    F_(1/3)+(1/3)x1(y1^2-y2^2)+(1/24)(|x|^2+|y|^2).

When M has full rank, the difference between the sufficient threshold (1) and the necessary ROC threshold (2) is exactly sigma2(M)^2/16. No claim of QC failure in that interval is inferred.

## 1. Explicit minor supports and a convex lift

At each background A=(x,y) set

    lambda_A=nu-|x|^2-2|y|^2.                              (4)

I prove that under (1), for every matrix B,

    P(B)-P(A)-DP(A):(B-A)-lambda_A N(B-A) >=0.              (5)

This is a global inequality, not only a positive Hessian condition. Since N is a quadratic null Lagrangian, (5) supplies affine supports in the ordinary minors variables. Explicitly define

    G(B,n)=sup_A { P(A)+DP(A):(B-A)
                   +lambda_A[n-N(A)-DN(A):(B-A)] }.        (6)

Every expression inside the supremum is affine in (B,n), so G is convex. Equation (5) says G(B,N(B))<=P(B), while A=B gives equality. Thus P(B)=G(B,N(B)), a polyconvex representation.

The lift is finite everywhere, if this convention is required: every point (B,n) is the midpoint of two minor-graph points (B+R,N(B+R)) and (B-R,N(B-R)), by selecting R with N(R)=n-N(B). Convexity and finiteness on the graph then bound G above at every point; any one support bounds it below. There is no regularity or global selection assumption beyond the explicit formula (4) and the proved inequality (5).

## 2. Proof of the global support inequality

Write the increment B-A=(H,K). Independent proper rotations of the x and y coordinate planes correspond to proper rotations of the original matrix on both sides. They preserve F0, the isotropic quadratic, N and the selector (4), while transforming M by orthogonal multiplication. Hence ||M||_F is unchanged, and for K nonzero we may take

    K=(k,0), H=(h,l), k>0,
    M=(m,n), q=|H|^2, a=q+k^2, Delta=q-k^2,
    s=H·m, t=H·n.

Here m,n are the two columns of the transformed M. Assume first q>0. Let E be the left side of (5). Direct expansion and completion in the four background coordinates gives

    E = |a x+4kH y1+2k^2 H+(k^2/2)m|^2/a
          +(4 Delta y1+2k Delta+k s)^2/(4a)
          +(4q y2+k t)^2/(4q)
          +k^2[q+2nu-(k^2|m|^2+s^2)/(4a)-t^2/(4q)].      (7)

This identity holds for every real M and every background x,y. The independent receiver reconstructs P and its gradient and verifies (7) symbolically.

At nu=||M||_F^2/8, the last line equals

    k^2 q + k^2 det(H,m)^2/(4a)
             + k^2 det(H,n)^2/(4q),                       (8)

because q|m|^2-(H·m)^2=det(H,m)^2, and likewise for n. Every term in (7)–(8) is nonnegative. Raising nu adds exactly 2(nu-||M||_F^2/8)|K|^2 to E. The cases q=0 or K=0 follow by continuity of the original polynomial E from the dense set q>0,K!=0. There is no division at a singular point in the final conclusion.

This proves (5) for all backgrounds and all increments. It also proves polyconvexity of F0 itself by setting M=0,nu=0. Historical priority of that homogeneous fact is not claimed; the new use here is its explicit lower-tail support extension.

The proof minimizes background coordinates only to certify a pointwise polynomial support inequality. It never treats the minimizing field as a gradient. Compatibility enters the QC consequence through the valid convex-minors representation and the ordinary null-Lagrangian identity.

## 3. Sharpness for this selector and the rank-one coefficient theorem

The threshold (1) is sharp for the explicit selector (4). From (7), after minimizing the background, the remaining gap is its last line. Fix k=1 and send H to zero in the direction of n when n is nonzero. Then

    (k^2|m|^2+s^2)/a -> |m|^2,
    t^2/q -> |n|^2, q->0.

If n=0, use any direction for H and the same limit holds with its second term zero. Thus a negative remaining gap occurs when 2nu<||M||_F^2/4. This excludes (4) below (1), not every possible polyconvex support selector.

For rank M<=1, however, (1) agrees with the previously established necessary ROC threshold (2), so no other argument is needed: PC implies QC implies ROC, and the global support proof gives the reverse direction at precisely the necessary coefficient. This includes every rank-one M, not only one fixed orientation or one sampled matrix. The family is preserved by argument translation, affine terms, arbitrary multiples of N (a linear minor term), and addition of convex quadratic forms. In particular, for

    Q=alpha |x|^2+beta |y|^2,

write nu=(alpha+beta)/2 and add ((alpha-beta)/2)N. The theorem requires alpha+beta>=||M||_F^2/4, and this is an exact ROC/QC/PC classification for rank M<=1, including quadratics with a negative individual coefficient. Its support selector is alpha-|x|^2-2|y|^2. No classification of arbitrary cross quadratic tails is claimed here.

## 4. An exact non-polyconvex ROC interval in the unresolved family

Take M=I and write

    nu=3/16+d,       d>=0.

These polynomials are globally ROC by the earned sharp criterion. They are **not polyconvex** throughout the explicit interval

    0<=d<1/6237.                                         (9)

A stronger algebraic interval proved below replaces 1/6237 by

    d_*=(43-3 sqrt(205))/288 > 1/6237.                    (9a)

This proves that a complete positive resolution of the original QC question cannot proceed by asserting polyconvexity of all ROC lower tails.

Here is a two-cut certificate allowing arbitrary convex lifts, not just the selector (4). At the fixed background

    A: x=(-1/4,0), y=(0,-1/4),

any polyconvex lift supplies some scalar lambda such that

    P(B)-P(A)-DP(A):(B-A)-lambda N(B-A)>=0                (10)

for all B. To justify existence without a smooth support selector, use an ordinary subgradient of the finite convex lift at (A,N(A)); differentiating its restriction to the graph gives the coefficient DP(A)-lambda DN(A). The midpoint argument from Section 1 ensures the lift is finite everywhere.

Use first the infinitesimal increment

    R: H=(0,1), K=(26/25,0),       N(R)<0.

The quadratic term in (10) must be nonnegative. The exact Hessian gives

    lambda >= (47-20816d)/816.                            (11)

Use next the finite increment tau W with

    W: H=(-2,0), K=(0,1), N(W)=3, tau=1/18.

In fact the entire support gap on this line is exactly

    tau^2[9tau^2-tau+5d-3(lambda-1/16)].                  (12)

At tau=1/18 it requires

    lambda <= 23/432+5d/3.                               (13)

The lower bound (11) exceeds the upper bound (13) precisely for d<1/6237. Thus (10) is impossible in (9), proving non-polyconvexity. Every coefficient and comparison is rational.

To optimize the infinitesimal cut, write e=lambda-1/16 and use the entire support-Hessian block in the x2,y1 coordinates. It is exactly

    [[1/2+2d-2e,-1/2],[-1/2,1/2+2d+2e]].

PSD therefore requires e^2<=d/2+d^2, while (13) requires 3e<=5d-1/36. For d<1/180 these can coexist only if

    5d+3 sqrt(d/2+d^2)>=1/36.

The left side is strictly increasing for d>=0 and reaches equality at d=d_* from (9a); squaring at this positive branch gives 20736d^2-6192d+1=0. Thus every 0<=d<d_* is non-polyconvex. The receiver checks the exact block determinant and radical identity. The earlier rational two-cut certificate is a slightly smaller, wholly rational subinterval of this conclusion.

At the left endpoint d=0 there is an especially short local explanation. The ROC acoustic zero forces lambda=1/16 if a PSD convex-minors support Hessian exists. Along W, (12) then becomes tau^3(9tau-1), strictly negative for 0<tau<1/9. Neither this support failure nor the local Hessian test is an actual compatible QC energy violation.

## 5. What the continuation adds and what remains

The shared checkpoint already supplied the canonical four-mode matrix M, the full exact ROC inequality, the sharp isotropic ROC threshold, and a compatible QC heat certificate for the conformal M modes at nu>=1/4. It also proved that the fixed primary heat completion cannot improve that coefficient. Those facts were retained at their exact scope.

This continuation supplies a different construction: an explicit convex-minors support and rational sum-of-squares identity valid for EVERY M at nu>=||M||_F^2/8. It newly covers the anticonformal modes and arbitrary combinations of all four cubic coefficients, and reaches the exact ROC boundary for every rank-one M. It strengthens the earlier large-quadratic conformal QC family to polyconvexity. The two-cut certificate proves a genuine non-polyconvex interval of globally ROC polynomials inside the unresolved conformal QC gap.

For M=I the complete scientific status from these artifacts is:

* nu<3/16: not globally ROC.
* 3/16<=nu<3/16+d_*: globally ROC and non-polyconvex; QC is not decided here.
* 3/16+d_*<=nu<1/4: globally ROC; neither QC nor polyconvexity is decided here.
* nu>=1/4: polyconvex, hence QC.

The original fixed-leading task still includes every full-rank M, sharp lower quadratics with all cross terms, and actual compatible gradients. No full-face QC proof or ROC/non-QC separation has been obtained. A stronger next construction must cover a non-polyconvex lower tail, or an independently ROC-admitted candidate must be paired with an actual compatible negative-energy field.

## Artifacts and source scope

`verify.py` independently reconstructs the global support identity, the nonnegative remainder for all M, the complete support-gap polynomial on W, both rational support cuts, their exact intersection, and the optimized local block giving d_*. `verification.txt` records the passing output. Run `python3 verify.py` in this directory. `polyconvex_probe.py` and `support_probe.py` preserve the exploratory calculations that led to the support construction and the non-PC cuts.

Sources were restricted to the frozen packet, the named capsule, and the prior files of this attempt. The ordinary convex-minors support principle is also explained in the packet's `math/hopf_structure/PROOF.txt`; it is used with a new explicit selector and lower-tail calculation here. The inherited homogeneous QC and primary heat primitive retain their original source credits, but neither is needed to validate the new polyconvex certificate. No network, sibling continuation, external result search, numerical optimization or agent delegation was used. The claims are internally symbolically checked, with no historical-priority or external-audit claim.

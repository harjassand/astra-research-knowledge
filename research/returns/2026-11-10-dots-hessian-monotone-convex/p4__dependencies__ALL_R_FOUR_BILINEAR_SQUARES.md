# All-parameter four-bilinear-square factorization

Date: 2026-11-09. Independently derived analytic continuation by the reviewing lane. No symbolic execution, numerical sampling, optimization, or global quasiconvexity conclusion.

## Statement

This extends the k=1 identity supplied by the parent/audit lead to the unchanged full family. It uses the selector in ALL_R_COMMON_SELECTOR.md, SHA256 454060110d5fdbd2043d703ea5f5a1a2efbf03b77e8a58486442d62c6cd5de96. The independent matrix review is INDEPENDENT_SELECTOR_REVIEW.md, SHA256 41b1345b8138eff89df0e75a668983d10755488232bd95fbf1a5c4b9c4e58967.

Let k>1/3, ell=3k−1, m=3k+1, n=k+1, and beta=ell/(8n). Here beta denotes the quartic coefficient called B in the governing source, to avoid confusion with a bilinear form below. Write X=[x,y] and Y=[p,q] by columns. Use x wedge y=det[x,y] and define

    A=x dot p, B=x wedge p, C=x dot q, D=x wedge q,
    E=y dot p, F=y wedge p, G=y dot q, H=y wedge q.

For q_k(Y)=Y^T S_kY with NO half factor,

    q_k(Y)=(3ell/m)(k|p|²−|q|²)+(24k/m)(p wedge q),
    P_k(X)=D²J_k(X)−det(X)S_k.

Then the exact identity is

    Y^T P_k(X)Y
      =ell/(4m) [3(kA+G)+(D+F)]²
       +3/(4nm) [ell(kA−G)+(5k+1)(D−F)]²
       +ell²/(4nm) [kB−C+E−H]²
       +3ell/(4m) [kB−C−E+H]².                       (1)

All four coefficients are positive for k>1/3. This provides an elementary sum-of-squares proof of the common-selector positive-semidefinite inequality, independent of the singular-surface/inertia proof.

At k=1, ell=2,m=4,n=2, formula (1) becomes exactly

    [3(A+G)+(D+F)]²/8
      +3[(A−G)+3(D−F)]²/8
      +(B−C+E−H)²/8
      +3(B−C−E+H)²/8.

At the excluded endpoint k=1/3, its continuous limit is 2(D−F)², consistent with J_0=det² and its rank-one selector remainder. No strict-rank statement is imported at that endpoint.

## Direct algebraic derivation

All eight displayed quantities are ordinary dot/wedge bilinears. The single relation needed to rearrange their quadratic products is

    BH+CE=AG+DF.                                      (2)

Useful elementary identities are

    |x|²|p|²=A²+B²,   |x|²|q|²=C²+D²,
    |y|²|p|²=E²+F²,   |y|²|q|²=G²+H²,
    detX |p|²=BE−AF,  detX |q|²=DG−CH,
    |x|² detY=AD−BC,  |y|² detY=EH−FG,
    detX detY=AG−CE=BH−DF.

Set alpha=3ell k/m and gamma=24k/m. The parameter identities are

    F0=4beta+1,
    4F0−gamma=(k−1)(alpha/k−8beta).

Differentiate the original quartic, substitute the dot/wedge identities, express detX detY initially as AG−CE, and add the identically zero quantity

    (alpha−8beta k)(BH+CE−AG−DF).

The result separates into two groups. The group in B,C,E,H is, with L=kB−C and K=E−H,

    4beta(L²+K²)+(8beta−alpha/k)LK
      =2beta(1−2/m)(L+K)²
        +2beta(1+2/m)(L−K)².                         (3)

These are the last two squares in (1), since m−2=ell and m+2=3n.

For the other group set a=kA, g=G and c0=alpha/(2k). In the vectors v=(a,D), w=(g,F), the group is

    v^T M v+w^T M w+2v^T Nw,

where

    M=[[12beta,12beta],[12beta,12beta+2]],
    N=[[(12beta−c0)/k, −12beta+c0],
       [−12beta+c0, 4beta(k−2)−alpha/2−2]].

Its two sum/difference blocks are exactly rank one:

    M+N=(c0/3) [[9,3],[3,1]],
    M−N=3/(2nm) [[ell²,ell(5k+1)],
                 [ell(5k+1),(5k+1)²]].

Applying

    v^T M v+w^T M w+2v^T Nw
      =((v+w)^T(M+N)(v+w)
          +(v−w)^T(M−N)(v−w))/2

gives the first two squares of (1), because c0/6=ell/(4m). This proves the identity without an empirical coefficient test.

## What the factorization buys

For each X, let R_k(X) be the 4-by-4 matrix whose rows are the four bilinear forms in (1), viewed as linear forms in Y and multiplied by the square roots of their positive coefficients. Then

    P_k(X)=R_k(X)^T R_k(X),

and R_k depends linearly on X. Thus the positive metric has an explicit four-component linear factor rather than an unspecified matrix square root. Its covariance under a compatible field is

    H=<D²J_k(X)>=<R_k(X)^T R_k(X)>,

using <detX>=0. This can be used in the exact all-background Schur problem or a nonlocal stress construction.

On setting Y=X, the four unweighted forms in order reduce to

    3(k u_X+v_X),
    ell(k u_X−v_X)+2(5k+1)detX,
    0,
    −2 x dot y.

The third metric channel therefore contributes to H but not directly to P_k(X)X. It is a real positive reserve, not permission to discard another term.

## What remains unpaid

Euler's identity is still

    3DJ_k(X)=R_k(X)^T R_k(X)X+det(X)S_kX.

The second term has a generally nonzero average on compatible gradients. The four-square identity does not convert it to a null Lagrangian or prove a contractive nonlocal representation. Pointwise positive-metric Cauchy–Schwarz applied only to the first term is insufficient.

There is a concrete pointwise warning. At X=[[1,t],[0,−m/2]], the selector has kernel I, while

    DJ_k(X):I=−ell(k+1)/4=−D.

Indeed the bilinear pairing X^T S_k I is 3ell(k+1)/(2m), detX=−m/2, and the selector kernel kills the other Euler term. Thus DJ_k(X) is not even in the pointwise range of P_k(X) on that surface. A pointwise representation of the entire cubic solely through its four metric channels cannot be assumed. Averaging and genuine curl compatibility are essential.

No global quasiconvexity conclusion, counterexample, or historical novelty assertion is attached to this factorization. The all-parameter extension was derived here from the lead's k=1 identity and frozen selector; it has been sent to the lead for a separate analytic check.

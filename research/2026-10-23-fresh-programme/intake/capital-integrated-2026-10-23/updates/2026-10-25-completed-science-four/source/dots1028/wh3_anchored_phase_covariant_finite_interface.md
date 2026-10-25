# Exact finite convex interface for an actual-N anchored gradient

2026-10-25. This reduces a genuine source-compatible anchored-gradient question without removing the channel Jensen gap. It does not settle the remaining finite minimization or arbitrary noncommuting marginals.

Let P=|psi><psi| be a rank-one maximal eigenprojection of A, normalized so

A=P+T, 0<=T<=I-P.

Let R=Tr_A A and R_P=Tr_A P. Assume [R,R_P]=0. Define the actual gradient

g(A;P)=Tr EP log EA-2Tr NP log NA,
N=W3 tensor id, E(X)=I3/3 tensor Tr_A X.

## 1. A legitimate twirl preserving the actual gradient comparison

Choose a common eigenbasis of R and R_P, and use a Schmidt decomposition

|psi>=sum_(i=0)^(k-1) u_i |i i>, u_i>0, sum u_i^2=1, k<=3.

Apply independent phases on physical Schmidt labels and their opposite phases on the matching reference labels; give unused reference eigenvectors independent phases too. This group fixes P and EA. WH covariance maps it to a corresponding output unitary group fixing NP.

For fixed EA, the function A -> -2Tr NP log NA is convex by operator convexity of -log. Hence averaging A over this group cannot increase g. The averaged A still satisfies A P=P, 0<=A<=I, and has the same R.

The averaged input consists of one arbitrary k-by-k block X on span{|i i>:i<k}, plus scalar occupancies a_ij on all other basis vectors. It obeys

Xu=u, 0<=X<=I_k, 0<=a_ij<=1,
r_j=X_jj+sum_(i!=j) a_ij,

for occupied reference labels j<k, with r_j the corresponding eigenvalues of R. All reference labels outside the Schmidt support can be discarded from this calculation, because the averaged state is reference-block diagonal there and neither EP nor NP has support on them. They do not enter g or its feasibility on the retained block. This is a source-preserving objective reduction, not an entropy-monotonicity claim about arbitrary reference discarding.

Thus for a fixed commuting pair R,R_P the minimizing actual anchored gradient has reference dimension at most3, regardless of the original reference dimension. No commutation of X with the diagonal R is imposed.

## 2. Exact Schmidt-rank-three objective

For k=3, the input has the correlated block X and six scalar occupancies a_ij, i!=j. For each unordered pair i<j define

v_ij=(u_j,-u_i)^T,
K_ij=(1/2)[[r_j-a_ij,-X_ji],[-X_ij,r_i-a_ji]].

The restriction of NP to the output pair span{|i j>,|j i>} is v_ij v_ij*/2. Its diagonal |i i> entries vanish. The actual N(A) has the displayed K_ij blocks, so

g(A;P)=sum_j u_j^2 log(r_j/3)
        -sum_(i<j) v_ij* log K_ij v_ij.                 (1)

At fixed u,r, this is a convex objective in X and the occupancies, over the exact affine/semidefinite constraints above. Singular output blocks are treated on the support of v_ij; NA>=NP makes the weighted logarithms well-defined. A faithful regularization can be used for computation.

The off-diagonal phase of X is retained. There is no replacement by diagonal spectra or a matrix mean.

## 3. Exact Schmidt-rank-two objective

For k=2 write u=(sqrt(l0),sqrt(l1)), l0+l1=1, and

X=P_u+t(I-P_u), 0<=t<=1.

There are four occupancies a10,a20 in column0 and a01,a21 in column1. Put p=a20,q=a21. The source constraints become

a10=r0-X00-p, a01=r1-X11-q,
0<=p,q,a10,a01<=1.

Define v=(sqrt(l1),-sqrt(l0)) and

K=(1/2)[[X11+q,-X01],[-X10,X00+p]].

The remaining two supported output atoms have masses (r0-p)/2 and (r1-q)/2. Hence the exact actual-channel objective is

g=l0 log(r0/3)+l1 log(r1/3)-v*log K v
  -l0 log((r0-p)/2)-l1 log((r1-q)/2).                   (2)

For fixed l0,r0,r1, equation (2) is a convex three-variable minimization over an explicit polytope in t,p,q. This is not merely a guessed ansatz: Section1 proves that it attains the source-face minimum whenever [R,R_P]=0.

For k=1 the same construction reduces to scalar occupancies. No arbitrary-dimensional quantum bath remains in these commuting-marginal source faces.

## 4. Remaining load-bearing question

To establish the maximal-gradient principle on this class one must prove that the minima of (1)-(2) are nonnegative for every feasible u,r. Their convexity at fixed r does not make the global problem convex after the positive logarithmic term in r is restored. Checking vertices of the source polytope is not sufficient for a convex minimization.

If [R,R_P]!=0, the phase averaging changes EA and its positively weighted log term. The displayed twirl then has no established direction for g, so that general interface remains outside this reduction.

## 5. Real rank-three reduction and exact diagonal feasibility

In the aligned Schmidt basis P and B are real. Complex conjugation preserves the source face and leaves g invariant. Convexity at fixed B therefore permits replacing A by (A+conj(A))/2 without increasing g. In the phase-twirled form this makes X real and leaves the scalar populations unchanged.

Let lambda_i=u_i^2>0 and d_i=1-Xii. The equation (I-X)u=0 now uniquely fixes every offdiagonal entry:

 2u_i u_j Xij=lambda_i d_i+lambda_j d_j-lambda_k d_k,

where {i,j,k}={0,1,2}. Thus X is determined by its three diagonal defects; no extra coherent phase remains in the minimization. Set D=I-X with these entries, tau=Tr D and eta=sum_{i<j}(Dii Djj-Dij^2). Since Du=0, the two remaining eigenvalues are real with sum tau and product eta. Consequently the exact constraint 0<=D<=I is equivalent to

 0<=tau<=2, eta>=0, 1-tau+eta>=0.

Proof: the first two imply the two eigenvalues are nonnegative; the last says they lie on the same side of 1, and tau<=2 rules out both exceeding 1 (except equality). Conversely the inequalities are immediate for eigenvalues in [0,1]. One may instead keep the affine LMIs 0<=D<=I to retain manifest convexity.

The complete aligned rank-three actual-g minimization therefore has three diagonal-defect variables and six scalar populations aij in [0,1], with r_j=1-d_j+sum_{i!=j}aij. At fixed r, the three marginal equalities leave six real degrees of freedom, subject to the stated LMIs/box constraints. Its objective remains the exact three 2x2 matrix-log expressions from Section 2. The scalar Rayleigh reduction is not valid as a final sign certificate: see `wh3_rank_three_pair_jensen_obstruction.md` for an exact actual-source failure and its quantitative within-pair gap repair.

## 6. Exact pair-gap resource, without a scalar tangent relaxation

For any positive 2x2 output block K and the unit anchor vector v of its NP block, choose a unit orthogonal vector w and set m=v*Kv, n=w*Kw, c=v*Kw. Then the exact scalar-log Jensen gap is

 J(K,v)=log m-v*log K v
       =|c|^2 integral_0^infinity ds / [(m+s)((m+s)(n+s)-|c|^2)].

This follows directly by subtracting the scalar and compressed resolvents; it remains valid by monotone limiting when K has a null eigenvalue orthogonal to v. Thus the exact aligned rank-three objective equals the scalar occupancy certificate G plus the three positive payments w_k J(Kij,vij). Here w_k=1-lambda_k and the total is two. In the orthonormal basis (v,w), |c|^2 is exactly the variance of K in v.

For maximal entanglement lambda_i=1/3, the real reduction gives, for pair (i,j) excluding k,

 m_k=(1+Xkk+a_ki+a_kj)/4,
 n_k=(2Xii+2Xjj-1-Xkk+a_ki+a_kj)/4,
 c_k=(Xjj+a_kj-Xii-a_ki)/4.

Consequently the missing log payment is explicitly driven by source imbalances, rather than an uncontrolled generic channel Jensen loss. A universal inequality comparing these three exact payments to the negative part of G remains unproved.

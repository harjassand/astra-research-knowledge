# Source-topface exclusion and exact Schmidt-sector reduction

2026-10-25. Proven local stationary exclusions and an exact reduced optimization; not an unrestricted entropy theorem.

Let E(X)=I_3/3 tensor Tr_A X. Let 0<A<=I, ||A||=1, P its top eigenspace, B=EA, C=(A+3B)/4, and j=Tr P(log B-2log C). The conditional receiving argument is in source_maximum_eigenspace_reduction.md.

## 1. Only coherence crossing the TOP eigenspace can obstruct this principle

If [P,B]=0, then j>=0, regardless of whether [A,B]=0. Indeed P reduces A,B,C and

C_P=(I_P+3B_P)/4.

The actual-source index A<=9B gives B_P>=I_P/9, and B<=I. For 1/9<=b<=1,

16b-(1+3b)^2=(1-b)(9b-1)>=0.

Functional calculus therefore gives

j=Tr_P log(16B_P/(I_P+3B_P)^2)>=0.

Consequently any negative faithful stationary minimizer in the regularized receiving argument must satisfy [P_max,EA]!=0. This is stronger than requiring [A,EA]!=0: arbitrary lower-tail reference coherence alone cannot produce such a minimizer. This statement does not assert that every point with [P_max,EA]=0 has nonnegative entropy deficit, since the receiving argument concerns stationary minimizers.

### Stronger rank-one exclusion inside a degenerate top eigenspace

The receiving argument may use ANY unit vector psi in the top eigenspace, not necessarily its entire projection. If psi is also an eigenvector of B, then j_psi=log[16b/(1+3b)^2]>=0 directly, since 1/9<=b<=1. Hence a negative stationary minimizer's top eigenspace contains no B eigenvector at all. This excludes more than [P_max,B]=0. In particular, if a B eigenspace has dimension d, then rank(P_max)+d cannot exceed the ambient dimension; otherwise their intersection contains such a vector. For B=I_3 tensor B_R and maximal reference spectral multiplicity d_R, rank(P_max)<=3n-3d_R is necessary.

## 2. A quantitative open neighborhood of this exclusion

Put Q=I-P, D=PBP, F=QBQ, V=PBQ+QBP, mu=lambda_min(B)>0, r=rank P, and

s(D)=Tr_P log(16D/(I_P+3D)^2)>=0.

The block logarithmic loss is L(X)=Tr_P log(X_PP)-Tr P log X>=0. Exact block decomposition gives

j=s(D)-L(B)+2L(C).

Moreover L(B)<=r||V||^2/(2mu^2), so the computable condition

s(D)>=r||PBQ||^2/(2mu^2)

certifies j>=0. Here ||V||=||PBQ||. To prove the bound, set B_t=diag(D,F)+tV. Both endpoints are >=mu I (pinching preserves this lower bound), hence every B_t>=mu I. For h(t)=Tr P log B_t, h'(0)=0 and the resolvent formula gives

|h''(t)|<=2r||V||^2 integral_0^infinity (mu+s)^(-3) ds
           =r||V||^2/mu^2.

Taylor's integral remainder proves the bound. No commutation of D,F,V is assumed. The condition loses efficacy near a singular marginal or the scalar endpoints 1/9,1, as expected; it is sufficient, not necessary.

## 3. Exact reference-dimension-free reduction for rank-one P and [EP,B]=0

Suppose P=|u><u| and [EP,B]=0. Choose simultaneous eigenbases so

u=sum_{j=1}^k sqrt(p_j)|j,j>, 1<=k<=3, p_j>0, sum p_j=1,
B=I_3 tensor diag(b_1,...,b_n).

This choice is possible by Schmidt decomposition followed by unitary rotations inside degenerate eigenspaces of Tr_A P. Consider ALL effects A=P+T, 0<=T<=I-P, ET=B-EP. Their minimum j equals the minimum of

sum_{j=1}^k p_j log b_j - 2<u,log((X+3diag(b_1,...,b_k))/4)u>

over k by k Hermitian X satisfying

0<=X<=I_k, Xu=u,
max(0,3b_j-2)<=X_jj<=min(1,3b_j), 1<=j<=k.       (R)

Thus no matter how large the reference or how complicated the lower spectrum, this entire source-topface problem has dimension at most three.

Proof: independently twirl phases on the three A basis vectors and compensating inverse phases on the first k reference vectors; give remaining reference vectors independent phases. This local-unitary twirl fixes P and B. All correlated vectors |j,j>, j<=k, have trivial character; every other basis vector has its own nontrivial character. Therefore the twirled A consists of a k-dimensional correlated block X and scalar diagonal entries t_ij elsewhere. Convexity of -Tr P log((A+3B)/4) shows that the twirl can only decrease j. The source constraint in column j<=k is

X_jj + sum_{i!=j} t_ij=3b_j, 0<=t_ij<=1.

There are exactly two such off-correlated entries per column, giving (R). Remaining columns require only sum_i t_ij=3b_j, feasible because 0<=b_j<=1. Conversely every X satisfying (R) extends to a physical source-compatible effect by distributing each column's remainder among its two or three scalar entries. The log objective only sees X because P is supported in that invariant block. This proves equality of the minima, not a relaxation. The closure allows an enlarged top eigenspace, which is harmless for a lower bound on the original face.

## 4. Schmidt rank two reduces to a one-variable endpoint

For k=2 let p=p_1, 1-p=p_2 and u=(sqrt p,sqrt(1-p)). Every admissible X equals

X=P_u+t(I_2-P_u), 0<=t<=1.

The objective is nonincreasing in t by operator monotonicity of log. Its minimum is therefore at

t_max=min(1,(3b_1-p)/(1-p),(3b_2-(1-p))/p).

The lower diagonal bounds only impose lower bounds on t and do not alter this maximum for a nonempty face. This yields a completely explicit two by two logarithm test for every rank-two Schmidt source face with [EP,B]=0. A universal analytic nonnegativity proof of that endpoint is NOT supplied here.

## Boundary of the advance

The top-commuting exclusion, its stability condition, and the exact source-preserving reduction are proved. Universal positivity of (R), and the case where EP and B do not commute, remain open. A bounded numerical rank-two minimization approached zero at the identity endpoint; this is not used as evidence in any theorem above.

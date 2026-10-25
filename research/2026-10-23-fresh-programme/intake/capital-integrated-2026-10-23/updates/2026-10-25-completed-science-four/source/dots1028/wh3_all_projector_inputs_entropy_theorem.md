# The full WH3 entropy inequality for every normalized projector input

2026-10-25. Analytic receiving theorem from the noncommutative Schur-log transport, with the physical resource bound acquired from the conditional expectation itself. This covers arbitrary input rank and arbitrary finite quantum reference, not only rank-one or flat reference states. General mixed input spectra remain open.

## Theorem

Let N=W_3 tensor id_R, where W_3(X)=(Tr(X)I_3-X^T)/2. Let E(X)=I_3/3 tensor Tr_A X. For every nonzero orthogonal projection P on C^3 tensor R, of rank m,

D(P/m || E(P/m)) >= 2 D(N(P/m) || E(P/m)).          (1)

No flatness or commutation of the reference marginal is assumed. Equivalently, with the homogeneous deficit

Delta_N(X)=D(X||EX)-2D(NX||EX),

one has Delta_N(P)>=0 and hence Delta_N(P/m)>=0.

The governing transport theorem is operator_schur_log_transport_theorem.md. We spell out its actual receiving interface and the singular support limit rather than assume them.

## 1. Both index bounds are physical

Put B=E(P). The established complete index inequality X<=9E(X) for X>=0 gives

P<=9B.

Apply the SAME inequality to the positive complement I-P. Since E is unital,

I-P<=9E(I-P)=9I-9B.

Therefore

0<=9B-P<=8I.                                      (2)

This is the required operator budget, not merely a trace budget or an assumed operator norm. It holds in every finite reference dimension. Also 0<=B<=I.

## 2. First treat full marginal rank 3m

Restrict the reference to the support of R=Tr_A P and write P=UU*, where U:C^m -> C^3 tensor R is an isometry with three blocks U_i:C^m ->R. Then

R=sum_i U_i U_i*, sum_i U_i*U_i=I_m.

If dim R=3m and R>0, the square matrix M=[U_1 U_2 U_3] is invertible and R=MM*. Hence

U_i*R^(-1)U_j=delta_ij I_m.

It follows that

U*B^(-1)U=3 sum_i U_i*R^(-1)U_i=9I_m.             (3)

Conversely, uniform cap saturation P B^(-1) P=9P in a faithful source pair forces dim R=3m, because Tr(P B^(-1)P)=3 rank R. We need only the forward implication for the construction.

Split the physical space as P plus Q=I-P. Since B>0, its Q block V=B_QQ is positive definite. Equation (3), through the block inverse formula, says its Schur complement is exactly I_P/9. Thus, for W=B_PQ V^(-1/2),

B=[[I_P/9+WW*, W V^(1/2)],
   [V^(1/2)W*, V]].                               (4)

Define Wtilde=3W and Vtilde=9V. With L the column matrix [Wtilde; Vtilde^(1/2)],

L L*=9B-P<=8I,

so

Wtilde*Wtilde+Vtilde=L*L<=8I.                      (5)

This is exactly the operator Schur-log transport's hypothesis, with arbitrary rectangular Wtilde and noncommuting coefficient operators. Equality of nonzero singular values of L and L* justifies the implication; no trace-to-order inference occurs.

## 3. Receive the exact compressed-log inequality

For r>0 define the actual block pencil

X_r=[[rI_P+Wtilde Wtilde*, Wtilde Vtilde^(1/2)],
     [Vtilde^(1/2)Wtilde*, Vtilde]],

and J_r=P log(X_r) P-(log r)I_P.

The operator transport theorem and (5) give

J_1>=2J_4.

Here X_1=9B and X_4=9B+3P. Put C=(P+3B)/4; then X_4=12C. The scalar logarithms cancel exactly, so the obtained inequality is

2P log C P-P log B P=2J_4-J_1<=0.                 (6)

All off-diagonal Schur correlations in B remain present. This is not an application of a scalar inequality to noncommuting coefficients.

## 4. Approximate every projection by full-marginal-rank projections

A rank-m projection has marginal rank at most 3m. Restrict to its current marginal support and enlarge the reference, if necessary, to dimension 3m by adjoining unused orthogonal directions. Neither P nor its nonzero entropy spectra change.

Choose an isometry U_0 with three blocks (U_0)_i=J_i/sqrt3, where J_i embed C^m into three mutually orthogonal m-dimensional reference subspaces. Its matricization [ (U_0)_1 (U_0)_2 (U_0)_3 ] is invertible.

For small real e>0 set

Z_e=U+eU_0,
U_e=Z_e(Z_e*Z_e)^(-1/2),
P_e=U_e U_e*.

The unnormalized matricization [U_1+e(U_0)_1, U_2+e(U_0)_2, U_3+e(U_0)_3] has determinant a polynomial in e whose top coefficient is the nonzero determinant of the U_0 matricization. It therefore has only finitely many roots. Choose a sequence e down to zero avoiding those roots. Right multiplication of every block by the common invertible matrix (Z_e*Z_e)^(-1/2) preserves the matricization rank. Thus P_e has rank m and full marginal rank 3m, and U_e->U, P_e->P.

By the preceding argument,

U_e*[2log C_e-log B_e]U_e<=0,

where B_e=E(P_e), C_e=(P_e+3B_e)/4.

## 5. Pay the singular logarithms uniformly

Ordinary norm continuity of log cannot be used because B=E(P) may have a kernel in the enlarged reference. Instead use the acquired domination P_e<=9B_e. For a cutoff epsilon>0 define log_epsilon X=log(max(X,epsilon I)) by functional calculus.

The omitted low-spectrum term is negative semidefinite after compression, with norm bounded by its trace:

||U_e*(log B_e-log_epsilon B_e)U_e||
<=Tr P_e [log_epsilon B_e-log B_e]
<=9 Tr B_e [log_epsilon B_e-log B_e]
<=9D epsilon/euler_number,

where D=9m is the fixed ambient dimension. The last step uses x log(epsilon/x)<=epsilon/euler_number for 0<x<epsilon. The same bound holds at the limiting pair on its actual support; P has zero component on ker B.

For C_e, one has P_e<=4C_e. The identical argument bounds its compressed low-spectrum tail by 4D epsilon/euler_number.

For fixed epsilon, log_epsilon is a continuous scalar function on the common bounded spectral interval, so finite-dimensional continuous functional calculus and U_e->U give convergence of the truncated compressions. Then let epsilon tend to zero using the uniform tail bounds. Therefore

U_e*log B_e U_e -> U*log B U,
U_e*log C_e U_e -> U*log C U,

where the limiting logarithms are used only on their supports. Equation (6) consequently holds for EVERY projection P, with no maximal-marginal-rank assumption.

## 6. The full entropy target on this input class

The channel N is self-adjoint, unital, fixes B and satisfies

N^2=(1/4)id+(3/4)E,

so N^2(P)=C. Operator Jensen gives

N(log(NP))<=log C

in the appropriate supported limit. One rigorous way to take it is to apply Jensen to NP+epsilon I>0, use N(NP+epsilon I)=C+epsilon I, multiply by P and trace. Self-adjointness yields

Tr P N(log(NP+epsilon I))=Tr NP log(NP+epsilon I).

As epsilon tends to zero, the left spectral sum converges to Tr NP log NP with 0log0=0. The compressed right logarithm converges because C>=P/4. Hence

2Tr NP log NP<=2Tr P log C<=Tr P log B.

Since log P=0 on its support and E is a trace-preserving conditional expectation,

Tr P log B=Tr B log B.

Moreover N fixes log B on its support, yielding the homogeneous identity

Delta_N(P)=Tr P log B-2Tr NP log NP>=0.

Finally relative entropy is homogeneous under simultaneous scaling of its two arguments, so Delta_N(P/m)=Delta_N(P)/m. This proves (1).

## Exact scope

All normalized projections P/m are now covered, regardless of rank, reference dimension or marginal spectrum. The statement is stronger than a rank-one endpoint exclusion and has a direct full-target entropy consequence. It does not cover arbitrary nonflat density spectra. Writing a general state as a mixture or layer integral of projections does not transfer this nonlinear entropy deficit without an additional proved inequality; no convexity of Delta_N is asserted.

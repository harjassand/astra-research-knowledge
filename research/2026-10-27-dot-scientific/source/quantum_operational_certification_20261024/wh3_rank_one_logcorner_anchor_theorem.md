# Rank-one correlated block: logarithmic-corner anchored theorem

## Actual source theorem

Let u=(sqrt(lambda_0),sqrt(lambda_1),sqrt(lambda_2)), with positive weights summing to one, and let P=|psi><psi| for psi=sum_j u_j|jj>. For arbitrary 0<=aij<=1, i!=j, set

 A=P+sum_{i!=j}aij |ij><ij|,
 r_j=lambda_j+sum_{i!=j}aij.

Then the stronger Jensen-relaxed top certificate is nonnegative:

 j(A;P)=Tr P log EA-2Tr P log[(A+3EA)/4]>=0.        (1)

Consequently the actual WH3 anchor g(A;P)>=j(A;P)>=0. No column-sparsity restriction is needed. Zero Schmidt weights in the strong certificate follow by the uniform supported limit proved below; the actual-anchor conclusion is also consistent with the earlier aligned rank-two theorem.

On the correlated span, (1) is exactly

 j(r)=sum_j lambda_j log(r_j/3)
      -2 u*log[(uu*+diag r)/4]u,
 r_j in [lambda_j,lambda_j+2].                    (2)

The rectangle is the true source marginal domain, not an independently relaxed budget.

## 1. General rank-one logarithmic diagonal convexity

Let u have positive entries and let all fixed diagonal entries r_i>0. Then

 F(x)=u*log[uu*+diag(r_1,...,exp(x),...,r_n)]u

is convex in x. The claim holds in any finite dimension.

Fix the varied coordinate j, write a=|u_j|^2 and y=exp(x). For s>=0 define

 q(s)=sum_{i!=j}|u_i|^2/(r_i+s),
 q_2(s)=sum_{i!=j}|u_i|^2/(r_i+s)^2,
 q_3(s)=sum_{i!=j}|u_i|^2/(r_i+s)^3.

Schur complement and Sherman-Morrison give the varied resolvent component

 [(uu*+diag r+sI)^(-1)u]_j
   =sqrt(a)/[(1+q(s))(z(s)+y)],
 z(s)=s+a/(1+q(s)).

Thus W(s)=a/(1+q)^2 and z'=1+a q_2/(1+q)^2. Differentiating the log resolvent twice with respect to x=log y yields

 F''(x)=y integral_0^infinity W(s)(z(s)-y)/(z(s)+y)^3 ds.

Exactly as in the earlier two-dimensional log-corner argument, integrate by parts:

 F''(x)=y [W(0)/z'(0)] z(0)/(z(0)+y)^2
   +y integral_0^infinity (W/z')'(s) z(s)/(z(s)+y)^2 ds.

All displayed quantities are finite and z(0)>0; the boundary at infinity vanishes. Crucially,

 W/z'=a/[(1+q)^2+a q_2],
 d/ds[(1+q)^2+a q_2]
   =-2(1+q)q_2-2a q_3<=0.

Therefore (W/z')'>=0 and F''>=0. This proves the convexity without a commutativity assumption or a pointwise sign claim for the unintegrated second-derivative kernel.

## 2. The entire source rectangle reduces to genuine projection corners

The first term of (2) is affine in each log r_j, while the second is minus twice a convex function of that logarithmic coordinate. Thus j is separately concave in log r_j. Iterating the endpoint minimum property over the three coordinates gives

 j(r)>=min_{epsilon in {0,1}^3} j(lambda+2epsilon).

For every corner epsilon construct the ACTUAL source projection

 Q_epsilon=P+sum_{j:epsilon_j=1}sum_{i!=j}|ij><ij|.

Its summands are orthogonal, and E(Q_epsilon) has the required marginal r_j=lambda_j+2epsilon_j. The already proved all-projector compressed-log theorem states

 Q_epsilon [log E(Q_epsilon)
       -2log((Q_epsilon+3E(Q_epsilon))/4)]Q_epsilon>=0.

Since psi belongs to its range, compression to psi gives exactly the corner inequality in (2). Every corner is therefore nonnegative, proving (1) for the entire source rectangle.

## 3. Actual-channel receiving step and full entropy class

For a normalized top anchor, operator Jensen for the self-adjoint unital channel N gives

 Tr NP log NA<=Tr P log N^2 A,
 N^2 A=(A+3EA)/4,

with the supported limiting interpretation already established in the projector/source chain. Hence actual g>=j.

As a full-value consequence, every input

 A=alpha P+sum_{i!=j}beta_ij |ij><ij|,
 alpha,beta_ij>=0,

satisfies Delta(A)>=0, for arbitrary pure matched-correlated P and arbitrary diagonal populations. Use its orthogonal eigenbasis consisting of psi and the product basis populations. Whenever psi is at the top level, normalize by alpha and apply the anchored theorem above; product top vectors use the universal product-top anchored theorem. Spectral lowering preserves this source class at every step. Finish at a scalar support projection (already safe) or zero by entropy continuity. This is a genuine full-value class, not an assumed entropy-convexity lift.

## Dependencies and limits

The corner payment is the full compressed-log result in `wh3_all_projector_inputs_entropy_theorem.md`, not merely its traced entropy corollary. The integration-by-parts mechanism generalizes `schmidt_two_topface_logcorner_reduction.md`, with rank-one Sherman-Morrison replacing its 2x2 sign condition. This theorem does not assert logarithmic-coordinate convexity for arbitrary higher-rank correlated X; that would require a new proof.

## Endpoint, scale, and support details

For the STRONG certificate j, zero Schmidt weights are handled by continuity, not by borrowing a weaker actual-anchor result. Choose positive probability vectors lambda^(epsilon) tending to lambda and keep every population aij fixed. Then r_j^(epsilon)=lambda_j^(epsilon)+sum_i aij, and the diagonal weighted terms converge because r_j>=lambda_j and t log t tends to zero.

For the correlated matrix M_epsilon=P_epsilon+diag r^(epsilon), one has P_epsilon<=M_epsilon. Uniformly in epsilon, the omitted low-spectrum compressed log tail is bounded by

 Tr P_epsilon [log_eta M_epsilon-log M_epsilon]
 <=Tr M_epsilon [log_eta M_epsilon-log M_epsilon]
 <=3eta/e.

For fixed eta>0 the truncated functional calculus is continuous. Passing epsilon to zero and then eta to zero proves the strong j limit on the anchor support. If a Schmidt coefficient is zero but its column has positive populations, the matrix-log term is ordinary continuous there. Thus the stated strong theorem includes all Schmidt ranks.

For the full-value input alpha P+sum beta_ij|ij><ij|, arbitrary nonnegative coefficients are allowed. If alpha=0 the input has a product eigenbasis and is already safe. If alpha>0, whenever P participates in the current top spectral level L=alpha, divide the entire current source by L. The coherent coefficient becomes one and every population lies in [0,1], exactly as required by the anchored theorem. The entropy-deficit gradient is invariant under this scaling because its logarithmic constants cancel. Top product vectors are covered independently, including intervals when some populations exceed alpha.

Choose the orthogonal eigenbasis consisting of psi and the positive product populations. During top-level lowering this source representation is preserved, including degenerate top levels. The derivative of the entire top projector is the sum of its rank-one derivatives in that eigenbasis. Lower only to the smallest positive spectral level: the endpoint is a scalar support projection, covered by the all-projector theorem. On every open segment the input support is fixed and each varied projection is dominated by a positive multiple of the current A; N and E preserve the corresponding support domination. Therefore all supported entropy derivatives used in the receiving proof exist. No extra regularization across a changing support is required. Division by Tr A then gives the normalized-state target.

Complex Schmidt amplitudes are removed by local basis phases, using WH covariance and entropy invariance. The finite matched reference span may be isometrically embedded in any larger reference space; all statements use the actual supported operators.

## Arbitrary-source rank-one matched-compression receiver

Let 0<=A<=I have a top vector psi whose reduced projector commutes with R=Tr_A A. Choose a common reference eigenbasis and the corresponding Schmidt basis, and let J be the isometry into the matched correlated span. If

 J* A J=uu*,

then the actual anchored gradient is nonnegative, even when A has arbitrary coherences outside that span. Indeed the source-preserving phase twirl from `wh3_anchored_phase_covariant_finite_interface.md` fixes P and EA and cannot increase actual g. Its relevant correlated block is exactly rank one, and its remaining relevant entries are populations in [0,1]. The log-corner theorem applies. Reference components outside the Schmidt support contribute neither to EP nor NP after the twirl.

Thus a negative global stationary minimizer of the full deficit cannot possess an aligned maximal eigenvector with rank-one matched compression. This is an actual-source exclusion. It does not say that marginal alignment alone forces that compression to be rank one.

## Entire ambient-scalar-floor extension

A further full source family is acquired without an assumed scalar-noise lift. Let

 X=beta I_3+c uu*, c=1-beta, 0<=beta<1,

and let every offdiagonal product population lie in [beta,1]. The actual normalized input is X on the correlated span and those populations elsewhere. Its marginal rectangle is

 r_j in [3beta+c lambda_j, 3beta+c lambda_j+2c].

The strong certificate remains j=sum lambda_j log(r_j/3)-2u*log[(X+diag r)/4]u. Its separate logarithmic concavity follows from the same Schur proof. In the notation of Section 1, now use

 q(s)=sum_{i!=j}lambda_i/(beta+r_i+s),
 W=lambda_j/(1+cq)^2,
 z=s+beta+c lambda_j/(1+cq),
 W/z'=lambda_j/[(1+cq)^2+c^2 lambda_j q_2].

The denominator derivative is

 -2c(1+cq)q_2-2c^2 lambda_j q_3<=0,

so the integration-by-parts proof is unchanged.

At every marginal corner, all offdiagonal populations in a column equal either beta or one. The resulting ACTUAL source is

 A_corner=beta I_9+c Q_epsilon,

where Q_epsilon is the same projection used in Section 2. The shifted all-two-level COMPRESSED-log theorem applies on its top projection Q_epsilon. After max-eigenvalue normalization its top log-A term is zero, so it gives j>=0 on psi. Thus every corner is paid, and separate logarithmic concavity proves strong j>=0 throughout this entire shared-floor source family. The beta=1 endpoint is the identity and follows directly or by continuity.

Consequently every input

 A=alpha I_9+gamma P_psi+sum_{i!=j}dij |ij><ij|,
 alpha,gamma,dij>=0,

satisfies Delta(A)>=0. During spectral lowering, product populations above the coherent level are handled by the universal product-top anchor. Whenever psi is top, its level is L=alpha+gamma and the normalized source has beta=alpha/L, with all normalized populations between beta and one. The just-proved floor theorem therefore pays its derivative. Lowering preserves the common ambient floor alpha and ends at alpha I_9, where Delta=0. If alpha=0, use the earlier fixed-support/continuity receiver. Complex phases and matched reference embeddings are handled as before.

The proof DOES NOT cover populations below the correlated scalar floor. Their log-rectangle corners have spectrum 0,beta,1 on a nonproduct support and are not licensed by the ambient-I two-level theorem. This distinction is the remaining load-bearing boundary for a further extension.

## Operator-valued populations within Schmidt reference columns

The scalar-population value theorem extends to genuine physical matrix populations. Fix Schmidt bases psi=sum_j sqrt(lambda_j)|j,r_j>. For every Schmidt reference column choose a positive physical matrix D_j annihilating its matched physical basis vector e_j:

 D_j e_j=0.

Then every input

 A=alpha I+gamma P_psi+sum_j D_j tensor |r_j><r_j|,
 alpha,gamma>=0,

satisfies Delta(A)>=0. Positive reference-column matrices outside the Schmidt support may also be included. No common diagonalization of the D_j is required.

Each D_j is therefore supported on the physical orthogonal complement of e_j. Therefore the population tail annihilates the matched correlated span, and its eigenvectors are product vectors orthogonal to psi. The reference marginal stays diagonal. The source-preserving phase twirl fixes P and EA and reduces the physical column matrices to scalar populations; if psi is top, their eigenvalues and diagonal entries lie between the common ambient floor and the current top level. The rank-one or shared-floor anchored theorem therefore applies. All other top eigenvectors can be chosen from the product tail eigenbasis.

Spectral lowering preserves the reference-column support condition and the common ambient floor. Thus the full-value receiver is exactly the same as before. This family is not reference-classical as a whole: P retains coherence across Schmidt reference columns, while the tail matrices can have arbitrary physical coherences within each column.

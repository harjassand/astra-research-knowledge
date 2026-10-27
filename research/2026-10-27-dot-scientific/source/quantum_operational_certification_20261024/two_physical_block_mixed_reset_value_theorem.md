# Two physical reset blocks with arbitrary coherent logical baths

Status: independently received PASS in two_physical_block_reset_independent_audit.md, corroborated for fixed-K and both payments by two_physical_block_summed_bath_reciprocal_audit.md. Scope is actual reset tau=|1><1| tensor T1+|2><2| tensor T2 with arbitrary PSD logical T1,T2 and Tr(T1+T2)=1. Neither logical bath must commute with sigma or the other bath. Arbitrary physical coherences between the two blocks, or three nonzero physical blocks, are not inferred.

Claim: for E(rho)=p rho tensor sigma+q Tr(rho)tau, Delta>=0. Equality iff p q=0 or sigma(T1+T2)=0.

Set S=p sigma/3 and Qi=q Ti/3. The exact source expansion and pointwise n>=5 payment are in rank_two_physical_block_reset_three_degree_reduction.md. Actual-source Gram identity replay on40 complex k2/3 examples has maximum error2.8e-15 (rank_two_physical_block_reset_source_check.py). Degree1 is a sum of strictly positive pure-physical resources, zero exactly if S(Q1+Q2)=0. Only n2–4 need a new argument.

## Summed-bath reciprocal lemma

Define
J_n(S;Q1,Q2)=integral Tr[(P_S(P_Q1+P_Q2))^n] ds,
I_n(S,Q)=integral Tr[(P_S P_Q)^n] ds.

The function F(u,v)=J_n(S/u;Q1/v,Q2/v) is jointly convex by the same Zhang trace theorem as the received two-operator reciprocal lemma. To see the exact fixed-K representation, let
A=diag(I+us S^(-1), I+us S^(-1)),
B=diag(I+vs Q1^(-1), I+vs Q2^(-1)),
K=[[I,I],[0,0]].
Then B^(-1/2) K* A^(-1) K B^(-1/2) has the same nonzero eigenvalues as P_S^(1/2)(P_Q1+P_Q2)P_S^(1/2), with the stated inverse-scale arguments. Zhang's theorem for invertible fixed K extends to this square singular K by taking K_epsilon=[[I,I],[0,epsilon I]] and continuity of finite-dimensional positive trace powers. Integration preserves convexity, and F has degree-minus-one homogeneity. Therefore 1/F is concave. Its midpoint consequence is

J(S;Qi)/J(3S;Qi)+J(S;Qi)/J(S;3Qi)<=4/3.             (R)

Faithful matrices suffice initially. Singular PSD inputs follow by adding epsilon I and dominated convergence; near infinity the integrand is O(s^(-2n)) uniformly and near zero it is bounded by a dimension-dependent constant. No dimension-dependent constant enters the final value claim.

## Two complementary payments for the same positive resource

Fix n=2,3,4. Write
C=J_n(S;Q1,Q2), c=I_n(S,Q1)+I_n(S,Q2),
A=J_n(3S;Q1,Q2), b=I_n(S,3Q1)+I_n(S,3Q2),
alpha=3^(-n), beta=2^(1-n), k=2^(n-1), D=alpha A+b.

The actual degree numerator is D-beta(C+c).

First, trace-power superadditivity gives A>=sum_i I_n(3S,Qi). Apply the received ordinary reciprocal lemma and weighted Cauchy separately to each bath:

D>=K1 c,  K1=(3/4)(sqrt(alpha)+1)^2.                 (P1)

Second, trace-power convexity gives J_n(S;3Q1,3Q2)<=k b. Apply (R) and weighted Cauchy:

D>=alpha A+J_n(S;3Qi)/k>=K2 C,
K2=(3/4)(sqrt(alpha)+1/sqrt(k))^2.                  (P2)

Combining these two bounds on the SAME D,

beta(C+c)<=theta_n D,
theta_n=beta(1/K1+1/K2)<1.                         (P3)

Exact rational upper bounds are

theta_2 <242763/245000<1,
theta_3 <41556033/44700500<1,
theta_4 <24165027/26645000<1.

They follow by using sqrt2>7071/5000 and sqrt3>433/250 in the exact expressions

theta2=1203/392-72sqrt2/49,
theta3=221931/89401-160299sqrt3/178802,
theta4=2066283/1065800-3888sqrt2/5329.

Thus all three integrated degree numerators are nonnegative, strictly positive when D>0. The trace-power superadditivity used in (P1) is elementary for these integer degrees: expand Tr(U+V)^n. For n2 and n3 every mixed cyclic trace is nonnegative. For n4 the mixed terms are 4Tr U^3V+4Tr UV^3+4Tr U^2V^2+2Tr UVUV, all nonnegative for PSD U,V. No operator-power order is assumed.

## Whole value, singular limits, equality

The finite collection of positive log series is absolutely summable after integration (each equals a finite entropy difference). Hence regrouping into degree1, degrees2–4 and degrees>=5 is legitimate. All three groups are nonnegative. Degree1 is strictly positive whenever S(Q1+Q2) is nonzero. Conversely if S(Q1+Q2)=0, the success and reset logical supports are orthogonal, all overlaps vanish and Delta=0. Continuity and the resolvent dominated bounds remove faithfulness. This proves the claimed whole value and equality; the exact fixed-K theorem application and actual source interface have now been independently received.

Dependencies: pure_physical_mixed_logical_reset_value_theorem.md; flat_rank_two_integrated_resolvent_reciprocal_proof.md; rank_two_physical_block_reset_three_degree_reduction.md. The primary external convexity theorem is Haonan Zhang, arXiv:1811.01205v2, Theorem1.1(2), https://arxiv.org/pdf/1811.01205 . No reset-mixture concavity is invoked.

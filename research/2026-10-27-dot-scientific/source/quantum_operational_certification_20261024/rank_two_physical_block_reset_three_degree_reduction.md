# Arbitrary two-physical-block reset: exact reduction to three integrated degrees

Historical interface status: the remaining three degrees are now paid in two_physical_block_mixed_reset_value_theorem.md, independently received by two_physical_block_reset_independent_audit.md. The exact reduction below remains useful.

Take E(rho)=p rho tensor sigma+q Tr(rho)tau, where tau=|1><1| tensor T1+|2><2| tensor T2, T1,T2>=0 and Tr(T1+T2)=1. They need not commute with each other or sigma. This includes any rank-two physical product reset omega tensor eta, but also correlated physically block-diagonal resets. Set S=p sigma/3, Qi=q Ti/3. Denote P_X(s)=X(X+sI)^(-1).

## Actual-source expansion

The input success/noise Gram overlap has two blocks with overlap amplitudes 1/sqrt3. The reference has two full-overlap blocks; output antisymmetric pair12 sees both noise blocks with amplitude1/sqrt2, and the other two pairs each see a single block with that same amplitude. The resulting exact entropy log-degree n contribution is the integral of

1/n {3^(-n) Tr[(P_(3S)(P_Q1+P_Q2))^n]
     +sum_i Tr[(P_S P_(3Qi))^n]
     -2^(1-n)[Tr[(P_S(P_Q1+P_Q2))^n]+sum_i Tr[(P_S P_Qi)^n]]}.     (1)

All traces mean positive-sandwich trace powers. Resolvent log series converge to the entropy terms; the finite collection of positive series permits regrouping.

For n=1 the integrated expression is the sum over i of the received pure-physical linear payment K(S,Qi). Therefore it is nonnegative and strictly positive if S(Q1+Q2) is nonzero.

## All n>=5 are pointwise paid

Put J=Tr[(P_S(P_Q1+P_Q2))^n], C=sum_i Tr[(P_S P_Qi)^n]. Positive-sandwich monotonicity gives the first positive trace in (1) at least J, and the reference sum at least C. Convexity of Tr X^n for PSD X gives J<=2^(n-1)C. Since 3^(-n)-2^(1-n)<0, the numerator of (1) is at least

[3^(-n)-2^(1-n)]J+[1-2^(1-n)]C
 >=[2^(n-1)/3^n-2^(1-n)]C >=0  for n>=5.

No commutation or scalar spectral-pair averaging was used.

## Exact remaining target

At the time of this reduction, only integrated n=2,3,4 remained unpaid. When Q1=Q2, the newly received reciprocal-rescaling proof pays them and gives the flat-rank-two physical reset theorem. For unequal or noncommuting Q1,Q2, that two-argument reciprocal result does not automatically apply to the sum P_Q1+P_Q2. The subsequent proof establishes positivity of all three integrals in (1) via a summed-bath reciprocal lemma and two complementary bounds on the same positive resource. No claim follows from convex mixing of reset blocks.

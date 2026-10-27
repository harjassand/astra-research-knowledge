# Independent audit: summed-bath reciprocal lemma and two-payment closure

Date: 2026-10-26. Reviewer: derive_integrated_resolvent_scaling.

## Verdict

PASS for the fixed-K summed-bath reciprocal lemma, the n=2,3,4 trace inequalities, both complementary payments, and the exact constants in `two_physical_block_mixed_reset_value_theorem.md`. This audit does not independently rederive the physical source identity; the whole-source reviewer handles that separate dependency.

## 1. Exact fixed-K representation, including orientation

For faithful inputs let

    P=(I+ut S^-1)^-1,
    Ri=(I+vt Qi^-1)^-1,
    A=diag(P^-1,P^-1), B=diag(R1^-1,R2^-1),
    K=[[I,I],[0,0]].

Then

    K* A^-1 K = [[P,P],[P,P]],
    B^-1/2 K* A^-1 K B^-1/2 = L*L,
    L=[P^1/2 R1^1/2, P^1/2 R2^1/2],
    LL*=P^1/2(R1+R2)P^1/2.

The matrices L*L and LL* have identical nonzero spectra; the former merely has extra zero eigenvalues. Therefore their n-th power traces agree for every n>0. This precisely represents the desired summed-bath integrand, with no commutativity assumption.

The external theorem is Zhang, arXiv:1811.01205v2, Theorem 1.1(2), verified at https://arxiv.org/pdf/1811.01205, PDF page 3. Set p=q=-1, s=n>0. Although its stated K is invertible, take fixed invertible

    K_epsilon=[[I,I],[0,epsilon I]]

and pass epsilon to zero in the finite-dimensional positive trace powers. Pointwise limits preserve convexity. Thus the integrand is jointly convex in (u,v) for the desired singular K. No inverse of K is used in the extension and no integrated uniform bound for K_epsilon is necessary.

## 2. Integration and reciprocal concavity

For n>1/2, integrate the jointly convex integrand over t>0 to obtain

    F(u,v)=J_n(S/u;Q1/v,Q2/v).

It is finite and has F(cu,cv)=F(u,v)/c by t -> ct. The normalization argument in `flat_rank_two_integrated_resolvent_reciprocal_proof.md` proves that 1/F is concave. Consequently

    C/A+C/B <=4/3,
    C=J_n(S;Q1,Q2), A=J_n(3S;Q1,Q2), B=J_n(S;3Q1,3Q2).

This is not a generic assertion that sums of reciprocal-concave functions retain reciprocal concavity. The fixed-K trace representation is essential.

For singular inputs regularize S,Qi by adding epsilon I. With epsilon<=1 the integrand is bounded by

    d * min(2, (||S||+1)(||Q1||+||Q2||+2)/t^2)^n,

which is integrable for n>1/2. This proves convergence by dominated convergence. State the inequality as 3C(A+B)<=4AB when denominators may vanish. C=0 iff S(Q1+Q2)=0; in that case A=B=0 as well. If one Qi alone has zero overlap, the ordinary single-bath payment remains valid by continuity rather than division by zero.

The same fixed-K construction works for any finite number of baths by using a block row of identity matrices and otherwise zero K blocks. This observation is only a mathematical lemma; no physical source theorem beyond the audited two-bath setup is inferred.

## 3. Trace-power comparisons

For U,V PSD and n=2,3,4:

    Tr(U+V)^n >=Tr U^n+Tr V^n,
    Tr(U+V)^n <=2^(n-1)(Tr U^n+Tr V^n).

The first follows by word expansion: n=2 has 2Tr UV; n=3 has 3Tr U^2V+3Tr UV^2; n=4 has

    4Tr U^3V+4Tr UV^3+4Tr U^2V^2+2Tr UVUV.

All are nonnegative: traces of products of two PSD matrices are nonnegative, and Tr UVUV=Tr[(U^1/2 V U^1/2)^2]>=0. The second follows from convexity of the positive trace-power functional (or the Schatten n-norm triangle inequality followed by scalar convexity). Apply these to Ui=P_S^1/2 P_Qi P_S^1/2, with the appropriate scaled arguments, then integrate. Thus both A>=sum_i I_n(3S,Qi) and B<=k b are valid with k=2^(n-1).

## 4. Same-resource combination and exact constants

Use author's notation alpha=3^-n, beta=2^(1-n), c=sum_i I_n(S,Qi), b=sum_i I_n(S,3Qi), D=alpha A+b.

Ordinary reciprocal payment applied separately gives

    D>=K1 c, K1=(3/4)(sqrt(alpha)+1)^2.

The summed-bath reciprocal lemma and B<=k b give

    D>=alpha A+B/k>=K2 C,
    K2=(3/4)(sqrt(alpha)+1/sqrt(k))^2.

Both bounds concern the same D; using c<=D/K1 and C<=D/K2 is therefore legitimate:

    beta(C+c)<=theta_n D,
    theta_n=beta(1/K1+1/K2).

Independent symbolic recomputation exactly reproduced

    theta2=1203/392-72sqrt(2)/49,
    theta3=221931/89401-160299sqrt(3)/178802,
    theta4=2066283/1065800-3888sqrt(2)/5329.

Their approximate values (diagnostic only) are .990849459370146, .929609219122362, and .906915494369189. The author's rational bounds follow by substituting sqrt(2)>7071/5000 and sqrt(3)>433/250, whose squares are strictly below 2 and 3 respectively. Each resulting upper bound is strictly below 1. Hence

    D-beta(C+c)>=(1-theta_n)D>=0

for n=2,3,4, strictly positive whenever D>0. No logical-bath commutativity is used anywhere in this audit.

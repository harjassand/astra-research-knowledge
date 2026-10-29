# Exact conditional label retention for independent pure preparations

30 October 2026. C construction. Root independently extended the projector mechanism to arbitrary mixed preparations; that stronger theorem and its ownership are separate. This file proves the pure-frame theorem and its actual same-source certificate.

## 1. The operation

Let tau_i=|psi_i><psi_i| be n>=2 normalized pure preparations and I_cl the classical identity experiment on the same n labels. Define

    C_rev = inf{c>=0: J_Icl(rho,sigma)<=c J_tau(rho,sigma)
                       for every finite quantum reference and admitted pair}.

J is the SUBTRACTED/conditional Umegaki quantity throughout. In particular references may change between hypotheses. Then

    C_rev = max_i (G^{-1})_ii,        if the psi_i are linearly independent,
            infinity,               otherwise,                         (2)

where G_ij=<psi_i|psi_j>. The same constant is attained as a supremum by scalar-reference faithful classical input pairs. Thus equal-reference and conditional coefficients coincide in THIS class by the explicit proof, not by importing the earlier classical-output theorem.

This gives an exact finite matrix operation on a supplied pure experiment. It is NOT a quantum state-recovery map, a guessing success probability, a capacity or a robust physical preparation claim.

## 2. Dual-projector receiver

Assume independence and compress output to span{psi_i}. There are unique reciprocal vectors phi_i with <phi_i|psi_j>=delta_ij. Put P_i=|phi_i><phi_i| and d_i=||phi_i||^2=(G^{-1})_ii. On HS(out), define T(X)_i=Tr(P_i X). Exact multiplication gives

    T|tau_j>=e_j,
    [T L_tau_j T^*]_ik=Tr(P_i tau_j P_k)=delta_ij delta_kj d_j,
    [T R_tau_j T^*]_ik=Tr(P_i P_k tau_j)=delta_ij delta_kj d_j. (3)

There are no omitted off-diagonal terms: if i!=j or k!=j, the appropriate reciprocal vector annihilates psi_j. For arbitrary two-family effects from BKM_BRIDGE.md, Q_i=E_i^L+E_i^R,

    (T tensor I) W_tau (T^* tensor I)=diag(d_i Q_i),
    (T tensor I)b_tau(u)=(u_1,...,u_n).

The inverse quadratic Cauchy inequality, valid for ANY linear T and W>0, gives

    F_tau^(2)(E,u) >= sum_i (1/d_i)<u_i,Q_i^{-1}u_i>
                   >= (1/dmax) F_Icl(Q,u).                 (4)

One proof minimizes x^*W^{-1}x subject to Tx fixed, or applies the Schur complement to the Gram block(W,x;x^*,x^*W^{-1}x) after congruence. It needs no trace-preservation or positive-operator-map property of T. Equations(1)-(4) in the BKM bridge imply J_tau>=(1/dmax)J_Icl even for unequal reference marginals. This resolves the marginal-subtraction gate rather than merely lower-bounding uncentered D.

For rational prepared-state matrices the receiver can be constructed WITHOUT phase-gauge vectors: S=sum_i tau_i and P_i=S^+ tau_i S^+ on the output support. P_i and d_i=Tr P_i are exact rational matrices/numbers. State purity, rank(S)=n and all identities in(3) are finite exact algebraic checks. Ordinary rational Gaussian elimination/pseudoinverse on a supplied support pays the construction; no optimizer or unknown reference state is needed.

## 3. Sharpness and dependence obstruction

Fix i and let omega be any strictly positive mixture of the OTHER preparations. Write P for the projection onto ker omega inside the full output support, and r_i=Tr(tau_i P). For an independent pure family, ker omega is the reciprocal direction, P=P_i/d_i and r_i=1/d_i. Set input probabilities

    q_i=t, q_j=(1-t)/(n-1),
    p_i=1-t^2, p_j=t^2/(n-1), j!=i, 0<t<1.

Both are faithful. Their classical relative entropy is log(1/t)+O(1). The reference is scalar, hence its subtracted term is zero. The reference output is sigma_t=t tau_i+(1-t)omega. On P it has small eigenvalues of order t, with spectral projection P+O(t); its other eigenvalues stay bounded away from zero. More explicitly P tau_i P is positive on P, since a vector in ker omega also annihilated by tau_i would be in the kernel of the TOTAL support. A block Schur complement or elementary separated-spectral perturbation gives

    log sigma_t=(log t)P+O(1)

in operator norm; the O(t) spectral-projection change times log t is bounded. The first hypothesis tends to tau_i and has bounded entropy. Its expectation of P tends to r_i, so D_tau(p||q)=r_i log(1/t)+O(1). The ratio tends to d_i. Maximizing i proves sharpness of(4).

If the pure vectors are dependent, some psi_i lies in the span of the others. Then r_i=0 and omega is positive definite on the total support. D_tau(p||q) stays bounded as t decreases, while classical D diverges. If the limiting output divergence vanishes, the reverse ratio still diverges or its denominator is already zero; a nonconstant alternative other-label mixture can be chosen unless the channel is constant. Constant preparations directly give J_tau=0<J_Icl. Thus no finite coefficient exists.

## 4. Explicit rational Choi certificate on SAME0,+

For tau0=|0><0|,tau1=|+><+|,

    P0=[[1,-1],[-1,1]],  P1=[[0,0],[0,2]],  d0=d1=2,
    T=[[1,-1,-1,1],[0,0,0,2]],

using column vectorization. In the order9 source pencil, let Z be the9-by3 matrix whose HS4-by2 block is T^T, whose bottom-right entry is2, and whose other entries vanish. Then EVERY constant/symmetric/skew coefficient obeys

    B_Icl,c=2(x) = (1/2) Z^T A_tau(x) Z.

This is one Kraus with V=Z/sqrt2. Its27-by27 Choi matrix is the EXACT RATIONAL rank-one PSD matrix (vecZ)(vecZ)^T/2; no PSD remainder is needed. certify_two_family.py rebuilds all source/target coefficient matrices and checks the equality. The numerical solver result is not a proof premise.

More generally let c=dmax and use the arrow Kraus with top T^*/sqrt c and bottom sqrt c. It contributes diag(d_i Q_i/c) on the target top, the exact target U off-diagonal, and cI on the bottom. Separate source-effect Kraus terms fill each nonnegative deficit (1-d_i/c)Q_i from BOTH left/right effects. All Choi entries are rational whenever T,c are rational, despite the intermediate square roots in a Kraus notation. For COMPLEX rational coefficients the source-first convention is explicitly C_(a,p),(b,q)=conjugate(Z_ap) Z_bq/c, namely vec(conjugate Z)vec(conjugate Z)^*/c, for the arrow matrix Z=c^(1/2)V. This conjugation cannot be omitted; the executed0,+ case is real. This gives an explicit finite CP certificate rather than an uncut SOS hierarchy.

## 5. Strong ordinary comparator

Unambiguous discrimination is established prior, with Chefles1998 SectionII giving reciprocal-state operations and SectionIII equal-success optimization. It has the SAME qualitative independence condition. A uniform-success heralded inverse has probability at most lambda_min(G), so instrument DPI gives the ordinary upper C_rev<=1/lambda_min(G). For0,+ this is2+sqrt2, while(2) is exactly2. The improvement is an entropy comparison coefficient, NOT a better heralded physical inverse: T in(3) need not be CPTP or one jointly normalized POVM. No simulation or decision-order improvement is inferred.

Matsumoto's RLD/reverse-estimation framework and standard BKM/complete-order methods are also strong predecessors. The exact quantitative retention formula at full conditional semantics requires a close priority check; no world-priority conclusion is drawn from the targeted search. Root's mixed-state extension may provide the broader operation; arbitrary pairwise CQ comparison/design remains outside this theorem.

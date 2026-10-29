# A correct two-family sufficient receiver for CQ conditional J

30 October 2026. Independently derived by C and root. This is a sufficient receiver; necessity of unrestricted two-family effects is NOT asserted. The exact pure/mixed retention special cases below do not require that necessity.

## 1. Hypotheses and the genuine Hessian

Fix density operators tau_i on output B and compress B to supp(sum_i tau_i). Let A_i>0 be classical-input reference blocks, with sum_i Tr A_i=1. Write M=sum_i A_i and let H_i=H_i^* be tangents with sum_i Tr H_i=0. IMPORTANTLY sum_i H_i need NOT vanish: the reference marginal is allowed to change. Output and marginal are

    Omega_tau=sum_i tau_i tensor A_i,
    H_tau=sum_i tau_i tensor H_i,     H_M=sum_i H_i.

For a positive state Y, the BKM quadratic form is

    g_Y(H)=integral_0^1 <H,[s L_Y+(1-s)R_Y]^{-1}H>_HS ds.

The Hessian of Tr(Omega_tau log Omega_tau)-Tr(M log M) is exactly g_Omega(H_tau)-g_M(H_M). Thus proving an inequality for these conditional Hessians at EVERY faithful base and tangent, then integrating along the affine path between the two input hypotheses with the nonnegative Bregman weight, proves the corresponding inequality for the SUBTRACTED Umegaki quantities J. An inequality only for g_Omega cannot be substituted here: its common-reference part is multiplied by a different constant.

## 2. Exact normalization at a fixed BKM parameter

Fix s in[0,1] and put Z=s L_M+(1-s)R_M on HS(R). It is positive definite, including at the endpoints. Define

    Q_i^L=Z^{-1/2} s L_Ai Z^{-1/2},
    Q_i^R=Z^{-1/2}(1-s) R_Ai Z^{-1/2},
    a_i=Z^{-1/2}|H_i>, v=sum_i a_i,
    Q_i=Q_i^L+Q_i^R, u_i=a_i-Q_i v.

All Q_i^L,Q_i^R are PSD, sum_i Q_i=I, and sum_i u_i=0. On HS(B) tensor HS(R), define

    W_tau=sum_i L_tau_i tensor Q_i^L + R_tau_i tensor Q_i^R,
    b_tau(u)=sum_i |tau_i> tensor u_i.

Column vectorization is fixed: L_tau=I tensor tau and R_tau=tau^T tensor I on HS(B). Tensor factors may be permuted consistently when vectorizing B tensor R. Common congruence by I_HS(B) tensor Z^{-1/2} transforms the output denominator into W_tau and its tangent into b_tau(a).

Let Jv=|I_B> tensor v. Since L_tau_i|I>=R_tau_i|I>=|tau_i> and Tr tau_i=1,

    W_tau Jv=sum_i |tau_i> tensor Q_i v,
    J^* W_tau J=I,
    J^* b_tau(u)=sum_i u_i=0.

Therefore b_tau(a)=b_tau(u)+W_tau Jv and exact expansion gives

    <b_tau(a),W_tau^{-1}b_tau(a)>-||v||^2
       =<b_tau(u),W_tau^{-1}b_tau(u)>.                     (1)

The subtracted ||v||^2 is PRECISELY the marginal BKM integrand, not a guessed score. This proves the required conditional gauge for arbitrary changing reference marginals.

## 3. The sufficient free operation and its unproved converse

For arbitrary PSD effects E_i^L,E_i^R summing jointly to I and arbitrary u_i summing to zero, set F_tau^(2)=<b_tau(u),W_tau^{-1}b_tau(u)> with the same formula. Faithful effects make W positive; all boundary statements use the closed Schur pencil or common-center regularization rather than an inverse on a null support.

If F_K^(2)<=c F_L^(2) universally, then (1), integration in s, and the conditional-Hessian/Bregman argument imply J_K<=c J_L for ALL faithful input hypotheses and every finite reference. No equal-reference assumption has been made. Common faithful mixing extends the result to finite-divergence boundary hypotheses. For each finite D, joint convexity gives limsup of the regularized D at most D, while lower semicontinuity gives liminf at least D; reference and output terms converge separately before taking their finite difference.

The condition uses two UNRESTRICTED effect families. Actual families in Section2 come from left/right multiplication by the SAME A_i and have compatibility before the common congruence. Thus no necessity or general exact CQ comparison theorem follows from the gauge. COUNTEREXAMPLE.md shows that dropping one family instead is false, even strictly inside faithful prepared outputs.

The one-family form is nevertheless a valid LOWER witness family, not an upper characterization. At a supplied Q_i>0 and sum u_i=0, put the reference base blocks sigma_i^eps=(1-eps)Q_i/d direct_sum eps p_i for any positive input prior p, with off-diagonal Hermitian tangent [[0,u_i],[u_i^*,0]]. The outputs have active block(1-eps)W_tau/d, vacuum block eps*sum_i p_i tau_i and off-diagonal Z_tau. Both diagonal blocks are faithful on the compressed support. In their separate eigenbases the BKM divided differences are(log w-log(eps b))/(w-eps b). Dividing by log(1/eps) leaves1/w in every active/vacuum cross entry. Summing the finite matrix entries gives exactly the traced one-family F_tau, up to the same overall factor for both compared channels. First taking the tangent step to zero and then eps to zero realizes its comparison ratio by equal-reference hypotheses. This proves C_one<=C_equal<=C_conditional, while Sections2-3 prove C_conditional<=C_two whenever the two-family bound is finite. Equality between these different coefficients is not granted in general.

## 4. Finite free-pencil certificate

Replace u_i by operators U_i with sum U_i=0, as justified by vector tests. The source unit-ball pencil is

    A_L=diag(E_1^L,...,E_n^L,E_1^R,...,E_n^R)
         direct_sum [[W_L, b_L(U)], [b_L(U)^*,I]],

and the target is B_K,c=[[W_K,b_K(U)],[b_K(U)^*,cI]]. There are4n-3 selfadjoint free variables after eliminating one effect and one U. Source coefficient order is2n+d_L^2+1, target order d_K^2+1. At the center E_i^L=E_i^R=I/(2n),U_i=0, the source constant is positive definite on the compressed support; its HS block is(L_S+R_S)/(2n), S=sum_i tau_i. Source nonconstant coefficient traces vanish, and Tr A0=d_L+2.

The same operator right-normalization and ordinary definite free-linear Farkas lemma as in the frozen classical proof give a finite Choi+PSD-remainder certificate for this SUFFICIENT comparison. Unknown target prepared matrices and c enter AFFINELY; target state PSD/trace constraints are ordinary SDPs. The constant preparation tau_i=I/d_K supplies a strict rational baseline for a positive budget and a known full-support source, and the constant match bounds certificate traces. Complex matrices use complex Hermitian Choi variables or their standard realification; no unsupported real-Choi averaging is imposed on arbitrary complex prepared states.

These observations yield a constructive conservative CQ design operation, not a new generic Positivstellensatz or an exact characterization of physical CQ Umegaki order. The main exact construction of this packet is the retention class in PURE_FRAME_REVERSE.md; root's mixed-state extension is separately owned.

## 5. SAME0,+ target compression

For tau_0=|0><0|,tau_1=|+><+| and classical identity target, target HS space restricts EXACTLY to its diagonal subspace. The source has order9 and the target order3, so Choi order27 suffices. The one numerical solve in two_family_upper.py returned optimal_inaccurate and c~2.000000000044. It is only a proposal, with no independent positivity/fidelity claim. The exact rank-one certificate in certify_two_family.py proves c=2 without trusting or rerunning that solve.

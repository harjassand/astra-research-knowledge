# Every classical channel: complete SLD equals complete and conditional Umegaki

24 October 2026. Mathematical construction proposed by the parent and checked here. External priority is not established. The theorem concerns classical stochastic transmitted channels with arbitrary finite quantum references; it does not assert the corresponding result for general quantum channels.

## Notation

Let K(y|x) be any finite stochastic matrix. A faithful input cq baseline is sigma=direct-sum_x sigma_x, where every sigma_x is positive definite on R=C^r and sum_x Tr sigma_x=1. Let H=direct-sum_x H_x be a Hermitian tangent satisfying sum_x H_x=0. Put sigma_y'=sum_x K(y|x)sigma_x and H_y'=sum_x K(y|x)H_x. Remove identically zero output rows, so every remaining sigma_y' is positive definite.

Write Omega_a=(L_a+R_a)/2 for the SLD arithmetic-mean superoperator on complex Hilbert-Schmidt space HS(R), and g_a^S(h)=<h,Omega_a^-1 h>. The metric is defined on positive subnormalized blocks as well as densities. The complete SLD coefficient C_S(K) is the supremum of

    [sum_y g^S_(sigma_y')(H_y')] / [sum_x g^S_(sigma_x)(H_x)]

over all such finite references, baselines, and nonzero zero-reference tangents.

## The new boundary realization

Fix any admissible sigma,H and any strictly positive probability distribution q_x. On the enlarged quantum reference

    R_tilde = HS(R) direct-sum C|v>,   dimension r^2+1,

define, for 0<epsilon<1,

    Gamma_x(epsilon) = diag((1-epsilon) Omega_(sigma_x)/r, epsilon q_x),
    Z_x = [[0, |H_x>>], [<<H_x|, 0]].

Here |H_x>> is the ordinary complex Hilbert-Schmidt vectorization. Omega_(sigma_x) is a positive definite Hermitian matrix on HS(R), not an operation being physically applied to an unknown state. This is a direct construction of a new state.

Since Tr_HS Omega_a = r Tr a, the direct sum Gamma(epsilon)=direct-sum_x Gamma_x(epsilon) is a faithful density. Every Z_x is Hermitian and traceless, and

    sum_x Z_x = 0,

because sum_x H_x=0. Thus Z has exactly zero reference marginal; it also has zero classical-label marginal blockwise.

Linearity of a -> Omega_a gives exact channel compatibility:

    sum_x K(y|x) Gamma_x(epsilon)
      = diag((1-epsilon) Omega_(sigma_y')/r, epsilon q_y'),
    sum_x K(y|x) Z_x
      = [[0, |H_y'>>], [<<H_y'|,0]],

where q_y'=sum_x K(y|x)q_x>0 on every retained output row.

Let omega_xj>0 be the eigenvalues of Omega_(sigma_x), with h_xj the coordinates of |H_x>> in the corresponding eigenbasis. The exact BKM quadratic form is

    g^B_(Gamma_x(epsilon))(Z_x)
      = 2 sum_j |h_xj|^2
          [log((1-epsilon)omega_xj/r)-log(epsilon q_x)]
          / [(1-epsilon)omega_xj/r-epsilon q_x].

Use the continuous divided-difference value if two arguments coincide. Therefore

    lim_(epsilon -> 0) g^B_(Gamma_x(epsilon))(Z_x)/log(1/epsilon)
      = 2r sum_j |h_xj|^2/omega_xj
      = 2r g^S_(sigma_x)(H_x).

The identical limit holds at the output, with the same factor 2r. There are finitely many blocks, and the nonzero input denominator stays strictly positive. Consequently the complete BKM ratios of this faithful enlarged family converge to the original complete SLD ratio. Taking suprema proves

    C_S(K) <= C_B(K).

This is a ratio realization, not an inference from the pointwise ordering SLD<=BKM.

## From local metrics to actual finite pairs

For every fixed epsilon>0, Gamma(epsilon) is faithful and Z has trace zero. Hence Gamma(epsilon)+t Z is a faithful density for all sufficiently small real t. Its reference marginal equals that of Gamma(epsilon) exactly. Taylor expansion of relative entropy gives its channel relative-entropy ratio tending to the BKM metric ratio as t tends to zero. Equivalently, the balanced ensemble of Gamma(epsilon) +/- t Z has a Holevo ratio tending to that same metric ratio. Both reference and classical-label marginals are independent of the balanced label.

The order of limits is legitimate and explicit: fix epsilon, take t small enough, then decrease epsilon. The reference dimension r^2+1 is fixed throughout this limit. No singular state is itself used as a finite witness. No resource-efficiency claim follows.

## Equality with conditional Umegaki

The independently checked universal SLD gauge and untouched-reference-qubit integral imply, for every local quantum channel N,

    C_conditional,Umegaki(N) <= C_S(N).

For completeness, the two identities used there are:

1. Given arbitrary sigma,H, subtract V=Omega_sigma(I_A tensor L), with L=Omega_(sigma_R)^-1(H_R). Then H0=H-V has zero reference marginal, and the conditional SLD deficit equals g^S_sigma(H0). This gauge commutes with every channel acting only on A.
2. With tau_s=diag(1,s)/(1+s) and X=|0><1|+|1><0| on an untouched reference qubit,

       g^B_sigma(H) = integral_0^infinity
          g^S_(sigma tensor tau_s)(H tensor X) ds/[4(1+s)^2].

Applying the uniform SLD coefficient, integrating, and then integrating along state-pair segments proves the displayed conditional-Umegaki bound. Conversely, equal-reference state pairs are a subset of conditional pairs, so

    C_complete,Umegaki(N) <= C_conditional,Umegaki(N).

For a classical K, the boundary realization above supplies the missing reverse inequality C_S(K)<=C_complete,Umegaki(K). Hence

    C_complete,Umegaki(K)
      = C_conditional,Umegaki(K)
      = C_S(K).

The complete Umegaki coefficient can equivalently be defined through its complete BKM local ratios, by the usual finite-dimensional Hessian integration and infinitesimal-pair argument.

## Restrictions and the genuinely quantum obstruction

The crucial new equality is the exact compatibility of the Liouville lift with scalar stochastic mixing:

    Omega_(sum_x K(y|x)sigma_x) = sum_x K(y|x)Omega_(sigma_x).

For a general quantum transmitted channel N, vectorization of Omega_sigma uses both left and right copies of the transmitted system. N acting on the physical transmitted subsystem does not automatically implement both copies, so this proof cannot be silently generalized by replacing K with N.

A different attempted flag lift writes H=X+X*, where the SLD minimizing factor is X=sigma L/2 and H=(sigma L+L sigma)/2. Its leading boundary BKM cost can realize the SLD input norm, and the output cost has the correct variational inequality. But equal-reference feasibility requires X_R=0, whereas H_R=0 only implies X_R is anti-Hermitian. No repair of that anti-Hermitian marginal obstruction is proved here.

# Complete factor2 for the phase-covariant boundary family
2026-10-29. Separate analytic addendum to the frozen general K=2+sqrt2 construction. Independent receiving review pending. This does not prove complete factor2 for every unital self-compatible qubit channel.

## Binary pinching contraction with arbitrary quantum reference
Let Z be any Hermitian unitary and Delta(rho)=(rho+ZrhoZ)/2. Set Lambda_a=Delta+a(id-Delta), 0<=a<=1. For every finite-dimensional density rho, including any quantum reference on which Z acts trivially,

 D(Lambda_a rho || Delta rho)<=a^2 D(rho||Delta rho).       (P1)

Proof. Put rho0=Delta rho and X=rho-rho0. Then ZXZ=-X, Zrho0Z=rho0, and rho0+/-X are positive. All operators can be restricted to supp(rho0), which contains supp(rho); rho0 is faithful there. Define g(a)=D(rho0+aX||rho0). Since TrX=Tr(X log rho0)=0, logarithm's resolvent formula gives

 g'(a)=-integral_0^infinity Tr[X(rho0+aX+tI)^(-1)]dt.

For B_t=(rho0+tI)^(-1/2) X (rho0+tI)^(-1/2), one has ZB_tZ=-B_t. Its eigenvalues occur in +/- pairs and |B_t|<I for t>0. Expanding (I+aB_t)^(-1), odd traces vanish, yielding

 g'(a)=sum_(k>=1) a^(2k-1) integral Tr(B_t^(2k))dt,
 g(a)=sum_(k>=1) a^(2k)/(2k) integral Tr(B_t^(2k))dt.

Every coefficient is nonnegative. For a<1, the expansions and integration are justified by the resolvent identity and monotone convergence of the nonnegative paired-eigenvalue expressions. The a=1 endpoint follows by continuity/monotone convergence; g(1) is finite on the finite-dimensional support. Therefore a^(2k)<=a^2 gives (P1). There is no scalar Bloch-radius or commuting-reference premise.

Since Delta Lambda_a rho=Delta rho, (P1) is equivalent to

 S(Lambda_a rho)-S(rho)>=(1-a^2)[S(Delta rho)-S(rho)].       (P2)

## Product pinching tensorization for correlated inputs
Let Delta_i be the binary pinching at site i, Lambda_i=Delta_i+a_i(id-Delta_i), and Delta_all=product_i Delta_i. The maps commute across sites and leave Delta_all rho invariant. The exact chain rule is

 F(rho):=D(rho||Delta_all rho)
 =sum_i D(Delta_<i rho || Delta_i Delta_<i rho).

For rho'=product_j Lambda_j(rho), apply DPI for all Lambda_j except Lambda_i to the ith chain term, then (P1) at site i. This bounds that term by a_i^2 D(Delta_<i rho||Delta_i Delta_<i rho). Summing gives

 F(rho')<=a_max^2 F(rho),
 S(rho')-S(rho)>=(1-a_max^2)[S(Delta_all rho)-S(rho)].       (P3)

All steps include arbitrary correlations among sites and arbitrary finite quantum references.

## Application to the phase-covariant stress channel
In Pauli coordinates let Phi_a have multipliers (a,a,a^2). It factors exactly as Lambda_y(a) composed with Lambda_x(a). Therefore its entropy gain is at least that of Lambda_x(a), since the later channel is mixed unitary. For products Phi=product_i Phi_ai, all x-partial-pinching channels can be applied first and all y-partial-pinching channels afterwards. Applying (P3) to the x stage proves

 S((Delta_x,all tensor id)rho)-S(rho)
 <=1/(1-a_max^2)[S((Phi tensor id)rho)-S(rho)].             (P4)

For every a_i<=1/sqrt2 this is complete factor2, independent of system size and reference dimension. The boundary a=1/sqrt2 is the standard symmetric phase-covariant cloner marginal; its local singular values are (1/sqrt2,1/sqrt2,1/2). The factor2 is attained asymptotically by weak input polarization along y (and a product reference), so it cannot be improved for this specified x-dephasing comparator. The proof does not require a cloning realization: (P4) holds for the explicitly factored channel as stated.

The stationary-barycenter actual-prior consequence from the governing manuscript now improves to average EB error<=sqrt(delta), even for correlated ensembles on arbitrarily many sites in this phase-covariant class. For nonstationary barycenters the visible correction remains sqrt(delta+kappa), not sqrt(delta).

## Scope
This addendum resolves the specified noncommuting-auxiliary stress case through a reference-stable operator proof. It does not derive the arbitrary-channel N371 conjecture, remove the stationary-barycenter restriction for the delta-only consequence, or claim historical novelty for binary-pinching contraction/entropy tensorization. Those standard-tool connections require explicit prior comparison before publication.

# Independent receiving review: nonunital direct trace recovery comparator

2026-10-29. Reviewer: review_finite_quantum_sampler. Verdict: PASS for the frozen governing result and biased diagonal-barycenter addendum. The actual-prior numerical supplement was replayed. No unrestricted N371 closure, generic tensorization, arbitrary coherent/correlated-barycenter extension, physical recovery implementation, or historical novelty is accepted.

## Exact scope
Phi_gamma=Ad_X composed with amplitude damping gamma, 1/2<=gamma<1, eta=1-gamma. The comparator is computational dephasing Delta, known independently of the ensemble. For arbitrary finite quantum references, the stationary relative-entropy loss controls T(rho,Delta rho) with coefficient 1/gamma. For a finite actual ensemble whose A barycenter is diagonal sigma_p, the unreferenced average disturbance is at most sqrt(delta)/(1-a_p), where a_p=sqrt(eta p/(gamma+eta p)); uniformly it is at most (2+sqrt(2))sqrt(delta). The complete ensemble statement requires barycenter sigma_p tensor omega_R. These are direct trace bounds, not entropy-gain comparisons.

## Structural premises independently checked
The family is self-compatible. An explicit isometry to A,B,E is |0> -> |000>, |1> -> sqrt(eta)|100>+sqrt(eta)|010>+sqrt(1-2eta)|001>. Its two receiver marginals are amplitude damping gamma. Apply X on A and B. This avoids assuming that every antidegradable channel's relevant extension is supplied operationally.

For any 0<eta<=1/2 the normalized Choi support is span{|01>+sqrt(eta)|10>,|11>}. A general vector in this support has coefficient determinant -sqrt(eta)a^2. Thus its only product ray is |11>. If a positive multiple of a CPTP EB channel were below Phi in CP order, its separable Choi support would lie in this space and hence in that single ray. Its input marginal could not be I/2. Therefore zero positive EB-component weight is a valid premise throughout the family, not just at gamma=1/2. It does not imply absence of any useful EB comparator.

## Pinned primary recovery theorem and normalization
Read Junge–Renner–Sutter–Wilde–Winter, https://arxiv.org/pdf/1509.07127v3 (7 August 2018), Theorem 2.1, Remark 2.2, and stabilization in Remark 2.4. The theorem gives the fidelity remainder for the beta0-weighted average of rotated Petz maps with t/2 modular exponent. The manuscript uses the opposite modular sign; because beta0(t)=pi/[2(cosh(pi t)+1)] is even, this produces exactly the same average. Fidelity is the unsquared trace-root convention, so L>=-2log F implies F^2>=exp(-L). Consequently Fuchs–van de Graaf yields T(rho,Rbar Phi rho)<=sqrt(1-exp(-L))<=sqrt(L), with natural logarithms. There is no missing factor two.

For the product reference state sigma_p tensor omega_R and channel Phi tensor id_R, both unrotated Petz and every modularly rotated Petz map factor as R_t tensor id_R on supp(omega_R). This follows by direct cancellation of the reference density powers and is also the primary stabilization property. If omega_R is singular, restrict to its support; every positive-weight ensemble state has support there when this is its average reference state. For the pointwise stationary theorem one may use omega_R=rho_R. The actual universal A recovery is unchanged by that choice.

## Stationary and biased Petz arithmetic
The fixed state is sigma=diag(eta,1)/(1+eta). Kraus matrices K0=[[0,sqrt(eta)],[1,0]] and K1=diag(0,sqrt(gamma)) satisfy sqrt(sigma) Kj† sigma^(-1/2)=Kj. Thus unrotated Petz equals Phi. Direct action on E01 gives (R_t Phi)(E01)=eta exp(it log eta) E01. Diagonal operators stay diagonal. Its beta0-average has real off-diagonal multiplier z with |z|<=eta.

For sigma_p=diag(p,1-p), 0<p<1, the output state nu=diag(eta(1-p),1-eta(1-p)) is faithful. The actual Petz Kraus operators sqrt(sigma_p) Kj† nu^(-1/2) are trace preserving. Their composition coefficient on E01 is

 a_p = eta sqrt[p(1-p)/(r(1-r))] = sqrt[eta p/(gamma+eta p)].

The rotated coefficient is a_p exp(it theta), with theta=[log(p/(1-p))+log(r/(1-r))]/2=log(a_p). This checks the reversal of E01 under Phi; ignoring that reversal would give the wrong phase. Averaging gives real z and |z|<=a_p. Since a_p<=sqrt(eta)<=1/sqrt(2), the uniform constant is 1/(1-1/sqrt(2))=2+sqrt(2). At the stationary p, a_p=eta, recovering the sharper 1/gamma coefficient.

## Why recovery distance controls the specified comparator
Let O=(id-Ad_Z)/2 acting only on A. It is not claimed CP, but it is trace-norm contractive by the triangle inequality and unitary invariance. It extracts the off-diagonal block: O rho=rho-Delta rho. The recovered composition has no diagonal-to-off-diagonal mixing and multiplies this block by z, so

 O(rho-Rbar Phi rho)=(1-z)O rho.

Thus (1-a_p)T(rho,Delta rho)<=T(rho,Rbar Phi rho)<=sqrt(L_p). This works for operator-valued off-diagonal blocks and arbitrary references. No unrotated-Petz remainder is substituted for the required averaged recovery theorem. No entropy comparator D(rho||Delta rho)<=constant L is needed.

## Actual-prior identity and necessary boundaries
For a fixed reference tau equal to the actual ensemble average, sum_x p_x D(rho_x||tau)=chi(input), and the corresponding output equality holds with Phi(tau). Hence average L_x is EXACTLY the Holevo loss delta. Jensen gives the stated average trace bound without kappa. For a product barycenter, the recovery factorization above makes the same explicit Delta on A valid for the correlated individual states. The priors themselves need not factor.

For a different fixed tau the correct identity is average L_x=delta+[D(bar_rho||tau)-D(Phi bar_rho||Phi tau)], so the extra term cannot be silently dropped. The biased addendum legitimately removes it by choosing the actual diagonal barycenter; it does not justify coherent A barycenters or correlated AR barycenters, whose Petz map need not preserve this scalar off-diagonal action. At p=0 or 1, positivity forces every ensemble state's A marginal into the same one-dimensional computational subspace; the A dephasing disturbance is zero. In the referenced case the reference states may still differ, so one need not claim the full AR states coincide.

On AR, Delta tensor id_R is only a local dephasing comparator; it is not EB on the entire AR input-output bipartition. The unreferenced A comparator is the advertised ordinary two-outcome EB channel.

## Independent evidence
All three author manifests verified. Replayed 1,500 base state tests, 90 rotated coefficient tests and 180 explicit actual-prior ensembles in the audit folder without modifying originals.

New independent checks symbolically verify general-p Petz TP and a_p^2, and the general-eta unique-product-ray calculation. Independently constructed the ACTUAL beta0-averaged recovered output in 90 pointwise cases, with reference dimensions 1,2,4, pure/full-rank states, gamma in {.5,.7,.99}, and strongly biased p values including .0001 and .9999. Checked positivity/trace, the recovery fidelity remainder, exact off-diagonal action and final trace inequality. The beta0 characteristic function quadrature agrees with theta/sinh(theta) to 5.56e-16; this optional identity is diagnostic, not needed for the bound. No violations appeared. These are symbolic identities plus floating diagnostics, not interval certificates or a physical experiment.

## Significance and unresolved work
This is a mathematically valid rescue of the desired trace metric for a nonunital family where the EB-minorization route is unavailable and a complete entropy comparator fails. It does not reverse the failure theorem: square-root trace control tolerates the logarithmic entropy activation. The actual implementable comparator is simply Delta; averaged Petz recovery is an analytical witness and need not be acquired or executed. The result is single-noisy-qubit with untouched finite reference; generic many-noisy-qubit tensorization and unrestricted actual-prior reconstruction remain unresolved. Universal recovery itself is established prior art, and no novelty beyond the checked explicit transfer is asserted here.

# Arbitrary complex POVM pairs: restricted PPT and separable orders collapse

24 October 2026. Parent's stronger resource-cone proposal independently verified. The conclusion applies to relative comparisons between TWO measurement channels. It does not replace either channel by quantum identity, and it is unrelated to the unresolved separable Werner–Holevo MI-ratio question.

## Theorem and conventions

Fix two finite POVM channels P,Q on the same quantum signal A, with no reality or antiunitary assumption. Fix either resource class C:

- states PPT across A:R; or
- states separable across A:R.

Allow every finite quantum reference R. For each finite c>=0, the following uniform comparisons are equivalent:

1. **Complete equal-reference Umegaki within C.** For rho,sigma in C with rho_R=sigma_R,

       D(P rho||P sigma) <= c D(Q rho||Q sigma).

2. **Conditional Umegaki within C.** For rho,sigma in C,

       D(P rho||P sigma)-D(rho_R||sigma_R)
          <= c [D(Q rho||Q sigma)-D(rho_R||sigma_R)].

3. **Complete SLD within C.** For every faithful baseline sigma in C and Hermitian H with H_R=0,

       g^S_(P sigma)(P H) <= c g^S_(Q sigma)(Q H).

Identity maps on references are implicit. The SLD statement permits every zero-reference tangent at a faithful resource-boundary baseline; equivalently, first restrict to resource-interior baselines and then take white-noise limits. Output zero effects can be deleted; all other output blocks are faithful for a faithful input. The statements concern pairs with finite displayed entropies; standard common faithful regularization extends the result to finite-relative-entropy boundary pairs. Stating uniform inequalities rather than ratios avoids 0/0 conventions. Infima of valid constants and corresponding reverse inequalities therefore agree as extended-real coefficients.

## 1. Resource interiors and white-noise regularization

For a state sigma in either class, let

    sigma_delta=(1-delta)sigma+delta I_AR/(dr),
    d=dim A, r=dim R, 0<delta<1.

This is faithful and in the interior of the chosen normalized resource set. For PPT, both sigma_delta and its partial transpose are strictly positive. For separability, the maximally mixed state is an interior separable state, so a positive mixture with it is interior. One elementary justification of the latter fact is to take finite affinely spanning sets of local density matrices containing positive and negative small perturbations of local identity. Their product states affinely span the bipartite trace-one Hermitian space, and their strictly positive uniform barycenter is the maximally mixed product state.

Consequently every sufficiently small Hermitian trace-zero perturbation of an interior baseline stays in the resource class. Local tensoring with a faithful auxiliary reference state also preserves interior membership: a white-noise component tensor a positive definite auxiliary state contains a nonzero full white-noise component plus a separable remainder. The analogous PPT assertion follows directly from positive definiteness before and after signal partial transpose.

## 2. The generic-complex Liouville top state preserves the cones

On A tensor R tensor R', with dim R'=r, define

    G_sigma=[sigma_AR tensor I_R'
             +Swap_(R,R')(sigma_AR^(T_R) tensor I_R')Swap_(R,R')]/(2r).

It has trace one. For every complex POVM effect E_i, writing sigma_i=Tr_A(E_i sigma), its output is exactly

    Tr_A(E_i G_sigma)
       =[sigma_i tensor I+I tensor sigma_i^T]/(2r)
       =Omega_(sigma_i)/r.

Here Omega_a=(L_a+R_a)/2 acts on HS(R), identified with R tensor R'. The transpose is partial on R, not full on A,R.

### PPT membership

If sigma is PPT, both summands of G_sigma are positive. Moreover

    G_sigma^(T_A)
       =[sigma^(T_A) tensor I
          +Swap(sigma^T tensor I)Swap]/(2r)

is positive. If sigma is faithful, G_sigma is strictly positive because its first summand is strictly positive; G_sigma^(T_A) is strictly positive because its second summand is strictly positive. Thus the top state is strictly PPT even if the original faithful sigma has a singular partial transpose.

### Separable membership

If sigma=sum_k p_k alpha_k^A tensor beta_k^R is separable, each summand of G_sigma is separable across A:RR': the second term merely replaces beta_k by beta_k^T and swaps reference copies. Hence G_sigma is separable. For sigma_delta as above,

    G_(sigma_delta)=(1-delta)G_sigma+delta I_(A RR')/(d r^2).

This supplies an explicit positive white-noise component and proves interior separability, not just positivity or full rank.

## 3. The full flag baseline and tangent stay in the resource cone

Use the enlarged reference R_tilde=(R tensor R') direct-sum C|vac>. Choose the bottom signal density a0=I_A/d and put

    Gamma_epsilon=diag((1-epsilon)G_(sigma_delta), epsilon I_A/d).

Let the top-to-bottom rectangular operator X have physical blocks X_ab=|H_ab>>, the vectorized R-valued blocks of H. Let Z have reference-offdiagonal blocks X and X*. Then

    Tr_A X=sum_a |H_aa>>=|H_R>>=0,

so Z is Hermitian, traceless, and has zero enlarged-reference marginal.

For PPT, Gamma_epsilon and its signal partial transpose are strictly positive. Since Z and Z^(T_A) are bounded finite matrices, Gamma_epsilon +/- tZ stays PPT and faithful for every sufficiently small t.

For separability, it is important not to infer interior from full rank alone. The top block contains white-noise coefficient (1-epsilon)delta/(d r^2), while the bottom contains coefficient epsilon/d. Choose

    0<kappa<min{(1-epsilon)delta/(d r^2),epsilon/d}.

Then Gamma_epsilon-kappa I_(A R_tilde) is explicitly separable: each block is a sum of the separable remainder already exhibited and a nonnegative product identity block. Thus Gamma_epsilon has a strictly positive GLOBAL white-noise component on the whole top-plus-vacuum space and is interior separable. Therefore sufficiently small +/-tZ perturbations remain separable, including their cross-reference coherences.

## 4. Complete Umegaki within the cone implies SLD within the cone

Under any effect E_i, the lifted baseline and tangent become

    Gamma_i(epsilon)
       =diag((1-epsilon)Omega_(sigma_delta,i)/r, epsilon q_i),
    Z_i=[[0,|H_i>>],[<<H_i|,0]],
    q_i=Tr E_i/d>0.

The familiar finite-dimensional divided-difference calculation gives

    g^B_(P Gamma_epsilon)(P Z)/log(1/epsilon)
       -> 2r g^S_(P sigma_delta)(P H),

and identically for Q. All input pairs Gamma_epsilon +/-tZ used to extract these BKM metrics lie in the chosen resource class and have identical enlarged-reference marginals.

Apply comparison1 to such pairs and first let t tend to zero. Then divide by log(1/epsilon) and let epsilon decrease to zero. This proves comparison3 at sigma_delta. Finally let delta decrease to zero. Faithfulness of the original baseline and nonzero output effects ensures continuity of all SLD metrics, yielding comparison3 for every faithful sigma in the resource class.

The limits are nested, not interchanged. For each delta and epsilon, choose a sufficiently small nonzero t within the corresponding resource-interior ball.

## 5. SLD within the cone implies conditional Umegaki within the cone

Take interior input states rho,sigma in C and their affine segment sigma_u. Convexity preserves the class and its interior. For any Hermitian tangent H, the usual reference score

    L_R=Omega_(sigma_u,R)^-1(H_R)

defines H0=H-Omega_(sigma_u)(I_A tensor L_R), with H0_R=0. The exact SLD gauge at both measurement outputs converts their conditional SLD deficits to the full SLD quadratic forms of their output H0. The baseline stays sigma_u, so comparison3 applies; the gauge need not preserve an arbitrary finite displacement because every tangent is locally feasible at this interior baseline.

The untouched-reference-qubit representation of BKM uses sigma_u tensor tau_s, with faithful tau_s. Such tensoring preserves interior PPT or separability across A:(R tensor qubit). Apply the same gauge and comparison3 there, then integrate in s to obtain the conditional BKM comparison. Integrating along u gives comparison2. Approximate resource-boundary input pairs by common white-noise regularization if needed.

Comparison2 implies comparison1 trivially by restricting to equal-reference pairs. This completes the three-way equivalence.

## 6. Independent check: the saturated-filter necessity stays inside either cone

The universal necessity construction uses

    alpha=sigma tensor tau,
    beta(eta)=[sigma tensor W+eta H tensor L]/Tr W,

where W is faithful on an auxiliary reference, tau is a fixed auxiliary state, and Tr L=0. At an interior resource baseline sigma, sigma tensor W/Tr W is also interior PPT or separable by the faithful local-tensor argument. Hence beta(eta) stays in the resource class for sufficiently small eta of either sign. Alpha remains in the same class; if numerator faithfulness is required, replace tau by its faithful regularization first. The same marginal saturation and resolvent-filter Hessian derivation then applies within the resource class. Boundary baselines follow by white-noise approximation.

Thus no unrestricted entangled input was silently used in the saturated-filter necessity. This check is consistent with the theorem but not needed to bypass its measurement-specific Liouville step.

## Scope

The theorem establishes resource-restricted comparison orders for arbitrary complex POVM PAIRS. It does not establish the unrestricted complete/conditional equality, and it does not establish complete-Umegaki equality for arbitrary quantum-output channel pairs. In particular quantum identity is not a POVM output. It also says nothing by itself about a beta bound on mutual-information ratios.

The existing generic-complex negative lift witness is NPT. The restricted-cone theorem makes that distinction substantive: within separable or PPT preparations, this measurement-order gap cannot occur. Any remaining unrestricted measurement-order separation requires genuinely NPT input preparation, not merely noncommuting separable quantum memory.

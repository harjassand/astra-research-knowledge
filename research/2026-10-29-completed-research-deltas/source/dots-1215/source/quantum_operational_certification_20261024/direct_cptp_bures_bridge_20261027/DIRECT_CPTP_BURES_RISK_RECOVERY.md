# Direct CPTP decoding from Bures-risk tomography

27 October 2026. Standalone completion of `../direct_cptp_bures_risk_recovery_root.md`. This document proves the statistical composition and gives a finite feasible optimization/implementation contract. Representation-theoretic circuit primitives are explicitly imported below; they are not newly proved here. Independent receiving, when completed, is recorded in a separate file.

## Theorem and resource model

Let E:L(C²)→L(Cˢ) be a stationary memoryless CPTP source. A valid integer upper bound R≥1 on its normalized Choi rank is supplied. Put

    ell_opt(E) = min_{D CPTP, Cˢ→C²} [1-F_e(D∘E)],
    F_e(Λ) = <Φ₂|(id⊗Λ)(|Φ₂><Φ₂|)|Φ₂>,
    |Φ₂> = (|00>+|11>)/sqrt(2).

For 0<gamma,epsilon≤1 there is an ordinary-six-input, pre-datum quantum-bank procedure whose **averaged physically implemented** recovered channel has

    ell_alg ≤ (1+gamma) ell_opt(E) + epsilon.                 (T)

For s≥2 set

    k=min(s,2R), r=min(R,k), D=2^ceil(log₂(kr)),
    L_D=log(2D)+1,
    n=ceil[15360 D L_D/(gamma epsilon)], N=6n.                (1)

The source-call cap N is deterministic and includes every calibration output, including any subsequently unused record or bank. It is

    N = O(R² log(2R)/(gamma epsilon)).                       (2)

Known quantum gates, storage and classical bit operations are polynomial in R, 1/(gamma epsilon), and log(s), with the finite-precision allocations below. The payload is one additional independent source output, not included in the calibration count N. All N calibration calls occur before it arrives. A complete bank and that datum participate in one common dimension reduction; the bank is consumed. This is not a reusable classical physical-space decoder, a generic-many-qubit scalability claim, or a practical gate count.

For s=1 the source discards the input; any fixed qubit replacement is optimal with F_e=1/4, so no bank is needed. Below k,D≥2.

## 1. Imported physical primitives, with checked source interfaces

**Joint reduction.** A known CPTP map R_{s→k}^{(M)} obeys, for every isometry W:Cᵏ→Cˢ and every operator X on (Cᵏ)^⊗M,

    R_{s→k}^{(M)}[W^⊗M X (W†)^⊗M]
      = ∫ U^⊗M X (U†)^⊗M dU.                               (3)

It has a poly(M,log(s),log(1/nu)) gate approximation in diamond norm. The arbitrary-operator domain, TP completion, and gate statement are in [Lowe–Tan v2, Theorem 1.1 and Section 5.2](https://arxiv.org/html/2606.23592v2). The paper attributes this universal-decoder primitive to Yoshida–Soeda–Murao (2023), Eq. (22). Equation (3) also holds with any untouched reference, by expansion in reference matrix units.

**Random purification.** A known receiver-local channel maps rho^⊗n, for rank(rho)≤r in dimension k, to a mixture of n copies of a purification in Cᵏ⊗Cʳ. It requires no source environment. Its efficient Schur implementation is supplied by [Pelecanos–Spilecki–Tang–Wright v1, Theorem 1.1 and Section 3.3](https://arxiv.org/html/2511.15806v1). The rank-at-most case is explicit in Lowe–Tan Theorem 3.1; alternatively it follows by continuity of the same finite-dimensional channel from rank-r states. Each homogeneous bank is purified separately; simultaneous purification of different states is neither needed nor asserted.

**Finite design.** The qubit Clifford group is an exact unitary 2-design, and its elements can be selected and compiled efficiently: [Dankert et al.](https://arxiv.org/abs/quant-ph/0606161), [Koenig–Smolin](https://arxiv.org/abs/1406.2170). Only its first two Born-weighted projector moments are used below. Approximate finite-bit seed generation is charged to the implementation budget, rather than declared exactly uniform at fixed random-bit cap.

Local precursor derivations are `../inverse_accuracy_bridge_20261027/exact_clifford_polynomial_gate_recovery.md`, `../inverse_accuracy_bridge_20261027/direct_joint_reduction_oracle_compiler.md`, and the positive-cost lemma in `../multilevel_cost_recovery_20261027/GENERAL_Q_COST_SENSITIVE_RECOVERY.md`. The present proof does **not** import their reflection/phase-kickback processor or their weaker factor-two comparator.

## 2. Exact positive risk for the full CPTP decoder class

Let P_j be the six pure Pauli eigenstates, with j ranging over ±X, ±Y, ±Z. Write rho_j=E(P_j) and b=3/2. For any TP qubit channel Λ, expansion in the Pauli basis gives

    (1/6) Σ_j Tr[P_j Λ(P_j)]
      = 1/2 + (1/12) Σ_{a=X,Y,Z} Tr[a Λ(a)]
      = [2F_e(Λ)+1]/3.                                     (4)

Consequently, for every CPTP decoder D,

    R_rho(D) := (b/6) Σ_j [1-Tr(P_j D(rho_j))]
              = ell(D∘E).                                 (5)

Because D† is positive and unital, its loss effects are

    L_j(D)=b[I-D†(P_j)],  0≤L_j(D)≤bI.                      (6)

For arbitrary estimated densities tau_j, including estimates inconsistent with any TP source, define R_tau(D) by the same formula. It remains a nonnegative risk in [0,b]. It need not be the entanglement loss of a channel, which is immaterial: optimization and transfer only need (6). The six trusted inputs are an exact state 2-design; no signed reconstruction coefficients or accepted-decoder trace-budget restriction occur.

## 3. Uniform Bures square-root-risk transfer

Use root fidelity f(rho,tau)=||sqrt(rho)sqrt(tau)||₁ and set

    delta=(1/6) Σ_j [1-f(rho_j,tau_j)].

For every decoder in the same CPTP feasible set,

    |sqrt(R_rho(D))-sqrt(R_tau(D))| ≤ sqrt(2b delta).         (7)

Proof. Choose Uhlmann purifications u_j,v_j with real overlap f(rho_j,tau_j), so ||u_j-v_j||²=2[1-f(rho_j,tau_j)]. Form the direct sum of (sqrt(L_j(D))⊗I)u_j with weight 1/sqrt(6), and the corresponding v-vector. Their squared norms are the two risks. Their squared distance is at most 2b delta by (6). Reverse triangle inequality proves (7). These purifications are proof objects, not extra source access.

Let Dhat be any feasible eta-optimal estimated-risk decoder, and let D* minimize the true risk. Twice using (7) gives, **pointwise in every estimator record**,

    sqrt(R_rho(Dhat))
      ≤ sqrt(ell_opt)+2sqrt(2b delta)+sqrt(eta).              (8)

The inequality is uniform in D; Dhat may depend on all estimates, and the estimates need not be independent. If E delta≤m, Minkowski in the record probability space yields

    E R_rho(Dhat)
      ≤ [sqrt(ell_opt)+2sqrt(2b m)+sqrt(eta)]².              (9)

Let z=2sqrt(2b m)+sqrt(eta). Young's inequality and 0<gamma≤1 give

    (sqrt(ell_opt)+z)²
       ≤(1+gamma)ell_opt+(1+1/gamma)z²,
    z²≤16b m+2eta,
    1+1/gamma≤2/gamma.

Thus

    E R_rho(Dhat) ≤ (1+gamma)ell_opt +48m/gamma+4eta/gamma.  (10)

The same bound holds without expectation on any event delta≤m. This is why ordinary biased Bures tomography suffices for this **full TP-decoder** problem: weighted Keyl covariance is not the required interface.

## 4. One shared quantum frame, with the correct chronology

A Kraus decomposition with at most R operators shows

    rank E(I₂)≤2R,     rank E(P_j)≤R.

All outputs, including every source-Choi output block, lie in S=supp E(I₂). Extend S to a k-dimensional subspace and mathematically write E=Ad_W∘E₀. The learner is never given W.

Acquire n independent outputs of each P_j and store all six banks unmeasured. On arrival of the independent datum, apply exactly one R_{s→k}^{(6n+1)} to **all banks and the datum**, leaving source labels and the logical reference untouched. By (3), the resulting state is a mixture over a single common U of

    ⊗_{j=1}^6 [E_U(P_j)]^⊗n   ⊗   (id⊗E_U)(payload),
    E_U=Ad_U∘E₀.                                           (11)

At each fixed mathematical U, the banks and datum are independent, and each bank has the iid source distribution required by tomography. Also

    ell_opt(E_U)=ell_opt(E):                                (12)

restrict a physical decoder along W for one direction, and extend a compressed-space decoder by an arbitrary replacement off WW† for the other; conjugation by U preserves the feasible class. These are comparison maps, not an implemented unknown inverse.

Apply the random-purification channel separately to each bank, tomograph it as in Section 5, solve Section 6's finite classical optimization, and apply Dhat to the still-stored compressed datum. The probability of every learner record is independent of the logical datum conditional on U. Therefore the implemented Bell infidelity is the average of R_{rho^U}(Dhat), and (10) applies uniformly in U.

The virtual Haar U need not be sampled, measured, learned or exposed. It is a decomposition of the known joint channel. Separate reductions of programme and datum would lose (11). Measurements and discards **after** joint compression are legitimate: this direct algorithm never reverses them. No retained tomography environment, coherent SDP, SELECT over histories, or controlled unknown operation is required.

## 5. Actual finite-Clifford Bures tomography and confidence

Fix one bank and condition mathematically on its random pure purification Phi=|phi><phi| in Cᵏ⊗Cʳ, padded into dimension D. On each of its n copies choose an independent uniform Clifford V, measure V Phi V† in the computational basis, record outcome j, and define

    P=V†|j><j|V,        X=(D+1)P-I_D.

Born weighting and the exact 2-design identity give

    E P=(I+Phi)/(D+1),    E X=Phi,
    X²=(D²-1)P+I,
    E X²=D I+(D-1)Phi,
    E(X-Phi)²=D I+(D-2)Phi≤2D I,
    ||X-Phi||op≤D+1.                                      (13)

For Xbar=n^-1 Σ_i X_i, matrix Bernstein yields, for 0<t≤1,

    Pr(||Xbar-Phi||op≥t)≤min{1,2D exp[-nt²/(5D)]}.           (14)

Indeed the denominator is at most 4D+(2/3)(D+1)t≤5D for D≥2.

If w is a top vector of Xbar and e=||Xbar-Phi||op≤1/2, its eigenvalue is at least 1-e and projection orthogonal to phi gives

    1-|<w|phi>|² ≤ e²/(1-e)² ≤4e².

For e>1/2, the bound follows from infidelity≤1. The resulting tail bound integrates to

    E[1-|<w|phi>|²]≤min(1,C_D/n),
    C_D=20D[log(2D)+1].                                   (15)

Use finite arithmetic whose **total backward Hermitian error**, including vector normalization/rounding, is at most a and output a top vector of that nearby matrix. This can be done in polynomial arithmetic with no source or empirical eigengap promise. An equivalent certified implementation uses a near-top eigenvalue and residual of size O(a). Replace e by e+a and use

    min(1,4(e+a)²)≤2min(1,4e²)+8a².

Trace out the known purification register; send any padded-block leakage to a fixed k-state via a known CPTP completion. Fidelity monotonicity, and 1-|z|≤1-|z|², show that the estimated density satisfies

    E[1-f(rho,tau)]≤2C_D/n+8a².                            (16)

Finite normalized rational-vector outer products can encode genuine density matrices (normalization divides by a positive rational squared norm); state-coefficient rounding is included in the certified a or separately paid in Section 6, not ignored. Equation (16) is uniform over the purification and outer frame. Taking

    n≥15360 D L_D/(gamma epsilon),
    a²≤gamma epsilon/3072                                  (17)

makes the two terms in (16) at most gamma epsilon/384 each, hence m≤gamma epsilon/192.

### Finite-confidence strengthening

For any 0<m≤1, choose

    t=sqrt(m)/4,   a≤sqrt(m)/4,
    n≥(80D/m) log(12D/beta),    0<beta<1.                   (18)

On e≤t, the total pure infidelity is at most 4(t+a)²≤m, hence mixed root-infidelity is at most m. Equation (14) gives failure at most beta/6 per bank, and the union bound gives all six estimates good with probability at least 1-beta. Independence between the bank estimates is not necessary for this union bound. This statement holds for each fixed virtual U after averaging its purification variables.

Therefore the **ideal common-frame training interface** has, with probability ≥1-beta,

    ell(Dhat∘E_U)≤(1+gamma)ell_opt+48m/gamma+4eta/gamma.       (19)

It is not a bound conditioned on every exposed physical learner record. Averaging good and bad histories adds at most beta, since true Bell loss is at most one. Approximate inner tomography changes the probability of a fixed virtual-frame good event by at most half its unhalved diamond error. Approximate outer reduction is safely transferred at the averaged-channel level; it does not itself export a literal U or justify a physical-record confidence claim. Independent same-frame validation and encoder selection require their own failure/precision accounting. For a target virtual-frame failure beta after finite inner implementation, run (18) with beta/2 and require the total inner learner-record channel discrepancy to be at most beta in unhalved diamond norm. Then total variation adds at most beta/2. Decoder synthesis error is separately allocated at the desired loss scale O(epsilon), not the confidence scale; classical feasibility/objective arithmetic must retain its deterministic eta guarantee. This only increases precision logarithmically in 1/beta. An O(epsilon)-accurate record distribution alone does not preserve an arbitrarily smaller beta.

## 6. Finite feasible decoder SDP and known-matrix synthesis

Use the **unnormalized** Choi matrix C of D, ordered input k then output 2. Define

    H_tau=(b/6) Σ_j tau_j^T ⊗ (I₂-P_j) ≥0.

The exact empirical problem is

    minimize Tr(H_tau C),
    C≥0, Tr_output C=I_k.                                  (20)

Its dual is

    maximize Tr Y,
    H_tau-Y⊗I₂≥0, Y=Y†.                                    (21)

The normalization is important: Tr C=k, not one. Equations (20) and (5) agree exactly. There are explicit strict points C₀=I_k⊗I₂/2 and Y₀=-I_k; ||H_tau||op≤b and Tr H_tau=b. The feasible primal set is compact and has an explicit interior radius in its affine space. Near-optimal duals can be restricted to a polynomial norm bound: Y≤bI, while a lower objective cap bounds its negative eigenvalues. Standard finite-dimensional weak SDP optimization thus has polynomial bit complexity in k, inverse additive accuracy and coefficient bit length. This is a conventional explicit SDP, not an unknown-source optimization oracle.

A floating solver status is insufficient. The output must have certified feasibility and additive optimality. One concrete finite repair avoids any source-state inverse:

1. Obtain a rational Hermitian weak primal Ctilde with lambda_min(Ctilde)≥-kappa, ||Tr_output Ctilde-I||op≤kappa, and an initial primal/dual objective gap at most eta/8; obtain a dual whose negative slack has its own certified bound delta_dual≤eta/(8k).
2. Set T=Tr_output Ctilde-I and C₁=Ctilde-(T⊗I₂)/2. Now Tr_output C₁=I exactly and lambda_min(C₁)≥-3kappa/2.
3. Mix C₂=(1-lambda)C₁+lambda C₀. It has margin at least lambda/2-3kappa/2. Choose kappa≪lambda and lambda=O(eta/b).
4. Round Hermitian entries to operator error e, then repeat the affine correction of step 2. Partial trace over dimension two has operator norm at most two; total perturbation is at most 2e. Choosing 3kappa/2+2e≤lambda/4 gives a strictly positive exactly TP rational C. All objective changes are bounded by b times the operator perturbation (because H_tau≥0, Tr H_tau=b); mixing costs O(b lambda).
5. Shift the near-feasible dual Y downward by delta_dual I; its dual objective decreases by k delta_dual≤eta/8. Certify the final primal/dual gap, including coefficient rounding, at most eta. Decreasing the solver tolerances by explicit polynomial factors makes all these requirements hold. For example lambda=eta/(8b), kappa≤eta/(192b), e≤eta/(128b), initial primal/dual gap≤eta/8, and the separate delta_dual≤eta/(8k) leave ample room below eta. A k-independent dual-slack tolerance would not suffice.

If ||Htilde-H_tau||op≤h, every feasible objective changes by at most kh. Thus allocating h≤eta/(8k) and an additional eta/4 to the two optimization comparisons covers coefficient rounding. Known, uniformly conditioned congruence normalization of the partial trace is an alternative repair, but unnecessary for the rational certificate above.

Factor the final feasible C into at most 2k Kraus operators K_a:Cᵏ→C². Its isometry

    V|v> = Σ_a K_a|v>⊗|a>

has output dimension at most 4k and satisfies V†V=I exactly. A known unitary extension can be approximated by dense linear algebra and finite universal-gate synthesis in polynomial work in k and the requested precision. The positive margin created above supplies a polynomial conditioning bound for this known factorization. Compiled gates implement an actual CPTP decoder; their discrepancy from the ideal C-defined channel is paid below. No unknown state, unknown source inverse, or unbounded history table appears. Learning is genuinely measured and classically processed, so no coherent reversal of optimization is needed.

## 7. Finite-control budget and proof of (T)

Take

    m≤gamma epsilon/192, eta≤gamma epsilon/16.              (22)

Equation (10) then contributes epsilon/4 from tomography and epsilon/4 from decoder optimization. The eigensolver/vector arithmetic in (17), and coefficient/feasibility arithmetic in Section 6, have already been charged to m and eta.

Let nu≤epsilon bound the **total unhalved diamond discrepancy** between the actual finite protocol and the exact-reference protocol whose risks were just bounded. This includes all ordinary probe-preparation errors summed over the N calls, the single joint reduction, the six actual purification channels, any truncated/rounded Clifford randomization, and final known-decoder synthesis. Contractivity and telescoping make their sum a valid nu. The Bell probability changes by at most nu/2 because the compared outputs are normalized states. Thus

    ell_actual≤(1+gamma)ell_opt+epsilon/2+nu/2,

proving (T). Do not double-charge arithmetic already included in m or eta, or omit arithmetic not included there. One may allocate nu over a fixed polynomial gate cap G, and input errors over N preparations; per-operation precision must actually meet these allocations. Classical random-seed generation can be capped and its small failure mass assigned to a fallback Clifford, counting twice its total-variation discrepancy in the unhalved diamond budget nu. This yields a deterministic source cap and polynomial worst-case processing, rather than unbounded rejection sampling hidden in an exact-uniform claim.

Since kr≤2R² and D<2kr≤4R², (1) proves (2). Initial bank storage is N ceil(log₂s) qubits, with polynomial receiver workspace. The common-frame computation starts only after the datum arrives; its memory lifetime and latency have not been optimized. No gate-level noise threshold or laboratory implementation is established here.

For (19), the expected physically implemented conclusion is instead bounded by its right side plus beta+nu/2. If that high-probability route is used to prove a total additive epsilon, its m,eta,beta,nu allocations must sum accordingly; a confidence term is not free. The expected-risk route above already proves (T) without a beta parameter or a log(1/epsilon) copy penalty.

## 8. Scope and nonclaims

- This closes the **polynomial-processing** gap for the stated full-TP qubit comparator by changing the learning objective. It does not assert that a biased tomography estimator satisfies a missing weighted covariance theorem for a smaller accepted-decoder class.
- Positivity is not asserted to be exclusive to TP decoders: accepted CP trace-nonincreasing decoders admit an erasure-aware positive loss too. This theorem does not exploit a small accepted-decoder trace budget, and does not supersede resource advantages of weighted-covariance learners in that different parameter regime.
- Reduced-frame output tomography plus ordinary decoder SDP is the correct conventional comparator. This is not entirely tomography-free, nor environment tomography.
- On exactly reversible E(a)=V(a⊗sigma)V†, ell_opt=0. The previously received Omega(R²/epsilon) worst-case source-copy lower bound is a comparison on its specified reversible family, not newly proved here. The upper exponents match up to log R for fixed gamma.
- R can grow exponentially with physical qubit number. Polynomial dependence on R and on output Hilbert-space dimensions is not generic-noise scalability.
- The complete bank is consumed with one independent datum. The virtual frame is not a reusable classical support estimate, and the theorem gives no later physical-datum decoder reuse.
- Source calls are ordinary labelled pure probes. There is no physical Choi probe, supplied support basis, source environment access, source inversion, spectral floor, omitted postselection cost, or coherent reversal of discarded local work.
- No historical novelty, practical quantum advantage, optimal diamond-error recovery, unknown-rank adaptation, temporal-drift robustness, approximate-support extension, or fixed-record quality theorem is claimed.
- The numerical checks accompanying this proof test finite algebra, SDP certificates and scalar budgets. They do not execute the collective Schur/purification circuit or establish practical costs.

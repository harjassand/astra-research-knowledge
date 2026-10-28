# Independent statistics and global-channel audit: joint local logical recovery

28 October 2026. **PASS under the explicit reset, compatible-local-algebra, relative-margin, global-dominance, and paid-control contracts.** Final source SHA256: `f22c549bcb545387b4761ff31ec90886ff7b677c1d1f32a411b05e65024f89c0`. This is an analytic proof review, not a source simulation or newly acquired experiment. The received one-logical manuscripts and completed pilots are unchanged.

## 1. The per-logical input experiment is a legitimate reuse of the local core

To probe input label i, the actual input is its known X/Z eigenstate with every other logical input maximally mixed. The latter preparation bits and individual uniform-anchor labels are discarded or ignored by the estimators. One must not condition the Bures guarantee on these labels. The other logical subsystems join the proof gauge; no matrix for that enlarged gauge is supplied or reconstructed.

The resulting four state banks have one shared physical marginal rho=E0(I/2^q), with X_(i,j)=B_(i,j)|X_(i,j)| and kappa rho<=|X_(i,j)|<=rho. Each true pair is local on one interval and obeys the same relative-margin argument. This does not require a Y_i acquisition margin, positivity of every single-logical Pauli contraction, or a single-logical noisy-source oracle claim. Only the coarse locator, local CPTP empirical-risk estimator, comparison tournament, and their physicality/confidence guarantees are imported.

For each local channel D_i, its two-axis excess r_i is nonnegative and satisfies (kappa/2)ell0_i<=r_i<=ell0_i. The ERM result r_min<=20m/kappa+2zeta, with zeta<=m and m=kappa^2 eta/256, implies

    r_min <=(22/256) kappa eta < kappa eta/8.

With t=kappa eta/(4h^2), the received comparison cap is exactly ceil[512L/(kappa t)]=ceil[2048h^2L/(kappa^2 eta)]. The tournament then gives

    r_selected <=(2*22/256+1/4) kappa eta
                =(27/64) kappa eta < kappa eta/2,
    ell0_i <=2r_selected/kappa < eta.

For R_max=1, comparisons and their undefined logarithm/height formulas are skipped; the lone good candidate already suffices. All candidate channels are exactly CPTP even on statistical bad histories. Their later use is to supply known local pullbacks, not to be naively deployed in sequence.

The coarse and fine colored-bank experiments retain the received same-output correlated-marginal contract. Fresh fine banks are conditional on the completed coarse record; fresh comparison banks are conditional on prior contenders and controls. The conditional failure bounds remain uniform on arbitrary preceding histories. Thus the union bound costs at most q(beta_0+beta_A+beta_Q)+beta_C, without independence assumptions among modules or successes. A fully positive explicit choice is beta_0=beta_A=beta_Q=epsilon/(32q) and beta_C=epsilon/32, totaling epsilon/8. There is no uncharged empirical support test or failure postselection.

## 2. Weighted sign rounding is valid without a spectral floor

For the actual single-logical channel obtained by holding the other inputs maximally mixed, each Bloch diagonal obeys 1-t_jj<=2ell0_i. Its known pullback A_j=D_i†(sigma_j) is a Hermitian contraction. Hence

    a_j=Tr rho(A_j-B_j)^2 <=2(1-t_jj)<=4eta.

The true B_j commutes with rho. In a common eigenbasis of rho and B_j, and an eigenbasis of any Hermitian C_j, each opposite-sign overlap has |b-c|>=1 for b=±1. Its contribution to the squared reflection error is four, bounded by four times (b-c)^2. Summing nonnegative rho-weighted overlaps proves

    Tr rho(B_j-sign C_j)^2 <=4Tr rho(B_j-C_j)^2.

This remains valid for a data-dependent C_j, arbitrary signs on its kernel, and degeneracies. It requires neither [C_j,rho]=0 nor forward eigenvector stability. At the prescribed total operator residual ||C_j-A_j||<=sqrt(eta)/2, weighted Hilbert–Schmidt triangle inequality gives

    delta_j <=4(sqrt(a_j)+sqrt(eta)/2)^2 <=25eta.

These are actual exact-reference reflections built from a finite backward representation. The bound does not declare floating eigenvectors exact or assume a source eigenvalue floor. Their universal-gate implementation discrepancy is paid separately in the one whole-process budget.

## 3. The reversible receiver gives a joint, not marginal, guarantee

The three gates C_Z(B'_Zi), C_X(B'_Xi), C_Z(B'_Zi) are unitary for arbitrary learned reflections. With the true logical generators they are the ordinary three-CNOT SWAP of logical i and its receiver ancilla. Distinct true generators are compatible under the same U, but learned generators need not anticommute within a pair or commute across pairs. No such learned compatibility is used in the proof.

Preparing ALL receiver output ancillas in I/2 is essential to this particular polynomial-error argument. In the global Bell experiment, the reduced state on the full physical register and all receiver ancillas is

    rho_PA=(U tensor I_A)[I_(L,A)/2^(2q) tensor Gbar](U† tensor I_A).

Every ideal elementary gate acts unitarily on the logical-plus-ancilla factors and trivially on the gauge, so EVERY ideal elementary prefix leaves exactly this rho_PA invariant. The full reference R, gauge purification E, and ancilla purifications S stay in the proof. This is an unconditioned marginal identity, not a claim about fixed coin labels, arbitrary payload marginals, or actual imperfect prefixes. Pure reset ancillas would not give this same invariant marginal and could make a naive weighted-state hybrid invalid.

For one C_Z replacement, the difference operator is (B'_Z-B_Z) tensor (I-X_A)/2. Its squared norm on that invariant marginal is delta_Z/2. The C_X replacement similarly has squared norm delta_X/2. Therefore the three replacements for each logical index contribute delta_Z, delta_X/2 in total squared-error sum.

Telescoping the complete product with ideal prefixes and actual suffixes is the correct hybrid order: each actual suffix preserves vector norm, and each individual error is evaluated in the known invariant ideal marginal. Cauchy–Schwarz over the 3q elementary errors gives

    ||psi_actual-psi_ideal||^2
       <=3q sum_i(delta_Zi+delta_Xi/2)
       <=(225/2) q^2 eta.

The ideal final pure state contains the FULL maximally entangled state on R:A as a tensor factor. Projecting onto its orthogonal complement kills the ideal vector, so the actual global Bell loss is at most this squared vector distance. Tracing physical registers and proof purifications does not change that Bell-success probability. This proves the stated joint entanglement-fidelity guarantee, including coherence across the logical block. It is not a product of separate marginal fidelities or an assumption of independent learned errors.

The procedure must retain the physical register until all swaps finish. Applying the acquired CPTP maps D_i themselves sequentially, with their discarded registers, would not have this proof and is expressly not the deployed method.

## 4. The global oracle needs the separate dominance promise

The proof-only gauge POVM representation of a joint decoder gives F_e(D E_x)=sum_alpha Tr G_alpha(x) T_alpha, with T_alpha>=0 and sum T_alpha=I. The explicitly separate condition G_I>=G_alpha for all global Pauli labels makes identity correction optimal among ALL CPTP decoders. Its excess loss obeys

    ell(D E_x)-ell_star(x)
       <=Tr G(x)(I-T_I)<=4ell0_joint,

because every positive scalar pairing of the four-coordinate quadratic G(x) is bounded by its coefficient trace, giving G(x)<=4Gbar. No learner enumerates the 4^q proof labels.

The retained q=4 example is a valid counterexample to inferring dominance from local margins: probabilities 1/10 on I, 3/10 on XXXX, and 3/20 on each of four single-X errors sum to one; every X_i contrast is one and every Z_i contrast is 1/10, although XXXX is the better correction. Thus the source contract genuinely distinguishes acquisition of the ideal logical algebra from globally optimal correction of the noisy joint source.

At eta=epsilon/(16384q^2), the uniform noisy-source regret is at most

    450q^2 eta=(225/8192)epsilon < epsilon/20.

Without global dominance the joint extraction guarantee for E0 remains valid, but the unrestricted noisy-source comparison does not follow. The manuscript states this boundary correctly.

## 5. The encoder observations are genuinely global ordinary Bernoulli tests

After freezing the entire joint decoder, sample a known uniform global q-qubit Clifford C, prepare C|0^q>, and test the decoded output by C† followed by the all-zero readout event. The input may be entangled INSIDE the q-qubit input block, but no protected reference is retained through the source. One trial returns one Bernoulli error bit for a joint rank-one projector, not q independently scored marginal errors.

Here is a self-contained two-design derivation. Let d=2^q, and expand a sampled pure state pi=(I+sum_(P!=I) r_P P)/d in Hermitian Pauli operators. Random Pauli signs force E r_P=0 and E r_P r_Q=0 for P!=Q. Clifford transitivity makes every E r_P^2 equal. Purity gives sum_(P!=I)r_P^2=d-1, so E r_P^2=(d-1)/(d^2-1)=1/(d+1). The Pauli expansion of Swap then gives

    E(pi tensor pi)=(I+Swap)/(d(d+1)).

For ANY TP joint channel T, including nonunital channels, this identity implies F_avg=(d F_e(T)+1)/(d+1). Consequently the actual joint-test error mean is

    e_D(x)=d/(d+1) * ell(D E_x).

This conversion has no exponential signal suppression. Product single-qubit six-state ensembles do not replace this global two-design identity. The manuscript appropriately disclaims the global qualification/fast encoder theorem under a product-only logical-input/readout interface.

Because x still has only four real coordinates, this mean is a nonnegative ten-feature quadratic for the ACTUAL frozen joint channel on every training history. Its Bernoulli variance is at most its mean. The received active design at epsilon_e=epsilon/8 yields additive Bell loss at most (d+1)epsilon_e/d<=2epsilon_e=epsilon/4. Combining uniform decoder regret <=epsilon/20 with gamma<=1 gives at most (1+gamma)ell_star+7epsilon/20 on the joint good event. The displayed J, b and N_count are the received formulas with epsilon_e substituted; no exponential d factor enters their source count.

Uniform Clifford sampling and realization are real controls. The stated recursive uniform ordered symplectic-basis sampler is valid: at each nondegenerate complementary space choose a uniform nonzero vector and a uniform partner in its symplectic-product-one affine hyperplane, then recurse on the orthogonal complement. Every ordered symplectic basis has the same probability. A uniformly chosen Pauli sign vector completes the uniform Clifford distribution modulo irrelevant global phase. Partners can be drawn by finite linear algebra with no rejection. Nonzero draws have failure probability at most 1/4 per attempt. Across at most q*N_count such draws, a predetermined retry cap can bound total sampling discrepancy inside nu, with a fixed fallback on truncated histories. Clifford compilation, routing, seeds, input gates and inverse-output measurement gates are not free. Truncation affects the actual process budget, not the exact ideal two-design identity.

## 6. Finite full cap and operational boundary

The cap

    q[2cN0+4c1N1+(R_max-1)Npair]+N_count+1

is deterministic on every history, with the comparison term zero for R_max=1. All logical modules use separately charged source calls; colored sharing is only within each prescribed disjoint-patch bank. The final one is an actual payload use. Fine and selection costs scale as q^3/epsilon because eta is proportional to epsilon/q^2; this amplification is explicit, not hidden in a confidence parameter.

These are block-source calls: q logical input-qubit uses and n physical output-qubit exposures occur per call, plus supplied selector/control registers. Only N_count+1 invocations deploy the complete joint decoder; local acquisition/comparison has its own separate controls. Each joint invocation retains n+q data qubits and uses 3q controlled width-w reflections, 4q ancilla Hadamards and q maximally mixed ancilla preparations. The concrete end-block routing witness costs at most 2(n+q) SWAPs per logical index while restoring labeled physical and earlier-output positions. Collective Bures memory, cross-copy routing and global Clifford preparation/readout remain additional paid controls.

Adding bounded-loss statistical failures of total at most epsilon/8 and linked whole-process discrepancy nu<=epsilon/8 to the good-event additive 7epsilon/20 gives at most 3epsilon/5, hence the claimed epsilon with slack. The high-probability reference-process statement should not be confused with a per-transcript or per-key guarantee for the actual imperfect process.

Global Bell loss is not itself a dimension-free untwirled diamond guarantee. The stated bound min(2,2d sqrt(ell)) follows from normalized-Choi trace distance and the general d factor. The optional whole-q Pauli twirl is a changed averaged service: it costs coordinated 2q key bits and Pauli controls, discards the key, preserves Bell loss, and yields a possibly correlated global Pauli channel with unhalved diamond error exactly 2ell. No independence of logical Pauli errors or exported-key guarantee is asserted.

An equally informed conventional learner receives the same tomography/ERM, spectral comparisons, reversible swaps and global Clifford testing. This audit establishes no advantage over that learner, historical priority, new experiment, arbitrary-noise theorem, or fault-tolerant device claim. No source/private parameters were read, no source sampler was executed, and no previous artifact was modified. The companion receipt binds this analytic review and its received imports.

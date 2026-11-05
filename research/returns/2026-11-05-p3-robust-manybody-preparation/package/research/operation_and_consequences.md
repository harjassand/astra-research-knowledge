# Preparation of one-dimensional quantum Gibbs states through fixed local noise

Research construction, 5 November 2026. This note composes the new robust-block theorem with the already accepted noisy Bell/tree boundary compiler. It does not reprove or extend the accepted compiler, passive bath, memory, syndrome sampler, TFD, or input/output theorems. All trace distances are D(rho,sigma)=||rho-sigma||_1/2. Diamond norms in the inverse-radius inequalities are the full diamond norm.

## 1. Selected scientific question and resolution

For a digitally specified finite-range one-dimensional quantum Hamiltonian at any fixed positive temperature, can a physical apparatus with a fixed nonzero component error rate deliver the unencoded Gibbs state to arbitrarily small global trace distance, rather than leave an error proportional to the number of output qubits?

The answer is affirmative in the accepted independent-Pauli noisy-control model, with a temperature- and range-dependent component threshold. The central new mathematical operation is a constructive decomposition into bounded contiguous mixed blocks with a uniform spectral floor. This supplies positive local inverse inputs even when the smallest eigenvalue of the full Gibbs state is exponentially small in chain length. The physical implementation prepares those inputs with the accepted protected controller and exports through its acquired product boundary. Its precision is statistical and computational; physical primitive noise stays fixed.

The theorem is broad but its sufficient constants are unusably large. It is an existence and constructive threshold result, not a demonstrated laboratory design, a practical numerical noise threshold, a passive storage theorem, or a total-resource advantage over ordinary fault tolerance.

## 2. Mathematical theorem and exact noise radius

Fix beta<infinity and interaction range r. Let H=sum_j h_j on N qubits, with one bounded term per starting position, each supported on at most r consecutive sites and ||h_j||<=1. A larger uniformly bounded number of terms per position is absorbed into the interaction-strength normalization. Arbitrary noncommuting terms and spatially varying coefficients are allowed. Let rho_beta=exp(-beta H)/Tr exp(-beta H).

The robust-block theorem proved in comparators/robust_1d_block_opening.md gives computable constants B(beta,r)<infinity and eta(beta,r)>0, independent of N and requested accuracy, and an exact ensemble

    rho_beta = E_mu tensor_{A in P_mu} tau_(mu,A),
    |A|<=B,      tau_(mu,A) >= eta I_A/2^|A|.

Its finite-accuracy version has a polynomial classical sampler at fixed beta,r. It retains a floor at least eta/2 and approximates the delivered mixture to any chosen trace error. Its cost includes the first-stage sampler of Pilatowsky-Cameo, Styliaris, Bakshi and Malz, arXiv:2609.35973, and is not asserted to be near-linear. The input numerical model is the same digital-H model as that source. The new bounded-matrix arithmetic is independently precision-controlled below; it does not upgrade the source to an independently proved stronger bit-complexity theorem.

Let Lambda_i be any single-qubit CPTP channels with ||Lambda_i-id||_diamond<=delta<1. They may be nonunital, heterogeneous and non-Pauli in this mathematical statement. Neumann inversion and tensor telescoping give

    ||Lambda_A^(-1)-id||_diamond <= (1-delta)^(-|A|)-1.

Consequently the explicit sufficient radius

    delta_0 = 1-(1+eta/2^(B+1))^(-1/B)

ensures that every sigma_(mu,A)=Lambda_A^(-1)(tau_(mu,A)) is a density matrix and

    sigma_(mu,A) >= (eta/2) I_A/2^|A|.

Proof: the inverse perturbation has operator norm at most its trace norm, at most eta/2^(B+1), whereas tau has minimum eigenvalue at least eta/2^|A|. Inverses preserve trace and Hermiticity. Averaging tensor products of these positive states gives an exact preimage sigma_beta satisfying

    (tensor_i Lambda_i)(sigma_beta)=rho_beta.

This is a size-independent local-noise interior theorem. It does not say a linear inverse is a physical channel on arbitrary inputs. The inverse is computed to select a known positive state to prepare.

For the finite-accuracy sampler, invert each actual sampled block, rather than apply the global inverse to an approximate Gibbs matrix. Its forward image is the original sampled block. Thus the mixture approximation error is inherited unchanged at the output. Approximation of sigma_beta itself is neither needed nor asserted. A bound using the extensive global inverse norm would lose this fact.

For finite precision, use sampler floor eta/2 and

    delta_* = 1-(1+eta/2^(B+2))^(-1/B).

Require actual channels to lie within delta_*/2 of identity and acquired channels within delta_*. This leaves an explicit positive spectral reserve for the inverse and matrix synthesis.

## 3. Fully specified compatible physical model

The chosen implementation uses the accepted stationary independent Pauli model. Each outgoing primitive wire is followed by the same unknown one-qubit Pauli channel, independently at distinct space-time locations. The native bounded-arity gates, preparations, resets, idles, readout and record-capture templates are fixed and have no additional independently unknown SPAM laws. Gates include the universal protected-control set in the predecessor. Mutable classical control is noisy and is protected using that same code. Nonlocal active links, their routing, occupied time, errors and costs remain paid architecture. Fresh ancillas and noisy resets are actual operations.

The accepted boundary compiler simulates a protected circuit and produces, up to arbitrarily small execution and coupling error, independent product Pauli channels K_i at a prescribed unencoded output time. Their strengths are O(p), uniformly in the simulated circuit size. The comparison is uniform over old references and external records; fine Bell and tree histories are discarded/reset. No raw classical selector or ideal encoder is inserted here.

The component law and effective endpoints are acquired using the predecessor's noisy opposite-sign idle contrasts and protected simulation of the explicit templates. This acquisition is included in the cost. It relies on stationarity, independence and the specified shared component law; no finite calibration certifies those promises against arbitrary drift. The new mathematical radius covers more channels than this physical construction, and that distinction is retained.

Choose p below both the accepted controller threshold and delta_*/(2 C_end), where C_end is its uniform endpoint diamond-norm constant. This is a nonvanishing constant at fixed beta,r and compiler, independent of N and epsilon. Its numerical value can be extraordinarily small.

The target H and beta are supplied as a finite classical description. The apparatus need not fabricate H, implement its couplers, isolate its checks, or couple the output to a Davies bath. This removes those requirements by changing the task to preparation of a specified quantum state. It does not learn the Hamiltonian of an unknown material. Unknown physical Hamiltonian identification requires a separate access model and bill.

## 4. Executable preparation route

1. Commission the noisy control platform and acquire the required endpoint channels Khat_i. Use a physical channel estimate within the permitted radius. Keep an explicit confidence budget.
2. Execute the robust-block sampler in protected classical computation. Its output is a random partition and a list of explicit positive matrices tau_tilde_A on at most B qubits, with their spectral floors certified.
3. Compute sigma_hat_A=(tensor_{i in A} Khat_i^(-1))(tau_tilde_A). All inversion and state synthesis use matrices of dimension at most 2^B. Apply the numerical reserve above. Prepare their tensor product using actual protected circuits with noisy resets, ancillas, gates and routing.
4. Export every qubit using the accepted Bell/tree compiler at a common scheduled time. The reference output is tensor_i K_i applied to the valid prepared state. There is no ideal final output port.
5. Reset/discard fresh ensemble labels, fine interface records and preparation garbage, or explicitly make their actual correlated extension part of the delivered specification. Previously retained external records remain protected by the compiler's guarantee.

For the exact acquired channels, Khat maps every prepared block back to tau_tilde_A. A telescoping forward-channel comparison gives

    D[K(sigma_hat), Khat(sigma_hat)]
       <= (1/2) sum_i ||K_i-Khat_i||_diamond.

There is no global inverse condition-number factor in this metrology bound: sigma_hat is an ordinary density matrix. Adding source, finite arithmetic/synthesis, controller, tree, acquisition and target-description errors yields

    D(rho_delivered,rho_beta)
       <= eps_source + eps_numeric + eps_execution + eps_tree
          + (1/2) sum_i ||K_i-Khat_i||_diamond
          + Pr(acquisition confidence failure) + eps_H.

Choose these budgets to sum to epsilon. This is a physical noisy-delivery construction at fixed p, not a formal inverse with an ideal state-preparation oracle.

If target local terms have description errors at most xi in operator norm, D(rho_beta(H),rho_beta(Hhat))<=beta N xi. This follows by differentiating the normalized Gibbs operator along the segment between H and Hhat, using Schatten Holder on the Duhamel integral. Thus O(log(N/epsilon)) target-coefficient bits suffice at fixed beta, provided that precision is actually supplied or acquired. This is not a claim that an unknown device yields those bits for free. Use the uniform interaction bound for both H and Hhat, or enlarge the declared bound by its known approximation margin.

## 5. Records, repetition and useful endpoint

### A literal finite-bit fallback, without an exact-real sampler oracle

The physical existence result need not rest on interpreting any source sampling oracle as exact real arithmetic. There is a direct, exponentially costly fallback. The exact positive preimage constructed in Section 2 obeys a global floor

    sigma_beta >= (eta/4)^N I,

because every block inverse has floor (eta/2) I_A/2^|A| and at most N blocks occur. Let delta bound the acquired channels Khat_i that are actually inverted, and put g=(1-delta)^(-N). Compute the digital Gibbs matrix by full 2^N-dimensional matrix exponentiation and normalization, then apply the tensor inverse as a linear map. Certified arithmetic, including the inverse calculation, with trace-norm error much smaller than min(epsilon,(eta/4)^N) makes the final Hermitian, trace-normalized matrix positive and epsilon-close to the exact acquired preimage; the input Gibbs matrix error is reduced by the factor g. The sufficient precision is O(N log(4/eta)+N log(1/(1-delta))+beta N+log(1/epsilon)) bits, plus fixed input constants and dimension bookkeeping. Full matrix evaluation and purification synthesis cost 2^O(N) times polynomial precision work.

A final PSD projection removes even the need for floor-scale numerical accuracy in this fallback. If the computed inverse is zeta-close in trace norm to the positive exact acquired preimage, Hermitianization and trace fixing increase this to at most 2 zeta. Its negative mass is at most zeta. Projecting to its positive part and renormalizing changes it by at most 2 zeta more, for total trace error at most 4 zeta. Thus O(epsilon) inverse accuracy suffices, with the input matrix error divided by g. This needs O(N[1+beta+log(1/(1-delta))]+log(1/epsilon)) precision bits in addition to input representation terms. Residual-controlled diagonalization avoids an eigenvalue-gap assumption. This is still exponentially costly global computation, not the bounded-block efficient implementation.

Prepare this positive matrix with the same actual protected controller and acquired boundary. All calibration, enlarged circuit, routing, output-tree and reset costs still apply. Choose deterministic circuit-size caps before acquiring the endpoint templates. This establishes a fully finite digital operation without an ideal probability or real-arithmetic oracle. It carries exponential work and is not the polynomial-source implementation or a resource advantage. The efficient ensemble implementation retains the primary sampler's stated computational convention; the new structural theorem and physical existence do not depend on a separate unpublished first-stage bit-complexity result.

The endpoint is an actual N-qubit density matrix at the announced release time. The global trace guarantee controls every subsequent measurement or CPTP use by data processing. It covers joint, nonlocal and adaptively selected measurement protocols through their operational probabilities, not merely a fixed list of local observables. Subsequent noisy computation has its own paid implementation; subsequent storage has its own model. This theorem does not extend the previous passive hold to noncommuting Hamiltonians.

Fresh source labels cannot be retained while claiming the conditional state is Gibbs: conditioning on a label exposes its generally different block-product component. In the theorem they are erased/discarded. Calibrations may be retained when the confidence and channel-mismatch bound hold uniformly on the accepted confidence set; failure probability is charged. With these conventions the construction is compatible with arbitrary pre-existing references and records, but it prepares a known target and does not transmit an unknown quantum input. It does not prepare a prescribed purification or TFD.

Repeated calls with fresh reset resources and per-call error eps_j compose by a hybrid bound sum_j eps_j, including adaptively chosen digital targets within the uniform beta,r/norm limits. A finite commissioned randomness stream can have a single joint error allocation, but every physical output, reset, exposure and active location is still charged. Postselection on an internal preparation label changes the target and is not free reuse of the Gibbs marginal.

## 6. Explicit resource ledger

Write C_src(N,epsilon;beta,r) for the actual published first-stage sampler plus modified finite-state sampling and finite-precision cost. It is polynomial in N and 1/epsilon at fixed beta,r in the source's numerical-input convention. Retain this term, rather than replace it by O(N). Matrix work per bounded block is a finite cost exponential in B; a safe pure-purification synthesis bound has a factor 4^B times a polynomial in precision. The number of actual blocks is at most N.

For ternary regenerator noise parameter s<=0.01, let alpha=21s<1, and q_c be the accepted raw-pool local-stochastic parameter. With 2N roots, choose

    h = max(0, ceil[log(2N q_c/eps_tree)/log(1/alpha)]).

The physical leaf count is 2N 3^h, of order N(N/eps_tree)^kappa, kappa=log(3)/log(1/alpha), with the actual q_c and constant prefactors retained. This overhead is polynomial in inverse accuracy, not ordinary polylogarithmic fault-tolerance overhead.

If V is the resulting protected circuit size, the inherited concatenated-code recursion p_(ell+1)<=a p_ell^2 chooses ell=O(log log(V/eps_execution)). Actual location cost contains V g^ell, with the fixed base-code/gadget constants a,g charged. The predecessor's conservative base already has 2047 physical qubits per logical qubit before further concatenation. No useful threshold or hardware count is inferred from big-O notation.

For G_max stochastic locations per endpoint simulation template, estimating the shared primitive law to O(eps_cal/(N G_max)) costs O((N G_max/eps_cal)^2 log(1/eps_fail)) noisy trials, plus protected capture and arithmetic. Directly acquiring N potentially distinct effective laws to O(eps_cal/N) costs O(N^3 eps_cal^(-2) log(N/eps_fail)) simulated samples in the conservative general route, multiplied by their actual simulation sizes. Identical templates can share calibration; the bill must use the templates actually built. Preparation/reset, metrology time, simulator faults and returned records are included. The optional finite-factory direct-assay construction in the boundary notes has a narrower model and is not silently substituted here.

Total physical space-time is the integral of occupied qubits and controller registers over physical time, including calibration, routing, protected waits and disposal. A proper energy ledger is

    E_total = E_fabrication + E_acquisition + E_controller + E_gates
              + E_routing + E_resets + E_cooling + E_idle.

There is no given platform energy model from which to calculate a numerical advantage. Reset entropy and refrigeration are real costs; Landauer bounds concern the erased conditional entropy, not an assumed fixed energy for every syntactic reset. An ordinary active-preparation comparator receives the same gates, links, cooling, switching, metrology and input access.

Even the explicit existence bound is astronomically unfavorable: the conservative base length m0=ceil exp[r max(1,beta)(2240)^(2r)] already has exponent about 5.0e13 at r=2,beta=1. The later superblock and inverse-radius constants are worse. The theorem establishes a nonzero radius; it does not make this bound usable.

## 7. Broad deductions and sharp boundary

### Entangled targets can have positive local-noise preimages

For a Heisenberg dimer H=(XX+YY+ZZ)/3,

    rho_beta = [I-t(XX+YY+ZZ)]/4,
    t=(exp(4 beta/3)-1)/(exp(4 beta/3)+3).

Two depolarizing channels with Bloch contraction lambda have a positive preimage exactly when t<=lambda^2. It is the same Werner state with t_in=t/lambda^2. The target is entangled for t>1/3, so there is a nonempty entangled reachable region whenever lambda^2>1/3.

More strongly, the exact best possible trace error over every input state is

    inf_sigma D[(D_lambda tensor D_lambda)(sigma),rho_beta]
       = (3/4)(t-lambda^2)_+.

Proof: SU(2) twirling fixes the target and commutes with the channel. Contractivity lets one restrict to Werner inputs with parameter u in [-1/3,1]. Their output parameter is lambda^2 u and the distance is (3/4)|t-lambda^2u|. Choose u=min(t/lambda^2,1); for lambda=0 choose any input. The preimage or the singlet attains the optimum. This is a channel-range boundary, not a limitation of the proposed algorithm. Fixed nonzero endpoint noise cannot work uniformly down to zero temperature.

### Uniform resistance to remote heralding

For the exact Gibbs state in the representation, if the near-identity local channels are depolarizers with replacement probability gamma>0, every conditional state on a retained set A, after any nonzero-probability measurement outcome on its complement, has eigenvalue floor at least gamma^|A|/2^|A|. Move the complement instrument back through the complement channels; it leaves a positive conditional input on A. The all-sites-replaced term in the remaining channel has weight gamma^|A|. Thus arbitrarily rare postselection elsewhere cannot remove this local thermal mixedness in the exact target. This is a deduction of the representation; no priority over existing Gibbs local-comparability results is claimed.

The approximate physical output has its ordinary conditioning cost. If its unconditioned trace distance is at most epsilon and the chosen outcome has target probability q>epsilon, the actual outcome has positive probability and the conditional trace-distance error is at most 2 epsilon/q. No outcome-uniform positive floor is claimed for arbitrarily rare heralding from the approximate implementation.

### Thermodynamic-limit statement

The constants do not shrink with system size. Fix one compatible family of single-site channels on the infinite chain satisfying the uniform radius, and use its restrictions on every finite volume. Whenever the finite-chain Gibbs states converge locally, their preimage states have a weak-star subsequential limit; the same fixed local tensor channels pass through that limit. Hence the limiting thermal state lies in the image of the infinite product of this channel family. This is not merely a finite-matrix interior estimate based on the global smallest eigenvalue.

### Separate high-temperature, weak-apparatus corollary

For arbitrary bounded-degree Pauli interaction graphs, the BLMT coefficient invariant supplies a separable finite-radius palette preparation at sufficiently high temperature. The constructive weight condition and its device convex-hull test are proved in the separate noncommuting and boundary notes. That operation may use entanglement-breaking local factories: quantum capacity is not required to prepare known sufficiently mixed targets. This is a corollary of existing high-temperature preparation structure plus the actual noisy palette interface, not a new invention of high-temperature separability or a general quantum communication theorem.

## 8. Comparators and unsuccessful routes

The strongest existing ideal preparation methods already cover every fixed-temperature one-dimensional Gibbs state. They must not be presented as unavailable: the bounded-block source gives constant ideal quantum depth, modern exact Gibbs samplers give ideal near-linear gate bounds, and current system-bath methods give roughly N/epsilon evolution time. Ordinary FT can protect their internal circuits and can also use this new positive-preimage theorem with the same product boundary. Generic precompensation already solves the known-channel inverse/SDP task; the new content is a uniform many-body interior theorem and a constructive positive preparation ensemble. FT I/O already leaves controlled boundary noise. Engineered autonomous correction is a different dynamical implementation, and can be a legitimate controller if its physical interfaces are supplied.

The naive argument 'all blocks are full rank, so finite isolated noisy cells eliminate all growing quantum error correction' is not completed. Random partitions, masks, coupler selection and routing can induce cross-block errors when the classical decisions are faulty. A calibrated isolated-cell convex hull does not by itself implement the needed random partition on a fixed chain. The completed all-temperature physical route therefore retains the accepted protected fabric. General coherent, non-Markovian or gate-dependent physical noise is not covered merely because the mathematical inverse radius allows arbitrary local CPTP channels. A compatible product-boundary construction is still needed for such apparatus.

## 9. Evidence and preservation

The algebraic proof is independently audited in noncommuting/robust_1d_independent_audit.md. Finite code checks verify softened spectral identities, the positive mixed-Pauli expansion, a variable-cut nine-qubit dressed mixture and transfer law, small noncommuting inverse states, a heterogeneous nonunital norm bound, and the sharp dimer boundary. They are finite identity/counterexample checks, not implementations of the astronomically large source sampler, a physical experiment, or empirical lifetime evidence.

The preceding accepted research archive is preserved unchanged in this package. This round changes none of its scopes, including the unknown-reference register, finite passive-time coupling, positive syndrome prefixes, raw-port lower bound, separate coherent TFD/central-sector constructions, repair companion, productive control, burst loss, intervention and first-event results.

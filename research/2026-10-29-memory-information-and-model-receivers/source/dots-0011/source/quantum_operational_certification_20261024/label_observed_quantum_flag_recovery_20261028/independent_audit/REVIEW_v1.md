# Independent review: observed error labels and noncommuting quantum flags

28 October2026. **Accepted at the explicit stationary mixture/source-feature, observed-label and trusted-control mathematical/simulated-record scope, subject to the full-Pauli-basis clarification noted below.** This review does not concern the separate weighted-tree stability proposal, to which this reviewer contributed. The present label-observed theorem uses no such lemma.

## Complete decoder reduction

Expand every decoder Kraus map in the FULL4^n Pauli operator basis, K_b=sum_x P_x tensor <v_bx|. Trace preservation followed by partial trace over the logical register gives sum_x,b |v_bx><v_bx|=I_G. The entanglement-fidelity Kraus formula selects the matching Pauli coefficient, giving sum_x p_x Tr(M_x tau_f(x)). The M_x are therefore a POVM, and measuring that POVM followed by the corresponding Pauli correction attains the same objective. This is a full joint logical-plus-gauge CPTP comparison; an ancilla-assisted or coherent joint decoder cannot evade it.

IMPORTANT: the X-only subgroup does not span arbitrary decoder Kraus maps. In that case still expand over all4^n Paulis and set source probabilities to zero outside the supported subgroup. Effects on those unused labels can be reassigned to any allowed correction without decreasing the nonnegative objective. Only then may the reduced POVM be indexed by the2^n allowed error labels. The separate author clarification is part of the accepted proof.

Within a known feature fiber, identical flag states make the largest true word probability optimal for every allocated positive effect. Grouping effects and choosing the fiber mode yields the stated K-matrix discrimination problem. Unknown or input-dependent flag states outside the common-feature promise are not covered. Independent numerical checks use100 random complex qubit-gauge joint CPTP decoders; the extracted gauge effects are positive, sum to identity within6.67e−16, and reproduce direct Kraus fidelity within1.67e−16. These checks supplement the dimension-independent algebra.

## Acquisition and error bound

Observed error labels give actual counts and three bounded flag moments. The unnormalized estimator is Hermitian; it need not be positive because it is an objective coefficient, not a prepared state. For qubit Hermitian error(a I+v.sigma)/2, the trace norm is exactly max(|a|,|v|), proving the stated uniform error e.

The empirical fiber mode has true mass at least the true mode minus2delta_p, including an unseen feature with a fixed valid fallback. For any physical K-outcome POVM, coefficient perturbation costs at most K e. Passing to and from the empirical optimum therefore gives2K e+eta_alg, in addition to2K delta_p from mode selection. No rare conditional state is normalized, and no state-rank or probability floor enters.

The count Hoeffding bound and moment Bernstein bound are correct. Moment variables have second moment<=3 and centered magnitude<=4; the displayed positive-series mgf argument gives the stated exponent. Uniformity over all A possible labels permits data-selected words, even though only observed labels need to be stored. Log A is linear in n for the two supplied label-observation interfaces. General K requires the stated small known-data POVM solve; the delivered K=2 pilot implements its own certified binary solve, not an unknown-source optimization oracle.

## Independent execution and exact physical measurement

All4,194,304 training records were independently regenerated and accumulated through integer joint histograms, not the author's weighted-bincount code. Every count and moment matches. The selected words are00000000 and11111111. The exact rational stereographic parameters give a unit Bloch vector, so the proposed effects are a physical rank-one projector and its complement regardless of the floating proposal calculation. The integer-square-root bound reproduces the empirical optimization slack. Exact rational exponential-series arithmetic independently reproduces the training failure bound and regret .04264120000003671.

All65,536 fresh holdout source/flag decisions were independently replayed. The reviewer computes actual corrected computational-basis output bits e XOR correction, then checks whether all are zero, rather than importing the author's success predicate. The2201 failures agree. An independently factored binomial-tail polynomial, not the author recurrence, matches both saved integer digests and passes the .95 target at alpha .001. The combined training-plus-validation allowance is at most .00104106; these are two distinct statements, not a claim that the observed point estimate is an exact physical fidelity.

Under the promised X-only Pauli mixture and flag-only measurement, corrected data remain an X-only Pauli mixture. Their all-zero/Z test succeeds exactly on the identity Pauli term, which equals full8-qubit entanglement fidelity. This equality is conditional on the source promise. The raw simulation uses exact rational categorical probabilities; NumPy integer draws are a model of uniform sampling, not evidence of laboratory acquisition or an independently audited randomness device. The saved plan supports internal fixed-plan provenance, not external preregistration.

Exact-source diagnostics agree: learned fidelity .9675410647976247, full-CPTP oracle .9675416845888335, and no-flag full-CPTP oracle .4965104825174895. They are not used to select the measurement or decide acceptance.

## Necessary negative control: invisible phase noise

Compose the source with an unflagged fair mixture of I and Z^tensor8. For every actual |0>^8 bit-flip probe, this changes only phases of computational-basis outputs. Therefore every training label, flag distribution and corrected-Z holdout outcome has exactly the same law. Yet each previous Pauli label splits into two distinct orthogonal Pauli labels carrying the same flag. The full-CPTP discrimination coefficients are all halved, so the best global entanglement fidelity is .48377084229441675, not .96754. Thus these ordinary Z-only records cannot establish the bit-flip frame, and would give a false quantum-fidelity interpretation without that premise. The general-Pauli Bell-probe route avoids this particular blindness by paying its different reference-storage and Bell-readout resources.

## Scope and cost

The construction tolerates arbitrary spatial correlations and exact zeros within its specified classical error-mixture/feature model. It does not tolerate unrestricted phase noise, coherent error-label superpositions, input-dependent flags, unknown feature partition or returning source memory for free. It does not establish those promises from the recorded probes.

The delivered cost is4,259,840 complete calls,34,078,720 data-qubit exposures and4,259,840 emitted flags. The ordinary bit-flip pilot uses no stored entangled references; the full-Pauli alternative would. Deployment needs one known single-qubit measurement and at most8 X gates. The rational projector defines an ideal small physical operation, but timed/noisy synthesis and control error are not supplied by this pilot. It must not silently inherit the separate noisy-controller certificates.

Conventional count selection and Helstrom measurement can perform the identical operation with identical information and resources. The no-flag comparison removes an actual accessible quantum resource, rather than proving algorithmic advantage. A different code with a smaller payload can exploit this strongly correlated source; this theorem preserves the fixed full8-qubit input instead. The accepted contribution is the explicit finite acquisition-to-recovery path at that scope, not historical novelty or a general quantum-memory breakthrough.

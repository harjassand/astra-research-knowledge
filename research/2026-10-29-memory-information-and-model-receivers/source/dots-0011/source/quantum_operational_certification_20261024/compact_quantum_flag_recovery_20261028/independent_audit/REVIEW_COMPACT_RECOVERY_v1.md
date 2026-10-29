# Independent review: feature-free compact quantum-flag recovery

28 October 2026. Accepted subject to the explicit clarification addendum bound in this receipt. This removes the supplied feature/identical-flag-state promise from the stated learner. It does not remove the Bell-label interface, flag dimension, independent-call source contract or physical control assumptions.

## Oracle scope and acquired quantities

For any fixed input-data to output-data-plus-flag CPTP map, normalized Choi Bell projections produce positive subnormalized flag matrices sigma_x. Moving the final Bell test backward through a flag POVM and conditional Pauli gives exactly sum Tr(M_x sigma_x), even when the source has coherent off-diagonal Bell blocks. Thus this quantity is the optimum over the specified flag-measurement/Pauli-correction class for arbitrary sources.

It equals the unrestricted collective CPTP recovery optimum only for the Pauli-plus-flag source. Expanding a decoder Kraus operator over the COMPLETE Pauli basis and partially tracing the TP relation produces a complete flag POVM; Pauli orthogonality yields the stated objective. The source correctly uses the full basis even for the X-only promise, whose unused labels can then be reassigned without reducing the true objective. The general coherent-source claim must not be read as full-CPTP optimality.

The independent checker directly constructs 80 arbitrary coherent Choi sources, physically composes their Kraus maps with actual flag measurements/Pauli corrections, and compares their complete entanglement fidelity with Bell-block scores. Agreement is below4e−16. This challenges the coherent case rather than only rechecking diagonal sources.

## Acquisition and uniform concentration

The Pauli flag estimator r*1[label=x]*bW is unbiased because the Pauli expansion is sigma=(1/r)sum_W Tr(W sigma)W. Its second moment is r²p_x I, including the identity setting. The centered second moment and norm bounds stated in the source are valid. Independent exhaustive measurement-outcome checks verify both moments for qubit and four-dimensional flags.

The reviewer inspected Tropp's primary Theorem6.1(ii), https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf , printed pp23–24. With dimension r, total variance at mostNr², centered bound2r and thresholdN delta, applying both signs and union bounding A labels gives exactly the displayed denominator2r²+(4r/3)delta and prefactor2Ar. Independence is across complete calls. No independence of separate label estimators is required.

The qubit pilot uses its previously received scalar-component event instead; the source does not incorrectly mix its constants with this new general-r readout. The source-call scaling is polynomial in n at fixed r for additive regret, but the known flag dimension r, Bell reference storage/readout and source stationarity are substantive resources. No unobserved phase-error promise is inferred from ordinary X-only probes.

## Dummy reduction, regret and support

Every unobserved empirical coefficient is exactly zero. Merging all unobserved effects into ONE genuinely unobserved allowed label therefore preserves the empirical objective. If all allowed labels were seen, no dummy is added. Searching at most the first |S|+1 labels for a missing word is polynomial in observed input size, and does not enumerate an exponential alphabet. This reduction does not set the dummy's true coefficient to zero; its error is controlled by the same uniform event.

For any physical complete POVM, |sum Tr M_x(Shat_x−sigma_x)|<=delta sum Tr M_x=r delta. Applying it on either side of a certified empirical optimum proves2r delta+eta regret, with no number-of-labels factor. Indefinite raw Hermitian coefficients are permitted because they are objective data rather than implemented quantum states. The clarification uses I/m, m actual outcomes, for a strictly feasible primal point. The old I/(N+1) wording would not sum to identity unless explicitly padded.

Real linear dependence of more than r² effects supplies the support reduction. Moving to the sign-appropriate endpoint of the feasible scaling interval cannot decrease empirical score and removes an outcome. It need not preserve the physical channel or true score; the uniform regret theorem is what continues to hold. A rational weight LP supplies a basic optimum and controlled bit complexity without relying on uncontrolled repeated-denominator growth. The tetrahedral qubit example correctly forces four nonzero effects by complementary-slackness rank-one kernels and affine independence, so an r-outcome universal claim would be false.

## Physical measurement construction and resource ceiling

Stacking sqrt(M_i) gives an isometry because sum M_i=I. Completing it to a known unitary and measuring the outcome register implements the POVM on a space of dimension at most r³. Its synthesis is polynomial in the known matrix dimension and precision, not automatically polynomial in log(r). Independent Naimark completions reconstruct all effects in 80 four-outcome qubit tests within1.4e−15. Generic hardware compilation is not claimed to have been run; the previously saved binary qubit projector is the concretely instantiated operation.

Empirical optimization slack and whole-recovery implementation error are separate budgets unless explicitly split into a common total. Actual corrections still require known Pauli controls on n data qubits, calibrated flag measurement and fresh outcome ancillas. No hardware precision/noise assurance follows merely from SDP feasibility.

For normalized flag states, y_x=Tr(M_x tau_x) lies in[0,1] and sum y_x<=r. Maximizing its weighted sum gives the top-r-prior ceiling. Orthogonal flags for the r most likely labels attain it, so it is sharp. This ceiling is a useful limit: a constant-dimensional flag cannot preserve a full payload against a diffuse exponential error distribution. Near-oracle acquisition can be easy when the oracle itself has very low fidelity. No code-rate or quantum-memory-threshold claim follows.

## Same-bank exact certificate

The reviewer independently checks ALL256 empirical dual constraints, not only the53 observed labels and one dummy. All203 unobserved labels have exactly zero empirical coefficient, and the saved dummy label5 is valid. Exact rational principal-minor tests prove Y>=Shat_x for every label. The saved projector has exactly unit Bloch norm and yields positive complementary effects summing toI.

From the same integer counts, the two global highest-count labels are0 and255. Recomputing their primal score and the saved dual trace exactly reproduces the gap3.6713538954604314e−14. The rational upper bound on sqrt(3) yields operator error .00533015 and full-CPTP regret .021320600000036712. The scalar event's failure probability independently recomputes to4.105574902131763e−5. No known root feature or chain law is used by this certificate.

The measured decoder is unchanged, so its earlier fresh95% validation remains applicable to the same bit-flip instrument without needing the shared-flag feature assumption. This is a stronger analysis of the same observations, not a new independent experiment or new physical execution. The older raw-record replay is a received dependency; this review adds zero source calls. The initial label-order failure and v2 correction are preserved.

## Twirl and preconditioner boundaries

A committed actual Pauli twirl dephases the source Choi state into the required diagonal form when the key is retired. Its full-CPTP comparator is then the TWIRLED source's oracle, not the original coherent source's oracle. The H-tensor-n example correctly loses from perfect reversible performance to2^(-n) under blind twirling with no flag. The independent checker verifies the one-qubit Bell weights exactly to floating precision.

After a frozen actual coherent preconditioner, identity/flag discard belongs to the compact correction class, so the regret bound cannot reduce its existing Bell performance by more than the stated regret and implementation bill. This is a valid positive composition, but data-selecting a preconditioner requires fresh acquisition or a separate uniform policy argument.

A private outer twirl of the completed DATA-OUTPUT service preserves Bell fidelity and gives half-diamond distance1−F_e for the reduced Pauli channel. The clarification removes the redundant Tr_G after a decoder already typed LG->L. This guarantee excludes retained/exposed key or bath registers and does not establish inter-call memory robustness. Two physical Pauli layers, fresh2n-bit randomness and their errors must be charged.

Accepted: source/comparator distinction; uniform matrix acquisition; finite dummy-label SDP; label-independent regret; r² support and known Naimark construction; sharp resource ceiling; exact same-bank certificate; scoped twirl/preconditioner compositions. No historical novelty, unrestricted coherent recovery optimum, acquired useful preconditioner, noisy-device capability or equal-resource algorithm advantage is received.

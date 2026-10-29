# Deferred final-Bell statistics for the unkeyed resource service
2026-10-29. New extension, independent review pending. This is NOT an equality of full resource states or a declaration that conditioned source memory is unchanged by measurement.

## Claimed object
Use the accepted unkeyed mixed-role entanglement-resource protocol: actual service outputs are isolated and never Bell-measured during acquisition; actual probes update the learned span; all controls depend on actual classical records only. We claim an exact representation of the joint distribution of

  (actual probe records and roles, hypothetical FINAL Bell-basis labels
   of the isolated service resources).

Only this distribution is needed to calculate the good-span projector weight used by the received twirl-free outer decoder. The original coherent resource state is generally NOT a Pauli mixture. The exact keyed direct-payload comb identity remains a different, stronger channel statement requiring actual private pads.

## Retain the discarded gauge registers mathematically
At a service birth, after applying C_t† on the source output, the actual protocol traces out the gauge halves on both the reference and output. For purposes of analyzing the final logical Bell-projector measurement, implement those traces by retaining the discarded registers in an inaccessible spectator environment. They never interact with the source, any payload, subsequent controls, or each other again. Tracing them at the end reproduces the actual protocol exactly on every assessed register.

Refine the final Bell measurement of each logical service resource by also Bell-measuring its retained gauge reference/output pairs. This refinement does not change the logical-label distribution. Together these are the full n-pair Bell basis on that service's private reference and decoded output. Label its result by w in canonical compiled coordinates, and map it to physical Pauli label v via the known Clifford relation C_t†P_v C_t=phase_v P_w.

## Adaptive instrument commutation
Fix a complete actual transcript of roles and probe outcomes. Every later quantum operation along this transcript acts on source memory, new input/output registers, new private references and classical controller registers, but not on an older isolated service register or its discarded-gauge spectator. Every service Bell projector therefore commutes with every later branch Kraus operator on that transcript. The fact that later controllers choose C_{t'} from the actual transcript causes no problem: for each fixed transcript the chosen operator still acts on disjoint registers.

Move every refined final service Bell projector backwards through these branch operators to immediately after the corresponding service's decoding. This does not change the joint probability of that transcript and those final refined service labels. Sum over transcripts if desired. Service labels are never fed to the controller in this reordered mathematical experiment; introducing such feedback would define a different protocol. Later source memory conditioned on a moved label generally **does** change, and must be propagated using its actual conditional instrument. The claim is equality of the specified joint probabilities, not equality of these conditional states before and after inserting a measurement.

## Equality of the refined service and probe memory instruments
For any current memory state (including correlations with earlier isolated resources), expand joint source Kraus operators V_r=sum_v P_v tensor A_rv. A physical probe prepares encodedBell(C_t), applies C_t* on the reference after the source, and Bell-measures, giving

  I_v(rho)=sum_r A_rv rho A_rv†.

The refined service instead applies C_t† on the output and measures the full canonical Bell label w. The Bell trace identity gives its amplitude operator

  (1/2^n)Tr_B[P_w† C_t† V_r C_t]
    =phase_v A_rv,

where v is the physical label corresponding to w. Therefore it has the SAME CP instrument I_v, including the correct conditional source-memory update. The logical portion of w is a nonidentity error only if v lies outside the compiled harmless gauge envelope, hence outside S_t.

Because the current role is chosen privately after the identical source-facing call (or hidden with no pre-call effect), the refined physical label instrument can be sampled before that role coin. The opportunity-stream coupling now applies to the refined joint-statistics representation. Thus the numberF of nonidentity logical Bell blocks in the hypothetical final measurement satisfies

  F <=_st NB(m*,1-q),   m*=dimS*<=2g.

In particular, for integer t>=0 and knownm>=m*,

  Tr[(I-P_good,t) Omega_J]
    <= Pr[Binomial(m+t,1-q)<=m-1],

where P_good,t is the span of all logical Bell strings with at mostt bad service blocks. Finite service or call/probe-budget stopping only truncates the opportunity stream; cap abort remains a separate charged event. The statement concerns each finiteJ. No physical service Bell measurement or actual twirl is required.

The received outer decoder effect E>=P_good,t then gives final resource Bell infidelity at most this negative-binomial tail, even though Omega_J may have coherent cross-Bell terms and arbitrary correlations. This is exactly why the corrected-span operator inequality, rather than a false equality to a Pauli-diagonal resource, is used.

## Diagnostic that separates the two claims
`deferred_bell_tail_check_v1.py/.json` uses a common rank-one Pauli algebra supported on I,Z of an initially unprotected qubit, with a noncommuting retained two-dimensional memory. It compares the actual **unpadded** adaptive physical circuit to a latent Pauli-instrument model. For two isolated services by cap24 the entire completed Choi state differs from the latent Pauli mixture by Frobenius norm0.1830, decisively rejecting full-state equivalence. Nevertheless all16 final Bell-basis probabilities agree to below6e-16, as predicted by the deferred-projector argument. No virtual outcome is used to choose later controls in either branch. This is a small exact-branching check, not the general proof.

## Restrictions
Source access to an older service system or discarded gauge spectator would invalidate the commutation. Control dependence on hypothetical service labels would also invalidate it. Merely tracing source memory and replacing it iid is not permitted. Joint Bell acquisition access, trusted isolation/storage, exact common algebra, private current roles and finite resource accounting remain the same as in the governing service theorem. This addendum does not convert an unkeyed direct-payload channel into a Pauli channel or remove permanent key-isolation requirements from the separate direct-payload theorem.

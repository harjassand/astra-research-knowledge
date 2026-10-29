# Candidate direct-payload bridge: private logical-pad instrument identity
2026-10-29. New load-bearing lemma and proposed streaming composition, NOT covered by mixed-service receipt. Independent review required. Do not conflate with already accepted resource theorem.

## Exact single-call identity, including prior payload–memory correlations
Let the actual joint source Kraus operator be V_r=sum_v P_v tensor A_rv on B,M, with Hermitian physical Paulis and arbitrary memory operators. Trace preservation, after partial trace over B, gives sum_{r,v}A_rv†A_rv=I_M. Let the compiled encoder C map g gauge and k logical qubits into B, and write

  C† P_v C = phase_v Q_g(v) tensor Q_l(v).

The phases have modulus1 and can be absorbed into A_rv. Let rho_LMR be an arbitrary joint state, with R any spectator (previous/future payload, external reference); no independence between L and M is required.

Implement an actual service:
- prepare gauge I/2^g independently;
- choose a fresh uniform private k-qubit Pauli K, independently of rho;
- apply K on L and C on G:L, then make the joint source call;
- apply C† on returned B, discard G, undo K on L; retire the key.

The exact resulting joint channel on L,M,R is

  rho -> sum_{r,v}(Q_l(v) tensor A_rv tensor I_R) rho
                     (Q_l(v)† tensor A_rv† tensor I_R).        (P)

Proof: expand in v,w. The gauge partial trace is delta_{g(v),g(w)}. Averaging conjugation by the private logical Pauli K makes the phase character average delta_{l(v),l(w)}. The Clifford label bijection makes both equalities imply v=w. Thus every off-diagonal term vanishes and (P) follows. This is an actual randomized channel identity with retired keys, not a claim that unrandomized service errors can be virtually measured without disturbing future memory. It holds on the entire correlated input, not only the maximally mixed logical state.

Tracing L,R in (P), the memory label instrument is exactly rho_M ->sum_r A_rv rho_M A_rv†, the same as the physical-frame Bell probe. Source-visible pre-call state, averaged over the fresh hidden pad, is I_B/2^n tensor rho_M, and is decoupled even when the original payload and memory were correlated. Hence pre-call service/probe choice can be hidden from the source if the source has no key access and no physical timing/control side channels. Equality of source marginals must be used at the level of the joint state with all source-accessible memory; an inaccessible payload reference is allowed.

## Proposed actual-payload finite-mistake protocol
Use private Bernoulli role choice before the source call. On a probe prepare the same encodedBell input as the accepted service theorem and undo C by conjugate on the retained reference after the call. On a service, take the next logical block of a pre-encoded outer payload, implement the private-pad service above, and isolate the returned logical block. Compile C from actual previous probe labels only; pad gauge to fixedg. No private pad is needed on probes because their source input is already maximally mixed and independent of all past systems.

Because (P) is a genuine Pauli-instrument decomposition, introduce latent labels on service calls as a mathematical dilation of the **averaged keyed protocol**. This is legitimate here but was not assumed in the unkeyed Bell-resource theorem. Conditional on all latent labels and actual probe history, current source memory may be arbitrary. The same source coefficient instrument applies to both roles, and label v outside the current learned span has probability p_out. A service logical fault is possible only when v lies outside its harmless gauge envelope, hence outside the span. Actual probe innovations still occur at mostm*<=2g times pathwise. Conditional Bernoulli charging therefore suggests E[#faulty service blocks] <=[q/(1-q)]m* through any fixed numberJ of services, with a finite-call cap charged separately.

If the single-call identity composes exactly as stated through the adaptive source comb (to be independently checked), an outer quantum code correcting t block-Pauli faults gives final entanglement fidelity at least1−m*q/[(1−q)(t+1)], even when the original payload blocks were jointly entangled. The outer code must be applied to the payload *before* these service calls, not retroactively to already delivered data. This is not necessarily a diamond-distance bound from that fidelity alone; exact correction on each latent fault pattern and a positive bad-pattern weight should give a direct reduced-channel trace-distance bound, but the input-dependence of latent probabilities and the reference-uniform conclusion need an explicit comb proof.

## Physical scope and open checks
This potentially replaces long-lived pre-created Bell resources with actual outer-encoded payload operations, but it does not make physical interfaces free. Probe Bell measurements still require joint quantum access to a trusted retained reference and returned output; this is not automatically available for a remote one-way channel. Outer payload preparation, private keys, input/output isolation, and quantum storage during the entire encoded operation must be paid. If the alleged benefit is merely local storage while a trusted noiseless memory already exists, conventional bypass remains a relevant comparison. The natural interface is a trusted controller repeatedly invoking an unknown noisy operation on selected encoded registers.

Keys must be fresh and inaccessible throughout the source interaction, then retired for (P). Retaining key/source/payload joint records is not covered. The source support promise remains the same common Pauli algebra at every joint interaction. Unknown tensor frame, faulty acquisition, and untrusted controls are not solved. This file proposes no historical novelty claim.

## Exact finite checks
`private_pad_instrument_check_v1.py/.json` directly averages all four logical one-qubit pad keys for a two-physical-qubit source, arbitrary coherent joint unitary on source+2D memory, and eight correlated L:M:R density matrices. Direct physical implementation agrees with(P) to1.1e-16 Frobenius norm; source-facing pre-call decoupling agrees to2.6e-17. The source is not assumed Pauli-diagonal. These checks address the one-call identity, not the whole adaptive composition.

## Candidate comb proof, made explicit
Assume the entire fresh outer-encoded payload, including its external reference, is initially independent of source memory. Expand each padded service using the **exact** instrument(P), and each probe using its actual Bell instrument. Condition mathematically on every latent service label and Kraus index as well as actual probe results. Inductively the unnormalized state factors into (i) the entire payload with a definite history of known-location Pauli faults on already serviced blocks and (ii) a source-memory state. This is because every branch operator is a tensor product of one payload Pauli and an operator on memory, while probes act only on memory and fresh probe systems. The encoder for the next block depends only on actual probe records, not on the unknown payload state. Hence branch weights and stopping/role laws are independent of the unknown payload and its external reference. Source-memory dynamics can depend on time and accessible history, but not on the fresh private pad or role beyond its quantum interaction.

Under that factorization, each service block suffers a definite logical Pauli Q_l(v). Its being nonidentity implies v outside the current learned span. Conditional on the full latent history, source coefficients induce the same distribution on v for probe versus service, so Bernoulli charging applies to actual probe innovations. Thus the entire pre-outer-decoder payload channel is a correlated Pauli channel with input-independent weights, and expected number of nonidentity service-block errors is at mostC=m*q/(1-q). On every fault pattern of weight<=t, an outer stabilizer decoder returns the exact payload (including any external reference). On other patterns the decoder remains an actual CPTP map. Therefore the total decoded channel is (1-p_bad)Id+p_bad*Bad, with p_bad<=C/(t+1), giving half-diamond distance<=C/(t+1). A finite-cap failure supplies at mostdelta_cap extra distance by the same input-independent coupling, with fixed correctly sized outputs on abort.

This establishes the proposed mathematical composition if the source/controller interface meets the stated no-leakage assumptions. It still requires independent review of the latent-history factorization, and does not replace the earlier frozen receipt. If the original payload is correlated with source memory, the single-call identity still holds, but this input-independent correlated-Pauli channel decomposition is no longer asserted.

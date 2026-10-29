# Independent receiving review: finite learned-frame recovery architecture

2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler`. **Accepted as a conditional finite channel construction for the stated memoryless four-spin family, with ideal trusted controls and the explicit resource/availability qualifications below.** This is not broad unknown-noise fault tolerance, practical memory preservation, a hardware demonstration or a quantum advantage.

## Dependency status and actual port

I read the actual common-four-spin source derivation, singlet encoder/reset decoder, product-Choi PBT receiving review, history-uniform program receiving receipt, and the already reviewed homogeneous/heterogeneous transducer interfaces. The history-uniform receipt is now present and accepted at its stated IID scope, rather than still pending. This review does not silently promote any stronger arbitrary-memory or control-noise claim.

The SAME memoryless four-spin source supplies acquisition and service. Its pair-label second moment is exactly the required isotropic law; it need not equal the full SU2 Haar twirl on arbitrary four-spin operators. Its24 collective Clifford elements nevertheless fix the total-spin-zero sector exactly. The source is fixed across calls, with a fixed unknown local frame W and fixed eta. A valid eta<=eta_U bound is a condition of the theorem. If obtained statistically, confidence failure and calibration calls require separate accounting; conditioning on later readiness must not silently preserve an unconditional confidence probability. Source-family membership is a promise, not established by one scalar flag rate.

## Preparation, resource independence and PBT

Preparing all resources before payload admission removes stochastic growth/transducer failures from the payload path. Each successful history-conditioned rotation program has the proved isotropic envelope; independent batches give conditional product inputs to the heterogeneous transducer. Discarding three outputs and retaining one per independent batch gives the conservative valid Choi interface. Reusing four outputs as independent ports would be invalid.

Full separate preparation transcripts can give different per-port channels E_i and different errors nu_i. The PBT receiving review already handles this: the delivered channel is sum_i E_i composed Gamma_i, where Gamma_i are ideal-product-resource CP branches summing to a TP map. For every input/reference state, the branches have nonnegative traces summing to one, so channel error from these resources is bounded by max_i nu_i, not their sum. The ideal PGM contributes at most3/(N+3), giving e_g=nu+3/(N+3) with arbitrary references. This does not assume all port errors identical.

Conditional on complete preparation histories, distinct consumed gate resources factor, and the memoryless service source gives product channel uses. The initial unknown frame is a fixed parameter, not an uncharged random shared environment. Work registers must be reset/discarded between independent subroutines as specified; uncontrolled shared quantum storage or source memory would invalidate factorization. Averaging over coarsened success histories need not preserve independence, but uniform conditional performance bounds may be averaged AFTER proving them branchwise. The same applies to the full encoded payload, not just product inputs.

## Gauge cancellation and inner channel

With W_rel=I tensor(V1V0†) tensor(V2V0†) tensor(V3V0†), W=W_rel V0^tensor4. Collective SU2 acts identically on the singlet code, so W E0=W_rel E0. Thus the three star-relative frames suffice. Choice of SU2 lifts changes only irrelevant global phases, not the encoded channel. No absolute root frame is assumed. The canonical reset-completed D0 is CPTP on all outputs, not merely an inverse defined on the code.

For perfect frame gates, T_W is identity on the encoded port and depolarization produces the fixed D0(I16/16). Known logical Pauli conjugation averages that replacement state to I2/2 while preserving the identity branch. Therefore the ideal closed channel is exactly(1-eta)id+eta D2 and has nonidentity Pauli probability3eta/4. Independent exact symbolic checks on nontrivial rational SU2 frames verify the gauge equation. With reset state logical0 the replacement is diag(15/16,1/16), whose Pauli average is I2/2; the general argument does not require this particular reset state.

Replacing the three forward and three inverse local gates by maps within e_g in half-diamond distance changes the inner channel by at most6e_g. This is a six-step channel hybrid; CPTP encoders/decoders/source and arbitrary references are covered. Fresh independent logical Pauli twirling, with the key retired as specified rather than conditioning the code analysis on its value, produces a genuine Pauli channel and contracts that distance. For Pauli channels, half-diamond distance is the total variation of their Pauli weights, so the nonidentity probability obeys p<=3eta_U/4+6e_g. Neither the physical depolarizing part nor imperfect control is erased by the twirl. Additional implemented known-control errors must be budgeted; the current theorem treats those controls as ideal.

## Ordinary five-qubit correction and concatenation

The four specified stabilizers commute and generate a group of size16 without -I; thus their joint +1 space has dimension2. The15 one-site Paulis exhaust the nonzero syndromes. Correcting each observed syndrome by its assigned one-site Pauli corrects all weight-zero/one errors. XXXXX and ZZZZZ supply an anticommuting logical pair.

I independently enumerated ALL1024 five-qubit Pauli patterns, not just the15 generators of the error set. Every syndrome-corrected residual lies in the normalizer and induces a logical Pauli. Counts of nonidentity logical results by physical weight0,...,5 are0,0,90,210,270,198. Benign higher-weight patterns are allowed; the bound does not assume they all fail.

Given five independent possibly nonidentical Pauli ports, each with nonidentity probability at most p, a nonidentity logical result requires at least two physical nonidentity errors. Union-bounding the ten pairs gives p_next<=10p². Disjoint block processing preserves product channel structure conditionally on preparation histories, including for entangled encoded inputs; no independent-input-state assumption is made. Induction gives p_L<=(10p)^(2^L)/10 with K=5^L service calls. Its half-diamond error equals its logical nonidentity probability. The condition p<1/10 is essential. Even with arbitrarily accurate learned gates, this sufficient criterion requires eta_U<2/15; it is not a theorem for every eta<1.

This is conventional channel-use QEC with ideal known syndrome/control circuitry, not a fault-tolerance threshold for noisy gates or a lifetime guarantee for an uncontrolled physical memory. Primary code source checked directly: Laflamme et al., https://arxiv.org/abs/quant-ph/9602019. No code novelty is claimed.

## Explicit finite preflight accounting

Let P=6KN be the number of consumed Choi ports. To make the source-call accounting fully explicit, suppose one history-certified rotation-program routine has a deterministic cap C_R ordinary calls and success probability at least1-a. Two fresh routines and one transduction form a Choi-port attempt using at most2C_R calls. Conditional success is at least

s=(1-a)^2 p_trans(v_U)>0,

where p_trans is the accepted transducer lower bound, at least2/9 on the admitted error range. The history-uniform quality envelope remains valid on every successful attempt; discarded failures never see the payload. With q fresh capped attempts per port, total preparation abort probability is at most P(1-s)^q. A finite q can make this at most any prescribed delta_pre. Total ordinary acquisition calls are bounded by2PqC_R; add K service calls and any separate calibration calls. This is a sufficient paid schedule, not an expected-cost-to-deterministic-cost shortcut. It does not assert that a cap preserves the uncapped average output state.

All P resources are retained before payload admission. The lower bound2P=12KN protected program qubits is correct, with acquisition/transducer/PBT work, outer-code buffers, resets and readout additional. Source calls cannot be counted only as K. Resource failures constitute an availability flag before admission; the logical-error bound describes service after readiness. An inclusive flagged specification must retain preparation abort rather than silently call it successful transmission.

For eta_U=.01 and e_g<=1/2400, p<=.01. Splitting e_g equally gives nu<=1/4800 and N>=14397. Independent exact count checks give:

| L | Service calls | Logical error bound | Choi ports | Program-qubit lower bound |
|---:|---:|---:|---:|---:|
|1|5|10^-3|431910|863820|
|2|25|10^-5|2159550|4319100|
|3|125|10^-9|10797750|21595500|
|4|625|10^-17|53988750|107977500|

These omit neither the conceptual acquisition cost nor the need to multiply it by the port count; actual native-control costs remain additional and enormous. No full multi-million-port device was simulated.

## Remaining limitations and conclusion

The protected controller already has enough trusted quantum storage to bypass the source for a small payload. This construction therefore does not demonstrate a generic storage advantage; its legitimate capability is paid transmission through the specified unknown-frame noisy port, assuming that use is required. Equally informed classical frame estimation and reusable classical controls remain strong competitors. No environment tomography is required, but no superiority over calibration is proved.

The accepted conclusion is finite availability and arbitrarily small conditional service error for the stated sufficiently low-noise memoryless family, with paid trusted program preparation and ideal known control. Arbitrary retained source memory, family misidentification, model drift, realistic control faults, scalable native synthesis, useful overhead and practical/quantum advantage remain outside scope. The new exact code/gauge checks support interface consistency, not those broader claims. Original sources were left unchanged.

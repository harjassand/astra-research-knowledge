# A finite joint-payload service through retained quantum memory

28 October2026. **NEW PROOF CANDIDATE, dependent on the separately reviewed fast bandit construction.** Zero acquisition samples. This formalizes the earlier unreceived `prequential_mixed_service_bridge_scratch_20261028.md`; it does not alter that saved derivation or any received source.

Dependency: `ordinary_prequential_small_loss_decoder_bandit_20261028.md`, frozen SHA6edb6a3af1118947c1a864113a24d77eef437386eafb7d8694a4aa651dc8d1dc. Its finite rational whitening/prox and physical decoder-return controller is under independent main/statistics review. Only its actual conditional bit law, exact local-norm estimator, finite certified mirror step and receiver synthesis are imported. No result is received merely by this dependency citation.

## 1. Service, independence, and costs that cannot be hidden

There are q>=1 unknown logical input qubits, possibly arbitrarily entangled with each other and with a reference R. Their FULL joint Q_1...Q_q R state is initially product with the retained source memory and all fresh private controller randomness. The inputs are held in trusted isolated storage until individually sent. Each recovered output is immediately stored outside ALL future source interactions and controller feedback. No later test, recovery choice or source control measures or reuses a delivered payload output.

The actual source has the same known w-qubit output patch (d=2^w), fixed encoder, complete causal CPTP retained-memory interface and current private-control boundary as the one-terminal construction. TEST and USE enter through the SAME complete physical source port and timing/control schedule. A current role/key/decoder label must not select a different external source map or leak through another port before that call is complete. Quantum discrimination of the input is included in the same map, not prohibited by fiat. Past disclosed records and quantum memory may affect later calls arbitrarily.

The learner applies an actual compiled exploratory CPTP decoder on EVERY active call. On TEST it uses an ordinary six-state input and the one-bit mismatch measurement; on USE it sends the next held unknown qubit and does not measure the decoded output or update from it. The encoder/decoder choice is fixed before the current call. Fine probe records may be retained or retired according to a declared controller; the proof conditions on the actual records it uses. It does not require complete TEST/USE memory-instrument equivalence, matching fine outcomes, or an all-probe occupation law.

The protocol terminates after q COMPLETED PAYLOAD ATTEMPTS, regardless of their unknown correctness, or at a deterministic call cap N. There is no supplied noise flag and no test of whether a payload was correctly recovered. If fewer thanq USE coins occurred by N, the missing output slots receive physical replacement states; the corresponding unsent inputs are discarded. Trusted storage is not treated as a free transmission/bypass channel.

The objective is the averaged JOINT q-input channel, not independent marginal promises. Optional private Pauli framing in §6 gives a changed averaged joint service with a dimension-free diamond guarantee when its global Bell loss is small. No capacity/indefinite-stream statement follows.

## 2. Actual mixed occupation and importance-weighted learning

Use k=2d and D=3d² as in the bandit source. Let A_t be the predictable indicator that fewer thanq USE attempts have occurred before round t. In an analysis extended toN rounds, inactive rounds have zero gradient and zero service loss; no physical source call is required after stopping.

While A_t=1, draw a fresh private USE coin with probability r, and TEST with probability p=1−r. Draw the exploratory decoder's i,z independently as in the bandit source, fixing that physical decoder before the source call. On TEST acquire its actual mismatch bit y and use the coordinate gradient ghat/p. On USE do not acquire a gradient. Thus the actual update record is

    gtilde_t=A_t I_TEST ghat_t/p.                        (1)

For the current source channel E_(t,h), defined on the global Choi experiment below, let q_t(C)=(2/3)ell(D_C E_(t,h)). The new occupation law h includes the actual mixed roles and test outcomes, not the old all-probe histories. Conditional on the prior history,

    E[gtilde_t|h]=A_t grad q_t,
    E[||gtilde_t||_(H_t^(-1))²|h]
                  <=(8D²/p) A_t q_t(C_t).              (2)

The learner's physical action is the sampled exploratory decoder, whose mean Choi equals C_t. This equality does not substitute a different receiver on an actual payload.

Define the cumulative marginal comparator

    C_N(D)=r sum_(t=1)^N E_h[A_t ell(D E_(t,h))].         (3)

D is FIXED, and the memory states are those ACTUALLY visited by the DECLARED IDEAL TRUSTED-INTERFACE mixed-service controller interacting with the given unknown noisy source. “Ideal” here refers only to its specified preparations, classical updates, controls and storage; the unknown retained-memory source is not idealized away. It is not an all-probe occupation or a counterfactual learning-policy trajectory. All bounds below, including the implementation-error and framed-service bounds(11),(14), retain THIS same comparator convention. A single whole-channel discrepancy nu transfers the service guarantee, but does NOT automatically replace C_N by a cumulative comparator evaluated on the physically imperfect controller’s different histories; that change could need an additional q-scale occupation/comparator debit. More importantly, C_N(D) is a SUM of per-use Bell losses, NOT the global entanglement loss of an oracle joint channel. Strongly correlated logical errors can make those quantities very different. No relative global-oracle comparison is claimed. Under the received uniform CP-order Pauli/gauge family, one fixed hidden decoder D_* is optimal at every conditional history, so it attains the infimum in(3). For the logical-noiseless member of that family, C_N(D_*)=0 even with coherent arbitrary retained gauge memory.

## 3. Global Choi proof, including earlier reference correlations

For analysis initialize q independent Bell pairs R_j Q_j and source memory in a product state with all of them. This is the GLOBAL Choi input of the complete q-input channel. It is not an entangled calibration resource used by the learner.

At an active round let j be the next unsent payload index. Conditional on every actual previous classical history, the untouched pair R_j Q_j remains exactly a Bell pair product with the rest of the quantum process. Earlier references and recovered outputs may be highly correlated with the source memory. These correlations remain present; they are not reset or replaced by a classical latent variable. The next pair is product because no previous operation has acted on it and the initial Choi pairs were product.

Therefore, on a USE at that history, the marginal current Bell failure is exactly ell(D_play E_(t,h)), where E_(t,h) is obtained from the ACTUAL conditional memory density operator. A TEST at the same history has the Bernoulli law in the bandit source. Both are fresh branches of the same causal map; the role coin and current decoder exploration are independent of the prior process. This proves(2) and the USE conditional mean while keeping the reference system.

After a payload is delivered, all future operations act outside its isolated R_j,O_j pair. They form a trace-preserving process when later outcomes are summed, even though each conditional later record can steer that pair. Consequently its FINAL marginal Bell failure, averaged over those later records, equals the failure at delivery. This is not an assumption that the later conditional states coincide.

Let S be the event that fewer thanq USE attempts occur by the cap, with probability beta. On its complement allq pairs have been delivered. The commuting Bell projectors satisfy

    I−tensor_j Phi_j <=sum_j(I−Phi_j).

Apply this on the completed histories; on S use only the bound1 for GLOBAL loss. Since every Bell-failure term is positive, dropping completion restrictions only increases the sum. The result is

    ell_global <= beta + (3/2)r sum_t E[A_t q_t(C_t)].   (4)

Shortfall is paid ONCE, notq beta. The right-hand side sums only delivered marginal failures before adding that one bad event. It does not pretend that separate marginal fidelities alone imply an independent product channel. The proof has used the actual joint channel, its full Choi reference, isolated outputs and the operator union bound.

Because the complete algorithm is CPTP on all q inputs, this analysis defines a genuine channel acting on arbitrary jointly entangled inputs. Conditional independence of arbitrary service inputs is NOT asserted; only the global Choi experiment has the untouched-pair product property used above. Without the optional twirl, global Bell loss does not become a dimension-free diamond guarantee.

## 4. Fixed caps, finite mirror update and loss accounting

Let rational 0<epsilon,gamma<=1 and define the integer

    L_short=ceil log2(16/epsilon),
    m_role=2q+8L_short,
    L0=ceil log2(16m_role/epsilon).                      (5)

Choose N to be the least power of2 satisfying

    N>=max{2m_role,1024m_role D² k L0/(gamma epsilon)},
    r=m_role/N, p=1−r>=1/2.                            (6)

At mostN independent Bernoulli role coins are needed. Imagine unused coins drawn too solely for analysis. Reachingq USE attempts before the cap is equivalent to at leastq successes among allN coins. Thus

    beta=Pr[Binomial(N,r)<q]
      <=exp[−m_role/8]<=epsilon/16,                    (7)

since m_role>=2q and m_role>=8log(16/epsilon). This coin-only event is independent of quantum correctness and does not infer successful recovery from a flag.

Use the SAME finite rational whitening/prox construction, but with

    eta=gamma/(128D²),
    zeta=epsilon/(16m_role),
    delta=eta epsilon/(64m_role).                       (8)

The maximum local gradient norm in(1) is at mostsqrt(8)D/p<=2sqrt(8)D, so eta||gtilde||*<=1/16. The same exact proximal existence/radius proof and fixed-grid rational residual certificates apply, with these actual parameters and this horizonN. All implementation counts are recomputed for them; they are not inherited with the old epsilon substituted informally.

The direct mirror-descent proof gives, for L=E sum_t A_t q_t(C_t) and any fixed comparator D,

    (1−8eta D²/p)L
      <= E sum_t A_t q_t(C_D)
          +zeta N+k log(1/zeta)/eta+N delta/eta.         (9)

Indeed the pathwise divergence bound is applied to the actual importance-weighted records, and the comparator is smoothed by(1−zeta)C_D+zeta C0. Only active-round losses appear; bounding sum A_t byN is conservative. Since8eta D²/p<=gamma/8, multiply(9) by(3/2)r and use(6): the three additive contributions before the factor(3/2)/(1−gamma/8) are at mostepsilon/16, epsilon/8, epsilon/64. Therefore

    ell_global <=(1+gamma)inf_D C_N(D)
                    +(39/112)epsilon+epsilon/16        (10)

for the ideal trusted interface, with C_N defined by its genuinely mixed occupation in §2. One WHOLE-PROCESS implementation discrepancy nu<=epsilon/2, measured in HALF-DIAMOND distance on the entire q-input service channel (or a stronger complete-process norm), yields

    ell_global <=(1+gamma)inf_D C_N(D)+epsilon.           (11)

For the noiseless common-decoder subfamily this is a true small global error bound onq temporal payloads under retained quantum memory. For general logical noise it retains the cumulative comparator in(3), which may exceed1 and make the bound uninformative. Nothing silently converts it to relative global oracle risk.

The cap is

    N<2048m_role D² k L0/(gamma epsilon)
      =36864m_role d^5 L0/(gamma epsilon).              (12)

The second term in(6) dominates2m_role in the stated range. This is near-linear inq, up to the displayed logarithms, at fixed local physical dimension and target. It is notq recovered qubits per call: each USE carries ONE logical qubit, and the rest are genuinely consumed TEST calls.

## 5. Paid randomness, storage, computation and controls

* Each active role coin is exact: draw a uniform integer in{0,...,N−1} using log2N fair bits and declare USE iff it is belowm_role. No unbounded rejection or source-correctness-dependent stopping occurs. At mostN such draws are charged even when the protocol stops early.
* Decoder direction i and six-state axis j use the fixed capped integer samplers of the fast source, with a shared global sampler discrepancy allowance and the new N. Each current direction/input sign is fresh. On a USE, drawing and retiring dummy axis/sign coins can equalize the public schedule if necessary; their bits are included in the worst-case count. An explicit cap before optional framing is N[log2N+2+R(ceil log2D+2)] with R=ceil log2(4N/nu_rng).
* At mostN complete source calls, w physical output qubits per call, one actual compiled CPTP decoder per call and at mostN ordinary return measurements. No protected calibration reference and no source-memory reset. q input qubits are supplied as the actual service; up toq input-storage andq isolated output-storage slots are conservatively paid, distributed across the endpoints. The reference R is not manipulated or supplied to the learner as an acquisition resource.
* The received finite rational center/direction/prox algorithms apply with horizonN and learner-only interior bound2^(-(N+2))/(2d). Their classical cost is polynomial inN,D and numerical bit precision; it is not claimed near-linear inq. Every dense receiver is synthesized with environment at most2d, a unitary embedding at most4d, at most two additional local reset qubits and O(poly(w)4^w) gates before precision/routing overhead. This is exponential inw.
* All actual source-preparation/decoder/measurement/storage errors, capped sampler exhaustion and any trusted classical numerical implementation discrepancy fit ONE complete adaptive-process allowance nu. This allowance is uniform over arbitrary JOINT payload inputs and untouched references: the resulting actual and ideal q-input service channels differ by at mostnu in half-diamond distance. A merely Bell-loss or calibration-trajectory allowance is insufficient for the diamond claim below. Complete local control/instrument error bounds, extended over every future-accessible memory, telescope through arbitrary intervening causal source maps; capped sampler discrepancies couple with their uniform abort probability. The storage/key/routing boundary is included, not inferred from gate fidelity alone. Finite rational certificates are checked on every history. A failure fallback remains physical, but an unearned numerical optimizer guarantee is not declared statistical success. The long duration of holding unknown inputs and isolated outputs is a real resource limitation.

## 6. Optional changed-service global Pauli guarantee

Choose2q fresh private key bits, independent of the inputs, source and all learning coins, defining Paulis P_1,...,P_q. The learning/control policy must NOT use these key values, expose them to the source, or receive feedback from a payload output. Apply P_j immediately before that input's eventual USE, and P_j† after its actual decoder before isolation. Missing-slot replacement outputs also receive P_j†. At separated endpoints the same key must be available through the stated trusted private-control/shared-key interface; this secret classical resource is charged, not silently assumed to travel through the unknown source.

Let Lambda be the complete UNFRAMED adaptive q-input channel, including role stopping and missing-slot replacement. Each future input frame commutes through all earlier operations that do not touch that input. Each output inverse frame commutes through all later operations because that output is isolated. On a shortfall branch an unused input frame disappears under discard, but its replacement OUTPUT frame remains essential. Hence, for EACH key tuple, the actual framed service equals

    Ad_(P_1† tensor...tensor P_q†) composed with Lambda
              composed with Ad_(P_1 tensor...tensor P_q). (13)

This equality concerns the full adaptive channel, not only input marginals or scalar failure rates. At the global Choi input the input frame can also be moved to its untouched reference, so tracing the references leaves the same actual classical record law; no new all-probe occupation is assumed.

Averaging the independent private keys gives the conventional global Pauli twirl of the IDEAL declared service. It preserves global Bell fidelity and yields a q-qubit Pauli channel. For such a channel the half-diamond distance from identity equals its total nonidentity Pauli weight, which is exactly its global Bell loss. The actual finite-control framed service need NOT remain exactly Pauli. Require the SAME single allowance nu to bound its half-diamond distance from that ideal framed service, uniformly over joint inputs/references and the actual complete frame/key interface. The triangle inequality then chargesnu once, so the averaged actual CHANGED service has

    (1/2)||Lambda_twirl−id||_diamond
       <=(1+gamma)inf_D C_N(D)+epsilon.                 (14)

This is not a guarantee conditioned on the secret key, not free authentication, and not a claim that an untwirled Bell-loss bound was dimension-free. The actual trusted Pauli controls, secret bits, replacement framing and output isolation are load-bearing operations.

## 7. Comparison and current evidence

The equally informed conventional competitor is the same small-loss decoder bandit and private-role controller with the same storage/secret-control access. Abstract bandit methods, Pauli twirling and operator union bounds are prior machinery. The new composition sought here is finite ordinary TEST acquisition followed by multiple genuine entangled USE inputs on one unreset retained-memory process, with all controls paid and no process-model reconstruction.

It is complementary to the acquired predictive-model branch: no full-process restart, core-rank/conditioning certificate or physical memory reconstruction is supplied here; equally, this controller does not learn a policy-planning model or optimize an encoder. Known local output access, fixed encoder, trusted holding and strict output isolation remain strong structural premises.

Author deterministic evidence is `prequential_mixed_service_channel_check_20261028.py/.json`: two full logical inputs and their full Choi reference, one coherent retained memory qubit,3- and6-round caps, actual ordinary six-state test instruments and a decoder depending on prior mismatch parity. It enumerates all roles/outcomes through their CP maps, not source samples. The final delivered-marginal accumulation residual is below2.3e−16;32 actual key schedules match the algebraic full-channel frame identity, and the twirled global Choi offdiagonal residual is below2.2e−17. This is a generic coherent-memory diagnostic, not a learned-bandit performance run or an oracle-family experiment. Independent channel/composition and statistics reviews are required before receiving.

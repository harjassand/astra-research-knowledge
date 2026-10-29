# Resource-first finite retry with changing learned candidates
2026-10-29. New composition construction, awaiting independent receiving review. This compiles existing guarded operations; it does not invent teleportation, distillation or heralded channel correction.

## What prior Astra already supplies
The actual `learned_pauli_algebra_compiler_20261029/MIXED_ROLE_SERVICE_THEOREM_v1.md` and `DEFERRED_RESOURCE_FAULT_TAIL_v1.md`, with their independent reviews, already prepare isolated Bell resources before accepting unknown payloads. Their unkeyed deferred-Bell theorem concerns final Bell-label statistics under a common Pauli algebra, NOT equality of full resource states. We do not promote it to such an equality.

Astra N1023/U1023 complete coarse-instrument equivalence, actual source TheoremB lines58–107 and obstruction lines188–196, already establishes entanglement-first versus Pauli-encrypted service under its exact interfaces. It explicitly prices reference storage, terminal correction and record privacy. The current construction instead uses the FULL accepted-operation diamond certificate of the newer arbitrary-source guard, then composes finite changing-candidate attempts. The old common-algebra resource factory remains a different useful mechanism.

## Primitive and assessed registers
For any chosen implementable candidate encoder/decoder and any current source-memory state, suppose a finite guarded operation has accepted map G_i satisfying

 (1/2)||G_i - id_L tensor B_i||diamond <= epsilon_i.

L has fixed dimension2^ell. B_i is the actual accepted coarse source-memory/controller map under the governing guard theorem; outer decoder syndrome/trash and private twirl keys have been retired as required. A uniform simulator memory map could also be used if that is the primitive's precise proved target, but it must be stated rather than silently substituted. The bound must be uniform over initial L-memory correlations and external references. The actual rejection map is retained as an actual CP instrument branch, not replaced by an ideal bath reset. All native-call caps and control-error allowances are included in the primitive.

Prepare ell perfect local Bell pairs R:L independently of current source memory. Send only L through the complete outer-encoded guard. Keep R isolated. The accepted resource-generation map A_i:M->R,L,M' then obeys

 (1/2)||A_i - (Phi_RL tensor B_i)||diamond <= epsilon_i,

by fixing the primitive's logical input to one half of a maximally entangled state. This is a FULL joint resource-and-source-memory trace/diamond statement, not merely a Bell fidelity statistic. It remains valid with an arbitrary external reference entangled with M.

## Finite first-success protocol without a future-source oracle
Choose a finite maximum A attempts, deterministic error allowances epsilon_i with sum<=epsilon, finite acquisition-call caps, finite guard-call caps, and a common requested output size ell. At attempt i:

1. Acquire an allowed further bank of fresh known probes. Maintain previous classical counters if desired. Source memory is not reset. Candidate construction is any fixed measurable function of actually acquired classical records (e.g. the existing product-Pauli estimator, proper-polar rounding and a declared fallback). It cannot inspect simulator bath states or future source maps.
2. Freeze that candidate for the attempt. Prepare fresh encoded Bell resources and run its finite guard at error budget epsilon_i. On rejection, discard all that attempt's resources, keep only the allowed actual classical acquisition/controller records, and continue if budget remains.
3. On the FIRST acceptance, isolate the resource and stop all source/acquisition calls. Only now accept the unknown payload D, Bell-measure D with R, communicate the2ell classical outcomes, and apply the receiver corrections. The resource is consumed once. No postselection on outer-decoder success or teleportation outcome is added.
4. If allA attempts reject/cap out, return NO RESOURCE. No unknown payload was sent to the source. If a payload was already waiting in a trusted buffer, the physical operation on it was identity during preparation; for initially correlated D:M states the conditional outcome can still steer D through an operation on M, so 'untouched' is not a claim of conditional statistical independence.

Acquisition history may determine candidates, further calibration length within caps and trusted parameters. Soundness needs neither a correct learned frame nor a stationary/common-algebra source. Those structural assumptions can support useful yield, but are not inferred from accepting a resource. Every chosen primitive must meet its uniform declared interface and allowance.

## Composition proof
Let R_<i,h be the actual trace-nonincreasing memory map of reaching attempt i with allowed classical history h, including previous rejected-resource instruments and intervening acquisition. The histories are disjoint and sum to a trace-nonincreasing map. At each history replace only the accepted resource map by its certified ideal Phi tensor B_i,h. By the uniform bound and trace-norm contraction, the contribution at attempt i to the full first-success output difference is at most epsilon_i times the probability mass reaching that attempt, hence at most epsilon_i. Sum over disjoint histories and success indices. The all-rejected branch is left EXACTLY actual and does not act on an as-yet-unsubmitted payload.

Therefore the complete finite resource factory, including first-success index and NO RESOURCE flag, is within half diamond distance sum_i epsilon_i of an ideal factory producing an exact Bell resource on each success branch with the specified memory map. Trusted teleportation is a CPTP postprocessing, so the completed finite payload instrument obeys the same bound. This is a subnormalized/flagged operational guarantee, not epsilon conditional on an arbitrarily rare success. Dividing by success probability requires a separately justified lower bound and the appropriate normalization analysis.

The preceding proof permits arbitrary changing source memory and candidates. It does not substitute an iid geometric waiting-time model. A fixed per-attempt epsilon repeated without a finite/summable allocation is unsafe: a device can reject with probability1-epsilon and accept ONLY an orthogonal Bell resource with probabilityepsilon. Each attempt has accepted distanceepsilon from its ideal accepted branch, but the first acceptance after unlimited retries is wrong with probability1. The supplied exact-rational example quantifies the finite amplification.

## Concrete finite35-qubit compilation
Keep the reviewed inner n=4,K=2 code and outer GF32 [[31,7,13]] code: J=155 service blocks, ell=35 output qubits, correction radius t=6. Choose four resource attempts, b=0 permitted test failures, R=2/3 at each. The per-attempt source-induced accepted error bound is

 (R/(1+R))^(t+1)=(2/5)^7=128/78125.

Total four-attempt allowance is512/78125=0.0065536<1/128. For a six-state witness C=3/2 choose service probability s=R/(C+R)=4/13; for matching C=2 choose s=1/4. Finite caps only add abort, not accepted soundness error. For exampleL_i=ceil((2J+256)/s) yields1840 calls for six-state and2264 for matching. This does not guarantee acceptance.

A concrete oracle-free acquisition schedule adds known-probe calls to cumulative totals1000,10000,100000,1000000 before attempts1–4; guards interleaved between those banks alter the actual bath history, so the earlier uninterrupted-prefix simulation cannot be reused as this protocol's yield. The candidate is constructed from the actual accumulated probe counters. Product-probe setting privacy, common native ports, trusted finite controls and output register typing remain required. The supplied controller specification is finite and uses no futureU0 oracle; an actual adaptive-trajectory implementation is separately identified if executed.

## Physical bill and limits
For ell=35, resource-first adds35 locally protected reference qubits during each attempt, on top of outer encoding/buffers and the inner four-qubit port. After acceptance retain35 receiver qubits until use, perform35 Bell measurements, transmit70 classical bits and apply35 corrections. Sender/receiver code workspaces, isolation, resets, all failed resources, calibration calls, control duration and storage error are charged. The maximal native source-call count is1,000,000+sum_i L_i; endpoint noise contributes its separately bounded complete-interface error. Resource aging after acceptance is a new storage interval, not free persistence of the certificate.

Public teleportation feedforward does not invalidate the FULL resource-state norm bound: retaining its classical record is CPTP postprocessing and the ideal Bell resource yields a uniform record independent of the corrected payload/memory. This is distinct from the earlier N1023 coarse-instrument substitution, where exposing fine records before such a full joint bound could change the memory process. Existing twirl keys, pre-certificate decoder syndrome and private preparation records remain subject to their original retirement requirements.

For communication, protected sender-side storage can be a natural separately supplied resource. For a single-location memory task, keeping35 clean reference qubits for the full duration may already be as strong a storage resource as keeping the35-qubit payload directly. Thus resource-first is NOT a self-bootstrapping solution to all quantum storage noise. Its actual benefit is avoiding destructive attempts on an unknown input at a specified asymmetric/assisted interface, not avoiding trusted memory.

## Sources
- Local governing mixed-role and deferred-resource proofs/reviews named above (prior00:11/02:09 source packages).
- Astra N1023 source SHA cde7f192676b414f607ea020d8b45c6bb6702b773c2cbef267a9b76e00b4899f, current revision1d03a0f1942512a1132478741373b73511a30935; actual TheoremB and decisive obstruction passages fetched2026-10-29.
- Bennett etal, 'Purification of Noisy Entanglement and Faithful Teleportation via Noisy Channels', arXiv:quant-ph/9511027, established distill-then-teleport paradigm. The new item here is the scoped compiler from existing current-port guard to finite changing-candidate first-success use, not historical priority for that paradigm.

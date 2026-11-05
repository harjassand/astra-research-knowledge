# Formal compiler and boundary supplement

This supplements `p3_construction.md`; it makes its hierarchy contract explicit. Arbitrary-input normalization and double-EC are credited to existing exRec machinery, particularly Balasubramanian–Davydova–Lake (Quantum 2026), Appendices B and C.1. The contribution tested here is the padded bounded-island implementation and its physical Poisson/finite-seed bridge.

## Lemma: a finite local arbitrary-fault amplifier

Fix a finite nearest-neighbor Boolean gate basis. Write an input circuit as synchronous, time-dependent Boolean update layers f_t on a line, using a fixed boundary convention. There exist constants a,c_0,w_0 such that, for every sufficiently large integer B and every integer U>=c_0 B, the explicit compiler C_(B,U) has the following properties.

**Geometry.** Each logical bit site is replaced by exactly B binary sites. Five separated sites hold Info; all others are workspace. Each logical layer is replaced by U layers from the same finite nearest-neighbor Boolean gate basis. The layout is a fixed finite template with B as a spacing parameter. Its node degree, local state alphabet and microscopic gate rate do not grow with hierarchy level.

**Decoder and regularity.** Let d_B be majority of the five Info bits, ignoring workspace. Let R_b be all physical block states in which at least four Info bits equal b; all workspace may be arbitrary. Encode b using five b replicas and zero workspace.

**Local window.** The output macrocell i during macrostep t uses a region W(i,t) of spatial half-width at most aB and duration U. It includes all input-normalization, message, holding, computation and final-commit operations. Every gate/color uses the same global pass barriers, and all output Info commits are simultaneous.

**Nice-field guarantees.** Fix an island width w>=w_0, and choose B sufficiently large compared with w. If the faults in W(i,t) fit in one spatial interval of width w and one temporal interval of width w, then:

(R) arbitrary incoming block states give output in R_0 union R_1;

(C) if each input block is in its corresponding R_b, output is in R_(f_t(b)).

**Arbitrary-field projection.** For any raw register-corruption support E and regular encoded initialization, the boundary-decoded trajectory is a noisy trajectory of the input Boolean circuit with fault support contained in

    P_(B,U)(E) = Bad_(B,U)(E) union N^+ Bad_(B,U)(E),

where Bad(i,t) means E intersect W(i,t) is not nice, and N^+ expands by one macrostep forward and by the fixed gate-input neighborhood. This support map is monotone and independent of corruption values.

### Proof

The compiler performs one normalizing refresh round and one logical round, each consisting of three independent decode/compute/broadcast passes. A refresh round computes identity of the decoded input; the logical round computes f. Keep Info fixed during all three passes, reset Work each pass, retain results in separate Hold tracks, and finally take local majority of the three Holds at the five output sites. Idle gaps exceed w. The five replica positions are separated by more than w, including the fixed local flattening guard.

For regular input, at most one initial bad replica and one newly corrupted replica occur per input; every clean pass decodes correctly. A temporal island spoils at most one pass globally and only one spatial output position in all other Hold tracks. The final vote is correct outside that position. This proves C for a round with regular input.

For arbitrary input, if the island hits normalization, the logical round is clean and computes the same f of fixed majority-decoded inputs in all three passes. Its output is a perfect repetition. If the island hits the logical round, normalization was clean and supplied perfect inputs, so regular-input correctness applies. Gap or commit faults affect only one replica. This proves R. The same argument preserves the intended value whenever the original inputs were regular, proving C for the two-round composition.

Let I_t(i) flag irregular boundary Info. R implies I_(t+1)(i)<=Bad(i,t). C implies a logical transition error at (i,t) can occur only if Bad(i,t) or an input I_t(j) occurs. Substitute the first inequality into the second to obtain P(E). This is an arbitrary-E statement; no global nice-trajectory premise remains.

### Concrete finite routing and closure

Use one fixed message lane for every input-replica message. Copy along nearest-neighbor paths to the fixed computation site, hold early arrivals, evaluate a fixed Boolean circuit, then broadcast along separate lanes to five output positions. Only finitely many neighboring macrocell routes share any physical location, so the lane count is a fixed constant. A global coloring serializes intersecting routes by a fixed factor, with all colors finishing pass i before the pass-i idle gap. Each pass takes O(B) time.

Represent the finite tracks by adjacent binary sites. Each multitrack update is a constant-size local Boolean function/permutation and has a constant-depth nearest-neighbor implementation. Info moves only within its constant-size microcell during this implementation and is restored after each simulated tick; long routes carry copies. The enlargement of any raw fault island is therefore a fixed guard. The recursively substituted circuit is this flattened binary circuit, including every workspace bit. It never treats the entire growing simulator state as one logical alphabet symbol.

Padding U beyond the active routine uses explicit identity/reset gates. After further compilation, those identities are themselves protected refresh gadgets. No long unprotected wait or per-level storage track is omitted.

## Corollary: recursive influence regions

Let E_0 be the microscopic fault-support envelope and E_(k+1)=P_(B,U)(E_k), with L_k=B^k and tau_k=U^k. A specified membership test in E_k depends only on E_0 in a fixed translated spacetime region. With fixed constants a_1,b_1 including the previous-period/neighbor guard, its half-widths satisfy

    rho_(k+1) <= a_1 L_(k+1) + rho_k,
    eta_(k+1) <= b_1 tau_(k+1) + eta_k.

Thus rho_k/L_k and eta_k/tau_k are bounded uniformly in k by geometric sums. Pick w larger than twice those uniform bounds plus the truncated-radius guard. Non-niceness at the next scale then provides two child tests whose truncated Poisson influence regions are disjoint. The recurrence and large-burst term in `p3_construction.md` follow with C(B,U)=O((BU)^2), up to fixed neighborhood factors.

## Initial workspace and scale-conversion boundary

The pointwise projection above has an explicit initial irregularity term if the initial encoding is arbitrary. That term must not be silently omitted for newly installed workspace.

For a constant logical reset f=0, every clean pass produces a zero Hold word independently of incoming Info. The same three-pass argument therefore gives output in R_0 from arbitrary incoming states whenever the reset macrostep is nice. Run the reset/normalization routine before any previously unused macrocell is read, and include this prewarming period in its dependence region and operation count. At subsequent scales use the same reset circuit substitution; its work registers are normalized/reset as ordinary mutable sites. Warm up scale 1 by a constant reset, then scale 2, and so on. The first reset at each new projected scale is constant, so its semantic correctness does not require a regular initial encoding; the ordinary initial-irregularity contribution is omitted only for this explicitly proved constant-reset case. After it, R restores the ordinary previous-Bad invariant. Failures of lower resets remain as support-envelope faults to be corrected by the higher scale; they are not union-bounded over every microscopic reset. A constant number of preliminary periods per scale therefore has total duration bounded by the geometric sum of tau_j. New level-k blocks can be prewarmed in parallel while the retained source is maintained at level k; these extra level-k identity/reset periods count in M(B).

More explicitly, do not replace this induction by a claim that one depth-k compiled reset works from an entirely arbitrary physical state with no initial boundary term. At stage j, lower-stage irregular encodings are already bounded by the preceding Bad_(j-1) support, so every lower-scale transition of the stage-j reset has the ordinary geometry-only support envelope. The incoming level-j decoded values may still be arbitrary; the constant-reset property is precisely what removes that value dependence. This establishes the stage-j output regularity bound, and hence the guarded interface for stage j+1. All resets at one stage run in parallel over the future block. This avoids a probability union over its exponentially many physical subblocks.

At an upward conversion, the lower-level projected circuit writes the exact next-level Info pattern and initializes its work registers on the event that none of its finitely many coarse locations fails. This is regular initial data for the next projection. Physical residues below that projection are already represented by lower Bad/ForwardNeighbor flags and the previous-period guard; they are not assumed erased. Downward conversion has the same guarded interface, ending at a fixed finite terminal circuit. Charge conversion failure by the union of the M(B) relevant coarse-location events and never condition the Poisson-pair independence argument on a successful history.

Algebraically, all ports use the same binary substitution: C^(k+1)(f)=C^k(C(f)). The upward adapter is C^k(Enc_B), where Enc_B is an ordinary nearest-neighbor Boolean circuit that writes five copies and zero workspace in a fresh B-site macrocell. The downward adapter is C^k(Dec_B), where Dec_B transports the five Info bits to a local majority circuit and retains one output. These adapters have O(B) child depth and O(B^2) child spacetime locations, including waiting identities and resets. Before and after an adapter, the underlying C^k blocks and their boundary decoders are identical. Only the outer grouping changes. Thus no ideal decode/re-encode operation is inserted at a scale boundary.

Use a fresh adjacent destination interval for each upward conversion. Prewarm that interval while the source runs compiled identity gates; reset masks never touch the retained source. For example, if the scale-k source occupies [s_k,s_k+L_k), take s_(k+1)=s_k+L_k and give the new source width L_(k+1). The union of all such intervals has extent at most a geometric sum O(L_K). Since L_k is divisible by every lower L_j, the newly introduced parent grid is compatible with the existing lower grids. Old source blocks can be retired only after transfer and reused on the downward ladder. Before reuse they receive the same staged reset; the current source remains separately maintained. A level-(k+1) identity while a smaller destination warms adds only a fixed number of charged rectangles.

Start and end each conversion at a child-macroperiod boundary. Introduce the new parent time origin at that boundary, and pad the finite encoding circuit with protected child identities if needed. The preceding child-period guard stays in every fault-support dependence region across the interface. These deterministic phase choices are part of the input-independent schedule and preserve the uniform influence bounds; they do not create a fresh stochastic origin or erase earlier faults.

All finite-horizon hardware, its blank initialization, schedule compilation, working gates, waiting identities, conversion and terminal operations are counted. The only idealized protection is the immutable update-law/schedule premise already stated by P3.

The O(L_K) site count is the active binary-register array. An explicit list of scheduled local gates has O(L_K tau_K) instructions, with O(log T) address/time bits per instruction; it can be generated uniformly within a proportional polynomial bit cost. A compact recursive description is possible because the compiler template is fixed. Implementing a reliable controller for that description is outside the gate/schedule premise, and no assertion is made that it needs no additional hardware or energy. The claimed optimality comparison concerns spatial extent within the granted scheduling abstraction, not complete physical controller hardware.

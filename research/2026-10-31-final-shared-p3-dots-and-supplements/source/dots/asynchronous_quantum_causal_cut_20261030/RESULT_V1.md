# One-way quantum actuation with an asynchronous classical controller

2026-10-30. Independent construction attempt. Status: exact quantum-interface lemmas below; no autonomous universal-computation theorem. Existing accepted native memory and compiler results are not weakened.

## Useful result

A static, spatially unrolled circuit admits a quantum-safe replacement for classical copying and rollback: every gate transfers its input into a fresh, permanently assigned output bank and resets the consumed input. A repaired classical command may be replayed arbitrarily often, but its actuator never acquires access to a later circuit location's output bank. Once a good successor consumes a bank, arbitrary later operations confined to that bank are harmless to the already-transferred state. More generally an arbitrary set F of replayed modules has only O(|F|) quantum boundary ports, not an entire codeblock's worth merely because a command was replayed.

This is a locality lemma. It does not establish that the actual Gács controller supplies a sparse set F, a physical quantum causal cut, or adequate quantum waiting times. Those distinctions are essential.

## 1. Governing classical source, inspected in body

Primary source: Peter Gács, *Reliable Cellular Automata with Self-Organization*, corrected and strengthened manuscript, January 24, 2024:
https://cs-web.bu.edu/faculty/gacs/papers/long-ca-ms-24.pdf

Theorems 7.4–7.6 and Corollary 7.21 supply continuous-time classical reliability. Definition 10.3 and Lemma 10.5 give a deterministic damage-pair witness, not merely a marginal output bound. Lemma 16.4 and Corollary 16.5 bound attributed-colony progress away from higher-level damage. Theorem 8.1 explicitly retains both Cur and Prev. Section 18 copies classical messages. The simulation decoder can inspect bounded past history. None of those operations is automatically a quantum actuator.

For the source's notation, Lemma 10.5 has the condition

    epsilon* >= c_Dam [(B*/B)(T* / T) epsilon]^2.

Its proof finds two lower-level damage windows with disjoint enlarged supports. The pointwise indicator domination is a promising combinatorial receiver for a separately earned inclusive norm expansion. It is not itself a quantum/noisy-generator norm theorem.

The source is not replaced by the 2008 Cook–Gács–Winfree draft: that draft's introduction explicitly leaves its required local-slowdown bound unresolved. Wang 1991 was located bibliographically, but no claim here relies on an unread Wang proof.

## 2. Exact destructive-transfer channel

Let a circuit module g have input bank I_g and output bank O_g of equal finite dimension. Each physical bank is assigned to exactly one circuit wire segment. It is never recycled for a later segment. For a unitary gate U_g define, including an arbitrary reference R,

    T_g(rho_IOR) = |0><0|_I tensor
                  (U_g tensor I_R) [Tr_O rho_IOR]_(I -> O,R)
                  (U_g^dagger tensor I_R).

This is CPTP: reset O, SWAP I with O, and apply U_g to O. The same construction works for any CPTP channel Phi_g, after padding input/output dimensions and using its finite Stinespring implementation. It discards no unknown input. It does not copy it. The output-bank reset discards only the bank assigned to this new wire segment.

A local gate set and bounded fan-in give a fixed full footprint. Therefore the accepted exact native attempt compiler implements T_g on clean completed attempts using only its stated two-site Hamiltonians and onsite resolved resets. Its rollback acts on the finite current Stinespring prefix, not on previous unknown computation. Use the physical one-shot DONE latch to stop repeated nominal execution within a command window; the native two-SUCCESS witness supplies attempted-channel service, not command-window acceptance.

### Lemma 1: consumed-bank firewall

Immediately after a good T_g,

    rho_(I_g,rest) = |0><0|_(I_g) tensor rho_rest.

For every subsequent CPTP map A supported on I_g and any other already-consumed banks, with an arbitrary retained local environment, tracing those banks and that environment leaves the marginal of all later live banks and external references unchanged. This follows from trace preservation/no-signalling. No assumption about the unknown logical state is used.

The qualification 'already consumed' matters. A replay of T_g before its successor consumes O_g can destroy the live output. It is a real fault on that wire segment, not harmless idempotence.

## 3. Boundary-port lemma for arbitrary replays

Represent the target circuit as a bounded-degree DAG. A bank e belongs to the output of its producer and the input of its consumer. Assume a specified set F of modules may perform arbitrary joint-system/environment operations, at arbitrary times and arbitrarily often, on their fixed full footprints. Every module outside F must perform exactly one correct destructive-transfer map, and every edge whose endpoints are outside F must obey producer-before-consumer order. These are explicit premises of this lemma, not supplied by Gács in this note.

Then the computation outside F is an ideal circuit with an arbitrary, possibly non-Markovian boundary comb on at most

    sum_(g in F) (number of input wires of g + number of output wires of g)
    <= 2 k |F|

wire segments, for maximum bank arity k. For a geometric module footprint containing extra workspace, include the bounded number of neighboring banks it can touch; replace 2k by that fixed incidence constant.

Proof. Excise F from the circuit diagram. A retained gate consumes all its inputs, overwrites its outputs, and leaves the consumed inputs in a fixed product state. Its incident wire registers therefore have three phases: before production (overwritten before use), live between production and consumption, and after consumption (fixed disposable registers). Before/after operations can be included in the retained environment of the excised subsystem, while live-register operations cross only one of the incident boundary wires. Retained gates have the circuit causal order by hypothesis. Thus the excised dynamics can communicate with the retained circuit only through its incident boundary ports. Arbitrarily many internal events do not create additional ports. Keep the environment rather than assuming independent fault maps or a Pauli mixture.

This does NOT say an arbitrary bad gate is equivalent to a single instantaneous Pauli or even a single instantaneous channel at its original scheduled time. The comb may act at several boundary times. A threshold receiver must allow this bounded multi-port correlated fault, or absorb the adjacent gates into an enlarged bad rectangle.

Erasure/rejoin rule: if a module loses provenance, it may reset banks it owns only while the module is charged bad. Rejoining means returning its controller to the prescribed command for this same fixed circuit location, never relabelling an unknown bank as an earlier state. Descendants are not recursively erased. The boundary lemma bounds the resulting quantum damage provided the number of incorrectly actuated modules is itself controlled.

## 4. Why this does not yet close autonomy

### 4.1 A physical actuator is not a history decoder

Gács's decoded simulated trajectory can repair classical history, copy records, and infer a simulated transition from a bounded look-back. A quantum gate already applied in the laboratory cannot be undone by changing that interpretation. One must exhibit a physical output port and command latch whose good histories give the premise of Section 3 and whose bad histories are charged to finite enlarged damage islands. The source's classical output-error marginal alone does not supply this.

### 4.2 Pointwise correctness does not bound premature irreversible use

Even if a command is wrong with probability p at each of m separated checks, its probability of ever falsely firing can be 1-(1-p)^m. A future module that waits for the whole computation cannot simply latch the first asserted command forever. A valid adapter must overwrite stale pre-activation work, quarantine live inputs, and show that its first valid activation creates a fresh local cut. Otherwise pre-activation faults accumulate over the entire waiting lifetime.

### 4.3 Bounded attempted service is not bounded quantum waiting

The native compiler's two-SUCCESS theorem bounds attempted-channel service. It does not bound how long one input bank waits for another parent or for a valid classical command. Global reliable computation and eventual progress do not by themselves imply a uniform tail for this local exposure. In a causal DAG, completion times obey a maximum over predecessor completion times; a long remote delay may affect local waiting. An actual active-wire lifetime estimate is needed.

The existing accepted native memory protects unknown already-encoded states, but its live handoff is at deterministic/exogenous times. It cannot be silently substituted for a controller-selected handoff, and it does not furnish arbitrary logical gates. That remains a separate potential continuation, not an assumption of this construction.

### 4.4 Measurement records and feedforward

A concrete MBQC implementation must include the actual online capture, storage, copying and processing of each nonrepeatable measurement result. Gács's encoded-initial-input theorem is not automatically an online record-injection theorem. A corrupt classical bit with unbounded fanout can corrupt many quantum locations. The boundary-incidence constant must include its entire physically implemented, protected classical dependency network. Alternatively finite local CPTP modules can internalize bounded feedforward, but this does not eliminate large-scale QEC decoder dependencies for free.

## 5. A non-perfect resource-preparation component

For a bounded-degree graph, let

    U_G = product_(edges uv) CZ_uv,
    K_v = X_v product_(u neighbor v) Z_u,
    P_v^+/- = (I +/- K_v)/2,
    E_v(rho) = P_v^+ rho P_v^+ + Z_v P_v^- rho P_v^- Z_v.

Exactly,

    E_v = Ad_(U_G) o R_v^(+) o Ad_(U_G)^(-1),

where R_v^(+) resets v to |+>. Hence E_v are commuting, idempotent, bounded-support CPTP channels. The common fixed state is the known graph state. These are explicit finite channels available to the native attempt compiler, not a supplied perfect cluster factory. Conjugating a bounded-body local perturbation by the fixed-depth bounded-degree graph circuit only enlarges its support by a fixed neighborhood.

This algebra does NOT license leaving all pumps on during computation. A pump whose support intersects a measured/injected frontier can measure or erase the logical information. Pumps disjoint from the supports of all past measurements commute with those measurements and still stabilize the ideal residual state. Therefore a moving, physically controlled pump-off boundary is required. Faults in that boundary are local, but their number and exposure duration need the same missing causal-window proof. The included finite-dimensional check demonstrates the danger.

## 6. Required norm receiver, without assuming it

Suppose an actual physical adapter were proved to assign bad quantum modules F to enlarged controller/service boxes, each box incident to at most K quantum modules, and supplied a deterministic witness extraction compatible with the same nominal CP record expansion as the accepted cavity theorem. Then inclusive box bounds could be combined with the bounded-port lemma, yielding a constant-root degradation of local error strength of the form C q^(1/K), followed by a conventional circuit threshold receiver.

The words 'compatible with the same nominal CP record expansion' are load-bearing. A classical probability theorem does not imply this for coherent or signed joint-bath perturbations. In particular, one must not invent an actual nominal SUCCESS record after generic calibration changes. Lemma 10.5 provides deterministic witness geometry, but the physical classical-controller embedding, the actuator association, and the signed expansion compatibility remain to be proved.

## 7. Honest resource comparison and stopping status

Unrolling spends at least one distinct quantum bank per circuit wire segment: O(L) banks for a bounded-arity L-location circuit, before geometric routing and controller colonies. A d-dimensional scheduled layout ordinarily becomes a (d+1)-dimensional spacetime layout, or pays extra routing in d dimensions. No polylogarithmic autonomous-overhead claim follows. Each local channel may have an astronomically large but fixed compiler/controller alphabet.

Fault-tolerant MBQC already establishes that one-way computation plus a correct noisy classical feedforward implementation can meet a threshold. Nielsen–Dawson's in-body treatment explicitly uses buffered resource growth to control storage noise and handles errors in accompanying classical computation. Our unsolved gain would be native autonomous causal-window control, not one-way universality.

Verstraete–Wolf–Cirac's dissipative computation provides a time-independent local ideal computational construction, with a history-state clock and inverse transitions. Its stated relaxation gap scales as T^(-2). It does not, merely by being dissipative, furnish the fixed-strength continuous-noise threshold sought here.

No access denial blocks the mathematical work. The actual block is an unproved interface: establish a physical Gács-controlled actuation rule whose post-repair quantum cut and active-wire service satisfy Sections 3 and 6. Current notes deliberately do not assert such a rule has been constructed.

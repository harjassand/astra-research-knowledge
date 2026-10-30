# Leveled fresh-window cut: removing old inactive-bank accumulation

2026-10-30. Exact conditional semantic lemma and an identified norm interface. This is not a completed native autonomous threshold theorem.

## 1. Why levelling helps, and the extra ordering it needs

Take a circuit in levels, inserting identity-transfer modules on every idle wire. Give each directed wire its own permanent bank. A good level-l producer and good level-(l+1) consumer should use this bank within a bounded physical interval. A bad consumer may miss its deadline; do not make the rest of the fabric wait for its raw DONE. The missed incident bank is already an open bad port.

There is one additional freshness ordering. Refreshing the consumer only after its incoming unknown state arrives is too late: an inherited dirty prefix or cached RUN can touch the new state before refresh completes. Therefore every consumer must complete its fresh pre-ARM service BEFORE its good parents produce its incoming banks. Its finite vulnerability window starts at this pre-ARM, not just at its eventual RUN.

## 2. Explicit local schedule contract

For a module g let s_g be its pre-ARM start. The contract below is imposed only for modules declared good; it is the concrete contract the classical phase implementation must prove, not a supplied reliable schedule.

1. From s_g through a fixed fresh-service span A, the actual command is ARM. The full-footprint native implementation keeps refreshing, clears old private work, and produces the required actual fresh completions. All native owners that can retain a DATA-moving prefix on g's footprint are included in this test.
2. No good parent produces an input of g before s_g+A. No good child produces an action consuming g's output before g's designated production.
3. After pre-ARM, g's command passes through HOLD (or remains ARM) into one RUN band. HOLD is DATA identity and preserves ARMED. ARM is forbidden after RUN begins until the circuit's use of g is over. The actual common command/latch lock serializes observations and writes.
4. g has its actual correct accepted completion by s_g+H, for a constant H. Its good children have their corresponding completions by s_g+H' for another constant H'. These are deadlines of the virtual phase program; they do not wait for an untrusted native DONE.
5. While the relevant bank is live, the complete good native footprints are free of the perturbation and satisfy the required service/cleanup tests. All remaining partial transactions crossing a boundary are included in the marked neighborhood.

All constants may depend on fixed controller/gadget parameters, but not on circuit width, depth, or elapsed runtime. Whether Gacs's one-dimensional source can realize this contract on a desired geometrically local leveled layout is a separate obligation.

## 3. Freshness and permanent-bank lemma

Suppose the preceding contract holds. Let F contain every module whose contract fails, plus the fixed native overlap neighborhood needed to include compromised partial transactions.

For every edge between two modules outside F:

* all old malformed local work has been retired before the bank's legitimate production;
* the producer resets the fresh output bank, transfers its input into it, and applies its gate;
* until consumption, every good module has exactly its intended guard behavior;
* the consumer performs its intended destructive transfer, leaving the input bank disposable.

Thus the edge is an ordinary open-circuit wire with only a bounded physical live span. No error budget from the entire earlier lifetime of that bank is needed. An early false run can alter dormant banks and an old latch, but a later legitimate producer overwrites dormant quantum contents and the fresh pre-ARM service overwrites the actuator provenance. A false run that touches an already-live input is NOT erased from the accounting; it is an incident bad port.

Proof of the old-history erasure statement is channel-theoretic. For a dormant output O, the producer begins with R_O(rho)=|0><0|_O tensor Tr_O(rho). Any correlations of O with a retained bath/reference are removed from O by this map, without resetting that bath. The bath's subsequent interactions are retained in the bad comb or in separately charged local perturbations. For an input already consumed and decoupled by the correct destructive transfer, later trace-preserving operations on the disposable input and retained environment cannot change the already exported marginal. If that environment later touches another live bank, that interaction is an explicit port/noise contribution, not an invisible erased event.

The full physical process therefore consists of the good open circuit contracted with an arbitrary retained comb on the bounded ports of F. This is the receiver in OPEN_TENSOR_CORRECTNESS_V1.md. It is not a causal gate-fault replacement theorem.

## 4. Bounded incidence, conditional on a real local schedule

If the controller's single-island wake and each native fresh window have bounded spatial and temporal extent, each physical defect box can invalidate only a fixed number R0 of these contracts. Each quantum location sees only a fixed number M of such windows, even if its absolute activation time is very late. An island may cause many attempts at one permanently assigned module; it cannot retarget successively new quantum identities.

This geometric statement is distinct from a norm bound for windows chosen at late random times. A bound on deterministic spacetime boxes does not by itself license summing over a randomly selected box without paying for all candidate times.

## 5. What the primary classical source actually supplies

In the corrected/strengthened Gacs manuscript (2024):

* Definition 7.9 defines a constraint process with a stopping time sigma and a window/type measurable at sigma, wholly in its future.
* Definition 7.10, equation (7.11), gives the product bound for disjoint such adaptive windows, including conditioning on prior events. The window cannot be selected retrospectively after seeing its faults.
* Definition 7.13, equation (7.13), requires a pointwise domination of each higher violation by a sum of products of lower violations in disjoint lower windows. The witnesses themselves are constraint processes.
* Theorem 7.2 preserves the strong-trajectory property under this canonical simulation. Propositions 7.11 and 7.12 establish it for the source classical Markov media.

These passages do support fresh windows started by a genuine nonanticipating classical phase, rather than a union bound over the entire program lifetime. They are not just a fixed-time output reliability theorem.

## 6. Exact remaining physical seam

The reviewed CP-cavity theorem currently defines its compatible family G_A on a deterministic tiling of physical time. Its good boxes preserve actual nominal SUCCESS instruments only inside their analytic cavities. It has NOT yet been proved that one may:

1. select a cavity's on/off times using a phase history that itself changes when that cavity is inserted;
2. retain a common genuine stopping instrument under all members of the cavity family;
3. preserve the mixed noise-restoration identity and the uniform derivative bound without extra terms from the moving selector;
4. establish the global inclusive signed bound for the resulting fresh quantum windows.

A formal call to a classical strong Markov property does not close these points for coherent joint-bath perturbations. Nor may one assign imaginary nominal jump records to the actual perturbed generator. One sufficient route would be a proved actual CP stopping instrument with a compatible cavity extension; another would be a deterministic-time causal-witness argument that avoids summing over all possible activation times. Neither is established in this note.

The other remaining geometric seam is explicit: the source controller is one-dimensional. The serial phase wave in SINGLE_ISLAND_COMMAND_CUT_V1.md is a valid chosen target program, but has long live waits on an arbitrary wide quantum circuit. A local two-dimensional leveled fabric needs an actual controller/routing construction with bounded local phase skew. Serializing that control through a long one-dimensional path and calling its growing delay a constant is not allowed.

## Bottom line

Levelling plus PRE-production actuator freshness removes the need to charge old dormant quantum banks forever, and gives an exact bounded-live-span open-circuit statement. The unsolved part has narrowed to a real bounded-skew classical schedule on the chosen geometry and a strong/adaptive version of the native signed cavity contract, not to copying or rewinding unknown DATA.

Primary source: https://cs-web.bu.edu/faculty/gacs/papers/long-ca-ms-24.pdf, Sections 7.2-7.3.

# Early physical-consequence audit — NOT a useful-cost memory yet

## Decision first

The witness construction may establish a new abstract fixed-controller capability, but its PRESENT constants and primitives do not establish practically consequential self-protecting memory. There is no verified finite code instance, native interaction implementation, or competitive noise threshold in hand. The conservative certified route is catastrophically expensive. Do not promote bounded-degree expander locality to 3D physical locality, or finite local lookup tables to cheap noisy controllers.

## Actual primary inputs

Leverrier–Zémor v3, https://arxiv.org/pdf/2208.05537, Theorem6 provides an explicit entropy-based robustness constant for random local codes asymptotically in Delta. Theorem1 assumes Delta large enough; its distance bound scales as delta^2*kappa_rob^2*n/(256*Delta). The decoder proof also invokes large-Delta inequalities. No numerical small-Delta pair, tested product expansion certificate, or hardware circuit is supplied by the inspected statements. These are existence-family inputs, not a chosen runnable instance.

## 1. Quantitative audit of the actual current proof constants

Take source local-rate parameter rho=1/4, yielding nominal quantum rate lower bound (1-2rho)^2=1/4. Set delta=.03 (below H_2^{-1}(.25)=.04169269027), decoder epsilon=1/12. Theorem6's displayed guarantee evaluates to

kappa_rob = 4.8199937853e-6.

This is a GUARANTEED conservative robustness constant, not a measured property of an actual finite local code. The corresponding A=1+1/[kappa_rob(1-epsilon)] is about 226330.98.

Use the witness proof's conservative basin density r0=R_n/n, move support bound b=2Delta^2, and drift denominator K=8Delta^4+2Delta^2+1. For a boundary at reduced radius R_n/4, its potential density is at least w_bar=r0/(8Delta^2). A one-site data Y error changes at most four compatibility blocks, so a conservative potential increment is b_noise=4(Delta^2+1); witness bit errors cost at most Delta^2+2. With one norm-h Hamiltonian term on EACH of the 5n data/witness sites, the small-a drift/load comparison has the diagnostic scale

h/kappa_rate < w_bar / [5 K b_noise].

This is NOT the parent's finished lifetime theorem or an optimized threshold; it isolates the scale already imposed by the current proof. Additional safety factors only worsen it.

Delta | R_n/n | w_bar | diagnostic h/kappa_rate
16    | 3.22184e-28 | 1.57316e-31 | 5.83198e-41
32    | 1.00830e-29 | 1.23083e-33 | 7.15566e-45
100   | 3.38477e-32 | 4.23097e-37 | 2.64402e-51
1000  | 3.38494e-37 | 4.23118e-44 | 2.64448e-64

IMPORTANT: these small Delta rows are optimistic, UNVERIFIED substitutions. They are not asserted to satisfy the source's large-Delta hypotheses or to be actual quantum Tanner code instances. Even this optimistic arithmetic is unusably pessimistic.

A further diagnostic of the asymptotic proof: define alpha=delta^2*epsilon^2/1024=6.103515625e-9. Choosing the ordinary-vertex fraction a=3/4 in the source's exceptional-vertex comparison, an elementary conservative closure requires a Delta of scale

8192/[3 alpha^3 kappa_rob^2 epsilon^2] = 7.44386e40.

Derivation: average relevant columns over the clustered set is at least 2a alpha Delta=1.5 alpha Delta. With at most Delta columns per vertex, at least alpha/2 of that set must be exceptional. Its size is at least 3|S0|/(16Delta), giving >=3alpha|S0|/(32Delta) exceptional vertices. Compare the upper bound 256|S0|/(alpha^2*kappa_rob^2*epsilon^2*Delta^2). This displayed sufficient comparison is NOT a necessary code degree, NOT an optimized complete Delta certificate, and NOT evidence that actual codes require astronomical degree. It shows why merely saying 'take Delta large enough' carries severe hidden constants in this proof route.

The proof's asymptotic noise-scale loss is approximately Delta^(-13), with additional small powers of robustness/distance. Improvement by a few numerical factors is immaterial. A materially useful route must replace these constants with verified finite-family expansion/local-decoder certificates or a different mechanism, not merely deepen the current asymptotic derivation.

## 2. Conditional moves and honest rate normalization

Per sector, check views number 2n/Delta^2, and mismatch-update vertices number 4n/Delta^2. Across both sectors there are 12n/Delta^2 repair/update locations. Assigning each location a Poisson attempt rate kappa gives that total attempt rate, not an exponential multiple of it.

For each location, choose ONE move deterministically from its current local pattern. If represented as separate jumps for patterns, the projectors are mutually orthogonal, so sum J_p^dagger J_p <= kappa I at that location. We do NOT assign kappa independently to exponentially many simultaneously eligible codewords. A data or witness qubit participates in a constant number of such view locations on the square complex, while each location accesses O(Delta^2) degrees of freedom.

But orthogonal-pattern rate normalization is a mathematical channel budget, not a circuit implementation. Realizing all branches with bounded microscopic gate/control rates may require an enormous selector network. Serially searching candidates reduces the effective kappa by the search time; parallel channels require explicitly counted hardware and energy.

For rho=1/4, the local dual-tensor code has dimension approximately (13/16)Delta^2; enumerating its codewords takes 2^[(13/16)Delta^2] candidates. The mismatch input has Delta^2 bits, so a direct complete lookup table has 2^(Delta^2) entries, each storing O(Delta^2) output bits. A compatibility repair can be indexed by its residual local syndrome, about (3/16)Delta^2 bits, but its coset-leader table is still exponential in Delta^2. No efficient finite-instance implementation of these optimal local selections has been earned. Specialized certified local codes could change this; their existence is not established by this audit.

The physical selector must preserve locality and tolerate its OWN noise. Calling its full conditional channel primitive sidesteps this engineering task, and is permissible only as an explicitly idealized mathematical model.

## 3. Actual interaction order and reset cost

A mismatch predicate reads disagreement across a Delta^2-qubit view: up to 2Delta^2 witness bits. Its distributed correction flips at most 2Delta^2 witness bits. A compatibility predicate involves a local block of up to Delta^2 physical data qubits through its commuting checks plus Delta^2 witness bits. Thus an abstract jump has O(Delta^2)-body support, NOT a native two- or three-body interaction. Projector expansion can contain exponentially many high-weight Pauli terms.

One may synthesize a constant-size channel with ancillas and local gates when Delta is fixed, but this gives no uniform useful time/error bound as Delta becomes enormous. Naive extraction of O(Delta^2) checks each of weight O(Delta^2) already costs O(Delta^4) two-qubit interactions per view before optimization, plus decoding, conditional action, uncomputation/reset, and interference management. The same data participate in overlapping checks; any implementation must schedule or autonomously mediate them without reintroducing an assumed clean controller.

The downhill map is generally many-to-one. A reversible dilation must export distinguishing information to ancillas/environment. Up to O(Delta^2) bits of local information per update may need processing/reset in a straightforward implementation; no zero-cost entropy sink is assumed. Imperfect reset/coupling noise must satisfy the local perturbation model after eliminating these ancillas, which has not been derived.

## 4. Expander graph versus 3D apparatus

The required interaction graph is bounded-degree but expanding. At fixed unit density in a roughly cubic 3D region with O(n) hardware cells, a geometric cut has only O(n^(2/3)) nearest-neighbor links, whereas a balanced expander partition needs Omega(n) interaction edges crossing it. With bounded bandwidth per physical link, maintaining constant service per logical expander edge therefore cannot be free: routing imposes at least an Omega(n^(1/3)) aggregate slowdown across such a cut, or requires additional cross-section/hardware, growing-range links, or nonlocal interconnects.

This is a capacity argument under the stated layout assumptions, not an impossibility theorem for optical links or a universal volume bound. If the effective kappa shrinks with n while local decoherence h remains fixed, the fixed-ratio stability condition is eventually lost. Added routing/repeater qubits bring their own noise and control problem. Treating them as noiseless communication wires would invalidate the apparatus-inclusive claim.

A device with explicitly available long-range high-fidelity links may legitimately use graph locality. Then link distance, loss, heralding delay, bandwidth, connection arbitration, and preparation/reset must be charged in both this architecture and the active comparator. No such realization has been supplied.

## 5. Same-resource ordinary competitor

Give an active Tanner/LDPC memory the exact same code, four witness qubits/data, expander connections, channel access, total interaction rates, reset budget, and noisy-control hardware. It can run the same local inference or stronger clocked/parallel decoding. Nothing here proves better error rates, usable threshold, throughput, energy, or encoded capacity. If perfect high-arity conditioned jumps are granted as native, the demonstrated distinction may be removal of a trusted external timing/decoder service—not superior fidelity per hardware resource.

Conversely, if the proposed jumps must be compiled into realistic few-body noisy hardware, the ordinary comparator receives the SAME compiler/resources; cannot price its clock and processor while declaring our jump selector free. Initial quantum encoding and final protected readout are also shared costs, not supplied by a storage theorem.

## Mission judgment

The abstract hardest step—extensive local restoring drift with an actually noisy finite witness alphabet—is consequential if independently correct. However the current proof has not established a useful-cost path to the north star. The next promotion gate should be a concrete finite local-code/interaction instance with certified constants and a physically timed noisy jump realization, or a different family that avoids the giant local degree/selector. More refinement of exponentially tiny abstract thresholds alone has limited additional consequence.

# What the restricted autonomous-memory result actually adds
2026-10-29. Primary constructions/assumptions inspected, not merely abstracts. No global-priority claim. “Our result” below means the present conditional synthesis with its separately reviewed interfaces, not a published or experimentally established theorem.

## Bottom line
The potentially substantive contribution is a **conjunction**: constant-rate graph-local quantum storage, a time-independent finite-rate noisy quantum controller, an explicit two-site-qudit-Hamiltonian/one-site-reset implementation, and a physical-time threshold for arbitrary local CPTP Poisson kicks with retained bath. The exact forest gauge and actual-record fault/service bounds pay for a compiler layer that none of the four supplied papers automatically supplies.

It is NOT the first autonomous-memory proposal, the first quantum/classical reduction, the first coherent qLDPC threshold, or constant-overhead fault tolerance in general. It does not settle the strongest geometrically local, translation-invariant autonomous-memory problem stated in the October paper. It offers no demonstrated hardware advantage yet.

## Strict comparison with the supplied primary results

### 1. Drechsler–Oreg–Aharonov, 2610.05589v1 (4 October 2026)
Governing inputs: Definition 2.22, Eq.31–33; register extension §7.1; construction Eq.190–195. Their asynchronous reduction assumes stabilizer-algebra Hamiltonians and syndrome-conditioned Pauli jumps with sector-specific rate conditions. Their constructive synchronous-to-continuous conversion uses globally scheduled Reset–Read–Execute stages and noisy classical registers. It is Floquet, not time-independent. Their stated strongest open problem additionally demands geometric locality and translation invariance. [Primary text](https://arxiv.org/html/2610.05589)

**Consequence:** our ideal Pauli-sector interpretation is not a new replacement for their equivalence; once a suitable classical asynchronous process is proved, much of that lift is standard. Our coherent quantum controller with arbitrary CPTP kicks does not satisfy their classical syndrome-rate hypotheses automatically. The new work is the full-instrument compiler and asynchronous stability, not renaming CSS decoding. Our non-TI expander graph does not solve their low-dimensional/TI problem or provide a black-box conversion of every SPCA.

### 2. Han et al., 2609.20537v1 (17 September 2026)
Governing inputs: §II.1–2 and Theorems 1–2/18–19. Noise is a constant-depth bounded-support circuit of small coherent gates, or local CPTP errors; perfect syndrome measurement and recovery follow. They prove code-capacity diamond-error suppression for broad qLDPC families using cluster resummation. Their discussion separates repeated noisy extraction and persistent non-Markovian environments as further problems. [Primary text](https://arxiv.org/html/2609.20537)

**Consequence:** neither coherent same-syndrome cancellation nor a single-block qLDPC threshold is ours to claim. Their theorem cannot be iterated through our controller without proving the intervening recovery, fault propagation and physical-time service contracts. Conversely, our rare arbitrary-kick theorem does not include their weak continuous/coherent-error regime merely because each kick can be non-Pauli. These are different noise parameters. Their resummation is a plausible tool for the next missing extension, not an already-proved autonomous extension.

### 3. Dünnweber–Styliaris–Trivedi, 2601.20818v2 (21 May 2026)
Governing inputs: §III.1–2, especially Eq. for sum gamma(Phi−id), and Discussion. They protect a self-simulating noisy control hierarchy in two spatial dimensions; the continuous realization uses finite-neighborhood CPTP update jumps and local unitary noise jumps. The Discussion explicitly calls the continuous-time proof an outline and leaves its detailed proof for future work. Constant encoding rate is separately identified as open. [Primary text](https://arxiv.org/html/2601.20818v2)

**Consequence:** “noisy autonomous controller” and universal autonomous computation are not new aspirations. Their 2D/TI architecture is stronger geometrically and includes computation, which ours does not. The candidate advance here is constant-rate storage with explicit finite-rate instrument/physical-window bounds and nonunitary retained-bath Poisson kicks. Our two-site coherent compiler is not supplied by their many-site update-jump formula. The earlier infinite marching-soldier exposure counterexample must NOT be advertised as refuting v2's finite synchronization neighborhoods; that would exceed its proved scope.

### 4. Midha–Abanin, 2609.38139v1 (29 September 2026)
Governing inputs: setup following Fig.1 and supplementary machine construction. They explicitly work at code capacity with perfect syndrome measurements, using distributed BP processors and local feedback; active-check moves have independent Poisson clocks. They establish threshold transfer from suitable BP decoders and give further numerical code-family studies. [Primary text](https://arxiv.org/html/2609.38139)

**Consequence:** autonomous local Tanner-graph inference is already established as a useful architecture. Our additional obligation is sustained quantum storage while the syndrome-processing hardware and controllers themselves suffer faults, rather than decoding an initial error with perfect syndrome access. Their setup does not by itself compile to our noisy finite-dimensional quantum controller or prove its long-time memory bound. This is a difference in guarantees, not proof that our constants or practical decoder performance are better.

## Strong conventional comparator, not omitted
Christandl–Fawzi–Goswami prove constant-qubit-overhead FT computation for general diamond-norm circuit noise, using constant-rate linear-distance qLDPC codes. However, their explicit model §II.C makes purely classical gates perfect and specifies a layered gate schedule, including noisy idles. [Primary published paper, §II.C and Theorem 3](https://journals.aps.org/prxquantum/pdf/10.1103/k4cm-pp9p)

Thus constant overhead plus coherent quantum-gate noise is not a new capability. Our result does not dominate this theorem: we have weaker noise and no computation/readout compiler. Conversely its scheduled, perfect-classical-control interface does not automatically prove our unscheduled noisy-controller memory. Composing it with a universal autonomous simulator would still require a size-independent noisy synchronization, storage-time and overhead theorem—the very step that cannot be assumed.

## Is the result just a standard corollary?
Not from these inspected theorems alone. A proposed black-box derivation must exhibit a theorem simultaneously preserving: constant storage rate; bounded hardware dimension/rates; no global schedule; noisy local controllers; bounded physical-time fault clusters; and a valid quantum output interface. None of the inspected statements directly provides that substitution.

The individual ingredients—Stinespring compilation, Feynman gauges, correctable spans, local cluster counting, SSF confinement—are conventional. The candidate technical contribution is their exact combination with reset-first transactional isolation, coherent-mask preservation, late-ancestor multiplicity bounds and genuinely fresh-service instruments. This is a scoped novelty hypothesis for expert review, not proof of priority over all literature.

## Costs still hidden by asymptotic notation
* “Two-site” means two fixed-dimensional hub/resource QUDITS, not arbitrary hardware two-qubit interactions. Local dimension, circuit length, monitor machinery and constant slowdown may be enormous.
* Constant rate is graph-local: expander-style connections, wiring, bandwidth and spatial embedding are not free. No fixed-dimensional geometric/TI implementation is proved.
* Maintained one-site reset and monitor reservoirs export entropy indefinitely. Exact nominal channels remain present; arbitrary continuous miscalibration of those channels is not covered by the Poisson-kick model.
* The physical clock rate is constant in system size, but the proved service/noise constants may be unusably small. No numerical advantage over ordinary scheduling is established.
* Initialization supplies an encoded state and clean A0/workspace0/free-lock controllers. Final decoding includes the forest frame and ideal recovery. Neither fault-tolerant loading nor noisy physical readout is already solved.
* This is memory, not universal computation, a passive equilibrium phase, or a finite-fuel device.

## Next hard scientific obligation selected
**Prove—or refute for this architecture—a uniform long-time memory bound under weak continuously acting local Hamiltonian and Lindblad perturbations of DATA and controllers, rather than exogenous rare channel kicks.**

First make the target precise: retain the nominal reset instruments and add bounded local Hamiltonian/system-bath terms plus local Lindblad terms, with a per-neighborhood norm budget eta. Require a decoded error bound O(t N exp(−c sqrt(N))) at eta below a size-independent threshold, with no Pauli twirl, no reset of the retained bath, and no externally scheduled refresh. Then treat actual reset-operator deformation J→J+delta J; its real record must replace any fictional nominal reset record.

The required missing proof object is an **inclusive connected-spacetime norm bound** that combines coherent fault insertions with long-lived malformed controller episodes and the backward SSF certificate. It must resum unselected insertions before taking norms, avoiding a factor exponential in total spacetime volume. Positive Poisson event probabilities cannot simply be reused. The forest gauge preserves local support but does not provide this norm resummation.

Success would establish a capability absent from both the code-capacity coherent theorem and the periodic/scheduled controller theorems: sustained unscheduled noisy-control protection against continuously accumulating errors. Failure should be an explicit arbitrarily weak allowed perturbation with asymptotic logical failure, not merely a failure of one proof method. Either outcome is more scientifically consequential than optimizing a harmless coloring constant or declaring the present restricted theorem decisive.

### Why the noise upgrade is not a change of terminology
A finite-rate CPTP-kick generator has the form Lambda(Phi−id), with Phi CPTP after aggregating its finite total rate. Pure nontrivial Hamiltonian evolution cannot have this form: its finite-time channel is an extreme unitary channel, whereas the Poisson expansion contains a positive identity-channel component exp(−Lambda t). The components could all equal that unitary only if the evolution were trivial.

Likewise, for a qubit amplitude-damping generator D[sigma_minus] at rate gamma, the putative aggregate map id+(gamma/Λ)D[sigma_minus] sends the excited population to 1−gamma/Λ and multiplies coherence by 1−gamma/(2Λ). Complete positivity would require the square of the latter factor not to exceed the surviving population; it exceeds it by gamma²/(4Λ²). Thus no finite Λ gives the exact generator as CPTP kicks. An arbitrary rare nonunitary channel kick is genuinely allowed by our theorem, but ordinary continuous amplitude damping is not automatically included. This sharp distinction is why the proposed next target changes the memory capability rather than its wording.

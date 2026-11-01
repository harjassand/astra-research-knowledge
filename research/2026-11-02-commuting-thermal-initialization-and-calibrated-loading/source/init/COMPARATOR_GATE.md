# Reachable loading and physical ports: comparator gate
2026-11-01. Read current EXACT_SPIN_ENVIRONMENT_PHASE_THEOREM.md, SHA cf76fc3fa3ee42a28446340f7df85c0d683dbe0877f9a5caf4f81b2368212e38. This is a capability/resource comparison, not a re-audit of its mathematics.

## Decision
The delivered result is an equilibrium-initialized storage theorem, NOT yet a reachable quantum memory. Under its literal resources, neither its endpoints nor an active fault-tolerant computer are supplied. Giving active fault tolerance unlimited resets while charging passive loading would be unfair; giving passive memory an exact interacting Gibbs state and instantaneous logical overwrite while charging active loading would be equally unfair.

The class includes V=0 and H_B0=0. Then the designated bath is not a cooling or reset device. Exact joint unitary evolution preserves the spectrum and cannot generally convert an arbitrary initialization into the target joint Gibbs state. No mixing rate follows from locality or stationarity. Taking a thermodynamic bath-volume limit does not fix this counterexample. More generally, reaching a nearby temperature globally is not enough unless its relevant logical/syndrome domination is controlled.

## Same-resource comparison
| Resource | Current passive theorem | Active comparator, only after matching added access |
|---|---|---|
| Geometry / strengths | Fixed bounded-density 3D finite-range bounded-spin Hamiltonian | Nearest-neighbor constant-duration bounded-strength gates are compatible with 3D, but controllability must be specified |
| Noise | Weak bounded-body coherent local V; correlated equilibrium start | Coherent Hamiltonian fault-path threshold can cover weak finite-body V; stochastic threshold is not substituted |
| Initial state | Exact interacting Gibbs state supplied | Product/reset ancillas supplied; their availability is an extra entropy-export capability |
| Write | Fixed full decoded-subsystem overwrite, abstract CPTP operation | Fault-tolerant encoded transfer/encoding; raw unprotected input still incurs interface error |
| Hold | No controller or reset; exponential-in-n^eta bound | Repeated local correction, finite-rate control and continuing resets; resource consumption grows with hold time |
| Read | Ideal global decoder | Encoded transfer or local measurements plus protected classical processing; raw output has a port error floor |
| Preparation cost | No bound | Conditional threshold construction has scalable circuit costs; not free hardware admission |

No numerical crossover can honestly be computed: the passive preparation map, its time, required controls, reset fidelity/throughput, decoder cost, and microscopic gate-error parameters are missing. In particular, there is no given preparation budget with which to equalize the competitors.

## Strong coherent-noise active route
Preskill, *Sufficient condition on noise correlations for scalable quantum computing*, QIC13,181–194(2013), primary full text https://preskill.caltech.edu/pubs/preskill-2013-sufficient.pdf . Theorem1/Corollary1: set alpha=max_k(t0 max_i sum_{i2...ik}||H^(k)_{i,...}||)^(1/k). For m-qubit gates, effective fault amplitude is at most 2m alpha exp(((e−1)/2)/(1−2alpha)). It bounds NORMS of sums of fault paths, not probabilities of stochastic Pauli errors. A finite maximum body size and bounded incidence give a positive weak-coupling regime. Bath Hamiltonian/state need not be thermal. Preparation, measurements and reusable reasonably good fresh ancillas are explicit assumptions (§2 and Conclusions). Thus the same weak spin-noise class is not outside known active fault tolerance once control and entropy export are furnished. This theorem does not certify that the existing static H0 apparatus realizes those gates: its O(1) stabilizer drift must be synthesized around, cancelled or otherwise included in intended evolution.

Gottesman, *Fault-Tolerant Quantum Computation with Local Gates*, quant-ph/9903099v1 (30 March1999), https://arxiv.org/pdf/quant-ph/9903099 , supplies explicit geometrically local concatenated layouts, including nearest-neighbor constructions in 2D/3D; transport/ancilla placement affect the threshold, while asymptotic space/time overhead remains polylogarithmic in target inverse logical error. This is the routing component, not an independently sufficient theorem for arbitrary coherent noise. A joint implementation must evaluate coherent fault-path bounds on its routed gadgets and price clock/classical handling. Do not use its stochastic threshold number for V.

Conditional resource comparison: with an admitted local threshold architecture, holding for T with error delta uses polylog(T/delta) encoded hardware overhead and continuing operations/reset supply roughly proportional to T times that overhead (architecture-dependent constants). At T=exp(c n^eta), polylog(T/delta) is polynomial in n, but total active work remains exponential in n^eta. Passive storage could save that continuing control/reset burden; it has not yet demonstrated cheaper or attainable loading. This is a possible advantage in resource TYPE, not a proved finite-size hardware advantage.

## Why known thermal initialization does not close it
Bergamaschi–Gheissari–Liu, arXiv2507.10976v1 (15July2025), https://arxiv.org/html/2507.10976v1 . Theorem1.7/7.8 mixes syndrome states rapidly starting from an already prepared ground state, using engineered quasi-local conditional block updates and connectedness/local-correction hypotheses (parity checks and metachecks LDPC). Theorem1.8 gives efficient two-qubit implementation of block updates specifically for 4D toric code; generic block channels can have exponential gate depth in block size. Corollary7.9 starts from the maximally mixed ground space. This neither prepares a codeword from local raw input nor supplies generic noncommuting interacting-spin equilibrium. The 3D base paper itself identifies its non-LDPC metachecks as preventing direct application: https://arxiv.org/html/2605.10943v1 , initialization outlook/footnote4. A metastable logical sector can mix rapidly despite globally slow mixing; therefore 'exponential lifetime implies exponential preparation' is NOT a valid blanket argument.

Ma–Khemani–Sang2509.15204v3's thermal channel encoders likewise require target-state-dependent recovery maps and a stable-clustering path. They are not disorder-independent physical gates or a preparation guarantee for this family. See prior gate for exact source conditions.

## Local encoding constraint, correctly scoped
König–Pastawski, arXiv1310.1037v1 (3October2013), https://arxiv.org/pdf/1310.1037 , Theorem1 proves time Omega(d^(1/(D−1))) for Lieb–Robinson-local encoding into a geometrically local commuting-projector code space, including dissipative dynamics. In 3D this is Omega(sqrt(d)), subject to the theorem's code/geometric setup. Bounded-density irregular layouts need their embedding into that setup made explicit. It directly challenges any ground-codeword preparation shortcut. It does NOT automatically lower-bound writing into the candidate's finite-temperature correlated gauge/bath state: that requires a mixed-state cleaning/indistinguishability argument. Nor does it prohibit consuming pre-established long-range resources. Classical communication cannot be silently instantaneous when it carries logical corrections.

## Concrete missing operation and fair decisive test
Specify an allowed, finite-rate local loader L_n and reader R_n, their noise/entropy-export channels, control norm and classical signal speed. Start with the SAME locally provided input/reference and SAME explicitly preparable ancillary state for both competitors. Require:
1. finite preparation time and peak qubits, resets, energy/work, controls and bath-contact budget;
2. reference-safe write/read error including the raw port, with no hidden noiseless logical swap;
3. the loaded joint state satisfies a sufficient storage admission condition, e.g. proximity to the theorem's encoded equilibrium state, or a proved bounded domination/rare-bad-syndrome alternative;
4. robustness during loading and extraction under the actual H0+HB0+V, not merely the hold Hamiltonian;
5. compare total end-to-end error and continuing control budget against a routed coherent-noise FT memory at identical capabilities.
A joint trace-distance preparation error epsilon_p adds at most epsilon_p after subsequent physical channels by contractivity; it need not be multiplied by T. Therefore a storage theorem with exponentially small intrinsic error can still be useful at fixed preparation tolerance. Conversely, an arbitrary unknown single-qubit input corrupted before redundancy is established cannot have that error magically removed; compare encoded input ports or honestly retain a fixed injection floor. The same applies to decoding into one exposed output qubit.

The strongest consequential next result is a polynomial-cost, fault-tolerant local write/read and equilibrium-admission protocol, with temporary controls/resets switched off throughout exponentially long storage. A generic Gibbs sampler, ideal decoder circuit, or a theorem that presumes an encoded initial state does not supply it.

## Access and uncertainty
All inherited access stops preserved. No stopped work/mirror retrieved. Primary sources above opened successfully. No exact same-resource numerical comparison is possible because the delivered physical loading/reset interface is unspecified, not because of an access failure. No assertion of historical novelty or practical superiority.

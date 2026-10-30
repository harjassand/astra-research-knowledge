# Strong ordinary alternatives and the remaining interface
30 October 2026. Targeted primary-source comparison; not a novelty certificate. The local Astra construction is still under completion/review. Claims below concern the exact sources read, not an exhaustive literature search.

## 1. Reliable classical memory already includes faulty correction logic
Chilappagari–Vasic, *Reliable Memories Built from Unreliable Components Based on Expander Graphs*, arXiv:0705.0044, §§II–III and V.B, Theorems 1–2:
https://arxiv.org/html/0705.0044

The supplied architecture stores an LDPC codeword and periodically applies parallel correction using unreliable XOR and majority gates. Theorem 1 tolerates a sufficiently small fixed fraction of failures in storage and correcting components. Theorem 2 gives failure probability at most L exp(-Omega(n)) over L correction periods under independent component failures, with bounded redundancy and linear information capacity. The proof starts by writing a codeword at t=0. It does not construct capture from one presently unencoded physical random latch, establish joint quantum-bath read dynamics, or realize asynchronous continuous Lindblad majority. It is nevertheless a stronger storage-rate baseline than one enlarged repetition-like block per record. Exponential memory lifetime, expander correction, and unreliable control logic must not be called new capabilities here.

## 2. Intermediate perfect classical processors are not fundamentally required
Aharonov–Ben-Or, *Fault-Tolerant Quantum Computation With Constant Error Rate*, quant-ph/9906129, §§4.2, 7.2 and 8.4, Theorem 11:
https://arxiv.org/pdf/quant-ph/9906129

This supplies universal fault-tolerant circuits with polylogarithmic overhead and general nonprobabilistic noise under its circuit model. Intermediate measurements and classical operations are unnecessary. Its encoding procedure starts from repeated basis-state input; §7.2 explicitly duplicates each input bit, and final decoding uses recursive majority. Therefore an assertion that physical control can never avoid noiseless classical processing is false. Conversely this theorem does not automatically supply the finite input-transduction channel from Astra's exposed raw latch or the same autonomous/native fixed-rate hardware. Ordinary reversible/classical fault-tolerant circuitry is an informed alternate architecture, not an impossibility target.

## 3. The early non-Markovian theorem has a narrower bath contract
Terhal–Burkard, *Fault-Tolerant Quantum Computation For Local Non-Markovian Noise*, quant-ph/0402104v2, §1.1 and Theorem 1:
https://arxiv.org/pdf/quant-ph/0402104

The theorem uses scheduled parallel gates, fresh off-line exact zero ancillas, and the stated bath structure: noninteracting qubits have noninteracting baths. Noise strength is a bounded system–bath interaction spectral-width scale times gate duration. It obtains accurate output distributions with polylogarithmic overhead. Its fresh-input and bath assumptions are not the same as arbitrary dirty local targets with persistent shared quantum memory. Do not cite this older theorem alone as either covering or excluding Astra's broader shared-bath setting; the next source addresses that distinction.

## 4. Arbitrary shared baths and incident-strength noise have a strong established comparator
Aharonov–Kitaev–Preskill, *Fault-tolerant quantum computation with long-range correlated noise*, quant-ph/0510231, equations (1)–(5), (24)–(25):
https://arxiv.org/pdf/quant-ph/0510231

The joint Hamiltonian contains an arbitrary bath Hamiltonian and always-on pair terms acting on two system qubits and the bath. A small per-qubit sum of pair interaction norms times gate duration suffices for scheduled fault-tolerant computation. The proof converts this to the established local-noise amplitude bound, with square-root dependence for pair terms; it also explains the fixed higher-body extension, including cube-root dependence for triples. Bath memory need not decay. Thus common quantum memory and spatially correlated coherent perturbations do not by themselves distinguish Astra's capability. This is not verbatim a theorem for arbitrary local HP Liouvillian perturbations, atomic dissipative majority, dirty-controller reuse, or the present full-Hilbert-space read process. A dilation/compiled-circuit interface must be earned before importing it wholesale.

## 5. Recent adversarial fault tolerance is stronger in one direction, not the same resource
Breuckmann–Golowich–Vazirani, *Fault-Tolerant Quantum Computation with Adversarial Errors*, arXiv:2608.16857v2, Theorem 1.1, §2.2.4, Remark 3.15:
https://arxiv.org/pdf/2608.16857

The construction supports universal computation with arbitrary quantum inputs/outputs and almost-linear adversarial support per layer. The displayed bound uses at most logicalN^(5+epsilon) physical qudits, subpolynomial time overhead, and a tolerated support N/2^{O(sqrt(log logicalN))}. The circuit gate set explicitly includes free noiseless classical computation, primarily for decoding; classical function gates measure, compute noiselessly, and reinitialize. It therefore does not presently close Astra's physical classical-computation/read interface. Also its guaranteed corrupted fraction shrinks with size, whereas fixed small weak noise can act at every site. A direct parameter substitution from the latter model to its support promise is invalid. It is a major stronger universal-operation comparator, not proof of the narrower native apparatus or a constant-density adversarial threshold.

## 6. What the current construction would actually add
These are deductions from the resource comparison, not claims of historical novelty.

The viable target is a composable physical interface: a supplied genuine measurement outcome is copied from its exposed latch through noisy bounded-strength stages into enlarged blocks; each retained physical port has a joint small-error law under the same quantum bath and can drive a continuously protected native receiver without an immutable classical register. The particular contribution, if completed, is the actual receiving contract and hardware/compiler construction, not reliable computation's existence or tolerance of correlated quantum noise.

There are two honest alternatives. (A) Finish the scheduled bounded-body atomic construction with its genuine classical input boundary, fixed seed calibration, growth cost, positive final port instrument, and quantum receiving gap. (B) Replace it by scheduled fault-tolerant circuit gadgets, paying for fresh-state preparation, finite detector and input/output interfaces, and all classical control. The known theorems give strong reasons to expect B, but no source above proves that all of B's resource promises are delivered by the current apparatus. A conventional architecture may be operationally preferable even if it abandons autonomous-controller ambitions.

## 7. Elementary capture boundary: later storage cannot undo an erased source distinction
For clarity, consider a special admissible input: a uniform unknown classical bit m, identical unrelated bath state for both values, and a raw latch exposed for duration tau BEFORE any operation distributes information about m. Let its only disturbance in that interval be the local bit-flip generator eta(X rho X-rho). The effective raw-bit channel has crossover p=(1-exp(-2 eta tau))/2. All subsequent processing, including an arbitrarily large perfectly reliable memory, is a channel acting on that noisy latch and m-independent resources. Trace-distance contraction bounds optimal final reconstruction success by 1-p.

This is a direct elementary proof under its explicit pre-copy exposure assumption. It is not a lower bound for every concurrent copying design or for an input furnished with redundant correlated side information. It does show why increasing the final block alone cannot be advertised as suppressing all acquisition error when a vulnerable unencoded ingress remains. Astra's fixed-seed parameter is allowed to remain a small local error floor: the downstream source/code must tolerate that floor. The genuine historical outcome m and a possibly wrong physical detector estimate of an earlier quantum syndrome are distinct references.

## Assessment
The classical atomic resource remains worthwhile only insofar as the composition genuinely closes a previously unsupplied physical interface, or earns a better resource/robustness regime. The current evidence does not establish a practical advantage over scheduled fault-tolerant circuits, historical novelty, or a universal autonomous quantum computer.

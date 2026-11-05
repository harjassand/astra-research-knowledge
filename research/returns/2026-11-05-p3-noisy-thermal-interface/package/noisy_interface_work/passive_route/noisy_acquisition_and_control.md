# Noisy acquisition and classical control inside a compatible model

The inverse-noise theorem is mathematical. This note gives a concrete way to avoid silently perfect arithmetic, syndrome measurements and coefficient estimates in one specified control model. It also identifies where extra physical access is genuinely being added.

## 1. One noisy code for the controller and quantum interfaces

The chosen bridge uses Aharonov and Ben-Or's measurement-free native scheme throughout. All arithmetic, graph enumeration, sampling, decoding, frame storage and schedule evaluation are compiled into its protected reversible circuits. The native bounded-arity gates include NOT, CNOT, S, controlled-Z, H, Toffoli, SWAP, preparation and discard; idles and all mutable controller registers are noisy. There is no ideal classical side computer and no transfer of an ideal-classical-controller theorem to a different code.

The explicit conservative base and adjacent-level quantum interfaces are given in ../endpoint_route/same_code_controller_bridge.md. The punctured RM(5,11) CSS code corrects 31 errors, exceeding the conservative spread 16 of a native gate procedure preceded by correction. For a fixed rectangle constant a, the same-code recursion is

\[
p_{r+1}\le a p_r^2,\qquad\sum_{r\ge0}p_r\le2p
\]

at sufficiently small fixed p. AB's validity statement handles arbitrary incoming states; its logical correctness statement handles the permitted correctable incoming states. The syndrome subsystem is retained in the analysis. Arithmetic outputs and sampled parameters remain encoded when passed to subsequent protected operations. A classical-only repetition implementation could be substituted after separately validating its noisy gates and interfaces, but it is not the bridge used here.

### The final classical controls are constructed, not assumed independent

For each output prepare a fresh encoded Bell pair A,B, perform the protected logical Bell transform on the incoming data and A, fan out each resulting logical Z bit into M fresh code-zero blocks, and discard the consumed data/A registers. No fanout or old coherent-controller gate touches B. Disjoint actual descents of the copies have input-independent bad-fault tags with probability q_c=O(p), giving a local-stochastic wrong-leaf law uniformly over arbitrary correlations of the incoming gauges and records. Independence of the wrong leaves is not assumed.

Pass each copy pool through the fixed noisy majority tree proved in static_tree_regenerator.md. Its output differs by at most q_c alpha^L from a fresh binary-symmetric channel on the correct Bell bit, for fixed alpha<1. The native voter is CNOT(a,b), CNOT(a,c), Toffoli(b,c,a), retaining a. Every fixed Pauli bit-fault pattern preserves simultaneous complementation of its inputs. Two independent reference trees supply the two Bell controls. The pool size M=3^L is polynomial in requested inverse accuracy and must be charged in addition to the usual protected-circuit overhead.

B stays on its independent wait/descent path. Arrange the classical roots and B's raw output at the same prescribed clock, padding only while registers are protected. Apply the correction using always-scheduled physical CNOT and controlled-Z gates from the two raw classical bits to B. Their faults and the local SWAP belong to the endpoint channel. All fine controller/pool transcripts are reset. The uniform Bell labels themselves Pauli-twirl the independent B descent, while the tree prevents old gauges from entering through the final controls. Thus the terminal comparison channel is a product of known local Pauli channels up to the paid protected-prefix and tree-coupling errors. A Clifford-only controller is unnecessary.

For random sampling, logical |+> preparation followed by logical basis-label copying and discard produces a classical random bit inside the protected code. Finite rational-probability sampling uses protected Boolean computation. The outcomes, counters and parameter estimates remain encoded; they are not exported through one supposedly perfect raw classical bit and reimported. No analog probability need be programmed to inverse-polynomial gate precision.

## 2. A calibratable component-noise model

A particularly explicit acquisition model is stationary gate-independent Pauli noise: each outgoing physical wire of every elementary operation is followed by the same unknown one-qubit Pauli channel Lambda, independently in space and time. Reset, readout and record-capture templates are known native circuits whose only faults are this same Lambda, including noise on classical output wires. They do not introduce additional independently unknown SPAM channels. This is a concrete subclass of the more general independent bounded-arity Pauli model. General gate-specific fault laws need their own identification protocol or supplied parameters; idle ratios alone do not identify arbitrary extra SPAM channels. No finite calibration experiment certifies iid stationarity against unrestricted drift or correlated noise.

For each Pauli axis, prepare both signs of the noisy eigenstate, insert t idle locations, and make the same noisy Pauli measurement and protected record capture. Clifford basis changes are part of fixed preparation/measurement templates. Define m_t as half the difference of the captured expectations for the two signs. This contrast cancels any fixed additive asymmetry of the raw-to-protected classical capture. The expectation has form

\[
m_t=A\lambda^t,
\]

where lambda is the Pauli eigenvalue of the idle channel and A includes the stable preparation, readout and capture response. More explicitly, a fixed classical capture maps an input polarization y to c+d y; opposite preparation signs cancel c. Clifford/Pauli preparation gives a polarization along the selected axis, so the remaining contrast is multiplied by lambda at each idle. For noise below a fixed small threshold, |A| is bounded away from zero. The ratio m_1/m_0 therefore estimates lambda without perfect preparation, measurement or record import. Three axes identify Lambda. Hoeffding concentration plus protected arithmetic gives additive eta accuracy with O(eta^{-2} log(1/delta)) trials per axis. The quantum preparation/idle/readout experiment has constant duration per trial; protected capture, accumulation and arithmetic carry their separate compiled cost. All resets and measurements are counted.

### Generic acquisition of the effective endpoint

Once the complete component law and templates are fixed, a Clifford-only path admits stabilizer Monte Carlo. The chosen AB construction need not be Clifford. For it, run protected quantum simulation of the explicitly known finite endpoint circuit, intentionally inserting sampled faults according to the calibrated model. The simulator's own physical faults are suppressed by the same noisy native scheme.

To obtain the unconditional comparison syndrome, simulate the full encoded Bell-resource circuit and apply its coherent virtual decoder. Use a fixed extension of that decoder to the full physical Hilbert space. Discard the logical pair, reinsert an ideal logical Bell pair **inside the target being simulated**, retain the entire syndrome marginal, and re-encode. Simulate the complete independent encoded-wait/descent schedule, the classical reference-tree channel and the terminal gates. There is no selection of globally good fault histories, and no rejection sampling. Any weight outside the protected syndrome class is already charged to the resource-preparation error; it is not silently postselected away.

The coherent decoder is computable recursively: its fixed base-code lookup tables and native circuits are charged constants, and its recursion is polynomial in the block and template size. The resource simulation, decoder, discards, Bell replacement and descent therefore have polynomial circuit size in the known template size. Encoded Bell-basis measurement samples the resulting Pauli law. Sample labels, counters and parameter estimates remain encoded when used by the preparation algorithm. The ideal decoder and Bell replacement are computational targets of the simulator, not ideal devices acting on the unknown input.

An effective channel estimate to TV eta_i with failure delta_i uses O(eta_i^{-2} log(1/delta_i)) samples times this protected simulation cost. If a template has G_i physical stochastic locations, changing each location's fault law by TV eta changes its channel by at most G_i eta. Thus sufficiently precise component acquisition and simulation give a certified endpoint law. The required precision is a statistical/computational cost; the physical component error itself stays constant.

For n endpoint qubits, estimates with total one-qubit channel mismatch sum_i ||K_i-Khat_i||_diamond <= epsilon add at most epsilon to the final prepared-state error by a channel telescoping bound. It is unnecessary to bound K^{-1}'s norm in the full n-qubit diamond norm. The prepared distribution is a valid positive preimage for Khat, and then actual K versus Khat acts on an ordinary state.

## 3. Concrete acquisition of the dimensionless check coefficients

The following is an **additional paid calibration mode**, not a consequence of arbitrary quantum gate access. The hardware must permit selective switching of its commuting stabilizer couplers: isolate one actual check term J_a(1-S_a)/2 while all other terms touching that finite support are off. It must also permit that finite subsystem to couple to the same specified detailed-balance bath. Coupler switching must be a stable architectural operation with its errors included in the model; unrestricted coherent residual couplings are not covered.

The check support has bounded size w. Its isolated Gibbs excitation probability is

\[
r_a=\frac{1}{1+e^{\lambda_a}},\qquad\lambda_a=\beta J_a.
\]

In the specified local Pauli bath, take a jump anticommuting with S_a with known positive rate lower bounds in both energy directions. The check sector then follows a two-state Markov chain with spectral gap at least g_min>0. From any initial state, waiting

\[
t_{\rm cal}\ge g_{\min}^{-1}\log(1/\eta_r)
\]

makes its excitation law eta_r-close to equilibrium. Hidden modes within the sector do not matter to this measurement. This is only a constant-size calibration bath, so no full BDL equilibration is invoked.

Measure S_a with a finite Clifford ancilla circuit. Under the stationary iid Pauli circuit model, its raw outcome is the initial check bit XOR an independent classical fault bit. Include the entire noisy record-capture template when computing its effective classical response from the calibrated Lambda. That response has the affine form \(\widetilde m_a=c_a+a_a(1-2r_a)\), where a_a is bounded away from zero below a fixed threshold. If capture is symmetric, c_a=0. In general both coefficients are computable by the protected known-circuit simulation described above. Subtract c_a from the captured polarization and denote the result by m_a. Then

\[
m_a=a_a(1-2r_a).
\]

Repeated preparations/waits/measurements and actual noisy captures estimate r_a after this offset subtraction and multiplicative debiasing. Allocate acquisition/simulation accuracy to c_a and a_a as well. The inverse transformation lambda=log((1-r)/r) has derivative magnitude 1/[r(1-r)]. On the fixed interval lambda_a<=lambda_max, estimating lambda_a to eta_lambda therefore needs r_a accuracy O(e^{-lambda_max} eta_lambda). A sufficient trial count is

\[
O\!\left(e^{2\lambda_{\max}}\eta_\lambda^{-2}\log(m/\delta)\right)
\]

per check, plus the warm-up duration and finite Clifford gate cost. Initial reset and raw readout are noisy; their effects are explicitly included or eliminated by mixing/debiasing. A union bound controls all m coefficients. Taking eta_lambda=O(epsilon/m) gives polynomial total acquisition cost, with the severe fixed factor e^{2lambda_max} retained.

This mode calibrates beta J directly, so no separate ideal thermometer is needed. It probes the actual coupler, so it does not assume a faithful replica. It does require individually isolatable couplers, a lower-bounded calibration relaxation rate and stable switching. If the chosen physical family offers only global on/off switching, this operation is unavailable and a different Hamiltonian-learning protocol must be supplied. General precise Hamiltonian coefficients cannot be inferred from bounded Pauli-control errors alone.

## 4. Resource and scope consequences

The same calibration access, protected controller, ancilla resets, routing and switchability must be given to the strongest active error-correction comparator. None of these steps proves a total-energy or total-spacetime advantage. They establish that the mathematical source precision can, in one explicit model, be acquired with noisy primitive operations at a polynomial cost; the cost and the extra switchable-coupler fabrication must remain in the operation's ledger.

The holding Hamiltonian/bath contract remains supplied. No commissioning experiment establishes a Markovian Pauli-Davies model for exponentially long future time against unrestricted model misspecification. The resulting theorem is a fixed-component-noise interface theorem under that stated bath model, not general robustness to noncommuting fabrication errors or slow drift.

Primary threshold source: Aharonov and Ben-Or, *Fault-Tolerant Quantum Computation With Constant Error Rate*, https://arxiv.org/pdf/quant-ph/9906129. The calibration formulas above are elementary derivations for the specified model, rather than claims imported from a general tomography theorem.

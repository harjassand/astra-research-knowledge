# Complete learned-frame recovery for one full-rank unknown-noise family

2026-10-29. Root synthesis/derivation; independent review pending. This composes received operations to close an acquisition-to-recovery interface. It is not a new general fault-tolerance theorem, a demonstrated quantum advantage, or a hardware architecture at useful cost.

## 1. Actual source and paid interfaces
Use the accepted SINGLE four-spin memoryless source N_W^eta=(1-eta)T_W+eta D16. T_W is the24-element collective-Clifford twirl conjugated by an unknown W=V0⊗V1⊗V2⊗V3. The fixed parameter eta is in[0,1], initially unknown. A supplied or separately acquired valid bound eta<=eta_U is needed for the conditional cost/error theorem; the scalar flag calibration can provide a high-confidence bound under this promised family, but does not validate the family.

The controller supplies trusted known preparations/unitaries/measurements, protected ancillary records/programs and storage, and known classical arithmetic. Acquisition sends maximally mixed four-spin carriers through this actual source. Subsequent service uses the SAME source with encoded input. This is a circuit/channel construction with explicit known-control synthesis modules, not evidence that those trusted operations are protected in a real device. Control infidelity and source drift outside the promise remain unresolved.

## 2. Acquisition and finite preparation before the payload
For each star edge j=1,2,3, the received commutator acquisition yields independent labels sigma_j=[P_(c_j perpendicular)+eta P_cj]/(8+eta), c_j=vec(R_j R0^T)/sqrt3. The received exact history envelope and finite purification schedule prepare rotation programs within a specified isotropic error v_U on every successful complete transcript, including timeouts/restarts. The heterogeneous transducer produces one valid noisy Choi program with error at most w(v_U), using independent pairs/batches. Forward and inverse quaternion-to-Choi conversions are known fixed basis operations.

Prepare all program resources needed for the intended finite service batch BEFORE admitting the unknown payload. Every stochastic acquisition/transduction/purification failure is then a preflight abort/retry, never a failed operation on the payload. Use fixed public caps and union-bound the specified preparation abort probabilities. Complete batch transcripts may give different noise parameters; product factorization holds conditioned on the full separate acquisition histories because the source is memoryless. The bound can then be averaged over those histories. Do not infer product structure from a coarsened shared success flag alone.

Deterministic product-resource PBT uses N independent Choi ports for each desired local frame gate. For ideal exact PGM control the received qubit error bound is3/(N+3). With each port Choi's physical channel error at mostnu, the implemented local gate has half-diamond error at most
 e_g=nu+3/(N+3).
The noise term is paid ONCE per delivered gate, not N times. A separately approximated PBT/compiler contributes its actual joint channel error additively. One program output per independent conversion batch is the conservative interface; within-quartet independence is not supplied.

## 3. Unknown absolute gauge cancels
Let E0 be the known exact qubit encoder into the two-dimensional four-spin singlet sector P0, and D0 a known CPTP decoder with D0 E0=id including a specified leakage reset. Put W_rel=I⊗(V1 V0†)⊗(V2 V0†)⊗(V3 V0†). Since W=W_rel V0^tensor4 and every collective SU2 acts identically on P0,
 W E0=W_rel E0.
Thus the three acquired relative frames suffice; no absolute V0 gate is assumed. Encode with E0 then three relative-frame gates, call the source once, undo the three frame gates, and decode with D0. This uses six learned local gates per four-spin service, plus the previously compiled known fixed encoder/decoder.

For perfect frame operations, the logical channel is (1-eta)id+eta R_tau, where R_tau is replacement by the fixed decoder output D0(I16/16). Apply fresh known logical Pauli before encoding and undo it after decoding, and retire the key. Averaging the four keys turns R_tau into D2. Thus the ideal closed logical channel is exactly (1-eta)id+eta D2, whose total nonidentity Pauli probability is3eta/4.

Replacing the six ideal frame gates by the above approximate ones changes the complete port by at most6 e_g in half-diamond norm by composition, for arbitrary input references. Logical Pauli twirling is contractive and yields a genuine Pauli channel. Its nonidentity probability therefore satisfies
 p<=3eta_U/4+6e_g.
This bound includes frame acquisition/processor imperfections at their proved scope. It does not erase the physical depolarizing component.

## 4. An explicit ordinary error-correcting completion
Assume p<1/10. Across distinct services, conditional on their complete preparation transcripts, the noise maps are independent possibly nonidentical Pauli channels with each nonidentity probability<=p. This uses the memoryless source and independent consumed resources, not merely a marginal error estimate.

Use the standard five-qubit stabilizer code with generators XZZXI, IXZZX, XIXZZ, ZXIXZ. The executable exact binary-symplectic check verifies that all15 single-qubit nonidentity Paulis have distinct nonzero syndromes; the commuting independent generators define a two-dimensional code. A known Clifford encoder/syndrome decoder corrects every single-qubit error. Logical XXXXX and ZZZZZ commute with the stabilizer and anticommute with each other. This is established conventional QEC, not new machinery.

For five independent ports, failure requires at least two nonidentity errors, so a union bound over ten pairs gives p_next<=10p², including possible benign higher-weight errors conservatively. Disjoint-block concatenation gives after L levels
 p_L <= (10p)^(2^L)/10,
using K=5^L four-spin service calls. The decoded logical channel is Pauli; its half-diamond error from identity equals its nonidentity probability. Thus arbitrarily small logical error follows at finite L under the stated threshold and trusted-control contract. This is channel-use reliability, not a storage-lifetime or fault-tolerant-control claim.

All preparation must cover6KN noisy Choi ports (one per independent acquisition/transduction batch) if the full batch is prepared before payload arrival. This is at least12KN protected program qubits plus work space, and the recorded finite per-program source-call/control costs multiply accordingly. The K service calls are additional, not the total acquisition cost. The ideal known outer encoders/decoders also cost gates and storage; those are standard finite stabilizer circuits, not assumed zero hardware error.

## 5. Example and limitations
Choosing eta_U=.01 and e_g<=1/2400 gives p<=.01. L=1,2,3,4 then give error bounds10^-3,10^-5,10^-9,10^-17 using5,25,125,625 service calls. The quantum program cost is much larger: even splitting e_g equally between port noise and PBT requires N>=14397 ports per learned local gate. These are constructive finite bounds, NOT useful current overhead or simulation of the complete device.

An equally informed classical covariance/eigenvector estimate can learn these three low-dimensional relative frames without environment tomography and reuse its descriptions. It is a mandatory competitor; averaged-channel covariant estimation may match the relevant1/epsilon scaling. No practical or asymptotic superiority is established by this composition. The exact eta=0 quantum-record/classical-record separation is a different, fragile statement.

Model-family misidentification, arbitrary memoryful/adversarial noise, a physical implementation without a larger protected-memory bypass, realistic control noise, useful latency/energy and broad quantum-computing advantage remain open. The construction closes a finite quantum-program route for this explicit unknown-frame full-rank family, not the entire ambitious mission.

## Sources and dependencies
Primary conventional code source: Laflamme, Miquel, Paz and Zurek, Perfect Quantum Error Correction Code, arXiv:quant-ph/9602019, PRL77,198 (1996). The code is independently specified and syndrome-checked here; it is not asserted to be newly discovered.

Load-bearing local dossiers: four_spin_common_label_source_20261029 with its independent receiving receipt; history_uniform_program_purification_20261029 (receiving pending at draft time); noisy_transducer_audit_20261029 and heterogeneous_transducer_audit_20261029; product_choi_pbt_audit_20261029; earlier four_spin_bell_encoder_20261029 and its canonical leakage reset correction. Finite transducer dilation and exact preparation schedules remain distinct reviewed-or-pending implementation artifacts and must retain their actual review status.

# Capability-first physical operation report

Worker: gd_physical_operation. Date: 16 October 2026.
Input pin: 2688d7a383502df4fc1e64001d04bb76e6ec05e5.
Physical joint regime: NOT_ACQUIRED.
Practical advantage: NOT_ESTABLISHED.
New physical operation: NOT_ACQUIRED.

## Outcome

The strongest realistic candidate is coherent local syndrome recovery through an ancilla with an explicit entropy-export/reset path, followed by separately installed physical dephasing floors. Its basic recovery/reset mechanism is already experimentally established. The supplied structured compiler can make a qualified generator admit an exact positive proposal schedule, but this does not itself create better noise suppression or acquire the generator on hardware.

No acquired experiment demonstrates the simultaneous ingredients required here: the eleven-qubit pair correction, the declared sparse signed coefficient catalog and bounds, implemented matched floors, bounded spatial incidence, finite control/reset errors, and a useful common rate margin. The source theorem's threshold remains qualitative. Therefore there is no justified promotion to an obtainable memory capability.

## Exact input/output contract

The intended capability is unconditional preservation of an arbitrary unknown quantum state, including a reference-entangled input, at a specified channel-error tolerance and storage time. The comparator receives the same calibration/noise information, apparatus and control budget. Preparation, correction, reset, routing, idle time, final recovery and output readout count.

The mathematical input is a separately justified local GKSL coefficient catalog with bounds M_ab,u_p, bounded support diameter and incidence, plus a physically present Pauli floor. The compiler ceiling is 2 sum_ab M_ab + 2 sum_p u_p. Its input promise cannot be inferred from a small diamond norm, a sparse best fit, a T1/T2 pair, or a successful memory experiment using another code.

The supplied generators are kept distinct: active pair jumps, two-Kraus completed pairs, the separately measured finer completion, and the older whole-star depolarized regularization. The completed-pair coherent argument does not apply automatically to the active generator.

## Strongest candidate and decisive findings

1. The exact two-Kraus pair channel has a standard coherent dilation. Extract both checks into work ancillas, compute their AND in a flag, uncompute the work registers, conditionally write one face and reset the flag. A displayed construction needs three ancillas and 31 conventional two-qubit gates before routing/native-gate conversion. This is a valid ideal circuit, not an acquired device.

2. Ordinary separate measurements of the two checks implement a different channel. A three-data-qubit inactive-coherence test separates it from the stated channel by output trace norm 1. A direct conditional quantum-span lemma shows that this finer completion can use the same good-schedule certificate if all imported global premises hold, but the generator modification must be named.

3. Operation locality is not just the single written face. The eleven-qubit pair supports give 22 correction-stream incidences per data qubit. A direct independent-start gate realization therefore has finite-duration contention. For a hypothetical one-microsecond whole gadget, even a one-constituent 1-percent collision tolerance restricts the rate per pair stream to about 479/s. This is an implementation-specific falsifier of treating fast programmed circuits as the exact source clocks. A continuous-reservoir design might avoid this route, but no controlled eleven-qubit elimination model was acquired.

4. Adding matched dephasing is a real channel change. For a drift hP, the optimal one-mode worst-case floor gamma=u supplies proposal ceiling 2u, while also damping P coherences at rate 2u. For constant unknown h an ideal echo cancels the drift without adding that dephasing. Finite pulse costs matter, yet the compiler alone cannot be sold as superior local noise control.

5. Small coherent gate error is not automatically a rare faulty CPTP event. A nontrivial unitary channel has no convex decomposition containing any positive Id weight. High fidelity therefore cannot furnish the assumed independent rare fault process without an actual intervention or another error theorem.

6. Observed dephasing does not justify a scalar Markov generator. A finite-bandwidth random telegraph drive gives colored Hamiltonian noise, and an arbitrary continuous system-bath Hamiltonian can lie outside a system-only floor's dissipative range. A quantified model remainder needs its own transfer argument; the elementary bound T N delta does not inherit the source's exponential storage time.

The derivations and finite checks are in LOCAL_OPERATION_LEMMAS.md and calculations/CHECK_RESULTS.json.

## Experimental evidence that changes the decision

Recent primary channel-simulation and autonomous-QEC work already performs coherent error recovery and reset. Sun et al. explicitly use a finite repeated-channel approximation and optimize the recovery period against control error; Ni et al. explicitly count recovery and reservoir reset. These are the strongest local precedents and operational incumbents for the proposed route, rather than evidence of a new primitive here. [Sun et al.](https://arxiv.org/abs/2509.22191v1), [Ni et al.](https://arxiv.org/abs/2509.26042v1).

A published repeated surface-code memory is a stronger scaling comparator under its own apparatus and noise model. Its DD, leakage removal, reset and decoding are part of the operation, and its residual correlations caution against treating even a detailed fitted model as exact. It does not supply the proposed four-dimensional corrector. [Google Quantum AI and collaborators](https://doi.org/10.1038/s41586-024-08449-y).

Sparse Pauli learning and two-qubit noise spectroscopy support acquisition tools, but their explicit twirling/weak-coupling/model assumptions do not certify the signed coefficient interface on an eleven-qubit correction patch. [van den Berg et al.](https://doi.org/10.1038/s41567-023-02042-2), [von Lüpke et al.](https://doi.org/10.1103/PRXQuantum.1.010305).

The selected operation therefore remains standard ancilla recovery/reset with an unacquired joint model. All paper versions, decisive page locations and failed acquisitions are recorded in SOURCES.md.

## Decisive experiment and rejection rules

The next useful experiment is one controlled local gadget test, not a large memory campaign.

A. On three data qubits implement S1=Z1Z2, S2=Z2Z3 and Q=X2. Verify both active pumping and the inactive input (|000>+|001>)/sqrt(2), including its coherence and an external reference. Reset the apparatus each trial. The exact coarse channel preserves that inactive coherence; separate syndrome measurements remove it. Report the measured instrument and declare which generator is being pursued.

B. On the same device with correction/reset drives enabled, inject a calibrated bounded detuning and a separately controlled physical Z floor. Measure the floor's magnitude, bandwidth and spectator effects; acquire the residual noise catalog and out-of-catalog error. Check multiple times, correlated shots, leakage, drive-induced heating and drift. Do not substitute virtual-frame bookkeeping or a colored-noise exponential fit for an actual floor.

C. Acquire the entire correction/reset duration and noisy channel. Repeat isolated and overlapping triggers to test the proposed time law. Queueing or skipped triggers must enter the implementation model. A planned Poisson random-number generator does not certify the resulting physical map.

D. Compare against same-apparatus phase calibration/echo/DD and periodic coherent recovery with the floor removed where the incumbent permits it. Match wall time, initialization, readout, controls, entropy export and calibration effort. Use a held-out noise realization/test period. The primary endpoint is unconditional channel error or useful lifetime at a fixed infidelity.

E. Only after an actual eleven-data-qubit implementation and a useful numerical fault-rate criterion exist can these local measurements be assessed against the memory theorem. Four-dimensional connectivity, all incident rates, source imports and noisy initialization/final decoding remain separate gates.

Reject the exact C_pair claim if the inactive-coherence test fails. Reclassify a working finer instrument explicitly instead of hiding its extra dephasing. Reject the sparse-floor transfer if an unbounded/out-of-catalog term or uncharged reset correlation is found. Reject a superiority claim if the equally informed retained-drift/periodic/echo incumbent matches or wins. A successful local test would validate that local primitive only.

## Provenance and limits

Only this worker's directory was written. W and R/originals were read-only. No peer worker outputs were read, no subagent was spawned, no package was installed, no external message was sent, and no hardware experiment was run. Inputs and acquired primary sources are hash-pinned in the receipts and FROZEN.json.

Internal local algebra and exact arithmetic: checked at the declared finite sizes.
Imported global memory theorem: not re-audited here; external correctness remains unestablished.
Historical priority of the supplied compiler: not adjudicated here.
Physical joint regime and practical rate advantage: NOT_ACQUIRED / NOT_ESTABLISHED.

The consequential missing operation is a paid apparatus-to-generator bridge with a usable error margin. The existing algebra is not that bridge.

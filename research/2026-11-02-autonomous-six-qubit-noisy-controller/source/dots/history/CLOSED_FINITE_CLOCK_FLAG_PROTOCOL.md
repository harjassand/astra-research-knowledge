# Reconciled finite clock / flag / cache source

Exposure update 2026-11-01 16:26 UTC: after FIRST_DERIVATION.md, read the root's ROOT_OVERLAPPING_PAULI_PROBE_ALGEBRA.md and the sibling's 03_reconciled_small_qubit_clock.md. This proposal uses those supplied ideas and is not independent-origin evidence.

## 1. Concrete bounded-size machine per check

Assume bounded check weight w and bounded overlap degree Δ. Give check p: one probe a_p; active bit A_p; bad bit B_p; cache C_p (and optional valid bit V_p); a finite physical-qubit clock with M=O(w+Δ) phases. No mobile particle number sector is needed. Use the sibling's monotone domain-wall plus mode clock, adjacent 01->10 sorting repair, and a return phase. This is a static low-arity GKSL machine, NOT a claim of a two-body Hamiltonian realization.

One legal computation cycle executes:
1. Set A_p=0, reset B_p=0, and prepare probe in rho_prep=(I+s X)/2, 0<s<1. Use separate phases if necessary.
2. Set A_p=1.
3. For every overlapping neighbor q, execute one atomic channel: inspect A_q; if 1, set BOTH B_p and B_q to 1; otherwise do nothing. This is a classical irreversible TP channel on three physical bits, realized by explicit Kraus operators mapping each computational-basis input to the prescribed output. It dephases these bits; no clean classical bit is assumed. Neighbor degree/wiring is charged.
4. Execute controlled P_j for j=1,...,w on a_p and the appropriate data qubit.
5. Perform X measurement on a_p. If B_p=0, overwrite C_p with measured sign and set V_p=1. If B_p=1, discard the outcome and leave C_p unchanged. This is a TP instrument, with accepted/rejected outcome physically available to the detector; readout errors and inefficiency are admitted separately. An accepted same-value write still counts as a readout/overwrite, not as a cache bit flip. There is no output queue or downstream acknowledgement.
6. Set A_p=0. Complete clock return without data operations. Repeat.

Hold A_p=1 through step 5. Reset B_p only in the next step 1, while A_p=0. There is no waiting on neighbors, flags, detector acknowledgements, or decoder state. Every branch of every step advances its clock.

For any step channel E(rho)=sum_alpha K_alpha rho K_alpha†, implement clock-labelled jumps
L_(j,alpha)=sqrt(kappa) T_j tensor K_alpha.
Since sum K_alpha†K_alpha=I, sum L†L=kappa T_j†T_j. Thus on a legal enabled phase the total outgoing hazard is exactly kappa for EVERY data/probe/flag/neighbor state. Directed gates are the special case of one unitary Kraus operator. This removes coherent transport dark states by assumption of a stated low-arity dissipative primitive; it does not derive that primitive microscopically.

A phase condition uses the mode bit plus at most three clock bits. Scan uses three flag bits; readout/cache uses probe, bad bit, and cache (add a phase for valid bit if needed). Hence a fixed arity bound, approximately seven or eight physical qubits depending on encoding, suffices. Count all physical clock, probe, flag, cache, source/reset, detector and wiring faults.

## 2. Collision marking proof and timing boundary

In an ideal valid-clock history, suppose extraction phases of p and q overlap. Let q be the one whose extraction starts later. Before q starts extraction it has already set A_q=1 and scanned p. If its scan sees A_p=1, both bad bits are marked. If its scan sees A_p=0, p must become active later in order for extraction phases to overlap; p then scans q while A_q remains 1. Thus one scan marks both before the later relevant extraction proceeds. Because neither bad bit is reset while its active interval continues, both readouts reject.

More simply, compare the active-start order: the later starter scans the earlier one while it is still active if their extraction intervals will overlap; otherwise the earlier has completed before the later extraction, so there is no damaging extraction overlap. Long scan phases merely increase false rejections. Atomic test-plus-mark-both avoids a stale multistep flag-write race. An implementation that separates those operations needs its own handshake proof.

This proof excludes clock faults, bad-bit loss, active-bit errors, and interrupted/reset probes; those are explicitly physical faults, not clean flags. Root's completed-controlled-Pauli algebra explains why ideally completed rejected probes do not damage protected logical observables. It does NOT make their reports reliable.

## 3. What 'under all neighbor histories' can mean

Clock completion: YES. On valid clocks it is an Erlang sum of M fixed-hazard phases (plus return), regardless of all neighbor flag histories. Neighbors may set B_p but cannot disable a phase. Sorting gives a finite path from every invalid bit string to a legal one; an explicit local finite Poisson word can repair and complete from any state. Invalid competing transitions/noise require the sibling's repair-rate domination or a finite-time perturbation estimate; do not call invalid steps correct extraction.

Accepted fresh service: NOT under every externally fixed neighbor history. A neighbor artificially held active, or an adversary continually clearing/setting flags, can spoil every attempt. No protocol whose acceptance requires collision freedom can promise otherwise. The valid statement is a uniform conditional positive service probability over the ACTUAL joint autonomous clock law, for every initial neighborhood state and every past history. Do not condition away the future randomness supplying the quiet window.

## 4. Uniform local service minorization

Take the target p and every check sharing its data, a conservative finite closed neighborhood N[p]. For each initial classical clock configuration choose a finite allowed transition word:
(a) sort each clock into a legal state;
(b) run every neighbor to its phase just after A_q=0, then suppress its outgoing clock events;
(c) advance p to reset/preparation and then through a complete scan/extract/readout, keeping neighbors frozen inactive.
All phases are nonblocking. Initial A/B/cache values are removed where needed by actual reset phases. While neighbors are inactive, scans by outside checks do not mark them; only direct neighbors can mark p, and these are frozen. Include all channels capable of changing the local active/clock/flag state in the event's excluded-channel rate bound.

If each required jump has rate >=k_min>0, total relevant channel rate is <=R, word length <=L, and each word step is allocated a slot h, then a conservative bound is
p_word >= exp(-R L h) (k_min h)^L
(up to fixed factors for specified reset/readout Kraus outcomes). For service occurrence do not prescribe the measurement sign: sum both accepted outcomes, so the report quantum state does not suppress the hazard. Set T=Lh, minimizing over the finitely many initial configurations. This produces a strictly positive constant independent of total code size, though it may be impractically tiny.

Clock coherences are not an excuse to assume a classical initial state. One option is explicit local dephasing instruments with jumps sqrt(nu)|b><b| on each clock/flag bit. A finite prefix in which every relevant bit is dephased removes coherences; sum all outcome branches and choose the continuation word branchwise. This is an analysis partition of trajectories, NOT a hidden controller. Each branch has the same finite worst-case lower probability. All dephasing hardware/noise is charged. Alternatively prove the minorization as a CP operator inequality directly.

Preparation rho_prep gives instrument E_z(rho)=[(1+s)/2] Π_z rho Π_z + [(1-s)/2] Π_-z rho Π_-z in the collision-free full-check case. Thus an accepted event is an actual QND parity acquisition with imperfect classical sign, not a perfectly reset probe. Add detector error and decoherence to its local error budget. The usable service probability must retain the sign-quality factor; mere cache overwrite is insufficient for a decoder.

## 5. Noise and limitations

The service word proves an ideal-generator finite-time minorization, not a uniform clean-event probability for arbitrary coherent local perturbations. For Markovian stochastic helper faults one may include no-fault events with their actual finite rates. For coherent helper/data perturbations there is no no-fault event; derive a bounded local finite-time CP-map perturbation estimate or the parent's proposed positive-operator drift. In particular, do not export a global diamond error growing as total runtime.

The sibling's sorting clock proof concerns unitary computational words and a dressing. Here reset, flag, and measurement stages are CP, not invertible. Its clock-state repair path and fixed-hazard argument transfer, but its entire unitary-dressing theorem does NOT automatically transfer. Define the observable's stage-dependent instrument dilation and charge invalid CP steps explicitly. Ancilla/probe reset is allowed only at the proper phase; invalid premature reset is a real data disturbance, not harmless recycling.

All prior hardware caveats remain: bounded-arity labelled GKSL jumps are specified engineered primitives; no native two-body realization is supplied. The joint service bound is a conditional construction for bounded w, Δ, physical wiring and total local rates. Same-resource active extraction gets exactly these couplings, clock, flags, resets, and detectors; there is no superiority claim.

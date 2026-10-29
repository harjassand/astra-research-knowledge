# Exact two-site leased updates with one-site dissipative resets
Date: 2026-10-29. New complementary construction. Exact clean result; noisy fault-path completion remains open.

## Locality convention — explicit
A physical **site is one finite-dimensional qudit** carrying a data register and a finite internal clock/controller alphabet. 'Two-body' below means a term acts on two such neighboring physical qudits. It does NOT mean two elementary qubits after binary encoding the qudit. The latter reduction is an additional problem. No grouping of a system-size-dependent block is used: degree, data dimension, number of update types, and Kraus rank are fixed constants.

Primary comparators:
- Nagaj–Wocjan, *Hamiltonian Quantum Cellular Automata in 1D*, arXiv:0802.0886, Eq.(11), https://arxiv.org/pdf/0802.0886 . Already gives nearest-neighbor two-qudit program/data interactions, with 10-dimensional sites and autonomous unitary computation. It assumes a prepared legal program/input and is not the reset/noisy threshold construction sought here.
- Lloyd–Terhal, *Adiabatic and Hamiltonian computing on a 2D lattice with simple 2-qubit interactions*, arXiv:1509.01278, https://arxiv.org/abs/1509.01278 . Stronger elementary-qubit locality via a first-order effective Hamiltonian. Its perturbative passage is not a supplied uniform noisy runtime fault bound.
- Breuckmann–Terhal, arXiv:1311.6101, https://arxiv.org/abs/1311.6101 . Local space-time clocks are established prior art.

## Hardware alphabet
Orient each allowed neighboring edge e=(a,b). Site a is its controller; site b its partner. Each site has a single clock label chosen from:
- R: ready;
- C_s(e), s=1,...,m_e: pre-emission controller labels;
- D(e): emission completed but partner remains leased;
- T(e): controller awaiting final release reset;
- P(e): partner leased to controller e.

Tags refer to incident edges only. For one rank-m update per oriented square-lattice edge, outdegree=indegree=2, the clock dimension is 1+2(m+2)+2=2m+7. With m=2 and one data qubit it is a 22-level site. A finite number of update types per edge multiplies this by a fixed factor. No hidden neighborhood projector occurs.

Given a CPTP two-site data map Φ_e=Σ_s K_es(·)K_es†, define

A_e=Σ_s K_es ⊗ |C_s(e),P(e)><R,R|,
B_e=I_data ⊗ |T(e),R><D(e),P(e)|,
H=Σ_e [g_e(A_e+A_e†)+u_e(B_e+B_e†)].

Each term is two-site, finite range. ||A_e||=1 by Kraus completeness, ||B_e||=1; coefficients may be fixed finite constants independent of volume/runtime. Controller-only jumps are

L_es=√κ_e I_data⊗|D(e)><C_s(e)|,
J_e=√κr_e I_data⊗|R><T(e)|.

These are one-site jumps, not two-site resets.

## Protocol
1. RR↔C_sP coherently reserves both endpoints and performs the update's Stinespring isometry.
2. Emission C_s→D applies Kraus operator K_es, summing to Φ_e, and leaves both endpoints busy.
3. DP↔TR coherently releases the partner.
4. One-site reset T→R releases the controller.

The partner can start another operation while the old controller is T. A reverse release then cannot take the partner back unless it is ready again. This changes timing only; it cannot undo the completed data update.

## Exact clean intertwiner
Define abstract clocks with one C(e) label instead of the resolved C_s(e) labels. Start all clocks R and close the legal configuration set under the four steps above and their Hamiltonian reverses. Pending pre-emission edges form a matching: both endpoints are unavailable for other starts.

For a legal configuration c let P(c) be its pending matching. Define W_c by replacing each pending C(e) label with the Kraus isometry Σ_s K_es⊗|C_s(e)><C(e)|, leaving other labels unchanged. Pending edges have disjoint supports, so these maps commute and W_c is an isometry. Different abstract configurations give orthogonal occupation/phase sectors. Their direct sum W is an isometry.

The physical Hamiltonian obeys H W=W(I_data⊗H_clock): starts add one disjoint pending edge, reverse starts remove it via Kraus completeness, and releases are data-trivial clock transitions. The jumps obey

L_es W=W(K_es⊗√κ_e b_e),
J_e W=W(I_data⊗√κr_e j_e),

where b_e changes C→D and j_e changes T→R in legal abstract configurations. Summing s makes the no-emission losses data-trivial. Thus emission locations/times have a data-independent clock law and every first-stage emission applies exactly Φ_e at finite rates. No adiabatic elimination or externally perfect timing is used.

This proves an exact autonomous compiler for a **family of two-site update channels**, not yet a compiler of every high-body automaton update. A high-body update can be decomposed into a finite gate sequence, but the robust distributed sequencing/program flags must still be supplied and analyzed rather than silently assumed.

## Small explicit gate/channel family
Two-site unitaries CNOT and SWAP have rank1; one-site H and T can be included as H⊗I or T⊗I in a lease. A data reset has rank2, K0=|0><0|⊗I, K1=|0><1|⊗I. This fixed family supports measurement-free error-correction circuits with ancilla reset. The lease matrices are explicit controlled finite-alphabet transitions, not an unexplained high-rank channel oracle.

## Hostile clock faults and a failed repair shortcut
A fault resetting a controller C or D to R while its partner remains P creates an orphan P. Under the displayed clean generator, that orphan can persist forever. Thus the clean compiler alone has a perfect-legal-clock premise and is not a noise threshold result.

Adding a weak one-body watchdog resetting every busy label to R at rate μ repairs orphans, but interrupts healthy leases too. Healthy interruption rate is μ times lease occupancy; multiplying by orphan lifetime O(1/μ) can leave an occupancy contribution comparable to the healthy lease duty fraction, independent of μ. Long rare orphans also have strong temporal correlations. A simple μ/Γ+δ/μ heuristic is insufficient to establish local fault strength.

## Two-body fault-triggered repair candidate (not yet a proved noisy threshold)
Add distinct local repair labels Z. Let F_e=Σ_s|C_s(e)><C_s(e)|+|D(e)><D(e)| on controller a and P_e=|P(e)><P(e)| on partner b. Add

H_partnerrepair,e = g_r (I−F_e)_a⊗(|Z_P(e)><P(e)|+h.c.)_b,

and for each controller label f∈{C_s(e),D(e)},

H_controllerrepair,e,f = g_r (|Z_f(e)><f(e)|+h.c.)_a⊗(I−P_e)_b.

Every Z label has a one-body decay √κ_r |R><Z|. These terms are two-site. They vanish exactly on every clean legal lease history, so do not perturb the exact clean intertwiner. They activate only on missing-owner/missing-partner clock sectors. An arbitrary initial Z state also decays.

Normal lease dynamics conserves the orphan indicators F_e(I−P_e) and P_e(I−F_e); it cannot spontaneously supply a missing matching partner because start requires RR. The repair couplings remove orphan states through genuine finite-rate reset, not an ideal watchdog clock. Simultaneous repair branches can block one another's reverse transitions, but decay remains available. A uniform joint repair-time/fault bound under ongoing noise remains to be proved; absence of an obvious dark state is not that proof.

## Thermal and energy interface
Upward reversals of L_es, J_e or Z decays are one-site physical faults. With q=κ_up/κ_down fixed, their local generator norm is bounded by twice the sum of upward rates. For fixed g,u,κ,κr and finite alphabets, this is a finite local noise budget independent of N,t. It is NOT zero, and thermal jumps may leave the legal clock subspace; repair and data-fault analysis are necessary.

Preparing R clock states and low-entropy recovery ancillas costs entropy export. Repeated corrections require reset power/cooling capacity proportional to device volume at fixed activity. A finite-gap thermal reset obeys detailed balance only in a physically consistent bath regime. Degenerate clock transitions plus irreversible reset generally require a driven/non-equilibrium reservoir; a time-independent rotating-frame model is not a free equilibrium refrigerator. No claim is made that a finite closed battery powers indefinite computation. These are hardware resource specifications attached to the permitted one-body reset primitive.

## Regression
`two_site_lease_test.py`: overlapping edges 0→1→2, rank2 nonunitary maps, physical dimension480, ten legal abstract clock configurations. Isometry, H intertwining and all six jump intertwining residuals are exactly zero in the numerical regression.

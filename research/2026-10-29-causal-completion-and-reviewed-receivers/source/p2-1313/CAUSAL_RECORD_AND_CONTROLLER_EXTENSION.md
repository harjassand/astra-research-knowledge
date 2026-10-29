# Causal coarse records and quantum controllers

Root construction, 29 October 2026. This extends [CAUSAL_BOUNDARY_COMPLETION.md](CAUSAL_BOUNDARY_COMPLETION.md) and needs its own review. A faithful causal model of a noisy controller is not automatically noiseless computation.

## 1. Retain the controller rather than hiding its errors

Let D be an explicit bounded controller subsystem in the complete memory. Allow

    H_c(t)=sum_a B_a(q,p) tensor K_a(t),                    (1)

where B_a is a smooth modular control from the central theorem, K_a is bounded Hermitian on D and specified memory, and integral sum_a||K_a|| is finite. On the compact core, B_a=P_a,L tensor I_g. Define the reference

    H_ref(t)=sum_a P_a,L tensor K_a(t)
                        + I_L tensor H_g(t).              (2)

K_a and the memory coefficients in H_g need not commute. The first term is bounded and spatially constant in gauge coordinates. It commutes with gauge derivatives, leaving the torus Sobolev construction intact. Bounded perturbation supplies the physical propagator too.

All finite insertion histories remain common. Source differential words commute through the gauge-independent logical/controller controls; memory coefficients stay in their original chronological order. Intervening controls are unitary, so the word bound remains M C_0^(2k)((2k)!)^2 times the residual coefficient product. Hence

    ||F(T)V_0-J U_ref(T)(I_L tensor Q)||<=2E_k(T).           (3)

This is a causal logical-controller-gauge reduction. If K=theta'(t)Z_D multiplies f(q), the reference contains Z_L Z_D and retains that logical fault. It does not classify a noisy nonlinear actuator as protected polynomial background. A single causal controller law is allowed; unrelated laws chosen after seeing future interventions are not.

## 2. Global meaning of an actual coarse record

For square-cell parity, let

    Pi_mu(q)=sum_(m mod 2=mu) 1_[(m-1/2)L,(m+1/2)L)(q).

The physical position row gives, a.e. at boundaries,

    J^dagger Pi_mu(q)J=|mu><mu|_L tensor I_g.               (4)

Thus the complete source-retaining copy

    B_Z=sum_mu Pi_mu(q) tensor |mu>_C|mu>_E|mu>_F0          (5)

is exactly logical Z copying tensor identity on gauge, globally in SSS. C,E,F0 are fresh targets. F0 may be retained untouched as the actual report boundary; the complete comparison still keeps it. E may return later, while C is the actual selector. An extra fine position/ADC record is a different instrument; keeping it in a hidden purifier does not turn it into (5).

The reference copy preserves every periodic gauge Sobolev norm. The physical copy can create sharp boundaries on an actual spread state. That does not enter the finite expansion: on every raw compact history it is a logical-only map preserving physical finite-word domains. No derivative is moved backward through an actual sharp-record output.

## 3. New hidden returns and causal instrument composition

Insert finitely many copies (5), fresh finite record targets and controls (1) at their physical time boundaries. Use the same chronological bounded-memory coefficient law in both processes. Newly written E can occur in later coefficients, for example p_R q_B tensor X_E followed by q_R p_B tensor Z_E, with R and B still explicit source modes.

Induction over intervals proves equality of all finite reference histories: differential words preserve K; reference controls preserve K; copies act identically on logical/controller factors and do not change gauge support. Actual suffixes are isometries. The segmented finite expansion gives

    ||F_circuit V_0-J U_ref,circuit(I_L tensor Q)||
                                               <=2E_k(T), (6)

with the same total-lifetime b. U_ref,circuit is a chronological normalized unitary/isometric circuit, not one final unitary if new records are born. No operator is moved backward across its birth copy, no memory coefficient order is changed, and no polar normalization reweights histories.

An old oscillator remains explicit for every later unbounded interaction. Fresh finite record bits do not renew oscillator moments. Fresh encoded oscillator injection needs its actual preparation and joint word ledger. Hidden records cannot silently become clean targets, controlled sources or fresh ancillas.

### When the reference is the intended computation

Require later controls to depend only on faithful actual C and an explicitly transported digital frame. Residual coefficients preserve all actual selector projectors. Include an untouched F0, or another declared physical report-retention boundary, and independent fresh copy targets. Then each interval of reference gauge-memory dynamics is normalized within every controller sector. Induction on actual classical histories gives precisely the intended reduced logical/record instrument: future trace-preserving gauge operations cannot reweight earlier probabilities. Arbitrary initial logical-memory correlations remain allowed.

Here the intended controls specialize to known scalar envelopes within each faithful controller sector: K_a(t)=sum_h k_a(h,t)P_h tensor I_hidden. Extra quantum actuator couplings in (2) remain logical noise. The faithful-selector implication begins **after an accurately acquired copy**. Commutation with final record projectors is not sufficient during its coherent acquisition pulse, when the intended meter Hamiltonian itself changes C. A Z_C detuning commutes with those final projectors but can make the copy wrong; Section 4 retains that fault explicitly. This timing qualification was made explicit after the scoped record review.

If C is corrupted, the reference keeps the wrong selector and its resulting wrong control. The physical/reference reduction can remain accurate while the intended computation fails. Digital rewrites need explicit conjugation or immutable history, as in the saved forward-memory lemma.

## 4. A concrete finite-duration meter interaction

For a fresh finite meter qubit C define P_-^f=(I-f(q))/2 and

    U_copy^f=exp[-i(pi/2)P_-^f tensor(I-X_C)].              (7)

On the protected band P_-^f is the logical-one projector. The exact identity exp[-i(pi/2)(I-X_C)]=X_C shows that (7) copies logical Z with no untracked relative branch phase. Two subsequent acquired CNOTs C→E and C→F0 create the remaining copies. The interaction includes a local meter drive and a quadrature-periodic meter coupling; neither is a free classical computation.

Use finite g_r from [FINITE_HARMONIC_CONTROL.md](FINITE_HARMONIC_CONTROL.md) instead. Its global difference from f gives

    ||U_copy^g-U_copy^f||<=pi delta_r/2.                    (8)

In continuous execution the common polynomial background is included for the full pulse duration. Meter noise and the digital copy/readout noise either appear explicitly in the bounded controller model (2), or are separately acquired complete-port discrepancies. They are not suppressed merely by increasing k.

Two reference interfaces are legitimate and distinct. One inserts the ideal completed coarse copy (5) and separately compares an acquired meter at the same physical boundaries. The other includes the actual finite-duration smooth coupling (7) in (2) and carries its controller faults into a potentially noisy logical readout. The latter gives an accurate intended instrument only after those faults are bounded. A physical reporting/decoherence interface is still required; coherent copying alone is not an acquired classical readout.

## 5. Reach and reuse boundary

This constructs a causal native-control instrument with complete coarse records and newly returning hidden memory. The reference also supplies a place to analyze real actuator faults and wrong selectors without conflating them with polynomial background. It is a foundational reduction with a physical interaction target, not a device-performance claim.

Initial encoded supply, nonlinear coupling delivery, period calibration, entire lifetime exposure, meter/digital operations, eventual collection/readout/flags and renewal are paid. The result does not show that native ports beat measurement-free hybrid QSP or conventional finite-energy GKP protection on those costs.

The torus gauge may spread beyond K. Periodic smoothness is not physical moment regularity after J, because the physical boundary gluing is twisted. A new per-call Gevrey qualification or a zeroed exposure budget does not follow. The theorem is from the qualified initial boundary over the complete window; unconditional causal renewal is a separate problem.

## 6. Evidence and review scope

The central canonical and finite remainder machinery is an accepted dependency only at its recorded scope. This controller/record extension has a separate review. Exact finite fixtures test copy phases, memory chronology, corrupted-selector controls and causal marginals; they do not prove continuum domains or acquired device performance. The conventional companion independently checked (4) and (7)-(8), with the source-retention and report-boundary qualifications preserved.

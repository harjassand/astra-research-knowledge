# Scoped independent review: finite global-budget controller startup and native activation
2026-10-30. Reviewer: `challenge_live_busy_energy`.

## Verdict and exact sources
**Scoped PASS with the completing support, warm-margin and parameter-order details below.** The operation earns finite controller startup, finite boot-reset shutoff, and finite activation of the actual native memory under the instantaneous TOTAL joint cb-norm budget, including unknown bounded-strength defective controllers. It starts from SUPPLIED physically encoded DATA and does not assume exact ready controller hardware at a finite time.

Root source reviewed and copied verbatim:

- `global_budget_noise_root_20261030/FINITE_BOOT_ACTIVATION_CANDIDATE.md`
- SHA-256 `d037fa74cabe62e5a4820f5f765837192d0d337a1cb64d86c2e71c35e7b07738`.

Actual inherited finite-activation interface reviewed and copied verbatim:

- `recipient_memory_bridge_20261030/FINITE_NATIVE_ACTIVATION_AND_WARM_CHANNEL_V2.md`
- SHA-256 `25f4a6ed35d23c6cc8993267c7b710241e1499757984223fea5aa4c590297a33`.

Its accepted whole receipt and independent hostile component proof were read, not merely their status labels. Only the first-OFF support, finite CP waveform, positive warm replacement and BUSY initialization portions are reused. No Bell-resource, carrier, source-waiting, old-generator or teleportation noise scope is imported.

The preceding global-budget receipt, SHA `8712be47c16d6953389ef47a6efcce43590bb84c8163e286f0a9de6c2cf02171`, remains unchanged. In particular its earlier boot-switch limitation is not retroactively edited: THIS is the separately earned finite-switch composition.

## 1. Exact input and physical schedule
The initial channel is physical Enc(rho_LR) tensor a fixed controller/monitor/pointer/bath state, with arbitrary logical/reference rho_LR. The ancillary state may have arbitrary internal correlations but is fixed independently of the unknown logical input. A broader small-error input is allowed only through its separately proved positive common-span contract; none is presumed from a syndrome or fidelity estimate.

Use these supplied finite-rate controlled modes:

1. **Boot dwell.** Nominally ALL native acquisition/reversal, consistency-abort, commitment, C-payload/terminal, cleanup, verification and ready transitions are off. Only complete onsite hub clock/workspace resets to A0,W0, resource-tag resets to free, optional compatible label-preserving monitors, and the separate bath-only evolution remain. These nominal system maps act as DATA identity.
2. **Boot-reset OFF waveform.** Ramp those reset rates to zero over a fixed interval, retaining native activation off throughout. Rates remain nonnegative. This stage is still DATA identity and preserves every already-ready owner.
3. **Native ON waveform.** Ramp the actual native Hermitian edge-plus-adjoint coefficients and resolved nonnegative jump rates to their final values over a fixed interval Delta_on. Boot resets are already off. The final generator is the SAME accepted unified apparatus, with fixed later zeta, new Ai aborts, actual monitors and the one chosen first amplitude epsilon.

These statements describe the nominal commanded modes. Actual faulty local mode switches, missing resets or unwanted retained couplings need not obey them exactly: their bounded-body differences are charged to the SAME total budget at EVERY stage,

    sum_Z ||N_Z*(u)||_cb<=eta N.

Thus the proof does not assume that unknown defective components obediently turn off. It does assume the declared global commands/control resources and that all deviations across the schedule satisfy this joint-norm model. A corrupted unbounded-fanout command source or unmodeled classical controller is not covered.

At every stage the actual total evolution has the stated normal CPTP propagators. In the analytical nominal activation, remove ONLY the weak first A0<->A1 Hamiltonians, together with their adjoints. The remaining time-dependent nominal evolution is genuinely CPTP. No inverse dissipative interaction picture is used.

## 2. Global boot-count event, with no sitewise success assertion
Let P_i be the primitive nonready reset-block projections: one for each hub clock/workspace block and resource tag block. They commute. Let D_prim=sum_i P_i and m_prim<=nu N. During the boot dwell,

    L_boot,0*P_i=-kappa_i P_i,   kappa_i>=kappa>0.

Optional monitor terms must annihilate these tests, as actual label-preserving monitors do. Set

    H_boot=product_i(I+theta P_i).

The accepted global completion proof applies directly. It yields

    L_boot,actual*H_boot
       <=-lambda_H H_boot logH_boot+C_H theta eta N H_boot,
    lambda_H=kappa/(1+theta).

From arbitrary ancillary input, log Tr(H_boot rho_0)<=nu log(1+theta)N. Choose a fixed dwell T_boot and then eta so that

    exp(-lambda_H T_boot)nu log(1+theta)
       +C_H theta eta/lambda_H
       <=(alpha/2)log(1+theta).

Then the ACTUAL boot-deadline event satisfies, uniformly over logical/reference input,

    Pr(D_prim>alpha N)<=p_boot,
    p_boot<=exp[-(alpha/2)log(1+theta)N+O(1)].       (2.1)

A permanently hot module may still be nonready with probability one; only the total count is controlled. No old subset law, independence of resets, monitored trajectory record or known defect set is used.

Let C_boot=1_(D_prim<=alpha N). This controller-only projection is inserted ONLY analytically at the deadline. The actual boot channel and its C_boot compression differ by at most 2sqrt(p_boot) in the reference-stable trace/diamond comparison. Propagate that comparison through the SAME REAL CPTP reset-OFF/activation suffix FIRST. Its norm cannot grow. In particular the error is not fed through a signed Dyson truncation whose norm might be exponentially large.

## 3. Strong ready invariance and support of the entire order-one activation
The strong Ready_h projector is A0,W0 with no own o_h or z_h tag, with monitors unrestricted. The actual first-OFF alphabet preserves this subspace term by term, including when all other owners have malformed clocks/workspaces:

- later acquisition, C payload, commitment, verification and ordinary abort terms have no source on a genuinely ready owner;
- A0 refresh fixes its ready target;
- another owner changes only its own tags/private variables and cannot create h's tag or dirty h's workspace;
- label-preserving monitors keep the predicate;
- boot tag/hub resets, while present in the earlier ramp, also preserve every ready owner.

The only missing native edge that can create activity from Ready_h is exactly the first acquisition. Therefore all nonzero first-edge amplitudes during activation are charged insertions, not nominal noncreating dynamics.

A primitive nonready block can witness only a bounded number of nonready owners. At C_boot, every ket/bra controller mask has an owner set S with

    |S|<=c_prim alpha N.

For Q_S=product_{h not in S}Ready_h, the nominal first-OFF propagator preserves Q_S. Its Stinespring/Kraus coefficients have DATA identity outside the union D(S) of full owner footprints. Every physical DATA Hamiltonian belongs to a busy owner's C phase; physical terminal/abort/commit/reset jumps are DATA identity. This full-Hilbert statement is why arbitrary order-one native payloads during the ON ramp do NOT cost an uncontrolled order-one extensive error source.

A physical local insertion on at most q system sites can affect at most a_act owner ready predicates and act directly on at most q_data DATA qubits, with fixed constants after grouping. Its bath coefficients do not change this finite SYSTEM support statement. It maps Q_S into Q_(S union A(Z)). Subsequent strong nominal evolution stays within the enlarged union. The same argument applies after multiple insertions and to coherent S,S' coefficients separately; no union over all possible masks is taken.

Initial nonready controllers can carry arbitrary coherent workspaces. Their payload action may be nonmonomial but is still confined to D(S). Auxiliary-only resets/measurements may steer correlated coefficient states, yet remain DATA identity operators and cannot create a new DATA support outside the charged union.

## 4. One forward TOTAL-norm insertion budget, including the boot interval
Expand the REAL projected channel

    E_actual,suffix C_boot E_actual,boot

around the actual nominal CP boot/reset-OFF/first-OFF activation segments. The projection at the fixed boot deadline has completely bounded trace norm at most one. It may be interposed in the expansion without increasing its norm tail. Although it is a global controller count projector, it is DATA identity and preserves the label masks; it does not enlarge any DATA coefficient's support.

Count all physical noise during the full finite interval T_total and every nonzero first-edge Hamiltonian during its ON waveform. There is a fixed C such that

    A_int:=integral sum_Z ||D_Z(u)||_cb du
           <=C N[eta T_total+epsilon Delta_on]
           =N a_int.                              (4.1)

The first edges are OFF during the possibly longer boot dwell and reset-OFF stage. Thus epsilon multiplies only the fixed activation waveform duration, not an unpriced long preparation time.

The order-r forward Duhamel contribution is bounded by (N a_int)^r/r!. Discarding orders at or above ceil(gamma N) yields

    delta_D<=exp(N a_int)[e a_int/gamma]^{gamma N}

up to fixed rounding. Taking, for example, a_int/gamma sufficiently below 1/(4e) gives delta_D<=exp(-c_D N). The expansion is signed; only the actual underlying and projected evolutions are CP.

Before C_boot, nominal DATA dynamics is identity, so each retained insertion contributes at most q_data new DATA sites even though controllers may initially be dense. After C_boot, the strong support module above applies. With fewer than gamma N retained insertions, define conservative densities

    b=c_prim alpha+a_act gamma,
    w=q_data gamma+r_D b.                          (4.2)

Then the final strong BUSY count is at most bN, and each final left/right physical DATA coefficient has support at most wN+O(1).

At the activation endpoint apply the fixed forest inverse ONLY AS PROOF COORDINATES. It preserves strong Ready/BUSY masks and its nonidentity DATA factors belong to those same owners. Its support is already inside D(S_final), so it does NOT add a second r_D bN term in (4.2). No forest inverse is physically executed.

To avoid a convention ambiguity, let c_can be the fixed conversion from physical Pauli support weight to the total sectorwise canonical radius (it may be 2 when a Y error contributes to both X and Z weights). Let c_U be the actual unary-energy upper constant for both sectors. The retained comparison therefore obeys

    r_can<=c_can wN+O(1),
    M_busy<=bN,
    D_history<=M_busy<=bN,
    E=U+R D_history<=(c_U w+Rb)N+O(1)=E_0N+O(1).  (4.3)

All support/radius constants are fixed before epsilon and eta. They are not raw-syndrome counts or assumptions of classical Pauli mixtures.

## 5. Positive P_small handoff and fixed extensive warm gaps
Choose alpha,gamma so c_can w lies strictly inside the common canonical basin and twice the relevant physical error radius lies below code distance. Define P_small by the simultaneous bounds in (4.3), with harmless fixed rounding allowances. In forest/canonical coordinates its radius, raw energy and strong BUSY projectors commute. The signed low-order comparison is supported in P_small and has canonical logical identity on the ENTIRE coefficient span.

Let K be the actual CP/TNI projected channel at activation exit in those coordinates, and B_signed its retained low-order comparison. Then

    ||K-B_signed||_diamond<=delta_D,
    B_signed has range in P_small.

Because K is positive, its outside-P_small probability is at most delta_D for every logical/reference input. A final gentle compression has error at most 2sqrt(delta_D). Set A=P_small K P_small; A is CP/TNI, and compression contractivity gives

    ||A-B_signed||_diamond<=delta_D.

Small common DATA support and the canonical local-edge/distance condition imply

    B_signed(rho_L)=rho_L tensor tau_signed,

where tau_signed need not be positive. Fix a normalized logical omega and set

    sigma=Tr_L A(omega).

Then sigma>=0, its trace is at most one, it is supported in P_small, and

    ||A-(Id_L tensor sigma)||_diamond<=2delta_D.    (5.1)

Its trace deficit is bounded by the boot and P_small projection losses; it can be retained as TNI or normalized after charging that deficit. All controllers, pointers, monitors and the SAME bath remain in sigma. There is no hidden bath refresh or assumed independence inside sigma.

On P_small the accepted global storage bound gives the deterministic moment

    Tr(F_memory sigma)<=exp[(g+sE_0)N+O(1)].       (5.2)

Choose this coefficient and the steady memory coefficient nu_memory to satisfy

    max(g+sE_0,nu_memory)+q_t<s_prime e_cut

with a fixed positive gap. This earns the accepted GLOBAL warm-start contract, not merely low syndrome or approximate decoded fidelity.

If immediate and all-future live access is to use a smaller chosen canonical-output tail alpha_mem rather than the larger fixed killed-radius bound, impose additionally

    max(g+sE_0,nu_memory)+q_t<s h alpha_mem         (5.3)

with a fixed gap. Otherwise a merely basin-safe warm input need not already meet an arbitrarily smaller output radius at time zero. The densities can be made small enough to satisfy both (5.2)'s basin gap and (5.3); this is an explicit output precision, not an obstruction.

## 6. BUSY warm initialization without an exponential-observable error transfer
The positive sigma has M_busy<=bN. The physical embedding applies the forest/canonical representation back, but those embeddings preserve M_busy. The full-Hilbert activity observable itself need NOT commute the forest. Use only its accepted operator upper bound:

    G_busy<=exp(K delta_A M_busy).

For the physical positive warm comparison state this gives directly

    Tr(G_busy rho_warm,0)<=exp(K delta_A bN).       (6.1)

The global-budget actual BUSY law therefore yields, for every later eligible time u,

    log Tr(G_busy rho_warm,u)
      <=N max(K delta_A b,rho_A/lambda_A)+O(1).

Choose b and the shared epsilon/eta so this is strictly below k delta_A beta_out N by a fixed extensive gap. Then the positive warm process has the desired full-state BUSY-density tail at time zero and every later requested time.

Only AFTER these moments are proved on the positive warm process do we transfer bounded final events and channels to the actual startup output, using (5.1), the gentle errors and contractivity of the SAME real future joint CPTP evolution. No trace-distance error is multiplied by ||F_memory|| or ||G_busy||. Equations (5.2) and (6.1) are earned from deterministic support caps, not inferred by continuity of exponential observables.

Together with the accepted global killed comparison and the live prefix/common-span theorem, this supplies the same ordinary DATA decoder benchmark and base finite destructive-readout input at eligible times. The final error has the inherited storage factor plus exponentially small boot/activation errors. Scheduled/exogenous access remains required; no adaptive stopping or infinite-time no-excursion guarantee is added.

## 7. Noncircular one-apparatus parameter order
A sufficient order is:

1. Fix the code, local energy/support conventions, fast native hardware, new aborts, fresh dirty coefficients and positive later zeta. Fix the supplied boot-reset and reliable command resources. Construct the actual epsilon-independent first-OFF support/return constants.
2. Fix analytical s,R, a strict global basin, the desired output radius and the DATA proof constants c,d. Choose an epsilon ceiling on which all accepted local constants are uniform and g(epsilon),q_t(epsilon) leave a fixed positive energy/output gap; both entropy costs tend to zero with epsilon. Choose the fixed activity strength delta_A. No useful-service lower bound uniform as epsilon tends to zero is asserted: the actual memory threshold is fixed only after epsilon is chosen.
3. Choose positive b,w, equivalently sufficiently small alpha,gamma in (4.2), so the canonical/distance conditions, (5.2)–(5.3) and K delta_A b<k delta_A beta_out all have reserved fixed gaps. Choose the global completion theta and a fixed T_boot meeting the transient part of (2.1). Fix finite reset-OFF and native-ON waveforms and all later base readout durations. These requirements use the fixed fast support/return constants, not inverse powers of a not-yet-chosen epsilon.
4. Choose ONE epsilon below the ceiling, small enough for the native memory/live conditions and epsilon Delta_on's share of (4.1). This freezes the one final actual native apparatus and its positive memory threshold.
5. Choose ONE positive eta below that global storage threshold, the global boot-completion floor, the activity source margin, and the finite-window condition eta T_total in (4.1), together with the already accepted base readout thresholds. All durations are already finite. The permanent-defect interpretation requires c_def fR_def<eta, uniformly across every commanded mode.
6. Enlarge N0 for support/radius rounding and fixed O(1) terms in (4.3).

This order does not alternate between physically retuned devices. First edges being absent during boot is essential: it avoids imposing epsilon times an uncontrolled epsilon-dependent boot/service interval. The final small memory threshold may be extremely poor but is strictly positive and chosen only after the final epsilon.

## 8. Earned capability and retained boundaries
The construction now has an actual finite startup sequence for unknown bounded-strength defective controller/reset components, supplied encoded DATA, and a declared global joint-norm budget. Some components may never reset correctly; a sufficiently small UNKNOWN defective population is tolerated without locating it. Their missing/extra bounded dynamics are charged during boot, switching, activation and subsequent storage alike.

This does not create the encoded DATA input, manufacture a physical output port, supply a noisy global command network, or cover an undeclared loss space/infinite-strength failed component. The supplied boot-mode control is a genuine additional physical interface, now paid with finite waveforms; it is not autonomous self-starting. The old stochastic source/LOCC/carrier waiting models are not broadened. The earlier global receipt and all accepted retirement/readout sources are unchanged.

An equally informed scheduled QEC implementation must be allowed the same bounded global adversarial error budget, code distance, reset/control resources and ordinary common-span correction. No new coding principle, practical threshold, yield advantage or speedup over that comparator is established. The earned claim is closure of this specific native finite-startup-to-global-memory composition.

# Actual native autonomous LOCC Bell memory under weak continuous joint noise
2026-10-30. WHOLE-MANUSCRIPT CANDIDATE FOR FRESH REVIEW. Component receipts are not a whole acceptance. No external publication or upload.

## Result and exact scope

For a fixed CSS Tanner family satisfying the reviewed common linear-radius confinement and active-hub-density hypotheses, the actual rollback-native LOCC machine admits fixed positive rates and a sufficiently small continuous local joint-noise threshold, independent of blocklength, with the following proposed conclusion. For N sufficiently large, its framed, fixed ideal relative decoder yields k_N=Theta(N) encoded ebits, with target trace-distance/channel error

    error(T) <= 2 eta_source + C(1+T) exp(-cN),         (T)

uniformly over allowed syndrome-gauge/reference inputs and the retained bath. Here T is physical storage time. The physical starting resource can be raw physical Bell pairs; no pre-encoded Bell DATA is assumed. A noisy source requires its explicit common positive-record support/moment certificate, rather than high average per-pair fidelity alone.

This is a Bell-TARGET/gauge-input theorem, not arbitrary identity on the full two-party logical space. Its output includes the declared ideal forest frame and fixed mathematical relative recovery; no bare physical extraction, autonomous noisy receiver, arbitrary dirty startup, or practical threshold is inferred. The separately accepted native-recipient port has its own scope and is not silently promoted by this manuscript.

The nominal quantum hardware is exactly two-site hub/resource Hamiltonians and onsite separately resolved resets on fixed-dimensional GROUPED sites. Interparty transport is measured classical FIFO communication. Dimensions, capacities, circuit lengths, monitor resources and entropy export are fixed constants at fixed code degree, but can be very large. No elementary-qubit locality or coherent shared interparty bus is claimed. The finite proof circuits and spectral projectors below are analytical objects, never physical operations supplied for free.

The proof uses continuous operator bounds on the actual joint evolution. It does NOT reinterpret continuous coherent noise as Poisson fault records or import the stochastic depth-two ancestry theorem.

## 1. One actual physical generator and declared noise contract

Use the accepted native rollback integration sources, particularly EXTENDED_MACHINE_AND_OPERATOR_PROOF.md and EXPLICIT_LOCAL_PAYLOAD_GATES.md. Each hub has private clock, W, immutable active P, outer master/worker and finite reset monitor. Each DATA resource has a finite owner tag and monitor. The full read/write footprint includes all raw checks needed to evaluate every candidate energy change. It is not just the eventual Pauli mask.

The actual phases are I; A_i acquisition; C_t forward payload; B_(j,l) inverse rollback; Q_i cleanup; and separately labeled failed-test R leaves. R leaves claim all resources. C/B/R ownership persists until actual complete retirement T. C watchdogs enter an inverse B rail; there is no destructive workspace reset at nonzero B. Actual complete retirement, source-resolved over all erased W/P/classical values, enters Q0/W0/P0. Q0/W0 is mechanically good for every tag configuration. Tag cleanup and Q verification are actual local Hamiltonian/reset operations. Every complete bundle retains its actual scalar source loss; no coherently merged eraser or atomic read is substituted.

Alice's full read circuit consists of actual H, controlled-single-resource Pauli factors and H. Bob uses the same extraction, an explicitly defined finite onsite reversible lookup permutation, then workspace-controlled single-resource Paulis. The entire scratch register is retained until terminal erasure. In the exact forest frame every nominal Hamiltonian is DATA identity. Full terminals realize the actual intended read/GPT instrument; dirty partial terminals have bounded DATA support, not a fictitious completed map.

Use the explicitly VALUE-BLIND physical parameter choice: classical rates/guards depend on type but not DATA(a)/WANT(a) value; resolved bundle outcomes have equal rates; rail amplitudes/lengths do not depend on program value. Keep Alice LOAD at a fixed positive rate. Choose a common small positive Bob LOAD rate lambda after fixing the fast instance. 'Fixed positive Alice' need not be order one, but no estimate is uniform as that rate tends to zero. All other selected finite rates remain positive constants. No resource-monitor rate is weakened merely to make individual analytic killing terms positive.

Classical protocol is the accepted finite FIFO machine, including unconditional response dequeue/discard, actual G+1 SYNC purge and pending-READ retention through abort. In particular, neighboring Bob classical traffic continues at zero Bob LOAD and can drive Alice resource contention. The proof below retains that traffic.

The joint system/bath evolution must have well-defined normal interval-wise CPTP propagators on the stated common observable domain. Write the perturbation as bounded Hermiticity-preserving joint terms N_e(u), each with a nonempty SYSTEM support of size at most one fixed q, satisfying the explicit pointwise strength budget

    ||N_e(u)^*||_cb<=eta c_e(u),
    sup_u sup_system_site_x sum_(e:x in supp_sys N_e(u)) c_e(u)<=C_inc.

Thus sum_e ||N_e(u)^*||_cb<=C eta N. Bath-only terms are separated before this count. Exact forest conjugation enlarges q and this weighted budget only by fixed constants. A count bound on the number of terms without a bound on their weights c_e would NOT suffice. Terms can be centered so N_e^*(I)=0 at the accepted fixed norm cost without changing their total generator. A bath-only generator may be unbounded but must satisfy the stated propagator/domain and CP/TNI compression premises; bath-only support does not by itself prove existence. All finite-system-leg expansions and bounds are uniform in bath dimension and correlations.

The NOISE class here is deliberately the bounded-body, pointwise WEIGHTED incident-cb-budget class: partner sets may vary and need not belong to one fixed bounded-degree graph. The NOMINAL physical/read/communication graph and proof-witness supports remain the fixed bounded-degree native instance. This extension is checked directly, rather than imported from the earlier geometry-scoped noisy debt-moment receipt: a q-site noise term meets at most q fixed gate neighborhoods, its conjugated system support and energy/relative-Pauli bandwidth remain bounded by constants depending on q, and its relative norm costs C eta c_e. Summing the displayed weighted budget gives O(eta N). The radius crossing and finite-system-leg exit proofs use this bounded body size, not connectedness or a fixed noise-partner graph. A fixed graph-local noise family is an immediate narrower special case. Only NOMINAL witnesses, not the earlier noisy-moment conclusion, are imported from that receipt.

The nominal process is LOCC. The robustness contract may allow correlated quantum baths as adversarial noise; no such bath is used as a computational communication resource. If strict LOCC of the entire faulty evolution is required, restrict to local quantum baths with shared classical noise; the same estimate is a special case. This manuscript does not label a general entangled-bath fault process itself an LOCC channel.

## 2. Code, raw energy and concrete initialization

For each CSS sector use the actual integer Tanner potential U=sum_v dist(error|Q(v),C_local). It is a function of the FULL raw syndrome, with U<=2|error|, local Lipschitz bound, and integer decrease at least one for every nontrivial prescribed GPT move. Let r be the sum of the two fixed minimum-syndrome representative weights. Within a COMMON admitted radius r_dec N, strictly below both confinement and active-density radii in both sectors,

    U>=h r,          number of active hubs>=kappa_0 U. (1)

Both code distances are linear, and the rate is positive. These deterministic family hypotheses are retained, not newly proved here. No larger published radius or merely unary-energy decision information is substituted.

In the exact forest frame let B_g be the actual mechanical-history bad projector. Let D_false count EVERY false physical value token: Alice HOLD(DATA), every response FIFO DATA slot, Bob WANT in all engine phases, and P when phase-valid in A/C/B or R with A/C/B parent. P is invalid in I/Q and R with I/Q parent. WANT and a valid P can coexist and both count. LOAD consumes WANT while creating P; T deletes it. For each Bob patch h define Q_h as the OR of its current false-token condition and all mechanically dirty Alice parents whose full possible DATA support meets its compared checks. These are bounded commuting observables.

Choose fixed finite weights

    R_t>K_B,   R_B>K_B,   R_A>K_A+R_t J_A,
    E=U+R_t D_false+R_A sum_Alice B_g+R_B sum_Bob B_g,
    V=exp(sE), s>0.                                  (2)

K_A/K_B bound ALL touched raw-energy terms, and J_A counts ALL affected token LOCATIONS, not merely neighboring hubs. The reviewed full-workspace normalization and dirty-source envelopes give L_nom^*V<=0 with strict consuming/healing/improving charges. Incomplete/R prefixes are not assumed to normalize raw syndromes.

Concrete initialization for the new continuous statement is: engines I/W0/P0, all own tags absent/free, empty queues, Alice workers IDLE, Bob masters FLUSH_SEND(0), and the raw Bell-target/gauge resource with the declared source envelope. Monitor/bath/reference states may be arbitrary within the stated joint contract. This is stricter than the older stochastic theorem's allowance of arbitrary FIFO/worker contents. No unproved fast purge is used to inherit that allowance.

For ideal raw Bell DATA, relative syndrome is zero, E=0, all current GPT decrements vanish, and the later proof dressing is exactly identity on this initialized range. A certified source good instrument may instead lie in the common relative-error span with r<=z0 N and E<=e0 N (for clean auxiliaries U<=2z0 N suffices), with bad mass eta_source. The constants z0/e0 are chosen below the eventual fixed spectral margin. An arbitrary initial dirty quantum engine is not permitted: its first fast dirty reset can cause unsuppressed DATA damage.

## 3. Actual guarded A/C service and the exact credited raw potential

For Bob h, D_h requires mechanically good A/C, Q_h=0 and every overlapping FULL-footprint Bob neighbor FREE. FREE means phase I or Q_i AND no own o/z tags; it does not require W=0. The actual isolated A/C matrix includes acquisition/unacquisition, W-resolved COMMIT, C motion, finite timers/monitors and every actual abort loss. Kill it on A/C aborts and SUCCESS. The actual monitored path yields positive success effect P_s>=pI and finite survival integral R. Thus a fixed beta>0 gives

    A_h^c=P_s-beta R>0,       K_AC^* A_h^c=beta I-Gamma_s.

This is real acquisition service, not an assumed completed resource lock or abort-free C clock.

Let Phi_h be the SAME actual true-program GPT instrument and d_h=V-Phi_h^*V. The source-preserving analytic UCP credit T_h has action

    T_h(V)=V-t A_h^c d_h,     0<t<1/2.

It does not reset the engine virtually or implement a new physical operation. No one-step idempotence of GPT is assumed. On the guarded source the actual drift is `-t beta d_h-(1-t)Gamma_s d_h`; real clean LOAD entry contributes `-lambda t a_entry P_entry,h d_h`.

Full raw composition has been independently checked, including source-resolved semantic transfers, delayed dirty Alice healing, shared monitors counted once on observable blocks, actual cleanup and weak LOAD closures. A reviewer correction is essential: dirty I/Q with W!=0 can be physically FREE. Its DATA-identity, FREE-preserving reset COMMUTES neighboring credits, which must be factored through its W-healing charge, not called off-credit.

Put a_h=d_h/V on the true guard, with bounded current-relative raw-syndrome extension. Its support is the existing full decision footprint. Mutually exclusive overlapping credits and commuting disjoint normalized decrements give exact multiplicative-domain identities,

    V_c=product_h T_h(V)=V product_h C_h,
    C_h=I-t A_h^c a_h,    (1-t)I<=C_h<=I.             (3)

All C_h commute V, each other, and actual Q/B/ACTIVE masks. This is an exact local factorization; distant maps do not fix the GLOBAL d_h. No global exponentially small no-jump branch is used for local estimates.

The FULL actual raw bound, after local normalization, implies

    Delta >= c_D t sum_h D_h a_h
              +c_P lambda t sum_h P_entry,h a_h
              -C_L lambda t sum_h ACTIVE_h,           (4)

after dropping further positive charges. Here Delta=-V_c^(-1/2)L_nom^*V_c V_c^(-1/2). Complete guarded LOAD is retained, not replaced by lambda(Phi-I).

## 4. Direct conservative tilt and actual debt/activity return

Let S_t=V_c^(1/2). For actual local J_e,K_e=-iH_e-Gamma_e/2 define

    J'_e=S_t J_e S_t^(-1),       K'_e=S_t K_e S_t^(-1).

Every such operator is local with fixed enlarged support: disjoint commuting raw-energy/discount factors cancel. Local norms and inverse norms are uniform for t below a fixed t0<1/2. The tilted CP generator L_w and its conservative completion are

    L_w^*O=S_t^(-1)L_nom^*(S_t O S_t)S_t^(-1),
    L_c^*O=L_w^*O+{Delta,O}/2.                        (5)

The latter is genuine local unital GKLS with jumps J'_e and Hamiltonian `(K'_e^*-K'_e)/(2i)`. This identity holds even when individual Delta_e, or the total FULL-load Delta, are indefinite. No physical generator is split by a coherent guard.

For Bob LOAD off, the specific one-step credited gains commute every Q/B. This is an independently checked FULL-alphabet statement, not arbitrary joint-commutant preservation. Full terminals use actual complete label normalization. Dirty Alice blocks saturate every affected Q. The delicate cleanup z_h->free case pulls any newly opened A_i/A_l coherence into a wholly bad source on BOTH sides; V_c has no I/Q clock coherence that could bridge good and bad. Strong Alice LOAD, complete erasures and malformed target openings are included.

Consequently the zero-Bob-LOAD conservative generator preserves each individual Q/B zero range. The accepted raw-V tilted debt witnesses are fixed finite local operators `alpha R_v<=Z_R,v<=R_v`, where R_v lists Q_h and all B_g. Credited similarity changes their drift by O(t) inside their OWN corner, not by O(t)I. For fixed small t, restoring weak Bob LOAD only costs its actual local O(lambda) bound:

    L_c^*Z_R,v<=-r_R R_v+C lambda I.                  (6)

Actual raw-tilted Bob ACTIVE return is separately earned, not imported from the unweighted FREE receipt. The exact ACTIVE source algebra survives raw similarity, so FREE is invariant at Bob LOAD zero. The real retire/clear-own-tags/Q-return word has unchanged target supports, H and monitors, complete selected effect at least exp[-s osc(E_local)] times its original scalar effect, and bounded changed losses. Crucially those transformed complete effects/losses are block diagonal in the monitored source clock/tag labels: resets resolve source phase and retain tags or perform one fixed z-to-free transition, while V is clock/tag diagonal. They therefore cannot cancel the unique selected off-diagonal clock/tag Hamiltonian hop. A merely bounded but arbitrary off-diagonal loss would NOT suffice. The finite monitored-word theorem and local polynomial then give `alpha_A A_h<=Z_A,h<=A_h`. Credited O(t) transfer is A_h-supported; weak LOAD gives

    L_c^*Z_A,h<=-r_A A_h+C lambda I.                  (7)

All witnesses and supports are fixed for the same positive-Alice/zero-Bob-LOAD instance BEFORE choosing t,lambda. No 1/lambda-range resolvent is hidden.

## 5. FULL availability drift, contention and the repaired product

Use the independently checked reducing exposure construction and its clean, raw-commuting type extension Rbar_h for the SAME value-blind instance. Do NOT use private-pipe decoupling: Bob g's classical READ traffic drives Alice g and her shared resource locks, so h availability can depend on Bob g's master/FIFO at zero Bob LOAD. A no-move g terminal can change that availability.

Rbar_h retains all such finite-cone dependence. It is positive, locally bounded and commutes raw syndrome functions and every Bob ACTIVE mask by the accepted exact algebra. Define

    X_h=F_h Rbar_h a_h>=0,    F_h=I-A_h.              (8)

On a finite clean/true buffer G_h, the physical exposure drift, INCLUDING all neighboring protocol traffic, is `-cF_h+C P_LOAD,h+C A_h`. The last term pays actual ACTIVE-to-FREE inflow, rather than using an invalid zero extension. Clean value blindness makes this compressed derivative commute a_h.

Every clean DATA/energy-preserving operation is unchanged by the raw-V tilt on this buffer and contributes the physical derivative times a_h. The only clean DATA-changing reset is Bob full SUCCESS. Its entire source, its physical complete loss and its conservative complete loss lie in ACTIVE_g. Since X_h and Rbar_h commute A_g, every product/tilt discrepancy is supported inside A_g, even if Rbar_h fails to commute the terminal loss or reset. Its fixed norm is therefore paid by C A_g, not a generic C I. No false zero-cost assertion for a no-move terminal is needed. Thus

    G_h L_c,raw,fast^*X_h G_h
       <=G_h[-cF_h a_h+C P_LOAD,h a_h
                    +C sum_(g in local cone) A_g]G_h. (9)

The actual entry split is

    P_LOAD,h a_h<=P_entry,h a_h+sum_local R_v+sum_overlap A_g.

It explicitly charges false WANT, bad W/ownership and active neighbors. The change from raw to credited tilt costs O(t) locally, and actual weak LOAD costs O(lambda).

Clean/dirty derivative cross blocks are NOT discarded. With P_bad=I-G_h<=sum_local R_v, an explicit block Young inequality pays a zeta-sized cross term by a small debt allocation plus C zeta^2/delta on the identity. Dirty diagonals cost C zeta P_bad. All cones and incidence bounds are fixed. This is the independently reviewed repaired availability route; the failed decoupling note and its counterexample are preserved.

## 6. First-order service and the sufficient density hierarchy

Set exposure strength zeta=c_z lambda t, activity strength beta_A=C_b lambda t, and debt strength delta=C_d sqrt(lambda)t. Choose c_z small enough for the positive entry term in (9) to be absorbed by (4). Choose C_b large enough to pay the raw weak-LOAD closures, all full-availability ACTIVE terms and leave a negative activity coefficient. For lambda sufficiently small, delta dominates all dirty allocations. Equations (4),(6)-(9) give the FULL-Hilbert first-order bound

    -Delta+delta sum_v L_c^*Z_R,v
              +beta_A sum_h L_c^*Z_A,h+zeta sum_h L_c^*X_h
       <=-c lambda t B_cov+C rho_1 N I,
    B_cov=sum_h(F_h a_h+A_h)+sum_v R_v,
    rho_1=lambda delta+lambda^2 t+lambda t^2
                         +(lambda t)^2/delta.         (10)

Only fixed actual-source constants are suppressed. The extra uniform A/C charge can be dropped after it has created the real LOAD-entry service. No retained-terminal energy-payment refinement is required.

Because 0<=a_h<=1, F_h a_h+A_h>=a_h. In the admitted canonical radius, (1) and integer strict improvement give sum_h a_h>=c_s U. The fixed number of token slots per patch gives D_false<=C sum_h Q_h. Hence B_cov>=c_E E on that radius, though not globally. THIS RESTRICTION IS ESSENTIAL.

Take a fixed-color ordered proof circuit

    Y=product exp(delta Z_R/2) exp(beta_A Z_A/2) exp(zeta X/2),
    S=Y V_c^(1/2),       W=S^*S.

The independently reviewed local relative Taylor lemma gives, for the actual local J',K',

    L^*W<=S^*[-kappa D+C rho N I]S,
    D=B_cov/c_E>=E on the admitted radius,
    kappa=c lambda t,
    rho<=C[delta^2+lambda delta+lambda^2t
                   +lambda t^2+(lambda t)^2/delta+eta]. (11)

Each local relative term is exactly a sum of `(YJ'Y^-1)^*(YJ'Y^-1)` and the two `YK'Y^-1` terms. Its fixed causal cone bounds the second derivative; summing costs O(N delta^2), not N^2. The first-order killing anticommutator cancels exactly. Positivity of individual killings is unnecessary.

Same-bath local HP perturbations are conjugated through the fixed-depth SYSTEM circuit; disjoint factors cancel and only a finite system cone remains, giving C eta N. No bath dimension, selected Kraus noise budget or Poisson history is assumed. Therefore

    rho/kappa<=C[t+sqrt(lambda)+lambda+eta/(lambda t)]. (12)

This is an actual unconditional COVERAGE-observable drift. It is not yet an energy moment: S need not preserve the raw basin. The next sections repair that genuine obstruction, rather than invoking the old basin-commuting proof.

## 7. Actual outer canonical basin and common Bell module

Choose a fixed r0<r_dec with strict distance margin. Let P0=1_(r(relative syndrome)<r0N), without an energy cutoff. It commutes E and V_c because both use raw-syndrome diagonal functions and controller coefficients. All physical/proof generators have fixed local DATA support as established above. Let ell_max bound the sum of CSS relative Pauli weights in any such local system-leg expansion, with all finite frame/tilt/polynomial enlargements included.

Minimum-syndrome representatives satisfy the exact Lipschitz fact

    |r(delta+sigma(f))-r(delta)|<=|f|<=ell_max.

Thus every local P0/complement crossing has BOTH endpoints in `[r0N-ell_max,r0N+ell_max]`. For N large this lies below the COMMON admitted radius. Confinement on both sides gives a single crossing strip R0 with

    R0<=1_(E>=bN-O(1)),        b=h r0>0.              (13)

This checks the native boundary premise for all proof and physical legs. It is not inferred from low syndrome outside the radius, and no fixed noise-partner graph is required.

The correct common module M0 is the coherent span of `(I tensor R_delta)Omega_s` for r(delta)<r0N, with arbitrary auxiliary/bath/reference coefficients. A bounded Alice/Bob Pauli pair moves Alice's part to Bob up to transpose phases and an absolute-gauge shift. For two endpoints in P0 the canonical difference has zero syndrome and weight `<2r0N+ell_max<d_N`; it is a stabilizer. Hence every compressed local leg P0 O P0 maps M0 into M0, coefficientwise. This is exact linear common-span algebra, not a Pauli probability law.

Self-adjoint compressed proof generators leave M0 reducing; their exponentials, the compressed energy/discount circuit and its spectral calculus preserve it. This establishes the Bell-TARGET/gauge premise only. It need not give identity on a general two-party logical input; matched signed-sector actions can preserve the Bell target without being the identity there. The fixed ideal relative decoder maps the entire resulting module to the same Phi_(k_N) tensor an auxiliary state.

## 8. Compressed proof circuit and INNER spectral basin

Apply the separately reviewed compressed-circuit/two-basin mechanism with the actual premises just checked. On P0 H define

    Xi,0=P0 Xi P0,
    Y0=ordered product exp(epsilon_i Xi,0/2),
    A0=P0 V_c P0, S0=Y0 A0^(1/2), W0=S0^*S0>0.

The compression destroys naive geometric locality; no local Taylor theorem is applied directly to Y0. Choose a fixed a with 0<a<sb and define the INNER projector

    P1=1_(W0<=exp(aN)) within P0 H,
    F=W0+(I-P0).                                    (14)

Then [F,P1]=0 exactly. P1 is only an analysis filter; the physical apparatus never measures it.

For every FIXED integer m, energy-weighted local norms and [P0,E]=[P0,V_c]=0 give the exact higher-moment comparison

    V0^(2m)<=exp([2m c_t t+C_m delta]N) W0^(2m).       (15)

This follows from the ordered identity for A0^m W0^-m and bounded weighted norms of Y0 and its inverse, not by raising an arbitrary Loewner inequality to a power. On P1, the right side is bounded by exp([2ma+2m c_t t+C_m delta]N). Together with (13), this suppresses boundary components of EVERY partial original or compressed proof word, including a fixed number of local insertions.

Specifically block-diagonalize each Xi as P0XiP0+(I-P0)Xi(I-P0). Its difference from Xi is an R0-supported crossing. An exact one-gate Duhamel formula and O(N)-gate telescoping compare the true local circuit to the block-diagonal circuit. Boundary high moments beat all fixed coarse exp(CN) norms: first choose a<sb, then a fixed sufficiently large m, then t,delta small. This yields, uniformly on P1 and with references,

    ||P1 U^*(F-W)Vloc P1||<=exp(-c_b N)              (16)

for fixed local system legs U,Vloc, and the corresponding trace-norm comparison of S rho S^* with S0 rho S0^*. Complete actual Hamiltonian/gain/loss terms and finite system-leg expansions of joint cb perturbations are all included. Only polynomially many terms are summed.

Since S0 rho S0^* is EXACTLY P0-supported, D>=E may now be used in (11). This is the missing noncommuting-basin transfer; it is not inferred from a basin-supported input alone. Equation (16) gives the compressed full-generator drift

    Tr(L^*F rho)<=-kappa Tr(S0^* E S0 rho)
                       +C rho N Tr(F rho)+exp(-c_bN) (17)

for positive P1-supported states. All actual structural premises are detailed in ACTUAL_CANONICAL_BASIN_INTERFACE.md, independently reviewed at SHA `4e8348c2714f84b79fc57b9a4c7a6b429a19148e848cf4f885be5439783cf3cd`.

## 9. Exact entropy and actual killed-process comparison

Weighted conjugation also gives `S0 S0^*<=exp(gN)V0`, with g=O(delta). Operator-log monotonicity and polar functional calculus, without any [Y,E] assumption, imply

    S0^* E S0 >=[W0 log W0-gN W0]/s.                 (18)

Kill the ACTUAL full joint evolution at P1 using its assumed well-defined CP/TNI compression, retaining complete losses. Since [F,P1]=0, the killed adjoint subtracts positive outgoing gains from the compressed full drift. It is not the analytic tilted process that is physically killed.

For subnormalized killed rho let x=Tr(F rho), m_rho=Tr rho<=1. Spectral scalar Jensen gives `Tr(W0 log W0 rho)>=x log(x/m_rho)>=x log x`, with no assumption that rho commutes W0. Equations (17)-(18) yield

    x'<=-(kappa/s)x log x+(C rho+kappa g/s)N x
                               +exp(-c_bN).          (19)

Choose a fixed nu with `g+C s rho/kappa<nu<a`. For N large, the barrier x=exp(nu N) has negative derivative, so any admissible initial moment below it remains below it for all time. An ideal raw Bell-target initialization has x(0)=1 and lies in P1 exactly. A certified small source input pays its explicit initial moment; an initial P1 projection loses only exponentially small mass, with its gentle trace-norm cost included in (T).

For each bounded local system leg J, finite-depth uncompressed similarity gives `||S J S^-1||<=C_J`. Equation (16) transfers this to F on P1. The inner spectral complement is bounded by exp(-aN)W0 and the outer complement is controlled by (13)-(15). Hence

    Tr[(I-P1)J rho J^*]<=C_J^2 exp(-aN)x+exp(-c_bN).

Trace-norm Cauchy-Schwarz and finite system-leg expansion bound full-minus-killed generator action by `poly(N) exp[-(a-nu)N/2]`, uniformly over bath/reference. Actual CPTP propagation contracts the Duhamel integral. Thus the full evolution differs from its positive killed comparison by `poly(N) T exp(-cN)`, plus initial source/projection error. Polynomial N factors are absorbed by reducing the fixed exponent for sufficiently large N.

Every compressed physical/system leg and P1 preserve M0. The killed output therefore lies in the same relative-correctable Bell-target module at all times. The fixed ordinary relative recovery factors Phi_(k_N) from the ENTIRE coherent module. Positivity and the full/killed channel comparison prove (T), with reference-uniform constants and no sampled-Pauli or independent-bath assumption.

## 10. Noncircular parameter order and retained restrictions

1. Fix the code/locality instance, full payload/locks, finite message hardware, value-blind fast rates (including positive Alice LOAD), raw history/token weights and s. Construct fixed raw-tilted debt/activity and physical availability witnesses and their finite cones.
2. Choose r0 strictly within the common code radius and distance margin, giving b=h r0. Fix spectral exponent a<sb and a fixed higher-moment order m large enough for the boundary coarse-norm budget.
3. Choose t small enough for credited witness stability, local-density/condition-number budget and all fixed m boundary margins.
4. Choose lambda>0 small, then delta=C_d sqrt(lambda)t, zeta=c_z lambda t and beta_A=C_b lambda t. Enforce Young absorption, (12), g and boundary margins. All constants remain N-independent.
5. Choose eta>0 sufficiently small compared with lambda t. Choose source z0/e0 and initial moment below the fixed spectral barrier, or use the exact raw Bell source. Finally choose N above the fixed radius/distance and asymptotic error thresholds.

This order does not make an unearned service rate an assumption: real A/C and READ availability constants were constructed at the fixed native instance, and weak Bob entry is exactly linear in its complete LOAD rate. It does not require any elementary local killing to be positive. The small-density second-order budget is sufficient; exact joint debt commutants and raw-energy-commuting debt witnesses are false and unnecessary.

All physical constants can be impractically small or large. The result is not passive thermal self-correction, a practical numerical threshold, an advantage over a strong scheduled comparator, arbitrary noisy encoded preparation/readout, arbitrary initial dirty apparatus, or arbitrary logical identity. It supplies no new external control resource during autonomous storage. All previously accepted stochastic sources, corrections and failed routes remain unchanged.

## Review status and governing dependencies

A fresh independent WHOLE review of this manuscript and exact frozen dependency set is REQUIRED. The component receipts cover raw/token inequality; debt/FREE moments; raw conservative tilt; weighted debt; actual A/C service/rate; exposure extension; raw guarded composition/direct tilt; repaired full availability; generic Taylor; and the new basin mechanism only at their stated scopes. The first-order/tilted-activity receipt is SHA `771188407f6177a4edcd263b61ada28c280d5c09d99ea25303e9c7658fbaed8f`; the abstract two-basin receipt is SHA `cf09065b2d71a3afcef73d5584b9daebc4453e2813614b5cc1cf0988fe27ce13`. Their exact governing sources are included in the freeze inventory. No whole conclusion is declared accepted in this draft.

The accompanying DEPENDENCY_MANIFEST.json and DEPENDENCY_SHA256.txt include the accepted native stochastic hardware/payload sources (not its Poisson argument as a continuous proof), the actual operator directory, the fixed code/common-Bell algebra interfaces, and the root noncommuting-basin/Taylor/entropy sources. The failed private-pipe decoupling file is explicitly non-governing and preserved for audit history.

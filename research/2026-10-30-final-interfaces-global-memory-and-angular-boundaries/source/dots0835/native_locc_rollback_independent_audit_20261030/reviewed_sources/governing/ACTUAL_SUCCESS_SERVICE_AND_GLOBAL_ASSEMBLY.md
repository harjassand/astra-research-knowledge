# Actual two-SUCCESS service and native stochastic LOCC assembly
2026-10-30. New candidate. Uses the explicit new generator; no old instantaneous-watchdog or independent-word probabilities are imported.

## 1. The service record must count SUCCESS, not all retirements

Let S_h be the sum of Bob h's ACTUAL successful C_L->Q0 gains. Rollback and dirty aborts are T_h retirements, but are not useful evaluations and are not S_h. In particular frequent clean watchdog aborts make a two-retirement count insufficient.

Attach a passive local classical counter c_h in {0,1}, initially 0 at the beginning of the tested window. On the first S_h event it changes 0->1; later S_h events leave it 1. These are annotations of actual records, not a physical feedback gate. All other actual dynamics leaves c_h unchanged. Let J_h be the actual S_h gain restricted to c_h=1. Deleting J_h's gains but retaining its losses gives the genuine killed instrument for fewer than TWO successful terminal events since the window start. The c_h=1 initial case means fewer than one additional success and is also covered below.

Each record counter is finite, local and has no DATA effect. The enlarged generator has the same bounded locality/rate structure. No ideal global clock or controller resetting is added to the physical process.

## 2. Uniform full-Hilbert success effect from the actual finite path

The companion's native/FIFO service path, repeated if needed, gives a fixed T_s<infinity and p_s>0 with

    exp[T_s (L_0-J_h)]^*(I) <= (1-p_s) I                 (1)

on BOTH counter states and every physical Hilbert-space state. The path first executes an actual complete T_h to clear a malformed engine/master, clears/parks the finite competing owners using their actual monitored reset/cleanup transitions, passes a full finite FIFO purge, runs the Alice native READ macro, then the Bob native SUCCESS macro. Do this twice if the starting counter is zero. All possible read outcomes are retained, so no low-probability particular syndrome is selected.

Parking means an event with no competitor LOAD or I->Q0-watchdog emissions during the remaining finite word. Their anticommutator losses remain in the actual no-jump propagator. The finite projected-monitor step estimate charges these and EVERY background term intersecting the proof patch in B; it does not replace the generator by the externally halted generator. The initial monitor windows handle arbitrary coherent clock/tag/monitor states. Classical FSM basis-read instruments handle arbitrary finite queue encodings. The finite union of all label-conditioned paths is an actual CP record event with a uniform lower effect, exactly as in the inherited actual-reset proof.

Acquisition/load/cleanup attempts have finite rates and every chosen native Hamiltonian block is nonzero with a unitary payload. Thus the constants may be very small/large but are N-independent. This proves (1) by substitution in the inherited full-instrument finite-path estimate, not by treating native quantum gates as instantaneous classical attempts.

## 3. Local witness and many-owner miss bound

Apply the anchored finite-support polynomial construction of `transactional_regeneration_20261029/JOINT_LOCAL_LYAPUNOV_TAIL.md` to this **new** killed generator with the record counter. It yields a finite-support positive witness

    alpha_s I<=Z_h^s<=I,
    (L_0-J_h)^*Z_h^s<=-r_s Z_h^s.

The sole nonunital killed term is still local to h, so the anchored support argument is unchanged. Counter c_h participates in the local witness support. Bounded overlap gives a buffered spatial packing/color number P_s.

The actual noisy process is L_epsilon=L_0+sum_e epsilon c_e(E_e-id). All J_h remain real recorded gains. The same local CP comparison as for retirement witnesses preserves drift at sufficiently small epsilon, say r_s/2. For any owner set A, buffered packing therefore gives constants C_s,gamma_s>0 with

    || no-two-SUCCESS-on-every-h-in-A during [u,u+T] ||_diamond
        <= C_s^|A| exp[-gamma_s |A| T].                (2)

All counters are initialized to zero at u; the physical state at u is arbitrary. This is a CP event bound conditional on any prior physical record through the uniform operator inequality, not an independence statement. The same actual trajectory can be tested with fresh passive counters in different windows without altering it.

Let M_u(T) count Bob owners with fewer than two S_h events in that window. There are n_h<=c_h N owners. For any chosen m>0, use a union over sets of size ceil(mN):

    Pr(M_u(T)>=mN)
      <= 2^(c_h N) [C_s exp(-gamma_s T)]^(mN).          (3)

Choose T large enough that its exponent is negative with a fixed margin. Then (3) is Ce^(-c_m N), uniformly in u and in initial/reference states. Physical faults are retained in (2); their separate DATA/service effects remain charged in Q. There are no iid favorable-word trials.

## 4. Why two successes suffice for candidate service

Every SUCCESS is also a complete T_h. Thus the later of two successes follows a real retirement and a forced fresh purge; its mechanical source is clean unless a relevant intervening primitive fault occurred, and its semantic program is current unless a relevant primitive fault or dirty Alice retirement occurred. Those causes and any resulting charged successful emission are included in Q at their ACTUAL event times.

If an active candidate at window start is not resolved by any earlier clean move, bad DATA mask, or charged local service/semantic interruption, then its raw dependencies persist through this later terminal. The terminal is an unmarked exact ordinary GPT evaluation of its current relative syndrome and forces the reviewed integer energy decrease. Neighboring marked Bob retirement cannot stale the clean locked snapshot, by actual owned-support disjointness. A previous-window semantic mark is cleared by the first T; if the first success carries an error, that emission itself is included in this window's Q.

The factor two is conservative. An earlier abort may already have regenerated h; counting only SUCCESS avoids having to inspect that favorable history in the miss variable.

## 5. Conditional global assembly at the new honest scope

Import ONLY the reviewed deterministic Tanner density/confinement/clean-GPT/common-correctable-span facts used in `AUTONOMOUS_LOCC_GLOBAL_ENERGY_THEOREM.md`. Replace its atomic primitive implementation, primitive-only mark MGF and independent service-word concentration by the explicit native machine, `DEPTH_TWO_EMISSION_COUNT_MGF.md`, and (2)-(3).

On one physical window, Q is the sum of:

- direct dressed primitive fault charge, including controller-only service interruptions;
- every mechanically marked Alice retirement, charged for its bounded DATA/possible-reply action and the full bounded neighboring Bob semantic dependencies it can invalidate;
- every mechanically marked Bob retirement;
- mechanically clean but semantically marked Bob SUCCESS only (clean rollback is identity).

Each footprint has fixed mass. The distinct-root count lemma gives, at fixed theta,T,

    log || tilted_Q || <= epsilon C(theta) N T.

Choose a small q>0 and then epsilon so

    Pr(Q>qN)<=exp(-c_q N).

Together with (3), the same deterministic persistence argument yields

    U_(j+1) <= (1-a)U_j + A Q_j + B M_j

with newly enlarged but fixed a,A,B. The proof packs active full-dependency candidates; each charged event can resolve/spoil only a bounded number. It is not a gate-count approximation. Choose the source/window budgets so the existing first-exit margin is strict. The reviewed local Pauli-edge/canonical-representative argument then prevents both high reduced weight and logical-class change on every safe coefficient history.

At an arbitrary observation time t, use only completed service windows [jT,(j+1)T] ending by t, plus the charged mass on the FINAL PARTIAL interval [floor(t/T)T,t]. No service-miss event is required on that partial interval: clean moves decrease U and U(u)<=U(floor(t/T)T)+2Q_partial. The COUNT lemma covers its length <=T. Thus the safe/bad CP instruments are entirely measurable from records available by t; one must NOT condition the t-output on a future native quantum SUCCESS record. A union bound over these completed windows and the final partial mass gives the same C(1+t)exp(-cN) bound.

The forest frame F_A^dagger tensor F_B^dagger and the fixed ideal relative recovery extract the same known logical Bell target from every safe coefficient. Initial raw physical Bell pairs must satisfy the same common local-stochastic relative-support source condition as in the atomic theorem, and the native apparatus is initially clean with the concrete first-purge control described in the companion. Uniformity includes allowed gauge/reference/retained bath states. Positivity gives the candidate bound

    target trace error <= 2 eta_source + C(1+t)exp(-cN).

This is a NATIVE stochastic LOCC candidate in grouped-site two-site-H/onsite-reset quantum scope plus explicitly declared measured classical channels. It is not yet labeled independently accepted: the new count-MGF and two-SUCCESS witness transfer need exact-source review, along with this final assembly. It is not an arbitrary-logical identity theorem on the enlarged joint sector, bare-DATA output theorem, generic coherent-noise threshold, native preparation theorem, or efficient/practical implementation claim.

The separate accepted native continuous-noise memory theorem supplies useful owner/native proof machinery only. Its spectral coefficients, complete theorem, and continuous-noise acceptance are NOT imported into this new stochastic LOCC machine.

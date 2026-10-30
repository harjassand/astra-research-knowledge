# Local clean rollback corridor: exact instrument and reset-window audit
2026-10-30. Scoped PASS for clean rollback semantics and finite positive reset windows. NOT a full malformed-state, owner-history/no-creation, or native-controller integration theorem.

Audited candidate: `LOCAL_QUANTUM_ROLLBACK_COMPILER_CANDIDATE.md`, SHA256
`5ba3452e557ea31d1fc584b0487e8b0c0bbe6ce7d968c2084f73b2454fb39eed`.

## Result first

The proposed private inverse-prefix rail works. A workspace-blind watchdog can project the current computation position into a corresponding rollback branch without erasing a partially executed quantum workspace. The forest gauge makes both the watchdog and inverse-prefix Hamiltonian clock-only. A reset at the rail's prefix-zero endpoint then produces an exact DATA-identity abort instrument, rather than destroying an unfinished computation.

Every finite connected rollback path with nonzero hopping amplitudes and an endpoint absorber has a strictly positive integrated probability of reset during any fixed positive-length time interval. This is NOT a positive instantaneous reset hazard uniform over all clock states. Dirty ownership cases and the enlarged full-Hilbert forest still require explicit bookkeeping before any whole native compiler claim.

## 1. Clean model and immutable program

Write

    V_0=I,    V_j=U_j ... U_1.

The U_j may be controlled by a finite program register copied into the engine at entry. Treat that register as part of the payload. Its value must be NOMINALLY IMMUTABLE until retirement, and every program value must use the same fixed padded gate list and hopping amplitudes. Workspace may interact coherently with DATA; no intermediate syndrome measurement is required.

The clean engine enters at C_0 with the stated initialized workspace and an arbitrary DATA/reference/program state. Program may be classically correlated with DATA/reference. All required resource tags are owned by this engine and remain held throughout computation and rollback. In this clean history range, its physical computation state is obtained from a clock/payload product by

    F_C=sum_j |C_j><C_j| tensor V_j.

The factorization is important. Merely finding a corrupted state at some C_j with apparently correct tags does not make it a clean prefix state.

For every possible watchdog entry j0, allocate a private finite rail

    B_(j0,j0), B_(j0,j0-1), ..., B_(j0,0).

There are O(L²) rail states for a length-L payload, still finite at fixed local code degree. Outer control enters DRAIN on watchdog entry and must not launch a replacement job, alter the engine program, erase its workspace, or release its claims before actual retirement.

## 2. Workspace-blind watchdog

Use separately resolved onsite Kraus operators

    J_j=sqrt(mu) |B_(j,j)><C_j| tensor I_payload.       (1)

The indicated classical master/DRAIN update can be included in the same hub-local operation. Sum over j, but do not coherently sum distinct j Kraus operators when the intended instrument resolves/projects clock position. The total loss on the computation subspace is

    sum_j J_j†J_j=mu Pi_C tensor I_payload.

Thus its watchdog hazard is workspace/program blind. It preserves the actual prefix rather than resetting that prefix away.

Define on each rollback rail

    F_B=sum_(j0,ell) |B_(j0,ell)><B_(j0,ell)| tensor V_ell.

Then

    F_B† J_j F_C
       =sqrt(mu) |B_(j,j)><C_j| tensor I.              (2)

The watchdog is exactly clock-only in the clean forest frame. Any record dependence is in its scalar clock coefficients, not an uncharged DATA operation.

## 3. Inverse-prefix Hamiltonian

For 1<=ell<=j0, add the rail edge

    g_(j0,ell) |B_(j0,ell-1)><B_(j0,ell)| tensor U_ell†
       + its Hermitian conjugate,                    (3)

with each g nonzero and finite. Use the same actual resource-ownership guards as the corresponding data gate. In the clean all-owned range those guards are one. Because V_ell=U_ell V_(ell-1),

    V_(ell-1)† U_ell† V_ell=I.

Consequently F_B† H_B F_B is the ordinary scalar hopping path tensor payload identity. Coherent backward and forward motion on the rail is harmless: at every position ell the physical payload is the corresponding V_ell prefix. Reaching ell=0 returns it exactly to its engine-entry value.

A local two-site gate U_ell becomes its local two-site inverse; workspace-only gates remain onsite. All rollback clocks/program/workspace can remain in the same finite hub qudit. Nothing in (1)-(3) requires a quantum bus between Alice and Bob.

Allowed additional clean monitors must remain clock-only under this same gauge. Position-diagonal dephasing is harmless. A workspace-blind reset from ell to a DIFFERENT prefix level is NOT automatically harmless: it changes V_ell without undoing DATA gates. Such transitions must be absent, preserve the prefix level, or carry their required payload unitary. In particular a repeated outer watchdog must not directly reset a B_ell workspace or program.

## 4. Endpoint reset and exact abort instrument

Only at ell=0 perform the complete endpoint reset. For workspace basis states s use separate equal-rate Kraus channels

    L_(j0,s)=sqrt(kappa) |retired,0><B_(j0,0),s|.       (4)

If the program is retained until a subsequent retirement acknowledgment, include identity on it. If it is erased here, include its basis in s and sum those erasure outcomes. The total endpoint loss is kappa |B_(j0,0)><B_(j0,0)| tensor I_workspace, so the clock loss is payload independent.

Since F_B=I at ell=0, summing all reset-workspace outcomes applies only the prescribed trace/reset of internal workspace/program. The DATA/reference marginal is unchanged. For a clean entry with a payload-independent initial clock state, the first-abort-retirement DATA instrument therefore has the form

    dI_abort(t)=f_abort(t) dt id_DATA,                  (5)

with f_abort nonnegative and independent of the DATA input. A specified workspace-blind clock-monitor record may change the scalar density but not the DATA identity. This includes arbitrary DATA/reference entanglement.

Two qualifications are essential:

1. Equation (5) is a CLEAN-entry instrument statement. If clock and DATA are arbitrarily correlated in the forest gauge, conditioning on a clock reset can steer DATA. The uniform reset PROBABILITY bound below survives on that larger rail-supported domain, but scalar-times-identity need not.
2. A coherently summed workspace eraser is not (4). Also, conditioning on an individual reset value of a program correlated with DATA can steer DATA. The identity statement sums the appropriate reset outcomes, or keeps the program until its separately specified retirement. It does not assert scalar identity for every fine workspace/program label.

All ownership claims remain held through (4). Only after actual complete reset may Q/cleanup phases release tags. Thus another owner cannot interact with DATA while the inverse circuit still uses it.

## 5. Positive reset-window effect: direct proof

Fix one rail of length j0+1 and work in its scalar-clock gauge. Let H be its Hermitian tridiagonal hopping matrix, with nonzero neighboring couplings, and P0=|0><0|. Before the first endpoint reset, the no-reset propagator is

    K=-i H-(kappa/2) P0.

The effect of a reset by time T is

    G_T=kappa integral_0^T exp(K†t) P0 exp(Kt)dt
       =I-exp(K†T)exp(KT).                            (6)

For every T>0, G_T is positive DEFINITE. Indeed, if <v|G_T|v>=0, then <0|exp(Kt)|v>=0 for every t in an interval. Analyticity gives <0|K^m|v>=0 for every m. On a path with nonzero neighboring couplings, these equations successively force v_0=0, v_1=0, ..., v_j0=0. Thus v=0.

Put p(T)=lambda_min(G_T)>0. Then for any positive joint clock/payload/reference state supported on this clean rail,

    Pr(reset within T)>=p(T),
    ||no-reset instrument over T||_(1->1,positive)
       <=1-p(T).

Tensoring (6) with payload identity makes the bound reference-uniform. Iteration gives an exponential survival tail and finite mean reset time, bounded for example by T/p(T). There are finitely many rails, so the minimum of their p(T) is positive. The j0=0 rail is the immediate single-site absorber case.

The same argument applies to any positive-width later reset interval [a,a+T], since its Gramian is exp(K†a)G_T exp(Ka), still positive definite. A rank-one instantaneous effect at a fixed time need NOT be bounded below by p I; dark instantaneous clock states exist. The certified statement is integrated-window positivity, not a state-uniform pointwise density.

If other finite clock-only losses/monitors are retained, their exact generator must be specified. One may bound a suitable no-other-jump subinstrument; for the usual finite position-diagonal losses the killed matrix remains a connected tridiagonal path and the same observability argument supplies a positive reset-window effect. An arbitrary unspecified additional transition is not covered automatically.

From a clean computation phase, a watchdog has positive rate on the whole C subspace. A positive finite interval in which it fires before competing terminal retirement, followed by the rail reset event, has positive probability. Counting either successful terminal retirement or abort retirement only improves the total retirement bound. There is no claim of a simple exponential waiting law for the quantum walk itself.

## 6. What must be added before native/full-Hilbert promotion

The construction resolves clean watchdog rollback, not the entire dirty-controller proof. Required explicit work includes:

- Add EVERY B_(j0,ell) to the phase/claim table: computation-origin rollback retains the same full owner claim set as C.
- For every new rail state and every possible ownership mismatch, provide a route into the inherited DIRTY consistency-abort/reset mechanism. A two-site guard can disable a rail hop; without an added dirty exit this can create a stuck component.
- Keep all owned claims until complete dirty or clean workspace reset. No reset-free edge from B or a computation-origin dirty leaf to acquisition/free cleanup is permitted.
- Ensure dirty consistency leaves cannot coherently return to a computation/rollback state after some resource has been released. The existing reset-before-release obstruction applies unchanged.
- Define the full-Hilbert forest factors on all new B/dirty labels and malformed tag sectors, not just the all-owned clean range. Recheck commutation/overlap, incident patch bounds and data-independent good-range projectors.
- Recheck owner-history/no-creation inclusions for the new onsite watchdog, inverse Hamiltonian edges, DRAIN transitions, complete resets and cleanup. Copying a clean prefix formula does not certify these inclusions.
- Specify program copy, immutable lifetime, DRAIN/retirement acknowledgment and cache-reset gates. An outer timeout cannot erase/reprogram a live engine while its old prefix is still present.
- Re-establish the ACTUAL reset-tail and marked-emission moment for dirty paths, including changed constants and extra local phases. A clean finite-path Gramian does not prove a full malformed-state no-regeneration tail.

A fault changing ownership, program, clock or workspace can make an abort dirty. Such behavior is to be charged by a subsequently audited bounded-support forest/marked contract, not called clean identity. The candidate adds no new crossparty quantum coherence, but it also does not automatically integrate the classical FIFO machine with the native quantum engine.

## 7. Candidate-specific forest and regression receipt

The candidate’s malformed-mask assignment V_ell(m,a) has the stated LOCAL algebraic consistency, assuming the inherited forward-path convention: deleting ownership-disabled edges splits the path into components framed at their least index. Truncating a rollback rail above j0 does not change the least index of any component it retains. Therefore the same V_ell(m,a) flattens each present inverse edge, gives equal source/target frames on C_j->B_(j,j), and gives F=I at ell=0. This pointwise calculation does not independently prove the global commuting-forest/no-creation or dirty-retirement claims listed above.

The explicit Alice terminal pointer in the candidate is also a genuine measured output when ALL workspace basis channels are separately resolved, equally rated, and their DATA(y(s)) destinations are orthogonal classical records. It is not access to an unmodeled environment readout. Its preservation through cleanup and response-before-next-request discipline still belong to the combined FSM proof.

`check_local_rollback.py` tests five clean prefix/rail positions using generic program-controlled unitary payloads. It verifies scalar Hamiltonian gauging, watchdog frame intertwining, the first-reset DATA superoperator after SUMMING workspace/program reset labels, and strictly positive endpoint-absorption Gramian eigenvalues at fixed windows. Results are in `check_local_rollback.json`. This is not a malformed-state or full native-compiler regression.

## Conclusion

Clean rollback is sound and directly addresses the watchdog/prefix-erasure obstruction. The precise proved outputs are (2)-(5) and the finite positive reset-window bound (6). The next action is the explicit new-state consistency/tag/forest audit; neither full native LOCC compilation nor malformed-state liveness is certified by this receipt.

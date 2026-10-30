# Fast actual exposure of the Bob LOAD guard while the engine is FREE
2026-10-30. New availability lemma. Alice LOAD remains fixed positive; Bob LOAD is zero in the reference. This does not multiply a witness into DATA energy or finish useful service.

## Result

For Bob h let F_h be the accepted FREE projector and

    P_h=F_h 1_(phase I) 1_(master WANT(any value)).

At zero Bob LOAD, there is a bounded-support positive Hermitian R_h with fixed bounds aI<=R_h<=CI, commuting F_h and P_h, such that

    F_h L_fast^*(R_h) F_h <= -c F_h+C P_h.              (1)

The constants are uniform in N and independent of the removed Bob LOAD rate. Alice native READ/LOAD, transport, retirement and cleanup keep their fixed positive rates. Equation (1) is an actual fast LOAD-guard occupation/availability witness on the FREE restriction, not an assumed reliable cache or a uniform useful DATA decrement.

## 1. Exact guard-block algebra on FREE

At zero Bob LOAD, F_h is invariant under every nominal gain and Hamiltonian. Within F_h, P_h depends only on the private I clock label and the master WANT type; it does not test W/P or the value a. The actual terms preserve the algebra of operators block diagonal in P_h on this invariant range:

- Hamiltonians and actual finite reset monitors commute P_h. No Hamiltonian connects I to another phase when h has no own tags. Q verification acts entirely within the P_h=0 range.
- I watchdog source labels include the erased old master/cache value. A channel from I+WANT is entirely in the P_h=1 source block, and every other I source is entirely in its zero block. Q watchdogs are entirely in the zero block.
- READY has Q_k source, entirely in the zero block. Workspace refresh commutes the I/WANT predicate.
- A response creating WANT has READ_WAIT source, entirely in the zero block. Unconditional discard in WANT leaves WANT and the engine phase unchanged. All other request/master transitions either have a single zero source block or commute P_h. The ONLY nontrivial outgoing LOAD is removed in this reference.
- Other owners/Alice/message hops leave h's private clock/master alone. On F_h their tag action preserves absence of h's own labels, hence commutes its guard.

For a Kraus operator supported in one source block, J^*OJ remains in that block for EVERY O. For one commuting P_h, it preserves the P_h commutant. This proves the listed adjoint algebra statement. It is specific to this syntactic guard on FREE, not the false assertion that arbitrary semantic Q-block-diagonal or controller-type observables form an invariant global algebra.

## 2. Uniform actual arrival and an analytic observation

From any state supported on F_h, take an actual h I/Q retirement to reset the master to FLUSH_SEND(0), then READY to I. The h tags remain absent. Process the finite old request/reply backlog with the actual Alice quantum READ macros; Alice LOAD is fixed positive, so every old REQUEST can actually finish. Complete the G+1-SYNC purge, send a new READ, complete Alice's native read and measured response, and receive WANT at Bob I. Select no further h watchdog during the fixed final subword, retaining its losses. No Bob LOAD is needed anywhere.

All malformed Alice engines are handled by the accepted actual retirement/read path. The finite current alphabet/capacity and normalized complete monitor/path proof give a fixed positive lower probability of reaching P_h within a fixed time, uniformly over exterior/reference states. This availability argument can damage DATA if Alice was initially dirty; it makes no contrary initialization claim.

For analysis ONLY, add a unit-rate absorbing observation at P_h. Its loss is {P_h,O}/2, and its gain goes to an unused cemetery record. Append one positive-length observation box to the actual word, with all other losses retained. The resulting no-observation CP instrument contracts uniformly. This analytical observation is not a proposed native multi-resource reset or an externally supplied feedback operation.

## 3. A local reducing extension, to avoid a hidden support error

F_h is invariant but can have inflow from ACTIVE. It would be WRONG to extend a FREE-only resolvent by zero and assume its full adjoint has the same corner. Instead build a local analytical reducing extension L_red as follows. For each actual nominal Kraus leg J touching F_h, replace it by its two diagonal blocks

    J_diag=F_h J F_h+(I-F_h)J(I-F_h)

and use the corresponding complete GKLS loss sum J_diag^*J_diag. Hamiltonians already commute F_h. On its FREE block this generator is EXACTLY the original zero-LOAD evolution, since J F_h already lies in F_h. It has no inflow/outflow between the two blocks. Terms disjoint from F_h are unchanged, so only a bounded neighborhood is modified and locality/incidence remain fixed. It is an analytic CP/unital extension, not a physical protocol change.

Extend the observation intensity to

    C_obs=P_h+(I-F_h).

The outside block is then killed at unit rate. By section 1 the full reducing extension preserves the F_h/P_h commutant, and the killed generator

    K^*=L_red^*-{C_obs,.}/2

does too. Its full-Hilbert survival has a uniform finite contraction: on FREE use the actual word in section 2; outside use the unit-rate loss. Therefore

    R=infinity-integral_0 exp(tK^*) I dt

is a bounded positive operator, with aI<=R<=CI and [R,F_h]=[R,P_h]=0. It obeys

    K^*R=-I,
    L_red^*R=-I+C_obs R<=-I+C C_obs.                    (2)

No claim of finite support has yet been made at this stage.

## 4. Strictly local approximation with the correct derivative

Use the accepted finite-support telescoping-polynomial construction for the uniformly killed local generator K, starting from I. The exact telescoping identity controls K^*R_loc+I without an extensive generator norm. Choose the approximation tight enough that R_loc remains between fixed positive bounds and

    K^*R_loc<=-(3/4)I.

Every polynomial iterate stays in the actual F_h/P_h commutant, so R_loc commutes C_obs. Thus

    L_red^*R_loc<=-(3/4)I+C' C_obs.

Compress to F_h. Since the reducing extension equals the actual fast evolution on states in F_h,

    F_h L_fast^*R_loc F_h
      =F_h L_red^*R_loc F_h
      <=-(3/4)F_h+C'P_h.

This is (1). All supports/constants are fixed. No lambda-dependent approximation accuracy was required.

## 5. Important remaining DATA issue

R_loc is NOT claimed globally controller-only or raw-energy commuting. Dirty partial resets can turn tag coherences into DATA dependence, as demonstrated in FAILED_GLOBAL_CONTROLLER_TYPE_ALGEBRA.md. This proof avoided that false shortcut. To use (1) as a positive exposure correction multiplying a useful DATA decrement, one must earn a buffered-clean controller/syndrome restriction and a local dirty/active extension, or another explicitly positive weighted construction.

In particular, (1) and the clean committed credit cannot simply be multiplied together to assert a logical-memory theorem. Nor does (1) remain uniform when Alice LOAD goes to zero: an old REQUEST can then block the full-purge word. No CANCEL message or altered physical FSM has been introduced here.

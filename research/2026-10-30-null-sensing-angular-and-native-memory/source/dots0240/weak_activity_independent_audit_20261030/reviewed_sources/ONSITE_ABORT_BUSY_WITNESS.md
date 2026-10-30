# Earned full-Hilbert BUSY witness for the weak-first-edge / fast-abort variant
2026-10-30. This chooses a DIFFERENT explicit repair from the conflict leaves in `FAST_ACTIVITY_REPAIR.md`. Do not silently merge their generators.

## 1. Exact physical variant
Start with the reset-first transactional generator in `producer-workspace/RESULT.md` and its full-Hilbert forest frame. Retain its complete, separately workspace-label-resolved resets and finite-rate clock/lock monitors. Use the full raw-syndrome read plus correction footprint as R_h.

* Give only the first acquisition A0,f <-> A1,o_h amplitude epsilon.
* Keep every later acquisition, computation, cleanup and verification edge at fixed positive fast amplitude.
* Add, for EVERY acquisition phase A_i with i>=1 and workspace basis s, an actual on-site complete abort channel

    J_(h,i,s)=sqrt(mu_i) |Q0,0><A_i,s|,

  with mu_i>=mu_min>0 fixed. Include s=0 and keep the channels separate.
* All other original abort rules and the prohibition on coherent cleanup in R remain unchanged. The new resets are DATA-identity in the exact forest frame because all A/Q gauges are identity.

No first-edge reversal is used by the fast proof. No multi-resource projector or effective high-body reset is added. Later rates are not taken small: this is distinct from the main constructor's optional slow acquisition/cleanup hierarchy.

## 2. Full BUSY projections and operator blocks
Let Ready_h mean A0, workspace zero, and no own o_h/z_h tag on any R_h resource; monitor ancillas are unrestricted. Let P_h=I-Ready_h. The P_h are finite-support commuting projections. All assertions here concern these BUSY flags, not merely the earlier history-bad flags.

At epsilon=0 every Hamiltonian commutes every P_h:

* all C, Q, R and A_i>=1 phases are busy regardless of workspace;
* any A0 abort or cleanup source has an unexpected own tag, so it is already busy;
* good A0 has no fast exit;
* changing h's own label does not change any other owner's ready predicate, which tests only that other owner's labels.

Every actual complete reset is noncreating. Terminal/abort jumps originate in a phase busy regardless of workspace, and land in Q0, still busy. Their possibly nontrivial DATA instrument therefore cannot spoil BUSY mask preservation. Ready Q_k->A0 resets originate in a fixed busy source; their output may be ready or busy depending on remaining own tags, but never creates a busy flag from a ready source. Workspace refresh at A0 has separately resolved workspace inputs: a dirty source is busy, while the clean source keeps its existing own-tag predicate. Lock cleanup has a busy source whenever it can alter the owner's flag. Other flags are unchanged.

More than no-creation is used: the actual source/output structure makes the ADJOINT of every resolved reset preserve the algebra block diagonal in the joint P_h masks. A reset may map a busy input coherently to ready/busy output components; this does not create an adjoint cross block because its source is already in one busy corner. Summed complete losses and the monitor terms preserve the same algebra. Thus L0* preserves that block-diagonal algebra, not just the expectations of the flags.

## 3. Uniform local fast-return path
For a specified h, use only h and its resource sites as the monitored proof patch. Outside/boundary terms are retained in the fixed norm budget.

* A_i>=1: take the newly added complete acquisition abort immediately.
* R: take its complete abort reset.
* Inconsistent C or A0 or Q: take one existing failed-test abort and reset.
* Consistent C: follow the finite forward unitary circuit and take terminal reset. This works on arbitrary workspace/DATA/reference states; every selected gate is unitary on its eligible source block.
* In Q, remove every own o_h/z_h tag by cleanup drive/reset, then advance verification and take the complete ready reset.
* A0 with only dirty workspace: complete refresh makes it ready.

No neighboring owner is cleared and no weak or later acquisition edge is required. A conservative common selected-step bound is m=L_max+3k_max+4. The new abort rates, selected coherent amplitudes, and complete reset rates all have positive lower bounds independent of epsilon.

## 4. Actual finite-rate quantum bound
Apply the same resolved finite-rate monitor/projected-path instrument argument as `transactional_regeneration_20261029/ACTUAL_RESET_INSTRUMENT_TAIL.md`, now with this shorter path, patch {h}+R_h, and all selected amplitudes bounded below by a FAST constant. Keep arbitrary outside/reference entanglement, the full no-jump losses, all boundary-crossing terms, and the existing actual reset monitors.

The selected record ends in a true complete ready/refresh reset with all own tags absent. It therefore lands in Ready_h without measuring workspace or an abstract BUSY flag. Earlier arrival is already success, and Ready_h is absorbing under L0. The monitor flush and finite measurement windows have fixed positive probabilities and fixed error budgets, since no selected step has amplitude epsilon.

Consequently there are explicit fixed T<infinity,p>0, depending only on the finite patch parameters, such that

    exp(T L0*) P_h <= (1-p)P_h.                         (1)

This is an all-state operator inequality. It is not a stochastic assumption about initially classical clock labels. The constants can be instantiated directly from the cited path certificate with the new m, local B and fast g_min; all are volume independent. The exhaustive basis-transition audit supports the exact path eligibility but does not replace this quantum-instrument argument.

## 5. Finite-support commuting witnesses
Since P_h is noncreating, L0*P_h=-A_exit,h with 0<=A_exit,h<=nu P_h for a fixed local nu. Let

    G_h=int_0^T exp(t L0*) P_h dt,
    a=(1-exp(-nu T))/nu.

Then aP_h<=G_h<=T P_h and L0*G_h<=-p P_h. Every exact iterate of P_h remains in its P_h corner and commutes EVERY P_j, by the operator block statement in Section 2.

Use the anchored local-polynomial telescoping construction from `transactional_regeneration_20261029/JOINT_LOCAL_LYAPUNOV_TAIL.md`, with initial observable P_h. Its locality expansion starts on support(P_h), not on I. Each polynomial iterate remains in the same corner and joint block algebra. Therefore all approximation errors are bounded relative to P_h. Choose them below min(a/4,p/4) with the telescoping derivative identity, not by applying the extensive generator to a norm error.

The resulting Hermitian finite-support F_h satisfies

    (a/2)P_h<=F_h<=2T P_h,
    L0*F_h<=-(p/2)P_h,
    [F_h,P_j]=0 for every j.

Set X_h=2F_h/p. This EARNS the exact input of the collision hierarchy:

    cP_h<=X_h<=CP_h,  L0*X_h<=-P_h,  [X_h,P_j]=0.

Support radius and incidence are fixed, possibly enormous, but independent of volume/runtime. This proof is full-Hilbert; X_h need not be controller-only on malformed sectors. On the clean forest range the terminal source is the fixed complete-own-mask and W=0, and the resolved Phi_h terminal instrument factors from the controller, so controller-only closure is valid there. Full-Hilbert DATA-weighted multiplication remains separate.

## 6. Regression scope
`check_fast_busy_repair.py` extends the transactional source fixture with explicit clean/dirty workspace basis bits, deletes the weak edge in both directions, and adds the new on-site acquisition aborts. It checks every fast transition for Hamiltonian BUSY equality / reset noncreation and constructs an actual eligible clearing path for every owner in every configuration. See `fast_busy_repair_checks.json`. No numerical spectral fit or reduced classical schedule is used as the probability proof.

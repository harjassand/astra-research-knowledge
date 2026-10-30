# Unified native generator interface — fresh dirty resolvent with real acquisition aborts
2026-10-30. Exact compatibility note for the whole-manuscript author. No whole-memory theorem is asserted here.

## 1. One physical generator, with explicit amendments
Start with `producer-workspace/REPAIRED_GENERATOR.md`, then apply the reset-first changes of `producer-workspace/RESULT.md` and its `FULL_HILBERT_FOREST_GAUGE.md`:

* acquisition and committed C phases are distinct;
* commitment A_k,s->C0,0 is a complete, separately workspace-resolved ONE-WAY on-site reset;
* every C gate checks actual ownership on its target;
* terminal and abort are complete on-site workspace/clock resets to Q0,0;
* coherent own-lock cleanup remains disabled in every R abort phase;
* the actual finite-rate label-resolved hub/resource monitors of `ordered_lease_schedule_20261029/EXACT_RESET_MONITOR.md` remain present.

The intended payload is the accepted full-idempotent local orbit-minimizing Tanner/SSF CPTP map, synthesized on the FULL raw-syndrome read and correction footprint. For CSS, use the already specified sectorwise X and Z potentials and shared actual history flags; this note introduces no joint-confinement hypothesis.

Adopt the following additional physical terms/rates:

1. First acquisition/reversal A0,f<->A1,o_h has amplitude epsilon times its fixed nonzero edge coefficient.
2. Every later acquisition/reversal has amplitude zeta times its fixed positive coefficient. Zeta is fixed positive BEFORE epsilon is chosen, with epsilon<=zeta and ultimately epsilon much smaller.
3. Own o_h<->z_h cleanup and z_h->free resets have fixed positive FAST rates, not zeta-scaled rates.
4. For EVERY A_i with 1<=i<=k, including A_k, and EVERY workspace basis label s, add the actual on-site reset

       J_(h,i,s)=sqrt(mu_h,i)|Q0,0><A_i,s|,
       mu_h,i>=mu_min>0 fixed.

   Keep these channels separate and include s=0. No A0 abort of this new type is added. Since the A/Q forest gauges are identity, these new physical resets are exactly DATA identity in that frame.

All other abort drives, C gates, verification, commitment, terminal, ready, workspace refresh and monitor parameters are fixed positive finite constants. These are the conventions confirmed by the native manuscript author.

## 2. Actual monitor accounting, including the free piece
For a resource r the physical monitor is unchanged:

    H_mon=Omega I_lock tensor X,
    M_c=sqrt(kappa_m)P_c tensor |0><1|,

with DISTINCT actual label channels. Algebraically split its Hamiltonian into each owner's o/z block and its free block. Assign the g-owned Hamiltonian block and M_o_g,M_z_g to g. Assign the free Hamiltonian block and M_free ONCE to the lowest-index incident owner h(r). This static proof bookkeeping does not require a physical global-index operation or change the monitor.

Include that assigned free term and its support in L_h(r) and in every cavity/noncommutation support list. It annihilates every dirty owner's monitored owner algebra, but it may act on an activity-weighted observable and must not be omitted there. No physical monitor term is duplicated.

For a FIXED clean commutator [L,Q_h], by contrast, its isolated core contains ALL physical resource-monitor pieces on R_h. This is the per-commutator grouping in `NORMAL_FORM_MONITOR_ACCOUNTING.md`, not a second global owner decomposition. A clean isolated free-resource monitor is not generally a spectator.

## 3. Rebuild the DIRTY killed matrix from the amended apparatus
Let B_h denote the actual history-bad projection (not the larger BUSY projection). Form L_D,h^0 from the amended actual owner generator by omitting ALL h acquisition/reversal edges, including both the first epsilon edge and every later zeta edge. Retain fast cleanup, the owned resource-monitor pieces, its canonically assigned free pieces, actual hub monitor, all new mu resets, and every other fixed fast own term.

Restrict to the B_h corner and delete every gain landing in B_h=0, retaining all complete losses. This is the CP killed generator K_D,h,new. It is built from the new channel list; it is NOT the old generator evaluated on an old coefficient.

For an exact update formula, let K_D,h,old be the FAST-CLEANUP owner-block killed matrix immediately before adding the mu resets (not the historical slow-cleanup matrix). Since Q0,W0 is universally good,

    B_h J_(h,i,s)=0,
    sum_(i,s) J_(h,i,s)^dagger J_(h,i,s)
       =sum_(i=1)^k mu_h,i P_Ai tensor I_W.

Thus on bad-corner observables O,

    K_D,h,new*(O)=K_D,h,old*(O)-1/2 {M_h,O},           (3.1)
    M_h=B_h[sum_(i=1)^k mu_h,i P_Ai tensor I_W]B_h.

M_h is positive, commutes B_h and belongs to the private h algebra. Formula (3.1) is an exact substitution/assembly rule. It DOES NOT imply that the old Lyapunov S still works, or even justify an unqualified Loewner ordering of the old/new mean lifetimes: noncommuting added killing can change coherent transport. Recompute the resolvent and all normalization constants.

## 4. Monitored owner algebra is still closed
For each r in R_h use the already audited algebra

    A_(h,r)=B(span{o_h,z_h} tensor H_monitor)
             direct-sum C(I_other tensor I_monitor),

tensored with h's full private clock/workspace/hub-monitor algebra. B_h belongs to it. New M_h and all new reset losses are private h operators, so they preserve this algebra. Their bad-to-bad gains vanish exactly.

The retained fast cleanup and owned monitor pieces preserve the same algebra as in `FAST_CLEANUP_DIRTY_CREDIT_ADDENDUM.md`. Every other-owner/free monitor piece annihilates its elements; hence adding the full actual resource monitor for the absorption argument changes neither the restricted adjoint nor its resolvent. The canonically assigned free piece also has zero action on these coefficients, regardless of which owner received it in the global bookkeeping.

Exterior owner g preserves h's o_h/z_h predicates separately and acts in the h-algebra's scalar other block. The NEW g acquisition abort changes only g's private clock/workspace and touches neither h's private variables nor those predicates. Consequently exterior Hamiltonians/Kraus channels still commute the h coefficient algebra. Different h/g algebras remain commuting because their nontrivial resource-monitor blocks are orthogonal. Private analytic erasures change no lock or resource monitor. The freshly constructed dirty CP credits therefore commute with each other and with every exterior nominal term, including the new aborts.

No full BUSY-until-ready controller autonomy is inferred here: this DATA-free closure works because every terminal/abort DATA gain is DELETED in the dirty killed compression.

## 5. Uniform absorption is reproved for the NEW matrix
For arbitrary bad h input, including arbitrary coherent workspace, lock and monitor state:

* A_i>=1: the NEW complete acquisition abort immediately heals B_h, irrespective of structural inconsistency or workspace.
* A0 or Q with structural inconsistency: take an existing failed-test abort drive and complete abort reset.
* Consistent A0/Q with dirty workspace: use complete workspace refresh.
* Consistent C with dirty workspace: follow the finite forward unitary C path and take the terminal reset; inconsistent C instead uses a failed-test abort.
* Every R phase: take its complete abort reset.

All chosen edges/resets have fixed positive rates independent of epsilon and zeta. Retained fast cleanup may compete, but its fixed norm is included in the no-jump/path budget; if a competing event already heals B_h it counts as success. The actual resolved-monitor finite-path instrument proof applies with the NEW complete rate budget. It gives fixed T_D,p_D>0 for

    exp(T_D K_D,h,new*) I_bad <=(1-p_D)I_bad.

The argument uses the full actual resource monitors before removing their algebraically null other/free pieces. It neither conditions on an abstract B measurement nor assumes initially classical clocks.

Thus the fresh finite-dimensional integral

    R_D,h=new integral_0^infinity exp(t K_D,h,new*)I_bad dt

is positive definite and finite, and K_D,h,new*R_D,h=-I_bad. A uniform upper bound is T_D/p_D; a positive lower bound follows from the fixed total healing-intensity upper bound. The resolvent remains in the monitored owner algebra by closure.

Choose common R_D,max strictly above all these NEW norms and beta_D>0 so s_D=1-beta_D R_D,max>1/2. Set

    S_D,h=s_D I_bad+beta_D R_D,h,
    0<s_min I<=S_D,h<s_max I<I.

The new actual healing intensity is

    A_heal,new=A_heal,old+M_h,

and the exact identity is

    K_D,h,new*S_D,h=-beta_D I_bad-s_D A_heal,new.       (5.1)

These constants are fixed before any acquisition amplitude is chosen.

## 6. Fresh raw weighted credit, including the new DATA-free gains
Use the same private analytic erasure Psi_h to Q0,W0 and the correct-order Kraus credit built from S_D,h. This is a proof map, not an additional physical generator. If V=V0+B_h Delta_h with Delta_h>=0, then

    T_D,h(V)=V0+B_h S_D,h Delta_h.

V0 and Delta_h commute the fresh coefficient by the owner-algebra structure. The accepted token-surplus spectral envelope applies to the actual bad terminal/old abort DATA instruments with the same full affected-syndrome bound k. The new A_i aborts affect NO DATA, lock or other flag; their V0 change is exactly zero. They enlarge A_heal but do not enlarge A_payload or k.

Consequently the actual fast own drift on the bad source obeys

    L_D,h^{0*} T_D,h(V)
       <=-beta_D B_h Delta_h
          -(s_D-q_R) A_heal,new Delta_h,              (6.1)

for the same choice of token surplus with q_R<s_D (e.g. preserve the declared q_R<1/8 margin). This is recomputed from (5.1), not from monotonicity of an old S under added reset channels.

The new abort contributes no good/dirty cross block: its complete bundled intensity commutes B_h, its output is always Q0,W0, and its DATA/other-flag action is identity. The V0 gain cancels its V0 loss exactly; its remaining S-dependent contribution is supported on B_h. Old terminal cross-block cancellation still uses the accepted deterministic raw-syndrome clean Stinespring image. The fresh S does not alter that target image. Good sources retain the actual intended recovery decrement; every new good acquisition abort is DATA identity.

## 7. Restore actual acquisition at the declared rate order
Let H_acq,h contain the omitted first and later actual acquisition/reversal terms. They preserve B_h and every other history flag, and act identically on DATA. Hence they annihilate V0 and Delta_h, and

    i[H_acq,h,T_D,h(V)]
         =i[H_acq,h,B_h S_D,h] Delta_h.

The bracket is Hermitian, supported in B_h, and bounded above by 2||H_acq,h|| B_h. With fixed edge coefficients there is a uniform C_acq such that this cost is at most

    C_acq(epsilon+zeta) B_h Delta_h.

Choose zeta>0 AFTER the fresh beta_D, sufficiently small that C_acq(2 zeta)<=beta_D/2, then require 0<epsilon<=zeta. The actual native own drift has uniform raw dirty service at least -(beta_D/2)B_h Delta_h, independent of the subsequently chosen epsilon. No cleanup term is treated as small.

The private-erasure target compression at Q0,W0 of L_h*T_D,h(V) remains zero: the new physical aborts have sources only A_i>=1. Therefore the triangular positive-congruence inverse argument of `DIRTY_CREDIT_RAW_SIMILARITY.md` applies with the FRESH S_D,h and gamma=beta_D/2. It yields an exact bounded-support HP/unital normalized generator Lhat=T_D^{-1}L_native*T_D with raw uniform dirty charge and unchanged all-good restriction.

## 8. The clean BUSY and useful-resolvent proofs use THIS SAME apparatus
There are THREE different killed/fast objects; do not identify them.

* **Dirty matrix K_D:** omits ALL acquisition; deletes every bad-to-good gain, including the NEW mu gains; keeps fast cleanup. It earns beta_D before zeta/epsilon are chosen.
* **Global BUSY fast generator L0:** sets only the FIRST initiation epsilon to zero; keeps later acquisition at the chosen positive zeta, all new mu resets, fast cleanup and the FULL actual monitor generator. Its reviewed ready-return path uses no acquisition edge at all, so the new aborts/cleanup give fixed service even as epsilon vanishes. The polynomial X_h is built from this actual L0.
* **Clean isolated useful matrix K_I,h(epsilon):** freezes all overlap neighbors ready and kills ONLY successful Phi_h terminal gains. It RETAINS new mu abort gains and cleanup returns, keeps the first epsilon edge and later zeta edges, and includes ALL actual monitors on h and R_h, even when a free monitor piece was assigned to another owner globally. The clean per-commutator regrouping justifies this exactly.

For K_I the phase graph still has separate I/A/C/Q families connected between families only by one-way commitment/abort/terminal/ready resets. The new aborts make whole excursions p Phi_h+(1-p)Id, not an idempotent map; the successful terminal Phi_h remains idempotent and is the one used in the useful resolvent. Every later acquisition amplitude is fixed positive at zeta, so the actual one-weak-hop success probability is c(zeta)epsilon^2 with c(zeta)>0. The general isolated proof gives beta_I,h=b_h(zeta)epsilon^2 and the required O(1) spectral excess. These constants may be extremely poor as zeta shrinks; no uniform limit zeta->0 is claimed or needed.

Thus the clean normal-form rate order is consistent: fix fast rates and mu; rebuild dirty R_D and choose zeta small; at that FIXED zeta derive the clean isolated/BUSY constants; choose the proof constants b,c,d and then epsilon sufficiently small. Finally t=c epsilon^2 and delta=d epsilon^2 with c<<d<<sqrt(c b) are proof parameters, not extra physical interactions.

## 9. Checks and exact scope
`unified_interface/check_new_abort_resolvent.py` reconstructs a diagnostic killed bad matrix and S independently for mu=0,.2,1,3. All resolvent equations and raw/slow drift checks pass (maximum equation residual below 1.2e-15). This is a 36-dimensional controller fixture without the full fast-cleanup/monitor apparatus; it supports the substitution, not the native theorem. The physical new-abort/BUSY path audit remains the previously reviewed 116,640-state full clock/lock/workspace-basis check. Owner-algebra closure and actual monitored absorption are proved above with the accepted fast-cleanup construction.

This note establishes compatibility and supplies the exact fresh-matrix construction required by the unified manuscript. It does not assert whole-memory preservation, noisy physical retrieval, or an unrestricted-temperature/passive device.

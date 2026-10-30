# Addendum candidate: fast cleanup with the ACTUAL resource monitors retained
2026-10-30, revised after the resource-monitor objection. This does not alter the frozen all-bad-flag credit source. It needs a separate audit; no effective dephasing map is substituted.

## 1. Why the naive version was insufficient
Allowing o_h/z_h coherences in R_h makes the actual label-resolved resource monitor nontrivial. It can no longer be declared a spectator. Including a shared monitor naively could also spoil commutation of h and g credits. The following owner-block decomposition is the proposed repair.

## 2. Monitored owner-block algebra
For a resource r with its actual two-level monitor define

    A_{h,r}= B(span{|o_h>,|z_h>} tensor H_monitor)
              direct-sum C (I_other tensor I_monitor).

`other` includes free and every other owner's o/z labels. Tensor these algebras with the full private h clock/workspace/hub-monitor algebra. The bad projector B_h belongs to it. The coefficients may act arbitrarily on the resource monitor ONLY when r is in h's o/z ownership block. On the other-label block they are scalar in BOTH lock label and monitor.

## 3. Exact decomposition of existing monitor terms
The actual resource monitor has H_mon=Omega I_lock tensor X and distinct jumps

    M_c=sqrt(kappa_m) P_c tensor |0><1|.

Its Hamiltonian is EXACTLY the sum

    H_mon=sum_g Omega(P_o_g+P_z_g) tensor X
              +Omega P_free tensor X.

Assign the g-owned Hamiltonian block and its two already distinct jumps M_o_g,M_z_g to g's local fast generator. Leave the free Hamiltonian block and M_free as a resource-only term. This is an algebraic decomposition of the EXISTING physical generator, not a new conditional monitor, added feedback, or effective Markov dephasing.

All g-owned pieces for g!=h and the free pieces commute with A_{h,r}: they act in its scalar other block. The h-owned monitor pieces preserve A_{h,r} and are retained in h's finite killed matrix.

## 4. Enlarged fast bad-sector generator
In addition to the original fast terms, retain o_h<->z_h cleanup and z_h->free at fixed rates; omit only acquisition/reversal A hops. Retain the h-owned resource-monitor pieces above, as well as the actual hub monitor. Cleanup acts within the h-owned two-level block. The z-reset gain maps an other-block value back onto |z_h>, and that other-block value is independent of the monitor, so the adjoint again lies in A_{h,r}.

Abort tests, C gates, Q verification, workspace refresh, commit and ready depend only own o/z predicates and preserve the same algebra. Terminal/abort DATA gains are deleted in the killed B_h compression because they clear B_h; all retained gains are DATA-free. The bad survival resolvent therefore stays in this monitored owner-block algebra. On an `other` resource-label block it is monitor-independent; this follows from the algebra closure, not an assumed uncorrelated monitor state.

For the absorption proof one may include the FULL actual resource monitors, including their other-owner/free pieces, in the finite local killed matrix. The extra pieces annihilate every element of A_{h,r}, so they do not alter its restricted adjoint or the resulting resolvent; they can be removed again exactly for generator accounting. This avoids assuming a monitor fires on a conditionally inactive block. The ordinary structural-abort / workspace-refresh / C-forward path now uses the already accepted full finite-monitor argument verbatim, with added bounded cleanup terms included in the local path norm budget. All resource/hub monitor variables are retained, and the matrix remains finite. No monitor has been assigned twice in the final physical drift identity: the removed pieces have zero action on the credited observable.

## 5. Exterior and mutual commutation
An exterior owner g preserves h's o_h and z_h labels separately. On a shared resource, its acquisition/cleanup/reset and its assigned monitor terms act entirely in the h-algebra's scalar other block. Its forest payload unitary is identical on o_h and z_h sectors: neither is owned by g, so the corresponding payload gate is absent. Hence every exterior nominal Kraus/Hamiltonian term commutes with the h credit.

For different h,g, their nontrivial resource-monitor blocks are orthogonal: a single lock cannot lie in both owners' o/z blocks. In each joint owner-block sector the sets of monitors acted on nontrivially by h and g are disjoint. Their private hub factors are also disjoint. The coefficients preserve owner-block sectors, so the full h and g coefficient algebras commute, including offdiagonal o/z and monitor coherences. Private analytic erasures change neither locks nor resource monitors, and hence preserve this allocation. The complete CP credits therefore commute.

The unassigned free monitor terms commute with every credit and have zero raw V/W drift. No physical record or auxiliary state is discarded.

## 6. Remaining small perturbation and scope
All steps of ALL_BAD_FLAG_CP_CREDIT_CANDIDATE.md now go through with E_h consisting ONLY of acquisition/reversal A hops. These distinguish free from another owner's tag and need not preserve the displayed algebra. They remain DATA-free, preserve other flags, and obey no-creation for B_h, so their contribution still factors against D_h^flag and is absorbed at sufficiently small fixed amplitude epsilon.

This would permit fast cleanup in a later weak-initiation design. It does not prove clean acquisition service, does not permit unguarded DATA gates, and does not make a busy-until-ready resolvent controller-only when terminal DATA gains are retained. The owner-block monitor decomposition and global CP commutation require an independent audit before use.

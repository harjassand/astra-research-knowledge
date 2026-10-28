# Raw-joint core acquisition for boundary physical residual simulation

28 October 2026. **New substantive acquisition extension; independent receiving pending.** The frozen normalized-core source `COUNT_CERTIFIED_PHYSICAL_RESIDUAL_SIMULATOR.md` (SHA `59b53f8b7a4d54e2f38cb7eb3d643c13d4b356646a3de14967dfa1df6d0da6f2`) and all received CP-lift sources are unchanged. This extension closes a real core-access gap: selective branch words may be required to span the observable process even though all normalized discard preparations are uninformative. It uses joint-event counts, not conditional state preparation or an uncharged rare-event oracle.

## 1. The normalized-core obstruction

A persistent classical bit, realized by a qubit with initial density `diag(p,1-p)`, `0<p<1`, has only the native nondemolition Z projective instrument. Every **normalized** preparation using arbitrary classical feedback, private randomness and almost-sure stopping, then discarding its entire record, leaves this same density: the underlying bit never changes; after observing it, its state is a fixed point of every allowed subsequent operation; and normalized stopping has total probability one on each bit. This induction also covers the empty preparation and any finite random mixture. Consequently the normalized preparation span is one. But the empty branch state and first observed-0 state `p|0><0|` span dimension two, and the empty/next-0 tests distinguish them. The raw-joint observable core has rank two. Within a single episode, no controller feedback can create a spanning normalized core from this declared native library without adding a new physical control. Separately paid heralding/restart-until-success preparation is **not** ruled out: resetting on a failed bit can prepare a normalized conditional state if that extra interface and its expected/worst-case resources are supplied. The present advantage is using raw joint counts without requiring that additional preparation interface or any division by a success probability, not a universal impossibility of all paid normalized preparation. This is a classical special case of a boundary HQMM, not a quantum advantage example.

A separate, narrower illustration starts a qubit in `I/2` with projective X, Y and Z instruments. Every **open-loop** composition/mixture of their nonselective maps leaves `I/2`, while the raw selective states span all four Hermitian coordinates. This illustrates failure of open-loop discarded-outcome strings only: it must not be read as an obstruction to arbitrary feedback preparations. For example, measuring Z and measuring X only after outcome + changes the normalized state even after discarding the record. The persistent-bit example above supplies the stronger obstruction actually used here.

## 2. Subnormalized branch cores and the changed trace row

A preparation `p_j` is now a declared finite native action/outcome word, represented by its **unnormalized** branch state. The empty preparation is first. Let source branch states be `rho_j>=0` with masses `m_j=Tr rho_j<=1`; fitted physical candidate branch states are `sigma_j>=0` with masses `m^f_j<=1`. Neither state is supplied to the learner. Candidate states are computed from its own full CP model. All nonempty states remain unnormalized throughout.

Acquire raw joint tables

    H_ij=Pr(p_j then f_i),      H_z,ij=Pr(p_j then z then f_i),

where `f_0` is empty. Thus the trace row is now

    m=H_(0,:),      m^f=H^f_(0,:),

not necessarily `1^T`, and generally not the same in source and candidate. With the same source rank/core exhaustion and exact candidate rank checks as the frozen theorem,

    C_z=H^(-1)H_z,       C^f_z=(H^f)^(-1)H^f_z,
    c_0=e_1,            m e_1=m^f e_1=1,
    m sum_o C_(a,o)=m,  m^f sum_o C^f_(a,o)=m^f.            (1)

For every true history `c_h`, `p_h=m c_h`, and `(Hc_h)_0=p_h`, `0<=(Hc_h)_i<=p_h`. Consequently the **same** interval inverse certificate and positive-cube computation give `||c_h||_1<=K_core p_h`. Crucially, `D_H` must now include uncertainty in its first row; it is not set to zero except at genuinely known entries.

The fitted lift is still

    T(v)=sum_j v_j sigma_j,      ||T(v)||_1<=||v||_1,       (2)

since every candidate branch mass is at most one. Exact candidate observable rank makes all fitted future functionals agree with this lift, even when physical section intertwining fails. Thus the native true-prefix/fitted-CP-suffix insertion bound is unchanged:

    U=Hhat^(-1), A=|U|D_H, ||A||_infinity<1,
    M=(I-A)^(-1)|U|,
    E_z=M[D_z+D_H|C^f_z|+|Hhat C^f_z-Hhat_z|],
    b=(K_core/2)max_a max_j sum_(o,i) E_(a,o)[i,j].         (3)

This is deliberately a conservative unweighted norm bound; small masses are not silently divided out or treated as normalized preparations.

## 3. One indispensable terminal mass debit

The lift's trace is `m^f v`, not `m v`. Therefore the final trace functional must also be compared. An acquired bound is

    e_m,j=|Hhat_(0,j)-m^f_j|+D_H,(0,j),
    b_mass=(K_core/2) max_j e_m,j.                         (4)

**Extended full-law theorem.** Under the frozen physical-candidate/rank assumptions, with subnormalized branch cores instead of normalized preparations,

    TV(P_true,P_fit) <= min(1,b E_true[L]+b_mass),          (5)

for finite horizon or common almost-sure termination with finite expected native calls. A private pre-call abort coin gives `min(1,b gamma/delta+b_mass)`. Several memory-retaining invocations can be regarded as one complete native transcript from the shared process start; when their only inter-invocation actions are recorded classical decisions, the terminal mass debit is paid **once at the final end**, not once per call. Actual additional quantum macro-readouts must be included as native instruments.

**Proof.** For a fixed native word, telescope with the true endpoint functional isolated first:

    m C_n...C_1-m^f C^f_n...C^f_1
      =(m-m^f)C_n...C_1
       +m^f sum_k C^f_n...C^f_(k+1)
                        (C_k-C^f_k) C_(k-1)...C_1.       (6)

The native terms have exactly the frozen theorem's CP suffix bound. For the terminal term at a true leaf, `|(m-m^f)c_h|<=max_j e_m,j K_core p_h`. The true terminal leaf masses, including clock coins and all terminal labels, sum to one. Summing and dividing by two proves (5). The same labelled truncation argument handles the clock. Neither the intermediate algebraic hybrids nor `T(c_h)` need be positive; true prefix weights and both physical endpoint laws are positive. QED.

For an actual **final POVM** library, use raw joint terminal rows `q_ab,j=Pr(p_j then terminal outcome b)` and candidate rows `q^f_ab,j=Tr(F^f_ab sigma_j)`. The fitted POVM is physical, and source/candidate row sums are `m,m^f`. The one final debit

    (K_core/2) max_a max_j sum_b Q_ab,j,
    |q_ab-q^f_ab|<=Q_ab                                  (7)

already includes their differing mass rows. Do not add (4) a second time. Abort and other no-measurement termination branches use the one-outcome trace test. The final-effect restriction remains: no memory-retaining repeated macro is certified by effects alone.

### Exact failure if the mass debit is omitted

Consider a persistent classical bit, realized by qubit Z projectors, initialized with probability `p` of 0. The core consists of the empty preparation and the first observed 0, and tests are empty and next 0. Then

    H(p)=[[1,p],[p,p]],       m(p)=(1,p),
    C_0=[[0,0],[1,1]],        C_1=[[1,0],[-1,0]].          (8)

Both predictive maps are independent of `p`. Thus sources/candidates with `p=1/3` and `p'=1/2` have **identical native C maps** and zero native residual, but their depth-one and every longer nonempty transcript have TV `1/6`. The trace rows differ. Here the positive-cube constant is `K_core=3`, so (4) is `1/4` and safely bounds the actual error. This is not a technical rounding term; it is mathematically necessary.

## 4. Finite exhaustive core search without conditional-success samples

Supply a finite physical memory-dimension upper bound `d` for the source interface, and put `D=d²`. Supply a tight observable-rank upper bound `r` (equivalently, source rank is `r` for the following eventual-success statement). These remain architectural promises, not consequences of noisy data.

Let `s` be the number of declared native branches. Include **all** raw preparation words of lengths at most `D-1`, and all future test words of lengths at most `D-1`, seeded by trace and every eventual final effect. Reachable and dual observable Liouville spans stabilize by that length: after a stage fails to grow it is invariant, and a strictly growing chain has at most `D` dimensions. The finite Hankel matrix therefore has the complete observable rank. The nonzero empty preparation can be extended to a column basis; the trace row can be extended to a row basis. Hence an invertible `r×r` core containing both empty entries exists in this finite pool.

For `q=sum_(l=0)^(D-1) s^l` words, the trace-only probability pool has at most `(1+s)q²` core/shifted joint events before deduplication. Extra terminal seeds multiply the appropriate future count. The trace-seeded core/shift words have native lengths at most `2D-1`; a terminal seed adds its separately declared physical/native call cost, which is not hidden in that bound. Every event is acquired by a fully specified action sequence from an independent whole-process start, retaining the complete outcome word. If an early required outcome fails, the episode is still a charged episode; its contribution to the indicated joint event is zero. There is **no** division by a prefix probability and no repeated-until-success normalized state oracle. Ordinary simultaneous binomial/Hoeffding intervals apply; shared-setting multinomial events need not be independent for a union bound.

After these counts, enumerate the finitely many `r`-cores containing empty preparation/test and apply the interval inverse test. A selected core can depend on these simultaneous intervals. If none passes, return UNKNOWN. For any truly nonsingular core the test eventually passes as widths shrink; bad conditioning can demand arbitrarily many starts. Native-call and preparation/test lengths, the exponential word list, the number of minors and all count settings are paid. A repeated-round procedure needs a predeclared summable failure allocation. A **loose** rank upper bound alone does not justify choosing a smaller invertible minor and claiming no unseen modes; that remains UNKNOWN unless an independent tighter upper bound is supplied.

Once a core is certified, the frozen finite semialgebraic physical-candidate search works with these polynomial raw-joint word probabilities and the same supplied `d`. Exact rank constraints and PSD/TP remain mandatory; boundary/algebraic witnesses are allowed. On the confidence event the actual finite-dimensional process is a feasible witness. Search inside the rational bands gives `e_m<=2D_H,(0,:)` and the same uniform candidate residual bound

    E_z<=2M[D_z+D_H M(|Hhat_z|+D_z)].                    (9)

Thus both native and terminal terms tend to zero with the bands, under fixed actual core conditioning. This closes the normalized-discard preparation restriction without providing an efficient learner, a dimension-free shot bound, a source-state oracle, or a microscopic reconstruction guarantee.

## 5. Scope and remaining burden

The new mechanism is the raw-joint core plus the explicit terminal mass-row correction, not a claim of new spectral or HQMM learning. S7 already permits subnormalized preparation masses in its quotient norm; the present issue is extending the **physical residual simulator's two-model lift** when those masses differ, and supplying a finite branch-word acquisition pool. It remains equally available to a conventional physical HQMM learner with the same promises.

The source's stationary finite action/terminal interface, independent full-process starts, supplied dimension/rank bounds, and eventually certified core conditioning remain substantive. So do exact physical-candidate rank verification, expensive semialgebraic search, finite numerical/synthesis precision and possibly exponential policy planning. No external coherent reference, physical-memory distance or normalized rare-history promise is inferred from the classical full-law result. The received terminal-test/payload transfer may be invoked only with its separately stated input independence and same-terminal-operation assumptions.

`raw_joint_core_residual_exact_check.py/.json` provides exact symbolic checks of the persistent-bit fixed points and zero-native-residual/mismatched-trace control, and the explicitly open-loop XYZ nonselective obstruction. It obtains zero source samples and is not a count acquisition or solver demonstration.

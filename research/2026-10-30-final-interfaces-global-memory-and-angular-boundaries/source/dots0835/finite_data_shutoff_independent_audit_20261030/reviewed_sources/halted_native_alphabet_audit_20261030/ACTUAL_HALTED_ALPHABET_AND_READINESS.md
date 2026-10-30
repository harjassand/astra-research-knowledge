# Actual halted native alphabet: absorbing readiness and epsilon-independent path
2026-10-30. Complementary PHYSICAL-ALPHABET audit for the root retirement candidate. This proves the stated nominal alphabet/path interface, not the later local polynomial witness, noisy readiness hierarchy, finite-halt energy margin, or whole extraction theorem. The accepted reusable-frame tracker remains separate and unchanged.

## 1. Governing physical instance and exact halt
Read together, with later amendments taking precedence:
1. `repaired_multilock_noepoch_20261029/REPAIRED_GENERATOR.md`;
2. `transactional_data_bridge_20261029/RESULT.md` and `FULL_HILBERT_FOREST_GAUGE.md` (distinct A_k/C0, irreversible complete commitment, every C edge ownership guarded, NO own cleanup in ANY R phase);
3. `weak_initiation_compiler_20261030/UNIFIED_GENERATOR_INTERFACE.md`, frozen SHA256 `c083a0d491e7eb44ee0e575d222ba256152c56a682cadedd08d7785c6032105f` (all actual Ai>=1 complete aborts including Ak, fast cleanup, later acquisition zeta fixed, actual monitors);
4. `ordered_lease_schedule_20261029/EXACT_RESET_MONITOR.md` (separate finite-rate clock/lock-resolved monitor channels).

The halt sets BOTH directions of ONLY the first acquisition edge A0,f<->A1,o_h to zero, for every owner. It leaves every later acquisition/reversal, every Ai>=1->Q0 complete reset, all commitment/C forward and reverse gates, all consistency-abort drives, R resets, terminal resets, A/Q workspace refresh (including A0), Q verification, ready resets, own cleanup, lock resets, and all finite monitors unchanged. The halted generator is exactly the previous physical BUSY fast generator L0. Since its only epsilon-dependent edges have been removed, the whole nominal halted generator is independent of epsilon, with zeta and all other actual physical rates already fixed.

Residual leakage of a nominally disabled edge is a perturbation, not part of this nominal absorption proof. A finite halt ramp is handled separately by the root moment budget. Readiness absorption begins only once the nominal first-edge coefficient is zero.

## 2. The actual commuting readiness projectors
For each owner h with k>=1 ordered resources define

    O_h,r=|o_h><o_h|+|z_h><z_h|,
    C_h=product_(r in R_h) (I-O_h,r),
    P_h=P_A0,h C_h,      B_h=I-P_h.

These are physical CLOCK/LOCK label projectors, identity on DATA, workspace and every monitor. Every P_h commutes every P_g, even at shared locks. A0 with arbitrary workspace is ready in this sense. A0 with ANY own o_h/z_h tag is NOT ready. This is deliberately not the earlier history-bad flag, nor the stronger workspace-zero BUSY flag.

The full forest F is block-diagonal in clocks and locks, so [P_h,F]=0 exactly. On P_h the h forest factor F_h is I, regardless of workspace; more generally every A/Q/R(A)/R(Q) h factor is I. Since the owner factors commute, on a sector with at most m nonready owners the full forest has at most m nonidentity factors, each with its fixed structural DATA support. P_h also commutes the canonical syndrome and actual history-bad projectors, hence with the global memory basin. These are explicit label-algebra facts, not inferred from basin preservation alone.

## 3. Term-by-term Hamiltonian audit: [H_halt,P_h]=0 for EVERY h
- **Own first acquisition:** absent in both directions. This is essential: the original A0,f->A1,o_h edge leaves P_h.
- **Own later acquisition/reversal:** both clock endpoints have A_i with i>=1; both lie in B_h regardless of malformed locks/workspace.
- **Own C gates:** both endpoints are C, hence B_h. Their arbitrary DATA/workspace unitary does not affect this statement.
- **Own consistency abort edge p<->R_(p,j):** R lies in B_h. If p!=A0 then p lies in B_h. If p=A0, the failed-test projector requires an own o_h/z_h tag, so that source ALSO lies in B_h. The reverse uses the same failed test.
- **Own Q verification/unverification:** both endpoints are Q, hence B_h.
- **Own coherent cleanup o_h<->z_h:** if h is A0 both endpoints still carry an own tag and are in B_h; otherwise its clock alone puts it in B_h. Cleanup remains disabled in all C/R sectors as specified in the forest construction, although the readiness commutator alone would not justify changing that architecture.
- **Another owner's acquisition/cleanup:** it changes only free, o_g,z_g labels with g!=h, never the predicates o_h or z_h. It never changes h's clock. Another owner's clock or payload gate likewise commutes P_h.
- **Actual hub/resource monitor Hamiltonians:** act on the finite monitor only, with identity on clock/lock labels, and commute P_h. Their label-resolved reset channels are audited below.

These statements hold for the actual coherent operators on the FULL Hilbert space. They do not assume dephased clocks, clean histories, fixed workspace, autonomous controller marginals, or a classical update process.

## 4. Every physical reset preserves readiness; exact drift and lower bound
Every complete reset has a clock/lock-diagonal bundled loss. Workspace outcomes are SEPARATE channels with the declared complete sum, including s=0. Therefore all J^dagger J commute P_h.

The gain audit is:
- Own commitment, terminal, R abort and new Ai abort sources and targets have non-A0 clocks, so they are B_h-to-B_h for THIS readiness flag. They may heal other flags, but do not by themselves retire the owner.
- Own Qk->A0 ready reset enters P_h exactly when ALL own o_h/z_h tags are already absent. If malformed tags remain it enters A0 but stays B_h; no false readiness is credited.
- A/Q workspace refresh keeps clock and locks unchanged, so it preserves P_h even when it resets dirty A0 workspace.
- Own z_h->free cleanup reset enters P_h only when h is A0 and this is the LAST own tag. Otherwise it stays within B_h.
- Other-owner resets never create an h tag or alter h's clock. In particular their cleanup maps z_g to free, both of which are 'not h'.
- Every actual monitor jump is a label projector times monitor reset and commutes P_h; it does not change the label.

Consequently no jump takes P_h outward, and the exact adjoint identity is

    L_halt^*(B_h)=-D_h,

    D_h = kappa_A,h P_Qk,h C_h
          + sum_(r in R_h) kappa_Z,h,r P_A0,h |z_h><z_h|_r
                              product_(s in R_h,s!=r)(I-O_h,s).       (4.1)

The complete workspace sum is what gives identity on workspace in the first term. Equation (4.1) is physical, before a forest transformation; it retains actual monitors and all other owners. The displayed supports of the ready and last-tag terms are mutually orthogonal. Thus one may take

    nu_h=max(kappa_A,h, max_r kappa_Z,h,r),
    -nu_h B_h<=L_halt^*B_h<=0.                    (4.2)

The looser sum of these rates also works. In particular P_h is an absorbing subspace of the ENTIRE nominal halted CPTP evolution, even with arbitrary outside/reference entanglement. Its complement is an invariant operator corner for the adjoint semigroup: if 0<=O<=c B_h then 0<=exp(t L_halt^*)O<=c B_h. By linearity this extends to every operator supported in the B_h corner. No claim of absorption is made after adding noise; the later perturbed hierarchy must pay reinfection.

## 5. Explicit ClearOwner(h) path with NO acquisition edge
Project h's clock and its resource lock labels using the actual finite monitor instrument (the projection is an analysis record, not assumed instantaneous hardware). Workspace, DATA, monitors outside the flush, and all outside sites may be arbitrary and correlated.

Use this deterministic label-dependent path:
1. If h is A_i for i>=1, take its NEW complete Ai->Q0 reset, even if structurally inconsistent. This includes Ak and does not require any ownership condition.
2. If h is any R label, take its complete abort reset to Q0.
3. Otherwise, if the ordinary phase is inconsistent, select one failed local test, take its p->R_(p,j) drive and complete R->Q0 reset.
4. A remaining C_t is consistent: every lock is o_h. Follow its FORWARD C_t->...->C_L unitary edges and take terminal reset to Q0. Never roll back through commitment.
5. In Q_i, clear each remaining own o_h by the enabled o_h->z_h drive and z_h->free reset; clear each pre-existing z_h by its direct reset. For a consistent Q_i, the already verified prefix has no own tags. Then follow Q_i->...->Q_k verification and its ready reset to A0. Verification tests 'not h', NOT 'free', so other owners can retain their locks.
6. A remaining A0 is consistent and is already P_h; do nothing. No workspace refresh is required for readiness or forest identity (the actual refresh channels stay enabled).

No step acquires ANY resource, and no step changes another owner's clock. No neighbor clearing, first-edge reversal, or epsilon-dependent drive is used. Own cleanup is invoked only in Q, never C/R. Each selected C payload block is a unitary on the FULL dirty DATA/workspace source, so the path's norm bound does not assume a clean payload channel.

A conservative length bound is

    M_h=L_h+3k_h+4.                               (5.1)

More precisely: Ai or R needs at most 3k+2 steps; inconsistent ordinary labels at most 3k+3; consistent C at most L+3k+2; consistent Q_i at most 3(k-i)+1; ready A0 needs zero. Zero/short paths can be padded after readiness because P_h is physically absorbing under the nominal generator. There is no invented reset-history flag.

The new Ai abort is load-bearing. With the first edge disabled, a consistent A1 that owns its first resource and is blocked by another owner on its second has no own progress edge if that reset is removed: reverse across the first edge is disabled, the next acquisition is blocked, its tests pass, and its claimed first lock cannot be cleaned. The repaired apparatus includes the required fixed-rate abort.

## 6. Finite actual-monitor path probability, uniform in epsilon and N
This is a direct specialization of the already reviewed actual-monitor instrument construction in `transactional_regeneration_20261029/ACTUAL_RESET_INSTRUMENT_TAIL.md` §§2–5 and `ordered_lease_schedule_20261029/EXACT_RESET_MONITOR.md`, with the amended path above and actual absorbing event P_h. It is not inferred merely from the old 'some terminal reset occurred' event.

Use a patch consisting of h and its complete resource sites (including their actual finite monitors). Include EVERY nominal generator term touching that patch, including boundary-crossing terms and any added grouped-column program terms when applicable, in a fixed norm bound B>=1. Terms entirely outside are retained as CPTP dynamics. Uniform bounded degree and finite dimensions/rates make B independent of N; with first initiation zero it is independent of epsilon. Let n bound the monitored sites, g_min>0 the minimum selected coherent path amplitude (C, abort, cleanup, verification), and kappa_min>0 the minimum selected reset intensity (NEW Ai abort, old R/terminal, lock cleanup, ready). No acquisition amplitude appears in these minima. If a branch uses only resets, unused coherent minima may be replaced by any fixed lower bound for the available selected types.

For example, adopt the reviewed conservative constants with M=max_h M_h:

    delta<=min(1/(16B), g_min^2/(16B^3)),
    p_step=min(g_min^2 delta^2/4, kappa_min delta/4,1/4),
    u<=min(1/(16B),p_step^M/[8B(M+1)]).

Let a_mon(t)>0 be the exact 2x2 'one resolved monitor emission' Gramian minimum, and set

    w=a_mon(u/n)^n exp[-kappa_mon(n-1)u],
    T0=M delta+(M+2)u,
    p0=(p_step^M/2) w^(M+2) exp[-kappa_mon n M delta]>0.  (6.1)

Nonuniform fixed monitor rates can use their uniform finite minima/maxima in the same inequalities. The initial monitor flush handles arbitrary monitor/reference entanglement. Subsequent timing-density conditioning supplies the normalized projected-path comparison before multiplying by w; no division by a rare-record weight is used. Selected blocks are unique and norm-preserving on their eligible projected label sector, including arbitrary DATA. Competing local terms are included in B. Early entry into P_h remains successful forever under the nominal process, so no later event can undo it.

For every initial state supported in B_h, including coherent clock/lock superpositions and arbitrary exterior/reference entanglement, the selected actual records yield final readiness probability at least p0. Combined with absorption this gives the operator estimate

    exp(T0 L_halt^*) B_h <= (1-p0) B_h.           (6.2)

All constants are fixed by the actual halted apparatus; none depends on epsilon or N. The separately reviewed polynomial-localization/noise proof must still justify its subsequent use of (6.2); this note does not treat a global semigroup observable as exactly local.

## 7. Permanent-frame compatibility and scope
For the accepted finite-group tracker, G acts on DATA/program, not native clock/lock labels, so [G,P_h]=0. Conjugating the entire halted native generator by the SAME permanent G preserves (4.1)–(6.2). Hold the program target during retirement. Its nominal program controls commute P_h and do not change native readiness. One may either work in the fixed G frame, where programs are spectators to the native path, or include their bounded physical terms in B. No native frame inverse is applied in this absorption argument.

The companion exhaustive fixture checks 116,640 arbitrary two-owner clock/lock/workspace-basis configurations, all actual transition directions after the halt, and a clearing path for each owner. Monitor and arbitrary DATA coherence claims rest on the operator block audit and actual-monitor instrument proof above, not on the finite Boolean enumeration. This is an actual alphabet/readiness interface. It does NOT by itself certify noisy retirement, global logical preservation during the halt, bare DATA retrieval, a noisy decoder, or the root's complete extraction theorem.

# Native local rollback with actual retirement: explicit machine and proof
2026-10-30. New candidate, not an independent audit. Prior accepted foundations are unchanged.

## Useful result

The clean rollback rail now has an explicit full-Hilbert owner machine, not an appeal to an unspecified safe abort. The machine has (i) actual two-site hub/resource Hamiltonians, (ii) onsite separately resolved complete resets, (iii) fixed-dimensional grouped sites, and (iv) **only measured classical communication between laboratories**. The new table supplies exact forest conjugacy, individual-reset no-creation, no release/reacquisition of a live prefix, and an actual complete-retirement tail from every malformed state. It also gives a concrete live-engine/FIFO composition with pending READ retention.

A decisive extra obstruction is exposed: **a delayed dirty Alice retirement can invalidate a neighboring Bob cache after Bob has already retired and flushed**. The old atomic theorem's primitive-only mark process is therefore not the native one. `DELAYED_ALICE_TAINT_AND_SERVICE.md` gives the necessary depth-two ancestry and the actual service construction. We do not assert that the old scalar watchdog moment bound or all its global constants survive unchanged.

## 1. Physical sites, entry and full alphabet

In each laboratory, a hub has private finite registers (clock, workspace W, immutable active program P, outer classical control, finite monitor). Resource r has payload D_r, one owner-tag register, and its finite monitor. R_h=(r_1,...,r_k) is the **full raw-read and write footprint**, not just correction support. Fixed k, degree d, circuit length L, workspace/program dimension and message capacity are independent of code size N. A native gate U_t(P) acts on the grouped hub and at most one resource; a hub-only gate may be guarded using any declared resource. Interparty request/reply links are a separately priced measured classical resource; no quantum register or coherent Hamiltonian crosses the laboratory partition.

A new isolated phase I is the engine's entry/ready phase. A one-way onsite load instrument I -> A_0 initializes W and copies the pending finite classical program into P. It is enabled only by the proper local outer READY/WANT condition. This is not a multi-resource ownership test. Capture is classical and onsite. P is immutable throughout A/C/B and their live-prefix abort leaves; responses arriving meanwhile cannot overwrite P. Commitment A_k -> C_0 resets W only, leaving P fixed. Cleanup/retirement can erase P.

The complete ordinary alphabet and claims are:

| Phase | Resource-j consistency test | Claims j? | Frame |
|---|---|---|---|
| I | tag_j not in {o_h,z_h} | no | I |
| A_i, 0<=i<=k | j<=i: tag_j=o_h; j>i: tag_j not in {o_h,z_h} | j<=i | I |
| C_t, 0<=t<=L | tag_j=o_h, every j | yes, every j | V_t(m,P) |
| B_(j0,l), 0<=l<=j0<=L | tag_j=o_h, every j | yes, every j | V_l(m,P) |
| Q_i, 0<=i<=k | j<=i: tag_j not in {o_h,z_h}; j>i unrestricted | no | I |
| R_(p,j), one distinct leaf for each nontrivial ordinary failed test | always history-bad | yes, every j | frame of p |

Here resource indices in the table start at one. All abort leaves claim **all** resources, even R(I), R(A), R(Q); conservative unnecessary claims are harmless and forbid accidental release under a returning dirty prefix. Every unused hardware basis encoding is absent (exact finite qudits), rather than left with undefined behavior.

Ordinary phase count is

    n_ord = 2k+L+4+(L+1)(L+2)/2.

Abort-leaf count is

    n_R = k[1+(k+1)+(L+1)+(L+1)(L+2)/2] + k(k+1)/2.

Thus the clock dimension n_ord+n_R is explicit and fixed. The full grouped hub dimension is this count times dim(W) dim(P) dim(outer) dim(monitor). Resource dimension is dim(D_r)(1+2d_r)dim(monitor). There is no elementary-qubit locality claim.

## 2. Every Hamiltonian and reset class

The Hamiltonian edges below include their adjoints and fixed nonzero finite amplitudes. They never use a joint projector on all k resources.

1. A_i,f <-> A_(i+1),o_h on resource i+1.
2. C_(t-1) <-> C_t with U_t(P), guarded by the actual tag o_h on its target resource.
3. B_(j0,l) -> B_(j0,l-1) with U_l(P)^dagger and the same actual ownership guard; its adjoint is also present.
4. Q_(i-1) <-> Q_i, guarded by tag_i not in {o_h,z_h}.
5. o_h <-> z_h on a resource, guarded by the hub's NOT-CLAIM predicate from the table.
6. p <-> R_(p,j), guarded by p's failed local test on resource j. Source p and leaf are unique.
7. The declared finite onsite clock/lock-label monitors, with no workspace/DATA resolution. All their added positions and norm costs are included.

The separately resolved onsite resets are:

- LOAD: I,W,cache(a) -> A_0,0,P=a,outer BUSY; source classical values and erased W basis labels are separate Kraus channels. Alice uses its fixed READ program.
- COMMIT: A_k,W,P -> C_0,0,P, with equal W-resolved rates.
- SUCCESS: C_L,W,P -> Q_0,0,0, with Bob outer FLUSH_SEND(0), or Alice held DATA(y(W)) as specified below.
- CLEAN ABORT: B_(j0,0),W,P -> Q_0,0,0, with Bob outer FLUSH_SEND(0); Alice preserves its pending READ.
- DIRTY ABORT: every R_(p,j),W,P -> Q_0,0,0, same outer retirement convention.
- NONPREFIX WATCHDOG: each I, A_i, Q_i, or R_(p,j) -> Q_0,0,0, separately resolved over erased W,P and classical input values. It is an actual complete retirement, not merely a request.
- PREFIX WATCHDOG: each C_t -> B_(t,t), identity on W,P and tags, setting Bob's outer state DRAIN. These are separate jump channels. **There is no watchdog reset from a nonzero B position.** Repeated watchdog attempts in B are disabled.
- READY: Q_k,W,P -> I,0,0. It does not change a held Alice reply or pending Alice READ.
- REFRESH: optional complete W-only overwrite in I/A/Q, preserving an active A program and Alice pending/held record. No W refresh in C/B/R.
- CLEANUP: z_h -> free onsite at the resource.

All erasure channels include the zero basis label and have equal intensities within a bundled source. Summed losses are clock/classical-register diagonal and scalar on the erased quantum workspace. No coherently summed eraser is substituted. R may use either its abort reset or the nonprefix watchdog; both are separately priced actual channels.

Let T_h denote the actual complete Q_0-retirement gain: SUCCESS, CLEAN ABORT, DIRTY ABORT and NONPREFIX WATCHDOG. PREFIX WATCHDOG, LOAD, COMMIT, READY, REFRESH and cleanup are **not** T_h. A retirement's DATA instrument is counted before its analysis mark clears.

## 3. Full-Hilbert forest, including malformed tags

Fix h's own-mask m_r=1_{tag_r=o_h} and program P. Delete absent ownership edges from the forward path C_0,...,C_L. In every resulting connected component set V=I at its least-index vertex and extend V_t=U_t(P)V_(t-1) on present edges. Every B_(j0,l) uses the SAME V_l as the forward path. Every R leaf inherits its parent's frame. I/A/Q use identity.

This defines a unitary F_h on **every** clock/tag/program sector. A nonidentity factor acts only on W_h,P_h and resources actually tagged o_h. The direct sums over P permit arbitrary program coherence; no unrecorded program measurement is invoked by this algebra. Different F_h commute because actually owned DATA supports are disjoint in every tag block. Hence F=prod_h F_h is a bounded-depth, bounded-support local frame, with independent factors F_A tensor F_B between laboratories.

- Forward and rollback edges flatten by V_t^dagger U_t V_(t-1)=I and its inverse.
- A B rail truncated at j0 retains the same least vertex of every component it contains, so the forward assignment remains valid.
- Each PREFIX WATCHDOG has equal source/target frame V_t. It becomes a clock-only jump.
- Dirty consistency edges connect equal frames. All I/A/Q Hamiltonians have identity own frame and preserve every other owner's own-mask.
- Own cleanup is disabled in C/B/R. Other-owner acquisitions/cleanup change only non-h tags and preserve h's mask. z_h -> free never changes m_h and occurs only on a resource absent from h's frame.
- Outer receives/discards do not change P, so cannot change F during a live prefix.

Therefore **every nominal Hamiltonian is controller-only in the forest frame**. All DATA changes occur at actual T_h jumps and dressed physical faults. A CLEAN ABORT at l=0 has F=I for every mask. R resets and dirty SUCCESS have bounded dressed DATA support in R_h. The output convention is dressed DATA; no arbitrary-time bare-DATA claim is made.

Conjugating a primitive local fault by F enlarges support only by the finitely many incident F_h factors, not by iteration through the graph. CPTP and reference-uniform norm bounds are preserved.

## 4. Individual-instrument good-range/no-creation proof

On a consistent I/A/Q block the physical good range is W=0. On a consistent C_t or B_(j0,l) block it is V_t(W=0) or V_l(W=0). On every inconsistent ordinary block and every R block it is zero. P is unrestricted by this **mechanical** history certificate: semantic validity of Alice's classical reply is a separate mark below.

In the forest frame P_h^good=I_DATA tensor Q_h is controller/program/workspace-only. The projectors commute for distinct h. Check each term individually:

- acquisition/unacquisition preserves all consistency predicates and carries W=0 unchanged;
- computation/rollback intertwines the corresponding prefix range;
- Q verification and cleanup preserve every structural predicate;
- a failed-test edge annihilates the good source, and its reverse cannot reach a consistent source because it has the identical failed-test guard;
- PREFIX WATCHDOG maps a clean C_t range to the corresponding clean B_(t,t) range, NOT to the bare W=0 range;
- LOAD has identical I/A_0 tag predicates and resets W; COMMIT has identical A_k/C_0 predicates and resets W;
- every T_h maps to Q_0,W=0, which is consistent for every tag configuration;
- READY has identical Q_k/I predicates; REFRESH fixes good W=0;
- all complete reset losses and label monitors commute with the good projectors.

Thus every Hamiltonian preserves each good projector, every individual reset preserves each good range, and T_h has its entire output in h's good range. Other owners' good ranges are unchanged: tags and their private workspaces are untouched by h's reset, and h's owned DATA are disjoint from any clean neighbor's full owned footprint. This is the **individual Kraus/range** statement, not just monotonicity of an averaged defect expectation.

Because Q_h is DATA-independent, Pauli expansion of a dressed local fault or marked reset preserves these inclusions coefficientwise, exactly as in `transactional_data_bridge_20261029/COEFFICIENTWISE_COMPILER_INTERFACE.md`.

### Episode ownership lemma

Let D_h=C union B union R(C) union R(B). On D_h every usable o_h projector is invariant under every nominal term until T_h. h cannot acquire, release, or rotate its usable resource set; other owners cannot acquire o_h. Every exit from D_h is a complete T_h reset into Q_0. There is no reset-free dirty bypass to A/Q/I.

One physical fault therefore marks only a bounded number of mechanical histories. Before their first following T_h, each affected owner emits at most one potentially nonideal DATA-reset instrument. Later unmarked mechanical sources are exact intended terminal instruments or identity clean aborts. This does not yet certify the semantic freshness of Bob's program.

## 5. Actual retirement tail on the entire alphabet

This machine has a simpler first-retirement path than a machine forced to complete acquisition:

- I/A/Q/R: choose the direct complete watchdog, one reset step;
- C_t: choose PREFIX WATCHDOG then a B path below, or a forward terminal path;
- consistent B_(j0,l): follow at most l ownership-guarded inverse edges to B_(j0,0), then complete reset;
- inconsistent B: choose an enabled failed-test edge to its distinct R leaf, then complete reset.

The last two alternatives cover missing ownership at ANY resource, even if a missing gate disconnects the zero endpoint. No disconnected rail is falsely called absorbing at zero. A conservative selected-step bound is m_ret=L+3. The relevant finite patch is h and its R_h, with all incident generator terms charged in the norm budget. Exterior dynamics preserves h's actually owned tags and commutes with its guarded live-prefix payload blocks. In I/A/Q the local finite-path monitor bound includes exterior terms; it does not freeze them without cost.

The actual finite-rate monitor construction and projected-step estimate of `transactional_regeneration_20261029/ACTUAL_RESET_INSTRUMENT_TAIL.md` apply to this **new enumerated generator**: unique nonzero blocks, positive uniform amplitudes, complete scalar reset losses, finite alphabet and norm bound are all present. Substituting the new n,m_ret,B,g_min,kappa_min gives T_ret<infinity and p_ret>0 such that

    (exp[T_ret (L_nominal-T_h)])^*(I) <= (1-p_ret) I.

Here L_nominal-T_h deletes only the gains of the REAL T_h channels, keeping their anticommutator losses. The bound is uniform on arbitrary malformed clocks/tags, workspace/program states, outside/bath/reference entanglement. Iteration gives a uniform exponential no-retirement CP-instrument tail. It is not a uniform instantaneous hazard for B.

The anchored-polynomial construction of `JOINT_LOCAL_LYAPUNOV_TAIL.md` then produces NEW finite-support witnesses alpha I<=Z_h<=I and (L_nominal-T_h)^* Z_h<=-r Z_h. Its simultaneous separated-owner product rule applies without independence of coherent controllers. Old numerical constants or old matrices are not reused.

This certifies retirement probabilities, not quality of an initially dirty emitted instrument. Arbitrary initial controllers can damage DATA or create an extensive initial forest dressing; native storage needs clean/local-stochastic apparatus initialization or a separate initializer. The atomic theorem's arbitrary-controller initialization claim is **not** imported.

## 6. Readiness lemma useful for physical drains

Disable the LOAD I->A_0 channel, and disable the harmless I->Q_0 watchdog in an external stop mode. Retain all live-prefix retirement, Q cleanup/verification, consistency-abort and other watchdog channels. For an owner, I with no o_h/z_h tags is then nominally absorbing with respect to its phase/tags (other owners can change free/non-h tags without changing readiness).

From any phase first execute the Section 5 retirement path if needed, then clear each own o_h via o_h->z_h->free, verify all k resources, and take READY Q_k->I. This is a finite path from EVERY malformed phase/tag configuration, with no resource acquisition. It uses at most L+3k+5 selected steps. The same actual-monitor proof gives a positive probability of readiness by a fixed time, uniformly over the exterior. Because readiness is invariant in the halted NOMINAL generator, the no-readiness effect decays exponentially. The anchored witness argument can use the killed first-entry instrument after adding a finite local analysis flag; readiness itself involves h and k tags, so its witness patch must include them.

This is a halt-mode lemma only. With LOAD active, readiness is not absorbing; with physical faults readiness may be lost and requires an additional sparse-fault comparison. It does not itself remove an ideal decoder or prove a bare-output threshold.

## 7. Regression and scope

`check_extended_owner_table.py` exhaustively checks 66,825 configurations of two overlapping owners with k=2, L=(2,1), over EVERY I/A/C/B/Q/R phase and every resource tag. It checks 449,190 directed transitions, 357,957 live-prefix ownership conservations, 8,505 C-to-B watchdog intertwinings at the label level, all flag no-creation relations, and reachability of halted global readiness from every configuration (maximum shortest path 17). These finite checks support the exhaustive table; the operator and finite-rate probability proofs above are separate.

No external publication/upload has been made. This is a local research candidate with explicit test receipts, not an independent native LOCC threshold audit or a new practical threshold estimate.

# Actual atomic FREE-tag erasure and DATA-free SEAL
2026-10-30. New construction by `producer-workspace/complete_local_rollback_bridge`, incorporating root's FREE-tag exclusion and the native/QCA worker's SEAL idea. Separate from all previously frozen sources. Independent review pending.

## Useful result and exact change

The accepted pause adapter had a real malformed-state hole: a false ERASE clock could reset DATA through a neighboring clean Stinespring prefix. The operation below closes that hole **on the entire Hilbert space**, rather than assuming the old ACK rail was honest. The onsite DATA reset simultaneously changes the ACTUAL resource tag from FREE to a new reservation ERASE. Every native forest factor excludes that DATA register on both tag sectors. Consequently each native mechanical-good range is invariant under the erasure even when the adapter clock, pause bits and command are malformed.

A separate DATA-free SEAL reset and idempotent pause rail give an actual adapter structural-good projector C_x, with a full nominal inequality

    L_nominal^*(I-C_x) <= -mu (I-C_x).

The erasure itself outputs the SEAL-start phase. A mechanically bad adapter therefore emits at most ONE structurally uncertified erasure before its first following seal/erase gain restores this certificate. This restores a meaningful mechanically refreshed-box interface. It does not make a corrupted request or release semantically correct, prove the repaired QCA clocks converge, or supply computational progress. An armed clean request may still be semantically unauthorized.

## 1. Governing hardware and tag extension

Use the exact generic attempt compiler in `autonomous_qca_native_bridge_20261030/EXACT_NATIVE_ATTEMPT_COMPILER.md`, based on `native_locc_rollback_integration_20261030/EXTENDED_MACHINE_AND_OPERATOR_PROOF.md`. Its actual full-footprint alphabet is I/A_i/C_t/B_(j,l)/Q_i/R_(parent,r), with native PAUSE/PARK extension as in the separately accepted adapter. All payload H, including malformed C/B blocks, have the ACTUAL o_h tag guard. Acquisition accepts exactly FREE. I/A/Q and PARK have identity forest; abort R inherits its parent. Full C/B good ranges require all footprint tags o_h. PARK is good iff W=0, with tags unrestricted, and is NOT-CLAIM.

At each erased resource x add one tag e_x=ERASE. It is distinct from FREE and every o_h,z_h. Extend every owner test literally:

* acquisition f->o_h continues to require f, never e_x;
* payload and inverse-payload edges still require o_h;
* consistency and Q verification treat e_x as foreign/not-own;
* NOT-CLAIM cleanup only handles that owner's o_h/z_h;
* e_x has its own onsite cleanup |FREE><e_x|, DATA identity, rate nu_e>0.

The e_x cleanup is safe immediately: the entire erasure occurs in one jump and there is no unfinished erase Hamiltonian or prefix protected by e_x. Larger quarantine safety is supplied by actual pause reservations, not by treating this short-lived tag as an indefinite lock. If a receiver needs a long-lived erased-cell reservation it must withhold this cleanup by a separately proved local guard and re-earn availability. We use the always-available cleanup here.

Resource dimension increases from dim(D_x)(1+2d_x)dim(monitor) to dim(D_x)(2+2d_x)dim(monitor), times its fixed adapter registers. Hub pause bits and all extra monitor labels are finite at fixed degree. Every intersite edge is between this resource/adapter and one incident hub. Every dissipative reset described here is onsite, separately source resolved; no remote many-owner reset is inserted.

## 2. The atomic erasure instrument and exact forest calculation

For a complete onsite desired DATA instrument {K_a} with sum K_a^dagger K_a=I (in particular K_b=|0><b|), use

    J_a = sqrt(kappa) |S_0,arm=0,e_x><H,arm=1,FREE| tensor K_a.

Other adapter source labels are separately resolved. No jump with any non-FREE tag is present. All erased arm/phase labels are resolved, not coherently merged. The total effect is kappa P_(H,arm=1,FREE) tensor I_DATA. The target S_0 is DATA-free and accepts arbitrary pause masks. An actual ERASE-DONE event can record this gain, but its semantic authority is not guaranteed on a malformed source.

Fix all owner-tag and program sectors. In the ownership-deleted forest F_h, the masks on x before and after this jump coincide: neither FREE nor e_x is o_h. A nonidentity F_h acts only on actually o_h-tagged DATA, hence it is identity on D_x in either sector. All other masks and programs are unchanged. Therefore, for every individual K_a,

    F_out^dagger J_a F_in = J_a,

with identity on all native workspaces. This is not merely a clean-source assertion. It holds for arbitrary adapter/native clocks, malformed ownership, program and workspace coherences, including abort leaves, because those forest blocks also use the ownership-deleted mask. The source and target physical mechanical-good projectors have identical native consistency predicates: the table distinguishes own o_h/z_h, not FREE from a foreign label. Thus J_a maps EACH native good range into itself, and its complete loss commutes that projector. The same statements hold for e_x->FREE cleanup.

For a clean C/B prefix using x the source is more strongly zero: its tag is o_h. A race with acquisition is exactly the orthogonality of the FREE and o_h sectors. In A there is no DATA prefix to cut; in a malformed C/B component the forest uses only presently owned resources. If a previous physical fault freed an already-used resource, the corresponding history was already dirty. This proof does not turn such an earlier fault into an ideal operation.

The conclusion does NOT say erasure preserves the logical DATA value. It is a bounded physical DATA channel at x, and may be wrong semantically. It says the erasure cannot secretly create another owner's incomplete-prefix defect. Direct DATA damage and controller semantic damage remain charged separately.

## 3. A fresh SEAL rail, not a stale ACK

Let h_1,...,h_d be ALL owners whose full read/write footprint contains x. Each has x's private pause bit p_j. LOAD is disabled if any pause bit is1. Old resets preserve the new fields; held PARK has no DATA action and cannot leave while p_j=1. QUIESCENT resets W_h to0 with scalar complete effect, preserving PARK and pause. Include every new adapter/bit label in the actual finite reset-timer monitor basis.

The adapter has an inactive IDLE phase, seal stages S_0,...,S_d, distinct intermediate E_(j,b) (0<=j<d,b=0,1), verification V_0,...,V_d, held H, and finite class-selective release phases. It has an arm bit. There is no direct IDLE->ERASE edge.

An actual fresh request capture at IDLE consumes a supplied local command token and enters S_0,arm=1. Command truth is the caller's obligation; consuming the token prevents its nominal replay. Replenishing or corrupting that token is an additional actual operation, not assumed reliable. A DATA-free SEAL reset acts from EVERY non-IDLE adapter phase (including intermediate, verification, held, and release phases) to S_0,arm=0. It preserves all remote pause bits and DATA. Its separately phase/arm-resolved channels have total effect mu P_active, with mu>0. It aborts an uncompleted erase authorization honestly; it never reports ERASE-DONE. No such reset is installed at IDLE: the gadget does not spontaneously quarantine an idle computation forever.

At S_j use the two-site edges

    |S_j,p_(j+1)=b> <-> |E_(j,b),p_(j+1)=1>,  b=0,1,

with distinct E labels carrying b, followed by complete onsite E_(j,b)->S_(j+1) jumps. These edges preserve arm. The first j pause bits remain1. A branch that started with p=1 never clears that bit, even before commitment; the reverse b=1 edge also has p=1. A branch started with0 can reverse only before its actual onsite advancement, when that bit has not yet been certified. Starting from a clean all-held H, a SEAL restart therefore never releases any existing held bit.

At S_d use an onsite transition to V_0. Verification edges V_j<->V_(j+1) test the ACTUAL joint onsite hub predicate PARK_(h_(j+1)) AND W_(h_(j+1))=0. This is a two-site Hamiltonian guard, not a projective test imposed externally. All p bits stay1. An already verified PARK,W0 is invariant while this bit is held: no unpark/LOAD/payload is enabled, all other owners act elsewhere on this private W, and QUIESCENT fixes W0. At V_d an onsite transition enters H. No cached ACK is stored.

If H has arm1, the section2 FREE-tag erasure may fire. Its target is S_0,arm0, not an unchecked HOLD label. Even on a malformed H source, this is a structurally good target. The adapter re-seals and freshly verifies without repeating the DATA erase. If H has arm0, it is a DATA-free sealed boundary. An actual caller may release it using the next section; it cannot recreate arm1 without first returning to IDLE and consuming a new command token.

## 4. Selective release and idle cleanup are real finite operations

Partition incident owners into fixed COMPUTE and REPAIR classes. REPAIR means its actual compiled payload is clock/auxiliary-only; merely saying the completed channel leaves DATA alone is insufficient if a dirty prefix can write DATA. Before an erasure, the seal includes BOTH classes and any auxiliary readers. After erasure, the caller can request either a fixed REPAIR-only release or an ALL release. The mask is captured into a finite local release-clock branch. The unselected bits remain1, so COMPUTE cannot restart during repair-only release.

For each selected bit use the concrete two-site clear edges

    |R_j,p=b> <-> |F_(j,b),p=0>, b=0,1,

with distinct F labels, then onsite F_(j,b)->R_(j+1). Reverse before the onsite advancement is allowed; no DATA operation occurs anywhere on this rail. At its end enter IDLE with arm0. IDLE does not clear unselected held bits: those are the actual continuing COMPUTE quarantine. A later probe/request starts S_0 and again seals BOTH classes. An ALL release clears every own bit. False class selection or premature ALL release is a semantic controller fault, not certified by this mechanical construction.

A separate explicit caller operation can request cleanup of orphan bits while IDLE, using the same DATA-free class-selected rail. It is not an unconditional clearing channel: after a legitimate REPAIR-only release, unconditional idle cleanup would wrongly unfreeze COMPUTE. Thus retained nonzero idle bits are intentional and do not imply an erasure authority. Availability/progress must use the intended caller phase rather than demand unconditional unpaused normal service.

SEAL resets on a release rail may abort release and reassert bits. They never perform DATA erasure and never clear a previously held bit. Positive probability of completing a held release word follows by selecting no SEAL gains over a fixed interval with their full finite loss retained; this is not guaranteed liveness under arbitrary corrupt commands. The higher clock algorithm must tolerate the abort/retry semantics.

## 5. An actual full-Hilbert adapter certificate and exponential healing

Define C_x as follows, including all arm values unless stated:

* IDLE and every release/clear phase: the entire pause/native Hilbert space; these phases have no DATA action and cannot reach an erase source except via S_0 and fresh verification.
* S_j: the first j own pause bits equal1; all later bits and every native engine/W are unrestricted. S_0 is the entire pause/native space.
* E_(j,b): the first j+1 bits equal1, with the explicit intermediate label b.
* V_j: all d bits equal1, and h_1,...,h_j have actual PARK,W0.
* H: all d bits equal1 and every incident h has actual PARK,W0.

This is a commuting local projector (phase/pause/onsite-W predicates), not an assertion that all clocks are classical. Its support is x and the finitely many incident hubs. The inherited native Hamiltonians preserve each verified PARK,W0 block while its bit is held. Every adapter Hamiltonian above interchanges exactly equal good/bad predicate sectors. Every individual reset maps the C_x range into itself, and every COMPLETE reset loss commutes C_x. In particular an ERASE gain always lands in unconstrained S_0, and a SEAL gain does too. Native QUIESCENT/retirement may bring a previously unverified/malformed sector into C_x but cannot leave a verified held-PARK,W0 sector. Other adapters change only their own pause bits; x's held bit already suffices to prevent verified PARK departure. Consequently nominal L^*(B_x)<=0 for B_x=I-C_x.

The SEAL bundle gives the stronger exact contribution -mu B_x: B_x is supported only on non-IDLE phases, its gain has zero B_x effect, and its loss is mu P_active commuting B_x. Hence

    L_nominal^* B_x <= -mu B_x.

This is an operator inequality uniform over arbitrary malformed apparatus, DATA/bath/reference correlations. Its consequence E[B_x(t)]<=e^(-mu t)E[B_x(0)] does not erase earlier DATA errors. It is a certificate-healing statement, not a logical initialization theorem. No finite monitored-path estimate is needed for this particular certificate.

On a nominal interval beginning mechanically bad, the first actual SEAL or ERASE gain maps the adapter into C_x. There is no later structural badness without a new physical defect. Therefore at most ONE ERASE from B_x is possible per such defect episode (the erasure itself ends it). Wrong erasures from a structurally good but semantically false command are not counted by this statement; they belong to caller/clock damage, which remains open.

Together with section2, EACH native mechanical-good projector is now invariant on the FULL adapter Hilbert space, not just C_x. The original first complete native retirement restores that native owner, and later adapter erasures cannot break it. The normal-or-quiescent two-hit event regains its native mechanical meaning without assuming the adapter was already healed. A genuinely sealed boundary additionally requires the actual fresh S_0->...->H completion, or the C_x+H source predicate, not an arbitrary initial H label.

## 6. Finite actual service and remaining receiving obligations

Orphan e_x tags are cleared by actual onsite cleanup; selecting those gains and then no new erasure while a finite service word runs has positive effect with all losses retained. Owner retirement/own-tag cleanup/Q/PARK paths are unchanged except for the finite new foreign tag. A held nonzero pause mask gives QUIESCENT; a zero mask gives the inherited actual ordinary attempt. The full monitored-word argument must include the expanded tag/adapter alphabet and the SEAL/release channels, with newly computed constants. It produces a fresh one-hit and then two-hit union-event bound; it does not turn QUIESCENT into Phi execution.

For adapter sealing itself, select a SEAL gain, the d idempotent set-to1 steps, the actual incident-owner retire/cleanup/QUIESCENT words, fresh PARK,W0 checks and H entry. Suppress conflicting local adapter changes only by real monitored records/no-gain intervals, retaining every loss. This finite actual word has positive complete effect uniformly on the full finite local alphabet; there is no selected favorable workspace outcome. Its final H source is both structurally certified and genuinely owner-good. At a structurally consistent source it has physically completed all requested pauses, not merely copied an earlier ACK.

The DATA erasure support remains one cell, native dirty first retirements remain bounded full footprints, and a bad adapter cannot create a new clean-prefix defect. These are useful inputs to a leading-rectangle/boundary-comb proof. No bound on all later algorithmic damage follows just from them. A receiving QCA proof must still establish: correct command/release semantics in good regions; actual read-only REPAIR compilation; legal/invalid clock constraints and an immutable-while-tested validity predicate; retry and convergence/progress; local damage induction under continuous noise; boundary-port factorization and consumer logical causal order. It must use the union event rather than demand computational updates in a deliberately paused box.

This is an active dissipative controller with continually available reset/monitor entropy export. No equilibrium passive storage, zero-power operation, environment reconstruction, elementary-qubit implementation, numerical threshold or reservoir heat cost is claimed. All prior memory, recipient and pause/stopped source bytes are unchanged.

## 7. Operator details, diagnostics and receiving form

The no-creation step uses an explicit operator fact, not a classical trajectory assumption. If a projection C satisfies [H,C]=0, each actual Kraus J has (I-C)JC=0, and each COMPLETE bundle effect Gamma commutes C, then

    sum J^dagger (I-C) J - {Gamma,I-C}/2 <= 0.

Indeed its gain is supported in the bad corner and is bounded by (I-C)Gamma(I-C). All new phase/arm-resolved bundle effects above have the required commutation. For SEAL the gain is zero in this corner and Gamma=mu P_active, giving exactly -mu B_x. Native complete losses are clock/tag diagonal and scalar on erased W, hence also commute the verified PARK,W0 predicates. The actual reset-timer monitors resolve only their declared finite labels and are included with their real Hamiltonian and losses; no ideal instantaneous pinching substitutes for them.

C_x commutes every native mechanical-history projector. In a block where it constrains an owner it specifies actual PARK,W0, where that owner's forest is identity; in its other blocks it is unrestricted on that owner's W. It also commutes the global ownership-deleted forest. Thus its forest-frame form is controller/workspace-only and the established coefficientwise local-error interface can include this new certificate. This statement is not preservation of an arbitrary full commutant algebra by every channel.

The one-uncertified-erase assertion has a source-range formulation: J_erase B_x has its entire range in C_x, and every subsequent nominal Kraus word preserves that range, so inserting another B_x-source erase gives zero. This does not assign Poisson parent records to general continuous noise. Under continuous noise a cavity/bad-region argument still has to charge the local insertions and semantic controller damage.

`check_atomic_tag_and_seal.py/json` checks 600,576 actual native label states over all four pause masks and 4,609,664 directed transitions, including 800,768 FREE/ERASE tag transitions. Every native structural flag is unchanged by those tag transitions, and all actual extended native no-creation checks pass. A separate 1,368-state SEAL graph tests the claimed certificate, including all 530 malformed states, coherent-edge predicate equivalence, full SEAL/ERASE target healing, and held-PARK invariance. Finally 48 full-workspace random-unitary ownership-deleted forest fixtures verify individual erasure intertwiners (maximum norm error 1.30e-15). The old unguarded CNOT-prefix counterexample remains exact with bad mass1. These are supporting diagnostics; the arbitrary-unitary proof and positive actual finite-path arguments are in the text.

The artifact does not revise the earlier scoped pause/stopped receipt. A receiver may replace its OLD unguarded erasure with this NEW alphabet only after accepting these actual hardware and abort/retry changes and recomputing its service constants. Neither the prior exogenous recipient theorem nor a noisy QCA theorem follows automatically.

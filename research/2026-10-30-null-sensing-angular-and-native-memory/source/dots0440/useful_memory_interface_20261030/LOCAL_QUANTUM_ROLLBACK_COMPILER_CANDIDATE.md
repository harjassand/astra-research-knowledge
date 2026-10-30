# Clean local rollback: finite-quantum-module bridge for the LOCC controller
2026-10-30. Exact clean-instrument mechanism plus explicit full-Hilbert frame extension candidate. This is NOT yet an accepted complete native noisy LOCC compiler.

## Useful mechanism
The broader autonomous FIFO theorem used atomic local quantum instruments. Its chief obstacle to a finite quantum-gate implementation is a watchdog firing in the middle of a data/workspace prefix: simply erasing that workspace can damage the code even without external faults.

A local rollback corridor removes that nominal damage. Preserve the transaction's private program and all resource locks; transfer the clock into a reverse-prefix corridor; reset workspace/program and release locks ONLY at the zero-prefix endpoint. Every clean canceled transaction then implements exactly the identity DATA channel, including arbitrary references. Everything is local to one laboratory. No coherent interparty bus is introduced.

## 1. Explicit clean corridor
Let the fixed finite local unitary payload be V_j(a)=U_j(a)...U_1(a), j=0,...,L, with V_0=I. The classical program a is copied into a PRIVATE engine register at the start, while the frame is identity. It is not erased or changed nominally until engine retirement. Pad all program variants to the same L and use the same clock rates.

The original computation path is C_0,...,C_L. Add private clock states

    B_(j0,ell),     0<=ell<=j0<=L.

For each j0, the rollback Hamiltonian has edges

    g_ell |B_(j0,ell-1)><B_(j0,ell)| tensor U_ell(a)†
       + Hermitian conjugate,       ell=1,...,j0.       (1)

The edge has the same actual ownership guard as its original payload edge. Workspace-only gates are onsite at the grouped hub; a data-touching gate is a hub/resource two-site Hamiltonian term, as in the native grouping.

A watchdog during computation uses separately resolved onsite jumps

    L_j=sqrt(mu) |DRAIN,B_(j,j)><RUN,C_j| tensor I_W,P.  (2)

It preserves workspace W, private program P and resource tags. All B phases retain the same full claim set as computation. Cleanup/release is forbidden until a complete terminal or dirty-abort reset. Repeated watchdog attempts in DRAIN are disabled/no-op; they do not keep restarting the rollback.

Only ell=0 has a nominal successful rollback-reset instrument,

    J_(j0,s)=sqrt(kappa_R)
                 |FLUSH_SEND(0),Q0,workspace0,program0>
                 <DRAIN,B_(j0,0),s|.                  (3)

Channels are resolved over ALL workspace/program basis states s. Summed loss is scalar on those registers. This reset restores the outer master to a fresh FIFO flush, not directly to a new quantum computation. Resource cleanup follows the actual reset-before-release convention.

## 2. Exact identity abort instrument
In the all-owned clean sector, define

    F_Cj=V_j(a),   F_B(j0,ell)=V_ell(a).

Conjugation removes every payload from (1), and (2) is unchanged because its source and target have the SAME frame V_j(a). The watchdog outcome j is a workspace-blind clock measurement. On a clean transaction its probability is independent of DATA/reference/program because the transformed clock evolution is scalar and program lengths/rates are padded uniformly.

The rollback source in this frame is DATA tensor workspace0. Every intermediate clock evolution is DATA-independent. At ell=0 the frame is I; summing the resolved reset labels in (3) therefore gives the identity on DATA. For each specified watchdog position and rollback reset-time/monitor record,

    I_abort,record = scalar_nonnegative(record) * id_DATA.  (4)

The assertion holds on arbitrary DATA/reference inputs and on classical program values correlated with a retained gauge/bath. It is an instrument identity, not a claim that the bare DATA is undisturbed at intermediate prefixes.

Each finite rollback rail has nonzero nearest-neighbor couplings and an absorbing reset at its endpoint. With no extra clock transitions, its no-reset non-Hermitian generator has no dark subspace: a vector vanishing at the lossy endpoint must vanish recursively along the connected tridiagonal path. Finite dimension gives an exponential no-reset tail with constants depending on the fixed L/rates. Compatible workspace-blind clock-diagonal monitors preserve the gauge; their actual absorption constants must be checked if added. No numerical/practical tail constant is asserted.

## 3. Full-Hilbert forest-frame extension to check
For an arbitrary ownership mask m, use the existing native prefix V_ell(m,a): missing ownership edges break the path into components, each assigned frame I at its least index. Assign EXACTLY the same V_ell(m,a) to every rollback copy B_(j0,ell) that contains ell.

Then:

- Every present rollback edge is flattened by the same intertwining identity as its forward counterpart.
- Each watchdog jump C_j->B_(j,j) has equal source/target frame even for malformed masks, so it is DATA-trivial in the dressed frame.
- F_B(j0,0)=I for every mask and program; the successful rollback reset introduces no extra dressed DATA operation.
- Nonidentity frame factors act only on private workspace/program and actually owned payload resources. Different owners' factors still commute.
- All new phases retain claims until reset, so a nominal cleanup transition cannot invalidate another owner's frame through premature resource release.

A missing ownership edge may isolate a rollback component above ell=0. It MUST NOT be declared able to reach zero. Attach the existing failed-consistency abort/reset mechanism to rollback positions: its leaf inherits V_ell(m,a), holds all computation claims, and performs an actual complete reset before release. Such a dirty reset has a bounded-support dressed DATA instrument, just as in the original forest proof. In a clean all-owned transaction those failed-test drives are disabled.

These identities give a concrete full-Hilbert gauge candidate, not yet the entire no-creation/ancestor theorem. The expanded label/claim/monitor table must be enumerated and checked; dirty bypasses, orphaned tags and actual reset tails must not be inferred from the clean calculation alone.

## 4. Export Alice's syndrome as a measured classical message
Alice's local payload is a finite unitary dilation of her commuting check instrument. Its workspace contains syndrome y. A terminal reset may write a held classical reply at the SAME local hub:

    K_s=sqrt(kappa_T)
          |Q0,engine0,program0,HOLD(DATA(y(s)))><C_L,s|. (5)

All s are separate Kraus channels, with equal rates. Thus the output y is genuinely classical/dephased; summed source loss remains scalar. The engine cannot start another READ until this held response has been enqueued. This preserves the response-before-next-request FIFO discipline. Private reset/cleanup may proceed without changing the held response.

Equation (5) replaces merely discarding the final syndrome workspace; it is an explicit physical pointer output, not access to an imagined environment measurement record. Its faults are counted. No quantum syndrome ancilla is sent between the laboratories.

Bob's engine uses the classical Alice reply as its private program a, acquires the full local read footprint, and runs the finite Bob-syndrome/table/Pauli circuit. His successful terminal reset consumes that program and sends the master to a fresh FIFO flush. A watchdog sends the master to DRAIN; neither the outer cache nor a later reply may overwrite the active engine program. New work is blocked until successful rollback or a charged dirty-abort terminal reset has actually retired that engine.

## 5. Why local locks suffice
Gate-level Alice reads must locally reserve their quantum footprints: even commuting COMPLETE check instruments can have incompatible simultaneous gate prefixes. Gate-level Bob corrections likewise reserve their full raw-read footprints through terminal/rollback reset.

No interparty quantum lock is required. In the tensor-product LOCAL forest frames, completed Alice instruments only measure stabilizers and do not change her dressed syndrome; unfinished local Alice prefixes are removed by her local frame. Bob's locked snapshot is fixed during his local payload. An Alice physical fault during a pending Bob read/program marks that Bob dependency and pays for its possibly stale correction. All crossparty synchronization is classical request/reply/flush communication.

The final mathematical memory output would be dressed by F_A† tensor F_B†. This is a local product frame, not an entangling crossparty decoder operation. Bare unfinished DATA remains outside the guarantee, as in the original native theorem.

## 6. Remaining proof targets before a native claim
1. Enumerate the extended C/B/dirty-abort/Q/acquisition label and resource-claim table; prove the individual-reset no-creation property for every new nominal term.
2. Prove the actual no-retirement tail for the expanded engine from arbitrary phase/tag/program state, including failed ownership, rather than only the clean rail tail.
3. Compose the physical FIFO and engine FSM: a watchdog clears semantic taint only after retirement and the forced flush, not at watchdog request time. Recompute the marked-emission/ancestor bound with that real lifetime.
4. Prove a uniform good-service word from arbitrary coupled lock/engine/channel state; neighboring local resets must clear resource conflicts without releasing a live quantum prefix.
5. Recompute dressed primitive footprints and the common positive-record noise majorants; retain controller/bath coherence.
6. Account for actual measured classical channel primitives. Even if all within-laboratory quantum gates use two-site Hamiltonians and onsite resets, the communication links are an additional declared resource, not derived from a shared coherent hub.
7. Re-audit physical terminal mode changes and raw-mask teleportation when live engine prefixes are present.

The clean rollback instrument and syndrome export in (4)-(5) resolve specific missing mechanisms. They do not justify treating the rest of this list as automatic.

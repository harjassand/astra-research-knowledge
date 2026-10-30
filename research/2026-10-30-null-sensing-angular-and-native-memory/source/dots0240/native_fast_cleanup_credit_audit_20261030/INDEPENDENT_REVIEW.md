# Independent audit: fast cleanup with the actual shared monitors
2026-10-30. Reviewer: `producer-workspace/review_simple_compiler`.

## Result first
**Scoped PASS.** The frozen addendum supplies the claimed exact repair of the shared-resource-monitor problem. Fast coherent `o_h <-> z_h` cleanup and fast `z_h -> free` reset may be retained when constructing the local bad-history credit. Only acquisition/reversal must be made sufficiently slow for this argument. This is a revised fixed-rate instance of the actual transactional generator, not an effective dephasing model.

No counterexample or substantive gap was found in the new bridge. The receipt gives the missing explicit algebra and absorption details below. It does **not** supply clean acquisition service or a native continuous-noise memory threshold.

Two essential readings of the source are part of the acceptance:
1. Cleanup retains the transactional eligibility rule: only Q, or unclaimed resources in A; **never R or C**. The addendum changes rates, not this rule.
2. Exterior commutation uses the exact **decomposed generator**. The unsplit full resource-monitor Hamiltonian does not commute with an owner's credit. No such false claim is needed.

## Frozen sources and governing interfaces
The author confirmed both sources frozen before this audit:
- `FAST_CLEANUP_DIRTY_CREDIT_ADDENDUM.md`: SHA-256 `56ef9fc6f44e81e5a4a2686542e71e1c599621283ee9bfa109c529a109b5e270`.
- `ALL_BAD_FLAG_CP_CREDIT_CANDIDATE.md`: SHA-256 `e5c58ae619461f41c44cd3ebc77b82d2cc9f0a5d2142b236b187b2c38e9342f2`.

Copies are in `reviewed_sources/`. I read the root's base all-bad receipt, actual repaired generator and transactional modifications, full-Hilbert forest gauge, actual monitor construction, finite projected-path proof, no-creation proof, and raw nonmonomial reset envelope. `SOURCE_SHA256.txt` identifies these exact inputs. I checked the base interfaces needed here rather than reopening the accepted code/barrier machinery.

## 1. The full owner algebra, not a classical mask restriction
For each shared resource r put `P_hr=P_o_h+P_z_h`, and define

    A_hr = B(P_hr H_lock tensor H_monitor)
           direct-sum C [(I-P_hr) tensor I_monitor].

For owner h use the finite C*-algebra

    A_h = B(H_private_h) tensor product_{r in R_h} A_hr,

where private includes clock, workspace and the actual hub monitor. Tensor with identities elsewhere. The complement is scalar in **both** lock label and resource monitor, but its coefficient may depend on the private h register and other resource factors. This interpretation is important.

Every h consistency projector, and hence the forest-frame B_h, belongs to A_h. The bad corner `B_h A_h B_h` is closed under the killed adjoint below. Members may have arbitrary `o_h/z_h` and monitor coherences; they have no coherence from that entire owner block to its complement. This is a property of an observable algebra, not a measurement or a restriction of allowed input states.

For distinct h,g the resource algebras commute. The non-scalar blocks `P_hr` and `P_gr` are orthogonal. On the h block a g operator is scalar, on the g block an h operator is scalar, and on the remaining block both are scalar. Their private registers are disjoint. Tensoring proves `[A_h,A_g]=0`, also when the operators entangle several shared monitors with their own private registers.

## 2. Exact accounting of the physical monitor
The actual physical terms are

    H_mon = Omega I_lock tensor X,
    M_c = sqrt(kappa_m) P_c tensor |0><1|,

with a **separate physical jump for each c**. Therefore

    H_mon = sum_g Omega P_gr tensor X + Omega P_free tensor X

is an exact linear Hamiltonian decomposition. Assign `Omega P_hr tensor X`, `M_o_h`, and `M_z_h` to h. Leave the free block as a resource-only term. No dissipator is split into different Kraus channels, no labels are merged, and no new conditional physical operation is introduced. The original single Hamiltonian is still exactly the sum written here.

Every other-owner/free piece commutes with A_h. Its Lindblad adjoint therefore annihilates A_h, not just B_h. The own piece generally does NOT commute with A_h and must be included in the killed matrix. This distinction survives arbitrary initial entanglement of the shared monitor with locks, DATA, private registers or a reference.

## 3. Closure with the real fast cleanup
In the forest frame all h Hamiltonians are DATA-free. In particular own cleanup is unchanged by the frame only because it is restricted to A/Q. The forbidden R cleanup is not restored.

Own cleanup is an A_h Hamiltonian. Abort tests, C ownership gates after gauging, Q verification, clock/workspace overwrite instruments, commit and ready all preserve A_h in the adjoint. Their coefficients use only own o/z predicates. The own-monitor pieces also preserve it.

The less immediate term is `J_z=sqrt(kappa_Z)|free><z_h| tensor I_monitor`. For X in A_h, its free block is monitor-independent and agrees with all other non-h labels. Hence `J_z^* X J_z` places exactly this scalar-complement coefficient on the z_h block. The anticommutator with `J_z^*J_z=kappa_Z P_z_h` remains entirely inside the own block. Thus the reset adjoint preserves A_h even though J_z itself is not an element of A_h.

Every actual terminal/abort gain exits B_h to universally consistent Q0 with workspace zero. Delete those gains, and the good-output parts of the other jumps, when forming the killed bad generator; retain complete losses. Consequently all retained gains are DATA-free. Because B_h lies in A_h, the killed adjoint preserves its corner. The survival effect and resolvent therefore belong to that corner.

## 4. Absorption without an inactive-monitor assumption
For the absorption proof only, add to the finite h matrix **all** resource-monitor blocks, including other-owner and free blocks. These additional generators annihilate A_h. They commute B_h and have no bad-to-good flux, so their killed adjoints also annihilate `B_h A_h B_h`. It follows by finite-dimensional uniqueness of the adjoint ODE that

    exp(t K_assigned^*) B_h = exp(t K_full-monitors^*) B_h

for every t. This is an exact equality of survival effects, not merely a norm estimate. Thus the full-monitor proof and the assigned-generator accounting give the same resolvent.

The added full monitors have precisely the physical form required by the accepted finite-rate monitor argument: no-monitor-emission evolution factors between the main clock/lock dynamics and all two-level monitors; distinct emissions project clock/lock labels without measuring workspace. Their finite-window emission Gramian is strictly positive, including for initially entangled monitors. The flush and subsequent finite measurement windows are therefore valid here. We never ask a conditionally inactive owned block to emit.

After a recorded joint clock/lock configuration, every bad source has one of the following bounded paths:
- inconsistent ordinary phase: an enabled failed-test abort edge, then complete abort reset;
- any R phase: complete abort reset;
- consistent A/Q with nonzero workspace: complete refresh;
- consistent C with nonzero workspace: the forward C path, then complete terminal reset.

The last path is forward, not a fictitious reversal through irreversible commitment. In a consistent C block cleanup is disabled and all required own tags are present. Every desired Hamiltonian edge has its nonzero scalar block; other cleanup terms do not cancel it. Added fast cleanup and reset terms only increase the finite local norm/loss budget in the small-time projected-path estimate. One selects no undesired ordinary resets on a path, and sums the complete workspace outcomes at its final healing reset. Workspace and reference entanglement are spectators in this estimate.

There are only finitely many local labels and path types. Thus for some fixed T,c>0,

    exp(T K_h^*) B_h <= (1-c) B_h.

Iteration gives an integrable tail. Hence

    R_h = integral_0^infinity exp(t K_h^*) B_h dt,
    0 < r_min B_h <= R_h <= (T/c) B_h,
    K_h^* R_h = -B_h.

All constants are size-independent, may depend badly on the fixed fast cleanup/monitor rates and finite circuit, and are independent of the omitted acquisition amplitude epsilon. This is enough for the base credit; no monotonicity of absorption under adding Hamiltonians was assumed.

## 5. Exterior physical terms and full coherent masks
An exterior owner g preserves each h label o_h and z_h separately. Its acquisition/free transitions, cleanup, and z-reset act entirely inside the h scalar-complement block; they commute every h coefficient even though some of their own Kraus operators cross the g owner/complement split. They do not act on h's private registers.

The exterior forest payload unitary is identical on o_h and z_h: neither label is o_g, so the corresponding g payload edge is absent in both cases. Equivalently, on the h block g cannot use this resource's DATA; on the h complement h's coefficient is label/monitor-scalar. Thus actual transformed exterior terminal/abort Kraus operators and their adjoints commute with A_h as well. This is a whole-matrix statement, including malformed ownership superpositions, not only a diagonal-mask check.

After the exact monitor allocation of section 2, every exterior grouped Hamiltonian and jump commutes with the h credit. Free-monitor terms commute with every credit and annihilate raw V/W. No monitor term is counted twice.

## 6. The base bad-credit proof transfers
Let `D_h=V(B_h=1)-V(B_h=0)>=0`, and write `V=V_0+B_h D_h`. The same holds for W. Every element of A_h preserves DATA syndrome and every other B_g, so it commutes V_0 and D_h.

Choose `S_h=s0 B_h+beta R_h` on the bad corner, extended by identity on good, with `s0=1-beta Rmax>1/2` and `Rmax>||R_h||`. The analytic erasure keeps all locks and monitors and resets only h's clock/workspace to Q0,0. Its input-weighted Kraus operators are

    sqrt(S_h),   E_erase,a sqrt(I-S_h).

They belong to A_h, are complete, and give `T_B,h(V)=V_0+B_h S_h D_h`. No pinching is inserted. Their basin preservation follows from syndrome/other-flag preservation and removal, never creation, of h's tokens.

The actual nonmonomial DATA cost is still needed. The base completion/envelope estimate is

    q_R = 2^(R+k) theta^[cR-(2-c)k] / (1-theta^R),

with R>k, c(R+k)>2k, and theta small enough for q_R<1/4. It bounds every complete terminal/abort DATA gain relative to flag removal, including arbitrary dirty workspace/reference input. Terminal clean/dirty cross terms vanish by deterministic-syndrome clean-image invariance; lock-preserving raw target observables give no cross-mask term. Enlarging S_h does not alter these target gains: every healing output has B_h=0. The complete losses and S_h cross-blocks are already inside K_h.

Consequently the exact assigned fast generator obeys the base inequality

    L_h,fast^* T_B,h(V)
      <= -beta B_h D_h -(s0-q_R) A_heal,h D_h

on bad sources, together with the unchanged raw good-source decrement. Data-free fast z-reset healing contributes to A_heal but not to the positive payload cost. Full good/bad cross terms for such jumps vanish by no-creation and complete-loss commutation. The same derivation holds for W.

Only actual acquisition/reversal remains in E_h. It is DATA-free, annihilates V_0,D_h, and preserves B_h exactly. Hence `E_h^*(B_h S_h)` is supported on B_h and has norm at most C epsilon. Taking epsilon<beta/(2C) gives uniform `-(beta/2)B_h D_h` service. All rates remain strictly positive fixed constants; no limit is taken.

Different bad credits commute because their complete Kraus operators lie in commuting algebras. They also commute with the accepted good committed-chain credits: for the same h their source sectors are orthogonal and the erasure target Q0 activates neither; for another owner the ownership-block argument applies. Global CP transfer is therefore exact, without an extensive remainder. On a dirty commit, any additional cleared-target C credit only lowers the gain; source flag-dense demand is not substituted for cleared-target demand.

The no-jump coefficient commutes each raw animal, so the existing lower comparison survives even though it does not commute individual own lock projectors. Only syndrome and actual flag projectors enter the animals. All operator statements extend by identity to a retained reference/common bath. This is not by itself a final noise/service coverage theorem.

## 7. Independent regressions
`check_two_owner_algebra.py` uses a 40-dimensional space (five lock labels, one actual monitor, two private registers). It checks every pair of 68 matrix-unit basis elements for the two proposed algebras: all 4,624 commutators are exactly zero numerically. All tested actual exterior terms commute, all other/free monitor adjoints annihilate the algebra, and the own cleanup/z-reset/monitor adjoint is exactly closed. The own monitor is demonstrably not a spectator.

`check_fast_cleanup_monitor.py` constructs a separate 48-dimensional actual-monitor fixture with Q0/Q1/R(Q1), four resource labels, both actual two-level monitors, fast A/Q-style cleanup, actual z-reset, verification, abort drive and complete abort reset. This is a transactional subapparatus regression, not a full-code simulation. It includes all coherences in its 24-dimensional bad space. Results:
- full physical-monitor versus assigned-monitor resolvents: norm difference `1.94e-15`;
- killed resolvent equation residual `7.61e-15`, positive spectrum `[0.76923,2.43666]`;
- omitted monitor adjoint on the resolvent: `5.75e-16`;
- own monitor commutator with the resolvent: `0.8824` (nonzero);
- exact full fast-service identity residual `4.81e-14`;
- no-creation and Hamiltonian flag commutator: exactly zero.

Scripts and full JSON outputs are saved with this receipt. These tests support the explicit general proof; they do not substitute a toy model for the actual generator audit.

## Remaining boundary
The result pays actual dirty flags with fast cleanup and slow acquisition, including coherent malformed masks and nonmonomial partial-payload resets. It does not pay a clean active DATA demand in an uncommitted A/Q/blocked sector. Clean acquisition/service remains open, as do any final native continuous-noise memory threshold and physical noisy preparation/retrieval claims. No old slow-instance constant is reused without recomputing the enlarged finite killed matrix.

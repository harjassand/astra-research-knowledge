# Independent common-model audit: repaired no-epoch multi-lock controllers

Auditor: `audit_guarded_clock_noise`, independent of construction author. Begun 2026-10-29 21:28 UTC. Separate from the completed guarded-clock receipt; no acceptance transfers merely by name.

## Verdict

The actual declared **complete-instrument, ownership-checked, finite-monitor generator** supports commuting quantum owner-history flags, full-space joint no-creation, uniform finite-time local bad-weight contraction, and—through the separately reviewed local-repair theorem—a uniform equal-time sparse owner-defect bound under sufficiently weak bounded finite-range local noise.

One real interface error was found: the original conditional healing theorem demanded individual syndrome-loss commutation, which the actual generator need not satisfy. The physical construction does not need to change. The correct sufficient premise is individual good-range invariance and commutation of the **summed** no-jump loss with the bad projector. The operator/path proof below verifies the bundled premise directly. This receipt does not assert that the old stronger premise was satisfied. Source status and correction are bound in the accompanying hash manifest and correction note.

No data-preservation theorem, DATA fault-path bound, logical threshold, bare physical output guarantee, thermodynamic microscopic realization, or elementary-qubit two-body implementation is accepted here.

## 1. Actual local architecture and general Hamiltonian intertwining

Each physical hub is a finite qudit containing clock and private workspace. Each resource qudit contains its payload and lock. Every displayed term acts within one hub/resource pair or one site; increasing local dimension is a priced assumption, not elementary-qubit two-body synthesis.

Work in a fixed joint clock/lock block. An inconsistent owner's good projector is zero. A consistent A/Q owner's projector is its private workspace-zero projector. A consistent G_t owner's projector is V_t Pi0 V_t^*. Two consistent executing owners cannot share a resource because its single lock would need two different exact owner labels. Thus all nontrivial executing projectors have disjoint data/workspace action; idle projectors are private. This proves commutation without treating non-permutation history projectors as classical variables.

For every Hamiltonian clock edge c->c' with payload U, the correct identity is P_h(c')U=UP_h(c). Acquisition preserves the consistency truth value, including at A_k=G_0, and preserves workspace zero. Verification changes only a condition already true on its edge. Cleanup exchanges o_h and z_h only where the owner does not claim that resource: both are equally forbidden in an unexpected/verified position or equally allowed in a Q suffix. Abort edges connect the original FAILED-test sector to a distinct intrinsically bad R label; their reverse uses the same failed-test projector.

For a program gate, the owner's consistent prefix projector is conjugated exactly by that gate. A different executing owner that shares the target requires a conflicting exact owner label, making the selected gate block zero. Otherwise its projector is disjoint. This is the decisive use of the actual target's ownership projector on EVERY gate. Clock-only monitor couplings also commute. These are full-operator statements valid for arbitrary workspace/data states, not just clean reachable configurations.

## 2. Joint reset no-creation and the discovered hypothesis mismatch

Every individual reset J preserves each owner's good range. Terminal/abort resets put the acting hub in workspace-zero Q0, whose clock predicate is always true. Ready reset preserves the no-own-tags predicate shared by Qk/A0. Own cleanup z_h->f can remove an inconsistency but cannot remove an exact required o_h; other owners see non-own labels both before and after. Workspace refresh and clock monitors have the stated good-range invariance. No reset acts on another hub's private workspace or data payload.

For a commuting product B_S, its kernel is the span of individual good subspaces. Their invariance implies B_S J(I-B_S)=0. Let A=sum_j J_j^*J_j for a complete physical instrument. Its scalar-workspace, clock-diagonal loss commutes with B_S. Then

    sum_j J_j^* B_S J_j = B_S (sum_j J_j^* B_S J_j) B_S
                         <= B_S A B_S = A B_S,

so the WHOLE instrument's adjoint dissipator is nonpositive on B_S. Individual dissipators need not be. Together with Hamiltonian commutation this proves L_clean^*(B_S)<=0 on the full Hilbert space.

**Counterexample to the original stronger hypothesis.** A terminal workspace history |+> has bad projector B=|-><-|. The individually resolved syndrome losses are |0><0| and |1><1|. Their commutators with B are nonzero, opposite matrices with entries +/-1/2. Their sum is I and commutes exactly. The complete reset to Q0 workspace zero has source-block drift -B. `check_bundled_loss.py/.json` verifies this with exact dyadic matrices. Thus replacing an unresolved coherent reset by separately resolved channels is necessary, but does NOT imply each syndrome loss commutes with the history flag.

## 3. Finite-rate arbitrary-state healing

The monitored paths use only a fixed local physical patch consisting of the hub and all its resources, including payload/workspace factors. All terms touching that patch must be included in its local norm B. The paths are:

- failed clock test: unique p->R_(p,j), then complete abort reset to Q0;
- initial R: complete abort reset;
- consistent dirty A/Q: complete workspace overwrite;
- consistent dirty G_t: reverse t gates to A_k, then overwrite workspace.

Every reverse gate is unitary and all required resources are already owned. No acquisition, availability oracle, neighboring rollback, global color ordering, or classical feedback is required. Distinct R destinations exclude cancellation of the chosen abort block. The path selected from the initial clock record is an analytical union of record cylinders of one fixed generator.

The cited CP-Dyson argument uses the SUMMED ordinary no-jump loss, with no off-diagonal block between selected clock positions. It never needs each syndrome loss separately to commute with the history projector. Complete instruments supply uniform reset intensity, including on dirty workspace sectors. Their separately resolved gains are retained. The displayed delta,p0,epsilon estimates therefore remain applicable with the corrected bundled premise. Monitoring resolves only clock/lock positions, not history workspace or data.

For reset monitors, the isolated two-dimensional event Gramian is strictly positive for any positive interval. The preliminary flush removes arbitrary monitor entanglement conditionally; later timing laws are clock-independent, and the whole recorded-instrument approximation costs 4B epsilon per window without an outcome-count multiplier. The selected finite-path probability therefore has positive volume-independent c at finite T, with the stated conservative monitor factors. This is not an infinite measurement-rate argument.

Exact no-creation gives 0<=T_t^*B_h<=B_h, hence the observable stays supported in the bad corner. Uniform selected healing probability on every initially bad-supported state gives T_T^*B_h<=(1-c)B_h. This also handles initial good/bad coherences and arbitrary references. It is contraction of bad weight/test probability, not automatically a classical first-entry stopping-time theorem.

## 4. Application of the local-repair sparse-defect theorem

The actual augmented generator meets the theorem's common-model interfaces: commuting bounded-support B_h, full-space no-creation, fixed finite-time healing, and bounded local strength/range/dimensions. Fixed positive coupling/reset/monitor parameters must be uniform over the family of systems; positivity separately at every site without uniform constants would not suffice.

The local-repair theorem's finite-T polynomial construction, rather than an assumption that T fits one Taylor disk, supplies finite-support F_h in the B_h corner and constants a,b,r with a B_h<=F_h<=b B_h and L^*F_h<=-rF_h. Normalize Z_h=F_h/b and K=b/a. Packing with buffers that include the actual clean/noise support neighborhoods yields, from a clean initial state,

    Pr[all owners in S are bad at time t]
      <= p^|S|,
    p=(K eta_R/r)^(1/P),  K eta_R/r<1,

uniformly in volume/runtime. eta_R measures terms touching the ACTUAL enlarged Z support. Perturbations must be Hermiticity-preserving, adjoint identity-annihilating, locally bounded on the actual retained-system/bath algebra, with legitimate total dynamics. Common retained baths are permitted within those interaction bounds. Physical finite range also needs bounded neighborhood volume/overlap for uniform packing.

This conclusion does not require a global mixing gap or a claim that logical data is repaired when B_h heals. The separately audited polynomial theorem is used as an interface, not re-proved here as a new contribution.

## 5. Regressions, negative controls, and limits

Copied source-identical scripts were replayed in this audit directory, preserving the construction's originals. Results: all 22,680 clock states and 141,561 directed transitions pass; 14 quantum block types, 51 Hamiltonian intertwining types, and 162 joint-reset range checks pass. The quantum test includes non-permutation Hadamard prefixes and overlaps. These finite checks accompany, but do not replace, the general proof above.

The scripts' dyadic entries are exactly representable and matrix sums here remain small; no floating eigenvalue tolerance is being used to accept these algebraic equalities. `check_bundled_loss.py` adds the independent negative test distinguishing individual from summed loss.

The following limitations are indispensable:
- B_h=0 certifies a consistent pending history relative to current data, not correct data.
- A dirty history can damage owned data before healing; reset can erase the flag without erasing that damage.
- Prefix dressing can change bare physical observables, so an output/drain/decoding contract is separate.
- Maintained label-resolved reset/monitor resources and coherent controls remain supplied effective operations; bounded imperfections are perturbations, not a microscopic reservoir derivation.
- Two-site refers to fixed-dimensional hub/resource qudits, not an unpriced elementary-qubit compilation.
- Equal-time sparse owner defects are not a spacetime DATA fault process or a scalable memory threshold.

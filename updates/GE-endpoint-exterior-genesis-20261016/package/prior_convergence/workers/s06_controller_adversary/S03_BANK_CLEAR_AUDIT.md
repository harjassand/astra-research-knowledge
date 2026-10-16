# Audit of the one-use unowned-B terminal clear

16 October 2026. This audits the revised `T` row in s03's `FINITE_DISCHARGE.md`; it is confined to that construction's fixed five-site code block and named one-fault set.

Before `T`, each output bank `B_i` starts in `|perp>` and has no live incoming owner. Let one onsite CP fault have Kraus operators `M_α` on the local pair `A_i⊗B_i`, possibly coupled to classical controller registers at the same site. The classical guards dephase those registers, so each observed controller branch still has a local Kraus operator. The terminal discard of `B_i` gives the induced A-only Kraus family

```text
L_(α,b) = (I_A ⊗ <b|_B) M_α (I_A ⊗ |perp>_B),
b ∈ {0,1,perp}.
```

Every `L_(α,b)` is a one-qutrit operator on `A_i`. The remaining `X_i⊕I_perp` and `C_i⊕I_perp` operations, including any skip/repeat/reorder from the admitted local phase-marker fault, remain on `A_i`. Across the other four tiles the ideal word acts on disjoint data sites. Hence every preterminal branch is a one-site qutrit error after the intended encoded `C_L X_L`. The 31-map Gram/KL construction in s03 spans all such maps on a code input and supplies a fixed recovery. This includes arbitrary reference entanglement; it is a channel statement, not a basis-state check.

The revised `T` channel first traces and prepares all unowned B banks, then applies the prescribed A recovery, moves the recovered code state to B, vacates A, and spends the majority-protected terminal flag. Composition of these CPTP operations is CPTP, and the guard has no raw B-occupancy predicate. A B-only phantom thus cannot block completion. Because `T` is a single fixed-size jump, no intermediate B reset is exposed to another ideal proposal in this finite model. The asserted Poisson service tail is unaffected by the B input state.

The **ownership premise is essential**. If an unknown legitimate packet could arrive in B before `T`, the unconditional discard would erase it; the above reduction would no longer certify the intended multiport operation. The present one-use stage explicitly forbids that arrival. The old `G/H/E` rows act only on A, and there is no B predecessor until this terminal transfer. Likewise, a sole B fault after `T` is corrected only at the separately named final decoder; first acceptance at `T` alone cannot include future noise. A noisy decomposition of `T` at a growing recursive level remains open.

I reran s03's `quantum_recovery_check.py`: its 31 qutrit error images have KL scalar residual `1.18e−15` numerically, and the intended transversal `C_L,X_L` channels have reported order-swap distance `2.828`. The exact correctness rests on the distance-three stabilizer argument and the Kraus reduction above, not floating-point tolerance.

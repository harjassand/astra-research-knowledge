# Independent review: reset-free sign epochs and actual access costs

Verdict: scoped mathematical/interface PASS. This receives the already reviewed sign-pair/epoch results and checks the additional gate, calibration and ordinary-comparator accounting; it is not another novelty or practical-advantage claim.

Source read in full: RESET_FREE_SIGN_EPOCHS_AND_ACCESS_COST.md, initially SHA3a2d595a89f219a960fa9ccce5f22a7b37cc8bdbcc0028843e5835ccf189f1d6. The two requested receiving clarifications were subsequently reread and the final SHA-256 verified as 11650859ab68db273f404b59954054e275e59010511d829d4a2bac7aa54e2c87. Date: 2026-10-31. Those changes explicitly require minimal-ceiling equal subdivision and old private controllers to cease controlling future hardware.

## Received schedule

Actual-state marginal induction is valid without bath reset under the previously reviewed uniform-input one-epoch contract. The final source now uses exactly ceil(Delta/tau) equal pieces per positive user-control interval, so its N bound is earned. It also explicitly makes old private registers idle or traced. These are needed conditions, not merely wording preferences.

The rational threshold, linear-time coefficients and zero-interaction convention agree with the earlier receipt. A dyadic cap in [tau/2,tau] doubles at most the 12b ell C1 endpoint-count contribution, while the existing linear and quadratic estimates cost at most 7b ell C1. Thus replacing 19 by 31 is safe. A tighter quadratic estimate could improve that number, but is unnecessary. Actual jitter must preserve the admitted maximum duration, total time and charged count; the statement does not erase finite-duration switching pulses.

## Exact involution and implementation errors

If an actual acquired system involution U anticommutes with K and commutes with H0, conjugating the positive joint channel by U at both ends gives exactly the negative-interaction channel with the same source generator. The supplied source is untouched. With user controls at boundaries, there are no hidden internal-control conjugations. Conservative cost is two U applications and one private fair bit per epoch; adjacent gates may be optimized only when their actual placement permits it.

For ||U_tilde−U||<=zeta, the unitary-channel error is at most 2zeta, so two boundary operations per epoch cost at most 4zeta and at most 4N zeta overall. This is a statement about the complete acquired operation including any concurrent physical evolution, not a claim that finite pulses are automatically cheap at large lambda. A coin bias a changes the mixture by at most 2|a| in diamond norm. Both constants are correct.

For independently mismatched analog couplings, the direct Hamiltonian Duhamel bound is 2sqrt(lambda)t delta_K per epoch. It is sufficient, not asserted necessary for separately certified centered mismatch. The source correctly distinguishes a boundary-operation error from a continuously amplified Hamiltonian calibration error.

## Mean and compatibility counterexamples

The common source-independent residual mZ produces distance 2|sin(sqrt(lambda)mT)| from the identity channel. If the residual reverses with the coin, the averaged channel instead has distance 2sin^2(sqrt(lambda)mT). These exact qubit formulas justify the different small-angle calibration scalings. They show why average centering is not branchwise centering. The statistical 1/a^2 discussion is explicitly tied to a bounded-observation mean-estimation setting, not a universal acquisition lower bound; exact symmetry can avoid that estimation.

A known mean cannot simply be deleted: its actual Hamiltonian action and altered commutators must be included, and a branch-dependent mean still needs a same-H0 interface or separately paid compensation. The source's received centered-model premise remains binding.

The repetition-code obstruction is correct. For odd length, product Z acts as logical Z and reverses a continuous logical-X drift. It therefore fails the same-H0 negative-branch condition despite reversing conditional-X recovery couplings. Compensation or a changed task is required. An actual product of n single-site Z gates costs up to n gates per U, hence up to 2nN rather than 2N free symbols.

## Strong ordinary recovery comparator

For mutually orthogonal syndrome projectors P_a summing to Q_code, with recovery R_a mapping into the code and R_a†R_a=P_a, the displayed channel has

    K0=P_code+e^{-t/2}Q_code,
    K_a=sqrt(1−e^{-t})R_a.

Its Kraus completeness is exact, and it is the stated recovery semigroup because a successful recovery lands in the dark code. A coherent implementation must retain an environment/syndrome label for the distinct Kraus outcomes while uncomputing other workspace; it must not erase that information unitarily. With this standard interpretation, coherent extraction, partial-jump flag and acquired correction implement the operation. Measured recovery is a separate valid comparator only for a matching output task. Syndrome/decoder/control costs are paid on both sides.

The mixed-output qutrit is a valid example where cold selection does not apply but ordinary Z supplies sign reversal. Its independently certified same-apparatus window is stronger evidence than the earlier floating diagnostics; this access note itself does not relabel a failed sufficient bound as a lower bound. Direct generalized amplitude damping and a small dense solver remain stronger alternatives for their respective logical-execution/prediction tasks.

## Scope

This receipt does not independently re-survey every cited randomized-compiling paper. The source appropriately acknowledges persistent environments, private randomness and coherent-error suppression as ordinary established machinery, and makes no absence-of-prior-art claim. No physical sign-setting device, calibrated pulse, gate backend, universal mean-estimation shortcut, source-output equivalence, or fault-tolerant many-site advantage is acquired by these formulas alone. Final source11650859... is accepted within these explicit conditions.

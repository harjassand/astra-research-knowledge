# Independent algebra audit: enlarged witness subsystem

Scope: sections 6 and 8 of `TANNER_WITNESS_DOWNHILL_CONTROLLER.md`; source combinatorics are outside this receipt. This is an independent derivation, not a certification of the overall memory theorem.

## Finding

The ground-space and conservative distance statements are valid provided H_v is exactly the local check map of the corresponding CSS stabilizers. No coherent-gauge counterexample was found. In fact the potential is gauge-independent after decoding, a stronger and useful formulation missing from the construction text.

## Derivation

Write the two copies in one sector as a_0,a_1 and their binary disagreement as d=a_0+a_1. Choose copy 0 as the control for the data frame. For both sectors let U apply controlled X and controlled Z in one fixed order. Each original data site and four controls form a disjoint five-qubit block. Conjugation is Clifford, and no operation crosses blocks.

For a physical Z check S_Z, conjugation by U attaches the product of Z operators on the chosen X-witness controls on its support. For a physical X check S_X, it attaches the analogous Z-witness product. There are no extra cross-sector factors in these transformed check operators: the factors already attached are Z on controls and commute with the other controlled layer. Changing the order changes possible frame phases, but not these constraint identities.

Under U†, the compatibility equations in the chosen copy partition are original syndrome equations; those in the other partition are the original syndrome equations plus H_v d. Agreement is precisely d=0. Hence all compatibility and agreement constraints reduce to original-code stabilizers and pair equality stabilizers. The exact ground subspace is U(C_original ⊗ K_aux), with K_aux defined by Z_0 Z_1=+1 for each witness pair. Each equality pair has one free gauge qubit. This argument is operator algebra and therefore includes arbitrary coherent or entangled gauge states.

Moreover U† W U is a function only of original stabilizer eigenvalues and pair-disagreement Z_0 Z_1 eigenvalues. It does not depend on the free auxiliary pair gauge values. Thus a diagonal scalar potential inequality established on all these syndrome sectors is an operator inequality also on all gauge coherences; no decohering assumption is needed to establish that extension.

Choose enlarged stabilizer S_ext=U(S_original × S_equality)U† and enlarged Pauli gauge group G_ext=U(S_original × G_aux)U†. A dressed nontrivial logical Pauli E of weight w is conjugated to a Pauli with total support at most 5w. Its original-data component must be in the original stabilizer centralizer and outside its stabilizer group; otherwise E would be gauge. Therefore d_original≤5w. This proves d_enlarged≥d_original/5 (not an optimized factor).

A single witness Z commutes with U and acts as an auxiliary pair gauge Pauli. It is harmless to protected information, though generic errors containing witness X/Y are not. Conjugating a witness flip produces a local Pauli on the decoded data and auxiliaries, as expected; no assumption of classical witnesses is required.

## Controller and barrier caveats

A local branch projector built from witness Z values and physical stabilizer values becomes, after U†, a function of original stabilizers and auxiliary Z observables. It can measure/dephase gauge information, but cannot directly measure protected logical information. The update Pauli remains a Pauli under U†. This excludes a simple logical-frame measurement bug.

The descent/minimum-representative argument is valid on a syndrome branch if its cumulative Pauli correction C satisfies wt(C)<r and wt(CE)<d_enlarged. The fact that CE returns that branch to ground then implies CE centralizes the enlarged stabilizer, hence is gauge by the distance bound. Consequently E is gauge-equivalent to C†, contradicting minimal r. This still requires an explicit basin definition as the span of correctable Pauli error sectors, and does not establish any censored-generator or boundary-leakage estimate.

Nothing here verifies the imported Tanner theorem constants, row/column orientation, physically synthesized jumps, or finite-noise lifetime.

## Executed sanity checks

`check_clifford.py` constructs the full 32×32 matrix of the five-qubit Clifford block and checks transformed X and Z data checks, all four witness-phase operators, both agreement operators, and ground projectors for single-check X and Z examples. Every identity had exactly zero residual in the executed NumPy arithmetic; ranks are four as predicted. The test also explicitly verifies U† X_(X-copy-0) U = X_data X_(X-copy-0): **witness flips are not generally harmless**. `clifford_results.json` retains outputs. These finite checks support the symbolic identities; they do not substitute for the Tanner-family proof or logical-channel preservation along a noisy trajectory.

Optional distance tightening: each disjoint U block contains exactly one original data qubit. A weight-w enlarged Pauli occupies at most w blocks, so its decoded *data component* has weight at most w, although its total decoded support may be 5w. The same dressed-logical argument therefore gives d_enlarged≥d_original for the stated disjoint-block encoding. The construction’s weaker /5 lower bound is safely valid and need not be strengthened for its stated linear-distance purpose.

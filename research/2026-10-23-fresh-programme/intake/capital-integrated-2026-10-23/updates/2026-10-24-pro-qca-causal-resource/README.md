# Related QCA constructions and finite-patch causal-resource witness

This update groups the selected sources for the fixed biased-source QCA construction, its maximally mixed-source tracial companion, and the finite-patch Hamiltonian causal-resource witness. The [source manifest](source_manifest.json) records the selected paths, receipt hashes, capture hashes, source statuses, review scope, and exclusions. The 15 captured source and audit files are retained byte-for-byte under [source](source/).

The two dispatcher receipts remain `IN_PROGRESS`: the 0638 receipt describes individual source reads rather than an atomic tree freeze, and the 0618 receipt describes a producer-workspace snapshot with transport/readback checks. The copied files match the recorded receipt hashes; this does not establish scientific validation or a complete workspace snapshot.

## Fixed biased full-rank source

The [source-dependent counterflow construction](source/chiral_quantum_A/asymptotic_counterfeit/SOURCE_DEPENDENT_COUNTERFLOW_CONSTRUCTION.txt) uses a binary A rail, an optional untouched B rail, odd block size `L = 2m + 1`, and a fixed iid Bernoulli source with `0 < p < 1/2`. Its reversible majority/syndrome block encoder gives the displayed three-layer block circuit

`Omega = S P^{-1} C_left P = P_{+1}^{-1} Pi P`,

with index one and strict quantum radius at most `2L - 2`. For `epsilon_L = Pr[Bin(L,p) > L/2]`, the reported fine-site mismatch against the reference translation is exactly `2 epsilon_L (1 - epsilon_L)`; the label-conditioned errors also vanish exponentially as `L` grows at fixed `p`. The result rules out a source-uniform polynomial tag-error certificate over all fixed positive full-rank source floors in this construction. It is not an arbitrary-QCA lower bound, an all-input or diamond-norm approximation, a full-record total-variation bound, or a repeated-cycle result.

The circuit-depth and preparation costs remain material. Three block-gate layers are not a fixed-time nearest-neighbor implementation: block arity and gate synthesis/clock control grow with `L`; majority requires at least `L - 1` nearest-neighbor depth, and the rotation requires `L - 1` SWAPs. The initial biased source has an extensive entropy deficit, and correlations after a period prevent treating fresh preparation or reset as free. The [uniform-selector audit](source/chiral_quantum_A/asymptotic_counterfeit/luna_circuit_sources/UNIFORM_SELECTOR_AUDIT.md) reports maximum mismatch `1/(2M)` and mean mismatch `1/(2L)` for `M = 2^k` payload bits and `k` header bits, optimal only in its stated block-code/single-countershift class. The [majority audit](source/chiral_quantum_A/asymptotic_counterfeit/luna_one_probe/MAJORITY_ENCODER_MISMATCH_AUDIT.md), [factorization audit](source/chiral_quantum_A/asymptotic_counterfeit/luna_nonnormal/TRACIAL_RECORD_AUDIT.md), and [reversible-CA prior note](source/chiral_quantum_A/asymptotic_counterfeit/physical_sources/SOURCE_DEPENDENT_REVERSIBLE_CA_PRIOR.md) are retained as source dependencies; no novelty claim is made.

## Maximally mixed-source tracial companion

The [tracial companion](source/chiral_quantum_A/asymptotic_counterfeit/TRACIAL_SOURCE_COMPANION.txt) concerns a strict-radius-`R0` QCA on joint cells `A_i B_i`, with dimensions `d_A >= 2`, `d_B >= 1`, `D = d_A d_B`, and an actually maximally mixed product input on both rails. Writing `r = R0 + 1` and `C = 9 + 20 r D`, its threshold is

`E_tr = [ln(d_A)/ln(D)]^2 / [1024 r^4 D^2 C^2]`.

It tests A input at `i - 1` against A output at `i`, and B input at `i` against B output at `i`, over `[-r, 5r - 1]`. If every joint input-label/mismatch rate is at most `E_tr`, the stated QCA cannot have index one. The source does not require one-site translation invariance or an exact A-only channel. At fixed local dimensions the maximum-error threshold scales as `O(r^-6)`; its disjoint-band mean lower bound is `E_tr/(6r) = O(r^-7)`. The explicit uniform-selector construction has `O(r^-1)` maximum error, leaving a lower/constructive gap. The result does not identify every rational index or establish affordable acquisition.

The proof route uses tracial `L2` control instead of conversion through an exponentially small density floor, followed by finite pinching/transpose reductions, a reduced tracial Choi comparison, and imported index/entropy results. The [root polynomial-bound derivation](source/root/TRACIAL_RECORD_POLYNOMIAL_BOUND.txt) is preserved unchanged, including its historical header `Root derivation, 2026-10-24. Independent Sol challenge pending.` The earlier [record-to-Choi opening](source/root/TRACIAL_RECORD_TO_CHOI_OPENING.txt) is also unchanged; its original bridge was preliminary, and its presence does not establish a completed independent proof audit. The retained [tracial record audit](source/chiral_quantum_A/asymptotic_counterfeit/luna_nonnormal/TRACIAL_RECORD_AUDIT.md) covers arithmetic and local reductions only; primary imports remain conditional.

## Finite-patch Hamiltonian causal-resource witness

The [finite-patch witness](source/chiral_quantum_A/hamiltonian_bridge/FINITE_PATCH_CAUSAL_RESOURCE_WITNESS.txt) treats a finite patch `W` of `32 ell` cells, nearest-neighbor bond norm `J`, finite time `T`, and arbitrary onsite controls. It allows arbitrary exterior/bath dynamics subject to charged end bonds and per-cell norm-bounded bath couplings; initial patch/exterior correlations are allowed. The patch input marginal is diagonal product with positive local floors, and drives cannot depend on classical input labels.

Its two-layer block circuit comparison `C` has index one and radius `R_C = 4 ell - 2`; it is a mathematical comparison circuit, not a device operation. The locality and bath terms are

`eta_ell = (2/3) F_ell(6gT) + (10/3) F_(ell+1)(6gT) <= 4 F_ell(6gT)`,

`nu_lambda = 2 lambda integral_0^T (1 + 12gs) exp(6gs) ds <= 2 lambda T (1 + 12gT) exp(6gT)`,

and the comparison mismatch obeys `e_C <= e_actual + eta_ell + nu_lambda`. The prior source-floor threshold is `E_ell = p^(2R_C+1) delta_ell^2/4`, with `delta_ell = 1/[1540 r D(9 + 24rD)]`.

The uniform-source threshold `E_tr` can replace `E_ell` only when the actual patch preparation is maximally mixed and the amended margin `E_tr - eta_ell - nu_lambda` is positive. A mismatch below that positive gap falsifies this specified finite-patch causal-resource envelope. The witness assigns no index to an arbitrary noisy process and does not identify which budget is absent. Norm, dimension, bandwidth, preparation, coupling, and finite-shot budgets have not been acquired; no experiment or practical utility is established. The [interaction-path audit](source/chiral_quantum_A/hamiltonian_bridge/luna_circuit_sources/TIME_DEPENDENT_PATH_TAIL.md) and [noise-Duhamel audit](source/chiral_quantum_A/hamiltonian_bridge/luna_one_probe/ACTUAL_NOISE_DUHAMEL_AUDIT.md) are retained but were not replayed.

## Review scope and relationship to prior handoffs

This source review read the selected biased construction and companion, the central tracial reduction and full derivation, the preliminary opening, the finite-patch witness, and the retained audit notes listed in the manifest. The two selected checker scripts are source dependencies only; neither was executed. No scientific replay, experiment, fresh novelty search, or physical validation was performed. Internal review is limited to the source scope described here; external correctness, novelty, affordable acquisition, and physical usefulness remain unestablished.

The previously frozen [common-filter/QCA handoff](../2026-10-24-u-common-filter-qca/README.md) and the merged [P2/P3 completed returns](../2026-10-24-pro-completed-returns/README.md) remain separate updates; this integration does not edit their source statements. The dispatcher receipts include unrelated material and are not copied in full. No unrelated source tree, evaluator material, private routing capture, or replay output is included.

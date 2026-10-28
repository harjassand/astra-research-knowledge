# Independent primary-import and physical-controls review: finite-time local evolution

28 October 2026. **PASS.** Source:

`ordinary_finite_time_local_evolution_recovery_20261028.md`

SHA256 `d0f308a5edfadea9c709032ffe4753fa36ac0ce6865fefd1efd14c7b75354180`.

The earlier fully read candidate was `6b8ca162e6955e23c64eb636bfcb2db784327c52cbd2cc0bbf44ee2dace0f091`. Two resource precisions were requested: include the inherited `1/gamma` encoder dependence, and make the polynomial-resource statement conditional on a fixed bounded SUPPLIED B, not merely a small actual JT. Both are present in the final source; a loose supplied bound can inflate the chosen width. No primary-theorem, protocol, width, source-budget, or risk constant changed. No source samples, simulations, Hamiltonian-learning calls, or changes to received files were introduced by this review.

## 1. Primary import is independently verified

The separate `nearest_neighbor_hamiltonian_locality_import_controls_audit_20261028.md` records the direct primary inspection of [Barthel–Kliesch arXiv:1111.4210v2](https://arxiv.org/pdf/1111.4210v2), definitions (3)–(7), conventions (8)–(9), shell assumption (13), and Theorem 2/equation (14). Its source-specific receipt and the approximately local theorem receipt are included in this manifest. This is a primary theorem import, not a new proof or historical claim about propagation bounds.

For the stated open-line, edge-grouped Hamiltonian the substitution `a=1`, `1<=Z<=3`, `b<=2J`, `M=2`, graph exponent 1 is correct. The commutator-zero/scalar-phase case is handled separately, avoiding an undefined overlap denominator. Independently bounded onsite terms are not silently included without regrouping and a new J bound.

The source correctly resolves the time-ordering issue using `H_tilde(t)=-H(T-t)`. Its Schrödinger propagator is the inverse of the original propagator; applying the primary Heisenberg convention therefore yields the required `U_H O U_H†`. A simple sign flip without time reversal would be wrong in general. This reversed generator is a proof device, never a physical inverse query or a supplied control.

The theorem is applied to the extended region bar(V), not V. The actual proxy-support interval contains `{y} union bar(V)`, including isolated sites. Proper balls have the exact integer distance D; full-chain and zero-generator cases use exact equality rather than an invalid infinite-distance formula. Boundary clipping and unknown site positions are accounted for.

The truncation is restricted to Hamiltonian dynamics. Unitary conjugation gives exact Hermitian local reflections and a common within-pair Pauli relation, without sign-rounding a dissipative contraction. The proxies remain unknown and are never implemented directly. The operator bound `4D exp(6eJT-D)` implies the weighted bound for every occupied gauge state, so no source eigenvalue floor appears.

## 2. The physical source promise is properly narrower than arbitrary local noise

The new common unitary is `U_H(T) Pi`, where Pi is an unknown injective placement of logical input factors. The Pauli/gauge operation precedes it. The common Pauli/gauge structure, aggregate margins, and global identity dominance remain separate assumptions, not consequences of finite propagation speed. The unitary and assignment are fixed across the four-coordinate encoder family. Reset calls and within-call time dependence are correctly distinguished.

The referenced literal selector family was checked independently: identity branch weights `(1,4/5,3/4,7/10)` imply every Pauli contrast is at least `2/5`, while each nonidentity probability is at most `1-p_I`, proving operator dominance after multiplication by each positive gauge state and summation. The unknown first selector vector gives a perfect encoder. Noncommuting, correlated or ill-conditioned gauges do not change these inequalities. This example has at least one gauge qubit as in its referenced definition; it is not needed to cover the theorem's zero-gauge boundary.

A four-dimensional selector physically uses two input qubits. Their preparation/interface is explicitly charged separately from the q logical inputs. There is no supplied exponentially large Pauli table, known hidden assignment, or free inter-frame alignment. A known-Hamiltonian/known-assignment inverse baseline is correctly described as more informed and must pay its own implementation cost.

## 3. Exact finite width and risk constants

The supplied rational bound B is a bound on JT, not an estimate of microscopic coefficients. Define

`C0=506880*3^12`, `L1=ceil log2(32/kappa)`,

`L2=ceil log2[C0*q/(kappa epsilon)]`,

`D=ceil(36B)+max(18,2L1,L2)`, `w=min(n,2D+1)`.

All positive logarithm arguments exceed one in the inherited integer/accuracy domain. Their ceilings can be obtained by exact rational/power-of-two comparisons. Width is fixed before any outcomes. No Hamiltonian estimation or fitted-tail oracle is inserted.

If w=n, the exact global generators themselves are legitimate full-register proxies with tau=0. This is a separate support choice and is correctly **not** justified by claiming every unknown center's radius-D ball covers the full chain.

Otherwise w=2D+1. The integer bounds used in the source are valid:

`S<=8W^2`, `A<=256W^4<=20736w^4`.

Since D>=4 gives `w<=9D/4`, the last expression is at most `3^12 D^4`. Squaring the operator tail then gives

`Delta <=126720*3^12*(q/kappa) D^6 exp(12eJT-2D)`.

For D>=18, `6 ln D<=D` (the difference is increasing thereafter and the endpoint inequality holds), so `D^6<=exp D`. Further, `D-ln D>=D/2`. With `e<3`, `B>=JT`, and `ln z<=log2 z` for z>=1, the chosen D satisfies both

`D>=12eJT+2ln(32/kappa)` and

`D>=12eJT+ln[C0*q/(kappa epsilon)]`.

The first gives `tau_D<=kappa/8`. The second and `C0=4*126720*3^12` give `Delta<=epsilon/4`. There is no circular dependence on an unknown A: its width-dependent upper bound has been paid in D before acquisition.

Running the received approximately local theorem at `epsilon_stat=epsilon/2` is the correct rescaling. Its comparison multiplies the floor by `1+gamma<=2`, giving

`epsilon_stat+(1+gamma)Delta<=epsilon`.

The stated oracle remains restricted to the supplied encoder family but unrestricted over physical CPTP decoders; the corollary does not enlarge the encoder optimization domain.

## 4. Paid source, control and service ledger

The substitution `eta=epsilon/(32768qA)` follows exactly from using epsilon_stat. Fine m, confidence allocations, operational discrepancy, and global active-encoder tolerance must all use that same rescaling, as the source explicitly requires. The complete cap retains all coarse acquisitions, exact-fill pooled fine banks, actual spectral tournaments, global encoder acquisition, and one payload. The `R_max=1` branch skips all comparison calls and invalid zero-height formulas.

No old holdout or decoder policy is reused. The newly acquired local reflections and newly ordered joint receiver are frozen before fresh global Clifford/stabilizer input tests and inverse-Clifford output readout. Ordinary means no protected source reference; within-input entanglement and the global measurement controls remain paid. Failed localization/estimation histories, physical replacement, finite synthesis and restored routing remain charged under the received contracts.

The proxy Hamiltonians are not compiled. The implemented controls are the **acquired** local reflections, with their width-dependent dense synthesis, q mixed receiver ancillas, three controls and four Hadamards per logical label, and restored routing. The only learned-joint-receiver invocations are the inherited encoder stage plus payload; local tomography and comparisons have their separate extensive controls. The source-call count is not a single-qubit traffic count: q logical input uses and n physical output exposures per call, plus the selector interface, are correctly retained.

## 5. Width-dependent resource scaling is not silently fixed-width scaling

From `4^w<=4*16^D`, ceiling bounds yield

`4^w <= constant * 2^(144B)`

`* max{2^72, (32/kappa)^8, [C0*q/(kappa epsilon)]^4}`.

The extra factors caused by each ceiling are absolute constants. Remaining width polynomials are polynomial in B and logarithms of q, 1/epsilon and 1/kappa. The inherited encoder stage additionally contributes `1/gamma`, explicitly restored in the final source.

Accordingly, for a fixed bounded supplied B>=JT the resource bound is polynomial in q, n, 1/epsilon, 1/kappa and 1/gamma, while the displayed conservative dependence on B is exponential. An arbitrarily loose B can increase the chosen width even when the actual JT is small. This does not preserve the previous fixed-width linear-q statement. If w reaches n, the actual `4^n` cost is paid and lies below the same width envelope; it is not a free full-system decoder. If B itself grows with n, the fixed-B interpretation cannot be used to conceal that growth.

The conventional learner with the same information can use this entire transfer and acquisition method. The argument neither certifies source-family membership nor extends to arbitrary local dissipative noise, non-reset histories, unknown unrestricted encoder families, or a dimension-free untwirled diamond guarantee. The received optional twirl is still an additional changed service.

## 6. Disposition and provenance

All requested primary-import, orientation, truncation, reflection-existence, boundary, exact-width, physical-input, control and resource checks pass. Both requested prose corrections—the explicit 1/gamma resource dependence and the fixed supplied-B qualification—are present in the bound version. No issue remains open in this review scope.

Primary theorem verification and the rational width derivation required no sampled experiment. The source-specific receipt binds this audit, the final corollary, the independent primary-import audit/receipt, the literal source-family document, and the received approximate-local sources/controls receipt. All hashes were checked at binding.

## 7. Narrow rebinding history

The controls review first bound source `bf09ccbb31979b4ad4cdaf727fdabd9e3306aa0aeea8f0af0e3f6913c7ad6e24` immediately before the supplied-bound wording correction arrived. That audit and receipt are preserved byte-for-byte as `ordinary_finite_time_local_evolution_recovery_controls_audit_20261028_pre_supplied_bound_clarification.md` (SHA256 `0fcd8dff2f0a5c12eab291f744619c90e79dcd1b4f105a1fec1952297011b6be`) and `ordinary_finite_time_local_evolution_recovery_controls_receipt_20261028_pre_supplied_bound_clarification.json` (SHA256 `617cc5cd46c439863f0365f9451545e33934ba7170070b3c60e6979bf5f1d929`). The exact previous source is preserved in its corresponding `_pre_supplied_bound_clarification.md` file; reconstructing only the three stated sentence substitutions reproduces its prior SHA256 exactly.

The correction changes only the resource interpretation, not the width definition, equations, protocol or source cap. The current receipt binds source `d0f308a5edfadea9c709032ffe4753fa36ac0ce6865fefd1efd14c7b75354180`. No new source calls, simulations or physical checks were required.

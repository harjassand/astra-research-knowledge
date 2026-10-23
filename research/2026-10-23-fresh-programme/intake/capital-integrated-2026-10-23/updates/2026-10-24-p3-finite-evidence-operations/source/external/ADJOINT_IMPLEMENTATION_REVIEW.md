# Adjoint implementation review

## Finding and scope

**The intended `adjoint_metric_certificate` path is consistent with the
two-sided adjoint identity on inspection. The public generic metric path was
unsound when supplied the adjoint subclasses.** A focused exact-rational
counterexample on the already exposed fixture confirms the latter; this is a
correctness issue, not a scientific failure of the adjoint construction.

This review covers the pre-interface-guard files identified by SHA-256 in
`ADJOINT_GENERIC_API_COUNTEREXAMPLE_BEFORE_REPAIR.json`. The parent owns the
announced guard repair and its post-repair regression. No completed bundle was
modified here. No new literature or benchmark wave was commissioned.

## Confirmed counterexample: public interface accepted the wrong semantics

Both generic `metric_certificate` and `uniform_certificate` accepted
`AdjointRepresentation` and `AdjointCorrelations` through `isinstance` checks.
The generic compiler used `T_a^T` in its upper-left block; the correct block is
`U_a^T`, with `U_a = T_{dagger(a)}`. For two actions, the difference between
the compiled predictions is

\[
e_0^T(T_a^T-U_a^T)D_b e_0.
\]

This can be first order in a fit error while the residual-product allowance is
second order. The tested construction uses exactly the existing three-state
`A B` / `B A` fixture and its exact two-feature representation. Set

\[
v=(T_0-T_1)e_0,\qquad
\widetilde T_0=T_0+\varepsilon v e_0^T,\qquad
\widetilde T_1=T_1,\qquad \varepsilon=10^{-4}.
\]

For the already measured word `(0,0)`, the generic metric path returned
`CERTIFIED_UNDER_CONTRACT` despite exact prediction error

\[
270027/3355443200000000
\simeq 8.04743\,10^{-11},
\]

and claimed uniform allowance about `2.96257e-14`. The exact error is more than
2,700 times its allowance. The adjoint wrapper on identical inputs has zero
prediction error and the same valid allowance: its first left residual is
zero because `T_1` remains exact.

The generic Euclidean path returned `UNKNOWN` on this same case, so no invalid
numerical certificate from that path is claimed. Its static path is nevertheless
unsupported: besides compiling the wrong upper-left block, residual
polarization uses the base `add`, which imposes pure-word reversal rather than
full adjoint reversal.

There is an adjacent mixed-type interface: the base `Representation.certify`
accepted any `Correlations` subclass, permitting selfadjoint forms with adjoint
data semantics. The valid adjoint override checks its map before calling the
shared base implementation. A repair should preserve that override while
rejecting a plain base representation paired with non-base data.

The parent-proposed repair is appropriate: exact-type guards on both arguments
of the public generic uniform/metric entry points; a private shared metric
routine for the validated adjoint wrapper; and a mixed-data guard in the base
per-word method. This review records the pre-repair finding, not a completed
post-repair verification.

## Parts checked and found consistent

- **Word identities.** `star` reverses order and applies the action involution;
  `canon` identifies a word only with its full adjoint. The adjoint form and data
  classes combine coefficients under that identity. Pure reversal is correctly
  absent from the intended wrapper path.
- **Nonsymmetric cross moments.** `inner_form(left,right,(a,))` represents
  `left^T H_a right` without symmetrizing `H_a`. The right residual uses
  `J_R = V^* A_a^* A_a V`; the residual for the dagger action uses
  `J_L = V^* A_a A_a^* V`. The scalar cross term
  `-2 <V T_a z,A_a V z>` is correct in the stated real Hilbert space.
- **Separate recurrences.** The left prefix uses `T_{dagger(a)}` in forward
  iteration order. The right suffix uses `T_a` in backward iteration order.
  The per-word base evaluator receives the overridden forms and does not
  reimpose pure reversal. Its first-order comparison also remains sound.
- **Compiler.** The validated wrapper replaces each upper-left block by
  `U_a^T`. Together with upper-right `H_a-G T_a` and lower-right `T_a`, this
  expands to the corrected predictor. The wrapper currently bounds both
  directions by one maximum contraction and one maximum residual over the
  whole dagger alphabet. This is conservative, not the sharper distinct
  `(r_L,r_R,kappa_L,kappa_R)` version.
- **Metric arithmetic.** The shared metric implementation's local `add` does
  not recanonicalize words. Its matrix inequalities use exact rational
  arithmetic and outward square roots. Taking row/column radius majorants
  controls nonsymmetric defect errors; no symmetry of `H_a` is required.
- **Finite reverse calibration.** The fixture executes the selected canonical
  word and charges `delta * count(reverse_label)` for that executed word.
  Its actual reverse is `(1-delta) A^* + delta P_0`. On the constant subspace
  the perturbation is zero and on the orthogonal complement its norm is at
  most `delta`, since `P_0-A^* = -A^*` there. Thus the stated finite-query bias
  allowance is justified for this authored fixture. The nine pointwise
  inclusion checks alone would not establish that operator bound.

## Remaining contract qualifications

The executable labels in an adjoint representation refer to **ideal** adjoint
actions. Enlarging intervals for approximate reverse acquisition does not
authorize predicting the future approximate reverse process under the ideal
label. The calibrated example correctly requests a true-forward-only target.

Common stationary preparation, the ideal adjoint relation, and the calibrated
finite-query error allowance are supplied warrants. The code does not acquire
or certify them. An obtainable physical operator-error certificate remains
`UNKNOWN`. These qualifications are already separate from the finite-data
algebra and are not repaired by additional authored examples.

## Exposure and evidence

The implementation, the exact fixture, the theorem, and the parent's 22-check
receipt were visible before this review. Those 22 checks were inspected, not
rerun by this worker. One focused same-fixture counterexample was executed.
Its target was deliberately short and measured, so an erroneous certificate
could be falsified exactly. There is **no independent transfer evidence** here.

Reproduction: `ADJOINT_GENERIC_API_REPRO.py` reads the current files by default;
`--archived` loads the parent's `*_before_interface_guard.py` backups. The exact
pre-repair outputs and hashes are preserved in
`ADJOINT_GENERIC_API_COUNTEREXAMPLE_BEFORE_REPAIR.json`.

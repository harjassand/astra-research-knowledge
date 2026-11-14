# Independent delivered-rounding and archive-dependency audit

## Confirmed defect

With the delivered flags `-O3 -std=c++17 -frounding-math -ffp-contract=off -fno-fast-math`, I independently compiled the minimal quotient probe and compared exact hexadecimal values with Fractions. For ALL three delivered activities201/200,101/100,51/50, the nominal UP quotient equals the DOWN quotient and is strictly BELOW the exact rational. The same occurs for41/40 and11/10. Storing the quotient in a volatile variable does not prevent common-subexpression reuse. This breaks the stated uninflated upper-weight contract. Small moment tests can still pass because later positive rounding masks the input underestimate.

Exact receipt: `check.json`. No frozen archive was edited.

## Repair review and tests

Radical's single-mode repair sets FE_UPWARD once and separately computes upper bounds on r and1/r from volatile operands, then forms both powers only by positive upward multiplication. This avoids changing mode around an identical expression. Each local weight is an upper bound by induction. The magnetic recurrence and binary scale updates are then monotone under the inherited no-overflow contract.

I separately compiled the repaired weight-table arithmetic and checked ALL positive and negative powers through951 for five rational activities against exact Fraction powers:9520 bounds pass. I separately compiled the DELIVERED convolution source and checked48 coefficients/tail sums, including both marked/unmarked modes and nondyadic decimal input conversion, against exact rational convolution. All dominate their exact answers. These checks are independent of radical's11-ratio full-moment tests and do not replace general arithmetic reasoning.

Correction to my initial scalar review: radical identified that a lower logarithm was multiplied under global CEILING before subtraction. I had missed this sign-sensitive intermediate. The repaired scalar explicitly computes that product under FLOOR. I independently recomposed all949 coefficient inputs using220-digit outward arithmetic and2847 exact moment hex values; every repaired input dominates this reference, and the repaired110-digit complete upper dominates the independent220-digit complete upper. See final_scalar_check.json. Separately, the949 ORIGINAL numeric coefficient inputs also happen to pass the same higher-precision comparison (old_scalar_actual_checks.json); this is a finite check, not rehabilitation of the original generic expression proof. Hex parsing, per-perimeter minimum, positive logsumexp, rational tail Taylor denominator and direct lower-log subtractions otherwise have the correct direction. No extra mode-switch/CSE issue appears in the convolution, which sets UP once. This is not a proof of the Decimal implementation or all compiler semantics.

A separate NEW direction-independent backward-error correction in `BACKWARD_ERROR_REPAIR.md` can preserve the rounded e^-6215 statement while waiting for full replacement runs, under its explicit finite IEEE operation contract. The original uninflated moments still must not be reused as if their upper status had been proved. Preferred repair is regeneration and scalar re-evaluation from the single-mode kernel.

## Earlier occupation archives are independent of this defect

Inspected these frozen package trees:

- `north_star_finite_occupation_closure_20261113`:233 files including manifest;232 file hashes pass.
- `north_star_all_four_occupation_closure_20261113`:249 files;248 hashes pass.
- `north_star_winding_sector_partial_20261113`:196 files;195 hashes pass.
- `north_star_two_axis_sector_partial_20261113`:168 files;167 hashes pass.

None contains C/C++ source, `fesetround`, `FE_DOWNWARD`, magnetic_upper, moment_201_200, or the marked s79/40 magnetic receipt in its code/document/receipt dependency tree. The executable capacity references point instead to the older `n1722_optimized_cut_capacity_20261113` exact-rational script/JSON. Its operative bounds are exp(-1548),exp(-4136),exp(-21502),exp(-217281), not exp(-6215). Its proof arithmetic uses Fraction, finite Taylor inequalities and rational logarithm bounds; diagnostic float fields are not used as bounds.

Thus the discovered magnetic CSE defect does NOT propagate into these earlier occupation certificates. Their original topology/proof/arithmetic assumptions remain, and this audit is not a reproof of every occupation lemma. All four manifests verified without modification.

## Later dependent work

The delivered global-cut package, above-field area-window receipts, common-area-tilt receipt, and any later gate-weight moment using the old mode-switch initialization need either regeneration or the separately paid backward-error inflation. Pure integer pair-partition and old rational occupation receipts do not depend on those moments. Do not silently replace a frozen package or its hashes; publish a separately versioned correction when authorized by the parent.

## Final repaired receipt verdict

The three complete magnetic activities were regenerated with the single-mode kernel and zero under/overflow flags. The repaired coefficient inputs, convolution and all complete scalar terms pass the independent checks above. The fresh complete upper is at most exp(-6215.66191582971263732051369...), so exp(-6215) survives. This is a corrected independently checked result; the delivered original enclosure proof was defective. No frozen archive was overwritten.

### Portable package location map

The independent220-digit check is `independent_scalar_check.py/json`. The quotient and repaired-kernel receipts are `compute_quotient_check.json` and `compute_repair_checks.json`. Alternative backward-error inflation and old-scalar retrospective checks are review context, not dependencies: this archive relies on full fresh regeneration and its directly included independent check.

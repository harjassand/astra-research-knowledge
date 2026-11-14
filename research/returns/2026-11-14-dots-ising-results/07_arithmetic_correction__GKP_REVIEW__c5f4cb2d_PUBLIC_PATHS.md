# Independent arithmetic review

Reviewer: north_gkp. This is a new review, not an alteration of any delivered archive.

## Single-mode rerun

Read `magnetic_upper_single_mode.cpp` and `convolution_upper_checked.cpp` in `n1722_magnetic_arithmetic_repair_20261113`. The replacement computes upper r and upper reciprocal r from volatile operands under ONE upward mode, then uses only positive products and sums. This removes the demonstrated cross-mode common-subexpression defect. The arithmetic argument is valid subject to the stated actual compiler/platform contract, not merely the presence of a pragma.

Gradual underflow under genuine FE_UPWARD preserves the upper enclosure: every strictly positive result below the minimum subnormal rounds to at least the minimum positive subnormal. An underflow flag therefore does not itself invalidate this corrected convolution. The startup test of half the minimum subnormal is relevant; no overflow is permitted. Positive decimal input conversion must likewise respect upward rounding.

Independently compiled the checked convolution with the recorded flags and tested three inputs, including `1e-4950` and `1e-4960` (the latter smaller than the positive long-double minimum). All eight marked powers for each input dominate their EXACT rational counterparts. Both tiny cases raise underflow and still retain valid positive upper outputs. `check.py/json` contains 24 exact comparisons. This tests actual conversion and subnormal arithmetic, rather than inferring safety from normal final outputs.

## Direction-independent repair of old output

Read quantum's `ROUNDING_INFLATION_REPAIR.md` and reran `repair_old_marked.py`. The power error must include the initially rounded quotient once PER power factor. Its exponent 2h+2 is safe. Each target/direction has one predecessor coordinate, so the positive recurrence does not hide a large summation depth. The proposed total B=2(M+2)^2 dominates the stage, closing-sum and scaling allowances at M1900. Recorded absence of inexact underflow in magnetic recurrence remains an explicit requirement; power tables themselves are normal at the delivered activities.

The convolution repair separately charges absolute underflow. With at most950 weights below1, coefficient propagation through at most eight stages has norm at most951^8<2^80. Marked final summation costs at most15201<2^14; q<.019 cannot amplify it. Fewer than2^32 operations and an extra factor2 for normal-error propagation give absolute loss below 2^(-16445+32+80+14+1), vastly below the chosen 2^-10000. This assumes IEEE gradual underflow and the recorded extended format; flush-to-zero is not covered by that tiny absolute bound. Normal coefficient summation depth plus Horner depth is below100000, including input parsing and repeated q use.

Thus, under those explicit hardware facts, both corrections are sufficient. The repaired scalar rerun gives log upper -6215.661915829711079..., preserving the integer e^-6215 conclusion. This does NOT validate the old uninflated per-perimeter values as upper bounds. Fresh single-mode full re-execution remains the preferred independent receipt.

Compute's looser magnetic backward-error repair also passes the normal-operation power/depth argument. Its downstream invocation of the old convolution requires either the single-mode upward contract or the separate absolute-underflow allowance above; it must not rely solely on absence of a convolution underflow log.

## Scope

This review checks arithmetic only. It does not strengthen the analytic contour envelope, acquire the large rejection sampler, close W/C, or silently restore prior archive claims. The source, target, clock and positive tail terms are unchanged.

### Portable package location map

The reviewed repaired kernels are packaged as `../01_global_cut/magnetic_upper.cpp` and `../01_global_cut/convolution_upper.cpp`. The24-case test is `subnormal_convolution_check.py/json`. The alternative inflation discussion above is historical context and is NOT a dependency of this corrected archive: this archive uses full single-mode regeneration, not inflation of old outputs.

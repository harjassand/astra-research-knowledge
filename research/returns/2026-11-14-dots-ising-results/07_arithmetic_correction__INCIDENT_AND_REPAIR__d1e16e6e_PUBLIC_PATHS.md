# Directed-arithmetic defect and repair status

## Defect

The delivered global-cut archive used `magnetic_upper.cpp`, which switched FE_DOWNWARD to FE_UPWARD around two identical integer-to-long-double divisions. On the actual compiler with the documented flags, common-subexpression elimination reused the downward quotient for the intended upper quotient. A volatile RESULT did not prevent reuse of the division's nonvolatile inputs. The pragma and -frounding-math flags did not justify the claimed enclosure across those switches.

The minimal `rounding_cse_probe.cpp` reproduces this at r=11/10: both original quotients print `0x8.cccccccccccccccp-3`, while a fresh division of volatile operands under UP prints the larger `0x8.ccccccccccccccdp-3`. The original magnetic recurrence consequently underbounds the exact perimeter-four moment at this test input. The earlier three-input small checks did not detect this defect.

This invalidates the GENERAL numerical enclosure argument used for the delivered global-cut calculation. It does not by itself prove that the three particular delivered large outputs lie below their exact values, nor that the rounded e^-6215 headline is false. That headline must not be treated as revalidated until a corrected complete computation passes.

The source copy from the delivered ZIP is preserved as `magnetic_upper_delivered.cpp`; the delivered ZIP is not silently overwritten. Only the global-cut ZIP includes this magnetic recurrence. Earlier occupation ZIPs use separate analytic/exact/Decimal arguments; independent dependency checking is requested rather than presumed from chronology.

## Repair

`magnetic_upper_single_mode.cpp` maintains FE_UPWARD throughout. It computes an upper bound for r and an upper bound for 1/r separately from volatile numerator/denominator inputs, then builds both power tables by positive multiplication under UP. No lower table, downward division, reciprocal of a lower power or rounding-mode transition remains. CSE of repeated expressions under the SAME rounding mode is harmless. All subsequent dynamic-programming operations are positive upward adds/multiplies and exact binary scaling, as before.

The software contract still requires the stated binary arithmetic/compiler behavior. It is not a formal proof assistant certificate. The actually tested platform has64 mantissa bits and passes the rounding-mode check. No claim is made for a platform merely because it accepts these flags.

`check_single_mode.py/json` independently compares exact Fraction moments with the repaired compiled program for11 rational activities through perimeter20, including all delivered activities and the failing11/10 test. Every repaired output is an upper bound. Small tests support, but do not replace, the one-rounding-mode positive-operation proof.

The three original perimeter1900 activities were fully regenerated in the repair folder, not into the delivered archive. All three reported no underflow or overflow. Complete scalar/convolution/source/target/tail calculations were rerun with a separately checked single-mode convolution implementation. The corrected log upper is -6215.6619158297126373205..., and the rounded exp(-6215) headline survives. This does not rehabilitate the original general enclosure proof. Stronger area-window and new gate implementations require their own checks.

An additional scalar expression was hardened: a positive multiple of a lower logarithm is now explicitly multiplied under ROUND_FLOOR before subtraction. This avoids relying on incidental next-minus slack. The actual convolution run reported no underflow/overflow; runtime tests explicitly check upward and gradual-subnormal behavior. The repaired magnetic program explicitly requires the actually tested64-bit mantissa. The guard-only compile change produced a binary identical to the one used for the large reruns (SHA256 a4f6f5a626a8aa348dac263beda947961630016da9e2026aba4ad5b93fa2cf8a).

## Implications for other new work

Pure translated-flow capacity LOWER receipts use independent Decimal/integer calculations and are unaffected by this C++ division defect. Their combinations with global W, including e^39.845 and e^37.534, depend on the respective repaired W upper and must remain conditional until its revalidation. The large-instance proposal identity is algebraic, but its numerical normalizer and acceptance guarantees also depend on corrected upper receipts.

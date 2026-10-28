# Acquired two-factor target/phase extension

This directory contains the continuation's E6 counting consumer, its proof,
independent checks, and retained failures. It removes the requirement that
the two nonzero target carriers coincide. The existing actual-algebra and
one-joint-simple-copy requirements remain. All affine phases are admitted.

The underlying finite E6 flag classification is classical. The new result
is the explicit finite-field census and its integration after the recovered
raw Boolean-circuit acquisition, with original-input reconstruction and
paid recognition, arithmetic, and output costs.

## Files

- `TWO_FACTOR_ARBITRARY_TARGET_PHASE_THEOREM.tex`: governing proof, scope,
  descent argument, exact orbit weights, reconstruction, costs, and evidence.
- `e6_phase_counter.py`: explicit 29-type catalogue, fixed Hom table,
  positive geometric census, signed histogram, and ordinary-DAG compiler.
- `e6_phase_audit.py`: independent finite-field subspace and local-matrix
  oracles, actual raw acquisition, original-gate checks, and formula growth.
- `e6_catalogue.json`: explicit prototype dimensions/maps, base-grid
  restrictions, statistics, and Hom table.
- `e6_phase_audit_results.json`: all executed checks, native acquired
  certificates, count data, and 32 positive original-input assignments.
- `e6_distinct_targets_native_n72.json`: the exact original ordinary circuit.
- `e6_formula_growth.json`: explicitly formula-only growing-field execution.
- `recovered_diamond_replay.json`: fresh replay of the recovered 256-phase
  control, including all 54 previously rejected phases.
- `audit_failures.md`: the corrected target-shift error in the new audit
  harness; production admission correctly rejected the malformed target.
- `SAMPLING_CONDITIONING_OBSTRUCTION.tex`: a legal single-bit condition can
  make the inherited semisimple multiplier algebra nonsemisimple.
- `AFFINE_SECTION_INDEPENDENT_REVIEW.txt`, `review_affine_section.py`, and
  `affine_section_independent_review_results.json`: independent review and
  actual-gate coefficient certification of the acquired affine right inverse.
- `e6_complete_pipeline_audit.py` and its `_results.json`: one raw acquisition
  reused by the E6 counter, all-target affine section, and description-admitted
  generic exact sampler; literal original-gate and exported-prefix checks.

## Reproduce

Keep this directory under `new_work/phase_constructive` alongside the
continuation's `recovered_source` directory. The production module imports
the recovered code read-only and suppresses bytecode writes there.

```sh
python e6_phase_counter.py e6_distinct_targets_native_n72.json --output native_replay.json
python e6_phase_audit.py
python e6_complete_pipeline_audit.py
```

The second command refreshes this directory's audit data and fixture. It
does not edit recovered sources. The native fixture has 72 independent
inputs and 24,635 gates. Its exact count is 71,228,562,270,584,832, independently
reconstructed as `64734 * 2**40 + 12 * 2**42` by the left-input/right-linear
oracle. The old diamond consumer rejects its distinct target carriers.

The exact geometric census visits at most `(k+1)**19` fixed-type
multiplicity profiles. This is a charged polynomial with a large exponent,
not a claim of practical superiority. The ordinary-circuit fixture also
fits the previous 256-character fallback. No uniform sampler for the full
E6 family, unrestricted circuit-counting theorem, or civilisation-level
capability is claimed by this result.

The complete-pipeline integration audit freshly acquired this same native
circuit once, then reused its certificates. E6, generic character, and prefix
counts all gave 71,228,562,270,584,832. The section witness and two exact-sampler
draws passed a separate literal interpreter of the 24,635 gates; the exported
acquired prefix equations were satisfied on the original 72 input bits. The
generic sampler was invoked only after checking `2**8 = 256` against both the
actual 2,040,317 file bytes and the 783,932 compact circuit-description bytes.
The recorded run took 16.950 seconds for recognition plus E6 count, 0.003 seconds
to construct the affine section, 0.059 seconds for sampler coordinates and
character preprocessing, and 2.584 seconds for two draws; total 19.663 seconds.
This establishes the complete actual pipeline on the small-codimension
fixture. Its sampler still costs `2**c` times a polynomial, and this audit does
not establish polynomial sampling for the growing-codimension E6 family.

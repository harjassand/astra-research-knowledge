# Complete fresh preprocessing cost

Both frozen instances were rebuilt from source graph JSON in this isolated
parallel directory. Screen, exact producer, and C++ source copies are
byte-identical to the originals. Their original relative paths were preserved,
so no source edits or path substitutions were required. Inputs, copies and
measurement-script hashes are recorded in `SOURCE_COPY_MANIFEST.json`.

No statistical sampling was performed in this replay. The original producer,
arrays, samples, seeds, confidence intervals and precommit files are unchanged;
`postrun_frozen_hashcheck.log` confirms the frozen manifest after the replay.

## Full preprocessing measurements

Each subprocess measurement includes Python imports, reading inputs, actual
floating construction or exact production, compilation where applicable,
compression, and output writing. Floating construction preceded exact
production for d13, and then for d21.

- d13: floating screen 10.915051676 s; exact producer 8.225011571 s.
  Sum of full stage times: 19.140063247 s.
  Continuous preprocessing wall time including launch/record overhead:
  19.141101465 s.
- d21: floating screen 145.246582517 s; exact producer 41.816707964 s.
  Sum of full stage times: 187.063290481 s.
  Continuous preprocessing wall time including launch/record overhead:
  187.065831040 s.

The d13 largest single-process peak was 113,604 KiB. The larger sampled
aggregate process-group peak was 173,672 KiB, because Python and the compiler
can coexist. For d21, the largest process peaked at 607,712 KiB and the largest
sampled aggregate group peak was 606,628 KiB. Sampling can miss the exact
instant of a peak, hence the latter may be slightly lower.

Every stage exited successfully. Neither distance approached the joint
20-minute preprocessing or 2-GiB aggregate resident-memory cap. Memory was
checked every 25 ms; this is a sampled monitor, not a kernel memory cgroup.
Linux wait4 supplies whole-child CPU accounting and the kernel-recorded
largest-process peak over waited descendants.

## Exact reproduction

For both distances, U.npy, J_lo.npy, J_hi.npy, distance.npy, W.npy and starts.npy
have equal shape, dtype, values, and SHA-256 bytes to the frozen arrays.
Exact Z, exact conversion TV, N, D, Q, q denominator/numerators, boundary
distances, and the producer's certificate fields are equal. These checks are
in `d13_equivalence.json` and `d21_equivalence.json`.

## Sum with separately measured acquisition and production

These are sums of complete stages from different runs, **not one uninterrupted
acquisition-to-production benchmark**:

- d13: prior full graph acquisition 3.196498230 s + fresh preprocessing
  19.140063247 s + prior full fixed-production process 27.656357260 s
  = **49.992918737 s**.
- d21: prior full graph acquisition 15.540504860 s + fresh preprocessing
  187.063290481 s + prior full fixed-production process 30.156478802 s
  = **232.760274143 s**.

Using the continuously measured preprocessing wall instead changes these sums
to 49.993956955 s and 232.762814702 s, respectively. All source records and
scope details are listed in `COMPLETE_COST_ACCOUNTING.json`.

The d13 acquisition timing comes from the earlier complete fresh-setup replay.
Its 137,492-KiB memory figure is the largest child over that entire earlier
pipeline, not an acquisition-only measurement. The d21 acquisition-only replay
records 205,520 KiB largest-child peak and 205,512 KiB sampled process-tree peak.

File-copy preparation, pre/post hash checks, equivalence comparisons, scientific
review and test-development work are not included in these operational stage
sums. Exact producer certification and compiler execution are included.
Nothing here establishes a universal runtime advantage. In particular, a
smaller exact normalizer does not imply lower fresh preprocessing or equal-shot
wall time; d21's complete cold cost is material.

## Files

- `measure_fresh.py`: capped subprocess runner and exact reproduction checks.
- `combine_resources.py`: joins already recorded costs; launches no computation.
- `d13_preprocessing_summary.json`, `d21_preprocessing_summary.json`.
- `d13_floating_screen_resource.json`, `d13_exact_producer_resource.json`, and
  corresponding d21 records; matching `.log` files preserve subprocess output.
- `SOURCE_COPY_MANIFEST.json`, both equivalence records, and frozen hash checks.
- Copied source/graph directories and their complete fresh outputs are retained.

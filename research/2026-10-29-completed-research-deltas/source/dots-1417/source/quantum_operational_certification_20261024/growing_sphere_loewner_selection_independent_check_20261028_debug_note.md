# Check-script implementation note

28 October 2026. When changing the independent test's medoid rule to the manuscript's FIRST fixed-radius qualifying center, its initial Python implementation tried to sum SymPy BooleanAtom objects. Both attempted runs stopped at that line with `TypeError: BooleanAtom not allowed in this context.` The prior JSON remained on disk and was not treated as evidence for the changed rule.

The fix casts each exact Boolean comparison to a Python bool and then an integer before summation. No numerical rule, threshold, matrix fixture, source input or sample was changed. The corrected script was then executed twice under `set -e`; both runs completed and their newly written JSON files compared byte-identically. All data in this check are deterministic prescribed matrices and exact moment sums. Zero source calls or RNG draws occurred before, during or after the code repair.

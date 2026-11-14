# Corrected-edition executed validation

The three perimeter1900 magnetic recurrences were fully regenerated using single-mode upward powers. Runtimes were107.958,108.613,116.720 CPU seconds; all underflow/overflow flags were zero. Complete unmarked and marked scalar/convolution bounds were regenerated. The checked convolution explicitly tests upward and subnormal behavior; the actual convolution runs recorded zero underflow and overflow.

The corrected complete marked log upper is -6215.6619158297126373205..., retaining exp(-6215). Exact repaired-recurrence checks cover11 rational activities through perimeter20, including11/10 that falsified the old implementation. Original model, source and proposal definitions are unchanged.

The earlier archive remains preserved and superseded, not silently replaced. Its operational clean-copy checks did not detect the arithmetic defect. The corrected edition passed a fresh default disposable-copy runner, including all broad moment checks, exact proposal and coefficient reconstruction, original clock and inherited thermal test. Independent compute review recomposed all949 coefficient inputs and the complete scalar at220 digits from2847 exact hex moments; every input enclosed its independent value and the full bound retained the correct direction. Independent GKP review tested24 convolution cases including1e-4950 and1e-4960, which correctly round upward even with underflow. Both reviews are included. Final archive extraction/manifest verification is requested separately after freeze; it is not inferred from these runs.

The final portable runner including the independent220-digit scalar and24-case subnormal convolution tests completed successfully before freeze. Manifest verification remains a separate archive-level check.

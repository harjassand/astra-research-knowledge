# Verification and limits

All four scripts completed successfully with assertions enabled. Source scripts are byte-exact copies. The manifest verifier and runner use portable relative paths.

- Exact refined example: q=16/101; 10 nonzero refined correction Kraus operators; exact weighted-Kraus Choi identity and residual trace completeness.
- Exact bath witness: c=99/101, s=20/101; bad effect diag(0,400/10201); squared norm distance 4/101; unequal good-filter squared singular values 1 and 9801/10201. Rank-one Choi support rules out every positive common CPTP bath-channel minorant.
- Floating-point illustration: two-frame residual approximately 2.09×10^−15; refined minimum residual eigenvalue approximately −1.01×10^−17, consistent with roundoff; unrefined residual approximately −0.12885. The latter negative eigenvalue illustrates the failure repaired by refinement; it is not a failed theorem check. The source numeric script prints diagnostics rather than asserting tolerances.
- Microscopic enumeration: 524,288 correction configurations, 245,760 monotonicity cover pairs and 6,291,456 face-fault configurations; zero failures.

The final ZIP is also extracted into a fresh temporary directory and the manifest plus all four scripts rerun there. Package-level success establishes file integrity, portable execution and the reported finite certificates. It does not independently verify every general proof step, the external contour theory, a numerical threshold or hardware performance.

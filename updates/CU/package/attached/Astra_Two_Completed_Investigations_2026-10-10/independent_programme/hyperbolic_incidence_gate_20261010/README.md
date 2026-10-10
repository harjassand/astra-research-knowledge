# N06 fixed incidence and link gate

The one scoped investigation is complete. The advertised fixed-parameter gate is proved; no repair was needed. The proof supplies the simultaneous random event, all finite bounds, correct puncturing/interpolation, Cartesian blocks, and the actual link immersions and rectangle turns.

Read PROOF.md for the full argument and its remaining dependencies. STATUS.json records the exact disposition; SOURCE_MANIFEST.json pins every recovered source. exact_checks.py is a self-contained Python standard-library replay; results.json is its completed output.

Run: python exact_checks.py --output results.json

The bound is P(reject) <= (128*r/c + 5)/q < 2e-73 at h=20, c=10^-40, r=10^42, q=2^521-1. It yields deletion of at most 6q^13 labels, at most 6q^14 newly exceptional points, N >= cm/4, |E| <= m/(2r), regular degree >= 4r^2, and Delta >= 15m/4.

This is a closed lemma obligation, not independent certification of the entire nonsofic theorem. The astronomical incidence data were proved to exist and were not physically acquired. The downstream permutation obstruction and sofic reduction remain at their previous scope. No new direction is opened by this package.

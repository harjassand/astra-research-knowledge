# Independent research handoff: rare multistage transformations

Pinned Astra source revision: `5489b118101275c81500d823361592c670ec77bb`

Start at `PROOF_AND_SCOPE.md` for the complete proof, precise access and cost contracts, primary-source links, exact source revision and SHA routes, strong comparators, counterexamples and scientific scope. This is an independently constructed research note; all generated data are synthetic. No peer-role drafts were consulted.

## Files

- `test_compiler.py` / `results.json`: 40-stage boundary-kernel compiler, 80-state generator baseline, same-information O(N) comparison, confidence/design and hidden-route falsifiers.
- `latent_memory.py` / `latent_memory_results.json`: a full spectral/moment-fit alternative that loses usable conservative decision precision in the selected rare example.
- `composed_ctmc_trials.py` / `composed_ctmc_results.json`: actual 300-state killed CTMC with hidden trap dynamics and persistent modes, 160,000 independent native Gillespie short assays, raw reaction time, 99% action decision and a stronger-information explicit-generator oracle check (not an equal-data comparator).
- `task_only_decision.py` / `task_only_decision_results.json`: four short-assay 99%-confidence all-length action ranking for two persistent latent modes.
- `identical_shorts_counterexample.py` / `identical_shorts_counterexample_results.json`: exact rational observational equivalence of two distinct three-mode systems with opposite long-run action preference.
- `three_mode_falsifier.py` / `three_mode_falsifier_results.json`: a separate exact rational three-mode sign-reversal falsifier.
- `hankel_and_contamination.py` / `hankel_and_contamination_results.json`: exact fourth-moment Hankel rank calculation, 10^-9 hidden high-persistence mode counterexample.
- `theorem_stress.py` / `theorem_stress_results.json`: randomized finite theorem stress checks (no violations, not a proof).
- `SOURCE_MANIFEST.json`: hashes and sizes for package files (created after all research files).

Requirements for main experiments: Python 3.10+, NumPy, SciPy. Pure-rational counterexamples require only Python standard library.

**Key status:** Conditional theorems and executable synthetic tests; no physical qualification or general scientific breakthrough established. A classical exact-milestoning/CTMC comparator ties the first compiler; an ordinary task-focused test can implement the sign rule once its structural theorem is supplied.

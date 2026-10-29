# Reproduce

From the audit directory:

```sh
python independent_checks.py
(cd author_replay && python check_random_code_moment.py && cmp check_random_code_moment.json ../source_snapshot/check_random_code_moment.json)
sha256sum -c SHA256SUMS.txt
```

Independent tests use Python, numpy and sympy. Sympy calculations are exact;
floating twirl checks and the author Haar Monte Carlo diagnostic are supplemental.
The audit imports no source script. All writes remain in this directory, never in
the original packet. Dependency source paths and hashes are recorded separately
in dependency_snapshot/DEPENDENCIES.json and the receipt. Finite compiler/learner
proofs are received by these interfaces, not claimed as executed software here.

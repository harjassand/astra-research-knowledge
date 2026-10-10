# Polynomial-orbit finite determination

Complete proof candidate, 9 October 2026. Internal mathematical check only. External validation, formal verification, and priority remain unresolved.

## The proposed result

For one polynomial update F in n variables and a polynomial output h, the candidate gives a coefficient-uniform, primitive-recursive bound on the number of consecutive initial zeros of h(F^t(a)), unless every term is zero. It includes singular points and dimension-collapsing maps. The proof is self-contained apart from standard elementary facts about irreducibility, projection, and Bézout degree bounds, whose use is explained.

With d = max(1, degree F), e = degree h >= 1, set

- Delta_0 = e, T_0 = 1
- T_(i+1) = (Delta_i + 1) T_i
- Delta_(i+1) = Delta_i^(n+2) d^((n+1) T_i), for i = 0,...,n-1

If the first nonzero output has finite index L, the candidate proves L <= T_n - 1. Consequently, zero outputs at all indices 0,...,T_n-1 certify all-time zeroness.

## Read first

1. proof/COMPLETE_PROOF_CANDIDATE.md: the full return-device construction, dimension descent, degree recurrence, endpoint, and scope.
2. checks/FOCUSED_MATHEMATICAL_CHECK.md: what the single completed internal mathematical check examined.
3. comparison/PRIMARY_COMPARISON.md: precise boundaries against Novikov–Yakovenko (1999), rational-recursive sequence work (2023), OPS difference elimination (2019), and Clemente (2025).
4. proof/COMPUTATIONAL_SCOPE.md: encoding, exact evaluation, and the distinction between a theoretical bound and a usable algorithm.
5. proof/OBSERVABILITY_BOUNDARIES.md: supporting examples separating finite equality, polynomial realization, and uniform-in-time robustness.

## Reproduce the small exact checks

Python 3.12 and SymPy 1.14.0 were used. In a suitable Python environment, install the pinned dependency with `python -m pip install -r requirements.txt`, then run `python checks/verify_boundaries.py`.

The script uses exact integers, fractions, and symbolic polynomial reduction. It rewrites checks/boundary_verification.json and prints the same results. Saved checks cover singular observable identities, dimension collapse, reducible guards, and a Boolean-counter exponential lower example. They do not verify a general theorem. The saved result was reproduced without alteration during packaging; the reproduction record gives hashes and versions.

## Essential limits

- This is a complete candidate, not an externally established theorem or a claim of historic priority.
- The tower height grows with dimension. No elementary bound uniform in dimension is obtained.
- The resulting rational-input decision procedure is primitive recursive in bit complexity, with no practical-efficiency claim.
- The target is whether every output is zero. This is not the Skolem problem of whether an arbitrary later zero occurs.
- The proof applies to one fixed polynomial map. Arbitrary control words, unrelated transition choices, and general partially defined rational maps are not covered.
- The primary-source comparison is scoped. It does not exclude an equivalent theorem or corollary elsewhere.

## Provenance

comparison/SOURCE_MANIFEST.json lists the exact primary URLs and the sections used in the supplied comparison. No local primary-source byte snapshots were available for this package, so their byte hashes are explicitly unavailable; none are invented. SHA256SUMS.json authenticates the actual packaged files, not the external papers.

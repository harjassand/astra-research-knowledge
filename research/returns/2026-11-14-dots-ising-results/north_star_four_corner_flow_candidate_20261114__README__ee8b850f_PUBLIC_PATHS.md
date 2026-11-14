# Four-corner Ising flow: reusable candidate construction and review

**Research candidate, not peer reviewed or fully machine-checked. Not the North Star solution.**

This archive preserves an explicit entropy-carrying physical flow, executable finite tests, directed scalar arithmetic, an independent mathematical review, and the prior corrected global-cut dependency needed to interpret the result. It is a substantial reusable mathematical partial construction. It is not an efficient rare-event sampler, a practical transition-time predictor, or a hardware result.

## Exact scope and conditional claim
The finite tuple is theta=4, R=200, phi=4/R=.02, L=1600, n=2,560,000, original augmented-component core radius r=5, epsilon=.01, and the original per-site rate-one heatbath clock and soft-source kappa. The target is physical pluscount n/2. Energies use the stated normalization relative to all-minus.

Four independently weighted Ferrers corner partitions of side d=132 define physical monotone spin-addition paths, with K=265 and M=600. The partition normalization is acquired by a positive recurrence, not supplied by a sampler oracle. A proposed overlap decoder bounds core-edge multiplicity by 2(d+1)^2=35,378. Prefix, merge, late growth, cross-phase overlap, thermal normalization and the shared reservoir edge are explicitly paid.

**Conditional on the geometric/overlap argument and stated original-model dependencies**, the directed scalar receipt yields

    C_kappa / Z_A > exp(-6267).

Combined with the included corrected cut certificate W_cut/Z_A <= exp(-6215), this gives

    W_cut / C_kappa < exp(52).

The directed quadratic receipt's normalized upper is approximately 0.574273, strictly below one. The more conservative cubic decoder receipt gives exp(57). The independent review also discusses a sharper 2d(d+1) decoder; **that sharper value is not used in the headline scalar**.

exp(52) is approximately 3.83 x 10^22. It remains enormous. These are upper bounds, not measured costs or proof that actual cost equals that number. In particular, the result does not establish polynomial work uniformly in growing R, a full original-model decision-time estimate, or manageable proposal acceptance/runtime. No large channel ensemble was enumerated and no R200 channel sampler was run.

## What has and has not been checked
- Native-weight floating finite tests: R=2,d=1 and R=4,d=2; actual spin geometry, path endpoints, neighbor counts, prefix bounds and numerical conservation.
- Exact integer conservation diagnostics: the same small geometries with q=1/2. This diagnostic law is **not** the native R=4 importance law. Native energy calculations in those tests remain floating.
- Independently implemented active-corner enumeration: d=1 through 5, maximum one-direction multiplicities 2,6,12,20,30. This is not exhaustive full-torus or asymptotic proof.
- Directed arithmetic: positive Fraction/Decimal enclosures for the specified formulas, including original-clock and thermal factors. Executing the script is **not** independent verification of every arithmetic argument or Python implementation.
- Independent review: general decoder reasoning, actual R200 geometry, thermal-normalization algebra and recovered original clock/core inputs. It is an AI-produced independent review, not external peer review or a formal proof assistant certificate.
- The supplied prior global-cut package contains corrected arithmetic and its validation history. Its default checks use saved large magnetic-moment receipts; only its `--full` option recomputes the large recurrences.

The general geometry proof, accurate source interpretation and physical-to-resistor-network derivation remain mathematical dependencies. Exact-random-bit implementation of transcendental channel weights and full large-instance acquisition/runtime are not supplied. The finite thermal bound is not asserted uniform as n grows at fixed temperature.

## Read in this order
1. `research_notes/capacity_resume_20261114/FOUR_CORNER_FLOW_CANDIDATE.md`
2. `research_notes/radical_structure_20261114/FOUR_CORNER_INDEPENDENT_REVIEW.md`
3. `research_notes/capacity_resume_20261114/four_corner_directed_scalar_degree2.json`
4. `research_notes/capacity_resume_20261114/R200_STREAMING_AND_NORMALIZATION.md`
5. `DEPENDENCIES.md`

The construction note preserves its chronological derivation. Early sections saying the scalar is uncertified are superseded **only for arithmetic of the stated formulas** by its final directed-arithmetic section. They are not superseded into a fully verified theorem. The independent review's original internal source locators are historical provenance; `DEPENDENCIES.md` maps them to included portable files.

## Reproduce without network access
Requirements: Python 3.10 or newer, standard library only, enough RAM for the finite d=5 enumeration. The dependency checks additionally require g++ with C++17 and supported directed floating-point rounding. No pip packages, credentials, private services or network access are required.

From this extracted directory:

```sh
python run_checks.py
python run_checks.py --with-cut
```

The runner works in a temporary copy and does not overwrite distributed receipts. The second command also executes the corrected global-cut package's default checks. Neither command regenerates its large R200 magnetic recurrences. To do that additional work explicitly:

```sh
python dependencies/global_cut_corrected/run_checks.py --full
```

Do not interpret the local finite tests as verifying all R200 channel configurations. See `VALIDATION.md` for what was actually rerun during packaging, and `validation_stdout.txt` for the exact log.

## Integrity and historical dependencies
`SHA256SUMS.txt` hashes all distributed files except itself. Hashes detect changed files, not mathematical errors. The prior corrected global-cut package is included intact, apart from omitting Python cache files. Its old lower bounds and attempt-count statements are historical; the candidate new lower bound is distinguished above and must not silently be treated as adopted in that older package.

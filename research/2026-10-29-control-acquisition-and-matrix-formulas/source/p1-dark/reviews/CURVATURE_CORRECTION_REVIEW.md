# Focused review of the curvature fallback corrections

28 October 2026. This follows the two P2 findings in `CURVATURE_REVIEW.md`.
The corrected implementation and runner were read directly and exercised by
`reviews/curvature_correction_checks.py`. Exact results are saved in
`reviews/CURVATURE_CORRECTION_CHECKS.json`. The five main acquisition cases
were neither rerun nor modified by this review.

## Disposition

**Both reported P2 paths are corrected in the reviewed versions. No new
invalid certificate was found in these focused checks.** Numerical proposal
failure now leaves the exact certificate path available; a nonpositive
acquired polynomial no longer prevents a valid conductance certificate or
a compliance tangent at an independently positive point.

### Numerical curvature proposal

Injected `numpy.linalg.LinAlgError` and NaN eigenvalue outputs both select
the rational Gershgorin fallback, record their failure, and pass the exact
strict matrix checks. A deliberately inaccurate finite zero eigenvalue
proposal for the known Hessian diag(2,0) is rejected on the first attempt;
the second rational attempt succeeds with mu>2. Thus finite proposal error
and failure to obtain a proposal are both covered.

The separate floating polynomial-data setup also degrades safely. A very
large exact constant polynomial causes floating coefficient conversion to
overflow while its rational Hessian remains zero. Exact curvature
certification still succeeds, `float_proposal_failure` is populated, and
the optional optimizer retains the existing finite command. This is an
arithmetic stress test, not a hardware dynamic-range specification.

### Nonpositive polynomial and optional optimization

The exact conductance upper bound now uses p directly and does not demand
p>0. The compliance bound sets `j0=baseline_lower` when p<=0 and uses the
unsimplified constant `-2/j0+p/j0^2`. Its curvature and error allowances
are scaled by the same `1/j0^2`. This agrees with the general positive
tangent proof; it does not silently clip p inside the simplified formula.

The checks construct strictly positive node intervals containing the exact
constant source J=1, while the acquired interpolant is respectively negative
or exactly zero at a legal DAC20 command. All 12 combinations of these two
cases, two utilities and three prices produce valid exact certificates.
Because the true source is constant and the cost is linear, its continuous
global optimum is known exactly; the checks compare against that optimum,
not only against sampled actions. These interval stress cases establish the
fallback's algebraic behavior, not a replay of physical receiver calibration.

Optional compliance optimization explicitly rejects nonpositive polynomial
values. Injected optimizer `LinAlgError`, NaN command output, negative p and
zero p all retain the initial DAC command and report an unsuccessful optional
proposal with zero source readings.

## Existing candidate and bound preservation

The actual corrected runner was exercised on a disposable synthetic
constant-source interval record, not on the five saved main cases. Two
scenarios were tested, each with six tasks:

1. An injected eigenvalue NaN and optimizer exception. The rational curvature
   fallback succeeds; the initial command is retained and the failure is
   recorded in the saved runner output.
2. An injected eigenvalue NaN and an optimizer result with `success=False`
   but a finite command. The finite result remains an optional candidate,
   receives an exact certificate, and is not accepted on its stopping flag.

In all 12 runner tasks, the old candidate lower bound and old global upper
bound remain in the comparison. The resulting regret bound is no worse
than the previous bound, encloses the exact continuous optimum, and applies
to a legal DAC20 command. The disposable input record is unchanged, and
the runner records zero additional source readings and zero acquired source
gradients. Actual numerical execution of a physical command remains outside
the review.

## Historical reproduction remains intact

`reviews/curvature_review_checks.py` now explicitly loads
`reviews/historical/polynomial_curvature.py` by file path and checks its
historical SHA-256. It hashes the historical runner rather than the corrected
runner and requires the unchanged simplex/hypograph dependency hashes. It
therefore still reproduces the original `LinAlgError` and nonpositive-value
assertion. The current entry point has been run successfully after this
change.

The byte-original old probe, old results, old implementation and old runner
in `reviews/historical/` remain unchanged. In particular the original probe
hash is `230046652a3b0718fe4319947e4f68e66d1d008ea3f996840017ca14e66ba7a8`.
The corrected-code checks are a separate file and do not rewrite historical
failures as if they had passed originally.

## Exact reviewed correction versions

Hashes were recorded before testing and verified unchanged afterward.

| File | SHA-256 |
|---|---|
| `code/polynomial_curvature.py` | `8b6d3bf18f603ec5da058cdf61c8905bc560d7dfe6afe860fe29092486c67b24` |
| `code/run_curvature_refinement.py` | `fe54463b99151c7884fda99682f735ad1e3581c5c127bd3ae4a274f37c8da56b` |
| `code/simplex_law.py` | `2ac69c52818d31b741f165bf6cb50fba5d990f14cd2ae6cedef5b4be1043505d` |
| `code/hypograph_control.py` | `3416567cd6079ef387bed376b5ac46742782fe2a6b96bd2edc8d14c0652294e9` |

This is a scoped post-correction implementation review. It does not certify
all future inputs, floating environments, source-law assumptions or the
complete research proof, and it is not an independent whole-proof audit.

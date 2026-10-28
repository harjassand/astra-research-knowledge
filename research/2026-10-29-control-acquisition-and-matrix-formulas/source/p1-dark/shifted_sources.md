# Sources and provenance for the shifted-reference branch

Read 28 October 2026.

## Governing Astra source

Pinned revision: `edfd18c223a49de697744a4437aa639fa70c23ee` of
https://github.com/harjassand/astra-research-knowledge .

The N1082 governing file was read directly from the saved source copy:
`../p1_next/sources/computation/N1082_governing.md`, especially sections 5.1
(generic illumination and signed exact transfer), 5.2 (reported finite exact
dark-source instance), and 6 (bounded-error excitation failure).

Its source path is
`research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-chemical-frontiers/source/global/ASTRA_PRO3_GLOBAL_RESPONSE_ACQUISITION.md`.

The prior reported 510-call numerical files remain UNACQUIRED here. The
small shifted execution in this directory is newly written and does not
relabel them as reproduced. No independent whole-proof audit was identified.

The prior noisy acquisition and signed-reference limitation were read from
`../p1_next/theory/NOISY_ACQUISITION.md` and
`../p1_next/selection/computation.md`. The current lattice proof and code
were read from this directory's `theory/SIMPLEX_LAW_ACQUISITION.md` and
`code/simplex_law.py` for the separately saved scoped Bernstein review.

## Strong conventional comparison

pyMOR's current official CoerciveRBReductor/CoerciveRBEstimator documentation:
https://docs.pymor.org/2026-1-1/autoapi/pymor/reductors/coercive/index.html
describes residual dual-norm estimation and requires an appropriate
coercivity lower bound for a guaranteed upper error estimate. That is the
relevant conventional comparison: certified reduced models account for
stability, rather than obtaining a reliable extrapolator merely from exact
algebra. pyMOR normally has richer operator access than this one-port scalar
protocol; both acquisition and computational access must be priced fairly.

The previously read primary active-PSD-completion source and working pivoted
Cholesky implementation remain relevant:

* Bhargava, Ganti, Nowak, Active Positive Semidefinite Matrix Completion,
  https://proceedings.mlr.press/v54/bhargava17a.html .
* Chen, Epperly, Tropp, Webber, Randomly Pivoted Cholesky,
  https://arxiv.org/abs/2207.06503 .
* Existing implementation,
  https://github.com/eepperly/Randomly-Pivoted-Cholesky .

Their entry/matrix interfaces are not free native scalar observations. An
equally informed conventional interval active-Nystrom/shifted-Woodbury
implementation can adopt the same acquired conversions, coercivity checks,
raw-error envelopes and cache rules. No priority or universal advantage is
claimed for the algebraic components here.

The new signed-resolvent and excitation arguments in this directory are
ordinary proofs supplied in full, not attributed to an unavailable external
audit. The exact code checks have their stated finite scope.

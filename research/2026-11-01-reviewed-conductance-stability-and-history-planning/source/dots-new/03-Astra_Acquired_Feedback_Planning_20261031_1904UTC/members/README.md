# Local scientific checkpoint: acquired-block feedback planning

The separate whole independent review is a conditional PASS, bound to the
exact 39-entry feedback freeze. Its receipt is included at
`two_rate_operator_acquisition_20261031/feedback_extension/INDEPENDENT_FEEDBACK_REVIEW.md`
(SHA-256 de32bcd24f3c11e64cc85cb66c29abf600f0baba1da85b405cfae7f2a0111c26).
The original frozen README still says review pending because it was written
before that receipt; the later bound receipt resolves that status, without
changing any frozen source bytes.

The useful result is a polynomially acquired sufficient operator-family
certificate enabling ordinary exact coarse-MDP Bellman planning for finite-
horizon acquired-block Markov feedback. n4096/r4/m2/L24 fixture: uniform
value error 0.0144023063, within-class regret 0.0288046127. Compatible-goal
reuse executes 16 DPs/64 initial-block tasks without new observations.
Physical sensors, hidden-state inference, microscopic/history-policy
optimality, historical novelty and practical speedup are NOT established.

All costs and unsuccessful work remain paid: 3,298,951,680 represented source
calls (aggregate simulation, not individual billion-query execution);
1,454,285,782 cumulative norm-acquisition integer products including the
historical exponential attempt. Current polynomial norm work is 146,865,304
products; receiving repeats 279,363,350. Original-goal DP uses 768 products
and reaches 669-bit integers. The map/policy/task interface occupies 2060
packed bytes in addition to the 468-byte coarse model and all certificates,
observations, metadata and state registers. Ordinary retained reduced-MDP
methods using this acquired certificate obtain the same planning capability.

Confidence is conditional on externally authentic iid source outcomes,
nonanticipating sampling schedules/supports, genuinely fresh independent
probes and source validity. Exact replay checks their finite-data algebra;
it does not authenticate these premises or give posterior-on-PASS coverage.

## Reproduction

Preserve this directory layout; use Python 3 with NumPy and SymPy already
installed, assertions enabled. Frozen environment: Python3.12.14, NumPy2.3.5,
SymPy1.14.0. No network, installation or equipment is needed.

```bash
export PYTHONDONTWRITEBYTECODE=1
python two_rate_operator_acquisition_20261031/feedback_extension/replay_polynomial_feedback.py --output producer-workspace/feedback_reproduction.json
python two_rate_operator_acquisition_20261031/feedback_extension/compatible_goals.py --output producer-workspace/feedback_goals_reproduction.json
python - <<'PYTEST'
import sys
sys.path.insert(0,'two_rate_operator_acquisition_20261031/feedback_extension')
import check_feedback_algebra, check_comparison_failure
print(check_feedback_algebra.run())
print(check_comparison_failure.run())
PYTEST
```

## Scope/allowlist

FILE_MANIFEST.json and SHA256SUMS bind every payload file, including this
README. All scientific originals are verbatim. The copied dependency subset
is sufficient for these replay commands; the earlier source freeze/receipt
reference additional historical/comparator files that are preserved in the
separate companion `Astra_Acquired_Routing_Certificate_20261031_1832UTC.zip`,
not duplicated here. Its hash is
0d7c200947fc4f08f2f230155637c23220e814bb57ca4e220cc823a35ecaa06e.
No claim is made that this feedback receipt independently re-reviews every
older file or that references to omitted historical files are new payload.

Excluded: post-freeze open-loop comparator and other ongoing research;
all caches/logs, administrative/private files, unrelated branches, older
archives, cloud/user-note paths. Local-only preparation; nothing uploaded.

The verbatim REVIEWER_RECEIVING_PROBES.py is preserved review evidence with
a workspace-specific path, not a portable command in this README. Its cached
negative-test scope is explicit and never replaces the full current replay.

# Reviewed local addendum: all block-observation history policies

Separate whole PASS receipt:
two_rate_operator_acquisition_20261031/history_policy_extension/INDEPENDENT_HISTORY_REVIEW.md
SHA-256 0704da790a4f4ab203e679fb992f91e9cd275c286f73f718701aa183691e0766.
The frozen author documents still use candidate/pending-review language
because they precede this bound receipt; their bytes are preserved exactly.

## Earned result and limits

The same acquired Markov policy now has a certified comparison against all
policies using the entire observed-block/action history and independent
private randomness, under the unchanged explicit-state simulator interface.
The proof combines unrelated child continuation vectors using paid acquired
block norms; it neither conditions on rare-history probabilities nor assumes
a surviving spectral contraction. No history controller or belief estimator
is stored/executed. Microscopic-state policies and physical sensors remain
outside scope; an exact one-step counterexample preserves that distinction.

For the original n=4096, r=4, m=2, horizon=24 task:
- history-uniform VALUE error: 0.04210299756104081; requested tolerance .05;
- chosen Markov-policy error: 0.014402306334221847;
- regret against the block-history class: 0.05650530389526265.
The value tolerance .05 is NOT a .05 regret guarantee.

No new observations or norm probes. Prior acquisition and unsuccessful work
remain paid, including 3,298,951,680 represented (aggregate-simulated) source
calls. Full receiving repeats 279,363,350 norm products and 768 Bellman
products. The new capped recurrence has a 78-bit acquired common denominator,
99 products and a 1,948-bit measured peak; lcm/gcd/comparisons/input work are
additional. Repeat testing/review incurs further verification work. The same
2,060-byte packed map/policy/task masks and 468-byte coarse model remain,
plus all counts/certificates/metadata/registers.

Independent checks include 9,806 inherited exact checks, 12 inherited and
11 new refusals, 1,132 exhaustive small-tree checks, 11 microscopic-limit
checks, 25 integer-backend checks, plus 480 independent unequal-block/three-
action randomized-tree checks and 18 additional task/alias refusals.

The source/probe iid, freshness, nonanticipation and unchanged-world premises
remain external; JSON and seeded fixtures do not authenticate them.
Historical novelty, best-method superiority and practical advantage are not
claimed. Ordinary retained coarse-MDP methods given this acquired certificate
obtain the same capability. The executable fixes the original task and
requires external reward/initial inputs; it does not silently implement the
proof's generic future-task frontend.

## Companion dependency and reproduction

Use with Astra_Acquired_Feedback_Planning_20261031_1904UTC.zip, SHA-256
c92b777c3edfc2fef64fa2fa8ae0aea2b40b0fa5eb16eb582830e55b3f07502d.
The scientific paths merge without changing any existing scientific file.
This addendum's metadata has its own HISTORY_ADDENDUM_META directory, so it
also preserves the companion's README/manifest. Exact dependency hashes are
listed in ORIGINAL_ALLOWLIST.json and the frozen scientific manifest.

```bash
export PYTHONDONTWRITEBYTECODE=1
python two_rate_operator_acquisition_20261031/history_policy_extension/receive_history.py --output producer-workspace/history_reproduction.json
python - <<'PYTEST'
import sys
sys.path.insert(0,'two_rate_operator_acquisition_20261031/history_policy_extension')
import check_history_trees as t, check_microscopic_limit as m, integer_history_trace as i
print(t.run()); print(m.run()); print(i.run())
PYTEST
```

Python 3 with installed SymPy/NumPy, assertions enabled; no installation or
network needed. Reviewer extra scripts are preserved verbatim review evidence
with their original path assumptions. They do not replace full receiving.
Excluded: ongoing AIS/prior comparison, status notes, caches/logs, unrelated
branches and all private/admin files. Local-only; nothing uploaded.

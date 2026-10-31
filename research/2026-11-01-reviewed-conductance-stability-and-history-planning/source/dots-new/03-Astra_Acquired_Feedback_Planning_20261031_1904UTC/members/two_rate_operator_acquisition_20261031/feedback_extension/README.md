# Acquired-block feedback planning — separate frozen scientific checkpoint

**Current useful result:** a sampled/acquired polynomial sufficient certificate
supports ordinary exact finite-horizon coarse-MDP planning, uniformly over
all acquired-block time-dependent Markov policies. It also supports new
compatible block rewards/initial laws without new source observations.
No new Bellman algorithm, historical novelty, strongest-baseline superiority,
practical advantage, physical sensor or hidden-state policy capability is claimed.

This directory is separate from the accepted 18:24 large-acquisition freeze
and local routing ZIP. Its source freeze is submitted for its own independent
review; only a separate bound receipt can establish that review's result.

## What to read

1. `PROOF.md`: interface, feedback leakage, uniform policy-value guarantee,
   paid Bellman regret, finite-bit and sensing/lookup scope.
2. `BLOCK_COMPARISON_PROOF.md`: acquired m r² norm geometry replacing the
   historical m^r family; explicit incompleteness counterexample.
3. `PRIOR_MATCH_AND_COSTS.md`: primary literature, explicit old L2-testing
   rate reductions, equally informed retained comparator and full ledger.
4. `replay_polynomial_feedback.py` + `polynomial_feedback_received.json`:
   final externally bound count/probe/DP/interface receiving, using only the
   prespecified polynomial error certificate (not minimum of two norms).
5. `compatible_goals.py` + results: 16 executed new goal DPs, 64 initial-block
   tasks, 833 checks, zero new observations; conditional on received operator
   event, not a replacement certificate verifier.
6. `check_feedback_algebra.py` and `check_comparison_failure.py`: 214 small
   exact checks and the seven-check exact sufficient-certificate failure.

`check_feedback_norms.py`/`feedback_norm_results.json` and
`plan_feedback.py`/`feedback_plan_results.json` preserve the paid historical
explicit-policy-family construction and its trusted-generation diagnostics.
The latter is NOT the final externally bound polynomial receiver. Its tighter
error value must not be substituted into the current polynomial result.

## Observed fixture and honest costs

n4096, learned r4, two actions, horizon24, epsilon .02, delta .001.
Current uniform value error 0.014402306334221847; within-class regret bound
0.028804612668443694. Coarse optimal original-task value approximately
0.6244843518542954. Reported exact rationals, not decimal displays, define
its certified interval. The current receiver passed 9806 exact checks and
12 adversarial preflight rejections. Fresh iid/nonanticipating sampling and
fresh independent probes are external premises, not authenticated by JSON
or mock seeds. False-admission confidence is unconditional, not posterior
confidence conditioned on a rare PASS.

3,298,951,680 represented source calls remain paid; aggregate multinomial
simulation is not actual billion-query execution. Additional polynomial
norm work is 146,865,304 sparse integer products. Including original norm
work and discarded exponential-family attempt, measured norm acquisition
is 1,454,285,782 products. Current receiving replays 279,363,350 products.
These are not total elementary operations; projections, big-integer/PSD/lcm,
serialization, memory and source execution are additional. Original-goal DP
costs 768 products, reaching 669-bit integers; all 16 goal DPs cost 12,288.

The complete original packed map/policy/task masks occupy 2060 bytes,
ADDITIONAL to the 468-byte coarse model and all certificate/count records,
metadata and registers. `block_map.bin` is 1024 bytes, policy is 12 bytes,
and each original task mask is 512 bytes. Future 16 policy tables need 192
packed bytes and their 16 four-bit goal vectors need eight bytes (computed
and hashed in results, not extra binary artifacts). A simulator must retain
its microscopic label and pay transitions and map/action lookups. Future
uniform block initials can be sampled by rejection with expected four
uniform-state draws/map lookups here; rare blocks incur the real penalty.

## Nonmutating reproduction

Use the directory structure of this workspace or the eventual strict local
archive. Python 3, SymPy and NumPy are already present; no installation or
network is needed. Run with assertions enabled (not `python -O`).

```bash
export PYTHONDONTWRITEBYTECODE=1
python two_rate_operator_acquisition_20261031/feedback_extension/replay_polynomial_feedback.py \
  --output producer-workspace/feedback_received_reproduction.json
python two_rate_operator_acquisition_20261031/feedback_extension/compatible_goals.py \
  --output producer-workspace/feedback_goals_reproduction.json
python - <<'PY'
import sys
sys.path.insert(0,'two_rate_operator_acquisition_20261031/feedback_extension')
import check_feedback_algebra as a, check_comparison_failure as f
print(a.run())
print(f.run())
PY
```

The first replay takes roughly one minute here; timing is not a theorem or
benchmark promise. It reads retained counts and stored probes without source
calls. The goal command consumes the current bound received artifact; it
is not standalone receiving. Saved elapsed-time fields can differ.

To rerun norm generation without overwriting originals, import the relevant
module, set only its `ROOT` to a fresh temporary directory and call `main()`;
its `PARENT` remains the scientific dependency directory. This regenerates
mock-seeded stored probes, not authenticates their provenance. Historical
explicit enumeration is much costlier and is not required by current
polynomial admission; its existing records remain included for the ledger.

## Bound dependencies and exclusions

`FEEDBACK_FREEZE_MANIFEST.json` lists each exact source/result byte hash,
with a separately identified dependency section. The accepted parent
mixed-norm, leakage, matrix concentration/norm-probe proofs, repaired source
replay, observed history counts, action model and imported exact PSD/replay
helpers remain unchanged. Their earlier receipt covers only those earlier
versions, not this feedback extension. The earlier source freeze also
preserves unsuccessful rounds and strong open-word comparisons; no refunds
or weaker cold-start baseline are used here.

Logs, caches, administrative/private files, unrelated branches and previous
ZIPs are not part of the source allowlist. All work is local only.

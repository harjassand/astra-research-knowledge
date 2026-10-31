# Separate history-comparator theorem — new source freeze

Root authorized a separate whole review. This directory is NOT covered by
any earlier receipt or archive. The final independent receipt, if produced,
must bind this exact new version. No earlier scientific original was edited.

## Useful candidate result

The acquired residual-block geometry can dominate unrelated continuation
value functions in each child of an observation-history tree. This avoids
assuming an inherited spectral contraction or dividing by rare-history
probabilities. The same ordinary Markov Bellman policy is then compared
against ALL block-observation/action-history policies, including randomized
ones—not microscopic-state policies or hidden physical sensors.

On the unchanged n4096/r4/m2/L24 source, the new bound is
E_history=0.04210299756104081, using kappa=1.0314396616974182 (>1 honestly)
and a capped recurrence. Combining with the previously received chosen-
policy error0.014402306334221847 yields candidate regret0.05650530389526265.
The new requested VALUE tolerance is .05, not the old .02 Markov tolerance.
All source/probe provenance premises are inherited, not authenticated anew.

## Actual receiving and tests

- `receive_history.py` calls unchanged full polynomial receiving:9806 exact
  checks and12 old preflight rejections. Its own11 external history-interface
  rejections bind original reward/initial masks, denominator, horizon, action
  count, confidence and new tolerance. Original-task prototype only.
- `check_history_trees.py`:1132 exact checks of all deterministic observation
  trees through horizon3 for balanced and unequal blocks, including value,
  residual and coarse Bellman/regret checks.128 trees per initial block at
  the final depth, with independent continuations in both child blocks.
- `check_microscopic_limit.py`:11 exact checks; microscopic action selection
  improves a one-step value from1/2 to11/20 even though every block-history
  policy agrees exactly with the coarse model. That scope restriction is real.
- `integer_history_trace.py`:25 exact checks of a common-denominator backend;
 99 recurrence products,78-bit common denominator,1948-bit peak integer.

No new source observations or random norm probes. Full receiving still
replays279,363,350 norm products and repeats768 Bellman products; earlier
3,298,951,680 represented source calls and all failed acquisition work remain
paid. Repeat test/review runs add their verification work, not free evidence.
The same2060-byte packed original map/policy/task interface and468-byte coarse
model remain; no history tree, belief estimator or new sensor is stored.

## Nonmutating commands

Python3/SymPy/NumPy already installed, assertions enabled. Preserve the
workspace layout and all frozen feedback dependencies.

```bash
export PYTHONDONTWRITEBYTECODE=1
python two_rate_operator_acquisition_20261031/history_policy_extension/receive_history.py --output producer-workspace/history_received.json
python - <<'PY'
import sys
sys.path.insert(0,'two_rate_operator_acquisition_20261031/history_policy_extension')
import check_history_trees as t, check_microscopic_limit as m, integer_history_trace as i
print(t.run()); print(m.run()); print(i.run())
PY
```

For a nonmutating callable full replay, use
`receive_history.run(**receive_history.fixture_task())`; the callable requires
explicit expected reward/initial task inputs. `fixture_task()` reads the
public task from the separately pinned original model artifact. Calling
`negative_checks()` executes only the cheap expected refusals.

The mathematical theorem covers compatible block tasks; this executable
intentionally refuses any task different from the pinned original prototype.
A future-task frontend has not been silently inferred. There is no historical
novelty or end-to-end practical superiority claim. Ordinary same-information
retained coarse-MDP methods using the acquired certificate obtain this result.

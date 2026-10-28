# Preserved development failures

1. First `test_pilot.py` run reached the final JSON writer after all numeric assertions had passed, then raised `TypeError: Object of type bool is not JSON serializable`. The conditional second-moment comparison produced a NumPy boolean. Fixed only JSON conversion by explicitly casting its ratio to Python float and pass flag to Python bool; all tests rerun. No pilot acquisition file changed and no new stochastic source calls were made.
2. An attempted independent-review subagent spawn was rejected by the collaboration thread limit. The parent reassigned an existing reviewer instead. No additional code or source operation occurred.

Pilot acquisition failures are individually preserved in every run’s `failures.json` (all empty). The runner records source-call counts and aborts, rather than silently restarting a trajectory, on exceptions.

# Exact negative-control correction

The first local receipt named the m=8, eta=4/5, p=q=2/5 case `fails_singleton`, although its asserted and returned status was EXACT. This was a weakly chosen negative control, not a counterexample or a false reported value. Version v0001 preserves both executable and receipt unchanged. The current script renames it `high_eta_exact` and adds m=2, eta=9/10, p=q=49/100. The new case asserts a positive tangent gap and CERTIFIED_BRACKET, detecting a singleton witness that fails full optimality. The analytic theorem is unchanged.

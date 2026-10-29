# Stronger conventional policy: test overhead need not scale with block length
2026-10-29. Root algebraic consequence of the accepted zero-failure hazard bound; pending separate review. This qualifies fixed-R comparisons, not the matching theorem.

For witness coefficient C, service probability s and test probability1-s, R=C s/(1-s). With zero permitted failed tests and correction of t bad service blocks, accepted bad-event probability is bounded by [R/(1+R)]^(t+1). Fix target delta in(0,1). The largest service probability permitted by this bound is exactly

 s_star = 1/[1+C (delta^[-1/(t+1)]-1)].

For an ideal good source with no test failures at any history and J services, uncapped expected tests are

 J(1-s_star)/s_star = JC expm1(log(1/delta)/(t+1)),

and expected total native calls addJ. If t=alpha J+O(1), fixed alpha>0, expected tests tend to (C/alpha) log(1/delta), independent of J. Hence even a linear-in-n witness coefficient does NOT imply an asymptotically vanishing source-exposure rate if J can grow faster than n and the outer code corrects a fixed fraction. Previous positive-rate note compared policies at R=1; it did not prove optimal overhead or an impossibility for variable R.

This strengthens the conventional logical two-basis/two-design comparator: full encoder/decoder tests may be expensive individually, but their total count can be constant in block length at fixed soundness. The service operations still each execute their encoder/decoder. Matching/orbit witnesses can reduce the coefficient and change the test interface; no unbounded overall speedup follows just from avoiding the encoder on test rounds.

Real yield depends on actual test failure, source memory and code error distribution. Retaining b>0 failure tolerance changes the tail and may increase yield. The long block also pays quantum storage, outer-code latency, endpoint controls and finite-cap noncompletion. Under unknown adversarial noise, no nonzero acceptance is guaranteed. This is accepted subnormalized correctness, not an ordinary capacity theorem or normalized posterior success statement.

Numerical elementary budgets in check_budget.py are proof checks, not new physical executions. Use expm1 to avoid small-exponent cancellation.

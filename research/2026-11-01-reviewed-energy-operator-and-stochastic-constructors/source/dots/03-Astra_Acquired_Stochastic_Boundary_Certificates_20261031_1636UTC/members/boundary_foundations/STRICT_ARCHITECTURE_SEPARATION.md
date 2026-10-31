# The non-complex-balanced witness strictly needs the other architecture

Use the exact three-species witness in `pivot_lift_results.json`, including the neutral linkage

    2B+C <-> B+2C.

The pivot-star construction is accepted at its frozen reviewed theorem/code. Its non-complex-balance obstruction is unchanged: the separate zero/A component forces a=1 while the 3A leaf forces a=2.

## The finite terminal-gap certificate fails on an actual admissible face

Take I={B,C}, O={A}, and current linkage L={2B+C,B+2C}. The stoichiometric vector (0,1,1) belongs to the global span: add two 0->A vectors and one each of 2A->A+B and 2A->A+C. Thus this divergent-coordinate set cannot be discarded as inadmissible.

Put w=(0,1/2,1/2). A terminal c in L has no A. The terminal-gap condition only permits sources s with s_A<=c_A=0. In this actual network those sources are 0,2B+C,B+2C. For either terminal, w.(s-c) is -3/2 for s=0 and 0 for either neutral source. Hence the exact nonnegative normalized w is a dual infeasibility certificate for that row. The terminal-gap finder cannot certify this network, despite its proved stability.

## Longer same-linkage episodes do not cure the problem

This is also a direct failure of the marked-target drift architecture, not just a conservative cone test. At residual rho=(0,n,n), n>=1, the only designated current-linkage phases are

    population(0,n+2,n+1), target(0,2,1),
    population(0,n+1,n+2), target(0,1,2).

Only the zero source and the two neutral sources are enabled. In either phase the carried-source factorial ratio relative to the other neutral source is exactly (n+1)/n>1. Its ratio relative to the zero source is the carried falling factorial, also strictly greater than1. Its ratio relative to itself is1. Thus every jump's shifted-log-factorial reward is nonnegative; a final ordinary jump has strictly positive expected reward. Every finite target-following episode confined to the neutral linkage therefore has positive expected reward, however many designated alternations are allowed.

The pivot-star correction succeeds for a different reason: V=t^N g(A) gives every neutral jump exactly zero reward, while g(0)>t g(1) makes the rare core birth on the entire A=0 face have a strictly negative reward. It pays the compensating A=1 death correction using the acquired reverse-star rate and finite-layer threshold. No unknown infinite-fiber invariant distribution or mixing theorem is invoked.

`separation_check.py` verifies the exact raw pair list, dual vector, stoichiometric admissibility, and 512 rational factorial-ratio cases. The all-n formulas above, not the finite cases, establish the separation. This is an architectural/certificate separation, not a claim that the stable process was previously unknown or that general recurrence has been solved.

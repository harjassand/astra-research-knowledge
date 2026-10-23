# Strong ordinary comparison

The accepted ordinary proposal-start independence-MH minimax amplitude is K at
scale 1/log n under the same population KL promise. The new critical hybrid
amplitudes are at least K and can be larger. This is a robustness analysis with
an adverse ordinary comparison; it is not a sampling speedup.

For the actual new native tree families, let q_i=b_n z^i,
pi_i=p_T n^-2(J-i), p_T=(log n)^-4, with the core completing both laws.
The accepted core-hitting comparison gives

    TV(q G^j,pi)<=p_T/(1-n^-2)
                   +b_n z/[(1-b_n)(1-z)]+b_n^(j+1).

The construction has (-log z)/loglog n -> infinity. At j/n->t0>0 the right
side is O((log n)^-4), including j=floor(alpha n/2). The hybrid's actual error
on these same families is order 1/log n. Both estimates retain returns.

This is a statement about transition laws. It does not equate target-call,
proposal, setup, cache, index or precision costs. A local delayed-acceptance
screen can have a different per-step cost; no measured computational benefit
has been established here. If the analytic target is disclosed, direct
sampling remains a legitimate additional control.

The independent precision diagnostic uses a changed target-oracle contract.
An ordinary sampler using the same corrupted target evaluations targets the
same changed law; it is not held to an unfair exact target while the hybrid
gets corrupted inputs. Exact ordinary IMH and direct q sampling solve its
disclosed true pi=q null. That example illustrates bias, not hybrid advantage.

The preserved finite expansion fixture is admitted at K=1; the coalescence
fixture fails K=1. Its numbers must not be relabelled an admitted control or
retuned after failure. No historical numerical suite was rerun for Cycle10.

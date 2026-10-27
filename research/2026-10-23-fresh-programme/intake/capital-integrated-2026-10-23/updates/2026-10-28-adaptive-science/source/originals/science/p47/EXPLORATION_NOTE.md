# Retained exploratory failure and its resolution

The first numerical continuation tried high-band starts 10,20,100 across caps
as small as 0.001. The moment-matching formula can have a nonpositive denominator
when the proposed high band is too low, and it can place the low optical band
above the proposed high band. Those outputs are infeasible; they were not positive
networks and do not support a gain. explore.py now labels both conditions and
excludes them before evaluating a supposed design. The governing theorem only
uses sufficiently large H, whose positivity/interlacing is proved. Every claimed
finite design has independently certified strict interlacing and positive parts.

The initial single-pendant all-cap hypothesis also failed: its fitted trace
multiplier becomes negative for sufficiently tight caps. That failure was not
used as a no-go proof. It supplied a concrete negative high-frequency dual
variation, then the moment-exact positive construction and general infimum theorem.
The jointly charged finite optimum required a new cubic dual and full five-root
certificate; a failed three-root certificate alone did not prove that result.

Exploratory floating scripts are secondary to the exact certificates and proofs.

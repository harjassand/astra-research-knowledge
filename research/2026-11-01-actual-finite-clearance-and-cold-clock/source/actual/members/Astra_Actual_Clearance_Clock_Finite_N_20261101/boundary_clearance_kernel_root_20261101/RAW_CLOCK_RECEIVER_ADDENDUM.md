# Raw-clock alternative to the startup-charged endpoint consumer

Root conditional addendum. No new stochastic drift or bracket estimate is proved here. It receives those estimates only if their source proofs explicitly include every enabled startup jump, including actual adverse terminal endpoints with L=0, rather than silently applying the padded-cone derivatives there.

Use all notation and assumptions of FINITE_CLOCK_ENDPOINT_RECEIVER.md. Suppose its stopped Dynkin drift/residual/bracket/jump statements hold from ORIGINAL time zero, not only the L=400 entrance. At the actual corner A=E=0,L=1,

 q0=b(1/T,0),   s_*-1/T<=q0<=s_*.

The derivative bound b_l in [-1,0] proves this exactly. No random startup state or preparation is substituted. After the successful startup the same global lower bound q>=-1/(70T²) applies, and the admitted macro target has |q|<=c_cap=3*10^6/T^6. Startup succeeds by800<4T under its separately paid actual event.

Consequently, provided

 s_*+1/T+r+m+1/(70T²)<4,

nonarrival at original4T is impossible on the successful budget/admission event. The actual clearance interval is

 tau_clear/T in [s_*-epsilon, s_*+epsilon+5/T],
 epsilon=1/T+r+m+3*10^6/T^6,

with the same explicit admission, two-sided martingale, and entropy-service failure charges. The conservative 1/T is used on both sides even though q0<=s_* sharpens the upper side.

A proposed numerical implementation may use the author-pending values
 r=11/20000+4380/(19T)+7254/T²,
 v=1449/(800T)+1285200/T³,
 j=27/(25T),

ONLY after their complete raw-time and startup-segment receiving proofs pass. For a log-tail parameter6, m=2j+sqrt(12v+4j²). Then the martingale failure is <=2exp(-6)<1/200; the last strict inequality follows from the rational sum sum_{k=0}^{17}6^k/k!>400. Remaining admission/service charges still must be added. A 99% claim requires their total plus the martingale bound to be below1/100.

This addendum leaves all previously frozen source statements unchanged. It is not independent acceptance of the numerical r,v,j values.

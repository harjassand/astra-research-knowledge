# Per-pass capture is not a complete-loop production law

## Fixed source and survival: the simplest exact counterexample

Let A be circulating fixed-N flow after the torch, epsilon the stable captured fraction per pass, and R=(1-epsilon)A the fixed-N flow returned. Let S be fresh fixed nitrogen generated per pass, and s in[0,1] the surviving fraction of returned fixed N. Regenerated NO remains fixed nitrogen; it is not new S. At steady state A=S+sR, hence Q=epsilon S/[1-s(1-epsilon)]. This counts repeated passes only once in product.

At fixed S and total power, raising capture .65 to .90 changes SEC by
(.65/.90)*(1-.10s)/(1-.35s).
It ranges from .722222 at s=0 to1 at s=1. At complete return survival, improved capture changes circulating inventory, not recurring product. The source's nominal5.3-to3.7 projection therefore does not follow from the two capture percentages alone. Nominal inverse-fraction scaling gives3.828 at the most lossy endpoint; the paper's65%,90%,30%,3.7 are approximate, so this numerical rounding difference is NOT a precise empirical falsification.

The same finite recurrence gives new fixed N = product + destroyed/lost N + final-minus-initial retained N. feedback_check.py verifies exact12-pass balances. A short favorable run may merely empty pre-existing gas/liquid stores. Completing shutdown/recovery may yield that stored N but requires its own time, heat and hydraulic work; it cannot be erased from either side of the comparison.

## More general source feedback can leave even the sign unidentified

A real torch need not make the same fresh S when recycled gas changes. Let A=f(R) be the measured quasi-steady post-torch fixed-N flow map at specified other controls, not a microscopic kinetic model. The closed loop satisfies A=f((1-epsilon)A). For differentiable f and a stable branch with 1-(1-epsilon)f'(R)>0,
 dQ/depsilon = A*(1-f'(R))/[1-(1-epsilon)f'(R)].

Derivation: differentiate the implicit steady equation to obtain A'=-A f'/[1-(1-epsilon)f']; then Q'=A+epsilon A'. For constant complete electric power, positive Q' improves SEC. If power also changes, use d log SEC/depsilon = E'/E-Q'/Q. Absorber pressure drop, pumps, oxygen preparation, power conversion and reset cannot be silently held free.

Three exact source maps share ALL the following baseline observations: epsilon=.65, A=1, returned R=.35, captured Q=.65. Choose f(R)=c+gR with c=1-.35g:
- g=0,c=1: upgraded Q=.90, SEC ratio13/18 (improves).
- g=1,c=.65: upgraded Q=.65, SEC ratio1 (unchanged).
- g=1.5,c=.475: upgraded Q=171/340~.50294, SEC ratio221/171~1.29240 (worsens).

Both operating fixed points are stable for every map, and all source flows are positive. The gain1.5 case is NOT a survival probability. For example it can be decomposed into survival1 and fresh production S(R)=.475+.5R; it represents an unidentified source dependence on return conditions. It is a logical countermodel, not fitted or asserted nitrogen chemistry. No empirical kinetic coefficient or favorable hardware property is invented to claim an operation. The construction proves only that the reported single baseline and a better absorber fraction do not identify a whole-loop gain, even its sign, without a source-response restriction.

A measured return response could restrict this class. Paired incoming/outgoing fixed-N molar flows at controlled RF/AC power, total flow, pressure, temperature, humidity, oxygen and carrier makeup would determine the relevant response. A small local response identifies a local derivative, not a finite .65-to.90 extrapolation. The actual loop may need a multivariable map when changing capture changes other states. Direct paired complete-operation measurement can answer the practical question without separating microscopic fresh formation from survival.

## Physical boundary and strongest ordinary control

The observed Cerawave acid batch stands independently of these projected upgrades. Its purge and returns are not zero; return survival and source response are not numerically identified in the recovered paper. The same upgraded ordinary packed absorber, PFR oxidation, chemical resources and heat-use options must be available to both comparisons. The efficient design is not automatically the one maximizing a per-pass fraction.

This is elementary flow/feedback algebra applied to the actual missing physical measurement, not a claim of a historically novel control theorem. It changes the next operation: compare complete-loop stable captured-product rate and full energy versus actual absorber intervention and return state, rather than automatically spending design effort chasing90% per-pass removal.

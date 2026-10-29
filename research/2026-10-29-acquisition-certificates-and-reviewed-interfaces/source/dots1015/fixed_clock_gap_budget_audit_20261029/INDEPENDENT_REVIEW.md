# Independent receiving review: fixed-clock certified solver-gap budget
2026-10-29. Reviewer sharpen_noreset_acquisition_certificate.

## Determination
ACCEPTED as a conditional variable-optimization-gap FTPL theorem at the supplied private-current-choice and fixed-computation interface. It is not an implemented engineering clock, empirical expected-gap certificate, uniform structured-family readiness theorem, practical-speed demonstration or drift-tracking result. Prior accepted exact-oracle proofs remain unchanged.

## Load-bearing argument
For each current continuous query w, any returned action has objective at most phi0(w)+epsilon(w), where epsilon(w) is bounded by the actual rounded-query certified gap e plus dR/M. The two coordinate finite-difference inequalities require epsilon only at THIS current w, not at a shifted input and not a uniform supremum. Averaging conditional on the actual past therefore introduces mu=E[e|past] in exactly the stated place. Uniform-box smoothing bounds the finite-difference error by h/(4R). Minimization of (mu+dR/M)/h+h/(4R) yields sqrt((mu+dR/M)/R). Feature ranges also bound this coordinate bias by1.

The crucial extra step is current feedback independence from the solver action AND its current private randomness, conditional on actual past. It holds under the inherited product-probe/current-source interface: probe preparation does not use the candidate, current source is fixed before the new private choices, and nonprobe feedback is0. Without that interface, an expected coordinate-bias bound could not simply be multiplied by720. The document retains the premise and does not infer it from bounded compute time alone.

Taking expectation of the conditional bias and applying Jensen followed by Cauchy gives

 sum_t E sqrt((mu_t+dR/M)/R)
 <=sqrt((T/R) E sum_t e_t+dT²/M).

The same potential telescope and fixed-comparator estimate therefore yield the displayed regret. Substituting M>=140T² and the previous uniform tolerance recovers an approximate-oracle allowance at most720/sqrt2, hence the earlier conservative720. For R proportional to sqrtT, E_T=o(TR) is sufficient for the extra regret/T to vanish. This is a substantive expectation-budget condition; no recorded trajectory alone verifies it.

## Sharpness and executable checks
There is an exact one-dimensional sharpness witness. Let K={0,1}, Z uniform[-R,R], |G|<=R, and always return action1. Then phi0(w)=min(0,w), smoothed optimum derivative=(R-G)/(2R), mean certified exact gap=(R+G)²/(4R), and action bias=(R+G)/(2R). Thus bias=sqrt(mu/R) exactly. Arbitrarily replacing square-root dependence with a generally linear mean-gap dependence is invalid.

`check_variable_gap.py/.json` verifies25 rational instances of this equality,100 finite-midpoint/private-internal-coin cases, an exact two-history Cauchy composition and uniform-tolerance recovery. These are proofs/checks of the mathematical inequality, not an actual quartic solver or quantum acquisition experiment.

## Operational boundaries
A fixed rational candidate and the negative coefficient-l1 bound provide a finite always-valid starting certificate. A bounded solver may improve candidate/lower bound but must retain only fully verified certificates when its public work budget ends. This avoids candidate-dependent rejection; it does not guarantee the resulting gap is small. Incorrect or incomplete SOS certificates must never be promoted to sound lower bounds.

A public bit-operation schedule is not automatically a physical clock or side-channel solution. Source/control isolation, timing, gate synthesis, buffering and calibration still need a supplied physical mechanism. The readiness consequence is conditional on the expected gap budget and the prior guard/outer-code interfaces. Actual logical protection can also be better than the commutator-loss surrogate certifies. Equally informed conventional adaptive methods may use the same solver-gap accounting; no comparative practical advantage is proved.

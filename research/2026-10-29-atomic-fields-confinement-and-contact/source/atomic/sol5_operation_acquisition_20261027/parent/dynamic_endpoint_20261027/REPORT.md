# State-changing readout: an executed conditional endpoint operation

Physical operation NOT_ACQUIRED; no new filtering method or practical advantage.
Read-induced moves need not be terminal if the final useful state can be tracked.
This replaces static preservation with a calibrated dynamic model and stopping
interface; it does not acquire those inputs.

Frozen source-informed multislice templates are native CrSBr and one approximate,
unrelaxed defect at layer15 or16. The source's physical operation is documented
by [Klein et al.,Nature2026](https://www.nature.com/articles/s41586-026-10431-9).
The selected fixed probe is near the interstitial projection. A fixed detector
mask plus399 score bins retains probabilities .00684,.00617,.00941 per incident
mean electron. Discarded counts are not renormalized or saved incident dose.
The minimum retained Bhattacharyya coefficient is B=.001435328 per incident mean
electron, versus .005184619 with full pixels. Hashes and parameters are saved.

The declared closed-state row generator is

    Q=kappa*[[-1,1/2,1/2],[1,-1,0],[1,0,-1]].

It is not fitted from source population rates; branches and reverse rates at
this probe are unmeasured. Initial state probabilities are uniformly known.
Conditional on the hidden path, detector marks have independent Poisson
intensities p_ik per incident mean electron e. Independence from atomic jumps,
known rigid emissions and closed three-state coverage are supplied assumptions.
Thermal mismatch, multiple defects, S/Br loss, leakage and relaxation are omitted.

With lambda_i=sum_k p_ik and A=Q-diag(lambda), the unnormalized row posterior
evolves as rho exp(A delta_e) between clicks, then multiplies by diag(p_ik) at
mark k. Hidden transitions are integrated exactly. The simulation independently
generates competing hidden-jump and click times, without time discretization.
Six matrix propagation checks agree with SciPy expm to2.3e-16.

This is ordinary point-process filtering. The strong comparator includes state
and parameter estimation:[Krishnamurthy/Elliott,1997](https://www.sciencedirect.com/science/article/pii/S0005109896002579)
and [Elliott/Siu/Yang,2010](https://digital.library.adelaide.edu.au/items/b58824ad-8c09-4269-952c-5e84b3eb913a).
It receives identical data and costs. A static fit is only a failure control.

Stop at a click when a posterior exceeds .995, censoring at100/B=69,670.5
incident mean electrons. Under the exact known model, conditioning bounds error
among reports by .005. This is not a worst-case unknown-model guarantee.

|Declared kappa/B|Reports/2000|Wrong|Mean incident electrons,all runs|Mean moves|Reports after a move|
|---:|---:|---:|---:|---:|---:|
|.001|2000|4|1117.7|.0015|3|
|.01|2000|8|1222.1|.017|33|
|.1|2000|5|2013.4|.286|428|
|1|1794|6|28048.1|40.365|1755|

The final case censors206 runs and reports1077 native,128 depth15,589 depth16.
Accurate endpoint reports are not high desired-defect yield or uniform selection.
The static full-record fit makes585 errors at those same reports. Ordinary
dynamic filtering obtains the good result too. The8000-run batch cost .20s
excluding import, template propagation and all physical/calibration acquisition.
These finite-bit Monte Carlo counts are diagnostics, not physical validation.

If the beam continues for ell incident mean electrons after the last usable
datum, the endpoint posterior is rho exp(Q ell). Any posterior is a mixture of
rows, so confidence in j cannot exceed max_i[exp(Q ell)]_ij. For either depth
in this supplied family that maximum is[(1+exp(-kappa ell))/2]^2. Thus .995
depth confidence needs kappa ell<=.005018839, even with perfect earlier data.
At20pA an illustrative100microsecond blind delay delivers12,483.0 mean electrons.
For kappa/B=.01, final-depth confidence is at most .842689. The corresponding
current ceiling for .995 at that delay is .560225pA. These are conditional gates,
not measured hazards or actual blanker specifications. Exposure, processing,
communication and blanker delays must be charged separately.

**This ceiling needs a genuinely blind interval:** neither late clicks nor
no-click survival may be used. It also bounds a target promise made before late
data. Ordinary buffered records through timestamped beam-off allow posthoc
filtering; electronics latency alone does not impose this posterior ceiling.
This stronger comparator was executed in `buffered_endpoint.py` and
`BUFFERED_RESULTS.json`, paying all late dose. After a current posterior reaches
.995, shutoff is scheduled100microseconds later at20pA. Every late mark and the
final no-click interval update the endpoint; reports still need confidence .995.

|kappa/B|Final reports/2000|Wrong|Mean incident electrons|Confident endpoint differs from trigger|
|---:|---:|---:|---:|---:|
|.01|1118|2|13681.4|149|
|.1|37|0|14533.5|28|
|1|0|0|41681.0|0|

At .01, blindly keeping the trigger label gives298 wrong endpoints among2000;
late data salvage1118 high-confidence reports. At1, zero reports means zero
errors are not success. This is conditional heralding with rejection and
state-dependent yield, not preselected-target preparation. Lower current,
different stopping and fuller records remain ordinary alternatives. This
additional6000-run batch took .26s excluding import/templates.

If all transitions and emissions scale linearly with current and dark evolution
is absent, predictable positive current variation is a random time change.
The dose-domain record law and information per move stay invariant. Lower
current reduces a fixed wall-time latency dose while increasing total time.
Probe changes, nonlinear excitation or dark dynamics break these assumptions.

The earlier static pulse model treated every read change as terminal; it was
explicitly conditional. This countermodel demonstrates a different endpoint
operation under stronger dynamic/coverage promises. It supplies neither actual
CrSBr tracking nor a new controller unavailable to ordinary methods. The missing
operation is a calibrated joint transition/emission kernel, unwanted-state
coverage, and a verified event-to-blanker path. Native calibration does not
automatically acquire changed-state response. The parallel branch tests that
transfer. A favorable static B alone cannot close the new interface.

`endpoint_tracking.py` regenerates `RESULTS.json`, using the preceding wave's
read-only environment/templates. All new writes are here. No physical experiment,
external write, purchase, package install or outreach was performed.

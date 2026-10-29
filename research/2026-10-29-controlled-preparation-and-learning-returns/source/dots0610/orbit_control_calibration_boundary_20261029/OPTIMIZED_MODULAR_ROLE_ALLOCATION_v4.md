# Explicit modular calibration role allocation

2026-10-29. Root algebraic construction, checked here; supplementary design
calculation, not an efficiency or hardware claim. Use only the fixed, isolated
endpoint and trusted-control hypotheses of the governing calibration theorem.

The square-root transfer and actual tests give

 e_service <= (sqrt(B q_R)+sqrt(4A q_L)+sqrt(C q_M))^2,
 B=2, A=c_n<=12/5, C=(n+2)/(n-1).

Write c=(B,4A,C). For any positive lambda_i summing to1, weighted Cauchy gives
 e_service <=sum_i c_i q_i/lambda_i.
With private service probability s and calibration-role probabilities
 a_i=s c_i/(R lambda_i), the current bad-service hazard is at most R times the
sum of current observed test-failure hazards. Normalize by choosing
 s=1/[1+sum_i c_i/(R lambda_i)].

At fixed R, total test/service ratio is sum_i c_i/(R lambda_i). It is minimized
at lambda_i=sqrt(c_i)/sum_j sqrt(c_j), with minimum
 (sum_i sqrt(c_i))^2/R.
If tests have per-execution costs w_i>0, the minimum weighted test cost per
service is instead (sum_i sqrt(w_i c_i))^2/R, with
 lambda_i=sqrt(w_i c_i)/sum_j sqrt(w_j c_j).
The service fraction must still be computed from its normalization above; a
cost-weighted optimization does not minimize unweighted number of tests.

For n large, the unweighted coefficient tends to
 (sqrt(2)+2sqrt(12/5)+1)^2, approximately30.39, compared with coefficient2 for
an actual full-path logical two-basis test. Even this optimized modular budget
is statistically much worse. Possible differences in preparation or hardware
costs need complete equal-resource accounting; none is established here.
Membership and round-trip calibration calls are NOT source exposures, whereas
matching and service calls are. Keep these resource units separate.

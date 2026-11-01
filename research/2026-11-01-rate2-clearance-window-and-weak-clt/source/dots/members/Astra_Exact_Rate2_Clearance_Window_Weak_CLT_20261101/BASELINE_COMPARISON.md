# Ordinary SSA / ODE / LNA pilot — separate empirical appendix

These are the already completed pilots at N=100,1000,10000 for the same rate-2
corner/clearance target. They are not theorem dependencies, validated CTMC
approximation-error bounds or new runs. Exact selected report/data/cost bytes
are under `sources/rate2_baseline_pilot_20261101/` and
`sources/rate2_lna_extension_20261101/`; the original complete log/harness
collections are not claimed reproduced. Any future proposal in an unchanged
historical report is not part of this milestone.

| N | main SSA paths | SSA mean (SE) | ordinary ODE event | LNA time variance | SSA sample variance |
|---:|---:|---:|---:|---:|---:|
|100|64|2.97018 (0.14189)|2.45338|0.70434|1.28854|
|1000|64|4.00183 (0.15328)|3.71483|1.36608|1.50366|
|10000|16|6.56216 (0.47201)|6.23440|2.62568|3.56466|

**Ordinary wins retained.** Compiled direct SSA was faster than Python/SciPy
stiff ODE at N=1000 in this pilot. ODE was cheaper at N=10000 but answers a
different question; its event time is not proved to be the CTMC mean. Ordinary
LNA's time-variance estimate is closer to the observed sample variance at
N=1000 than the asymptotic-clock candidate. The candidate's closeness at N=10000
(only 16 paths) is not CLT validation or a finite-N variance guarantee.

**Validity limits retained.** Direct SSA is exact as an ideal stochastic
algorithm; this floating/pseudorandom C++ implementation is not a certified
random-bit sampler. All 148 requested main/preflight paths completed; no
production censoring was hidden. Main-path DKW halfwidths, under the ideal iid
sampling assumption, are about 0.170,0.170,0.340, not small Gaussian error bars.
The mean-field ODE uses mass-action A² rather than falling-factorial A(A-1).
Tolerance/solver agreement is numerical consistency, not a validated error bound.

The full 5-mean/25-covariance LNA produced **impossible intermediate physical
state covariances**: B variance exceeded the actual-chain ceiling
`(N+2+t)^2+t` by factors about 3.85,744,142259. At N=10000 the LNA mean B was
about 3918 and its standard deviation about 3.77 million, while the initial
population is 10002. Independent Radau reproduced the peak to relative
1.98e-8. Loose BDF also showed an intermediate negative covariance eigenvalue;
that was retained, not repaired by projection. This defeats the claimed
full-state covariance interpretation there, **not** every possible timing
prediction or the asymptotic theorem. No Gaussian/CDF fit or finite-N
approximation certificate was earned by either pilot.

**All recorded costs and failed attempts remain charged.** The SSA/ODE pilot
records 224,543,093 clearance events, 18,431 C++ validation events and 18,430
Python reference updates: **224,579,954 total reaction updates** including
reference replays. Two compilations cost 2.024 s. Child wall time totals 31.187 s
and child CPU 26.421 s; the charged execution window is 45.684 s including the
failed instrumentation/debug/relaunch interval. Nested clocks must not be
added twice. The missing `/usr/bin/time` attempt and an early validation trace
that hit its horizon are retained in unchanged reports and cost reconciliation;
production caps were not adjusted. Nine ODE solves are included. Finalization
has its own 0.00669 s wall record. Exact all-session CPU/discovery cost is absent.

The LNA extension performed 13 integrations (nine primary, three domain
checks, one Radau peak cross-check), **zero new SSA**: 16.372 s launch-inclusive
numerical wall, 21.440 s numerical CPU, maximum reported child RSS 93,980 KiB.
Its final check has a separate 0.01990 s wall record. No solver step-rejection
count was available; its work remains inside measured process costs. Peak RSS
is not simultaneous whole-container memory. These historical measurements are
machine-specific observations, not complexity lower bounds.

The N=10^1300 encoded-input certificate is therefore a theoretical task-specific
capability with fully charged algebraic bounds, **not a practical benchmark
victory** over these ordinary methods or evidence of physical preparation.

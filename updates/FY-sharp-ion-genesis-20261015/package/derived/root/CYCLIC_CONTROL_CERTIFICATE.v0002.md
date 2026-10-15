# Restored-device transport: cycle certificates and the exact-zero boundary

Root derivation, 15 October 2026, version 2. Version 1 is preserved unchanged. Conditional finite-state control mathematics;
not an acquired membrane operation or a historical originality claim. Linear
programming duality, cycle spaces and node-potential certificates are classical.
This record specifies the receiving physical interfaces and a finite-execution
qualification that a bare convex mixture omits.

## Supplied operation model

Let a finite directed graph contain one distinguished restored device state z0.
An edge e is one legally repeatable, fixed operation with measured transported
salt s_e, collected cation-exchange amount x_e=(Li_e-Na_e)/2 and accounted time
t_e>0. Let B have -1 at the tail and +1 at the head. Reservoir composition is an
output and may change; edge responses must be validated throughout the allowed
activity range. Hidden adsorption, electrode state, switching, auxiliary paths
and reset must be represented or separately bounded. A graph with symbolic
states and assumed responses is supplied-model computation, not an experiment.

A finite closed walk starting at z0 has integer edge-count vector n>=0,
Bn=0. Its nonzero support is connected to z0. Every nonnegative integer
circulation whose nonzero support is connected and contains z0 is realized
by an Euler closed walk from z0. This is exact for the stipulated fixed edge
operations. Fractional edge counts require an additional divisible-operation
interface; they cannot be read literally as a physical schedule.

Restrict to the strongly connected component containing z0. The normalized
closure of closed-walk edge frequencies is

    C = { f>=0 : Bf=0, sum t_e f_e=1 }.

To prove sufficiency, decompose a circulation into directed cycles; approximate
its real cycle coefficients by rationals, repeat the integer cycles many times,
and connect them to z0 using legal paths in that same component. Connector
counts and costs remain bounded while cycle repetitions grow. Their normalized
contribution vanishes. This establishes a closure statement, not exact finite
salt cancellation. No cycles outside the reset component are included.

## Sharp asymptotic salt-balanced rate and its dual

Assume a legally executable zero-transfer idle loop at z0, so zero output is
feasible. Such an idle operation is not free at an existing chemical gradient:
leakage, time, energy and gradient changes must be modeled or bounded. If no
legal idle loop exists, use the actual feasible LP and do not infer eta>=0. The
asymptotic balanced rate is the finite LP

    eta = max x dot f
          subject to f>=0, Bf=0, s dot f=0, t dot f=1.

It has the exact dual

    eta = min tau
          subject to x_e <= kappa s_e + (B^T u)_e + tau t_e for every e.

The idle loop forces tau>=0. Finite dimensional LP strong duality applies
when C is nonempty; positive t bounds every feasible coordinate, so the
primal optimum is attained. The equality concerns a normalized closure:
legal closed walks can approach its salt rate0 and exchange rate eta.
It need not supply a finite exact-zero-salt walk, and unknown/drifting edge
responses invalidate its physical receiving interface.

In particular eta=0 iff there is a node potential u and a salt multiplier
kappa with

    x_e <= kappa s_e + u(head e)-u(tail e) for every edge.

Sufficiency is telescoping. Necessity follows from the dual optimum, whose
minimum is attained in this finite LP. This is a complete supplied-graph
asymptotic obstruction. It does not rule out an unmeasured operation, a
missing state, another electrolyte or a changed instrument boundary.

For an arbitrary finite path, any feasible dual certificate gives

    sum x_e <= kappa sum s_e + u(zT)-u(z0) + tau sum t_e.

This makes restoration and charging explicit. If the coordinate sum s_e is already inventory-corrected, an exchange inventory
bound C_X and endpoint potential span U give, for |sum s_e|<=epsilon,

    observed exchange <= |kappa| epsilon + U + C_X + tau total_time.

For an uncorrected salt assay S_obs with |S_obs-sum s_e|<=C_S and
|S_obs|<=epsilon, the required bound is instead

    observed exchange <= |kappa|(epsilon+C_S) + U + C_X + tau total_time.

C_S, C_X and U must be acquired or justified joint bounds. Dropping the salt
inventory correction is invalid when kappa is nonzero. Repeating the same
unclosed inventory discharge is not a restored operation. At tau=0 an output
beyond this bound falsifies the stated model/certificate, not every possible
physical explanation or every membrane.

## Why exact zero cannot be inferred from the LP

Take states0,1, unit-time edges0->1 with(s,x)=(1,0), 1->0 with(0,0), a loop
at1 with(0,1), and an idle loop at0 with(0,0). The graph is strongly connected.
The LP places unit weight on the loop at1 and obtains eta=1 with salt0.
Yet every finite closed walk based at0 that produces exchange must traverse
0->1 at least once and has salt>=1. Exact finite salt0 implies exchange0.

The walk0->1, loop at1 repeated N times, 1->0 instead has salt1, exchangeN
and timeN+2. Its salt rate tends0 and its exchange rate tends1. A useful finite
experiment can meet a specified *relative* salt tolerance by repeating a
validated cycle enough times, but the absolute connector salt does not vanish.
Its volume, activity changes, drift, work and device lifetime must allow those
repetitions. This exact counterexample distinguishes finite restored collection
from asymptotic graph feasibility without denying the latter theorem.

## A state-dependent selectivity gauge

The incoming static rejection X_j=k S_j is the single-state special case.
More generally, x_e=k s_e+u(head)-u(tail) allows different instantaneous X/S
ratios yet forbids closed-cycle salt-free exchange. Different transient edge
selectivities can be only reversible inventory charging. Only cycle-integrated
responses remove this node-potential freedom. Conversely memory-driven cycle
transport can exist when a steady-state waveform library is collinear; that
library is not a global controllability certificate.

## Robust acquisition and classical optimization boundary

For acquired edge boxes |x_e-xhat_e|<=epsx_e and |s_e-shat_e|<=epss_e, a sufficient
uniform dual certificate is

    xhat_e-kappa shat_e+epsx_e+|kappa|epss_e
      <= u(head)-u(tail)+tau t_e.

It is exact for the stated independent rectangular uncertainty set. Introduce
a>=kappa and a>=-kappa to express the certificate as an LP, with epss_e>=0.
For correlated acquired uncertainties replace the box term by its actual
support function; independence must not be silently invented. Shared calibration
and drift require joint coverage, not repeated intervals treated as independent.
A positive robust execution likewise requires a connected, realizable schedule
and a salt interval entirely within the predeclared tolerance.

Graph construction, state discrimination, response measurements, calibration,
coverage and reset costs are not included in this post-supplied-model LP.
Worst-case finite-time costs and useful product isolation must be compared with
an equally informed direct separator. The presently acquired ratchet workbooks
contain KCl conductance/electrical records, not the Li/Na/Cl responses or restored
state graph required here. This theorem therefore does not acquire cation
exchange, improve a demonstrated separator or establish technological novelty.

## Receiving-species and stochastic qualifications

A salt-balance row alone certifies the claimed pure Li/Na exchange only under
an independently justified neutral three-species Li/Na/Cl closure. Otherwise
append the cation-sum A=Li+Na row, other transported ions, solvent and relevant
charge/source nuisance rows to the LP. Their dual multipliers and acquisition
uncertainties must also be charged. Opposite chloride responses alone do not
supply cancellation of all those rows. The same-cycle reset must be measured;
global inventory return can conceal side-resolved storage changes.

The deterministic graph theorem concerns fixed acquired edge rewards. A Markov
or stochastic operation whose table contains expected rewards yields an expected
rate LP. A realized collection guarantee additionally requires a calibrated
concentration bound and joint statistical/measurement error. An expectation,
simulation, positive graph circulation or restored law is not a measured batch.

Independent internal audit: workers/fy_ion_control_adversary_root_audit/AUDIT.md
accepts the graph/LP proof with these explicit receiving qualifications. Root
check_cyclic_control.v0002.py supplies 24 exact checks including the finite-zero
counterexample and differing transient ratios under an exact potential gauge.
Classical LP/cycle machinery is credited. The presently missing Li/Na response,
reset-state and species-assay interfaces remain NOT_ACQUIRED.

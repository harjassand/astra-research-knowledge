HIDDEN NETWORK: USEFUL RESPONSE CONTROL CAN REQUIRE LESS THAN STATE CONTROL
Original conditional calculation,14 November2026 Brisbane.

Physical model and access

Take six vertices0--5 and edges, in order,
(0,2),(1,3),(0,5),(1,5),(2,5),(3,5),(5,4).
Vertices0,1,2,3,4 are external ports;5 is inaccessible. Every resistance r_e
is positive. At the reference state all seven r_e=1. Kirchhoff equilibrium
and the following adaptation laws are INTRODUCED model assumptions, not
measured constitutive data or a qualified persistent material.

During reading, input pressures are imposed at0and1 and reference4 is zero;
outputs2and3 and hidden vertex5 float. The free-node matrix at the reference
state, in order[2,3,5], is

  A=[[2,0,-1],[0,2,-1],[-1,-1,5]].

For unit input at0 the right-hand side is[1,0,1], and for unit input at1 it is
[0,1,1]. Thus W=[[11/16,3/16],[3/16,11/16]] maps the two input pressures to
the two output pressures. It is passive weighted averaging, with reference
weight1/8 in each row. Negative gains or powered output amplification are not
supplied. The read pressure fields determine the exact observable derivative.

For edge e=(a,b), let q_e be its oriented incidence vector. Differentiating
the free-node Kirchhoff equation gives

  du_free/dr_e = A^-1 q_e,free * (p_a-p_b)/r_e^2.

This defines the4x7 Jacobian J for response vector
w=(W00,W10,W01,W11), evaluated at the declared reference state. It is not an
observation of every hidden resistance. A physical controller would obtain
only terminal readouts and declared error bounds, not this simulator state.

Writing through exterior ports

During writing all five exterior pressures can be imposed, one gauge
redundant; hidden pressure follows its true conductance-weighted equilibrium.
Consider two separate model laws: dr_e/dt=d_e, or dr_e/dt=d_e^3, where d_e is
the actual local pressure drop. Both are smooth and odd on the positive
domain. Persistent memory and a shared read/write gate are separate physical
requirements, not consequences of Kirchhoff equilibrium. No interior clamp
or per-edge setter is installed in this calculation.

Use the following seven patterns on exterior vertices0--3, with reference4=0:
  P0=(-1,-1,-1,-1)
  P1=(-1,-1,-1, 0)
  P2=(-1,-1,-1, 1)
  P3=(-1,-1, 0,-1)
  P4=(-1,-1, 0, 0)
  P5=(-1,-1, 0, 1)
  P6=(-1, 0,-1,-1).

Let F1 and F3 be the7x7 matrices of resulting state-rate vectors at r=1 for
the linear and cubic laws respectively. Exact rational calculation gives
rank(F1)=4 and det(F3)=4536/1953125, so rank(F3)=7. The cubic law has more
local state-writing directions. This alone does not decide useful learning.
For the linear law, the exact cycle quantities r0-r2+r4 and r1-r3+r5 are
conserved throughout ANY pressure history. They rule out full seven-state
reachability, independently of the frozen rank. Lie brackets may add directions
to the frozen linear span but cannot remove these two cycle invariants.

Observable response result

Compose the actual state-rate fields with J. For C1=J*F1, columns[P0,P1,P3,P6]
form a4x4 matrix with determinant -13/65536. For C3=J*F3, columns[P0,P1,P2,P3]
have determinant49257/2560000000. Therefore BOTH laws have four independent
boundary-accessible RESPONSE directions at this reference state, even though
the linear law cannot control all seven internal states locally.

Conditional local theorem and proof

For either law, fix the four patterns with nonzero observable determinant.
Let Phi_j^t be the positive-domain flow under pattern j, and define

  H(t1,t2,t3,t4)=w(Phi_4^t4 Phi_3^t3 Phi_2^t2 Phi_1^t1(r0)).

For sufficiently small signed times these flows exist within the positive
domain and are smooth. Their derivative at zero is precisely the selected
observable matrix C. Its determinant is nonzero. The inverse-function
theorem therefore gives a local open set of four-coefficient target response
maps reachable from r0 by those boundary pulses. Negative flow time can be
realised by reversing the pressure pattern ONLY because the assumed local
law is odd and reversible. This is not negative physical elapsed time or
negative dissipated work. The nonzero determinant persists in a neighborhood
of r0 by continuity; no explicit uniform neighborhood radius is provided.

This proves local target-RESPONSE reachability without requiring independent
setting of every internal resistance. It does not yet supply an unknown-state
boundary-observed teaching algorithm, global target acquisition or a useful
uniform cost/error bound. Observable sensitivity could in principle be
estimated by terminal probes, but finite probe work, conditioning, noise,
returning from probes and actual constitutive reversibility must be supplied.
Complete state identification should not be imposed as a necessary step when
only the useful terminal function is wanted.

Earlier pulse construction does not transfer unchanged

The earlier exact three-field selector works when every vertex is clamped.
In this hidden graph its first-order increment for edge(0,2) is
[-6,0,-96/125,-6/125,24/125,-6/125,6/125]. A nonselected hidden link changes by
12.8%of the selected magnitude at first order. Finite positive-stateRK4
trajectories approach this expression with decreasing pulse duration;
8/16/32step refinement at duration.001 agrees to about1e-15. This is an
arithmetic check of the introduced ODE, not a physical measurement. The
observable theorem above is constructive evidence that this failed selector
does not imply impossibility of useful bulk response training.

Executable/source bindings

ROOT_HIDDEN_NODE_BOUNDARY_WRITE_FIELD_SCREEN_20261114.py
6897ASCII/SHA256863c510f381e224b08615b1b93559003c249f0b9a7f75b1cd372aecb4548c35c
records the hidden-pressure model, exact state-field determinant, leakage and
finite positive trajectories. Its original output JSON is6024bytes,
SHA256b1513357d85394757f7f179f47dc50b69690438a1c3b105f03dd8d1e6cc69cdb.

ROOT_OBSERVABLE_BULK_RESPONSE_TRAINABILITY_SCREEN_20261114.py rebuilds the
Kirchhoff/response derivative with exact Fractions and composes it with the
actual boundary fields. Central differences of independently solved read maps
at step1e-5 differ from the analytic derivative by at most4.39454e-12. Exact
rational determinants, rather than finite-difference ranks, govern the claim.
No producer code, data, library implementation or physical experiment is used.

Scope and missing operations

This is one graph at one reference state and a local neighborhood; no growing
bulk family or boundary-to-volume scaling is established. The pressure write
laws, gate and retention are not installed hardware. There is no complete
source-work/state-energy balance, bandwidth, material range/life, noise model
calibration, global safe domain, uniform conditioning bound or full-system
advantage. Nonlinear geometry, hysteresis or irreversible local kinetics may
invalidate flow reversal and need a different argument. The fluid result
does not automatically extend to vector elasticity or wave media. Existing
inverse-function control, adaptive system identification and physical-learning
methods remain prior machinery; no novelty verdict follows from this example.

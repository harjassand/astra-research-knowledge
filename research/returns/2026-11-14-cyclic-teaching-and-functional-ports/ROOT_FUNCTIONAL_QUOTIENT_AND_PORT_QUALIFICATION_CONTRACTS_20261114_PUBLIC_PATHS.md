ROOT: FUNCTIONAL QUOTIENTS, CHANGING CONNECTIONS, AND HIDDEN CHANNEL TESTS
14 November 2026 Brisbane. Conditional network identities and introduced models.

1. A supplied microscopic parameter need not be a useful physical coordinate

Consider the introduced unit-resistance tree with boundary0,1,2,3(ground), hidden
4,5, and edges(0,4),(1,4),(4,5),(2,5),(3,5). Its grounded port impedance is
  Z0 = [[3,2,1],[2,3,1],[1,1,2]].
Add a boundary chord of resistance rho>0 between0 and2. Set c=(1,0,-1),
v=Z0*c=(2,1,-1), and alpha=c^T*Z0*c=3. Inverting the rank-one admittance update
gives, exactly,
  Zrho=Z0-v*v^T/(rho+3).
This is an ordinary rank-one network identity, not a new inverse theorem.

Omitting a weak chord gives a positive error Z0-Zrho. Relative to the ACTUAL
network's energy, its worst-case error over all boundary current patterns is
  sup_(q!=0) q^T(Z0-Zrho)q / (q^T Zrho q) = 3/rho.
For proof, the rank-one error's generalized eigenvalue is
v^T Zrho^-1 v/(rho+3). Since Zrho^-1=Z0^-1+c*c^T/rho, this becomes3/rho.
The absolute Euclidean operator error is6/(rho+3), while
  ||dZrho/drho||_2=6/(rho+3)^2.
Thus recovering a large rho to a fixed absolute PARAMETER accuracy can demand
far more precision than approximating the useful port RESPONSE. In this known
example rho>=3/epsilon permits omission with energy-relative error<=epsilon.
That is a conditional response quotient, not acquisition of an unknown weak
edge, general tomography, or a physical process that deletes the chord.

The opposite limit has a different consequence. Contracting the strong chord
gives Zmerge=Z0-v*v^T/3, with absolute error
  ||Zrho-Zmerge||_2=2*rho/(rho+3).
But Zmerge*c=0 whereas c^T Zrho*c=3*rho/(rho+3)>0. Therefore the relative energy
error on input c is100% for EVERY rho>0. A small absolute error does not authorize
discarding a mode under a relative whole-response contract. The definition of
useful input/output accuracy must be fixed before claiming a quotient useful.

2. A nonenumerative many-weak-link sufficient bound

Let A0 be a known positive definite grounded full-network conductance matrix.
Add edges g_e*b_e*b_e^T with g_e>=0. Write
  alpha_e=b_e^T A0^-1 b_e, gamma=sum_e g_e*alpha_e.
Cauchy--Schwarz in the A0 metric gives
  b_e*b_e^T <= alpha_e*A0,
so A0 <= A=A0+sum_e g_e*b_e*b_e^T <= (1+gamma)*A0.
Inversion and restriction to boundary injection matrix P yield
  Z=P^T A^-1 P <= Z0=P^T A0^-1 P <= (1+gamma)*Z.
Consequently omission of ALL these edges has port-energy relative error at most
gamma for EVERY boundary current pattern. This requires finite supplied bounds
on the actual g_e*alpha_e, with their computation/acquisition paid. Many small
edges accumulate:1000 terms of.001 give gamma1, not.001. The bound is sufficient
and can be loose; it does not identify a particular physical weak subnetwork.

This positive static linear result does not automatically survive nonlinear
adaptation, AC parasitics, negative incremental elements or a changed interface.
For repeated programming it must hold throughout the declared reachable state
and load domain, or be reacquired with actual observations. A hidden coordinate
irrelevant under one connection can become useful under a later connection or
intervention. A current-response quotient is not a universal erasure of history.

3. Differential probing exposes an actual hydraulic ambiguity

INTRODUCED steady incompressible model: two nominal independent passages each
have total hydraulic resistance R>0, split into two equal halves. Their midpoints
x,y are joined by unwanted conductance g>=0. The respective inlet pressures are
P_A,P_B and BOTH outlet pressures are0. All four boundary pressures and signed
flows are part of this test contract. No unmodeled valve is inserted at a port.

Each half has conductance a=2/R. Midpoint pressure balance is
  (2a+g)x-g*y=a*P_A,
  -g*x+(2a+g)y=a*P_B.
Hence
  x+y=(P_A+P_B)/2,
  x-y=(P_A-P_B)/(2+g*R),
  Qcross=g*(P_A-P_B)/(2+g*R).

If P_A=P_B, Qcross=0 for EVERY g. Every intended inlet/outlet flow equals P_A/R.
This common-pressure test cannot distinguish even a very large cross-connection
from truly independent passages. It is not evidence against all boundary tests:
the missing differential excitation is available in the declared port model.

At P_A=P>0,P_B=0, the admitted A-flow is
  Qin_A=(P/R)*(4+3gR)/(2*(2+gR)),
and the fraction diverted into the two B ports is
  Qcross/Qin_A=2gR/(4+3gR).
Requiring that fraction<=eta<2/3 is equivalent to
  gR<=4eta/(2-3eta).
For eta=.01 this gives gR<=4/197 and leak resistance>=49.25*R. Differential
pressure/flow probing can therefore qualify this function without reconstructing
the exact hidden leak shape, PROVIDED the physical model, accessible pressures
and installed observations actually satisfy the declared contract.

Controlling P_B=0 includes a reservoir able to receive fluid at that inlet.
Closing the inlet changes the problem and requires a different calculation.
Measuring only one B outlet would see only part of the unintended flow here.
The model concerns hydraulic crossflow, not molecular diffusion, chemical carryover,
retained residue, mechanical proof strength, nonlinear junctions or future life.

4. Finite flow observation is part of the qualification operation

Suppose installed absolute error of EACH inlet/outlet channel is bounded by e,
and observed A-inlet/A-outlet values are m_in,m_out with m_in>e. The true diverted
fraction is at most
  max(0,m_in-m_out+2e)/(m_in-e).
Even zero OBSERVED loss is not a zero true leak. For equal readings5mL/min and a
1% acceptance gate, a sufficient error limit is e<=5/201=.02487562189mL/min.
This is an introduced installed-error requirement, not a maker specification or
a calibrated sensor. Shared offsets, control error and drift need their actual
joint bounds; no independent-noise averaging credit has been supplied.

For scale only, an INTRODUCED fully developed straight circular tube with
mu=.001Pa*s,L=.020m,d=.0003m has ideal Poiseuille resistance about1.006e11Pa*s/m3.
At5mL/min the ideal pressure drop is about8.38kPa and Reynolds number about354
at introduced density1000kg/m3. Entrance development, junctions, wall compliance,
roughness and clear-diameter tolerance remain unqualified. Its corresponding
model leak-resistance gate is about4.96e12Pa*s/m3. This supplies no real tube,
hidden connection, manufactured part or proof-pressure certificate.

5. Execution and scope

ROOT_FUNCTIONAL_QUOTIENTS_AND_DIFFERENTIAL_PORT_TESTS_20261114.py and its JSON use
only the standard library and ROOT-written code. Seven positive rho cases compare
the exact rank-one formula with independently inverted3x3 admittance matrices;
the error is exactly0 in Fraction arithmetic. Six positive/zero leak cases solve
the2x2 balances and check signed mass conservation and the differential fraction
exactly. The parameter sweeps are finite diagnostics; the all-pattern inequalities
above follow from the stated algebra and Loewner proof, not from the sweeps.

The earned operations are conditional functional-error certificates and a
specific differential port test. The growing-network boundary teacher, an
autonomous manufacturer, acquisition of hidden coefficients, a new physical law
and an actual qualified device are not supplied. These examples also show why
changing the objects used by a theory must change its predictions/constructions;
a renamed set of input/output labels is insufficient.

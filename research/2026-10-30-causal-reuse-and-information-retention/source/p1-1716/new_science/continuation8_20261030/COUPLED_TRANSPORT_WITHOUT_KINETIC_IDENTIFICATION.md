# From suppressing a current to coupling two transport processes

30 October 2026. Root follow-on construction. The larger question is whether
event memory can impose a useful transport relation, rather than merely make
one current quieter. It can, at the exact selective-gate interface below.
Tight coupling, cycle affinities and kinetic-independent stall relations have
strong direct predecessors. This is a consequence and operational construction,
not a claim to have discovered tight coupling or autonomous energy conversion.

## 1. Actual operation and the pathwise transport relation

There are two marked transport channels. A selected event in channel a has
signed unit increment delta=+1 or -1 in J_a. Set epsilon_1=+1, epsilon_2=-1.
The one-bit memory u is changed atomically to -u by every selected event. The
closed gate allows such an event precisely when

    epsilon_a delta = u_before.                            (1)

Unselected events preserve u and have zero increments in these two declared
currents. Their physical motion is not erased: it must still be included in
any density or complete-displacement observable. No external bit reset is used.
One explicit implementation in the current model is the actual selected rate

    r_e = k_e(x)[1+u epsilon_a delta],                     (2)

with nonnegative unknown k_e. For reversible baseline statements below the
reciprocity condition is imposed on the complete marked reverse pair. The rate
being exactly zero on the closed gate is an actual operation premise, not a
conclusion from a finite-data confidence interval.

Put g(u)=-u/2. On every selected event,

    Delta(J_1-J_2)=epsilon_a delta=u=Delta g.

It also holds on unselected events. Hence for every actual initial state,
every nonexplosive timing law on the allowed support, and every time t,

    J_1(t)-J_2(t)=g(u_t)-g(u_0)=(u_0-u_t)/2,
    |J_1(t)-J_2(t)|<=1.                                  (3)

No kinetic identification, stationary initialization, asymptotic limit, external
clock, or measurement of accumulated current is needed for (3). Actual channel
and direction selective coupling and atomic bit updates are essential. A global
bit coupled to distant ports retains its nonlocal physical resource cost.

Same-polarity coupling instead bounds J_1+J_2. Thus changing the actual gate
polarity selects a transport combination. It does not preserve both individual
current laws while changing only their correlation.

## 2. Actual force ports and arbitrary reversible kinetics

For a precise stationary consequence use a finite complete joint state space,
including all retained internal dynamics, at each fixed value of any frozen
hidden parameter. The baseline marked rates q_0(x,y,a) obey detailed balance
with a positive warranted law mu_0, and have the gate support (1). An actual
load port changes them to

    q_h(x,y,a)=q_0(x,y,a) exp[h_1 d_1+h_2 d_2],           (4)

where d_a are the marked signed current increments. Unselected transitions
have d_1=d_2=0. Reverse increments are -d. The full rates, force convention,
and inclusion of every nonconservative affinity are premises. Equation (4)
is a supplied physical operation here, unlike the mathematical weak tilt used
solely to prove the nonlocal LDP.

The kinetic magnitudes may be arbitrary, unknown and inhomogeneous. They may
depend on the complete hidden state. Positivity on the chosen support ensures
the same communicating classes; no uniform lower rate is needed for the
qualitative finite-system theorem. Each recurrent class has a stationary law.

In any stationary class, (3) gives equal mean channel currents,

    I_1=I_2=:I.                                          (5)

With dimensionless entropy in units of k_B, the stationary entropy production is

    sigma = sum_(x,y,a) pi_h(x)q_h(x,y,a)
               log[pi_h(x)q_h(x,y,a)/(pi_h(y)q_h(y,x,a))]
          =2h_1 I_1+2h_2 I_2=2(h_1+h_2)I >=0.            (6)

The stationary sum of the gradient log(pi_h/mu_0) vanishes. Pairing each marked
edge with its reverse proves nonnegativity. This is the standard stochastic
network entropy-production identity, used without estimating q_0.

If h_1>0, h_2<0 and h_1+h_2>0, positive I describes transfer against channel 2's
load, paid by channel 1. Under a warranted isothermal interpretation of (4),
input and output powers are 2 k_B T h_1 I and -2 k_B T h_2 I, respectively.
Their ratio is -h_2/h_1. This statement counts all affinities in the joint model;
it does not exclude unmodeled actuator costs or provide a complete apparatus
efficiency.

## 3. Exact stall and the productive-cycle condition

At h_2=-h_1=-h, the force increment h_1d_1+h_2d_2 is h Delta g. Therefore

    mu_h(x)=Z_h^-1 mu_0(x) exp[2h g(u(x))]
           =Z_h^-1 mu_0(x) exp[-h u(x)]                  (7)

obeys detailed balance for q_h. It is a genuine invariant law, not a prepared
initial condition. For a product baseline with fair u, its visible marginal is
unchanged. The stall relation h_1+h_2=0 is independent of all reciprocal kinetic
magnitudes. Preparation or convergence time to (7) is a separate requirement.

Nonzero conversion must also have an actual productive cycle. On any closed
marked path, (3) gives J_1=J_2=k. Its affinity under (4) is 2(h_1+h_2)k.
If a finite communicating class contains a cycle with k!=0, then for h_1+h_2!=0
Kolmogorov's cycle criterion excludes detailed balance. Its stationary entropy
production is strictly positive, and (6) proves

    sign(I)=sign(h_1+h_2).                                (8)

Without such a cycle, a gate can simply block transport. Equation (3) alone
does not certify useful power. An arbitrarily small common kinetic prefactor
also makes power arbitrarily small without changing (3), (7) or (8). No
kinetics-independent quantitative power or mixing guarantee follows.

## 4. Explicit productive support, not a hypothetical cycle

Use two oriented triangles 0->1->2->0 and 0->3->4->0, with two exclusion
particles on the five sites. The first triangle is channel 1, the second is
channel 2. Add reciprocal unselected chords 1<->3 and 2<->4 that preserve u.
Apply the opposed-polarity gate (1). With positive rates on every allowed
marked edge, the 20-state joint support is connected.

The following closed cycle is allowed. A pair such as 01 denotes occupied
sites; the sign following it is u:

| Transition | Channel increment (d_1,d_2) |
|---|---:|
| (01,-) -> (12,+) | (-1,0) |
| (12,+) -> (23,+) | (0,0) |
| (23,+) -> (02,-) | (0,-1) |
| (02,-) -> (01,+) | (-1,0) |
| (01,+) -> (14,-) | (0,-1) |
| (14,-) -> (04,+) | (-1,0) |
| (04,+) -> (03,-) | (0,-1) |
| (03,-) -> (01,-) | (0,0) |

Its current is (-3,-3); the reverse cycle has (3,3). Thus the qualitative
conversion theorem is nonvacuous. The ordinary unselected chords move particles
but do not carry the declared load work. Their motion is retained in the joint
description. No hydrodynamic law is claimed for this small network.

`check_coupled_transport.py` reconstructs this support witness and its reverse
rates exactly at the discrete level, then checks 15 forced population generators
with three independent choices of reciprocal prefactors over four decades and
five force pairs. It verifies stationarity, equal currents, the stall law and
the entropy identity. The largest entropy-identity error was 4.09e-15 in the
executed environment. These are numerical population checks, not experimental
calibration or the proof for arbitrary kinetic functions.

## 5. Errors, records and finite tolerance

If a selected event occurs with the wrong gate sign, its mismatch from Delta g
is plus or minus two. If an external or erroneous bit flip occurs alone, its
mismatch is plus or minus one. On every recorded actual path,

    |J_1-J_2| <= 1+2 N_wrong+N_extra_bit.                 (9)

This is an exact error budget, not a claim that those counts are known or small.
Support violations, missed actuation, unrecorded channels, or additional work
sources need their actual supplier and sensing model. A finite positive error
rate can accumulate indefinitely; exact and finite-tolerance coupling differ.

Stationary force conclusions require an actual stationary initialization or
an explicitly justified long-time limit in a recurrent finite class. The
pathwise relation (3) needs neither. Conditional use after calibration retains
the full future channel/gate law. Retaining a record does not pay for acquisition,
initial preparation, bandwidth or energy. Frozen hidden parameters are handled
one at a time; arbitrary nonstationary hidden histories do not inherit (6).

## 6. Strong predecessors changed the interpretation

Lipowsky and Liepelt, *Chemomechanical Coupling of Molecular Motors:
Thermodynamics, Network Representations, and Balance Conditions*, J. Stat.
Phys. 130,39--67 (2008), DOI 10.1007/s10955-007-9425-7, directly develops
network coupling, slip cycles, local and cycle balance conditions. Root read
the actual primary text at https://www.mpikg.mpg.de/rl/P/archive/275.pdf.
The stall/entropy argument above is an application of that established network
machinery, not a separate foundational thermodynamic principle.

Utsumi, *Join gate with memory in token-conserving Brownian circuits and the
thermodynamic cost*, Phys. Rev. E 113,024129 (2026), DOI 10.1103/pmx1-rz3n,
https://arxiv.org/html/2505.12390v2, is especially close operational prior art.
Its one-bit memory correlates two particle transfers, reverses the available
direction after firing, and has a concrete quantum-dot Hamiltonian/master-
equation proposal. Repeated directed output uses a paid reset protocol. Root
read the model, transition structure and reset discussion before interpreting
this follow-on as a new capability. The paper's finite-error physical gate
does not supply the exact atomic gate in (1), and our theorem does not inherit
its hardware realization merely by analogy.

Accordingly this coupled-current theorem is retained as useful machinery and
a possible consumer of an eventual supplied selective operation. It strengthens
the meaning of polarity control. It is not selected as an independent claim
to a major new foundational discovery. The round's stronger assembled result
remains the full nonlocal path law, its compatible hidden-kinetics supplier and
the removal of the external shared clock, together with explicit locality costs.

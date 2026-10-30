# Round 11 result: local contact can control native density, at a different task

The completed construction is SINGLE_FILE_CONTACT_CONTROLS_NATIVE_DENSITY.md.
One driven hard-core tracer in a one-dimensional no-passing ring creates
an order-one native density profile and moves the native population through
actual contact. This is a strong ordinary alternative, directly preceded by
the driven-tracer and local-battery literature. It does not preserve native
density histories, so it does not solve root's strengthened selected task.

## Exact result with hidden frozen rates

Native particle i has unknown fixed symmetric rate c_i between two positive
bounds. The tracer has supplied rates p>q>0 and affinity F=log(p/q).
Writing S_i=sum_{j<=i} 1/c_j,

\[
\mathcal J=(p-q)/(1+qS_M),\qquad
w_i=1+\mathcal J S_i,\qquad
\pi_H(g)\propto\prod_iw_i^{g_i}.
\]

Every particle has the same mean true velocity
v_N=mathcal J Z_{H-1}/Z_H. An exact partition-ratio inequality proves
v_N=Theta(1/N) uniformly over the frozen-rate class at fixed interior
density. Thus one auxiliary drives Theta(1) total native current.
There is no microscopic rate inference or unmeasured intervention.

If the cumulative native resistance homogenizes to bar r times label
distance, the limiting tracer-frame native density is

\[
\rho_F(x)=(1-t)\exp[-(e^F-1)t\,x/\rho],
\quad
\int_0^1[1-t(1+(e^F-1)u)]^{-1}du=1/\rho.
\]

The profile shape depends on F and total density, while the unknown
kinetics enter only the speed through bar r. The proof is a conditioned
geometric-array limit with explicit local-central-limit and concentration
steps. It is a stationary receiver; no cheap finite-time preparation is
asserted for arbitrary frozen arrays.

## Concrete physical target and resources

For F=log 2 and rho=1/[4 log(3/2)], the native profile is
rho_F(x)=(3/4)(2/3)^x. It falls from 3/4 in front of the tracer to 1/2
behind it. Native total mean current tends to 1/(4 bar r).

On physical time N^2 T, true native displacement is order N^2, while
mean ideal signed drive work is
N T log(2) log(3/2)/bar r. The same local-detailed-balance port is
needed for that work formula; hidden futile cycles and nonrecoverable
reverse-step work can increase the apparatus bill.

A canonical equilibrium preparation cannot produce this profile with
o(N) total work plus o(N) supplied excess free energy. The explicit
profile relative-entropy lower bound is at least 0.0103882 N in k_B T
units. Prepared native gradients, controller correlations, and chemical
sources must be included; this is not a universal sparsity prohibition.

The stationary laboratory mean is flat because the profile's origin is
the uniformly positioned tracer. The actual retained tracer position
identifies its nonflat physical density profile. A stationary battery at
one fixed native bond is an ordinary stronger direct actuator producing
a nonflat laboratory-frame profile without the mobile tracer.

## Passive and bandwidth boundaries

Sparse uniformly bounded reciprocal resistances are macroscopically weak
in a homogeneous one-dimensional conductor. Sparse resistances of size
Theta(N/R) are not weak: one critical barrier gives a membrane, and finely
periodic gates can change bulk diffusivity. An Arrhenius realization costs
barriers of order log(N/R), with actual prefactors and assembly still
required. Thus neither sparse mass nor local coupling alone prohibits
collective density control.

Root's later extensive elastic-train option is compatible with a different
resource tradeoff. A closed elastic belt is the strong ordinary comparison.
Large stiffness needs paid force/response range, literal local link
geometry, and a stated bath/friction interface; nearest-label harmonic
coupling does not automatically supply fixed-range mechanical links.
No full elastic-train receiver was constructed by this role.

## Verification and scope

The executable check_driven_tracer.py checks the exact stationary balance,
common marked physical velocities, hole-removal identity, partition bounds
and entropy-production/work identity for 48 finite cases, 1,560 states and
7,896 marked transitions, including nonuniform frozen native rates and
zero drive. All rational residuals are exactly zero; the floating marked
entropy/work residual is below 7.7e-17. DRIVEN_TRACER_CHECK.json preserves
the output and code hash.

This is a population-model verification, not an acquisition-precision,
hardware, hydrodynamic-path or mixing-time experiment. Native labels and
conserved cyclic order, source initialization, arbitrary old-record
conditioning, true displacement, and additional preparation costs are
kept explicit. SOURCE_SCOPE.md records the actual primary sources read.

All earlier continuations are unchanged. This role created no additional
agents, branches, transfers or external messages.


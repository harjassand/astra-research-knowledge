# Result

**The supplied C_CM<=1/4 point has an all-frequency no-improvement
certificate. A tighter compliance cap produces a genuine finite
two-resonance optimum when a finite stiffness budget is also charged.**

At the original m=1,M=2,K=1,theta=1/2 resources, the globally optimal
complete spectrum at C_CM<=1/4 is the ordinary spring-4 pendant:

    [0,sqrt5-1] union [2sqrt2,sqrt5+1],
    J=1.094388522317695923972117...,
    J/J_rigid=0.942353155061616461360470... .

This is a proof over every legal finite internal graph, not an optimizer
failure. It uses the exact compliance moment and a certified three-root
dual. See **PROOF.md**, Section 2, and `helper/PROOF.md`.

I continued beyond that closure to a stronger resource-complete opening.
At **C_CM<=1/20 and total internal spring sum<=24**, an actual finite
two-pendant star is globally optimal over all finite positive topologies:

    backbone mass 1; side masses
      0.06552741459340005487..., 0.93447258540659994513...;
    springs
      6.29361480175482849704..., 17.70638519824517150296...;
    J=1.142016098461582733349079... .

The component values are exact transcendental objects defined by a
certified scalar sign bracket, not rounded numbers assumed legal. Both
cost caps bind exactly. The best one-pendant comparator at the same
budgets has k=20 and J=1.142045387542071761716599... . Two active internal
resonances are necessary and sufficient for the finite optimum. The
saving is real but small: 0.000029289080489028... in J, about 0.00256% of
total comparator conductance. **JOINT_CAP_PROOF.md** gives the proof and
complete bands. A separate entirely rational cell also strictly improves
the comparator with spring sum 2300/99<24.

The mechanism generalizes. **FAMILY_PROOF.md** proves a universal
five-root bound for the proper four-moment Bose dual, with arbitrary trace
and log multipliers. Its resource Jacobian is strictly negative definite,
giving an analytic local two-cost design inverse and an open family of
finite globally optimal two-pendant cells. Fourteen nearby/extended
resource points were actually constructed and interval-certified,
including C=1/20 with stiffness caps 20.01 through 100. A finite list is
not claimed to be a global resource phase diagram.

**BOUNDARY_PROOF.md** gives the exact feasibility boundary
C_cap*kappa_cap>=1. At equality the active response is one pendant; at
C_cap=1/20, every positive stiffness slack above 20 permits strict
improvement by a second mode. An executed finite split at total stiffness
20.0064001280... has certified all-band gain 5.4891912382e-8.

For unlimited stiffness, **PROOF.md** also gives the exact C=1/20
infimum J=1.1419160253172373..., proves nonattainment by any fixed-m=1
finite network, and supplies legal charged approximants. The sharp
all-network small-compliance law is

    [J_rigid-inf J]/C -> 0.398643595583964859... .

The one-pendant coefficient is 0.377679197206601085...: extra modes improve
the leading saving by 5.55%, while the saving itself vanishes. The sharp
sequence spends unbounded stiffness, explicitly counted.

All core exact certificates and all fourteen finite-family certificates
execute successfully. Every optical band is included, and integral tails
have rigorous remainders. One same-settings helper reviewed the root
counts, resource signs, finite optimum, analytic family and asymptotic
mechanisms; its scoped reviews found no substantive errors. See
**REPRODUCE.md** for commands and provenance.

This uses inherited exact moments/inverse synthesis and ordinary
Foster/Stieltjes, sign-variation and convex-dual machinery. An equally
informed conventional designer can realize the same optimum. Historical
priority and algorithmic advantage are not established.

**Mission-level physical capability: NOT_ACHIEVED.** These are mathematical
results in a scalar harmonic ideal-contact model. The hardest remaining
physical obligation is to retain useful gain after finite contacts,
connector mass, geometry/strain, vector polarizations and nonharmonic
operation are actually charged. The general global resource phase diagram
is also unresolved. The finite two-cost optimum and analytic inverse now
provide a concrete controlled target for that next physical comparison.

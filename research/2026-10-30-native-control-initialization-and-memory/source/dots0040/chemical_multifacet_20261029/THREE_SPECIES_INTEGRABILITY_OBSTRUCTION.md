# A genuine three-species obstruction to logarithmic moving-fugacity transfer

Status: internally derived, unreviewed. This falsifies a proof representation, not recurrence.

## Network and unbounded class
Let y0=(1,3,0), y1=(3,0,0), y2=(0,3,3), y3=(2,0,3). Include

    y0 --100--> y1,  y1 --1--> y0,
    y2 --1--> y3,    y3 --100--> y2,
    0 <--> yi (both directions rate1), i=0,1,2,3.

This is one strongly connected linkage class, hence weakly reversible; stoichiometric rank3. The communicating class of0 contains all (A,B,C) with A divisible by3, B,C divisible by9, B≥C, A≥(B−C)/3. Indeed take n2=C/3 births of y2, n0=(B−C)/3 births of y0 and n1=(A−n0)/3 births of y1. These are nonnegative integers. Reversing those enabled births returns to0. Thus the rays used below occur within one genuinely three-unbounded-population class.

## Representation being tested
In the strictly ordered cone A≫B≫C≫1 write

    u=log(B+2)/log(A+2), v=log(C+2)/log(A+2), 0<v<u<1,
    F=A U_A(u,v)+B U_B(u,v)+C U_C(u,v),
    mu=exp(F)/(A!B!C!).

Require bounded smooth U, and the same local-fugacity premise used by the2D construction: for every fixed reaction displacement h, F(x+h)−F(x)=h·U(u,v)+o(1), uniformly on compact angular subregions. A sufficient, stronger version explicitly requires gradF−U→0 and enough second-derivative control to transfer to fixed shifts; no general equivalence is claimed. This is a substantive representation restriction, not a property of every positive dual measure.

The chain rule forces triangularity. In the C derivative the correction contains

    [A ∂v U_A+B ∂v U_B+C ∂v U_C]/[(C+2)log(A+2)].

Along fixed u,v, the A/C term dominates B/C, which dominates1. For the correction to vanish requires ∂v U_A=0 and then ∂v U_B=0. Similarly the B derivative forces ∂u U_A=0. Consequently U_A is constant and U_B depends only on u; c_A=exp(U_A), c_B=exp(U_B) cannot change with v at fixed u. This conclusion can instead be obtained directly from the fixed-shift premise and a Taylor expansion. The graph supplies the shifts ±yi through its star reactions; telescope them to obtain 3e_A=y1, 9e_B=3y0−y1 and 9e_C=3y2−3y0+y1. All finitely many intermediate shifts are valid on the positive rays. Smoothness makes the finite telescoping RHS converge to the corresponding lattice shift dotted with U. Applying the expansion at these lattice shifts gives the same dominant derivative terms; no unsupported unit-shift premise or stationarity is assumed.

## Two exposed faces demand contradictory fugacities
Take A~alpha t^3, B~beta t^2, C~gamma t^s, 0<s<2, s≠1, rounding into the class lattice above. Then u→2/3 and v→s/3. The four complex exponents are9,9,6+3s,6+3s. For s<1 the first pair is the unique maximal face; for s>1 the second pair is.

For any local fugacity c, exact factorial cancellation gives the leading adjoint coefficient at yi:

    d_i(c)=sum_j k_(j,i)c^(yj−yi)−sum_j k_(i,j).

Put rho=c_A^2/c_B^3. The first pair has

    d_0=rho+c^(−y0)−101,
    d_1=100/rho+c^(−y1)−2.

The second pair has

    d_2=100rho+c^(−y2)−2,
    d_3=1/rho+c^(−y3)−101.

A nonpositive eventual adjoint defect for every fixed alpha,beta,gamma>0 forces each exposed coefficient nonpositive: the ratio of the two leading monomials is alpha^2/beta^3, which can be any positive number, while U has the same limiting value independent of these fixed prefactors. Thus the first face requires rho>50; the second requires rho<1/50 (strict because the immigration terms are positive). But triangularity makes rho identical at u=2/3 on both sides. Contradiction.

Hence there is no dual envelope of this smooth bounded logarithmic-angular moving-fugacity type, with the fixed-shift local-fugacity premise, having nonpositive adjoint outside a finite set for this network. The result is not merely a finite collection of numerical failures: the contradictory inequalities occur on infinite asymptotic rays in one communicating class.

## What actually fails, and what remains possible
The2D success varied only the smaller population's fugacity, making derivative errors vanish. In3D, independently patching face fugacities generally demands variation of a middle population coefficient with the smaller population's angular coordinate; that creates an unbounded integrability correction. This cannot be repaired by choosing a larger constant fugacity or a farther-out threshold.

This does not exclude arbitrary positive dual measures, composition-dependent nonlogarithmic potentials, profiles with boundary layers narrowing with population, or exact shell resolvents. It does not refute the chemical recurrence conjecture. It specifically prevents promoting the2D coefficientwise face construction to arbitrary dimension by independently choosing compatible-looking angular fugacities. A replacement must solve the integrability/within-face profile problem, not assume it away.

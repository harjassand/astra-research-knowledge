# Exact feasibility boundary and modal splitting with arbitrarily small slack

Keep the actual m=1,M=2,K=1,theta=1/2 resources. Let kappa be the total
positive internal spring sum and take positive resource caps. A joint compliance/stiffness contract is
feasible **if and only if C_cap*kappa_cap>=1**.

To prove necessity for an arbitrary internal graph, write its physical
internal stiffness matrix as L and the relative-CM load as
f=(-1,m_1,...,m_n), with total side mass one. Then C_CM=f^T L^+ f. Use
the trial displacement x_b=0 and every side x_j=1. It has f dot x=1 and
x^T L x=k_incident, because every non-backbone edge sees zero displacement
difference. The compliance Rayleigh principle gives

    C_CM >= (f dot x)^2/(x^T L x)
          =1/k_incident >=1/kappa.

Thus C_cap*kappa_cap>=1 is necessary. The one-pendant cell with spring
1/C_cap proves sufficiency.

At equality C_cap*kappa_cap=1, all inequalities must saturate. Every
positive spring must be incident to the backbone, and equality in the
Rayleigh principle makes all static side displacements equal. On the
resulting star k_j must be proportional to m_j, with k_j=kappa_cap*m_j.
All branch squared frequencies coincide, so the complete active response
is exactly a single pendant with mass one and spring kappa_cap; any other
star modes are dark. Thus the feasibility boundary has an exact active
one-resonance characterization.

## At C_cap=1/20, any strict spring-budget slack allows improvement

The optimized one-pendant spring is k0=20. Fit its three-edge
unconstrained-stiffness dual

    R1(w)=g(w)+lambda/w+2mu*w-eta/w^3.

`certify_boundary_split.py` encloses mu<0 and eta>0. Therefore R1(w)<0
at all sufficiently large w, and it specifically certifies R1(10)<0.

Choose v=100, a new side mass epsilon>0, its spring H=epsilon*v,
and the remaining side mass 1-epsilon with spring

    k_epsilon=(1-epsilon)^2/(C-epsilon/v), C=1/20.

This is a positive finite actual star for all sufficiently small epsilon,
and its exact full CM compliance is

    epsilon^2/H+(1-epsilon)^2/k_epsilon=C.

Its total spring expenditure has the expansion

    H+k_epsilon
      =k0+epsilon*(v-k0)^2/v+O(epsilon^2)
      =20+64 epsilon+O(epsilon^2).

To check that the additional optical band actually improves full J, let
A0=[[k0,-k0],[-k0,k0]], Api=A0+4 e_b e_b^T be the limiting two-mass
endpoint matrices, and define

    G0(v)=e_b^T(v I-A0)^(-1)e_b
         =(v-k0)/[v(v-2k0)],
    Gpi(v)=G0(v)/[1-4G0(v)].

The new side's mass-normalized diagonal is exactly v and its coupling is
-v*sqrt(epsilon). Schur-complement expansion gives the new squared edges

    alpha_new=v+epsilon*v^2*G0(v)+O(epsilon^2),
    beta_new =v+epsilon*v^2*Gpi(v)+O(epsilon^2).

The finite new optical bandwidth is therefore

    epsilon*gamma(v)+O(epsilon^2),
    gamma(v)=2v^(3/2)*G0(v)^2/[1-4G0(v)]>0.

The three old positive edges move by O(epsilon). Since R1 is zero at each
old edge, their first-order contributions to integral R1(chi_new-chi_one)
vanish. The log, trace and compliance moments agree exactly, so

    J_new-J_one
      =integral R1(chi_new-chi_one)
      =epsilon*gamma(v)*R1(sqrt(v))+O(epsilon^2)<0.

At v=100, the certified leading coefficients are

    gamma=0.3755868544600938967...,
    gamma*R1(10)=-0.00054902083725784552449... .

For **every kappa_cap>20**, however small its positive slack, choose a
sufficiently small positive epsilon. This construction then fits that
spring budget and strictly improves on the optimized one-pendant design,
while retaining the exact compliance cap. This is an existence theorem
for any positive slack, not a uniform manufacturing-precision guarantee.

An actual finite member with epsilon=1/10000 is also certified:

    masses=(1,1/10000,9999/10000),
    springs=(1/100,99980001/4999900),
    exact C_CM=1/20,
    total stiffness=20.006400128002560051201024...,
    J_one-J_split in [0.000000054891912382394915,
                      0.000000054891912382394916] >0.

Every optical band is included by the rational exponential-sum integral
certificate. The infinitesimal calculation selects the mechanism; the
finite certified member demonstrates that it survives an executed full
spectrum comparison. It does not claim the split is optimal for its tiny
slack or that this small normalized effect is a practical-device gain.

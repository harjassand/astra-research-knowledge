# Optional exact scalar-fault tilting refinement

This refinement applies only to the exact scalar CP-contamination model of REPORT.md. It has been independently checked. It is not a justification for retaining the original clock law after postselection.

Let `mu=m gamma t`, all executed controls have the same scalar failure weight epsilon, and boundary count c is fixed. Set

`S0=(1-epsilon)^c exp(-mu epsilon)`,
`f=1-S0`,
`gamma_tilt=gamma(1-epsilon)`.

The Poisson Janossy density multiplied by the no-fault weight obeys, for each generator,

`exp(-gamma t) gamma^n (1-epsilon)^n = exp(-gamma t epsilon) exp[-gamma(1-epsilon)t] [gamma(1-epsilon)]^n`.

Thus, after removing its scalar mass, the healthy-parent path distribution is EXACTLY an independent Poisson family at gamma_tilt. Initial frames remain uniform because the scalar flag weights are seed independent. The reference theorem applies at this changed rate.

Let `q_tilt=min(1,a_ref^2,m B(J,gamma_tilt,t))`. The mixed partition proof gives the alternative homogeneous bound

`p <= min(1, f + S0 q_tilt)`.

The primary bound `f+q_ref(gamma)` also remains valid by positive, unnormalized domination. Their homogeneous minimum can be used; do not presume either dominates every coarse majorant parameterization.

For the enlarged bad event “proposed count N>M OR some executed control fault,” define

`T_M=Pr(Pois(mu(1-epsilon))<=M)`,
`f_M=1-S0 T_M`.

The accepted good weak effect is bounded both by the unrestricted tilted weak effect and by the independent accepted-path mass. Hence

`p_M <= min(1, f_M + S0 min(T_M,q_tilt))`.

The original fixed-path action theorem also gives the more explicit good-term bound

`S0 min[T_M min(1,a_ref^2), m B(J,gamma_tilt,t)]`.

Combining this with `f_M+q_ref(gamma)` is legitimate as a homogeneous minimum. No conditional truncated-Poisson process is asserted to remain Poisson, and no normalized endogenous quantum branch is used.

The simpler primary formulas are usually preferable when the additional tightness is immaterial.

# Corrections retained during root review

The initial draft of the root slew bound omitted the initial deficit in its corollary. The general bound is Delta<=max{Delta(0),sqrt(Rmax/Cmin)}; the smaller expression needs Delta(0) below it. The critical-radius direction is explicit in the repaired derivation.

The initial midpoint pressure-subflow integrator produced a spurious half-time-step lag for fast-filling throats. In the 500 nm illustrative row, that discretization exceeded the actual near-equilibrium lag scale. The repaired script uses implicit Euler with its quadratic root at endpoint pressure and reports refinement differences and a separately labeled quasistatic approximation. The original draft numerical values are not physical evidence.

The initial root witness called reaching a finite z=ln(a0/a) a seal. A positive cylindrical radius still conducts. The repaired witness establishes reaching a declared geometric/contact criterion; a gas-tight snap/contact/bond law must be independently acquired. No literal seal is inferred from the ODE. The same qualification was sent to the mathematics lead. This is a substantive modeling correction, not a notation change.

Independent discovery-lead review also rejected an interim worker ODE fit whose connected and sealed reference outputs did not actually match. That failed fit is not promoted into root evidence. Any repaired worker output has its own disclosed scope and must assert matching before use.

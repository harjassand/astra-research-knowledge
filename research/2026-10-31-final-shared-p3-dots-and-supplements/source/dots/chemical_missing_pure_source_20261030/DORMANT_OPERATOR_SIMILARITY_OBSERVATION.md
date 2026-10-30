# Non-small dormant return kernels: exact conservation can replace small row mass
Status: scoped personal observation for the next boundary test, not a full recurrence proof.

In the dormant residual chain2A'<->A'+D<->C+D, consider a bad section restricted to D=0 and bounded A,B phases, stopped immediately when D is created. While D=0, the unbounded reservoir C is exactly unchanged: connector reactions do not involve C, and the only enabled fast source involving no D is2A', whose firing exits the dormant face by creating D.

Consequently the residual r on this face has the form

    r=C+chi(phase),

with chi bounded on the chosen phase alphabet. For the actual dormant return kernel P_B at fixed C, exponential residual tilting is an exact finite diagonal similarity:

    P_B^(theta)=D_theta^-1 P_B D_theta,
    D_theta(phase)=exp(theta chi(phase)).

Its spectral radius is the same as the UNTILTED killed kernel, for every fixed theta. A large exponential row sum therefore does not prove instability. If the actual finite phase graph has a uniformly positive path to the D-creating exit, its killed Green kernel is finite; the tilted Green is obtained by the same diagonal similarity. This supplies a composition/phase profile without pretending that every bad-return probability tends to0.

For the explicit dormant face, activation supplies enough A to enable the D-creating source. At bounded phases and fixed positive rates there is a finite positive-probability path to that exit, independent of the frozen C. Thus this local killed phase problem is genuinely accessible by the previously preserved finite-phase machinery. The harder obligations are its outgoing seeded-state return law and enlargement beyond D=0 to small but nonzero D where C-dependent reactions are enabled. Those must not be replaced by a supplied absorption/return estimate.

This observation suggests the next general boundary operator should allow BOTH graph-earned small-mass blocks and finite-profile blocks whose tilt is a conservation-induced similarity. It does not yet resolve coupled multifacet or infinite-background return kernels.

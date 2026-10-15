# Temporary clearance topology: cost and self-erasure

Root derivations, 15 October 2026. Standard continuum and graph ingredients are credited; priority for this particular design synthesis is UNKNOWN. These are conditional model results, not a built manufacturing operation.

## Hydraulic cost of serially traversing partition lanes

Let a straight duct of length L and cross-section D carry steady, fully developed, no-slip, incompressible Newtonian flow of viscosity mu. Write -Delta u=1 in D with u=0 on its boundary. Then Q=(Delta p)/(mu L) integral_D u and hydraulic resistance R=mu L/(integral_D u).

The classical Saint-Venant inequality gives integral_D u <= A^2/(8 pi), where A=area(D), hence

    R >= 8 pi mu L / A^2.

One self-contained route is to set a(t)=area{u>t}. Integrating the PDE over a superlevel set gives integral_level |grad u|=a(t). Coarea and Cauchy-Schwarz give perimeter^2<=a(t)(-a'(t)). The planar isoperimetric inequality gives perimeter^2>=4 pi a(t). Consequently -a'(t)>=4 pi and integration of superlevel areas gives the bound. Usual regularity/approximation conditions on bounded duct sections apply.

If m separated lanes in the original edge are traversed in series and have areas A_j summing to at most A, Jensen gives

    R_serial >= 8 pi mu L sum_j A_j^-2
             >= 8 pi mu L m^3 / A^2.

For m=2 this is eight times the equal-area circular reference resistance. It is NOT an eightfold ratio to an arbitrary original noncircular duct. Finite septum thickness, bends, U-turns and junction losses can increase the cost. Slip, gas, yield-stress support and moving compliant walls require a different calculation. This is a genuine lower bound inside the stated flow class, not an impossibility result for removal methods.

Primary mathematics/context: Berger, A Beautiful Inequality by Saint-Venant and Polya, https://www.math.ualberta.ca/~aberger/papers/saintvenant_polya_monthly.pdf ; original channel-shape study Mortensen et al., https://arxiv.org/abs/physics/0412015 . The classical inequality itself is not an Astra discovery.

## Exact two-face dose cancellation in an ideal U-turn

Let the two lanes have equal plug speed u and length L. Inject a nondepleting reagent step of concentration c0 at the inlet at time zero. A longitudinal septum site x receives its outbound front at x/u and return front at (2L-x)/u. Its accumulated two-face concentration exposure is

    D(x,t)=c0[(t-x/u)_+ + (t-(2L-x)/u)_+].

For t>=2L/u this becomes 2c0(t-L/u), independent of x. Before that time D<=2c0 L/u. A uniform reaction-dose threshold H>2c0 L/u would therefore preserve all sites through the full preload and, in this ideal model, reach H everywhere at the same time t*=L/u+H/(2c0).

This is a possible design relation, not a robust erasure protocol. It assumes equal lane velocities, negligible reagent depletion, instantaneous transverse delivery, equal reaction law on both faces, no leakage and a dose-controlled erosion law. Alginate diffusion and chelator binding do not automatically supply those assumptions. An arbitrarily small proximal rate increase can open an upstream bypass before distal completion; the independent adversary derives an exponentially severe distal-flow reduction with distributed leakage. The remaining eroded polymer also has to leave the now-blind cavity. Simultaneous disappearance can trap it even if all primary support was already removed.

Thus paired arrival-time cancellation may assist preload design, but a retained hydraulic route, a qualified distal-first release protocol or an accepted and measured residue limit is still essential. No conditional simulation establishes those material properties.

# Why a pressure-free overwrite bound is impossible at fixed temperature

This is an exact obstruction to the all-plus-reference transport, not to the Ising research goal.

For an m-by-h free rectangle with the fixed boundary conditions of the paid open-anchor partition, select a set I of interior sites separated by at least three lattice spacings, with

 |I|>=floor((m-2)/3) floor((h-2)/3).

Starting from the all-plus free rectangle, flip an arbitrary subset of I to minus. The chosen defects have disjoint incident bonds. Every defect changes four plus/plus physical bonds and one field term, so its exact relative Boltzmann weight is z=exp(-8theta-2phi). Therefore the COMPLETE partition ratio necessarily satisfies

 Q(m,h)>=sum_{S subset I} z^|S|=(1+z)^|I|
         >=exp[|I| z/(1+z)].

This retains a genuine positive bulk pressure at every fixed finite theta. With m,h both proportional to R and phi=theta/R, its logarithm is Omega_theta(R²). Thus no uniformly valid bound Q<=poly(n,R) exp(c_theta R) can hold for this all-plus reference at arbitrarily large R. Replacing the current upper's exp(-2theta) pressure coefficient by a much smaller exp(-8theta) would greatly extend the useful finite window, but would not remove the asymptotic obstruction.

The issue is not only an unnecessary partition overcount. In a row-by-row upward overwrite flow stopped at the first majority target, choose an edge whose upper endpoint first has exactly n/2 plus spins, with all unprocessed spins minus. Require the updated site to have been minus in the source. Independently place the separated defects at earlier processed interior sites. Every such source remains below target until that last required update, and therefore uses the same edge. Its preimage weight sum contains the factor (1+z)^|I|, up to the fixed last-site factor. The information carried by the thermal defects has genuinely been erased by that transport.

The next uniform route must preserve, move or rethermalize those bits with a paid conditional law, or prove a native killed-time/interface-growth bound that does not use all-plus overwrite congestion. This is compatible with the valid finite-R certificates and does not invalidate them.

# Globally defined bbox/semiperimeter trial: constructive small-torus test

## Construction, with topology paid explicitly
For each plus component C on the periodic L×L nearest-neighbor graph, let w(C),h(C) be shortest cyclic coordinate interval lengths covering its coordinate projections. Let g=max_C(w+h), with g=0 at the empty state. Detect winding by attempting a consistent integer lift of every component's edges; any lift inconsistency means winding. Let c be component count and a total plus count.

The hard trial is f=1−1{g≥h or winding or a≥n/2}. This sets f=1 at all-minus and zero on the complete majority target, not just single-droplet targets. Native single-site edges include all mergers, winding changes and target overrides; nothing is removed from the generator. The target override is essential: disconnected majority configurations need not have a large bbox component.

The smoother construction aggregates native conductances by feature tuple (a,g,winding,c), with separate source and target labels. If C_ij=sum of all physical conductances between feature classes, solve the Dirichlet linear system on this finite quotient. Lift its potential to every original state. This is a valid full-state-space trial with exactly the quotient Dirichlet energy. It is an upper bound, not an equality to original capacity unless within-class equilibration is justified. The feature process is not assumed Markovian. This is standard variational coarse graining, NOT a novel invention.

## Executed finite calculation
`bbox_trial.py` exhaustively enumerates all 65,536 states and 524,288 undirected physical heatbath edges on L=4. Native energy relative to all-minus is E=2theta*perimeter−2phi*area, and c_xy=1/(exp(E_x)+exp(E_y)). Target a≥8. Source is only all-minus; this is NOT the R200 soft-source thermal core. Floating-point linear algebra and energies: numerical evidence, not directed interval certificates.

For theta=1, phi=.3, best tested hard bbox threshold log energy −10.5401 is worse than the original majority area cut −11.0710. For theta=4, phi=2, best bbox −48.5509 improves area −47.8411 by only .710 log units. The hypothetical universal bbox improvement is therefore unsupported.

Optimized area-only versus joint-feature log energy:
- theta=1, phi=.3: −12.59568418 versus −12.61492806 (only .01924 log improvement).
- theta=4, phi=2: −55.13362009 versus −55.15009354 (only .01647 log improvement).

Joint feature quotient has 65 vertices; area-only has9; bbox/winding/count-only has38. All computed potentials stay in[0,1]. The joint result is necessarily no worse than area-only because its function space includes area-only potentials. Its tiny actual gain in these tests indicates that adding bbox alone is not evidence of a transformative new bound.

## Unclosed R200 obligations
To use this on R200 one must bound every aggregate native inter-class conductance without enumerating 2^(2,560,000) states. That includes disconnected components, nonconvex shapes, mergers, wrapping and the original soft source. The four-corner family supplies only a subset and cannot upper-bound these aggregates. Full enumeration and these L4 parameter choices do not establish asymptotics, tractability or an R200 improvement.

A more plausible local next construction is a smooth area-based potential across the critical window, enriched by corner-invariant geometry only where aggregate weights can be bounded. However no R200 upper improvement is asserted here, and smoothing alone may already be included in stronger existing upper bounds.

# Static occupation bound beyond a fixed bounding-box width

Define an analytical core by two explicit conditions on each actual plus component S:
1. |S|≤422500;
2. its raw filled hull admits a finite planar lift whose projection onto the torus is injective.

This definition deliberately EXCLUDES winding/noninjective cases. It includes the box650 core but also many elongated planar components. It is not assumed equivalent to any original C_r convention.

Let P denote the raw outer perimeter. The lift gives |S|≤|hull(S)|≤P²/16, while the explicit size cap gives |S|≤422500. Consequently the hull-word contribution to the activity of S is bounded using the same exponent
−8P+.04 min(P²/16,422500)
as in CORE650_OCCUPATION.md. Here it is S's area cap, not an unproved cap on its filled hull, that is used. The remaining hole boundaries cost at least8 per edge; no favorable hole-area term is needed for this bound.

Every hole root has at most n distinct torus locations because the entire lifted hull projects injectively. Thus the hole gas is bounded by exp(nκ), with κ≤(1/745)^4/(1−1/745). Replace the previous651² root budget by n. The low-P exact counts, middle-perimeter convexity bound, and high-perimeter area-cap tail remain unchanged.

planar_area_core_occupation.py/json verifies the resulting exact rational normalizer excess is still below1.087e−7, using the exponential comparisons already checked in core650_occupation.py. By h_a≤1, this pays the entire hard-source numerator occupation within this analytical class, including all thermal companions and repeated visits.

Unknown occupation is now confined to states containing either a component of more than422500 sites, or a component failing the explicit injective-planar-hull condition. This is a static initial-occupation localization, NOT a bound on time outside the core. Nonplanar/winding states are not discarded; their contribution remains an explicit open term. A thin torus-spanning plus cross illustrates why winding cannot be reduced automatically to a pair of noncontractible boundary loops: its complementary face can be contractible.

## Candidate weighted reconstruction, not yet a theorem
Creative is investigating a connected-prefix seed whose bounding span first reaches400 in one direction; its other span is then at most400. Filling that seed rectangle and growing only the other dimension keeps each completed planar400×h rectangle at energy6400. For an arbitrary fixed exterior, comparing original inside pattern x to filled current rectangle z gives E(x)−E(z) at least the corresponding difference with minus exterior: each exterior-plus neighbor of an inside site missing from x adds16 to the difference. This can pay original configurations through a restricted standalone Gibbs partition function, without summing arbitrary exterior states.

This route requires a rigorous preimage mapping for every relevant current edge, a bound uniform up to height1600, treatment of hitting majority during any preparatory fill, and a separate wrapping phase. At vertical wrap, a width400 full-height strip has energy0; full-height widthw has E=25600−64w and reaches majority atw800. Its Gibbs reconstruction is cylindrical, not the planar rectangle calculation. None of these missing interfaces is assumed established here.

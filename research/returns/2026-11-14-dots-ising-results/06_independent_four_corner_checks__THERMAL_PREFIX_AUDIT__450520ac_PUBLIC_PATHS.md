# Independent audit of the inherited thermal-prefix estimate

Read full `n1722_compact_thermal_flow_20261113/RESULT.md` and its `BAY_CLOSURE_JOIN.md`, not merely the later aggregate summary. The high-area four-corner use does **not** violate a hidden6R² area ceiling: none appears in the fixed-fiber moment proof.

## Hypotheses required without relaxation
1. theta>=4, integer R>=80, phi=theta/R, L>=8R.
2. Filled embedded D with fixed plus endpoints on every physical boundary edge; embedded bounding rectangle.
3. Fixed interior spin pattern with M_D>0, subsequently summed over such patterns.
4. Sufficient fixed MINUS exterior collar under the actual augmented connectivity.
5. All exterior companion filled domains embedded, area<=R², and **disjoint from every frozen pin**. This last condition is explicit and cannot be replaced by informal component separation.
6. No additional global M<0 condition on the Gibbs source ensemble. States already in target B are included and carry zero-length paths/zero voltage.
7. All exterior sites toggled at most once in a deterministic geometry-only order; stop at first actual B.

For four corner notches in a4R-square, item2 holds and the bounding long side is4R>2R/a, where a=.999996. It must still be translated into an embedded chart. Items3–6 remain source-family restrictions, not facts about arbitrary high-mass states.

## Peierls and field-tilt step
At fixed interior and collar, the free exterior Gibbs law has no coupled interior constraint. For a specified companion filled disk V, flipping ALL of V is injective and preserves the exterior family because V avoids pins and |V|<=R². Nested thermal holes are not erased. Under any free-site fields in[0,3phi], its source/image ratio is at most exp[-2theta P+6phi min(P²/16,R²)].

For P<=R this is at most exp[-13theta P/8]; for P>R, isoperimetry and V<=R² imply V<=RP/4 and yield exp[-theta P/2]. Thus the inherited tiny uniform free-site plus probability bound remains valid independent of the area of D. Tilting by exp(4phi N_F^+) changes each participating field by2phi and stays within the tested range. Integration of the log-partition derivative gives E exp(4phi N_F^+)<=exp(4phi rho |F|). No FKG for the constrained exterior gas is needed.

## Exact resistance exponent
For F disjoint from D,
log[w(x)/w(x XOR F)] =2theta sum_(edges crossing F) sigma_i sigma_j +2phi sum_(i in F) sigma_i.

On original D-to-F edges the signs are fixed plus/minus, so their bond product is-1. On every other crossing edge the product is at most1. Consequently the bond sum is at most P(D union F)-P(D). The field term is exactly -2phi|F|+4phi N_F^+. Applying the preceding moment yields
E[w(x)/w(x XOR F)] <=exp[2theta(P(D union F)-P(D))-2phi a|F|].

This step is valid for arbitrary exterior defects. It does NOT say each physical XOR flip creates a plus spin.

## High-area prefix geometry and target
Four-corner filling preserves perimeter for each missing site in the geometry-only path; the earlier exact enumeration tests the same general monotone order. At the full square, adding a strip raises perimeter by at most2 transiently, while each completed strip of length at least4R lowers the displayed exponent. Wrapping can only reduce perimeter. Thus every prefix retains the inherited exp(4theta) bound.

Fixed D remains untouched. If a source starts outside B, completing every exterior XOR yields M_D-M_outside>0 since M_D>0 and M_D+M_outside<0. First-target stopping is legitimate. Source positivity is used HERE; it cannot be dropped by the FKG normalizer argument.

## Energy pooling and scope
For fixed D, the flipped site determines the prefix; the two orientations recover at most two source states. Interior patterns remain visible in the physical state on D, so pooling patterns does not add an exponential multiplicity. The heatbath edge resistance is1/w(z)+1/w(z^i). This yields unnormalized physical energy E_D<=2n exp(4theta) Z_D as in the inherited proof. Different contours can share edges; the later weighted triangle inequality pays that collision and is essential.

Verdict: the inherited prefix proof applies to the stated four-corner family, conditional on its explicit exterior pin-disjointness, collar, positivity and embedded-source hypotheses. I found no additional high-area obstruction. This audit does not prove those hypotheses cover actual source current or all high-mass configurations, does not establish an efficient numerical flow oracle, and does not independently certify the separate capacity upper bound.

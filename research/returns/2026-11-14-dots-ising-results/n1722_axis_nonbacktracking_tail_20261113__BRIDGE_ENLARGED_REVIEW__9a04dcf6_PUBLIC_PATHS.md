# Independent review of enlarged-cutoff two-axis integration ingredients

Reviewer north_bridge. This checks the enlarged ingredients and exhaustive source split described below; final packaged theorem and artifact still require their own verification.

## Marked contour geometry and count
An embedded contractible filled contour projects to a cyclic interval. Any covered column contains some filled site but cannot be wholly contained as an essential vertical column in a contractible disk. Thus an outer physical vertical boundary edge exists in that column and supplies the stated column root. Contracting the zero dual edges gives nonbacktracking physical walks; for a fixed continuation sequence the zero-edge resolution is fixed. The12L3^P overcount is safe and has no missing ambient horizontal-root factor.

The corrected cover extraction removes ALL intersection with the remaining cyclic target, not just its initial contiguous prefix in a fixed linearization. Because the chosen projected interval contains the target's left endpoint, the remainder is one interval or empty. This remains true when the hole also covers a suffix across the chosen cut. Every selected contour has no target columns remaining, so it cannot recur. The accumulated progress is exactly c and is at most the selected contour's lifted width. The substochastic first-passage-tree bound is therefore appropriate; no extra continuation series or repeated activity is needed. Full-circle projections terminate immediately.

## Enlarged area arithmetic
For alpha4/3, the residual coefficients8/5 and68/5 have product544/25>16alpha. Therefore the joint area-width bound with residual6P/5 follows; the old11P/8 is not reused. For P<=400,R>=1000, the retained quadratic term is P²/2000. The finite P4..80 sum, intermediate81..400 geometric bound and entire P>=401 tail are correctly split. I reran enlarged_certificate.py: exact fractions certify tilted kernel<2/5, displayed .2729646945538627.

Unmarked activities are treated separately. Small perimeters use3exp(-39/5)<1/800; the large-perimeter isoperimetric bound supports either the fluid1/96 or GKP's weaker1/90 ratio. Both tails begin at401 and are included. I reran raised_pressure.py; the pressure remains<2 at the two large instances. It is smaller than the prior pressure allowance, so retaining the old failed-completion numerical exponents is conservative.

## Large-hole complement
If a filled embedded contractible area exceeds4R²/3, planar physical isoperimetry gives P>sqrt(64R²/3). Marking ONE such contour incurs the explicitly rooted100n q^H/(1-q) factor. Other contractible contours retain the ordinary exp(-8P) wall pressure; they are not also required to be long and are not assigned the field-reduced marked-cover activities.

This complement uses the actual global non-target field cap exp(phi n)=exp(32L) and the two-axis nonbacktracking count at total essential perimeter>=4L-16. It does not use a conditional Gibbs arrival law. I reran compute's exact atanh/log certificate: the complete rooted bounds are exp(-457) and exp(-6265). The source normalization is ZA>=w_minus and occupation uses v<=1.

## Intended exhaustive full two-axis split
For exactly two ACTUAL axial essential walls, first separate full-line sources, short-wall sources and total essential perimeter>=4.6L. The remainder has each essential wall>2L-8 and total<4.6L. Split it by whether any contractible filled area exceeds4R²/3. The large-area branch has the preceding marked-hole bound. In the complementary branch, either a conservative actual-majority completion succeeds (GOOD), or both fail (the enlarged marked-cover pruning). These are six overlapping positive branches, not disjoint probability events. All use the same original w,v,A,kappa,B and clock. No extra factor for possible c is needed because it is fixed by essential-wall geometry and maximized pointwise.

The minimum branch exponent remains140/4358, and6<e² gives138/4356 at R1000/10000. This is not a claim at R80/200, nor coverage of diagonal/no-essential-wall sectors. Actual contour homology cannot be replaced by the homology of an auxiliary plus seed.

## Final unrestricted theorem text inspected
I subsequently read the updated TWO_AXIS_SECTOR.md headed 'Reviewed unrestricted-defect two-axis sector closure'. It matches the six-branch split above and explicitly removes the contractible-area cutoff only after including the independently paid large-hole complement. The additional global winding tail has weaker source restrictions; adjoining it as a seventh positive branch still costs<e². For four or more essential walls below total5L, parallel primitive homology and the length floor force axial type and at least one short wall. Two essential walls of primitive Manhattan norm>=3 are in the global tail. Thus the stated remaining topologies, zero essential walls or exactly two primitive-norm2 diagonal walls, are a valid enumeration of remaining obligations, not a claim that their masses are small.

No additional gap found in that final integration. The conclusion remains finite-parameter original-occupation control, not a total exit/residence theorem or a claim at R80/200. Archive self-containment and fresh execution are a separate pending verification step.

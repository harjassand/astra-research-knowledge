# Restricted predecessor join: pure one-component bay closures

## Purpose
Positive magnetization of the post-entry FILLED domain is not earned by existing source reduction. The preceding thermal-flow theorem can instead protect a smaller set with a geometric hole. This avoids that particular positivity assumption for the pure bay-closing subfamily. It does not remove the current-bias or multi-fiber collision obstructions.

## Generalized geometric hypothesis
Replace the filled domain D in RESULT.md by any fixed connected set H with:
1. An embedded nonwrapping bounding rectangle;
2. Every physical boundary edge having its H endpoint fixed plus and its outside endpoint fixed minus at the source;
3. Fixed interior magnetization M_H>0;
4. Bounding-rectangle long side >2R/a, where a=.999996;
5. The fixed plus support in H already retaining a genuine M5-violating witness under arbitrary changes outside H.

H may have a geometric hole. Its perimeter counts ALL physical boundary edges, including those around such a hole. The exterior companion ensemble must satisfy the same explicit domain-area and pin-disjointness hypotheses as before, without imposing global M<0.

All proof steps remain valid. In particular the edge cancellation uses only the plus/minus signs across the original boundary, not simple connectedness. Filling H's bounding rectangle geometrically by two-neighbor additions cannot increase its TOTAL perimeter, including internal boundary. The field-tilt estimate controls the thermal spins in the newly filled hole as part of the shell. Endpoint magnetization after flipping all outside H is positive for every initially non-target state because M_H>0.

Consequently the same fixed-fiber capacity bound holds:

 C_growth >= Z_H/[kappa_H^-1+2n exp(4theta)].

## Actual pure bay-closing source class
Let D_pre be the filled domain of the one large predecessor component. Suppose it has positive magnetization, area at least4.01R^2, and an embedded bounding rectangle. Let z be the single new plus gate. Suppose z attaches to that component only (no companion merger) and closes a bay so that the resulting outer filled contour exceeds5R^2.

Protect H=D_pre union {z}, NOT the whole post-entry filled domain. H can leave the formerly exterior minus bay as a geometric hole. Its fixed magnetization is M_pre+1>0. Its bounding-box long side is at least sqrt(4.01)R>2R/a. The old plus component and the retained gate still form the actual violating outer cycle; changing spins inside the bay or farther outside cannot destroy that fixed plus witness.

For a pure one-component attachment, the actual augmented outside collar is minus; otherwise z would attach another companion. When that collar is included as the source's fixed-minus layer, the free exterior sees a minus boundary. No extra 'gate field' perturbation is needed: the gate and its adjacent pinned minus sites contribute fixed energy factors. If a proposed source only fixes the OLD collar and leaves new gate-neighbor spins free, this argument does not apply without a further perturbation/support estimate.

Thus this subfamily can use the thermal flow without assuming that the newly enclosed post-domain is positively magnetized. The source reduction at exactly4R^2 must still be sharpened to4.01R^2 or another threshold above4/a^2; that change is not declared earned here. The source's augmented contour convention must also confirm the stated pure-attachment and collar conditions.

## What this does not cover
- Gates merging other components, whose spins may need to be retained to preserve the violating witness;
- Winding or nonembedded bounding rectangles;
- A conditional law containing companion filled contours that cross frozen pins;
- The original current-density second moment, which is not the same as the auxiliary Gibbs fiber capacity;
- Summation over all predecessor domains without paying weighted contour multiplicity.

This is a restricted source-boundary join and an exact extension of the geometric flow lemma, not a full growth/residence theorem.

## Subsequent source join supplied by the structural-current lane

The companion result `../n1722_protected_support_join_20261113/RESULT.md` now strengthens the surviving predecessor threshold to4.01R², prunes total joined-companion filled area>=R², and pays nonembedding bboxes. It defines

 H={gate} union all joined old FILLED predecessor domains,

without filling a new bay. Under that result's source/topology hypotheses, H is augmented-connected, has plus endpoints on every physical boundary edge, has the true minus exterior collar, and satisfies M_H>1.005R²+1 and bbox long side>2R/a. All exterior companion domains have area<R² and avoid the pins. The retained plus support preserves the actual M5 violation, even for mergers and bay closures.

These are exactly the generalized geometric conditions above. Therefore the FIXED-H thermal capacity construction applies to every such surviving fiber, without assuming positive magnetization of the post-entry filled domain. This application imports the structural-current result's exceptional-current and acquisition assumptions; it does not independently reprove its contour classification or scalar certificates.

Two barriers remain unchanged: actual current density relative to the Gibbs fiber, and aggregation of flows over different H and frozen interior patterns. A geometric source join is not a current-moment theorem.

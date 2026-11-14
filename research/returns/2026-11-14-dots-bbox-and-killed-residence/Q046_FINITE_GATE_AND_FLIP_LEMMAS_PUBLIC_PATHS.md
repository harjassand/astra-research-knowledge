# Finite gate topology and direct whole-domain flip preservation

These are explicit geometric proofs for the implemented fixed-diagonal augmented graph. They concern the new bbox trial; they do not prove magnetic-word counts, flow preimages, or kinetic efficiency.

## 1. No first winding or noninjective projection at a bbox exit

Let every old augmented plus component have a consistent integer lift of bbox widths w,h withw+h≤H, and supposeH≤L/2. Add one sitev. Only old components adjacent tov can join it. Setv's lift to(0,0).

For an affected component, align one adjacent vertex's lift to its actual displacementδ∈[-1,1]². If a second adjacent vertex required a different periodic alignment, their coordinate displacement inside the old lift would have absolute value at leastL−2. Its bbox width would then be at leastL−1, impossible because each old width≤H−1. Therefore every neighbor of the same old component aligns consistently.

Each aligned component lies in[-(H−1),H−1]²: its anchor-neighbor lies within one coordinate unit ofv, and its coordinate range has length at mostH−2 beyond that neighbor. There are no edges between distinct old plus components. All new edges are throughv and agree with these aligned lifts. Hence the merged component has a consistent lift, and its bbox width and height are at most2H−1<L. Filling bounded holes cannot enlarge its bbox. Its filled domain therefore projects injectively to the torus.

Thus no addition from this basin can create a first winding component or noninjective filled-domain projection, for ANY number of affected old components. AtL1600,H795 the new width/height bound is1589<1600. This does not say the new bbox semiperimeter remains≤H: that is precisely the structural exit being sampled.

The local fixed-diagonal planar resolution still specifies how vertex contacts connect; it introduces no periodic identification inside this injectively projected bbox. Keeping the old winding/topology overcount in the scalar certificate is conservative, but this finite argument means those first-exit failures need not be assumed or separately imported for this trial.

## 2. The augmented collar follows from the hull definition

For an old augmented plus componentC, letD(C) consist ofC and all bounded components of its complement in the SAME augmented graph, in the consistent lifted plane. This is exactly the operation implemented byfill_holes. BecauseC lies in its bbox, all points outside that bbox belong to one exterior complement component, soD remains inside the same bbox.

Ifu∈D has an augmented neighbor outsideD, thenu∈C. Otherwiseu would belong to a bounded complement component connected by that edge to the exterior, a contradiction. Therefore every augmented-boundary vertex ofD is an old plus vertex ofC.

Flip every spin ofD, preserving rather than discarding its interior information. New plus spins insideD are old minus spins, hence lie inD\C and have no augmented edge outsideD. Every newly created plus component remains insideD. Exterior plus components are unchanged and cannot join through the flipped domain. Their bboxes therefore do not grow. This proves bbox-cut preservation directly.

For several disjoint outermost domains, apply the same argument to each. Distinct such domains cannot have an augmented edge between them: both edge endpoints would be boundary vertices in their original plus components, forcing those components to be identical. The flips are compatible and preserve the cut. Given the domains, simultaneous flipping is an involution and hence injective.

## 3. Laminarity and structural gate provenance

The remaining qualitative planar fact is laminarity of filled outer domains of distinct augmented components. Under a fixed one-diagonal-per-plaquette triangulation, resolve each checkerboard contact according to that diagonal (the rule implemented infilled_trace.py). Different plus components become disjoint planar regions with disjoint outer Jordan boundaries. Their filled outer disks are therefore disjoint or nested. The old small-bbox domains are embedded in the torus, so the same conclusion holds for their contractible disks. This is ordinary planar separation, not a new quantitative contour estimate.

If an added site lies inside an old filled domain, the boundary property above prevents it from connecting interior components to the exterior. Any new component remains in that domain's bbox, so no structural bbox exit occurs. Consequently a structural gate lies outside all affected old filled domains; its adjacent components are outermost. The exact provenance validator should still check these conditions rather than infer them from a simple word or an empty thermal background.

## 4. Native energy ratio with thermal interiors retained

At each physical boundary edge of an actual old filled domain, the interior endpoint is plus and exterior endpoint is minus. FlippingD aligns these boundary spins, while every interior bond has both endpoints flipped and is unchanged. Hence, fororiginalX andinverseY obtained byflippingdisjointD_i,

w(X)/w(Y)=exp[-8ΣP_i+.04Σ(V_i−2|Y_plus∩D_i|)]
          ≤exp[-8ΣP_i+.04ΣV_i].

No equality between filled area and actual plus count is assumed. check_thermal_flip.py verifies this exact rational energy identity on actualL1600,400×395 domains with interior singleton/pair defects and an exterior thermal spin. The extra factorsareexp(-.08) orexp(-.16), as appropriate.

## 5. Executed finite support

The supplied exact tests cover881 small connected hulls across three diagonal patterns, vertex-touching contour reconstruction, nested thermal provenance examples (in sampler_resume), and torus boundary/gate tests. They support the implementations; the proofs above, not extrapolation from those tests, justify the finite geometric statements.

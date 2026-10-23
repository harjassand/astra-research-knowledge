# One actual degree-three atom root has a missing neighbor color

Bounded local contribution to Pro2 Cycle11, 23 October 2026. The principal
researcher owns the global bridge composition. This note proves the new local
interface and its intrinsic realization; it is not a global recovery theorem
or a claim of historical priority.

## 1. The local theorem

Let G be a finite simple two-connected chordless graph of treewidth at most
two and maximum degree at most four. Let u be an ACTUALLY specified vertex
of degree three. There exists a constructive star-four coloring c of the
ORIGINAL graph such that

    |{c(w): w adjacent to u}| <= 2.

In particular there is a color z different from c(u) and absent from the
actual neighbor-color support of u. Actual multiplicities are retained:
three neighbors occupying at most two colors include a repeated channel,
which is unflagged by the star condition. The missing-channel conclusion
is stronger and is what the bridge composition can use.

For any prescribed two distinct colors A,Z, a single global permutation
of the realized block coloring makes c(u)=A and Z absent from its neighbor
support. Adding one new parent vertex of color Z joined to u produces an
isolated edge in the pair {A,Z} and preserves the star property. This does
not prescribe any independently chosen profile at another vertex of G.

The theorem applies to every specified degree-three root, not merely a
terminal selected for convenience by the old unmarked normalizer.

## 2. Intrinsic preparation at an original edge

Choose any actual incident edge uv of G. Temporarily subdivide it by a new
symbol w, obtaining G': remove uv and add uw,wv. This is preparation only;
no action on the subdivided graph is queried.

Subdivision preserves two-connectivity, chordlessness and the degree cap.
For treewidth, retain a width-two decomposition of G and attach bag {u,v,w}
to a bag containing uv. All original edges remain covered except uv, whose
cover is no longer needed; the two new edges are covered by the new bag.
This proves treewidth at most two for G'.

The actual degree-two marked normalizer from Cycle10 can therefore be used
at w. It produces a native H8 expression for

    H = G' - w = G - uv

with terminals u,v and the exact original edge support minus uv. Its port
loads are (2,deg_G(v)-1), hence (2,d) with d in {1,2,3}. The old fixed
certificate classifies this expression into one of the 18 active families
with those degrees. No old closure search is executed.

One can see the essential chordless property directly: every simple u-v
path in H closes with the original edge uv to a cycle in G. A chord of
that H path would be a chord of the resulting original cycle. Thus all H
terminal paths are induced, the property used by the inherited H8 native
normalizer. Parallel single-edge branches are consequently absent from
the relevant normal form.

The executable adapter bijectively relabels u to local 0, v to local 1,
and all other original vertices to the remaining local IDs. It uses the
temporary symbol n only in the normalizer. It then realizes H on its
original n vertices, restores exactly uv and maps colors back to the
original IDs. The returned support has exactly n vertices and the original
edge list; there is no temporary vertex or formal edge in any action.

## 3. Exact terminal-edge closure criterion

For a proper star coloring of H with distinct nonadjacent terminals, write

    (a,b,dL,NL,FL,dR,NR,FR).

The two visible terminal colors are a,b. N is actual neighbor-color support;
F contains color q when a q-colored neighbor has another neighbor with the
terminal's color. The existing guarantee targets upper-bound N,F and retain
actual degrees and colors exactly.

Adding the original edge uv preserves the star property exactly when

    a != b,
    b not in FL,
    a not in FR,
    not (b in NL and a in NR).

Indeed an old two-colored P4 cannot appear except through the new edge.
If the new edge is an end edge of that P4, the old three-vertex continuation
is exactly the corresponding far-repeat flag. If the new edge is the middle
edge, its two old continuations are exactly b in NL and a in NR. The two
outer vertices are distinct because their colors differ. These cases cover
every new P4, and each failed condition constructs one. Nonadjacency before
the addition and original simplicity prevent duplicate edges.

At the restored root u, the actual new neighbor support is NL union {b}.
Its far flags are FL union ({b} if a in NR else empty). Therefore it is
enough to choose a valid edge-closing target with

    |NL union {b}| <= 2.

All these acceptance predicates are downward closed in N,F. Thus checking
them on a saved upper-bound target proves them for its actual realized
coloring. The restored root degree is exactly 2+1=3; multiplicities are not
replaced by their target bounds.

## 4. Literal projection of the existing certificate

The exact fixed source is loaded_star_certificate.json, 982625 bytes,
SHA256 63f4cdfd7ccc3b3159782a28a144a199422a315975aa207e5d144e8659e53525.
Its 73-family grammar theorem is an accepted dependency, not reproved here.

The new projection in results/DEGREE3_PROJECTION.json records one literal
target and missing color for every family of degree (2,d), d in {1,2,3}.
The 18 family IDs are:

    2,4,12,14,19,24,26,30,31,33,40,44,45,52,53,54,62,63.

Every one is nonempty. Each row includes its inherited target index and
complete eight-entry target, the restored neighbor-support upper mask,
far-flag upper mask and missing color. src/project_degree3.py checks only
the new edge-closure conditions and missing-channel requirement against
the fixed targets. It does not regenerate the old grammar closure.

By the inherited finite-certificate induction, the selected target has an
actual H coloring below its support/flag bounds for every expression in
that classified family. Section 3 restores uv safely. Section 2 proves
that every admitted actual marked atom reaches one of these families.
This establishes the theorem at arbitrary graph size. The finite native
examples supplement this proof rather than supplying its all-size scope.

## 5. Native implementation and actual diagnostic

src/degree3_atom.py provides Degree3AtomOracle.color(n,edges,mark,neighbor).
It returns the original edge list, actual colors, actual marked multiplicities,
actual far flags/missing channels, original protected edge, selected target
and native normalization evidence. A direct full-original-support check
rejects any monochromatic edge, any actual bichromatic P4, any root-degree
change or absence of the promised missing channel.

For integration, Degree3AtomOracle.from_prepared(verified_marked_bundle,
projection_path) reuses the Cycle10 MarkedAtomOracle's already hash-bound
certificate/table/index. Its only new preparation is the 18-row projection
check. The caller must supply that verified object, not an arbitrary table.
Standalone construction instead loads and binds the certificate itself.

The saved six-case native diagnostic includes both hubs of theta(2,2,2),
both hubs of theta(2,3,7), and both degree-three roots of a graph containing
an actual degree-three/degree-four adjacent pair. The latter is intrinsically
assembled from two a-b path2 branches and the branch a-x, followed by three
x-y path2 branches, followed by y-z-b. Its degrees are 3,3,4,4 at a,b,x,y.

The marked a root with protected edge ax has deleted-edge loads (2,3),
classifies to family24 and realizes root neighbor multiplicities (0,1,2,0),
far flag {1}, and missing channel3. Thus the actual test exercises a nonzero
flag; the theorem does not silently assume that every far flag vanishes.

The diagnostic separately enumerates simple original P4s instead of using
the producer's multiplicity edge test. It checks each missing color by
adding one genuinely new leaf in that color and verifying the star property
again; this demonstrates the local bridge interface, not global composition.
This alternate checker was written by the same contributor, so it is an
independently formulated calculation, not an independent scientist's review.

## 6. Costs, changes and scope

The recorded new projection took 0.022508045003633015 seconds wall and
0.022507138 seconds CPU, with 19922944 bytes peak process RSS. It includes
fixed-source read/parse and the 18-family scan, but excludes output serialization.
An initial exploratory projection of the same new conditions was unmeasured;
its cost is unknown, not zero.

The six-case native diagnostic took 0.027310747995215934 seconds wall and
0.027306322 seconds CPU, with 21315584 bytes peak process RSS. It includes
0.024846146996424068 seconds of fixed-certificate preparation, already inside
the body total. Scientific JSON serialization, interpreter startup, source
reading, authoring, proof discovery/review and integration are excluded.
Their totals remain unknown. No unsuccessful scientific execution occurred.

The sixth case's descriptive name was corrected from neighbor4 to neighbor2;
its actual edge, degrees, graph, coloring and checks were unchanged. No
scientific result was rerun for that label correction. A convenience method
for sharing an existing verified bundle was added after the standalone run;
the parent receiving operation can exercise that method without rereading
the fixed table. Preserve this distinction in execution accounting.

Reference work is O(n+m log m) with canonical sorting, O(n+m) storage and
linear expression traversal, plus fixed-certificate preparation or reuse.
This is a local coloring interface. Full original-action decoding, global
component control and practical comparison belong to the parent's operation.
No all-real query lower bound or historical-priority claim follows here.

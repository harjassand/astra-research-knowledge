# Concrete local-star certificates

**Result:** the declared Figure20 T-book interiors admit fixed-edge-basis vertex generators of weight at most **5**. The additional C4, K2,d, normalized K3,d and W5 link inventory admits weight at most **8** across all tested parity-star anchors and the recorded Par4 path-tree convention. These are exact local algebra certificates, **not yet an exhaustive global-family vertex-type theorem**.

## Computations and scope

`compile_t_vertex_stars.py` uses the actual six-/nine-polygon lists, the existing sheaf-incidence compiler, and the declared intrinsic-parent-page normalization. Off-seam vertices are namespaced by parent page; only the O–P–Q (or O–P–Q–R) seam is shared. It considers all seven nonempty page subsets, both seam colors, and two explicitly artificial outer-boundary closures (all-blue or all-red): 56 variants, 532 vertex stars.

The 42 seam-interior stars have no exterior port edge. Their full edge-basis supports agree between the two artificial boundary closures. Their maximal canonical generator weight is7; their optimized weight is at most5 and per-vertex qX at most2. This independence is verified, not inferred from a picture. They remain conditional on the declared complete selected-page seam incidence; they are not claims about uncompiled exterior endpoint gluing.

Full-page examples:

| Chart / vertex / seam color | Canonical weights | Optimized weights |
|---|---|---|
| doubled T / P / blue | 4 | 4 |
| doubled T / P / red | 3,6 | 3,3 |
| refinement / P / blue | 5 | 5 |
| refinement / Q / blue | 5 | 5 |
| refinement / P / red | 4,6 | 4,4 |
| refinement / Q / red | 4,7 | 3,4 |

Every port-incident star is labeled `EXTERIOR_TRUNCATED_ARTIFICIAL_BOUNDARY_CLOSURE`; its patch parameters must not be called physical family parameters.

## Complete abstract link compiler

`compile_link_vertex_stars.py` treats link vertices as edge germs and link edges as incident physical faces. The vertex stalk is exactly the set of face labels whose restriction at each link vertex belongs to the specified repetition/parity edge code. It compiles the physical edge-coordinate image and checks that every proposed vertex generator has zero face syndrome.

It covers 27 template/color families and **11,591** independent basis variants:

- C4 ordinary face-interior link: weight4.
- K2,d edge-subdivision links, d=1,2,3,4: maximum weight5 for d≤3; blue d=4 needs6; red d=4 at most5.
- K3,d normalized attaching-endpoint links, d≤4, all old/new colors: worst weight6 for d≤3; worst weight8 for d=4. These are **normalized endpoint templates**, not identifications with raw OPQ subdivision stars.
- W5 glued-cross endpoint wheel: blue weight5; red at most5 for every tested anchor/basis (best choices have4).

The largest vertex-stalk dimension is6. Every Par3 star anchor is enumerated. Each Par4 germ independently permits all four star anchors and the legacy path-tree basis `[3,5,12]` from `aligned_tree_basis_test.py`. Thus mixed choices of the two recorded conventions are included. Arbitrary GL(3,2) Par4 bases are not included.

Observed optimized qX is at most6 **at one vertex**, with the worst case in normalized K3,4 red/red. If this template inventory exhausts actual final vertices and fixed physical edge bases agree at both endpoints, it would imply qX≤12 globally. That conditional implication is not itself a closure certificate.

## What the optimization proves

For each fixed edge basis, the script enumerates every nonzero vector in F_v, maps it to physical qubit coordinates, and orders by physical Hamming weight. Linear-matroid greedy chooses a basis of minimum total weight and minimum bottleneck weight. It checks rank and equality of the canonical/optimized spans. The chosen tie-breaking is deterministic. qX is an observed upper bound for that basis, **not** a separately minimized objective.

Changing the vertex-stalk generating basis changes the actual Hamiltonian term list even though it preserves the stabilizer group. These output bases are candidate physical Hamiltonians. The source thermal decoder/full-trace theorem must be bound to that chosen basis; old Gibbs weights are not silently retained.

## Path-tree Z-weight opportunity

The legacy Par4 basis is a path on its four incident faces: `[f1+f2, f1+f3, f3+f4]`. Every face coordinate appears in at most two basis qubits. Par3 star bases also have maximum face-incidence2; repetition bases have1. If this path-tree convention is consistently adopted on all Par4 stalks, polygons with at most five edges obey **wZ≤10**, rather than the basis-agnostic15.

The existing aligned-tree resolution test verifies degree-one projection columns and inclusion rows at most1 for its matching Par4 split. A full-family claim still needs the same next-generation basis consistency argument used by the governing distance proof. Combining that consistency with exhaustive vertex-type closure could yield a no-auxiliary-cone candidate with wX≤8, wZ≤10. This is a concrete target, not a certified K10 family here.

## Exact remaining exterior/type data

No Euclidean coordinate table is necessary for the algebra. The necessary certificate is a finite, complete **colored vertex-link inventory with physical edge bases** and a proof that every construction step maps the inventory into itself. Specifically:

1. For each chart boundary vertex, identify which exterior face sectors and edge germs are glued to its ports. Supply complete coface lists and abstract parent-face IDs; geometric coincidence is not identification.
2. Bind the O and Q endpoints of the left T list, and O and R endpoints of the right list, to complete neighboring links. All non-seam outer vertices likewise need their adjacent page/sheet/band sectors, not an arbitrary degree-one closure.
3. Give the final links at inherited old vertices, glued-cross seams, T-cylinder attachment endpoints, free crossings, and physical domain boundaries, including page deletions and both colors. K3,d/W5 are admitted abstract templates only until this match is proved.
4. Include the actual degree-four tree-resolution endpoint links and the inherited seam/auxiliary-strip port identification. Resolving an edge stalk does not by itself specify the two endpoint vertex links.
5. Record the ordered incident-face labels and the physical Par3/Par4 basis at each germ, and verify that each global edge has the same basis at its two endpoints. A locally best anchor is not automatically a globally compatible one.
6. Prove one-step closure for ordinary refinement, blue/red doubling, and the finite T/glued-cross resolutions, relative to every exterior port. This can be a finite local-template argument; a growing full-family generator is not required.

Once these items are supplied, the existing link compiler computes the remaining matrices directly and can exhaust the finite list. The task is now a precise finite closure/port-binding problem rather than an unspecified request for a whole global incidence table.

Files: `t_vertex_star_results.json`, `t_vertex_star_summary.json`, `link_vertex_star_results.json`, `link_vertex_star_summary.json`, and their two reproducing scripts.

## Extended sweep: all path choices and boundary deletions

The later requested sweep is in `compile_extended_links.py` and `extended_link_results.json` (about28 MB), with concise summary files. It fixes every red degree-four germ to one of **all12 labelled Hamiltonian-path tree bases** (permutations modulo reversal), not merely the earlier legacy path, and independently varies every Par3 anchor.

In addition to the core links, it includes:

- K3,d for d=1,2,3 with one specified link edge subdivided once;
- theta graphs with path lengths (1,2,2), (2,2,2), and (1,2,3), all branch color combinations;
- C4 with a center joined to each nonempty subset of outer vertices;
- every nonempty face-subcomplex deletion of these added links.

Deletion means removing selected link edges, with isolated zero-face germs omitted. Colors at declared branch germs are inherited. If deletion turns an otherwise unlabeled degree-two subdivision germ into a degree-one boundary germ, both Rep1 and Par1 choices are explicitly enumerated. This avoids guessing a boundary color from span11.

**8,207 distinct colored links and 164,088 physical edge-basis assignments pass.**

| Category | Maximum optimized X weight | Maximum chosen-basis qX per vertex | Maximum dim F_v |
|---|---:|---:|---:|
| Core C4 / K2,d / normalized K3,d, d≤4 | 8 | 5 | 6 |
| One-edge-subdivided K3,d and deletions, d≤3 | 8 | 4 | 4 |
| Theta graphs and deletions | 5 | 2 | 2 |
| Partial wheels and deletions | 5 | 4 | 4 |

Some mixed-color **boundary deletions** of subdivided K3,3 attain weight8. It would be incorrect to test only full graphs and quote the smaller full-graph bound. The exact examples, edge masks, physical bases and optimized generator supports are recorded.

If the final-family port/type closure is proved, these certificates support the conditional no-added-data-qubit bounds

 wX≤8, qX≤10, wZ≤10, qZ≤4,
 K_native≤10, D_native≤1+10(14−1)=131.

Here qX≤10 sums the two endpoint contributions to an edge qubit, and wZ≤10 uses the path-tree face-incidence bound. The path on each global edge can be chosen once from its ordered face IDs, so local best-anchor choices need not be coordinated between endpoints; all paths have been checked. The required global closure remains unproved by this calculation alone.

### Thermal consequence available after that binding

The matrices also establish dim F_v≤6 for this inventory. Changing a vertex's chosen generator basis is an invertible syndrome transform within a block of size at most6. For the actual new positive stabilizer Hamiltonian, local-stochasticity therefore transfers to the old syndrome coordinates with the safe bound q_old≤6 q_new^(1/6), i.e. B_new≥6[B_old+log6]. This is a whole-Gibbs bound, not equality of the two generating-set Hamiltonians. Finite local edge-basis changes are Clifford isomorphisms and can be compared once at the final level, avoiding an artificial loss at every recursion step. The full decoder/trace/native join still has to charge these finite transforms and its new constants, but no HLL cone volume M is introduced.

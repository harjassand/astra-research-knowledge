# Constructed intrinsic-page completion and relative normalization

This supplements RESULT.md with a specified completion rather than leaving arbitrary unlisted cofaces. It retains the source geometric maps but gives abstract identity precedence over coordinates. It proves the claims below for this completion; an independent exact-cell rendering of every source drawing is not claimed.

## Definition by generators and ports
A page is an abstract disk with an ordered boundary word, a parent ID, and the source's piecewise-cellular geometric map. Interior polygon edges identify only within that page. A seam is an ordered path with its inherited code and ordered incident page list. Seam endpoints and external page boundary arcs are named ports. Only equal named inherited ports are glued. Free crosses are separate IDs even at equal coordinates; glued crosses identify the four rib arcs in one page. Copies carry a sheet bit. Cylinder pages carry the originating rib-arc ID and inherit the old page ID through that arc.

The finite chart generators are:
1. Ordinary parent face, edge-book, or vertex-star subdivision, with source lattice route.
2. The two Figure20 three-page-book words explicitly listed in PARENT_FACE_COMPLETION.md. Shared seam O-P-Q or O-P-Q-R; all other boundary arcs remain external ports. Each page's dual polygon graph is a tree.
3. Rotations/reflections of generator 2 and its recursive repetition, with relabeled ports. Thus Figure22/23 variants do not acquire any new abstract identification merely when their pictures overlap. A recursive step replaces a disk by another disk with the SAME ordered exterior port word, subdividing that word as needed.
4. Degree-four seam resolution: two degree-three seam paths joined by one auxiliary strip, preserving the four ordered exterior page ports. The code on both seam paths is Rep3 or Par3 according to the inherited Rep4/Par4 code. The transverse exact sequence is the tree resolution in RESULT.md §2.
5. Free-cross normalization: disjoint page disks with their separate exterior port words; no shared edge or vertex is added.
6. T subcharts: delete the absent pages and use Rep/Par on the surviving old seam incidence, including the degree-two span(11) and appropriate degree-one code. The interior page disk subdivision is unchanged.

This is a recursive incidence definition: every new internal cell belongs to exactly its declared page or seam; external attachment is solely through the inherited port word. It forbids extra interior cofaces, hidden seam cycles, and coordinate-driven identifications. It adds no geometric face images and does not alter source boundary routes. The degree-four auxiliary strip is the source Figure24 split, with its specified exterior four-page grouping; if that grouping is not specified, either fixed grouping is a constructed choice and must be retained in the next-level parent IDs. Packet accounting may safely allow all six face pairs, so it does not depend on this choice.

## Relative normalization theorem
Each chart admits a bounded cochain contraction to its unsplit parent chart, RELATIVE its entire external port subcomplex.

For a disk subdivision: cancel a leaf polygon along its unique interior edge, iterating the page dual tree; use interval subdivision cancellation on boundary subdivisions. These are elementary relative cell cancellations with transported sheaf coordinates. They leave every external port restriction map unchanged. For a general disk tiling choose a spanning tree and finish with the standard relative disk complex, retaining its one degree-two generator.

For a three-page book: perform these cancellations independently on its three disk pages, retaining the shared seam path, then cancel subdivisions of the seam interval with its same inherited L_e. This is the edge-book chart, not a topological identification of collapsed geometric vertices. Figure20's relative complexes are explicitly tested by boxed_relative_certificate.py: relative external page arcs, the two actual polygon lists have H0=H1=0 for either inherited color. H2 is 2 for Rep3 and 1 for Par3, exactly F2^3/L_e.

For degree-four resolution: the transverse new-edge-stalks -> auxiliary-face-coordinate map is surjective, with kernel exactly old L_e. Cancel its unit pivot, then tensor with seam interval subdivision. All four exterior page ports remain fixed. No Hamming-nonincreasing claim is made for this cancellation's degree-two projection; the Rep4 auxiliary maps to a pair.

For a free cross take the direct sum of its separate disk contractions. T subcharts are the same disk/interval proof with fewer pages. All maps are relative the named exterior ports; therefore adjacent normalized charts glue automatically with the untouched surrounding cells. This is stronger than checking each chart's absolute Betti numbers.

## Applying normalization to the ribs
Source W0 contains no ribs. Normalize its disjoint boxed charts relative their exterior ports BEFORE decomposing the complement of the rib graph. Thus the actual degenerate triangle need not carry its own hashtag. The normalization does not cross or modify a rib, and induces a contraction of C(X',R) onto the normalized pair complex. The normalized book/vertex charts have the ordinary cell-stratum complement: relative vertex costars, edge costars, and face chambers. Their H0,H1 vanish by RESULT.md §1.

The constructed completion ensures the normalized exterior seam graph is the original inherited graph: no closed seam can appear inside a chart because generators 2–4 contain only an interval or its tree resolution, generator 5 is disjoint, and all noninherited endpoints are internal subdivision vertices. Hence there is no extra local chamber cycle hidden in a collapsed W0 patch. Coalescing several physical old stars into one normalized chart is allowed; it is the relative contraction, not a claim they were one physical vertex, that proves exactness.

All chart sizes are uniformly bounded at ell=8. Recursive boxes refer to a finite template, not to an ever-growing matrix: previously created cells are normalized in the present fixed-size box only. Disjointness of the boxes makes simultaneous normalization local.

## Global shifted-rib isotopy
Define h(t+8)=h(t)+8 with knots

 t: 0, 2.5, 4, 5, 5.5, 8
 h: 0, 2.5, 3, 4, 5.5, 8.

The product warp H=(h,h,h) is monotone, has displacement at most 1 per coordinate, fixes neighborhoods of all coordinate residues 0,±2, and sends rib planes 4,5 to preimage planes 3,4. Its straight isotopy also fixes those neighborhoods. Refined residual boxes lie within normal extent 2+2/7<2.5, so they are fixed in their normal directions. Tangential long strips are preserved setwise; their endpoints lie in the fixed coarse-vertex neighborhoods. In the constructed page atlas, all bends and inherited seam endpoints use these fixed source routes. Thus H lifts labelwise to the abstract pages and preserves seam identifications, including separate free-cross sheets. It only changes ordinary subdivision grid positions.

A bounded common subdivision gives the cellular prism identity r_b q+r_a=d t+t d, without setting r_a=r_b. The cochain section is Jx=(x,qx,tx). Relative chart normalizations commute with this isotopy up to a bounded relative cellular homotopy because they fix all ports and ribs. This yields the bounded maps and degree-one correction identity on the actual cells of this constructed completion, not only on its normalized macrocomplex.

## Exact evidentiary boundary
The completion fixes all incidence choices by intrinsic pages, ordered seams, and inherited ports. It is compatible with the source's stated three T surfaces sharing O-P-Q, four glued-cross bands, separate free-cross surfaces, explicit Figure20 polygon words, and unchanged exterior routes; it uses their given geometric maps, hence adds no geometric multiplicity. The source figures do not provide an independent machine-readable parent-ID/port atlas. Therefore “the constructed source-compatible completion has these maps” is earned here, while “every conceivable reading of an omitted source incidence has these maps” is not asserted. Any externally specified identification that contradicts these named ports would require revising the completion and retesting it, rather than silently overriding that identification.

## Common blue lift and the two readout homotopies
The periodic warp fixes normalized parent strata and its cellular prism is chosen relative inherited ports. Therefore the two old-level subdivision projections commute with this identification (use the same old face/edge IDs for both sides). Choose one old-level inclusion and apply the prism construction to it. This gives a common J with PA J=PB J=1. Contract ker PA and ker PB separately onto their degree-two residuals while holding that section fixed. The resulting hA,hB satisfy the degree-one logical identities. In degree2 one has

 1-J PA = d hA + QA,    1-J PB = d hB + QB,

where QA,QB are the bounded-local residual/metacheck projectors. They vanish on actual syndromes d e. Thus fA=hA sigma and fB=hB sigma give exact common-lift cleaning identities on valid syndromes. Restrictions to active components require the separately specified residual-row dependency gate; global validity alone cannot justify arbitrary component restrictions.

On valid sigma, applying PB to the first identity gives

 PB sigma+PA sigma = d (PB hA sigma).

This is the bounded-local K needed to patch different sheet choices, with K=PB hA. It retains the projected correction term. It does not require PA and PB to agree on invalid arbitrary face vectors, for which QA may be nonzero.

## Physical port rule clarification: no accumulating common refinements
All common subdivisions in the homotopy proof are VIRTUAL and composed back to the original physical chart cells. They are not added to the next physical level. In particular a rational prism subdivision is never iterated as part of the code family.

Build the inherited abstract skeleton first: one old edge ID owns a single ordered routed word of source unit-length or zero-length edges, including its endpoint vertex IDs. Every incident page references that same word. Page interiors are completed relative this already fixed word. Port matching requires equal inherited lineage and exact word, not an affine identification of unrelated arcs with different numbers of segments. The exterior arc lengths of the two Figure20 charts therefore do not induce a universal fractional mesh or new physical vertices. The phrase 'subdividing that word as needed' in generator 3 means an ordinary scaling step's prescribed unit-edge subdivision, or a virtual comparison subdivision, NOT an arbitrary new physical common refinement.

An exact executable lattice-coordinate implementation still needs the finite routed skeleton words for every source template. The algebraic completion and chart contractions define how to glue and normalize them and rule out ambiguous coordinate gluing; they are not an independently checked list of those coordinate words. The finite inventory audit should record this distinction rather than treating symbolic relative-port compatibility as a measured physical atlas certificate.

The executable boxed certificate was extended to all seven nonempty page subsets, both Figure20 polygon templates, and both inherited seam colors: 28 relative complexes, all H0=H1=0. Degree-one inherited seams are distinguished from external degree-one ports, so the red-zero versus blue-full boundary codes are genuinely tested. This verifies the deletion subcharts rather than extrapolating them from the three-page ranks.

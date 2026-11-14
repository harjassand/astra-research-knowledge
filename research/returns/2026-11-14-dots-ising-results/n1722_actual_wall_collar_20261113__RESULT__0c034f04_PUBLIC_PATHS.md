# Actual noncontractible wall: plus-collar perimeter lemma

## Statement and scope
On the square torus with the program's fixed SW–NE zero-coupling triangulation, let gamma be one embedded noncontractible resolved domain-wall cycle of a spin configuration. Let p be its number of crossed **physical** nearest-neighbor edges. Let D contain every plus endpoint of every augmented edge crossed by gamma, including zero-coupling diagonal edges. Then

    P(D) <= 2 p.

P counts physical nearest-neighbor bonds only. This is a geometric lemma, not an occupation theorem or a complete monotone-growth construction. It is false for general contractible walls. It does not claim that D is nearest-neighbor connected.

## Proof
Classify triangles traversed by gamma into four types:

* A: two plus vertices; both crossed edges physical.
* B: two plus vertices; one crossed edge physical, one diagonal.
* C: one plus vertex; one physical, one diagonal crossing.
* E: one plus vertex; both crossings physical.

Every physical crossing belongs to two visited triangles, so

    2 p = 2 A + B + C + 2 E.

Push each wall segment to its plus side inside its triangle. In an A triangle this traverses the diagonal plus–plus edge; in a B triangle it traverses a physical plus–plus edge; in a C or E triangle it stays at the lone plus vertex. The resulting closed augmented-lattice walk has vertex set D and is homotopic to gamma. Indeed the elementary deformation is within the closure of each visited triangle and the deformations agree on shared crossed edges. It need not be simple, and may repeat edges.

Let G be the underlying trace graph, with v vertices, a distinct diagonal edges and b distinct physical edges. It is connected and contains a noncontractible cycle, so v <= a+b. The induced physical graph on D contains all b physical trace edges, hence

    P(D) <= 4v - 2b <= 4a + 2b <= 4A + 2B.

This argument explicitly pays repeated vertices and edges; it does not assume that the B steps are distinct.

The signed curvature identity for a noncontractible resolved wall is

    2(A-E) + (B-C) = 0.

One way to check the local identity is to contract the zero dual edges. At a triangle with two physical crossings the resolved square-dual walk turns by a signed right angle, contributing +/-2 in units of pi/4. Triangles with a diagonal crossing occur in pairs across that zero dual edge: their signed contributions +/-1 combine to a right-angle turn or a straight passage. The sign can be chosen consistently by orienting gamma with the plus side on the left; reversing the convention reverses the entire sum. An embedded essential curve on a flat torus has rotation number zero: it is isotopic to its straight primitive representative, and rotation number is invariant under that regular isotopy. Thus its total signed turn vanishes. Zero-edge contraction is interpreted with the original triangulation's local resolution, not as an unresolved square-dual crossing.

Combining the two displayed identities gives 4A+2B=2p and proves the result.

## Visibility and a separate unresolved path issue
If both endpoints of every gamma-crossed augmented edge stay fixed, each traversed triangle keeps all three spins fixed. Therefore gamma remains exactly the same resolved dual component, rather than merely a homologous curve. At a native transition there are at most O(n) such visible cycle labels. This is useful for potential congestion reconstruction.

But keeping both collars fixed can block nearest-neighbor bootstrap growth. GKP's independent exhaustive 4x4 test found 768 axial-wall cases (among 31,296 examined) for which the pinned two-neighbor closure does not form a nearest-neighbor winding cycle. Consequently the collar lemma does NOT complete arbitrary-wall occupation control. A valid native path with paid congestion, or a different reconstructible label, remains necessary. Completing a zero-temperature bootstrap argument is not equivalent to controlling the positive-temperature native paths.

## Checks and provenance
The matching independent randomized check is fluid's `ising_right_only_bootstrap_20261113/collar_test.py`: 3,744 noncontractible wall cycles from 5,000 seeded 8x8 configurations; exact curvature identity and P(D)<=2p passed, maximum ratio 2. Its contractible search found p=18,P(D)=42, explaining the essential-homology restriction. Those checks support but do not replace the proof above. The proof uses elementary trace-graph Euler counting and rotation number, not a claimed new general theorem.

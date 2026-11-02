# Root finite-packet metric for the explicit small-scale family

2026-11-02. A concrete metric construction, not yet a full-family lifetime theorem. It addresses an actual obstruction to raw Hamming contraction, not merely a proof constant.

## 1. Why raw projection can inflate
A blue repetition-four edge resolved into two repetition-three edges has fine syndrome columns

 L=f1+f2+a, R=f3+f4+a,

where a is the new auxiliary face. A chain projection retaining the L qubit has P2(a)=f3+f4, P2(fi)=fi. Thus a SINGLE fine auxiliary syndrome coordinate projects to TWO old faces. Raw parent-face parity is not a globally nonincreasing syndrome projection. Actual admissibility must not be assumed to forbid all such packets: the constructor found valid pairs of auxiliary defects in a complete first-blue-step fixture whose projected Hamming weight increases.

## 2. Uniform packet norm
For every current blue degree-four edge, permit ALL SIX pairs of its four incident faces as atoms of cost one, alongside singleton face atoms. This includes either side of every possible Rep4 resolution partition, so the metric does not depend on guessing the source figure’s split grouping. Define mu(sigma) as the minimum number of such atoms whose XOR is sigma. Then

 |sigma|/2 <= mu(sigma) <= |sigma|,
 mu(sigma+tau)<=mu(sigma)+mu(tau).

For a pair-only atom graph, an optimum can be chosen as a matching on occupied vertices plus remaining singleton atoms: paths through unoccupied vertices cost at least the two endpoint singletons, and cycles can be removed. Hence mu=|sigma|-maximum_matching_size on the occupied allowed-pair graph. With bounded pair components it is a finite local lookup table; without that extra property it is still a component-consistent matching cost, not a fixed-radius choice.

The norm is defined uniformly at each level from that level's actual blue degree-four incidences. It is not discounted by an accumulating factor per generation.

## 3. Atomic contraction test
Suppose the actual refinement/copy maps satisfy these specific column facts:

(a) Every fine sheet face projects to one old face, except a blue Rep4 resolution auxiliary which projects to one allowed OLD pair. A red Par4 resolution auxiliary can be projected to one old face by choosing a parity-pair pivot.
(b) Old degree-four junctions are resolved before doubling. Every NEW blue degree-four junction is a glued-cross vertical line consisting entirely of CYLINDER faces. In an X step all six of its pair atoms are therefore killed by BOTH sheet projections pA,pB.
(c) The two sheet projections have disjoint single-face domains; cylinder faces project to zero.

Then for every fine atom u,

 mu_old(pA u)+mu_old(pB u)<=1.

Apply triangle inequalities to an optimal atomic decomposition of sigma to get

 mu_old(pA sigma)+mu_old(pB sigma)<=mu_fine(sigma).

Choosing the lower-cost sheet gives the desired factor1/2 in mu, even though raw Hamming projection fails. This test does NOT require a favorable syndrome to be globally valid; validity/cochain compatibility are separate admission requirements for the actual decoder.

For a Z/red step, suppose its direct total-parent-page projection p maps each fine face to either one old face or one allowed old blue-resolution pair, and no fine blue pair atom has a nonzero image of cost>1. Then the same atomic proof gives mu_old(p sigma)<=mu_fine(sigma). The constructor's direct red flat-fiber total-parity calculation is evidence for this map, not yet the full edge/vertex proof.

## 4. Source-specific facts still to certify
The source inventory strongly supports (b): inherited degree-four glued crosses are split in refinement; new degree-four edges are the vertical glued crosses of the cylinder, blue in RX and red in RZ. Doubled T overlap edges are distinct degree-three edges, and free-cross intersections are not abstract degree-four gluings. This inventory must remain bound to the actual port/refinement construction, not inferred merely from a rendering.

The candidate pair graphs appear confined to the finite hashtag of a parent face because pair atoms cannot cross inherited degree-three T seams. If confirmed, this gives bounded-size packet blocks and a fixed local matching lookup. Full recursive boxed-port realization, exact cochain maps, and the red global map remain prerequisites.

## 5. Component ownership and the threshold consumer
Include complete packet blocks and preimages of all COARSE packet-block adjacencies in the fixed active dependency graph. Since maps and packet blocks are bounded, this preserves bounded degree and linear charge. It ensures output packet matching cannot silently combine different owner-components without their inputs being merged first. Componentwise smaller-sheet choices then have half as many charge units, with correction supports charged by mu via |sigma|<=2mu.

The charged-component contour theorem extends to these finite-state positive charges: replace occupied-site count by integer packet charge, retain the underlying occupied face bits as witness leaves, and use the uniform comparison to Hamming weight. State labels and packet matchings have only exponential-in-charge entropy. For two runs differing by one local Pauli, total duplicated leaf charge is at most twice the number of distinct original occupied face bits plus a fixed fault allowance. The product-Gibbs support lemma therefore still pays the contour cost. This extension requires the theorem's full causal/common-lift/cochain hypotheses; packet contraction alone does not prove logical stability.

## Scientific boundary
If the actual atlas and map obligations are earned, this metric can repair a structural energy-accounting failure in the small explicit architecture. It would be a different proof framework from insisting on the source sketch's raw syndrome-weight contraction. At present it is a concrete, checkable repair mechanism; no self-correcting lifetime is claimed for the full explicit family.

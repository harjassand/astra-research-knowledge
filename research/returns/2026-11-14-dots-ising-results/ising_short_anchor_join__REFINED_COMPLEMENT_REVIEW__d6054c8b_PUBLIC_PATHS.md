# Independent review of refined no-anchor exterior coverage

Reviewed `n1722_compact_dense_coverage_20261113/REFINED_NO_ANCHOR.md` and reran refined.py. No new defect found.

## Run and enumeration details
No solid segment of length2R+1 implies each cyclic plus run is at most2R. A full plus line is automatically excluded. Horizontal and vertical run counts yield Nplus<=R Ptotal/2, so the ORIGINAL weight relative to allminus is at most exp(-4Ptotal). This handles actual thermal holes without replacing actual volume by filled area.

After zero-edge contraction, every actual adaptive cycle is a physical edge-simple nonbacktracking walk. A repeated vertex in a closed such walk requires at least two length4 loops, hence at least8 physical steps. Therefore p4 consists exactly of n unit square-dual plaquettes, and p6 exactly2n length1-by2 rectangles. These are unoriented unrooted candidates; one global spin factor2 is sufficient for the full collection. No auxiliary-resolution factor is added. Length>=8 uses the deliberately loose100n3^p universe.

The refined pressure and the marked long outer contour in the minus-sea branch are paid separately. The selected contour may be overcounted again in the unrestricted product without invalidating an upper bound. There is no missing small-loop entropy factor.

## Same-encoding no-essential topology
Before contraction, the fixed actual adaptive triangulation has disjoint embedded contour cycles. If all are contractible, their disks are laminar, and the complement of the globally outer disks is the unique genus-one background region with one spin sign. Other spin regions lie in contractible disks.

The adaptive physical-plus rule makes augmented plus connectivity equal to physical NN connectivity: no mixed selected plus-plus diagonal exists. Its augmented minus connectivity equals8-connectivity: a checkerboard selects the minus-minus diagonal, and any other diagonal minus contact has a physical minus two-step alternative. Thus:
- Minus background: every physical plus component has a nonwinding embedded filled disk. Outside the NEW proof basin F means at least one such disk exceeds5R², providing the marked outer perimeter>4sqrt5R.
- Plus background: all minus8 components have finite embedded lifts, even if they contain small plus islands. Their ACTUAL areas sum to H>n/2 outside B. General finite-grid isoperimetry gives Ai<=Pi²/16; every physical disagreement edge is counted once among the Pi. Hence Ptotal>=4sqrt(H)>4sqrt(n/2).

This classification is made in the SAME adaptive encoding. It does not redefine the ORIGINAL fixed-diagonal core A. F is the separately reviewed physical-component down-set containing A, with its own normalizer comparison.

## Scalar/source conclusion
Refined exact exponents at R80,200,1000,10000 are:
- No-anchor minus-sea outsideF:2038,5122,25688,256367.
- No-anchor plus-background outsideB:903,2257,11224,104428.

Combine the first two branches with the solid critical-anchor native bound515,1521,4423 at the first three instances. Paying3<exp2 gives no-essential outsideF occupation/ZA exponents513,1519,4421.

The original numerator identity remains
 N/ZA =1-C/(kappa ZA)+eta_F+N_outside(F union B)/ZA,
 with the separately controlled eta_F. Core and basin mass are not discarded. These finite exterior estimates do not acquire C, prove a uniform growing-R polynomial algorithm, or establish the North Star. At R10000 the native anchor branch is still vacuous, so the entire zero-wall sector is NOT closed there.

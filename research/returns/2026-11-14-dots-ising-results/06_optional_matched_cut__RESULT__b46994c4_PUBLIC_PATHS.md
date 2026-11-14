# An acquired native crossing subset of the SAME global filled-area cut

This is a lower bound on the energy of radical's actual globally defined cut potential, NOT a lower bound on capacity. Its purpose is to match an acquired edge family to a complete upper on the same W, without substituting an actual-count trial or an unproved thermal completion.

Fix R200,L1600,theta4,phi1/50 and the actual cut M_(s²), s=79/40, filled-area cap V=156025. The trial is1 on M\B and0 outside, with the original reservoir vertex1. Consider embedded a by b rectangles with a,b between2k+4 and L-2. Cut four k-square Ferrers corners, leaving a common central cross, and set ALL other spins minus. Choose total cut area

 A=ab-V-1.

The larger endpoint then has actual and filled area V+1, outside M. Mark an addable cut cell in one Young corner and remove that plus cell. The smaller endpoint remains a connected orthogonally convex Ferrers droplet of filled area V, hence lies in M. Both endpoints have actual plus count below n/2, no exterior companions, and the same physical perimeter2(a+b). There is no changed source, free thermal reset or assumed companion event.

The marked native flip has two plus and two minus neighbors. Put q=exp(-2phi). Its conductance is w_large q/(1+q), where

 w_large/w_minus=exp[-4theta(a+b)+2phi(V+1)].

This follows either endpoint's detailed-balance rate and includes the actual rate-one clock. Every such native edge has squared trial difference1.

## Exact count and acquisition

Let S_k(z) be the k-box Young area polynomial and E_k(z) its area polynomial with a marked addable cell. The existing proved identity E_k=[k]_z G_(k-1,k)(z) acquires its positive coefficients. The number of marked quadruples at total A is

 H_A=4[z^A] E_k(z) S_k(z)^3.

Thus the actual edge-subset energy is

 Wgood/w_minus = n [q/(1+q)] exp[2phi(V+1)]
                 sum_(a,b) H_(ab-V-1) exp[-4theta(a+b)].

All eligible ordered rectangle dimensions are included once. The central cross ensures the physical bounding box is recoverable even after the marked removal; its cyclic origin, dimensions, corner diagrams and mark are determined by the edge. The two-site exterior gap prevents periodic or augmented wrap connections. Therefore the n translations and ordered dimensions do not duplicate edges. No separate orientation factor is inserted.

A normalized draw is acquired by selecting a,b with their positive summand weight, choosing the marked corner and its area by the positive E*S^3 coefficient convolution, and using the existing marked/ordinary Young traceback samplers. Physical exponential precision and weight-selection errors must be paid. The normalizer/coefficients are actually computed below; a large-torus physical spin-array draw has not been benchmarked.

Exact integer coefficients use carry-safe Kronecker convolution. geometry_check.py enumerates5,216 small native marked edges, verifies the unchanged physical perimeter, two-plus/two-minus rates, no duplicate edges and all marked-area coefficients. These geometry checks support the general bounding-box/Young argument.

## Same original-core normalization

The inherited full-wall core bound gives ZA/w_minus<=2 exp(S0),
 S0=6n q0^4/(1-q0), q0=4exp[-(8-phi(r+2)/2)].
For this tuple r5, q0<1/500. Hence S0<=6n/(500³*499). This retains the original core and its full thermal entropy; it does not pretend ZA=w_minus. The bound is valid here but grows extensively at fixed temperature, so bare companions do not establish a uniform asymptotic construction.

receipt.py acquires the exact summed crossing coefficients and uses outward Decimal transcendental evaluations plus the rational native-rate lower q/(1+q)>24/49. Correctly rounded Decimal exp/ln semantics are an explicit arithmetic dependency. The k100 receipt covers57,791 rectangle boxes and374 perimeter classes. Runtime is recorded as a one-run diagnostic, not an asymptotic complexity claim.

The complete global cut upper from global_walk_trial/cert_r200/certificate_s79_40.json applies to this SAME W, including structural, target and reservoir edges. It can be compared directly with Wgood. This comparison is not a capacity lower: C<=W, while Wgood<=W carries no inequality between Wgood and C.

## Thermal/source and quality limitations

A buffered thermal extension can be acquired using independent sites or finite interacting patches only when every exterior patch is augmented-separated from the droplet and all other patches, remains below the filled-area cap, and the source's actual majority condition is enforced in the positive count DP. Interior patches must stay away from the common outer collar and marked neighbors. Those restrictions can be imposed, but no unrestricted free thermal completion is imported here. The thermal core-XOR resistance flow is not an exact crossing-law oracle.

The current Wgood/Wupper comparison is far from1, so it does not prove a small omitted-energy fraction, polynomial acceptance, polynomial W/C or native decision cost. It supplies an honest acquired subset and a matched lower witness for rejection analysis, not full critical-channel coverage.

## Executed matched comparison

At k100 the outward receipt gives log(Wgood/ZA)>=-6235.0562629121, hence Wgood/ZA>=exp(-6236). The imported complete-cut receipt gives log(Wupper/ZA)<=-6202.0050095481, hence Wupper/ZA<=exp(-6202), with its original kappa<=1 scalar condition retained. compare.py verifies Wgood/Wupper>=exp(-34) and independently certifies q0<1/500 by a rational Taylor sum.

The exact log-ratio bound is approximately-33.0513. This is NOT a near-unity coverage certificate: the guaranteed omitted fraction can still be almost1. Nor does it imply the actual acceptance is that poor; it is a conservative lower witness. Further small changes in corner-box size should not be confused with solving the global acquisition or physical decision-time problem.

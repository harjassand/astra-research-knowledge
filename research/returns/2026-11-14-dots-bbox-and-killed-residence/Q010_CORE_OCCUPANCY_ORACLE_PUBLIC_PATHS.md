# Exact core current from inverse Ferrers decoding

## Result and scope
The acquired four-corner path law now has an explicit evaluable **core-edge occupancy oracle**, not merely an upper overlap bound. This is a constructive bridge toward resistance acquisition. It is not an oracle for the entire flow: prefix, merge, late, and source contributions are excluded. Their possible overlaps with core cannot be discarded when forming full squared currents. This does not estimate capacity, physical passage time, or deliver the North Star.

For corner bound d, start K=2d+1, last box M, q=exp(-1/25), and torus n, return
phi_core(S,S+v) = P_edge(q)/(n Z_d(q)^4),
where P_edge is a finite polynomial with nonnegative rational coefficients. The implementation sums all compatible direction/macro/corner-support preimages instead of assigning one latent channel to the physical edge.

## Translation and macro decoding
Every core configuration has a compact bounding rectangle of extent at most M in each coordinate and includes each coordinate between its extremal occupied rows/columns. With M<L/2, its torus chart is uniquely identified by the largest empty coordinate gap on each axis. Thus its anchor is unique; the uniform-translation probability is exactly1/n. This does not extend to wrapping or non-core configurations. `unwrap` implements the chart recovery, rejecting shapes outside these hypotheses.

In a chart, enumerate right growth and upward growth after swapping coordinates. If the oriented unchanged side length is h, the base width is a=h for right and a=h-1 for upward. Accept only K<=a<M. Sum both candidates: physical orientation overlaps are not treated as disjoint. Strip the candidate new outer line and decode row-contiguous intervals into stationary and active corner profiles. Geometry validation rejects inconsistent states.

## Central interval preimages
After positive-cut additions, active corners have completed profiles mu=(lambda-1)_+ and nu. Their original supports p,t range from their completed nonzero supports through d, with reconstructed partitions lambda_i=mu_i+1{i<p} and similarly nu. Reject invalid partitions. Stationary profiles remain unchanged.

The possible central domain is [p,h-t-1], length m=h-p-t. Let J=[a,b] be the occupied portion of the new outer line and j=|J|. It must be an interval. For an empty J, a proposed site z has conditional edge probability1/m if it lies in the domain. For nonempty J inside the domain and j<m, its state probability is1/(m-j+1). The outgoing left-edge probability is therefore
(a-p)/[(m-j+1)(m-j)],
and the outgoing right-edge probability is
(h-t-1-b)/[(m-j+1)(m-j)].
Multiply this by q^(area(stationary)+area(mu)+area(nu)+p+t), then sum valid supports. All latent positive-corner histories leading to the same physical state are included.

## Positive-cut preimages
Positive corner additions occur before any outer-line site. Their prescribed order is upper corner, descending corner index; then lower corner, descending index. The flipped row fixes which corner and the index k.

For the currently processed corner, its observed cut profile c determines every original row except that previously processed rows i>k may have been original1, now0. Enumerate original support p>=k+1; reconstruct lambda_i=c_i+1{k<i<p}; validate partition, support, and flipped site. During upper-corner processing the lower original profile is unchanged. During lower-corner processing the upper profile is already completed, so additionally enumerate its original support using the same completed-fiber formula. Each surviving original channel traverses that positive edge with probability1. Sum its q-area weight.

These are exhaustive alternatives because the deterministic positive phase has only these two orders and the central phase has the explicitly derived interval law. The numerical tests do not alone prove exhaustiveness; the inverse cases above supply the geometric argument under the separated-corner path definition.

## Executed evidence
- d2,K5,M7,q1/2: exhaustive1296 corner channels, all28944 distinct physical core edges; exact rational forward enumeration equals inverse oracle with zero mismatches.
- d1,K3,M5: every absent site in a6x6 containing box for all176 encountered states,3608 edge tests, including zero-current cases; exact agreement.
-300 wrapped translations on16x16 torus recover the same state, flip, anchor and current.
- Original R200,q=exp(-1/25),d132 channel: one central state of86402 sites and one positive-cut edge were acquired and their inverse polynomials evaluated with80-digit directed intervals, .45 seconds total. Central numerator has134 terms; positive has78. Their normalized current intervals are approximately7.2147111271e-139 and6.6765196778e-138. They are small probabilities, not capacities. d132 matches the executed recovered sampler; the later improved scalar certificate uses d131. The oracle is parameterized for either, but this R200 run used132.

## Arithmetic and reproduction
`core_occupancy.py` gives exact rational finite tests. `r200_occupancy.py` builds positive polynomials symbolically and evaluates with alternating-Taylor q enclosures and outward Decimal bounds, dividing by oppositely rounded n Z^4. Exactness remains conditional on the arithmetic/library contracts; this is not a formal proof-assistant artifact. `check_occupancy_extra.py` supplies zero-edge and wrap tests. No enormous state-space matrix or unimplemented committor oracle is used in the R200 calculation.

The direct decoder scans the supplied physical state and tests finitely many support pairs. It can be optimized using maintained row profiles; evaluating this scan on every one of a million path additions would be costly. An unbiased random path-edge resistance estimator can instead select an edge with known positive probability and weight its computed core occupancy by the reciprocal edge-selection probability. Its variance and stage-overlap treatment still need development before claiming efficient full resistance acquisition.

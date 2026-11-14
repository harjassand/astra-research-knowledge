# Current-weighted exclusion of low-retained-area hole closures and porous large precursors

Status: internally derived finite extension, not independently reviewed, not a growth or complete-coverage theorem. All assumptions and the thermal-core capacity lower from the preceding package are retained. In addition R>=10. Native clock is one proposal per site. Source is the actual soft core source with clock kappa, not equilibrium entrance sampling.

Write n=L², theta>=4, phi=theta/R, a=49999/50000,

 Dk = kappa^(-1)+2n exp(8theta R/a+8theta),
 Ck >= ZA/Dk,  ZM5/ZA <= 1/(1-u_r),
 s0=2theta-29/20.

## 1. Actual edge family with a newly enclosed gap

A labelled boundary edge (x,y=x+z), x in M5 outside B, y outside M5 and B, belongs to Fgap if:

* The old augmented plus components joined at z have k filled domains D_i, 1<=k<=8, pairwise disjoint, embedded and nonwinding. Each is an actual filled outer domain, so its area is at most 5R².
* The total old filled area S=sum |D_i| is <=(9/2)R².
* W=(union D_i) union {z} has an embedded nonwinding filled hull D equal to the filled domain of the violating new component. In particular |D|>5R². This inspectable geometric identity is an explicit hypothesis, not an assertion about every nested/winding entrance.

Let Jgap be the actual current over precisely these edges. Then

 Jgap/Ck <= min(1, [8n(126n)^8/(1-u_r)] Dk exp(-Egap)),
 Egap=s0[(526/45)R-4]-9theta R.                 (1)

This includes a single old component closing a long bay. Spins in the newly enclosed region need not all be minus: unchanged smaller components and thermal islands there are allowed, subject to the displayed filled-hull identity. It also includes disjoint small mergers that create an area jump. No exact filled plus disk is assumed.

### Geometric proof

Let V=|D| and Psum=sum P(D_i), physical perimeter. Pairwise disjoint old filled domains have disjoint site sets, and z was minus, so |W|=S+1. Inserting one site changes physical perimeter by at most 4, so P(W)<=Psum+4. Its boundary consists of the outside boundary of D and the boundaries of its complementary bounded regions. Source-compatible lattice isoperimetry, applied separately, gives

 P(W)>=4sqrt(V)+4sqrt(V-S-1).

For several complementary regions, sum sqrt(area_i)>=sqrt(sum area_i); no single large hole is presumed. Hence

 Psum >= 4sqrt(5) R+4sqrt(R²/2-1)-4
      >= (526/45) R-4,                         (2)

using sqrt(5)>=20/9 and sqrt(1/2-1/R²)>=7/10 for R>=10. All boundaries use the source's fixed diagonal contact resolution; only physical edges enter perimeter. The assertion requires an embedded hull, not a torus-wide area/perimeter inequality.

### Entropy-preserving map and contour sum

For a fixed canonical ordered tuple of the actual disjoint D_i, flip EVERY spin in their union. The outer plus boundaries turn minus. All newly created plus components inside D_i stay inside its <=5R² embedded domain; exterior components are unchanged. Thus the image is in M5. The map is injective with the recorded tuple; thermal holes and islands are complemented, not erased. There are no physical edges directly joining distinct old filled domains, since their outer plus boundary sites would then connect the old components. Energy changes add:

 w(x)/w(Fx) <= exp[-2theta Psum+2phi S].

Pay at most 6n*4^P per contour, as in the acquired source. Reserve eta=1/20 from each perimeter exponent. Since log(4)<7/5,

 (2theta-log4-eta)Psum-2phi S
 >= s0[(526/45)R-4]-9theta R=Egap.

The remaining sum for each contour is at most

 6n sum_{P>=0} exp(-eta P) <= 6n(1+1/eta)=126n.

Canonical tuple selection prevents any missing source label. Summing all tuples, including incompatible ones only as an upper bound, costs sum_{k=1}^8(126n)^k <=8(126n)^8. This does not assume independent droplets. The site-clock total outgoing rate is <=n, and 0<=v<=1, so actual boundary current is bounded by n times source weight. Combining with the displayed capacity/normalizer ratios proves (1).

The map's preimages may overlap across different recorded tuples; that is precisely why the tuple count is retained. No physical trajectory duration or conditional Gibbs entrance law is used.

## 2. Large precursor with substantial thermal holes

Let Fpor be boundary edges whose predecessor contains an actual filled component domain D with 4R²<=V=|D|<=5R² and at least V/4 MINUS spins inside it. Select such a domain canonically. Other thermal components, including nested islands inside its holes, are retained under the full-domain flip. Then

 Jpor/Ck <= min(1, [6n²(ceil(9R)+3)/(1-u_r)] Dk
                   exp[-(12theta-8log4)R]).          (3)

Proof: its signed interior magnetization is <=V/2, so the fixed-domain weight ratio is <=exp(-2theta P+phi V). Contour counting reduces the exponent to

 -(2theta-log4)P+phi min(5R²,P²/16), P>=8R.

The quadratic branch is convex. At P=8R the negative exponent is (12theta-8log4)R. At P=4sqrt5 R it is [(8sqrt5-5)theta-4sqrt5 log4]R, which is larger for theta>=4. For example the difference is (8sqrt5-17)theta+(8-4sqrt5)log4>0. Above this endpoint the contour sum is geometric with ratio 4e^-2theta<1/2. At most ceil(9R)+3 pays the finite and geometric terms. The map preserves M5 as above. Multiply by native outward rate n and normalize to prove (3).

This does NOT say that typical large precursors contain a solid seed. It only shows that the specified >=25%-minus predecessor family carries little actual source current under the certificate's parameter conditions.

## Exact finite certificates

certify.py uses fractions, integer roots, rational exponential lower bounds, log2<.7, and the actual source clock kappa=epsilon/(64D0), epsilon=.01. D0 is the acquired core deficit bound, not set to a convenient constant. At theta=4,L=8R:

 R=20 or40: both new bounds uninformative under that clock.
 R=80,r=5: Jgap/C <= exp(-451), Jpor/C <= exp(-300).
 R=200,r=5: <=exp(-1460), <=exp(-870).
 R=1000,r=6: <=exp(-8277), <=exp(-4699).

These are exact scalar certificates of the stated formulas, not independent geometry verification, physical simulations, or proof of the unproved full research goal. Input exponents are represented logarithmically; runtime of evaluating these explicit bounds is polynomial in the input bit lengths. Computing the underlying acquired core quantities remains subject to their existing source guarantees.

## Remaining source and missing physical growth

Neither theorem covers everything. Exclusions include nested/non-disjoint precursor domains, winding new hulls without another qualifying witness, gap jumps with total retained filled area >(9/2)R², and large >4R² predecessors with fewer than25% minus spins. Pure disjoint mergers with largest precursor<=4R² were separately pruned in the preceding package; pure mergers retaining a larger precursor remain.

Even a connected domain with75% plus occupancy need not contain a mesoscopic all-plus square. Nor does a contour-energy/perimeter bound automatically give an adequate thermal Wulff seed. Thus these are additional actual-current coverage bounds, NOT native growth probabilities, a periodic stable-sector gap, a residence bound, or a full mean-hitting-time sampler.

## Prior and provenance

Uses the authorized N1722/P2 source's diagonal-resolved contour count, filled-domain spin flip, M5/core mass ratio and actual current conventions; standard Peierls, lattice isoperimetry and Thomson capacity machinery. The finite thermal-core capacity lower was established in the preceding internal package. GMV arXiv:1809.07044 already supplies normalized soft-capacity lower bounds asymptotically for its own Wulff-box sectors; no claim that capacity normalization or contour erasure is new. This pass did not inspect held material or perform a new exhaustive prior-art search. The claim here is the explicit scoped combination and finite certificate, not a scientific novelty determination.

# Reduction of actual M5 structural entrance current to a dense large precursor

## Status

A finite internally derived extension of the two earlier current-certificate packages. This is not a physical growth theorem or a full mean predictor. It uses the existing N1722 fixed planar triangulation, actual filled-domain definition, contour count, native site clocks, and thermal-core capacity lower. No held source was accessed. The finite tests below are diagnostics, not independent review.

## Model and inherited bounds

Use the periodic L×L heatbath Ising model with one proposal per site, theta>=4, phi=theta/R, n=L², target B={M>=0}, and actual acquired core A=C_r. M5 consists of configurations whose augmented plus components have embedded nonwinding filled domains of area <=5R². Assume R>=32, L>=8R, 1<=r, r+2<=R/3, r<L/4, u_r<1, and all source conditions of the prior thermal-core package. In particular 5R²<L²/4.

Set

 a=49999/50000,
 Dk=kappa^(-1)+2n exp(8theta R/a+8theta),
 s0=2theta-29/20,
 q=4 exp(-2theta),
 c=6theta-4log4,
 AR=6n(ceil(9R)+3)exp(-cR).

Previously proved/acquired interfaces are

 Ck>=ZA/Dk,  ZM5/ZA<=1/(1-u_r),
 J_two_macro/Ck <= n AR² Dk/(1-u_r).          (A)

The last family consists of actual boundary edges whose predecessor has two distinct disjoint filled domains of areas >=R². These bounds keep the actual kappa, not kappa=1 unless explicitly chosen.

Only structural entrance edges (x,y) with x in M5 outside B and y outside M5 and B are considered. Their sum is at most Ck; it need not equal Ck because some current can reach B without leaving M5. Therefore a bound delta*Ck on excluded edges is NOT a claim that their fraction of the possibly much smaller entrance flux is delta.

## Planar classification: nesting is not an additional area-exit family

All filled sets here use the acquired fixed diagonal contact resolution. Equivalently, in a planar lift of an embedded component C, fill its bounded complementary regions. Its outer boundary lies on C and separates these regions from the unbounded complementary region. Zero-coupling diagonal edges are part of topology but never charged as physical perimeter.

### Separator lemma

If a newly added site z belongs to the old filled domain D_C of any old plus component C, the plus component containing z after the addition is contained in D_C, and so is its filled hull. Indeed, z is in a bounded complementary region of C unless already plus, which is excluded. A graph path from that region to the exterior must meet C. All plus components that can be joined through z are consequently either inside D_C or C itself; no old component crossing C exists. Filling a subgraph contained in the filled disk D_C stays inside D_C, because its exterior contains the connected exterior of D_C. Other plus components and their filled hulls are unchanged.

Thus this update cannot create a >5R² filled hull, winding, or a nonembedded hull. Every actual structural exit adds z OUTSIDE every old filled domain.

### Disjointness lemma

Filled domains of distinct plus components are laminar: disjoint or nested. To see this in a planar lift, each disjoint connected component lies in one complementary region of the other; its outside boundary cannot cross the other's boundary. Crossing would require intersecting components or crossing triangulation edges. If z lies outside every old fill, any old component adjacent to z must be outermost: an edge from the exterior of an enclosing component into its bounded complementary region cannot avoid that component. Therefore the old components joined at an actual structural exit have pairwise disjoint filled domains D_1,...,D_k, k<=8.

This does not require the entire configuration to have no nested thermal islands. Such islands may occur inside D_i and are retained by the full-domain spin flip. The assertion concerns only the joined components.

### Exact hull identity

For a nonwinding new component, choose its common planar lift. All joined old domains lie inside its filled hull. With W={z} union D_1 union ... union D_k, the actual new filled domain equals Fill(W). Filling the old bounded complementary regions before taking the union does not alter the union's unbounded complementary region. Thus the filled-hull identity in the preceding hole-jump theorem is automatic for actual nonwinding area exits under the source's filled-domain convention.

An additional 'nonembedded but nonwinding' finite-component case does not arise under this convention: a component with no nonzero-winding closed walk has a finite lift disjoint from its nontrivial translates. Its filled lifts are laminar. Two overlapping translates would therefore be nested; strict containment of a domain in a translate of itself, or the reverse, contradicts boundedness by iteration. Thus the filled lift embeds. The fixed contact resolution removes boundary-touch ambiguity. A structural failure not given by excessive filled area consequently has a nonzero-winding closed walk.

## Complete small-precursor area-exit bound

Let Jsmall be current over ALL nonwinding area exits whose largest joined old filled domain has area <=4R². Define

 E_low = s0[(547/50)R-4]-(19/2)theta R,
 E_high = [11s0-(19/2)theta]R,
 F = 8n(126n)^8 Dk/(1-u_r).

Then

 Jsmall/Ck <= min(1, n AR² Dk/(1-u_r)
                         +F exp(-E_low)+F exp(-E_high)).       (1)

### Proof and complete case split

The joined old domains are disjoint by the preceding lemmas. Write S=sum |D_i| and V for the new filled area; V>5R². If at least two old domains have area >=R², apply (A). Otherwise all except the largest have area <=R², and the largest is <=4R².

Case S<=(19/4)R². Since |W|=S+1, physical boundary decomposition and lattice isoperimetry imply

 sum P_i >= 4sqrt(V)+4sqrt(V-S-1)-4
         >= 4[sqrt(5)+sqrt(1/4-1/R²)]R-4
         >= (547/50)R-4.

The last step uses sqrt(5)>=559/250 and sqrt(1/4-1/R²)>=499/1000 for R>=32. The hole term sums ALL complementary regions of W; their thermal spins are immaterial. After reserving eta=1/20 of each contour perimeter for summation, the erasure exponent is at least E_low because 2phi S<=(19/2)theta R.

Case S>=(19/4)R². Let V1 be the largest old area. For i>1, sqrt(V_i)>=V_i/R; for V1<=4R², sqrt(V1)-V1/R>=-2R. Thus

 sum sqrt(V_i)>=S/R-2R,
 sum[(2theta-log4-eta)P_i-2phi V_i]
 >= (4s0-2theta)S/R-8s0R >= E_high.

In both cases, flipping every spin in all recorded disjoint old domains is injective and lands in M5, retaining their thermal interiors by complementation. The boundary-energy changes add. Each canonical ordered tuple has at most eight contours; the reserved tail pays <=126n per contour and <=8(126n)^8 over k=1,...,8. Native outward rate <=n and voltage drop <=1 give the current bound. Normalize with Ck and ZM5/ZA. No assumption that the new area equals S+1 is made: mergers and newly enclosed holes are both included.

For theta=4 the asymptotic coefficients of E_low and E_high are 33.657 and34.05, versus 8theta/a approximately32.000641 in Dk. This leaves a positive margin, subject to the actual kappa and finite prefactors.

## Complete winding-current bound

Let Jwind be current over structural exits that first create a nonzero-winding component. Then

 Jwind/Ck <= min(1, [6n² Dk/((1-u_r)(1-q))]
                         exp(10theta R) q^(2L-4)).             (2)

Proof: a new noncontractible simple cycle must contain z, because every old component was nonwinding. Remove z from that cycle. The remaining path belongs to ONE old component. In its lift it connects two neighbors of distinct translates of z, so its displacement has a coordinate of magnitude at least L-2. The old component's embedded filled domain therefore has physical perimeter at least2L-4, and area at most5R². Choose a qualifying old contour canonically, flip its entire filled domain, and sum its weight ratio exp(-2theta P+2phi V) using count6n4^P. The geometric tail is exp(10theta R)q^(2L-4)/(1-q). The clock contributes n, and the capacity/core ratios give (2).

A new winding cycle can traverse diagonal edges, but each step changes each coordinate by at most1, so the L-2 bound remains valid. No global half-density isoperimetric inequality is invoked.

## Remaining current class

Combining (1),(2), the two-macro bound, and the preceding >=25%-minus large-domain bound, every structural entrance edge outside a quantitatively small Ck-normalized exceptional current has:

* a nonwinding new component;
* one joined old component with filled area >4R² and <=5R²;
* all other joined components of filled area <R²;
* fewer than25% minus spins inside that large precursor.

The two-macro term can be reused once in a union bound, not assumed independent. It removes, for example, another >=R² companion to the large precursor. Unchanged exterior thermal components remain unrestricted. These conclusions are structural current concentration, NOT stochastic domination by a thermal Gibbs seed and NOT a positive probability of fast growth from every such state.

Native growth/return probabilities, a useful physical-clock residence bound, and efficient uniform handling of this surviving large dense precursor remain open. In particular high density does not ensure a solid mesoscopic plus square. We have not resolved the main remaining growth problem by relabelling it.

## Executed exact checks and finite clock

certify.py keeps the actual source clock kappa=epsilon/(64D0), epsilon=.01, and D0 from the authorized core interface. All scalar bounds use rational arithmetic and explicit inequalities. At theta4,L8R:

 R40: both complete bounds uninformative.
 R80: small-precursor bound uninformative; winding current <=e^-2584.
 R200,r5: Jsmall/C<=e^-77; Jwind/C<=e^-6610.
 R1000,r6: <=e^-1371; <=e^-33481.

The earlier porous-large-precursor bound at R200 is <=e^-870, and the two-macro bound is <=e^-845. Hence at R200 the combined residual outside the displayed dense class is, conservatively, <=e^-75 times Ck. This is an absolute Ck-normalized current bound, not a claim of a specified percentage of total structural flux.

topology_test.py exhaustively checks512 configurations and2304 minus-site additions in a padded3×3 planar domain with one fixed diagonal in every plaquette. It checks laminarity, containment for additions inside old fills, disjointness of joined fills for additions outside all fills, and the exact hull identity;24 additions create nonempty new hull gaps. All checks passed. This is a diagnostic of the graph lemmas, not a proof of the torus theorem or an independent audit. No native trajectory simulation was substituted for a theorem.

## Prior and source scope

All contour and current machinery is standard or already supplied in the authorized N1722/P2 source and previous internal package. Planar laminarity and winding-cycle lifting are standard graph topology. GMV arXiv:1809.07044 supplies related asymptotic Wulff-sector capacity and growth machinery, not a verified direct transfer of its native growth theorem to this source-conditioned periodic class. The new contribution claimed here is only this explicit finite combination and source-class reduction; scientific novelty has not been established. No new held materials or alternate copies were read in this pass.

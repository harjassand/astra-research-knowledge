# Four-corner thermal family: high Gibbs mass but small actual-voltage occupation

## Model and exact family

Retain the original periodic native heatbath Ising model, B={M>=0}, soft-core voltage v, capacity C_kappa and core normalizer Z_A. Use theta=4, phi=4/R, integer R>=80, L=8R,n=L², with the same inherited core r and actual clock kappa=epsilon/(64D0). The construction is not a change to the dynamics.

For each translated 4R by4R lattice square, remove an independently chosen Ferrers/Young diagram from each of its four R byR corner boxes, oriented toward that corner. These four boxes are disjoint. Retain the central2R by2R square and the side strips. Call the remaining filled domain D. It is physically connected, has the original embedded bounding rectangle, no geometric holes, physical perimeter16R, and area16R²-k, with0<=k<=4R². Its perimeter is unchanged because each removed right-angle corner is replaced by a monotone staircase of the same lattice length. The four diagrams and the box origin uniquely specify D; even the maximal allowed corner cuts leave its full bounding box, so the origin is recoverable.

For each D, use the COMPLETE thermal source envelope Omega_D: actual plus outer boundary of D, separating augmented minus collar, arbitrary interior spin pattern with M_D>0, and all exterior companion filled domains of area<=R² disjoint from the pins. Do not impose global M<0. Source states already in B are allowed and contribute zero path. Interior thermal holes and nested islands are not erased or replaced by plus spins. Each source has a unique large outermost domain, so distinct Omega_D are disjoint. Let G be their union, Z_G=sum_G w, and N_G=sum_{G\B}w v.

This is an explicit restricted family, not all large contours, all actual entrances, or all paths through the stable region. It includes exponentially many rough staircase boundaries, not just exact squares. It excludes arbitrary overhangs, winding, multiple exterior macroscopic droplets and other boundary geometries.

## 1. Full positive-interior normalization, without a phase-purity assumption

Put q=4exp(-2theta), alpha=6n q^(4R)/(1-q), q1=4exp(-3theta/2), u1=6n q1^(2r)/(1-q1). Assume alpha,u1<1. Let Z_D=sum_{Omega_D}w.

Conditional on the complete plus boundary, the interior is ordinary ferromagnetic Ising, independent of the exterior gas because the boundary pins shield the two. The event M_D>0 is increasing. The event that an interior MINUS filled domain has area>R² is decreasing. FKG therefore bounds its probability under M_D>0 conditioning by its unconditional positive-field probability; field monotonicity bounds that by zero-field plus-boundary probability. Zero-field full-domain Peierls flipping bounds the latter by alpha. This uses FKG only in ordinary interior Ising, never in a gas constrained by a component cutoff.

On the complement of the large-minus-hole event, flip ALL spins in D. Its boundary becomes minus and separates all new interior plus components (the old minus holes, each filled area<=R²) from the exterior small companions. The image is in M1. The map is injective for a fixed D and retains every thermal spin. Its weight ratio is at most exp[-2theta P_D+2phi|D|]. Removing the at-most-alpha bad fraction of the conditional interior and using Z_M1/Z_A<=1/(1-u1) yields

 Z_D <= Z_A/[(1-alpha)(1-u1)] * exp[-2theta P_D+2phi|D|]
     = Z_A/[(1-alpha)(1-u1)] * exp(-2phi k).       (1)

The equality follows from P_D=16R and the exact cancellation at area16R². No actual-current Gibbs law is used; (1) is a source normalizer estimate.

## 2. Native thermal flow for each D

Use the inherited bit-preserving thermal-prefix flow, whose assumptions are exactly met by each fixed interior pattern: D is filled/embedded, M_D>0, full plus boundary/minus collar, and complete small companion gas. Its geometry-only order first fills the Ferrers corner boxes (each geometric addition has two occupied neighbors and does not increase perimeter), then grows full strips from the4R square until the actual target is reached. Every interior bit of D is left untouched, while exterior source bits are XOR-flipped once rather than erased.

The conditional prefix moment is uniformly at most exp(4theta). It remains so after mixing all allowed interior patterns. For any fixed D and native edge, the flipped site determines the prefix position; inverse XOR reconstructs at most two source states in opposite orientations. The signed-flow inequality pays these without an extra factor2. First-target stopping and zero paths for initial B states are explicit. Thus there is a native flow F_D with divergence w on Omega_D\B, sinks in B, and

 E(F_D)<=2n exp(4theta) Z_D.                       (2)

This is an electrical construction, not a claim that physical pins survive or that the actual process follows a controlled sequence. Its paths can leave any area-capped region on the way to B.

## 3. Pay rough-boundary entropy by weighted aggregation

Take F=sum_D F_D. The disjoint source families make its divergence exactly w on G\B, with target sinks only. Instead of a worst-case label count, use the energy-norm triangle inequality:

 E(F) <= (sum_D sqrt(E(F_D)))².

For t>0, the unrestricted Young partition function satisfies

 P(t)=prod_{j>=1}(1-exp(-tj))^-1,
 log P(t)=sum_{k>=1}1/[k(exp(tk)-1)]<=pi²/(6t).

An R byR Ferrers sum is bounded by this unrestricted sum. There are n translated boxes. Using (1) with square-root weights, the four independent corner sums give

 sum_D sqrt(Z_D)
 <= n sqrt[Z_A/((1-alpha)(1-u1))] * P(phi)^4.

Hence

 E(F)/Z_A <= K_F,
 K_F=2n³ exp(4theta)/[(1-alpha)(1-u1)]
           * exp[4pi²/(3phi)].                    (3)

The finite Ferrers constraints can only improve the bound. No exponential-area interior-label multiplicity or assumed source-label uniqueness at intermediate edges is hidden here; the energy triangle pays all cross-contour collisions. All numerical coefficients in (3) are acquired by elementary scalar formulas without enumerating the flow edges. A polynomial edge-sampling oracle for F itself is not supplied.

## 4. Actual occupation, with no entrance-law substitution

Test F against the ORIGINAL global soft-core voltage v, whose native Dirichlet energy is at most C_kappa and which vanishes on B. Integration by parts and Cauchy imply

 N_G²<=C_kappa E(F),
 N_G/Z_A <= sqrt[(C_kappa/Z_A) K_F].                (4)

This is actual-voltage occupation, not equilibrium probability and not a squared-norm gap theorem. Any valid capacity upper can be used. The included optimized finite trial-cut bound uses the original source clock and gives the explicit certificates below.

## 5. A genuine high-mass baseline

G contains all n translated SOLID4R squares with otherwise minus spins. Each has exact weight w_minus because -2theta(16R)+2phi(16R²)=0, and each is outside B. All of these witnesses are outside B (their plus count is n/4), so Z_(G\B)>=n w_minus.

For core A, let k0=2theta-phi(r+2)/2 and q0=4exp(-k0). The core area/perimeter relation gives Nplus<=(r+2)P_total/4, hence every core configuration has w/w_minus<=exp(-k0 P_total). Encode ALL physical domain-wall cycles, including boundaries of every thermal hole, with the inherited fixed-triangulation convention. The triangulated dual has degree three, so the walls have a unique resolved cycle collection; the complete wall set plus one global spin bit determines the configuration. It would be invalid to keep only outer plus contours and discard the interior entropy. Dropping compatibility gives the standard contour-product upper, with a safe factor2 for the possible global spin label:

 Z_A/w_minus <=2 exp[S0], S0=6n q0^4/(1-q0).

Therefore

 Z_(G\B)/Z_A >= (n/2) exp(-S0).                       (5)

For the stated examples q0<1/500. Exact rational estimates give S0<.01 at R80,200,1000, so Z_(G\B)/Z_A>=n/3. AtR10000,S0<1 yields Z_(G\B)/Z_A>=n/6. These lower bounds decisively rule out obtaining the exponentially small occupation bound from v<=1 or any small-Gibbs-mass claim for this family.

## Limits

This is a nontrivial actual-voltage occupation result for a specific high-mass thermal rough-boundary family. It does NOT bound the full mean hitting time, the residence of arbitrary large/winding/multiple-droplet states, actual-current coverage of this family, growth probability, or time to reach it. It does not prove that this family dominates all relevant stable configurations. The inherited core/contour and thermal-prefix theorems remain dependencies; finite geometry/arithmetic diagnostics are not independent verification of the whole source archive. General potential theory, Ferrers partitions and Peierls arguments are standard; literature novelty of their specific combination is not established.

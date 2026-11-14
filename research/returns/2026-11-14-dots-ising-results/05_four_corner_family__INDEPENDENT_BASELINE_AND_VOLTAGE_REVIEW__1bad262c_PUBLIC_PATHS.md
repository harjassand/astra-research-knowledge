# Independent same-region baseline and actual-voltage review

## High mass: contour pressure proof
Section5 is valid if 'encode all physical domain walls' means ALL nested domain-wall cycles, not only outer plus contours. This distinction must be explicit: an outer-contour-only product would discard interior thermal entropy without paying it.

In the fixed triangulation, dual vertices have degree3. A spin-domain wall occupies degree0 or2 at each dual vertex, so its components are uniquely resolved cycles. The full cycle collection together with one global spin bit determines all spins on the connected torus. Compatibility and core membership may be dropped for an upper bound. The imported physical-perimeter contour count bounds the available cycles by6n4^p, with p>=4.

For each core configuration, every outermost plus fill has bounding side lengths<=r+2. Thus V/P<=ab/[2(a+b)]<=(r+2)/4. Sum over outermost fills to bound Nplus, and note that total wall perimeter includes their outer boundaries plus every nested wall. Therefore
 w/wminus=exp(-2theta Ptotal+2phi Nplus)<=exp(-k0 Ptotal),
 k0=2theta-phi(r+2)/2.

Summing every possible collection of distinct cycles gives
 ZA/wminus <=2 product_gamma(1+exp(-k0 Pgamma))
             <=2 exp(6n q0^4/(1-q0)).
No independence of actual contours is asserted: the product is an overcount. The global spin factor2 is safe even if the core fixes the majority background automatically.

All n translated solid4R squares are distinct, belong to the four-corner family with zero deficits, have exact weightwminus, and have n/4 plus sites at L8R. They therefore lie OUTSIDE B. The actual fair baseline is consequently
 Z_(G minus B)/ZA >=(n/2)exp(-S0),
not merely Z_G/ZA. The claimed finite n/3 lower bound for R<=1000 and n/6 forR10000 applies to exactly the non-target set appearing in N_G. This proves actual high source mass, rather than failure of one coarse mass upper bound.

## Flow and voltage scope
For each D, pooling interior assignments is valid because the fixed boundary shields the ordinary interior Gibbs law from the constrained exterior gas. The deterministic outside-XOR ordering depends only on D. Each physical edge with a fixed D has at most two opposite source preimages; signed cancellation is handled before the squared upper. First-B stopping makes all sinks actual targets and gives zero paths to initial B sources.

Across shapes, collision costs are paid by the energy-norm triangle inequality. Unique source geometry is needed only for divergence: a state with one outermost domain of area>=12R² and all exterior companions<=R² has exactly one such D. It is NOT necessary to reconstruct D from an intermediate edge. No factor2^area for interior labels is missing.

The final integration by parts uses the ORIGINAL global soft voltage v and its ORIGINAL source clock. Its native-edge energy is at most C_kappa. The paths may leave M6 and are not required to stay within a reflected contour family. Hence the inequality is genuinely about actual voltage-weighted occupation, not a new auxiliary committor.

## Four-corner roughness factor
Each independent corner contributes the finite Ferrers sum bounded by P(phi). Square-root source weights use exp(-phi deficit), not exp(-2phi deficit). Four corner sums followed by squaring the energy norm produce P(phi)^8, giving log energy overhead<=4pi²/(3phi). At theta4 this equals(pi²/3)R. The factor n for translated boxes is squared, with the additional n from path length giving n³. These factors are consistent.

## Independent alternative mass lower
HIGH_MASS_SQUARE_SECTOR.md gives a separate injection from typical core configurations into one fixed square sector. Compute independently verified it and tightened the original-field core density to1/40,000,000. This alternative is not needed once the full contour-pressure proof is included, but provides an independent same-region check. Do not present the density diagnostic as a simulation of the actual long-time chain.

## Conclusion
The scoped four-corner result genuinely beats the direct v<=1 bound on the SAME non-target high-mass region. Its unproved extension remains generic source coverage: arbitrary overhangs, winding domains, negative interiors and large exterior companions are not covered. It is not a full residence-time or breakthrough theorem. Original contour conventions, prefix-moment proof, core assumptions and finite actual-clock capacity certificate must remain in any package.

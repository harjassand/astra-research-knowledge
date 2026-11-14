# Direct occupation bound including arbitrary winding topology

For every non-majority state x, Nplus<n/2 and w(x)/w(a)=exp(−8P(x)+Nplus/25)≤exp(n/50−8P(x)). The hard-source potential satisfies0≤h_a≤1.

Resolve each physical Peierls boundary at degree-four dual vertices by a deterministic pairing. Its physical edges then form a set of closed oriented lattice walks on the torus, possibly winding and possibly revisiting vertices. Every edge is used exactly once; each walk has length at least4. Canonically root and orient each walk. There are at most n4^p possible rooted direction words at length p, including invalid words. The entire boundary set determines the spins up to a global flip; use the conservative factor2. Thus

Σ_x exp(−aP(x)) ≤2 exp[n Σ_{p≥4}(4e^-a)^p]

whenever4e^-a<1. This is an overcount by an unordered loop gas. It does not assert that physical contours are independent and does not assume contractibility, a single hull, or a bound on component sizes. The global-flip factor covers even empty boundary.

For any s∈(0,8−ln4) and perimeter threshold P0,
Σ_{x∉B:P(x)≥P0} [w(x)/w(a)]h_a(x)
≤2 exp[n/50−sP0+n Σ_{p≥4}(4e^{−(8−s)})^p].

Choose s=24/5=4.8 and P0=11200. Since4e^-3.2<1/6, the loop-gas log is≤n/1080=2370.37037…. The combined exponent is−189.629629…. Using e>8/3 gives the exact rational upper
2(3/8)^189 <10^-80.

high_perimeter_occupation.py/json checks the necessary exponential comparisons with exact rational Taylor lower sums, and the final rational inequality. No simulation is involved.

This pays ALL hard-source numerator occupation in high-perimeter states, including arbitrary thermal companions, winding strips, winding crosses, multiply connected shapes, and every possible visitation history. It preserves the native model and target. Native clock is already built into the occupation identity; no time rescaling is introduced.

## Remaining sector
Combined with the planar-area core bound, only low-perimeter states (P<11200) that contain a macroscopic component or fail the explicit injective-planar-hull condition remain unbounded. This set still includes smooth supercritical droplets and stripes and cannot be discarded. The result is a direct static localization, not a completed duration or numerator theorem.

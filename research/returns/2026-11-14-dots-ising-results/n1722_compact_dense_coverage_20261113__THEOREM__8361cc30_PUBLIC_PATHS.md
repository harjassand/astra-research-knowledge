# Finite no-essential-wall occupation theorem, with original source retained

## Statement and precise scope
Use the original periodic two-dimensional Ising model at theta=4, phi=4/R, L=8R, rate-one-per-site heat-bath clocks, original core A=C_r, soft clock kappa, target B={M>=0}, original decreasing voltage v, capacity C and Gibbs normalizer ZA. Define walls using the SAME deterministic physical-plus4/minus8 adaptive resolution as the delivered winding theorem. Let F be the independently proved physical-component downset: every physical NN plus component has a nonwinding embedded filled outer disk of area<=5R².

Let E0 be the original non-target states outside F with NO essential wall in this encoding. Then

                 sum_(x in E0) w(x)v(x) / ZA
       <= exp(-513), exp(-1519), exp(-4421)

at R=80,200,1000 respectively, with the inherited original core/capacity tuples. The proof is parameter-specific; the R10000 native-anchor receipt is vacuous. No uniform growing-R statement follows.

## Three-branch proof
1. If a horizontal or vertical SOLID plus segment of length m=2R+1 exists, the paid critical-anchor construction fills its width-m band, then joins the full-column native flow with the exact terminal unnormalized density bound. It does not reset to equilibrium. The independently reviewed pointwise congestion and original-current coordinate cuts give exponents515,1521,4423, respectively. Source: north_compute_20261113/ising_short_anchor_join/RESULT.md (Critical-width solid specialization) and solid_critical.py/json, built on its paid join and the original open-anchor/one-line proofs.

2. Otherwise all cyclic plus runs have length<=2R. Summing the horizontal and vertical run counts gives Nplus<=R Ptotal/2. Thus the ORIGINAL relative Gibbs weight is at most exp(-4Ptotal). For physical contour pressure, use exact unoriented counts n at perimeter4 and2n at perimeter6, and only from perimeter8 onward the conservative100n3^p bound. This pays all thermal loops; it is not a zero-temperature or no-holes approximation.

3. With no essential resolved wall, embedded contractible cycles have a unique genus-one complementary background region. If its spin is minus, every physical plus component lies in an embedded filled disk. Being outside F supplies an actual outer contour of perimeter>4sqrt5 R>8.9R. Marking it while retaining all other loop pressure gives exponents2038,5122,25688.

If the background is plus, all minus8 components have finite injective lifts. Their ACTUAL total minus area exceeds n/2. Isoperimetry and disjoint physical boundaries give Ptotal>4sqrt(n/2)=16sqrt2 R. A perimeter tilt1/2 retains contour tension7/2 and the refined short-loop pressure; this gives exponents903,2257,11224.

The three branches are exhaustive in E0. Their sum is at most three times the largest displayed branch bound, and3<exp(2), proving the statement.

Detailed equations, conservative exact constants and source assumptions are in REFINED_NO_ANCHOR.md. refined.py proves all scalar choices with rational bounds; short_loops.py enumerates the two exact short-loop counts as a diagnostic. These computations are not physical lattice dynamics simulations.

## Finite original-source consequence at R1000
The already delivered all-winding occupation theorem gives exp(-137) for all non-target configurations with an essential wall, in this same encoding. Combining it with exp(-4421) above yields

 N_(Omega\(F union B))/ZA <=exp(-136).

The separate F normalizer theorem gives ZF/ZA<=1/(1-u), and 0<=N_(F\A)/ZA<=u/(1-u). Hence the EXACT original-source identity implies

 1-C/(kappa ZA) <= N/ZA
 <=1-C/(kappa ZA)+u/(1-u)+exp(-136).

The large core contribution remains explicit. F is a proof basin, not a replacement for the original source A or its capacity. This does not acquire C, sample a rare entrance law, prove a reflected spectral gap, or yield the requested complete polynomial-cost mean-exit-time predictor. Rare-capacity acquisition and uniform growing-R guarantees remain open.

## Independent review
North_compute and north_gkp independently checked the critical run inequality, exact short-loop counts, adaptive-encoding phase dichotomy, minus-component isoperimetry, contour pressure, and source/F accounting. Their separate reviews are included as GKP_REFINED_REVIEW.md and north_compute_20261113/ising_short_anchor_join/REFINED_COMPLEMENT_REVIEW.md. The native short-anchor join was independently checked by bridge. The delivered winding theorem and physical-basin theorem retain their own prior reviews and dependencies.

## Historical notes
CANDIDATE.md and MULTIPLE_DROPLETS_EXTENSION.md are narrower preliminary small-hole-sector proofs. They are not needed for this final no-essential theorem and should not be read as extra hypotheses on it.

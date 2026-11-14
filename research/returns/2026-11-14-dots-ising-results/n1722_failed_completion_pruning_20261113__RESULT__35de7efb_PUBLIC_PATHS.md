# Weighted pruning of failed two-sided clean completion

This is a direct Gibbs-mass bound for a specified residual class, not a new dynamical mixing theorem. It strengthens the earlier isolated large-span counterexample into a bound on an entire thermal failure class. It does not cover all remaining winding states.

## Model and class
Use the original physical nearest-neighbor Ising weight
 w(s)/w_minus = exp[-2theta P_total(s)+2phi V(s)],
where V is the plus count, theta4, phi=theta/R, L8R, n=L². The original core contains allminus, so ZA>=w_minus. The original voltage satisfies0<=v<=1.

Consider states outside B whose deterministic resolved physical wall set has exactly TWO axial essential cycles with total physical length Pw<=49L/10. All other wall cycles are contractible, with embedded filled area at mostR². Erase these contractible walls to obtain the pure annular phase between the two essential curves. Call its area W. This erased phase, not merely the actual perforated state, is assumed to have NO full plus column in the axial direction.

Choose ordered proper transverse lifts of the two essential curves. Let fbar,gbar be their signed-area mean positions; then W=L(gbar-fbar). Let fmin,fmax,gmin,gmax denote their transverse extrema, and put
 a=fbar-fmin, b=gmax-gbar.
This does not require row-convex boundaries. Use the physical square-dual cell boundaries, with any checkerboard contacts separated by an infinitesimal resolution and take the zero-resolution limit. Their signed enclosed area equals the number of erased-phase plus cells exactly; do not substitute an uncorrected finite-area triangular-center polygon. Signed-area means lie within the extrema, and Stokes' formula gives the displayed area identity.

Let h count actual minus sites inside the erased plus annulus and k count actual plus sites outside it. Thus V=W-h+k. We require BOTH conservative padded completion guarantees to fall below majority:
 n-L(a+4)-h < n/2, and n-L(b+4)-h < n/2.     (F)
These conditions precisely state the failure class being bounded. If an actual permitted clean completion guarantees at least these areas, its genuine failure implies(F); no physical path is replaced by an artificial Gibbs reset. The geometric completion certificate must be checked separately before using this as an exhaustive case split.

## Deterministic geometry and defect inequality
From(F), a+b>L-8-2h/L. Absence of a full column in the ERASED phase implies fmax>=gmin. Therefore the sum of transverse spans is at least
 (fmax-fmin)+(gmax-gmin) >= gmax-fmin = a+b+W/L.
Each axial curve has physical length at leastL plus twice its transverse span. Consequently
 Pw >= 4L-16+2V/L-2(h+k)/L,
 or equivalently
 V <= LPw/2-2n+8L+(h+k).                         (1)

The defect area h+k is no larger than the sum of the filled areas of ALL contractible contours; nested contours are counted, not discarded. For an embedded contractible contour of filled area A<=R², physical isoperimetry P>=4sqrt(A) implies A/P<=R/4. Hence
 2phi(h+k) <= (theta/2) Pc,
where Pc is the total contractible physical perimeter. Using(1) gives the pointwise bound
 w(s)/w_minus <= exp[6theta Pw-32theta L+128theta]
                  * exp[-(3theta/2) Pc].        (2)
At theta4 the padding term is512. This pays arbitrary numbers of small thermal holes AND outside plus islands, including nested defects. No independence or conditional Gibbs law is assumed.

## Complete positive counting bound
Use the previously certified physical contour overcount100n3^p. Two essential walls with total length<=Q=floor(49L/10) have at most(100n)²(Q+1)²3^Pw encodings after summing their lengths; pay a global phase factor2. Drop loop compatibility only in positive sums.

Every contractible physical contour has perimeter at least4. With qc=3exp(-6)<1/130, their complete partition product is at most
 exp[100n qc^4/(1-qc)] <= exp[100n/(130³*129)].
This includes all contractible components, not merely outer contours. Increasing the loop alphabet only enlarges the bound.

Since log3<11/10,
 (24+log3)Q-128L <= -(501/100)L.
Combining(2), the full class G obeys
 Z_G/ZA, N_G/ZA <= 2(100n)²(Q+1)²
     *exp[-(501/100)L+512+100n/(130³*129)].       (3)

This is intentionally a DIRECT MASS certificate: N_G<=Z_G follows fromv<=1. It must not be presented as an improvement obtained from current transport.

## Exact finite receipts
check.py/json pays every scalar with exact rational inequalities and positive Taylor lower bounds. AtR80,200,1000,10000, equation(3) gives respectively
 exp(-2642), exp(-7445), exp(-39477), exp(-397948).

## Explicit unresolved complements
- Erased annuli with full plus columns that are all punctured by actual minus defects. A separate marked-hole coverage bound is being developed; actual absence of a full column is not enough for the hypothesis above.
- Contractible contours with filled area>R².
- Four essential walls, diagonal homology, or no essential walls.
- Any setting where the proper-lift/clean-completion guarantees are not earned.

The thermal algebra was independently checked by quantum. Fluid and quantum independently confirmed the signed-area version of the pure geometry, including overhangs. The current note does not assert that the union of previously proved transport classes and this failure class covers the whole research target.

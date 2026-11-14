# Two long axial walls: pruning failed clean completion with arbitrary small thermal defects

This combines RESULT.md's area comparison with fluid's independently checked marked-hole cover. It is a DIRECT MASS bound for the stated failure class. It does not by itself control the complementary successful-completion transport class or the full research target.

## Precisely retained hypotheses
Original theta4, phi4/R, L8R, R in{80,200,1000,10000}, original core ZA containing allminus and original voltage0<=v<=1. The state is outside majority B and has exactly TWO axial essential physical wall cycles. Each has length>2L-8 and their total satisfies Pw<=49L/10. Thus Pw>=4L-16. Every contractible contour has embedded filled area<=R², with nesting retained.

Erase the contractible contours to obtain the plus annulus. Choose ordered proper lifts; use signed-area means and extrema as in RESULT.md. Let h be actual minus defects inside this erased phase, k actual plus defects outside, V=W-h+k, and a,b the two mean-to-extremum distances. Both conservative padded completion guarantees fail:

 n-L(a+4)-h<n/2,    n-L(b+4)-h<n/2.              (F)

The actual configuration has NO full plus column in this axial orientation. The erased phase MAY have full columns; they are no longer excluded.

Set c=max(0,gmin-fmax), interpreted as the integer width of the common pure-plus column strip. Use physical dual cell boundaries with infinitesimal checkerboard resolution, so this width and the signed-area identities agree with spin-cell counts. Missing margins must not be hidden in a different finite-area dual polygon convention.

## Geometry and common residual contour activities
The extrema identity now gives
 spansum >= a+b+W/L-c.
Using(F),
 V <= LPw/2-2n+8L+cL+(h+k).
For a contractible wall gamma with area A_gamma, define
 a_gamma=exp[-8P_gamma+8A_gamma/R].
The total defect area h+k is no larger than the sum of these filled areas, including nested contours. Therefore the original state weight is bounded by

 exp[24Pw-128L+512+64c] product_gamma a_gamma.

The actual majority constraint separately gives

 exp[-8Pw+32L] product_gamma a_gamma,

because replacing the original contractible activity exp(-8P) by the larger a_gamma is a valid upper bound. Take the MINIMUM of these two phase factors; do not add their field budgets.

## Pay the holes that remove all actual full columns
If c>0, every one of those c erased-phase full columns contains an actual minus defect. Outer contractible minus-hole projections therefore cover the strip. Fluid's `ising_marked_hole_cover_20261113/RESULT.md` proves that their marked-chain sum, with these exact residual activities, is at most exp(-12c). Its exact uniform tilted kernel is<2/5. All UNMARKED loops retain the ordinary positive product factor

 exp[100n/(130³*129)],

since A<=RP/4 implies a_gamma<=exp(-6P), and3exp(-6)<1/130. For c0 the marked chain is empty and the same formula has factor1. No conditional equilibrium entrance or current law is introduced.

Thus, for fixed essential walls, the relevant phase/cover exponent is

 min(24Pw-128L+512+64c, -8Pw+32L)-12c.

Its maximum over c>=0 occurs at
 c*=2.5L-Pw/2-8>0
in this parameter range, and equals

 -2Pw+2L+96.

## Essential labels and complete bound
Pay the two essential contours with the same universal physical walk overcount100n3^p and a global phase factor2. Since log3<11/10 and Pw>=4L-16,

 (-2+log3)Pw+2L+96 <= -(8/5)L+552/5.

Let Q=floor(49L/10). Summing all two-wall length choices yields

 Z_G/ZA, N_G/ZA <= 2(100n)²(Q+1)²
  *exp[-(8/5)L+552/5+100n/(130³*129)].            (T)

There is no extra factor for possible c: it is determined by the essential-wall geometry and was maximized pointwise. The marked-chain first-passage argument already pays all contour choices and does not require a geometric-series continuation factor.

## Exact finite receipts
`combined.py/json`, using the scalar bounds from check.py/json, gives
 R80: exp(-861),
 R200: exp(-2390),
 R1000: exp(-12599),
 R10000: exp(-125550).

These are direct Gibbs-mass upper bounds, hence also occupation bounds becausev<=1. They are not a new gain from the current-transport method.

## Interfaces still not claimed
- The successful-completion counterpart needs a paid transport/partition theorem over its actual wall-length range. The existing p<=2L-8 theorem does not automatically extend to2.9L.
- Four essential walls, diagonal or no essential walls are outside this statement.
- A contractible contour with filled area>R² is outside the defect estimate.
- Geometric failure(F) must be linked to the actual clean-completion template with correct retained-hole and padding accounting before asserting an exhaustive decomposition of another source class.

Independent checks: quantum checked the thermal area algebra; fluid and quantum checked signed-area geometry beyond row-convex profiles. GKP independently reviewed fluid's column-root count, joint area-width inequality, exact tilted-kernel receipt, stopped-cover extraction, and unmarked pressure. The theorem uses standard contour counting as a paid closure step, not a claim of literature novelty.

## Audit correction: cyclic marked-hole extraction
Compute found that the initial ordinary left-to-right scan could select one wrapping hole twice. The marked-hole proof has been corrected to remove ALL of a selected hole's intersection with the remaining cyclic target interval, including a possible suffix. The remainder is one interval; every selected hole is used once; total removed width is exactly c. The same uniform tilted kernel and stopped-tree induction apply, with no change to the scalar constants above. GKP's first independent review missed this cyclic case; the corrected interval-peeling argument was subsequently checked. This theorem relies on the corrected extraction, not the original scan.

## Raised area cutoff at the two large instances (independently checked)
At R1000 andR10000 only, the same algebra can use A<=4R²/3 using the independently checked enlarged marked-hole12 cover in `ising_marked_hole_cover_20261113/ENLARGED_AREA.md`. The common activities remain exp(-8P+8A/R), so no phase exponent or cover optimization changes.

Independent unmarked-pressure receipt `raised_pressure.py/json` is complete. For P<=400 andR>=1000, A<=P²/16 yields activity<=exp[-(39/5)P], with3exp(-39/5)<1/800. For P>400, A/P<=sqrt(4/3)R/4<3R/10 yields activity<=exp[-(28/5)P], with3exp(-28/5)<1/90. The complete pressure is bounded by
 100n/[800³*799] +100n(1/90)^401/(1-1/90)<2.
This is below the old pressure upper at both large instances, so the already displayed exp(-12599) andexp(-125550) pruning bounds remain conservative without changing their scalars.

The joint inequality supporting a new marked cover also checks algebraically: after exp(12w) tilting, cost>=6P/5 follows from(8/5)W+(68/5)H>=8min(4/3,WH); its product544/25 exceeds16*(4/3). The full `enlarged_certificate.py/json` receipt has now been independently run and checked: its tilted kernel is below2/5 (display .272964695), and it retains the corrected cyclic full-intersection extraction. Thus the raised-cutoff pruning result is complete at these two instances.

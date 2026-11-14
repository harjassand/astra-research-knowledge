# Enlarged defect cutoff: A <= 4R²/3 at R1000 through10000

This changes the defect-area cutoff, not the original Ising source, clock, voltage or geometry. The marked-cover extraction is the corrected cyclic full-intersection removal from RESULT.md. Keep theta4, phi4/R, L8R and the activity a_gamma=exp[-8P+8A/R].

## Same coverage exponent12, larger permissible area
Let alpha=4/3. For A<=min(alpha R²,wh), P>=2(w+h), the joint inequality is now

 8P−8A/R−12w >=(6/5)P.

Indeed with W=w/R,H=h/R, the residual coefficients are8/5 and68/5. Their product544/25 exceeds16alpha=64/3. AM-GM therefore gives
 (8/5)W+(68/5)H >=8min(alpha,WH).

The old 11/8 residual is NOT reused. To pay the weaker long-tail exponent, split the actual perimeter sum more carefully, taking advantage of R>=1000.

For P<=400, A<=P²/16 yields
 3^P a_gamma exp(12w)<=3^P exp[-2P−12+P²/2000].
Use this exact expression for P4..80. For81..400, P²/2000<=P/5 and3exp(-9/5)<1/2, so their sum is bounded by exp(-12) sum_(P>=81)(1/2)^P. For P>=401 the joint inequality gives3exp(-6/5)<91/100. Thus the complete column-rooted tilted kernel obeys

 S<=12*80000 [sum_(P=4..80)3^P exp(-2P−12+P²/2000)
              +exp(-12)(1/2)^81/(1−1/2)
              +(91/100)^401/(1−91/100)] <2/5.

The exact rational certificate gives displayed value .272964695. The entire long tail is included. Consequently the SAME corrected first-passage proof pays exp(-12c).

## Unmarked pressure must also be resummed correctly
Do not substitute the earlier coarse activity exp(-6P), which need not hold at the enlarged cutoff. Instead split at400 again.

For P<=400, 8A/R<=P²/(2R)<=P/5, hence3^P a_gamma< (1/800)^P because3exp(-39/5)<1/800.

For arbitrary P, isoperimetry gives A/P<=sqrt(A)/4<=R sqrt(alpha)/4. Since2sqrt(alpha)<7/3,
 8P−8A/R >(17/3)P,
 and3exp(-17/3)<1/96.

Hence the complete ordinary wall pressure is at most

 A_enlarged=100n[(1/800)^4/(1−1/800)+(1/96)^401/(1−1/96)] <2

for L<=80000. This includes every unmarked contour; dropping compatibility is only a positive overcount.

## Integration
GKP's phase geometry and the minimum of the two field caps use the exact activity exp[-8P+8A/R], so are unchanged. Replace only the area cutoff and the ordinary pressure by the expressions above. The corrected marked-cover exponent remains12. The global tail for a contour with A>4R²/3 is a SEPARATE source-compatible argument, using global majority field cap, not these enlarged activities.

`enlarged_certificate.py/json` proves all displayed inequalities with exact fractions and positive Taylor lower bounds. No claim for R80 or200 is made by this extension. Independent review of the enlarged calculation and its integration is requested before promoting the unrestricted two-axis statement.

## Complement and independent scalar receipt
For a remaining source with total essential perimeter Pw>=4L−16 and at least one contractible area A>4R²/3, planar isoperimetry forces a marked contour perimeter
 H=floor(sqrt(64R²/3))+1.
The source-compatible global-field/NB formula is stated in LARGE_HOLE_BOUNDARY.md (replace its illustrative H by this value). It counts all unmarked contractible loops with ordinary exp(-8P) activities, not the enlarged field-reduced activity. Compute's independent exact receipt in north_compute_20261113/ising_enlarged_hole_tail/check.py/json pays every prefactor and gives exp(-457),exp(-6265) at R1000,10000. Fluid independently reviewed that formula and rational logarithm implementation. Thus this complement does not require an unproved near-isoperimetric contour enumeration.

GKP independently checked the enlarged AM-GM and pressure splits. Final integration of the two-axis union belongs to the sector theorem, not this local cover lemma.

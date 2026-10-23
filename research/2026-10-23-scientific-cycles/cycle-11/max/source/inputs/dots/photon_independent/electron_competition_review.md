# Independent electron-competition check

Reviewed the parent's existing electron_competition.py and electron_competition.json. No new source search, kinetic trajectory or model run was performed. This verifies the algebra and units conditional on the transcribed Wallace coefficients and prescribed dissolved oxygen, not their transferability to another matrix.

Let a = k_O2[O2] = 5.26 × 10^6 s^-1, k2 = 4.1 × 10^9 M^-1 s^-1 and k3 = 9.7 × 10^9 M^-1 s^-1. For nonnegative additional instantaneous electron sinks S (expressed as equivalent pseudo-first-order rate),

F_O2 = a / (a + k2[NO2^-] + k3[NO3^-] + S)
     ≤ a / (a + k2[NO2^-] + k3[NO3^-]).

Every denominator term has units s^-1; the ratio is dimensionless. This describes instantaneous gross electron capture, not eventual electron fate, net nitrite destruction, nitrogen retention or nitrate yield.

Writing C = [NO2^-] + [NO3^-] and y = [NO3^-]/C gives competing nitrite+nitrate hazard C(4.1 × 10^9 + 5.6 × 10^9 y). Since nitrate has the larger supplied coefficient, the bound decreases monotonically as y rises at fixed C and oxygen.

Strict oxygen majority means F_O2 > 0.5. A necessary condition is therefore

C(4.1 × 10^9 + 5.6 × 10^9 y) < 5.26 × 10^6.

At C = 0.001 M, the limiting y is (5.26 - 4.1)/5.6 = 0.207142857142857. Strict majority is impossible AT OR ABOVE that value. Equality produces at most 50%, even with all omitted sinks zero.

For majority not to be ruled out throughout 0 ≤ y ≤ 0.9 at fixed C and oxygen, the endpoint is limiting:

C < (5.26 × 10^6)/(0.1 × 4.1 × 10^9 + 0.9 × 9.7 × 10^9)
  = 0.000575492341356674 M
  = 0.575492341356674 mM.

Equality again permits only a tie at best, not strict majority. A non-strict ≤ concentration threshold is a necessary condition but should not be worded as guaranteeing that strict majority remains possible at its boundary.

The saved threshold arithmetic is correct. Recommended wording: “Above or at 20.714% nitrate at 1 mM nitrite-plus-nitrate, oxygen cannot capture a strict majority of electrons under the stated competition model. To avoid ruling out a strict majority through 90% nitrate, total nitrite-plus-nitrate must be below 0.575492 mM; this remains necessary, not sufficient.”

Do not equate majority with being the largest individual sink: nitrite and nitrate can jointly exceed oxygen even while each individually remains smaller. Missing sink strengths, activities, oxygen availability/transport, other nitrogen pools and altered rate coefficients remain unresolved. These concentration thresholds are conditional filters, not process design recommendations.

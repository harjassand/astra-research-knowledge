# Initial-occupation reduction through analytical box650

This avoids imposing a duration bound on every excursion that leaves the much smaller acquired core. Let A650 contain all configurations whose actual fixed-diagonal augmented plus components fit contractible650×650 boxes. This is an analytical set only; the source, target and native dynamics are unchanged.

The exact hard-source identity gives the contribution inside A650 beyond all-minus as
Σ_{x∈A650\{a}} w(x)h_a(x)/w(a) ≤ Z650/w(a)−1.
It includes all thermal companions and every return/re-exit history automatically. No simulated holding times or dynamics have been suppressed.

Using the previously reviewed raw geometric-face counting injection, a filled hull of perimeter P has area≤min(P²/16,650²). Its total rooted word activity is bounded by n4^P exp[−8P+.04 min(P²/16,650²)]. Handle P4/6/8 directly as before, and P10..40 using ratio1/674.

For42≤P≤2600, ln4<1.4 gives log activity per root≤f(P)=−6.6P+P²/400. This convex function has maximum at an endpoint; f(42)=−272.79 and f(2600)=−260. Hence at most2600 terms each bounded by e^-260 suffice. For P>2600 the area cap yields logactivity≤16900−6.6P, whose tail is bounded by2e^-260. Replace e^-260 by2^-260 conservatively. The bounded-hole gas factor is≤1/(1−651²κ), with κ≤(1/745)^4/(1−1/745).

The executable exact-rational certificate core650_occupation.py gives
Z650/w(a)−1 <1.087×10^-7.

Therefore all uncertain hard-source numerator occupation is confined to configurations with an actual component not fitting a650-square, including winding components. This is a substantially stronger localization than a rare first exit from box164; it does not presume those exits are short.

## What this does not do
No bound is obtained here on the occupation outside A650. Configurations there can carry large Gibbs weights and very small equilibrium potentials, so dropping h_a globally fails. Large elongated components, compact supercritical components, thermal companions and winding states all remain in the actual problem. A weighted initial-distribution comparison, growth proof, or complete killed-generator estimate is still required. This is not a mean-first-passage solution.

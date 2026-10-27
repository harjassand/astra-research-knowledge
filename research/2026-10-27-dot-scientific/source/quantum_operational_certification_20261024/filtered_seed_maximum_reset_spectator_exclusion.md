# Maximum-reset spectator exclusion at a faithful filtered-seed local minimum

26 October2026. Exact actual-source second-order/first-order contradiction. Independent PASS: `filtered_seed_maximum_spectator_independent_audit.md`.

## Statement

At a faithful fixed-TrH local minimum of Delta(X(H,A)) with A>=0 fixed, suppose H,A share a reducing eigenline and do not commute on its active2x2 complement. That common spectator CANNOT carry a largest eigenvalue of A. Together with the independently received middle-spectator exclusion, a noncommuting local minimum must use a MINIMUM reset eigenvalue as its spectator.

In the compact negative-value reduction, the reset has rank2. Hence the only remaining noncommuting negative-minimum core is a CLEAN spectator: A=0 direct-sum A2 with A2>0. No value sign is asserted for that remaining core.

## Actual Hessian order

Write A=A2 direct-sum b, with b>=lambda_max(A2), and H=H2 direct-sum h, h>0. Diagonalize A2 and gauge the nonzero H2 off-diagonal z positive. Use the stationary coefficients of `filtered_seed_faithful_stationary_common_eigenline_theorem.md`:

 alpha>0,beta>0,c,n real with n<0,
 c=-[alpha b+beta]/h<0.

Set r=-c>0 and N=-n>0. The actual transverse H13,H23 second variation has coefficient matrix B. Conjugating B by the fixed qubit swap gives exactly

 J B J*=N(H2-hI2)+r(A2-bI2).

Therefore the local-minimum Hessian condition B>=0 forces

 N(H2-hI2)>=r(bI2-A2)>=0.                         (1)

In particular H2>=hI2. This is a necessary source-derived order, not an assumed entropy-order comparison.

## Exact resolvent comparison

For each t>0, the active resolvent block is spectrally equivalent to

 K2(t)=sqrt(H2)(A2+tI)^(-1)sqrt(H2).

Since A2<=bI and H2>=hI, ordinary inverse/congruence order gives

 K2(t)>=H2/(b+t)>=h/(b+t)I2=k(t)I2.

Thus its active eigenvalue product p(t) obeys p(t)>=k(t)^2.

The exact active-trace derivative is

 g=F_s=2/(s+2)+2(k+2)/[p+(k+2)(s+k+2)]-9/(p+3s+9)-1/(s+k+1).

The elementary acquired positivity lemma in `filtered_seed_subthreshold_spectator_orientation_theorem.md` shows g>0 whenever 0<=k<=2, and also whenever k>2 and kp-k^2+4>=0. The latter condition here is strict because

 kp-k^2+4>=k^3-k^2+4>0.

For completeness, when k>2 the cleared numerator is A_c s^2+B_c s+C_c with A_c=3(kp-k^2+4), C_c>0; B_c is increasing in p and at p=k-4/k equals2(k-1)^2(k+2)(k^2+8k+4)/k^2>0. This proves the asserted positivity without an unproved spectral monotonicity statement.

Consequently g(t)>0 for EVERY t>0. But the active noncommuting orientation is a two-sided actual unitary variation, and its stationary equation is

 integral_0^infinity g(t)/det(A2+tI) dt=0.

The integrand is strictly positive, a contradiction. Singular A2 is harmless: the global rank2-reset derivative receiving already establishes integrability and the orientation variation never changes reset rank. Repeated maximum reset eigenvalues are also covered by(1); no strict spectral gap in bI-A2 is needed.

## Scope

This excludes a maximum-reset spectator using only H stationarity and local-minimum curvature at fixed A. It is stronger than excluding the former superthreshold TypeII core; no assumption h>2b is required. It does not transfer to the anchored gap, whose H derivatives include a changing baseline. It also does not imply generic physical/reference pinching or a universal orientation endpoint minimum, which has a separately certified counterexample.

## Direct whole-value order corollary

The same proof gives a value comparison without stationarity. Suppose H,A share a line with eigenvalues h,b and

 H2>=hI2, A2<=bI2.

Then for EVERY relative orientation of the fixed active H2,A2 spectra the actual resolvent obeys K2>=kI and hence F_s>0. Their active product p(t) and spectator k(t) are orientation-independent, while ordinary2x2 trace rearrangement minimizes s(t) simultaneously for all t by pairing the larger H2 eigenvalue with the larger A2 eigenvalue. Thus the actual deficit is bounded below by that aligned source, already paid by `aligned_filtered_seed_cq_dilation_value_theorem.md`.

Therefore this entire noncommuting shared-line class is nonnegative: a smallest main-Schmidt eigenline paired with a largest reset eigenline. No h<=2b assumption is required. Singular endpoints follow by the same common positive regularization preserving both displayed orders. This is a restricted actual orientation comparison, not the false universal endpoint-minimum claim.

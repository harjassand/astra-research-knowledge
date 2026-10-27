# Independent audit: all translated quartics pass both actual laws

25 October 2026.

## Outcome

The N=2048 interval moment receipt and exact rational Bernstein certificate establish

E_ν1 W_a(A+X)-W_a(A)>1,
E_peeled W_a(A+X)-W_a(A)>1,

for every real 2 by 2 background A and every -1≤a≤1. The second assertion uses the actual randomized-and-ball-peeled law, not a surrogate positive distribution. No parameter grid, background grid, or physical anisotropy sweep is involved.

This conclusion is limited to translations of the stated untransformed quartic family. It is not a statement about all rank-one-convex functions, all physical pullbacks, or full laminate completion.

## Independent checks completed

1. `check_all_background_reduction.py` verifies the complete full-matrix gap by symbolic expansion, including the skew coordinate, and independently verifies the exact trace square completion. It checks all four rational corners proving D>I/50, the ball fourth moments, the degenerate parameter identities, and the degree-four scalar numerator.
2. Read and audited every operation in `certify_background_bernstein.py`. Its degree-two Bernstein representations of α,β,γ are respectively [0,-4,16], [0,24,0], [16,-4,0]. Its exact interval multiplication, degree elevation and Bernstein product formula are correct. Hexadecimal input endpoints are interpreted as exact rationals. The numerator has the correct factor 6(1-a), and the gap target is subtracted before multiplying by the determinant.
3. Independently derived the ball moments Eτ⁴=243/2240, Eτ²|y|²=153/2240 and E|y|⁴=171/2240 from isotropic fourth moments. Subtraction of 1/30 of these gives exactly 81/22400, 51/22400 and 57/22400. The coefficient covariance subtraction gives 99/200. These signs and constants agree with the code.
4. Independently reran the entire N=2048 moment integration, processing all 4,194,304 phase boxes. All saved moment bounds, including their hexadecimal endpoints and auxiliary endpoint data, reproduced exactly. The independent run is `independent_nu1_moments_N2048.json`; elapsed time was approximately 4.27 seconds.
5. Ran the exact rational Bernstein certificate on those input bounds with uniform gap target δ=1. The five certified lower endpoints were approximately

   1.8866952118745164,
   1.6898266693751172,
   1.7889115025140410,
   1.2739923402645006,
   0.5921539941833247.

   These displayed decimals are only summaries. Positivity is checked on the exact rational endpoints in `independent_bernstein_N2048_delta1.json`.
6. Added a genuinely different algebraic implementation in `independent_certificate_audit.py`: construct the 4 by 4 augmented quadratic matrix directly from the unreduced full-background gap, compute its exact symbolic determinant, divide by its removable factor, and convert the resulting quartic from power basis to Bernstein basis. On an exact dyadic input tuple, all five coefficients agree exactly with the primary implementation. This tuple test is an algebra cross-check, not the positivity proof. The same script proves all 105 Bernstein multiplication/elevation basis identities through degree four and verifies exact moment repeatability and actual interval coefficient positivity. Its receipt is `independent_certificate_audit.json`.

## Why the endpoints and arbitrary skew backgrounds are covered

For the signed lower-bound proxy, write b=(p,h), x=(1+a)t, v=N-Lc/m and H=mD. For every parameter in the closed interval, including both degenerate endpoints,

G_proxy(A)-δ
 =24m[x+L/(6m)+(1-a)cᵀb/m]²
 +8(1-a)[b+D⁻¹v/2]ᵀD[b+D⁻¹v/2]
 +16m(1+a)r²
 +Pδ(a)/(3m det H).

This identity does not divide by 1+a or 1-a. Here m>0, D>I/50, and the last numerator has five strictly positive interval-Bernstein lower coefficients for δ=1. Therefore the last term is strictly positive and every preceding term is nonnegative. The potentially discontinuous optimized limit as a tends to -1 causes no gap in the proof.

## Source and order audit

The exact conditional root law lies below the uniform-partial law by direct one-dimensional rank-one Jensen on each original chord. The uniform coefficient ball is itself a laminate by three centered coordinate contractions. Thus its translated W gap is nonnegative. Since ω<1/30,

G_peeled ≥ G_root-ωG_ball ≥ G_root-(1/30)G_ball=G_proxy,
G_root=G_proxy+(1/30)G_ball ≥ G_proxy.

Both target conclusions therefore follow from the same proxy certificate. No downward-inheritance inference from a shared upper law is used.

The moment proof relies on the explicitly recorded IEEE-754 arithmetic model and the exact structural first-root formula, conditional-mean covariance identity and admitted global rank-one convexity of W_a. Its trigonometric endpoints use exact rational bounds, not library trigonometric evaluations. The independent rerun verifies reproducibility; the operation-by-operation interval audit supplies the enclosure justification.

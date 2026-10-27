# Independent five-eighths policy affinity receiving audit

2026-10-25. Governing specializations: `three_axis_w1_a625/` (actual .085 source-approximation policy) and `w1_smoothed_a625/` (actual .15 policy). These are NEW transformed laws: globally scale the underlying complete zero-root policy by5/8, S3-average, then Brownian-complete. Their affinity certificates do not assert that the transformed laws retain the original policy's W1 bound. Computational normalized pole weights are not themselves asserted paid.

## Discovered arithmetic gap, correction and receiving

Both inherited sample verifiers originally bounded sqrt input error by ds_error/(4/5). That denominator was valid for the halfscale distance envelope but NOT for the new guaranteed distance8/25: the sum of the two square roots need only be near16/25. I flagged this before accepting either specialization.

Both verifiers now assert ds_error<(8/25)^2-(3/10)^2 and use denominator3/5. Thus both square-root operands exceed3/10 and the bound is valid. Independent exact replay gives potential/flux error factors:

- .085 specialization:18490.650227864593u /866714.2048835759u;
- .15 specialization:14614.65022786459u /798884.2048835758u.

All remain below the existing fixed65536u and2^22u sample allowances. Therefore this proof correction requires no numerical interval weakening or new fit. The earlier invalid denominator is not retained as a justification.

## Geometry, source law and actual/proxy distinction

Each proxy pole is exactly checked in[-5/8,5/8]^3 and C(x)>37I/100. The trace-zero perturbation bound gives distance>=37sqrt3/200>8/25. Actual scaled poles have C>=3I/8; the segment between an actual pole and its proxy stays in the conservative envelope.

For .085, the previously independently audited2126 exact algebraic atoms and positive normalized2^80 weights give4378 merged S3 dyadic2^-60 proxy poles. For .15, the836-atom interface gives3409 proxy poles at denominator2^48. Independent reconstruction checks every actual endpoint enclosure, pole rounding, S3 mass merge, exact unit mass and underlying actual-policy/interface hashes.

The kernel full-variation Lipschitz constant is3/R<10 on the connecting segments. Therefore E=weight_L1+10*pole_displacement receives the ENTIRE full-variation error. For probabilities, the positive-part Cauchy-Schwarz argument yields affinity error<=sqrt(E/2). Exact exports verify payments1/400000000 (.085) and1/40000 (.15), both applied on BOTH sides of the final affinity intervals. These are not midpoint-only or weight-only payments.

Full source measure remains the actual Haar cosine pushforward, integrated on the entire4096-by4096 phase torus with cell mass1/N^2. S3 phase-orbit restoration is unchanged from the independently audited halfscale total-field receiver and does not assume even-sign invariance of either paid law.

## Wider holomorphic and boundary envelopes

For imaginary phases<=1/24, coordinate changes are bounded by1/23,1/23,1/11, so |Delta Z|<11/100. The exact inequality
(8/25)^2-2(8/25)(11/100)-(11/100)^2>1/64
proves the principal reciprocal-square-root field analytic and bounded by8. Bounds |Z_i|<=12/11, |Z_i-x_i|<=151/88, |partial_i F|<=552/121 give total complex flux bound<20000. Geometric alias tails use24/25; they have been changed consistently, not copied from the narrower halfscale strip. Real sample bounds are potential<4 and flux<70. Positive total mass1, not an unpriced pole-count factor, controls accumulation.

Global relative density upper110 follows from7pi/(2R^2)<110. For a vertex-height cap h<=1/8, every image pole is coordinate-separated in the local box by g=3/8-2h>=1/8. The eight-image triple Green derivative bound is20/(3pi g^4). Triple integration, tangent half-ball comparison, normal-flux factor1/2 and conversion to source density give
r<=240pi h^3/g^4 <(5280/7)h^3/g^4.
Taking min with110 is valid for every pole in the envelope and hence every positive mixture. Other vertices follow from transforming the domain/source/envelope, not the paid controls. The full-torus signed corner-height formula, positive rounding reserves and gap downward rounding receive every upper cell, including those outside central charts.

## New residual-grid sharpening is valid

The exact degree48 harmonic polynomial is unchanged by sharpening. The total-field DFT certificate supplies a finite trigonometric polynomial p and SEPARATE uniform actual errors E0,E1,E2 for R-p, its gradient and Hessian. No derivative is inferred from a value error.

The explicit normalized transforms evaluate p,px,py,pxx,pxy,pyy on the unshifted2048 grid. Real-part projection and the signed-frequency/Nyquist convention are valid: evaluation is of the real part of the finite polynomial, with all coefficient/alias discrepancies already paid. Every phase point is within coordinate displacement h=pi/N of a grid point.

Let A,L,H2 be the certified coefficient norms, H3=sum|c_k||k|^2(|k1|+|k2|). Then
D0<=gridmax|p|+hL+E0,
D1<=gridmax(|px|+|py|)+2hH2+E1,
D2<=gridmax max(|pxx|+|pxy|,|pyy|+|pxy|)+hH3+E2,
with the separately added evaluation errors shown in the script.

The gradient variation uses(|k1|+|k2|)^2<=2|k|^2; Hessian grid rows bound the real symmetric operator norm. The finite-polynomial Hessian variation uses the rank-one matrix k k^T and |exp(ik.d)-1|<=h(|k1|+|k2|). NO bound on the actual residual's third derivative is needed: H3 is only for p, and E2 already controls the true residual Hessian everywhere. Positive weighted H3 summation, binary64 grid maxima, decimal display conversion and FFT evaluation errors are paid. Taking the minimum with the older certified bounds is legitimate.

## Whole-cell assembly and scalar arithmetic

The Q_y global tangential-remainder/normal-flux argument and pi/4 density normalization are unchanged. The scalar-flux coefficient polynomial, its evaluation errors and actual-field E0/E1/E2 remain separately received. Each cell pays full Taylor variation, and both lower and upper densities are outward-rounded before exact integer square-root integration.

The new sharp chart constants exceed the old halfscale M<13 envelope. I flagged this explicitly. Actual maxima are<50, while both coefficient receipts give A<6,L<29,H<200 and actual-field errors<1. The new exact rational `three_axis_w1_a625/verify_sharp_assembly.py` checks these inputs and propagates the scalar assembly with |T|<=7, |Tx|,|Ty|<=30, B<=49, |Bx|,|By|<=193, h<=.001. Its error is<2.232e-12, below the final1e-10 reserve. Direct B/B-gradient input errors are separately paid by M*1e-6; the checker does not set them silently to zero. The tiny extra final reserve-add rounding is also far within the remaining margin. The implemented upper h is safely above pi/N and may itself be treated as the exact positive step bound.

## Scope of outcome

Sharpening improves a certificate for an existing law, not its actual affinity. Changing the underlying policy or global scale changes the law. The two5/8 intervals overlap, so their ordering of lower endpoints cannot prove the .085-derived law superior to the .15-derived law. Neither result proves a global optimum, exact source membership, fixed-envelope convergence, or the full Morrey claim.

Here “true residual/field” means the exact Brownian potential of the computational positive proxy, as opposed to its numerical trigonometric approximation. It does not silently replace the original unknown absorption weights. The transfer to the original paid law occurs only through the separately received variation/affinity payment.

All six derivative-factor arrays in the sharpening transform were additionally checked exhaustively against their exact Gaussian-integer formulas on the full2048-by2048 frequency grid. Thus the small complex powers used for derivative orders0,1,2 introduce no unpriced opaque-power discrepancy on this executed platform.

## Completed replays and accepted intervals

**PASS for BOTH specializations.** Full exact exporter, harmonic and flux compilers, corrected primitive verifier, total-field orbit DFT, six-field sharp residual receiver and full4096²-cell spectral receiver were independently replayed. Independent exact geometry/proxy reconstruction and complete saved-array integer integration also match.

- Actual .085-derived law at5/8: [.8893041904600858,.8978776135719108], including full2.5e-9 proxy payment.
- Actual .15-derived law at5/8: [.8859884591073331,.8977410500370644], including full2.5e-5 proxy payment.

Exact rational endpoints and independent receipts are saved in each specialization folder. The corrected sample-bound issue did not change the fixed spectral error allowances or any accepted numerical interval. The two intervals overlap.

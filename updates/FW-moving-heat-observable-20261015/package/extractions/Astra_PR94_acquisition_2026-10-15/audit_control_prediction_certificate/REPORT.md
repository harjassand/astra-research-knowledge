# Independent audit of finite-noise scalar-control certificate

## Verdict

The two current rational interval scripts replay successfully. The 14-setting nonreciprocal example has robust coercivity h = 0.197391674791637 and uniform unit-cube scalar prediction error bound 0.011826302949608439, strictly satisfying h > .19739 and error < .011827. The 13-setting reciprocal pair-hull variant has h = 1.2535765020417209 and error < .027424. These are sound deterministic, synthetic bounded-error certificate examples. They are not physical acquisition or measured-noise demonstrations. Audit command:

    python ../audit_control_prediction_certificate/audit.py

Canonical scripts are untouched.

## Interval identification and branch logic

All arithmetic is Fraction arithmetic. Square-root lower endpoints floor sqrt(numerator/denominator) on a 10^-30 mesh, and upper endpoints add one mesh unit; thus outward inclusion is exact. Division requires a denominator interval entirely on one side of zero. Every successful interval Gauss-Jordan operation encloses its exact arithmetic counterpart; interval dependency only enlarges the result.

For singleton differences delta(t), the t=1/2,1 formulas d=(delta(1)-2 delta(1/2))/(delta(1/2)-delta(1)) and a=2 delta(1/2)(1+d/2) are correct. Baseline reuse creates dependence, which the interval arithmetic safely ignores. All singleton and pair interpolation denominators in the examples exclude zero.

For a pair, p=H_ij H_ji and q=a_i H_ij+a_j H_ji satisfy q-delta p=r. The two-setting solution in the code has the correct sign. The directed-entry candidates are ((q-sqrt(q²-4a_i a_j p))/(2a_i),(q+sqrt(...))/(2a_j)) and the opposite sign assignment. The product and weighted-sum constraints are thus jointly respected before interval over-enclosure.

The worked script fixes the first pair branch. This is justified only for scalar-function identification modulo global weighted transpose Hstar=diag(a)^-1 H^T diag(a), with every a_i nonzero. This involution swaps every pair branch and preserves the scalar response for every diagonal control. Therefore a scalar-equivalent representative of the truth lies in the four enumerated boxes. It is incorrect to describe this as inclusion of every compatible physical H. The N854 source proof explicitly supplies the gauge; the new finite-noise statement must retain it. The example verifies positive a intervals.

A representative can be discarded only when its complete interval response enclosure is disjoint from the measured triple interval. This is what the code does. The measured triple interval is [8.7406660764,8.7406660964]; the three false-branch upper bounds are 8.71770747293, 8.70093632507, and 8.73831938077. All are strictly separated. The surviving box contains the fixture exactly, and the audit asserts this with rational comparisons. General algorithms must retain all nonexcluded candidates and return unresolved/no certificate if they cannot certify the resulting family; uniqueness cannot be presumed from exact generic identifiability.

The reciprocal example correctly intersects a discriminant interval with [0,infinity) before square root, provided its upper endpoint is nonnegative. This uses the algebraic fact that a real model's discriminant is a square. It then takes coordinatewise hulls of both branches, losing correlations conservatively, with no triple measurement or branch-separation requirement. This gives a valid enclosure even at exact weighted reciprocity and for nearby compatible coefficients. A wholly negative discriminant interval must cause rejection rather than clipping to zero.

## Coercivity, resolvent, and prediction proof

For diagonal positive Lambda, use ||x||_Lambda²=x^T Lambda x and the associated operator norm. If (Lambda H+H^T Lambda)/2 >= h Lambda, and D is diagonal with 0 <= D <= U I, then

    ||D(I+HD)^-1||_Lambda <= U/(1+hU),

provided 1+hU>0 (the examples have h>0). For positive D this follows by writing the operator as (D^-1+H)^-1 and taking the Lambda inner product. For zero entries, restrict to the active coordinates: w=D(I+HD)^-1x has zero inactive coordinates, and on the active set x_S=(D_S^-1+H_SS)w_S. The same bound applies. The active block is invertible by coercivity; the inactive block in I+HD is an identity block, so the full inverse exists. D=0 gives the zero operator directly. This avoids an unsupported continuity argument at an assumed singular endpoint.

The robust condition follows from a nominal weighted symmetric-part margin h0 and ||H-Hhat||_Lambda<=deltaH: h=h0-deltaH. For Lambda=I and three controls, ||E||2<=||E||F<=3 max|E_ij|. The scripts correctly take the maximum distance of both interval endpoints from a specified rational nominal matrix, not just half an interval width. Exact symmetric Gershgorin margins for those nominal matrices are h0=1/5 and 13/10 respectively. The audit independently checks these rationally.

With K_H=D(I+HD)^-1, the resolvent identity is K_H-K_Hhat=-K_H(H-Hhat)K_Hhat, also valid on the active coordinates. If both have bound B=U/(1+hU), then scalar prediction error is at most

    epsilon0 + ||a-ahat||_(Lambda^-1) B ||1||_Lambda
             + ||ahat||_(Lambda^-1) B² deltaH ||1||_Lambda.

For three coordinates and Lambda=I, the first coefficient-error product is bounded by 3 max|a_i-ahat_i|. For ahat=(1,2,3), ||ahat||2||1||2=sqrt(42)<13/2; for ahat=(1,1,1), this product is 3. These are precisely the script constants. The same robust h is valid for the nominal and every member of the enclosing box. The resulting bound is uniform over the full [0,1]^3 cube, not a grid check.

## Statistical interpretation

For independent zero-mean Gaussian repeats of known standard deviation sigma=10^-7 at each of M=14 fixed settings, N=1588 repeats per setting gives simultaneous radius eta=10^-8 coverage failure at most

    2 M exp(-N eta²/(2 sigma²)) = 0.009973781392596935 < .01.

Total samples are 22,232. Independence between different settings is unnecessary for the union bound; the usual independent-repeat assumption within each setting is sufficient. Known independent sub-Gaussian noise with the same variance proxy gives the same bound.

The correct conclusion is P(certificate passes and its claimed bound is false) <= .01. It is not generally correct to claim P(bound true | certificate passes)>=.99, because conditioning on a data-dependent pass event can alter coverage. Nor does the calculation guarantee that a noisy data set will pass: current readings are exact synthetic centers with declared deterministic error bars. A bounded nonzero bias does not decrease under repetition and must be added to the uncertainty radius or separately controlled. Repeated/adaptive tries require time-uniform or error-budgeted coverage; fixed-sample coverage cannot justify optional stopping. No uniform stopping guarantee follows near ill-conditioned or nonidentifiable models.

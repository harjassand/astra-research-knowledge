# Exact arithmetic margin certificate for the saved probe bank
2026-10-29. New construction by the independent reviewer; requires separate receiving review. It complements, rather than replaces, the matrix-Freedman theorem. No hardware claim.

## Statistical radius without a floating logarithm
Take e=23/200=0.115 and ell=3657/500=7.314. Exact rational arithmetic verifies
m e²/[2(900+31e)] >=ell,
for m=1,000,000. The sum of the first61 positive Taylor terms of exp(ell) is strictly larger than1500, verified with Fraction arithmetic. Thus exp(ell)>1500 and the three-edge failure bound75 exp(-m e²/[2(900+31e)]) is strictly below1/20. This is a rigorous conservative substitute for the decimal root0.1149605.

## Rational matrix congruence bounds
The actual sums are exact integers and Jembed has only zeros and ones. Consequently A=S/m-Jembed and B=A^T A are exact rational matrices. Floating SVD supplies candidate right vectors Q and squared singular values lambda_j; their binary floats are then treated as EXACT rationals, not assumed exact eigenvectors.

The verifier computes G=Q^T Q-I and C=Q^T B Q-diag(lambda) with exact Fraction arithmetic. Let delta=||G||_infinity and epsilon=||C||_infinity. Both matrices are real symmetric, so these row-sum norms bound their spectral norms. Each is below1e-12, checked exactly. Q is invertible since delta<1. Generalized Courant–Fischer for the pair(Q^T BQ,Q^T Q) bounds ordered eigenvalues of B between(lambda_j-epsilon)/(1+delta) and(lambda_j+epsilon)/(1-delta); the verified diagonal lower endpoints are positive. This supplies exact second-singular-value lower bounds0.3372,0.3508,0.3441, and verifies the first singular value is below e. Subtracting e gives the rigorous gap lower bounds0.2222,0.2358,0.2291.

## Certified singular direction and proper-rotation candidate
For the final candidate column q, exact arithmetic verifies |q^Tq-1|<1e-12, ||Bq-lambda_min q||²<1e-24, and the certified second eigenvalue minus lambda_min exceeds0.1. Expanding q in the exact eigenbasis shows its component outside the true minimum eigenspace has norm<1e-11. After normalization it lies within1e-8 of an appropriately signed exact unit minimum eigenvector; this deliberately loose bound also covers its normalization error.

Let R be the floating proper-polar candidate, interpreted as a rational matrix. Its exact Gram defect has row norm<1e-12 and its exact determinant is positive. Therefore its exact polar factor R_star exists in SO(3) and ||R_star-R||F<1e-10, since each singular value of R differs from one by at most delta/[1+sqrt(1-delta)] with delta<1e-12.

The verifier brackets sqrt3 between two exact decimal rationals whose squares straddle3. It uses this bracket to bound ||R-sqrt3 sign(q)||F² exactly, and obtains ||R_star-sqrt3 sign(q)||F<0.0600 for every edge.

Using the conservative s1>=0 in the singular-cone argument, alpha<=e/s2_lower. Exact squaring verifies h=sqrt(2-2sqrt(1-alpha²))<0.35. The true SO3 frame is therefore within sqrt3*0.35+1e-7 of one of the two signed approximate directions. The opposite sign has distance at least2-0.0600 from SO3: for any R_star in SO3, min_{S in SO3}||S+R_star||F=2, and apply the triangle inequality. Since1.94 exceeds the cone radius, the chosen sign is uniquely certified.

Finally ||R_star-C_true||F<0.0600+sqrt3*0.35+1e-7<0.667. This holds simultaneously on the same95% statistical event, conditional on the common-kernel structural promise. The certified mathematical rotation is R_star, the exact polar factor of the saved/reproducible rational candidate R. A real control implementation must still pay its approximation and calibration errors; this proof does not certify hardware rotations.

## Reproduction
Run check_rational_margin.py with the original actual_bank_counters.npz available at its declared path. NumPy proposes candidates; Fraction arithmetic verifies all load-bearing inequalities. The checks do not read true frame O, predictable bath moments, source coefficients or final bath state. rational_margin.json records the conservative claims. Original precise decimal values remain useful diagnostics, while these rounded margins have an exact arithmetic warrant.

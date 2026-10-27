# Independent audit: mean-dominant score and full commuting anchored filter order

**PASS — 26 October 2026.** Governing note: `mean_dominant_reference_score_and_commuting_filter_order.md`. This receives the full commuting reset/filter comparison. Noncommuting pairs and the original general accepted-only GLS comparison remain open.

## Actual score and balanced lower source kernel

The actual reference-congruence score scales both its main Schmidt weight r and its own reset weight a. The correlated input, reference and two WH pair blocks give exactly the displayed integral with prefactor r. Their signed masses and first moments cancel; this is not a derivative holding a fixed while changing r.

At fixed x and sum of companions, convexity of the reciprocal gives the stated lower bound by equal companions. Its multiplier `r s/(a+s)^2` is nonnegative. The balanced companion function is a scalar Stieltjes transform of total mass M0=(u+v)/2<=r; no physically realizable pointwise replacement is required because this is an explicit scalar lower bound on the acquired score integrand.

If the bath never exceeds one, the factorized kernel is pointwise nonnegative. Otherwise its unique crossing theta is positive. Scaling ALL main/reset masses by 1/theta and s=theta z leaves the sign unchanged (the original score is theta times the rescaled score). The rescaled bath has value one at z=1, hence total mass at least one and r>=1. The tilted weights sum to one and have mean `M=M0-1<=r-1` exactly.

## Effective harmonic bath and exact derivative certificate

For ell=E[1/(B+z)], beta=ell^-1-z satisfies 0<=beta<=M by inverse bounds/Jensen and beta'>=0 by Cauchy. The sharper Cauchy inequality using sqrt(B) and sqrt(B)/(B+z) rearranges exactly to `beta'<=beta(M-beta)/(zM)`. At fixed beta this upper bound increases with M, so replacing M by r-1 is valid. M=0 and r=1 are handled separately with beta=beta'=0; no division by zero is used.

The rational ratio is reacquired from the balanced actual score. Its total derivative is `R_z+beta'R_beta`, with BOTH partial derivatives at fixed r. Substitution `r=beta+1+k` occurs only after differentiation in the checker, so it does not erroneously vary the main weight. Affineness in beta' makes the two endpoint tests sufficient regardless of the sign of R_beta.

The self-contained exact checker was rerun to exit zero. It verifies the source ratio, the first endpoint's 662 positive coefficients, and the second endpoint's exact two squares plus 848 positive coefficients. Denominators are positive for z>0,r>1 by the displayed positive factors; r=1 uses the first endpoint. The mean constraint beta<=r-1 is load-bearing and is received from the actual tilted bath.

The resulting composite ratio is nondecreasing. Centering at z=1 against the old zero-area baseline therefore pays the signed integral. The ratio is finite at the crossing and at infinity; finite-bath/source formulas receive local integrability at zero. Alternatively all singular main/reset endpoints follow from the continuous XlogX score while preserving the mean-dominance condition by a common positive regularization of the three main weights. The pointwise-balancing and centered-integral arguments do not require a falsely monotone finite-r pure baseline.

Thus the actual congruence score is nonnegative whenever `2r>=u+v`, with arbitrary aligned reset weights. This includes, but is stronger than, the largest-coordinate condition. No positivity of smaller-coordinate scores is asserted.

## Finite commuting comparison

After removing the reference-unitary polar factor, simultaneous diagonalization is legitimate because A commutes with Z*Z. The current main weights are d*k_i and the current reset weights are a_i*k_i. Lowering the largest k1 to k2 always keeps that main coordinate largest, so its actual derivative Q1/k1 is nonnegative. Then lowering the tied pair together to k3 keeps each at least the remaining weight, and the sum of the two actual congruence derivatives is nonnegative. Both main and reset entries change along this path, precisely as required by the score theorem.

The endpoint is kappa times the original seed. Homogeneity therefore proves

`D(filtered) >= lambda_min(Z*Z) D(unfiltered)`

for every commuting invertible reset/filter pair. Singular K follows from K+epsilon I and entropy continuity; d=0 is the exact product-reset endpoint. This is not monotonicity along every arbitrary commuting path or for separately normalized deficits.

The actual-source checker was rerun: 40 mean-dominant scores (including own weight below the largest but above the companion mean), harmonic derivative bounds, and 24 complex commuting finite comparisons all pass. The exact Stieltjes/SOS chain is the proof; these are corroborating source tests.

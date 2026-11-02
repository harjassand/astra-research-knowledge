# Final result: a certified repetition obstruction, not a new capacity construction

For the explicit rectangular-GKP Gaussian-syndrome quantizers below, **no block length of maximally mixed repetition/GHZ code inputs has positive coherent information**, in any of the three Clifford-axis orientations. A separate parent calculation certifies that the selected flagged channel is **not antidegradable**. Thus this is a genuine restricted-family obstruction, not a zero-capacity claim.

## Actual channel and resource count

Use quadrature variance v=.38 (also checked at .4), rectangular aspect r=3, and normalized absolute syndromes in [0,sqrt(pi)/2]^2. Divide each axis into 64 equal cells. The provided 64×64 lookup labels each cell by one of K=3 flags; retain all flags. There are 4096 classical cells, NOT 4096 output flags. Physical syndrome coordinates are obtained by scaling the two axes by sqrt(r) and 1/sqrt(r).

The assignment is fully exported in `certified_repetition_quantizers.json`. Its row-major uint8 SHA256 at v=.38 is

`9e7cf502c6c734cc1fed4d63245f14fd86669c72829c75d90db424880a58e199`.

Central Gaussian-CDF integration gives one-use maximally mixed logical coherent information −.02169287080147868 bits, compared with −.01030412470924 for the continuous-syndrome diagnostic. Output likelihoods are actual Gaussian cell integrals, not fictitious quadrature weights. GKP preparation and syndrome-measurement implementation remain separate resource questions.

## All-n inequality and proof

For each flag f of probability w_f, write its Pauli probabilities in [I,X,Y,Z] order. In the Z orientation let

 rho = sum_f w_f[(p_I-p_Z)^2/(p_I+p_Z)+(p_X-p_Y)^2/(p_X+p_Y)],
 b = sum_f w_f h2(p_X+p_Y).

For the equal-mixture n-qubit repetition input,

**I_c(n) <= rho^n - b^n.**

To see this, write I_c=A_n-B_n. The phase-information term has the exact expansion

 A_n=sum_(k>=1) c_k [E(t^(2k))]^n,
 c_k=1/[ln(2) 2k(2k-1)], sum c_k=1,

where t is the phase bias conditioned on flag and bit error, and E(t²)=rho. Hence A_n<=rho^n. The bit-ambiguity entropy B_n is the conditional entropy for repetition over a binary-input symmetric channel W with H(W)=b. If a(t)=1-h2((1+t)/2), positivity of its power-series coefficients implies a(tu)>=a(t)a(u), by the nonnegative covariance of the two decreasing sequences t^(2k),u^(2k). Together with the polar chain-rule entropy identity, this implies H(W-plus-V)>=H(W)H(V). Iterating gives B_n>=b^n. Therefore rho<b excludes every n, without extrapolating a finite-size scan. Permute X,Y,Z for the other orientations.

## Interval certificate

At v=.38,r=3,K=3, rigorous enclosures for b-rho are:

- X: [.00492438187410, .00492439558708]
- Y: [.00526134471131, .00526135853606]
- Z: [.00773757787320, .00773759256262]

At v=.4 the respective lower bounds exceed .02132277, .02164296, and .02762084.

The certificate uses 50-digit interval arithmetic, composite Simpson integration with eight subintervals inside each receiver cell, and the conservative Gaussian fourth-derivative bound

 |f_v''''(x)| <= 10/[sqrt(2pi) v^(5/2)].

This follows from |y^4-6y²+3|exp(-y²/2) <=16/e²+12/e+3<10. Gaussian image terms |m|<=8 are retained; all remaining mass is enclosed by 2exp(-[(8.5)sqrt(pi)]²/(2v)). Integration subintervals are proof work, not additional receiver resolution. Maximum joint-mass interval width is below 3.6e-10. Exact dyadic lower/upper endpoints for every w_f p_f,P are exported for rational downstream verification.

## Independent validation and limits

The multinomial repetition formula agrees with full density-matrix calculations at n=1,2,3 and logical weights .1,.3,.5 to within 3.4e-16. This validates the implementation but is not substituted for the all-n proof. Finite searches found no positive repetition example; apparent machine-epsilon positives disappeared under stable entropy-deficit and log-likelihood evaluation.

The theorem covers the equal logical mixture only. It does not exclude unequal mixtures or arbitrary symmetric rank-two states. The parent's `non_antidegradable_rational_dual.json` records the independent non-antidegradability certificate; it is not needed for the repetition theorem. No positive-capacity construction, practical implementation, or novelty claim follows from this negative result.

Core files: `certify_repetition_quantizer.py`, `certified_repetition_quantizers.json`, `flagged_repetition.py`, `REPETITION_ALL_N_OBSTRUCTION.md`, `repetition_density_validation.json`. The seed extraction and broader diagnostic comparisons remain saved separately.

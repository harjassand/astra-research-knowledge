# Independent audit: modular-commuting receiver and canonical-pinching obstruction

2026-10-25. **PASS after correction of one rational simplification.** The governing note is `wh3_flat_marginal_and_modular_commuting_theorem.md`. Its flat-marginal receiver is independently reconstructed in `wh3_flat_reference_marginal_purification_corollary.md`.

## 1. Actual spectral flags give an exact receiving class

If [rho_AR,I_A tensor rho_R]=0, the distinct positive eigenspaces R_j of rho_R give an actual orthogonal reference-block decomposition of rho_AR. There are no coherences between distinct marginal eigenvalues. Positivity also confines rho to the support of its marginal. If lambda_j is the eigenvalue on R_j and r_j=dim R_j, its block has trace p_j=lambda_j r_j and normalized reference marginal I_(R_j)/r_j.

The proved flat-marginal theorem therefore applies separately to every normalized block, with arbitrary quantum correlations and global spectra inside that block. N and E preserve the reference label. The direct-sum entropy formula has the same classical entropy H(p) in output, input and marginal; it cancels with coefficients 2-1-1. Consequently Delta_N(rho)=sum_j p_j Delta_N(rho_j)>=0 exactly.

This is not an inference that pinching an arbitrary state preserves its deficit. The block decomposition is a hypothesis already satisfied by the original state. Degenerate marginal eigenspaces may have arbitrarily large dimension, so the result is not limited to classical or qubit references.

## 2. Pinching example reconstructed from the actual matrices

For the displayed sigma, its phi eigenvalue is 3/10+1/18=16/45 and its |22> eigenvalue is 1/5+1/18=23/90; all other eigenvalues equal 1/18. Its marginal is exactly diag(19/60,19/60,11/30). The perturbation H has zero partial traces and connects the two distinct marginal spectral blocks, so canonical reference pinching fixes sigma and annihilates H.

The input BKM metric is 2 log(a/b)/(a-b)=20log(32/23), because the off-diagonal amplitude is one and a-b=1/10.

Under WH3, NH=-H^(partial transpose_A)/2. It has two disjoint pairs, |20><02| and |21><12| with their adjoints, each of magnitude 1/(2sqrt2). On these basis vectors Nsigma has eigenvalues 47/360 and 7/45=56/360. Their difference is 1/40. Each pair therefore contributes 2(1/8)40log(56/47)=10log(56/47), giving total output metric 20log(56/47).

It follows exactly that

2g_output-g_input
=20log[(56/47)^2(23/32)]
=20log(2254/2209)>0.

The initial draft simplified this ratio to 1127/1104, which was incorrect. The corrected ratio 2254/2209 remains strictly greater than one, so the mathematical sign and conclusion are unchanged. The author corrected the governing note and reported checking related scientific files for the old ratio.

## 3. The strict local obstruction follows without an uncontrolled limit

sigma is faithful with minimum eigenvalue 1/18, and ||H||=1, so sigma+tH is positive for |t|<1/18. Its marginal is constant. The second derivative of Delta_N along this direction is g_input-2g_output, strictly negative by the exact rational-log comparison.

The reference unitary diag(1,1,-1) fixes sigma and sends H to -H. Since N acts only on A, this symmetry preserves input, output and marginal entropies, making the deficit an even smooth function of t near zero. Its first derivative is therefore zero. The strictly negative second derivative proves Delta_N(sigma+tH)<Delta_N(sigma) for all sufficiently small nonzero t.

This refutes the needed free-pinching reduction Delta_N(rho)>=Delta_N(pinched rho). It does not prove a negative actual deficit: the positive baseline margin may dominate the local decrease. The source note correctly preserves this distinction.

## Scope

The full absolute WH3 target is proved whenever the input commutes with its own reference marginal. A possible exception must leave that class and, under the special WH3 purification duality, also evade the corresponding proved class on the complementary reference. Neither the stronger mutual-information-half theorem nor arbitrary noncommuting marginal inputs follows from this argument.

# Independent conditional scaled invariant and covariance cone — PASS

26 October 2026. Reviewed `SCALED_SLACK_SUFFICIENT_EXHAUSTION_INVARIANT.md` and `COVARIANCE_CONE_COMPATIBLE_MEAN_STEPS.md` analytically.

## Sufficient invariant and rates

Under C>=cVI and delta−gamma²V>=sV² with fixed positive c,s, V>0, the stated regression observation is defined since C is invertible and delta>0. Orthogonality gives Eh=0, EXh=v, E[q(X)h]=0, including gamma=0. The global bounds use |X|<4, V<=3, ||J||=1, a^TCa<=E q(X)²<=16V and hence |a|<=4/sqrt(c). These receive ||h||infinity<=K/V^(3/2) with the stated K. Epsilon=V^(3/2)/(2K) gives BOTH positive factors in[1/2,3/2], exact null child means and D0. The entire two-branch conditional mean-variance payment is epsilon²=V³/(4K²).

If finite zero-displacement label policies place every nonterminal descendant in the invariant with the SAME constants and retain all branches, their average conditional variance is unchanged. Jensen then gives v_next<=v−v³/(4K²). For positive successive values, (1−x)^−2>=1+2x gives the stated reciprocal-square increment and v_n<= (v_0^-2+n/(2K²))^-1/2. Zero-variance branches contribute zero and may stop. Applying the previously received complete axis-chord/source-variance coupling gives W1<=sqrt(3v_n), thus O(n^-1/4). Each finite generation remains a finite actual mean tree when every invoked label decomposition is finite.

The preservation hypothesis is substantial and is NOT proved by this theorem. No source exhaustion is established absent such a policy. Rates count generations, not bounded total computation or uniformly bounded label counts.

## Covariance cone

D0 implies tr(JC)=0. Since trJ=0, S=C−cVI is PSD and J-trace zero; for c<1/3 and V>0, trS=(1−3c)V>0. The zero-Rayleigh orthonormal basis construction for H=S^(1/2)JS^(1/2) works also in singular/zero cases, by trace-zero compression induction. Consequently S=sum wi wi^T with q(wi)=0. At least one nonzero wi has norm²>=trS/3, and subtracting t vv^T leaves a PSD matrix.

For any source-AC posterior, the degree<=2 feature Gram is positive definite: the ten restricted quadratic features are linearly independent, and a nonzero analytic pullback cannot vanish on its positive-measure density support. Centering is an invertible feature change. Thus the three prescribed linear and six zero quadratic observation moments, together with mass zero, admit a bounded polynomial solution. Taking epsilon small enough for positivity AND epsilon²<=t yields both covariances C−epsilon²vv^T and common varianceV−epsilon². The same c-cone follows from S−epsilon²vv^T+c epsilon²I>=0; D0 is preserved exactly.

The matrix capacity bound does not bound the observation sup norm or pay a macroscopic epsilon. The separate sufficient-invariant observation need not be this cone-preserving observation. Joint positivity, quantitative scale and BOTH-branch scaled-slack preservation remain open. Zero-displacement labels cannot repair a violated cone on every branch, since averaging such inequalities restores the parent's cone.

Minor editorial ambiguity reported: the reference to timelike formulas should explicitly mean the positive-gamma/timelike case, not the immediately preceding gamma-zero case.

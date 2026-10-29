# Whole review: specified anisotropic rotation-kernel operation

29 October2026. Whole-read root_rotation_kernel/PROOF.md including Section4,
consumer.py and EXECUTION.json. Analytical/program-scope result: ACCEPTED.
No independent numerical replay, finite-bit certification or native-gas
qualification is claimed.

The linear pair map preserves sum and total kinetic energy pointwise. Its
covariance map is exactly Phi(M)=(M+E RMR^T)/2 on ALL real3-by-3 matrices,
not only diagonal covariances. It is real unital CPTP. The Poisson mixture
exp[t(Phi-I)] is CP and unital. Its Choi matrix is real PSD, hence has a
real Kraus representation of rank<=9. Query probabilities use the unital
identity sum K K^T=I, and each initial query uses K^T z with BILINEAR
quadratics. This finite CP alternative is sound, but was not executed by
the supplied reset consumer. Its matrix/precision work remains charged.

Under the specified Haar mixture, the conditional q>=2 separating chance
is at least eta/3; other rotations can only add separating probability.
The rare expensive singleton branch also has a charged mean cost. D
commutes with EVERY orthogonal conjugation, so the Section4 decomposition
is exact. The reset query (z^Tz)F_1^0(n) with a uniform REAL unit n has the
right trace average without a covariance oracle. On the other branch the
query evolves by transposed finite rotations. The consumer implements
fixed.T correctly. Counting actual Poisson rotations gives the maximum
(1-eta)/(e eta), without replacing long paths by uncharged work.

Thus the complete expected collision cost is bounded, for degree q, by
`3(q-1)/eta+q(1-eta)/(e eta)`, plus terminal/real-random arithmetic work.
The full-law contour and factories require no isotropy of rho beyond the
qualified splitting/singleton operations. Common Gaussian convolution
still commutes pointwise, so the resolved-input transport is valid too.

The consumer's9-by-9 row-vectorization reference agrees with its R M R^T
convention. It executes the reset operation, not a Choi factorization or a
physical circuit. Counts for singleton rotations/resets are separate from
the q>=2 counters and are actually retained. The25k singleton and1500 full
floating outputs are consistency/work evidence, not proof of the theorem
or a full-law practical advantage. No numerical result is discarded.

The supplied rotation-law process is not automatically a measured molecular
cross section. Known eta, sampleable mixture components and initial law are
actual inputs. No Haar component can be inferred for free from a finite
rotation data fit. A strongest same-input full-law comparison remains open.

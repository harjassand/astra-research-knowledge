# Independent audit: actual single-copy pair-Pauli fast acquisition

27 October 2026. PASS for the stated ideal-operation sample/representation theorem, local post-cutoff. No collective Keyl primitive or physical J copies are used in this alternative.

## Actual measurement and exact moments
For each pair, the matching probability1/(D-1), setting probability1/3 and coefficient3(D-1)/2 produce precisely half the Pauli expectation times that Pauli. Summing X and Y recovers the complex offdiagonal entry with the correct sign; Z recovers the diagonal. Uniform permutation pairing is a uniform perfect matching. Padding is known and source independent.

I independently calculated both second moments. The two offdiagonal settings together contribute3(D-1)/2 times (rho_ii+rho_jj) divided by the squared filter denominator. The diagonal setting contributes3rho_ii/(4g_i) for Sylvester filtering and3rho_ii/g_i² for full whitening. Each sample square is diagonal in the chosen KNOWN G basis, so these are operator bounds, not an invalid entrywise comparison. With rho<=cG, the Sylvester bound is at most(3c/2)D² and whitening at most3cD²/g_min. Offdiagonal coherences of rho do not alter these second moments.

## Acquired pilot
On a prior-good history with adjacent scale ratio<=2, G=rhohat_prev+uI lies in[3/4,5/4](rho+uI), hence rho<=2G and g_min>=u/2. The displayed abort tests cannot fire on such a history. At initialization G=I has the needed one-sided bounds. Fresh single-copy estimates in that learned eigenbasis have whitening variance<=12D²/u and centered norm<=12D/u. At deviation1/10, the Bernstein denominator is at most25D²/u; n_u=ceil4096D²/u log(2DK/beta_p) gives failure at most beta_p/K. Dewhitening yields relative error<=1/8. The first-failure union is legitimate; no guarantee is imposed after an unobserved failed history. The reciprocal-scale sum<=4/u_* also covers an appended final scale and all ceil costs via the explicit sum.

Applying this pilot to ACTUAL T at u_*=t/4 gives G_A in[7/8,9/8](A+tI). There is no unknown-state whitening operation: basis choice and filtering are functions of the learned classical matrix.

## Fresh contrast
Both T and omega obey rho<=A<=2G_A. Independent one-copy estimates give filtered centered contrast variance<=(16+36)*3D²=156D². The raw and centered norms30D/sqrt(t) and60D/sqrt(t) are conservative consequences of g_min>=t/2. At deviation sqrt(t), the Bernstein denominator312D²+40D is at most352D². The stated512D²/t log(4D/beta) observations therefore pay final failure beta/2. Each observation costs TWO physical calls, measured separately with classical storage between them.

The mean is exactly T_GA(4T-6omega). Reconstructing with sqrt(G_A) and using the already received Douglas/square-root-noise lemma yields ||Z||²<=9t/8 and ||R||<=2sqrt(9/8)t. Compression from the known padded space preserves the physical-space comparison. Thus the independently received exact/overlap deterministic localization bounds transfer, including finite optimization gap; no partial-trace or support promise was added.

## Complete accounting and limits
The explicit total cap is the sum of pilot counts plus2n_c. Pilot and final failure budgets give1-beta on the same source, and declared aborts versus undetected failures remain distinct. Substituting t proportional to nu²p0/r gives O(s²r/(p0nu²)) up to logarithms, with fresh holdout added separately under its independently verified mismatch premise. This extra ambient factor is not suppressed.

All quantum operations are specified known-basis single-copy measurements, using one returned source output plus local known registers, rather than a collective n0-copy POVM. Dense basis rotations can require ambient-quadratic two-level gates; no efficiency in log dimension or uncharged synthesis/bit-precision guarantee follows. Actual T/omega preparation retains the previously received ordinary labelled source access. This is a genuine separate-query alternative, not a proof of novelty, universal tomography improvement, accuracy-optimality, or hidden model verification.

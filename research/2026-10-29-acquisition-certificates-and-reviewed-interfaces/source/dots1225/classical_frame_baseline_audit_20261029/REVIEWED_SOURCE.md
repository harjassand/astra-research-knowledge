# Equally informed classical frame baseline

2026-10-29. Root derivation, receiving review pending. The promised noisy-twirl family has only a9-dimensional real Gram state to learn. Classical frame estimation also avoids reconstructing the complete environment. Any claimed quantum advantage must beat this route, not full process/environment tomography.

The acquired normalized label state is sigma=alpha I-g|c_R><c_R|, alpha=1/(8+eta), g=(1-eta)/(8+eta)>0. Suppose a valid contamination upper bound eta_U<1 gives g_L=(1-eta_U)/(8+eta_U). The upper bound can come from separate source-flag calibration; it is not silently known.

## Explicit trusted measurements and elementary bound
Measure nine diagonal observables |i><i| and36 real off-diagonal observables A_ij=|i><j|+|j><i| on fresh minus records. A_ij has eigenvalues+1,-1,0 and is implemented by the known two-level Hadamard basis on i,j. Divide its sample mean by2 to estimate sigma_ij. No imaginary entries are needed because this promised sigma is real. Each matrix-entry estimator has outcome interval of length1; diagonal outcomes also have length1.

Using m independent records per setting, Hoeffding and union bound give all45 entries error<=e with probability at least1-delta if
 m>=log(90/delta)/(2e²).
The resulting symmetric matrix estimate has operator error E<=9e (each absolute row sum<=9e). Its minimum eigenvector chat can be computed classically in fixed dimension9. If E<g, projecting its eigenvalue equation onto c-perp gives
 sin angle(chat,c)<=E/(g-E),
since the estimated minimum eigenvalue is at most alpha-g+E. For E<=g/2 this is at most2E/g.

Choose its real sign so det(reshape(sqrt3 chat)) is positive, then choose a nearest SO(3) matrix Rhat in Frobenius norm using an ordinary3x3 singular-value decomposition. In the local regime considered below the correct sign is unique: a matrix less than1 in operator norm from a rotation is invertible and has the same determinant sign. The Frobenius error of sqrt3 chat relative to R is at mostsqrt6 sin(angle); nearest-rotation projection at most doubles it. For the corresponding qubit unitaries, the half-diamond distance is ||Rhat-R||_F/(2sqrt2), giving error<=2sqrt3 E/g.

For desired0<epsilon<=1/2, choose e=g_L epsilon/(18sqrt3). Then E<=g epsilon/(2sqrt3), all local sign conditions hold, and half-diamond gate error<=epsilon on the good estimation event. The sufficient record cost is
 45 ceil[486 log(90/delta)/(g_L² epsilon²)].
These are conservative elementary constants, not a claim of optimal sample complexity. A better adaptive eigenvector/parameter estimator can substantially improve them. Measurement/control compilation, classical arithmetic and source waiting are paid. Minus records arrive at probability q=(8+eta)/18 in this IID source, so expected ordinary calls are the record count/q. A fixed cap can be handled by a binomial tail, with abort separately reported.

## Reuse and comparison
The estimated Rhat is a reusable classical control description. Given the same trusted known-control interface as the quantum program processor, it can implement later approximate gates repeatedly without consuming fresh quantum programs. For K uses of the same estimated gate, a direct hybrid bound is K epsilon. Estimating once toepsilon_total/K has sufficient record cost O(K²/(g_L² epsilon_total²) log(1/delta)); no new calibration per use is required. This matters against a processor consuming many new ports per use.

This does not refute the exact finite-query pure-program capability at eta=0: finite classical noisy statistics do not generally specify an arbitrary continuous R exactly. But once the objective is approximate robust gates, classical low-dimensional covariance estimation is a strong conventional competitor. The present noisy quantum construction has not demonstrated practical or asymptotic superiority over it. Its current value is a different, explicitly acquired quantum-program interface, not an exclusive ability to avoid environment tomography.

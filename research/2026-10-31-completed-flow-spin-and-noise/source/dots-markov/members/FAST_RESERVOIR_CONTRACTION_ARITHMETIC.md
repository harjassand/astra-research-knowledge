# Finite explicit dissipative matrices: contraction access without rate-linear work

31 October 2026. Unreviewed binding lemma candidate for `TWO_SECTOR_EXCURSION_COMPILER_CANDIDATE.md`. This is a finite-matrix arithmetic argument, not an implementation or an oracle for a system-sized matrix.

## Statement and paid input

Let Z be an explicitly available m-by-m complex matrix with Z+Z*<=0, let h>=0 be a finite binary time parameter, and let delta in(0,1/10). Matrix entries and an upper bound z>=||Z|| must be computable to arbitrary B-bit absolute accuracy with charged polynomial bit work. Then a contraction B approximating exp(hZ), and a unitary whose designated block approximates B, can be constructed with arithmetic and gate work polynomial in m, input precision, log(2+hz), and log(1/delta). Uniform controlled use for a finite binary time register is obtained by reversible evaluation with all loops padded to the largest allowed bounds. The system Hilbert-space dimension does not enter this dense arithmetic.

The coefficient-acquisition premise is essential. It does not grant access to an exponentially large implicit reservoir, an unknown generator or a free stationary state.

## 1. Certified approximate dissipativity

If Z is obtained numerically with operator error at most xi, replace the approximation by Z_hat-xi I. Its Hermitian part is nonpositive. Its error from Z is at most2xi. Duhamel's formula between the two contraction semigroups gives

    ||exp(hZ)-exp[h(Z_hat-xi I)]|| <=2h xi.

Thus xi<=delta/[100(1+h)] is sufficient. Entry precision delta/[poly(m)(1+h)] entails only logarithmic h dependence. This avoids propagating a small positive real part for a long time. Bounds below can use this exactly dissipative finite-precision matrix, with the acquisition error included.

## 2. Small exponential and repeated squaring

Choose n=2^j>=max(1,hz). Set X=hZ/n, so ||X||<=1 and A=exp(X) is a contraction. A Taylor polynomial of degree k has operator remainder at most e/(k+1)!; k=O(log(n/delta)) is more than sufficient for error delta/[100n(j+1)]. Matrix entries are computed with guard precision sufficient for the same operator-norm arithmetic error. Polynomial matrix multiplication in m is charged.

Starting with this approximation, square j times. If E_l is the error after l squarings, then before rounding

    E_(l+1)<=2 E_l+E_l^2,

because the exact squared factor is a contraction. Allocating each stage rounding error at most delta/[100n(j+1)] gives E_j=O(delta): induction or the bound (1+u)^n-1<=n u exp(nu) controls the quadratic term. Intermediate norms stay at most1+O(delta); no factor exp(hz) occurs. Precision uses O(log n+log(j+1)+log(1/delta)+log m) guard bits beyond coefficient sizes. Binary h causes no time-loop of length h.

If the final matrix F_hat satisfies ||F_hat-exp(hZ)||<=eta, define B=F_hat/(1+eta). Then ||B||<=1 and ||B-exp(hZ)||<=2eta. This known scalar division is an actual contraction repair; it does not rely on the approximate matrix accidentally having norm<=1.

## 3. Constructing the finite-dimensional dilation

For an exact contraction B its Halmos dilation is

    U_B = [[B, sqrt(I-BB*)],
           [sqrt(I-B*B), -B*]].

It is unitary, and the designated block is B. Approximate square roots require no inverse spectral-gap assumption at zero. For S>=0, ||S||<=1, regularize S_eta=S+eta^2 I. Functional calculus gives

    ||sqrt(S_eta)-sqrt(S)||<=eta.

Newton iteration X_(k+1)=(X_k+S_eta X_k^-1)/2 starting from X0=2I stays a positive function of S_eta in exact arithmetic. The eigenvalue interval is [eta^2,1+eta^2]. Its scalar relative errors first decrease by a fixed factor until the iterate is within a fixed relative neighborhood of the square root, then quadratically. O(log(1/eta)+log log(1/eta)) iterations suffice for O(eta) absolute accuracy. The smallest iterated eigenvalue is at least eta, so inverse condition and perturbation bounds are polynomial in1/eta; their logarithms, not their values, determine the required bit precision. There are polynomially many matrix arithmetic operations and inverse computations, with polynomial-bit guard precision. A conservative product-of-local-error bound across the O(log(1/eta)) iterations still uses only polynomial log(1/eta) bits.

This computes an approximate 2m-dimensional matrix U_hat within O(eta) of a unitary U_B. It need not itself be exactly unitary. Apply a finite QR/two-level-rotation synthesis to U_hat, choosing maximal remaining pivots. At each column the norm of the remaining column is close to1 after earlier columns have been removed; a maximal pivot is therefore at least a fixed multiple of1/sqrt(2m), provided the accumulated error is below an inverse polynomial in m. Stable Givens rotations remove the other entries. The orthogonalized unitary is within poly(m)*eta of U_B. Round/synthesize its O(m^2) two-level rotations with a corresponding per-rotation error. These rotations implement an EXACT unitary circuit up to the stated ordinary gate synthesis error; no almost-unitary matrix is silently treated as physical. Reducing eta to delta/poly(m) earns the requested block error. Two-level rotations on an m-dimensional encoded register have their standard polynomial-m control/decomposition costs included.

This argument intentionally accepts dense polynomial dependence on m. It is not optimized in dimension or precision, but does not hide a number of gates proportional to h or1/delta.

## 4. Application to the fast reservoir

For the excursion construction use m=d-1 and

    Z=D_Q+cI/2, h=lambda*t.

Z is dissipative. Evaluate its shifted exponential directly; never multiply a separately represented exp(+lambda*c*t/2) by an underflowed exp(lambda D_Qt). Its duration derivative has norm at most lambda||Z||, so path-time rounding is charged with that constant. The new dependence affects the precision logarithm, not the number of actual source flips simulated.

A stable basis taking psi to the first coordinate can be acquired from its explicitly known positive components. The Householder vector (psi+e0)/||psi+e0|| has denominator at least sqrt2, and a harmless global sign sends psi to e0. Finite stationary-state/basis errors must be included both in initial preparation and in generator acquisition; sufficiently fine absolute error O(delta/[poly(d)(1+lambda*T)]) costs only the corresponding bits. It is not legitimate to discard these errors solely because the exact basis has a dark vector.

Each selected fast interval invokes this finite arithmetic and contraction block encoding, and each inverse is paid. All inner work is uncomputed coherently. The operator-norm error per invocation can be allocated delta/K for K capped intervals, uniformly over system/reference/physical reservoir inputs. Combining this lemma with the source proof still requires the global source, OAA and private-clock error ledger; this local lemma alone is not a general-noise simulation theorem.

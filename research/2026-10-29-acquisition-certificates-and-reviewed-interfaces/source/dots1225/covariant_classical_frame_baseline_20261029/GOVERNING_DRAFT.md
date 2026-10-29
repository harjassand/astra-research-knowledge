# A stronger classical baseline at the same averaged-channel error metric
2026-10-29. Author derivation, independent review required. This is a conventional estimate-and-apply baseline, not a quantum advantage claim.

## Why the comparison matters
The product-program PBT theorem bounds the channel after averaging its internal outcomes. A classical estimator should therefore also be assessed as an averaged physical channel, not only by a stronger high-probability guarantee on every estimated rotation. Covariant randomization cancels first-order angular errors. It yields an inverse-error, rather than inverse-squared-error, acquisition bound even for fixed nonzero contamination in the promised noisy-twirl family.

## Fixed-dimensional estimator
Use independent normalized minus records sigma_R=alpha I-g cc^T, c=vec(R)/sqrt3, g=(1-eta)/(8+eta)>0. A separate valid upper contamination bound gives g>=g_L>0. Measure each of nine diagonal entries and36 real off-diagonal entries on m fresh records. For off-diagonal entries use half the outcome of |i><j|+|j><i|; every estimator has range length1. The real symmetric estimate obeys
 E||sigmahat-sigma||_F² <=81/(4m).
Write E=||sigmahat-sigma||op. On E<=g/4, take a minimum eigenvector, choose its sign so its reshaped3x3 determinant is positive, and project the scaled matrix to nearest SO3. The eigenvector perturbation bound gives sin angle<=E/(g-E)<=4E/(3g). Its scaled-vector Frobenius distance is at mostsqrt6 sin angle; this is below1 on the good event, so determinant sign is correct. Nearest-SO3 projection at most doubles that distance. Hence
 ||Rhat-R||F² <= (128/3) E²/g².
On the complementary event any two rotations have squared Frobenius distance at most8. Markov on E² gives the unconditional bound
 E||Rhat-R||F² <=[(128/3)+128] E[E²]/g² <=3456/(m g²).
A singular/tied estimate uses any deterministic measurable SO3 output; the bad-event bound covers it. This is a loose, explicit expected squared-error guarantee, not an optimal estimator.

## Covariant estimate-and-apply controller
Independently draw known A,B from Haar SO3. Rotate every label record by the known nine-dimensional action mapping vec(R) to vec(A R B^T). Run the fixed estimator above and obtain S. Implement the known qubit gate whose rotation is A^T S B. All randomization, label controls, measurement and classical computations are paid; no unknown source gate is queried or inverted.

Changing variables in A,B proves the averaged Bloch matrix M(R) obeys M(L R H^T)=L M(R) H^T for arbitrary L,H. At R=I the stabilizer L=H implies M(I)=kappa I, hence M(R)=kappa R. Thus the averaged implemented channel is the true unitary followed by a depolarizing channel. The squared rotation error obeys
 E||Rhat-R||F²=6(1-kappa).
For a qubit depolarizing channel, half-diamond error is3(1-kappa)/4. Therefore the implemented averaged gate satisfies
 halfdiamond <=432/(m g²)<=432/(m g_L²).
With N=45m normalized label records, this is19440/(N g_L²). It matches the inverse-error order of noiseless product-resource PBT and is a serious baseline for noisy quantum-program architectures. Constants here are conservative; no claim of numerical optimality is made.

## Finite randomization rather than an ideal Haar oracle
The complete estimator/controlled-gate apparatus is a fixed linear quantum channel from N record registers and a payload to an output, even though its classical postprocessing is nonlinear in measured frequencies. Its conjugated channel coefficients are polynomial of degree at most2N+1 separately in entries of A and B: each record conjugation contributes degree2, and each output corrective rotation contributes degree1. Thus finite exact SO3 polynomial quadrature suffices in the ideal known-rotation model.

One explicit quadrature uses ZYZ Euler angles. Conservatively choose L=4N+4 (larger than the degree bound above), and use2L+1 equally spaced azimuthal angles for each of alpha,gamma, and L+1 Gauss-Legendre nodes for cos beta, with the positive normalized quadrature weights. Products of at most L spin-one matrix entries decompose into integer-spin matrix coefficients of spin<=L. Azimuthal sums remove every nonzero magnetic frequency; the remaining zero-frequency terms are Legendre polynomials of degree<=L, integrated exactly by the chosen nodes. This gives O(L³) nodes per SO3 factor, not an unimplemented continuous random source. Approximate these finitely many algebraic weights by rational probabilities to a prescribed total-variation tolerance, and compile the known rotations to a prescribed operator tolerance. The resulting channel error increases by the explicitly budgeted probability/implementation error. Exact finite Clifford+T synthesis is not assumed. A full native implementation and tight cost optimization are not supplied.

## Boundaries
This theorem concerns ONE averaged gate use with fresh calibration records independent of payload. Reusing one noisy estimate for many coherent gates can create correlated systematic error; the single-use bound must not simply be multiplied as though fresh noise were independent. One can use fresh independent estimates per gate and the hybrid bound, or prove a sharper reusable-control theorem separately. This baseline does not establish a high-probability per-estimate diamond guarantee at inverse-error sample cost, nor exact finite-record learning of an arbitrary continuous frame. It does not invalidate exact pure-program capabilities in rank-deficient models. It does prevent an unjustified separation obtained by comparing different error criteria.


## Executed diagnostics
`check_covariant_estimator.py` executes6000 randomized classical calibrations at eta=.1, using45 settings and m=100,1000,10000 records per setting. Mean squared rotation errors are approximately1.5433,.04213,.003883. The divided-by8 values are scalar proxies for the exact twirled channel error, not an SDP estimate of the finite Monte Carlo channel. The exact trace/MSE identity holds to7.4e-15; finite-sample isotropy residuals are explicitly reported. `check_quadrature.py` tests600 SO3 entry monomials against a higher-order quadrature, maximum discrepancy4.45e-16. Neither numerical diagnostic is the mathematical proof or a native measurement execution.

The Euler/Gauss-Legendre sampling machinery is established: Khalid, Durrani, Kennedy, Wiaux and McEwen, *Gauss-Legendre Sampling on the Rotation Group*, arXiv:1508.03353. No new quadrature or universal estimation method is claimed here; the contribution is an explicitly matched conventional baseline for this channel/program comparison.

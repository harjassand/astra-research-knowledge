# Standard conjugate Gaussian squares cannot rotate away this density noise

## 1. Scope

Fix M>=2 and exactly K>=2 bosons of each flavor. The physical interaction is

`V=t sum_i(n_bi-n_ci)^2`, t>0.

Allow any number-conserving **standard conjugate Gaussian-square decomposition**, including arbitrary Hermitian one-particle channel matrices, either HS sign, exact identities on this fixed sector, arbitrary deterministic one-body corrections, and a scalar correction:

`V = sum_r lambda_r [B(A_r)-C(conjugate A_r)]^2`

`    - sum_s mu_s [B(E_s)+C(conjugate E_s)]^2 + one_body + scalar`,

where lambda_r,mu_s>=0, A_r,E_s are Hermitian, B(A)=b^dagger A b and C(conjugate A)=c^dagger conjugate(A)c. The channels have independent real Gaussian HS fields. A repulsive difference square gives imaginary opposite fields; an attractive sum square gives real equal fields, so every history preserves conjugacy. This is the standard sign-preserving Hermitian-square class of the primary construction.

It is NOT all positive representations: Bogoliubov/pairing channels, arbitrary non-Hermitian jointly correlated drifts, non-Gaussian amplitude decompositions, importance reweighting, and nonlinear/conditional changes of variables are outside the theorem. A real change of coordinates among these same independent Gaussian variables changes neither their joint covariance nor the conclusion. No claim of global sign-problem hardness is made.

**Theorem.** Every channel matrix A_r,E_s in this class is diagonal. On the charge-orthogonal subspace, the imaginary density-phase covariance is exactly tI, while every attractive covariance is a global-number-only mode. After integrating these scalar amplitude nuisances and removing the irrelevant common phase, the random canonical phase weight has exactly the original Gaussian law. Keeping independent scalar amplitude noise can only increase its relative second moment.

Thus neither a different offdiagonal channel basis, a standard Fierz rearrangement within this class, nor a fixed-sector quadratic gauge provides a new overlap mechanism. This is stronger than comparing only one Gaussian factorization, but deliberately weaker than a claim about all AFQMC algorithms.

## 2. Native paired-hop matrix elements force diagonal channels

For i!=j, consider the occupation transition that moves ONE b particle j->i and simultaneously ONE c particle j->i. Its bosonic occupation prefactor is strictly positive on an available K,K basis state. The target V, any one-body correction, and each single-flavor square have zero matrix element on this simultaneous two-flavor transition.

The cross term of a repulsive difference square contributes

`-2 lambda_r |(A_r)_ij|^2`

times that positive occupation prefactor. The cross term of an attractive sum square contributes the SAME sign,

`-2 mu_s |(E_s)_ij|^2`.

Their sum must vanish. Consequently every positively weighted offdiagonal entry is zero. This argument is an actual matrix element in the physical fixed-particle sector; it is not a free tensor-coefficient comparison that might be invalid modulo sector identities. It even works for K=1, although the covariance part below requires K>=2.

The resulting one-body corrections must also be diagonal, apart from the original hopping if it is included unchanged on both sides. They cannot mask a simultaneous paired hop.

## 3. Fixed-sector identities determine the remaining covariances

Write a_r and e_s for the real channel diagonals, and set

`D=sum_r lambda_r a_r a_r^T >=0`,

`E=sum_s mu_s e_s e_s^T >=0`.

On occupation vectors x,y of total K, their quadratic interaction is

`x^T(D-E)x+y^T(D-E)y-2x^T(D+E)y`.

Let P=I-11^T/M. Mixed finite differences in x and y by arbitrary roots e_i-e_j are achievable on this sector and annihilate affine one-body/scalar corrections. They force

`P(D+E-tI)P=0`.

Second finite differences within x, using K e_j,(K-1)e_j+e_i,(K-2)e_j+2e_i, force

`(e_i-e_j)^T(D-E-tI)(e_i-e_j)=0` for all i,j.

For a real symmetric matrix R this is R_ij=(R_ii+R_jj)/2, so R=1v^T+v1^T and PRP=0. Hence

`P(D-E-tI)P=0`.

Subtracting yields PEP=0 and therefore, by E>=0,

`E=e 11^T` for some e>=0, and `PDP=tP`.

Positivity is essential: w^T E w=0 implies Ew=0 on every w orthogonal to1. It also forces each attractive channel vector to be proportional to1. There is no nontrivial attractive spatial density channel hidden by the canonical quotient.

For q=x-y, 1^Tq=0, so q^TDq=t||q||^2. The remaining attractive term is simply -e(1^T(x+y))^2=-4eK^2, a known scalar. All spatial one-body corrections remaining in the equality must themselves be sector constants. In particular the fermionic identity n_i^2=n_i is not available here; bosonic K>=2 sector finite differences have paid the actual identity class.

## 4. The induced law and cost

At a zero-hopping interval of length delta, imaginary phases have covariance2delta D. Their projection Ptheta has the SAME law as the projected original density phases with covariance2delta tI. A common phase multiplies h_K by exp(iK phi) and leaves |h_K|^2 invariant. This remains true if common and projected phase components are correlated: the weight depends only on the projected marginal.

The only real noise is a common scalar xi of variance2delta e. It multiplies the two-flavor canonical trace by exp(2K xi); the physical scalar correction multiplies by exp(-4delta eK^2). Their expectation is one and they are independent of the imaginary phase fields in the specified square-channel class. Integrating them removes them exactly. If retained, the normalized independent positive factor has second moment at least one and cannot lower relative variance.

For zero hopping, dividing the interval into more independent HS slices simply adds the projected Gaussian phases, so the final law is still unchanged. With a prescribed hopping/Trotter schedule the common phases/amplitudes commute with the fixed total numbers, and the same projected field law survives at each slice; no new channel-basis mixing resource appears. This is not a convergence theorem for field MCMC or a different estimator.

The Gaussian direct-sampling lower bound from the root package therefore covers the optimum nuisance-integrated representation in this entire class. The separate PHASE_LAW_BARRIER theorem goes beyond Gaussianity and proves that changing unused local or bounded-block phase moments cannot remove the exponential direct/rejection cost either.

## 5. Ordinary escape routes remain genuine

Canonical field importance/heat-bath/Metropolis samples a different, generally globally correlated distribution proportional to base_density*|h_K|^2. Conditional integration changes the estimator itself. Cluster resummation and non-Gaussian/pairing representations may change both the algebra and dependence. None is excluded here. The exact diagonal occupation baseline in CONDITIONAL_EXECUTION.json is one such successful ordinary conditional operation on the same input, so this theorem identifies a failed representation lever rather than physical difficulty.

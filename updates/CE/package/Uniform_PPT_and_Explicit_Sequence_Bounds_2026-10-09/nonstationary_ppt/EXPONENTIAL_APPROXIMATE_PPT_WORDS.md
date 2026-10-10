# Uniform exponential approximation to EB for arbitrary 2-copositive CP words

9 October 2026. Complete proof candidate. This strengthens the stretched-exponential rate in UNIFORM_APPROXIMATE_PPT_WORDS.md without a dimension-by-dimension error recurrence. It is an approximation theorem, not an exact finite-word EB theorem. This was developed after the preserved focused reviews and is not covered by those reports. No priority or external-certification claim is made.

The later EXPLICIT_EB_NOISE_REPAIR.md supplies an explicit rate and a positive EB remainder, replacing the semialgebraic repair below by elementary depolarizing admixture. GAUSSIAN_PPT_CONCURRENCE_GAP.md provides c_d=1−1/(8d). This earlier complete route is preserved independently.

## Theorem

For each fixed d>=2 there are constants C_d,a_d>0 such that every length-n serial word T of CPTP, 2-copositive maps on M_d has an EB CPTP approximation E with

 ||T-E||_diamond <= C_d exp(-a_d n).                      (1)

In particular this holds for arbitrary PPT CPTP factors, independently varying, nonunital, with no invariant-state or probability assumptions.

Here 2-copositive means id_2 tensor (transpose compose Phi) is positive. Complete positivity plus this condition is precisely what is used: a qubit ancilla always has a PPT output. The theorem does not assert any tensor-power property.

The proof first obtains exponential destruction of qubit concurrence, then a semialgebraic error bound promotes this to exponential distance from genuine 2-entanglement-breaking channels. The published Schmidt-number iteration theorem finishes using only d-1 blocks.

## 1. Homogeneous qubit concurrence

For an unnormalized vector v in C^2 tensor C^d, define

 c(v)=2 sqrt(det[Tr_B |v><v|]).

If v has Schmidt coefficients s_1>=s_2>=0, then c(v)=2s_1 s_2. In particular

 0<=c(v)<=||v||^2,

with equality at the upper end exactly when the qubit marginal is (||v||^2/2)I_2.

For a positive operator rho define the convex roof

 C(rho)=inf { sum_j c(v_j) : rho=sum_j |v_j><v_j| }.

Only finite decompositions are needed. A uniform finite number of terms suffices by convex-hull Caratheodory applied to normalized pure states together with their c values, followed by a scalar rescaling. Thus C is convex and homogeneous, and on density matrices C<=1. No continuity theorem for C will be assumed.

### Exact filter covariance on the qubit

For any 2-by-2 matrix A,

 c((A tensor I)v)=|det A| c(v).

For invertible A, transforming ensembles in both directions gives

 C((A tensor I)rho(A* tensor I))=|det A| C(rho).          (2)

If A is singular, the output has one-dimensional first-party support and is separable, so both sides of (2) are zero. This proves covariance for all A, including the rank-deficient case.

## 2. A PPT state cannot have an entirely maximally entangled range

The Bell-flag structure below is known: Li, Zhao, Fei, Fan, Liu, Mixed maximally entangled states, arXiv:0906.5445v2 (26 February 2012), Theorem 1 and its subsequent remarks; https://arxiv.org/html/0906.5445v2 . Those remarks also discuss convex-roof concurrence. The following short polarization proof is included to make the exact qubit/PPT interface self-contained, not as a claim of a new classification.

Let rho be a nonzero PPT state on C^2 tensor C^d. We claim its range contains a nonzero vector v with

 c(v)<||v||^2.                                          (3)

Suppose instead that every v in S=ran rho satisfies equality. Then

 Tr_B |v><v|=(||v||^2/2)I_2                 for every v in S.

Choose an orthonormal basis v_1,...,v_r of S. Polarizing this matrix-valued quadratic identity yields

 Tr_B |v_j><v_k|=delta_(jk) I_2/2.                      (4)

Write

 v_j=(|0> tensor a_j + |1> tensor b_j)/sqrt(2).

Equation (4) says that all 2r vectors a_1,...,a_r,b_1,...,b_r are orthonormal in C^d. Consequently there is an isometry

 U:C^2 tensor C^r -> C^d

with U(|0> tensor |j>)=a_j and U(|1> tensor |j>)=b_j. If omega_2 is the normalized Bell projector, rho has the form

 rho=(id_2 tensor Ad_U)(omega_2 tensor tau)              (5)

for a nonzero positive matrix tau on C^r.

Partial transposition on the first qubit transforms omega_2 into F_2/2, where F_2 is the swap. Its antisymmetric eigenvalue is -1/2. Since tau has a strictly positive eigenvalue, (F_2/2) tensor tau has a negative eigenvalue. The local output isometry U preserves that nonzero negative eigenvalue. Equation (5) therefore makes rho NPT, a contradiction.

This proves (3). The argument includes mixed rho and arbitrary rank; it does not assume the range contains a product vector.

## 3. A common concurrence deficit on the compact PPT slice

Fix a PPT density matrix rho. Normalize the vector in (3). Because v belongs to ran rho, some p>0 satisfies

 rho-p|v><v|>=0.

Decompose the positive remainder into pure vectors. The resulting finite ensemble has

 sum_j c(v_j) <= p c(v)+(1-p)<1.                        (6)

This strict ensemble bound persists in a neighborhood of rho, without assuming continuity of the convex-roof infimum. Let W be the matrix of its vectorized ensemble columns and pad with zero columns until their number is at least 2d. There is a coisometry U_0 with U_0 U_0*=I_(2d) and

 W=sqrt(rho) U_0.

This follows by extending the polar partial coisometry on the kernel. For a nearby density matrix rho', the columns of

 W'=sqrt(rho') U_0

form an ensemble for rho'. They depend continuously on rho', and c of a vector is continuous. Therefore the ensemble sum remains strictly less than one on a neighborhood of rho.

The trace-one PPT states on C^2 tensor C^d form a compact set. A finite subcover of the preceding neighborhoods gives a constant

 0<c_d<1

such that

 C(rho)<=c_d                for every PPT density matrix rho.       (7)

One may increase c_d within (0,1) if the optimal bound is zero. This proof does not rely on any unverified global continuity or selection property of a convex roof.

## 4. Every 2-copositive channel contracts qubit concurrence

Let Phi:M_d -> M_d be CPTP and 2-copositive. For any normalized pure state psi on C^2 tensor C^d, Schmidt decomposition gives

 |psi>=(A tensor V)|Omega_2>,

where |Omega_2> is the normalized Bell vector, V:C^2->C^d is an isometry, and A is a 2-by-2 matrix satisfying

 |det A|=c(psi).

The density matrix

 rho_(Phi,V)=(id_2 tensor Phi Ad_V)(omega_2)

is PPT by 2-copositivity and has trace one by trace preservation. Quoted factorization is not an extra theorem: moving the qubit filter A past the local map Phi and using the proved covariance (2) gives

 C((id_2 tensor Phi)(|psi><psi|))
   =|det A| C(rho_(Phi,V))
   <=c_d c(psi).                                       (8)

The singular-A case is already included in (2). Taking arbitrarily close-to-optimal finite decompositions of a mixed input rho and using convexity gives

 C((id_2 tensor Phi)(rho))<=c_d C(rho).

Iterating over an arbitrary length-n word T proves

 C((id_2 tensor T)(rho))<=c_d^n                         (9)

for every input density matrix rho on C^2 tensor C^d.

## 5. Concurrence controls distance to separable states

For a normalized pure state psi with Schmidt coefficients s_1>=s_2, choose its normalized top Schmidt product vector u. Then

 || |psi><psi|-|u><u| ||_1=2s_2<=sqrt(2)c(psi),

because s_1>=1/sqrt(2). Apply this term by term to a pure ensemble, and take the infimum over ensembles. For every density matrix rho,

 dist_1(rho,Sep_(2,d))<=sqrt(2) C(rho).                  (10)

All comparison separable states here have trace one. Therefore (9) gives

 sup_rho dist_F((id_2 tensor T)(rho),Sep_(2,d))
   <=sqrt(2)c_d^n,                                     (11)

since the Frobenius norm is bounded by the trace norm.

## 6. Promote output defect to distance from the 2-EB channel set

The ambient compact set is the FULL CPTP slice A_d on M_d, identified with its unnormalized Choi matrices. For Lambda in A_d define

 f_2(Lambda)=max_{rho in D_(2d)}
                 min_{sigma in Sep_(2,d)}
                    ||(id_2 tensor Lambda)(rho)-sigma||_F.

The density-matrix set and separable trace-one set are compact semialgebraic sets. Separability is semialgebraic by a finite pure-product decomposition. Quantifying the extrema therefore makes f_2 semialgebraic. It is continuous, since the inner distance is Lipschitz and the outer maximization is over a fixed compact set.

Let E_(2,d) be the set of 2-entanglement-breaking CPTP maps: those Lambda for which every output in the preceding display is separable. Equivalently E_(2,d)={Lambda in A_d:f_2(Lambda)=0}. This is a nonempty compact semialgebraic set. Define

 g_2(Lambda)=min_{Z in E_(2,d)} ||J(Lambda-Z)||_F.

This is another continuous semialgebraic function on A_d, with the same zero set as f_2. The compact semialgebraic Lojasiewicz inequality yields dimension-dependent A_d'>0 and alpha_d>0 with

 g_2(Lambda)<=A_d' f_2(Lambda)^alpha_d.                  (12)

This is the ONLY use of semialgebraic error bounds in this proof. In particular it is not a claim that a small positive f_2 is already zero.

For Hermiticity-preserving Delta,

 ||Delta||_diamond<=||J(Delta)||_1<=d ||J(Delta)||_F.

For the first inequality, spectrally decompose the Hermitian Choi matrix into signed rank-one terms, represent Delta as the corresponding signed sum of one-Kraus CP maps, and bound each diamond norm by the squared Frobenius norm of its Kraus matrix. The second inequality is the dimension-d^2 trace/Frobenius bound.

Combining (11)–(12), every length-n word has a genuine 2-EB CPTP approximation Z with

 ||T-Z||_diamond<=B_d exp(-b_d n)                       (13)

for some B_d,b_d>0.

## 7. Only d-1 blocks are required

Published input: Christandl–Mueller-Hermes–Wolf, When Do Composed Maps Become Entanglement Breaking?, arXiv:1807.01266v2, Theorem II.1. A product of d-1 independently varying CP 2-entanglement-breaking maps on M_d is EB. Theorem II.1 was inspected directly at https://arxiv.org/html/1807.01266v2 . This result is credited, not reproved or claimed here.

Let r=d-1. Divide an n-word into r consecutive blocks of length m=floor(n/r), with a leftover exterior segment if needed. Replace each length-m block by its 2-EB CPTP approximation from (13). The product of the r replacements is EB by the published theorem, and remains EB after the leftover CPTP segment is composed.

All original blocks and replacements have diamond norm one. Telescoping thus bounds the total error by

 r B_d exp(-b_d m) <= r B_d exp(b_d) exp[-b_d n/(d-1)].

Increasing the prefactor covers n<d-1. This proves (1).

## 8. Effect-preserving non-TP extension

The backwards normalization argument in UNIFORM_APPROXIMATE_PPT_WORDS.md, Section 3, extends (1) to a word T of arbitrary 2-copositive CP maps:

 there is EB CP E with E*(I)=T*(I),
 ||T-E||_diamond<=C_d exp(-a_d n)||T||_diamond.           (14)

The proof only uses CP filtering, positive depolarizing regularization, and closure. These preserve 2-copositivity just as they preserve complete copositivity. No output normalization by an input-dependent success probability is asserted.

## Exact limit

Exponential approximation to a closed EB cone still does not show finite exact membership. This result removes the stretched-exponential dimension loss and the recursive low-rank-error bookkeeping from the unrestricted approximation theorem; it does not close the exact weak-margin branch.


## Attribution and bounded checks

APPROXIMATION_PRIMARY_COMPARISON.md records the targeted comparison with equal-map asymptotics, ergodic bistochastic processes, G-concurrence factorization, and Schmidt-number iteration. The qubit filtering identity is an established concurrence mechanism; the argument above is included to avoid an unspoken dimension or normalization assumption. The candidate contribution is the uniform contraction and semialgebraic approximation synthesis.

verify_qubit_concurrence_interfaces.py checks 6 Bell-flag partial-transpose identities, 30 finite-ensemble qubit-filter identities, and 30 pure-state trace-distance inequalities in dimensions 2,3,4,5,6,8. All pass at the declared floating-point tolerance. It does not compute convex-roof optima, a universal c_d, or a Lojasiewicz exponent. The effect-preserving normalization has additional exact rational checks in verify_determinant_and_effect_bounds.py.

## Bounded local verification

verify_qubit_concurrence_bridge.py and qubit_concurrence_bridge_verification.json check 100 pure-state filter-covariance and nearest-product-distance instances, six mixed Bell-flag partial-transpose spectra, and four explicitly PSD/PPT 2-by-4 matrices with positive ensemble peeling and aligned square-root lifts. All checks passed; the maximum filter-covariance error was about 5.4e-15. These tests do not optimize a convex roof or compute the universal constant c_d.

The separate verify_qubit_concurrence_bridge.py adds 100 pure-filter covariance/product-distance cases, six Bell-flag spectra, and four PPT ensemble peel/lift cases. Its output is qubit_concurrence_bridge_verification.json. The two scripts have distinct names and both are retained.

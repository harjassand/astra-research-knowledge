# ASTRA FRONTIER — Kernel-preserving measurement and transport reconstruction

**Date:** 12 October 2026.  
**Status:** A complete mathematical derivation of a randomized polynomial-time *finite-volume scalar prediction* algorithm is given below, using an established constructive one-dimensional short-time simulation theorem. This is a research result derived in this investigation, not independently reviewed mathematics, a formally verified implementation, or historical-priority clearance. The production locality-based simulator has not been implemented. Executed tests use small full-system calculations, exact rational block identities, and a synthetic trajectory assay, explicitly distinguished below.

## 0. Main result and its boundary

For fixed finite interaction range, bounded local coefficients, nearest-neighbour hopping bounded away from zero, and strictly positive on-site dephasing bounded away from zero, the finite periodic infinite-temperature current response admits a classical randomized additive approximation with total time and memory polynomial in system size, input bit length, inverse accuracy and logarithmic inverse failure probability. Dephasing need not dominate the interactions. The class includes the range-two interacting example t=1, U=4, V=1, d=2.

The algorithm does **not** construct the exponentially large response operator or assume a compact witness. It inserts a computationally useful complete occupation measurement at a positive rate, simulates restartable trajectories, and removes the inserted operation by quantitatively stable analytic interpolation. An exact constrained coherence quotient establishes the size-independent interpolation domain. A separate elementary polynomial inverse bound controls the time-integrated observable at each positive measurement rate.

This computes the full finite-ring response, not a first interaction correction, a detuning-only bound, a one-particle calculation, or transport in the artificially monitored model. It returns a confidence-valid scalar interval. It does not produce the explicitly represented, deterministically checkable rational pair f,g required by the literal previous G1 witness formulation.

The theorem is polynomial **at fixed physical ratios**. Its exponent can be very large when interactions are large compared with dephasing. It is not uniformly polynomial as d tends to zero. The conservative resource budget evaluated here is impractical. There is no demonstrated wall-clock superiority over specialised solvers. High-precision thermodynamic transport still requires a quantitative limit theorem, stated precisely in Section 13.

## 1. Contract and conventions

Take n spins on a cycle, with n at least 3 and larger than a fixed interaction footprint. Small exceptional sizes can be handled by constant-size direct computation. Let

\[
H=-\frac{t}{2}\sum_i(X_iX_{i+1}+Y_iY_{i+1})+H_{\rm diag},
\qquad
\mathcal L O=i[H,O]+\frac d4\sum_i(Z_iOZ_i-O).
\tag{1}
\]

The primary statement uses uniform t>0. H_diag is a sum of real diagonal Hermitian terms of fixed finite range R, with a bounded number and total norm per site. Its coefficients may be inhomogeneous. They, t, and d are supplied as rational numbers with at most b bits each, or as certified intervals used with Section 11. Fixed constants obey

\[
0<t_{\min}\le t\le t_{\max},\qquad
0<d_{\min}\le d\le d_{\max},\qquad
\sup_i\sum_{X\ni i}\|h_X\|\le G.
\]

There is no requirement d_min>G, no many-body gap input, and no target-state preparation input. The initial ensemble defining response is the normalized product trace, not an arbitrary-temperature Gibbs state. Energy is generally not conserved; occupation number is.

Use the complex Hilbert space of operators commuting with total occupation N, with normalized Hilbert–Schmidt inner product

\[
\langle F,G\rangle=2^{-n}\operatorname{Tr}(F^\dagger G).
\]

Define

\[
B=-\mathcal L=S+A,
\quad A=-i[H,\cdot],
\quad S=\frac d4\sum_i(I-Z_i\,\cdot\,Z_i).
\]

A is skew-adjoint and S is self-adjoint positive. Let P be complete dephasing in the occupation basis, Q=I-P. The number-conserving off-diagonal space has at least two occupation differences, hence

\[
S|_Q\succeq dI,\qquad \|S\|\le dn/2.
\tag{2}
\]

The fixed-point space is \(\mathcal F=\{f(N)\}\). Both B and B* annihilate it. Indeed, a B-zero mode has zero dissipative quadratic form, is diagonal, and then commutes with every allowed adjacent swap. It is constant on every occupation-number sector. This proves invertibility on F-perp in finite dimension; no numerical spectral gap is supplied.

For

\[
j_i=\frac t2(X_iY_{i+1}-Y_iX_{i+1}),\qquad
J=\sum_i j_i,
\]

we have J in Q and orthogonal to F, and

\[
a:=\|J\|_2^2/n=t^2/2.
\]

The output is

\[
\kappa_n=\frac1n\langle J,B^{-1}J\rangle,
\qquad D_n=4\kappa_n.
\tag{3}
\]

The inverse is restricted to F-perp. D_n denotes the finite-ring zero-frequency response with the previous susceptibility normalization. It is **not asserted** to be a certified approximation to the infinite-chain second-moment coefficient D at the same n.

## 2. Alternatives investigated and an exact failed interface

### 2.1 Direct coherence elimination does not give a classical process

A tempting operation is to eliminate Q and call the resulting population Schur complement a classical rate matrix. Positivity of its quadratic form is insufficient for nonnegative transition rates.

In the four-site periodic example t=1, U=4, V=1, d=1/2, in the two-particle sector, put

\[
H_{\rm diag}=U\sum_i(n_i-1/2)(n_{i+1}-1/2)
 +V\sum_i(n_i-1/2)(n_{i+2}-1/2).
\]

The periodic sums are used literally; at this small size the next-neighbour pair occurs twice. Let

\[
M_{\rm eff}=-PAQ(QBQ)^{-1}QAP.
\]

Exact rational calculation gives the off-diagonal entry from occupation bitmask 3 to bitmask 12 as

\[
(M_{\rm eff})_{12,3}=\frac{115904}{10076409}>0.
\tag{4}
\]

A negative-generator matrix for a classical Markov process must have nonpositive off-diagonal entries. Thus this elimination would assign a negative rate. The script `schur_check.py` reconstructs H, the superoperator, the elimination and the exact fraction. This rules out that particular sign-free representation, not all classical algorithms for the task. It does not contradict the previous exact exclusion operator, which eliminates with the bare dissipative inverse rather than the full coherent block inverse.

### 2.2 Why other direct routes were not accepted as solutions

The previous degree-preserving exclusion correction remains useful but does not control the degree or size of the coherence witness. A short arithmetic description of a large operator also does not establish cheap contraction or verification.

Breaking a long trajectory into short numerical time steps does not reset accumulated entanglement. A finite-time matrix-product bound must apply to the time since the last genuine state reset, not the integrator step.

Adding an ordinary identity regularizer B+lambda I damps populations as well and encounters a system-size-dependent slow scale. It will be used below only with an explicitly derived polynomial bound, not as the analytic continuation variable.

Hypocoercive separation of the dissipative kernel and Hamiltonian stirring, symmetric/skew variational formulas, Schur complements, and Richardson extrapolation are established methods [R2,R3]. None is claimed as a new primitive in isolation.

## 3. Exact kernel-preserving coherence quotient

Introduce the *artificial* complete occupation-measurement process

\[
\mathcal L_r=\mathcal L+r(P-I),\qquad B_r=B+rQ,\qquad r\ge0.
\tag{5}
\]

Operationally, at Poisson rate r, measure every occupation and retain the sampled configuration. This is a global numerical operation, not a claim that the target material possesses additional local noise. It preserves every population and destroys off-diagonal coherence.

Define the constrained off-diagonal space

\[
\mathcal K=\ker(PA|_Q),
\]

with orthogonal projector Pi, and the compressed operator

\[
C=\Pi(S_Q+QAQ)\Pi|_{\mathcal K},\qquad j=\Pi J.
\tag{6}
\]

These are proof devices, never supplied to or built by the algorithm.

### Theorem 1 — protected analytic response

For real r>=0,

\[
f_n(r):=\frac1n\langle J,(B+rQ)^{-1}J\rangle
=\frac1n\langle j,(C+rI)^{-1}j\rangle.
\tag{7}
\]

The right side extends holomorphically to Re z>-d and obeys

\[
\boxed{|f_n(z)|\le \frac{a}{d+\operatorname{Re}z}.}
\tag{8}
\]

The domain and the bound are independent of n.

**Proof.** Let x=p+q solve B_r x=J, with p=Px, q=Qx. Its population equation is PAq=0, so q belongs to K. The coherence equation is

\[
QAPp+(S_Q+QAQ+rI)q=J.
\]

Because A*=-A, the range of QAP is orthogonal to ker(PAQ). Projection onto K eliminates the population term and gives (C+rI)q=j. Since J is off diagonal, the desired inner product is <j,q>. Also

\[
\operatorname{Re}\langle q,Cq\rangle=\langle q,Sq\rangle\ge d\|q\|^2.
\]

Therefore C+zI is invertible whenever Re z>-d, with inverse norm at most 1/(d+Re z). Finite-dimensional holomorphic inversion and ||j||<=||J|| prove (8). QED.

This is the load-bearing representation change. The artificial measurement acts as a scalar shift **after imposing the undamped population constraint**. Slow population eigenvalues of the full generator do not shrink this scalar response's analytic domain.

## 4. Removing the artificial measurements with a charged error bound

Choose an integer m>=1 and rational nodes

\[
r_j=\frac d8(1+j/m),\quad 0\le j\le m,
\qquad
w_j=\prod_{k\ne j}\frac{-r_k}{r_j-r_k}.
\tag{9}
\]

All monitored systems have r between d/8 and d/4, not a rate tending to zero with n or target precision.

### Theorem 2 — uniformly stable reconstruction

\[
\boxed{
\left|f_n(0)-\sum_{j=0}^m w_jf_n(r_j)\right|
\le \frac{4a}{d}\,2^{-(m+1)}.}
\tag{10}
\]

The exact weight sum obeys

\[
W_m:=\sum_j|w_j|\le(4e)^m.
\tag{11}
\]

If every supplied node value has error at most delta, reconstruction error is enlarged by at most W_m delta. No exact-value oracle is assumed.

**Proof of (10).** Apply the Cauchy remainder formula for polynomial interpolation at x=0 on the circle |z|=3d/4. Theorem 1 bounds |f_n(z)| by 4a/d. In the remainder, the factor 1/|z| cancels the contour radius. Each numerator factor |r_j| is at most d/4, and each denominator |z-r_j| is at least d/2. Their product is at most 2^{-(m+1)}.

For (11), cancel the common d/(8m) in the interpolation weights. Then

\[
|w_j|=\frac{\prod_{k\ne j}(m+k)}{j!(m-j)!}
\le\frac{(2m)^m}{j!(m-j)!}.
\]

Sum and use m!>=(m/e)^m. QED.

For requested error epsilon, one safe choice is

\[
m=\max\{1,\lceil\log_2(16a/(d\epsilon))\rceil\},
\qquad \delta=\epsilon/(4W_m).
\tag{12}
\]

Then m=O(log(1/epsilon)), and delta^{-1} is polynomial in epsilon^{-1} at fixed a/d. Numerator and denominator bit lengths of weights are O(m log m), before their combination with the input d. A final rational rounding margin is reserved.

This is a rigorous use of extrapolation, not a fitted polynomial selected because it matches a few samples. Its validity depends on the complex-domain bound (8). Standard error mitigation already uses added noise and extrapolation [R3]; the relevant distinction here is the kernel-preserving analytic domain and efficient classical access to the monitored nodes.

## 5. A polynomial time-integral cutoff without a supplied many-body gap

The monitored node f_n(r) still integrates all physical times. We derive an explicit polynomial inverse bound to make that integration affordable.

### 5.1 Elementary population coercivity

For a diagonal p orthogonal to F,

\[
\|Ap\|_2^2=\sum_e t^2\,\mathbb E|p(\eta)-p(\eta^e)|^2.
\tag{13}
\]

This follows by writing the hopping matrix elements in the occupation basis. Diagonal interactions commute with p. One can use the known sharp exclusion spectral-gap theorem, but it is unnecessary here. The following coarse self-contained estimate suffices:

\[
\|Ap\|_2\ge\sigma\|p\|_2,
\qquad \sigma=\frac{t_{\min}}{2n^2}.
\tag{14}
\]

**Proof.** Work in a fixed-number sector. Lift p to a function F of a uniform permutation pi of a fixed occupation string. An independent uniform permutation tau can be written by Fisher–Yates as a product of at most n transpositions, independently of pi. Therefore

\[
\operatorname{Var}F=\tfrac12\mathbb E|F(\pi\tau)-F(\pi)|^2
\le \tfrac n2\sum_{s=1}^n\mathbb E|\Delta_s F|^2.
\]

Any transposition of two positions can be implemented by at most 2n adjacent swaps along the open path contained in the cycle; every path edge occurs at most twice. Telescoping and Cauchy–Schwarz give, for each transposition,

\[
\mathbb E|\Delta F|^2\le4n\sum_{e\text{ on path}}\mathbb E|F(\pi e)-F(\pi)|^2.
\]

All intermediate permutations remain uniform after conditioning on tau, so these comparisons use the same uniform law. Hence Var p <=2n^3 sum_e E|p-p^e|^2. Combining with (13) gives ||Ap||^2>=t_min^2||p||^2/(2n^3), which implies the deliberately weaker rational choice (14). Average over number sectors. F-perp is precisely zero conditional mean in each sector. The proof works for complex p as well. QED.

### 5.2 Full inverse bound

Let h_sum be a supplied rational upper bound on sum_X||h_X||, including hopping. Use

\[
a_H=2h_{\rm sum}\ge\|A\|,
\quad s_*=dn/2+d/4,
\]

and define

\[
\boxed{
\mathcal R=\frac2\sigma+rac1d\left(1+\frac{s_*+a_H}{\sigma}\right)^2.
}
\tag{15}
\]

For every r in [0,d/4],

\[
\|(B+rQ)^{-1}|_{\mathcal F^\perp}\|\le\mathcal R.
\tag{16}
\]

In particular Rcal=O(n^6) at fixed physical bounds. This is conservative, not optimal.

**Proof.** Write y=B_r x and x=p+q. The coherence equation and (14) imply

\[
\sigma\|p\|\le\|y\|+(s_*+a_H)\|q\|.
\]

Dissipation gives d||q||^2<=Re<x,y><=||x||||y||. Put X=||x||/||y||, c0=1/sigma and c1=1+(s_*+a_H)/sigma. Then

\[
X\le c_0+c_1\sqrt{X/d}\le c_0+X/2+c_1^2/(2d),
\]

proving (16). This reconstructs the needed inverse estimate rather than importing an uncharged gap. QED.

For lambda>=0, accretivity gives

\[
\|(B_r+\lambda I)x\|^2
=\|B_rx\|^2+2\lambda\operatorname{Re}\langle B_rx,x\rangle+\lambda^2\|x\|^2
\ge\|B_rx\|^2.
\]

Thus the same inverse bound holds on F-perp after adding lambda I. Resolvent subtraction now yields

\[
\left|f_n(r)-\frac1n\langle J,(B_r+\lambda I)^{-1}J\rangle\right|
\le a\lambda\mathcal R^2.
\tag{17}
\]

Choose lambda=min{1,delta/(8a Rcal^2)}. This costs only a polynomial inverse time. No decay rate for the full semigroup is needed.

## 6. A bounded monitored-trajectory estimator

Let T be an independent exponential stopping time of rate lambda. Write

\[
C_{n,r}(u)=n^{-1}\langle J,e^{u\mathcal L_r}J\rangle.
\]

Then

\[
f_{n,\lambda}(r)=\lambda^{-1}\mathbb E C_{n,r}(T).
\tag{18}
\]

This identity follows from the Laplace resolvent of a finite contractive semigroup. Conserved modes cause no difficulty for J.

Choose input bond i and output bond j uniformly, and sign s in {-1,+1} uniformly. Sample the efficiently preparable mixed state

\[
\rho_{i,s}=2^{-n}(I+s j_i/t).
\tag{19}
\]

Its other spins are independent uniform occupation bits. On the pair, use |00> with probability 1/4, |11> with probability 1/4, and the current eigenstate of eigenvalue st with probability 1/2. Only the initial pair is entangled.

Evolve a trajectory of L_r until T and sample Y=j_j/t, whose eigenvalues are -1,0,+1. Then

\[
\boxed{Z=\frac{nt^2}{\lambda}sY,\qquad
\mathbb E Z=f_{n,\lambda}(r),\qquad |Z|\le B_0:=nt^2/\lambda.}
\tag{20}
\]

**Verification.** Averaging s times the output expectation in (19) yields <j_i,e^{T L_r}j_j>/t^2. Averaging both bond indices and multiplying by nt^2 gives C_{n,r}(T); then average T. This estimates the full tracial response across all particle-number sectors, not a dilute-particle surrogate.

One can fix the input bond in a translation-invariant instance. This was done in the diagnostic only; the general estimator samples it. No physical specimen or quantum device is required by the classical algorithm: the preparations and measurements are sampled numerically.

## 7. Constructive classical access to monitored trajectories

### 7.1 Unravelling and actual restarts

The original local dephasing is exactly unravelled by independent unitary Z_i kicks at rate d/4. Between kicks, evolve under H. At each independent global measurement event of rate r, sample the full occupation string and replace the pure trajectory state by that product basis state.

In a frame incorporating the Z kicks, each coherent interval is generated by a piecewise-constant finite-range Hamiltonian with unchanged local norm bounds. A kick changes signs of some hopping terms but does not increase their range or norm. The number of changes is explicitly charged. At the end of an interval the known product of Z kicks is restored; it has no effect on occupation probabilities but can change the sign of the final current readout. It adds only single-site operations.

The entanglement that must be retained is only that created **since the last complete occupation measurement**. Classical occupation correlations across successive intervals remain in the sampled n-bit configurations; they are not discarded from the ensemble.

### 7.2 All rare-trajectory and stopping errors are charged

Take

\[
p=\min\{1/16,\delta/(64\max\{1,B_0\})\},\qquad
T_{\max}=\lambda^{-1}\log(1/p).
\]

If T>T_max, return zero. This introduces expectation bias at most B0 p, not merely an unquantified tail event.

The total kick/measurement rate is nu=nd/4+r. A Poisson tail bound supplies an explicit integer K=O(nu T_max+log(1/p)) such that more than K events before T_max has probability at most p. For example, upward rounding of

\[
K=4\nu T_{\max}+2\log(1/p)+2
\]

is sufficient by the exponential moment bound, using e-1<2. Abort such trajectories before expensive work.

There are at most K+1 coherent intervals in a nonaborted trajectory. Set

\[
\tau_{\max}=r^{-1}\log((K+1)/p).
\tag{21}
\]

A union bound over the first K+1 exponential global-measurement waiting times shows that a coherent interval longer than tau_max has probability at most p after the other caps. Abort it and return zero. The three truncations change the mean by at most 3B0 p. This remains valid for the final partial interval. No accepted-trajectory renormalization is performed.

Since r>=d/8 and d is bounded below,

\[
\tau_{\max}=O_{\rm physical}\big(\log n+\log\delta^{-1}\big).
\tag{22}
\]

The full stopping time can be polynomially long, while every retained coherent interval is only logarithmically long.

### 7.3 The matrix-product representation is derived, not assumed

A constructive one-dimensional locality theorem gives an operator-norm-eta approximation to bounded finite-range evolution over time tau as a constant-depth product of block unitaries with block length

\[
\ell=O_R\big(G\tau+\log(n/\eta)\big).
\tag{23}
\]

It permits time-dependent local interactions and is the established short-time simulation result of Osborne [R1]. Periodic boundaries can be handled with a constant number of overlapping partitions; a cut-crossing block only changes the constant number of layers. If the prescribed block covers the whole ring, n<=ell and direct computation is still within the same bound.

The following explains its constructive use here. Cut the chain into intervals, evolve the disconnected intervals, and correct each cut with a boundary unitary. In the interaction picture, the correction generator is the crossing interaction evolved by the disconnected dynamics. A finite-range Lieb–Robinson bound localizes that generator to distance O(G tau+log(n/eta)). Duhamel bounds the unitary error by its integrated generator error. Disjoint boundary neighbourhoods form a constant-depth block circuit. The argument depends on local norms and integrated time, not on smoothness across the finitely many Z-kick times.

After application to a product state, that circuit has matrix-product bond dimension exp(O(ell)). Sampling the occupation string or a local current outcome can be done by successive Born sampling and polynomial-time tensor contraction. The bound is polynomial here because (22) makes ell logarithmic in n and inverse required precision.

One must not compose a polynomial number of short-time approximate circuits **without** resetting their matrix-product state. The global measurement and product restart after each interval are essential.

### 7.4 Finite bits and rare measurement branches

Allocate total output-law error at most p across the at most K+1 coherent intervals, using operator errors eta=O(p/(K+1)) and an additional budget for timing and random-number arithmetic. Channel/state trace-distance telescoping gives this bound uniformly in the starting configuration. For a bounded payoff, total-variation error p changes the mean by at most 2B0 p.

There is no division by a minimum Born probability in this argument. One may use exactly unitary rational approximants to block evolutions: the Cayley step of a rational Hermitian generator is unitary with rational complex entries, converges at a controlled rate, and is computable by finite-dimensional rational elimination. Piecewise integration and boundary corrections occur on ell=O(log(poly(n,delta^{-1}))) spins. The number of time cells needed for inverse-polynomial error is polynomial. Products of their common denominators have polynomial bit length. A constant-depth circuit of such blocks can be contracted and sampled with polynomial-bit rational arithmetic; the fixed initial pair only adds a constant-degree algebraic number. Very small or zero branch probabilities do not require exponentially many digits beyond this bound.

Alternatively, stable finite-precision matrix-product sampling can be used with explicit absolute probability-error control. A fitted or unchecked numerical singular-value cutoff is not part of the theorem.

Exponential stopping times and Poisson schedules can also be generated to the needed finite precision. Truncate tails first; sample the bounded Poisson count to controlled variation error and conditional ordered uniform times to sufficient mesh precision. Couple rounded times to ideal times. The Hamiltonian evolution is Lipschitz in the resulting total interval-duration error with constant bounded by the known global norm, while kick and measurement counts are already polynomially capped. Required timing precision is inverse polynomial, and its bit length polynomial. This is a state/output-law error statement, not the false claim that a discrete time distribution is close in total variation to a continuous one.

These constructions account for memory, contraction, precision and output costs. They are a proof of an algorithm, not a claim that the supplied small-system diagnostic implements this full compiler.

## 8. Main computational theorem

### Theorem 3 — additive finite-volume transport approximation

Fix the physical bounds in Section 1. There is a classical randomized algorithm which, for every admissible n-site rational model, epsilon>0 and alpha in (0,1), outputs a rational estimate kappa_hat and interval

\[
[\widehat\kappa_n-\epsilon,\widehat\kappa_n+\epsilon]
\]

containing kappa_n with probability at least 1-alpha. Its total bit operations, memory, required random bits after tail truncation, and output verification of the analytic/statistical budget are bounded by

\[
\boxed{\operatorname{poly}_{R,G,t_{\min},t_{\max},d_{\min},d_{\max}}
(n,b,\epsilon^{-1},\log(1/\alpha)).}
\tag{24}
\]

For D_n=4kappa_n, request epsilon/4 internally. The theorem is an additive guarantee, not a relative guarantee for arbitrarily vanishing outputs.

**Algorithm and proof.**

1. Read the local model, compute h_sum, a, sigma, Rcal, and interpolation parameters m, w_j, W_m, delta from (12).
2. At every r_j, choose lambda and the capped monitored trajectory sampler from Sections 5–7.
3. Use at least

\[
N_{\rm samp}=\left\lceil128B_0^2\delta^{-2}
\log\frac{2(m+1)}\alpha\right\rceil
\tag{25}
\]

independent trajectories. Hoeffding bounds the sample-mean deviation from the implemented sampler's expectation by delta/8 simultaneously over nodes with probability at least 1-alpha.
4. The lambda bias is at most delta/8. The three abort rules contribute at most 3B0p, and numerical sampling law error contributes at most 2B0p. These totals are strictly below delta, leaving spare budget for rational output rounding. Thus every reconstructed node is delta-accurate on the confidence event.
5. Return sum_j w_j times the node estimates, with the analytic remainder, sampling allowances and final rounding budget. Equations (10)–(12) bound the total by epsilon.

Polynomiality is explicit: Rcal is polynomial in n; m is logarithmic in inverse accuracy; W_m and delta^{-1} are polynomial in epsilon^{-1}; lambda^{-1}, B0, N_samp, T_max and K are polynomial in n,delta^{-1},log(1/alpha). Each retained coherent interval has logarithmic length. Its block circuit and matrix-product sampling therefore have polynomial size, time and bit precision. The number of intervals is at most K+1. No operation invokes a global wavefunction or inverse operator of dimension 2^n, except when n itself is within the logarithmic block bound. QED.

The result is a probabilistic numerical certificate for the scalar, not a deterministic certificate of each random sample and not the previous rational witness pair. A prover's unsupported claim that sampling occurred is not verifiable from the final scalar alone; reproducible computation or independent reruns are required, just as for other randomized approximation algorithms.

## 9. What physical design knowledge becomes obtainable

The algorithm includes all interacting coherence corrections to the finite response. Increasing m and node accuracy targets the specified total error, not just an additional local commutator order. It can compare K supplied candidate finite models to tolerance epsilon with O(K) algorithm calls, using failure probability alpha/K per candidate. Selecting the largest estimated D_n gives additive regret at most twice the individual D_n tolerance. This is not a global optimizer over an unrestricted continuous many-parameter design landscape.

The algorithm does not simulate the unmonitored full trajectory for polynomially long times. It computes one time-integrated scalar through a family of differently monitored ensembles and a protected analytic continuation. It is therefore not an efficient general simulator for all output distributions of the original quantum dynamics.

All particle-number sectors contributing to the tracial ensemble are included. Finite-range diagonal interactions are neither dropped nor treated perturbatively. The physical d is retained; only the additional artificial rate r is removed. Sending physical d to zero invalidates the fixed-parameter polynomial claim.

## 10. Executed diagnostics and their actual evidential scope

### 10.1 Exact algebra

A seven-dimensional real S+A model with a two-dimensional undamped population space was tested with exact rational/symbolic arithmetic. Full and compressed response formulas agreed at five real/complex rates. Interpolation identities and the analytic bias bound were verified exactly at orders 1,2,3,4,6. Twelve physical spin-sector comparisons at sizes n=4,5,6 also checked full versus compressed resolvents and complex-domain norm bounds, using floating arithmetic.

The classical-rate counterexample (4) is exact rational arithmetic. It is separately reproducible and does not depend on an observed floating sign.

### 10.2 Nonperturbative interacting finite-ring reconstruction

For t=1,U=4,V=1,d=2, positive-node responses were computed by floating sparse linear algebra solely for a diagnostic of the reconstruction formula. The production theorem replaces those full-system solves by Section 7's monitored sampler.

| n | Direct floating D_n | Order-8 reconstruction | Absolute observed difference |
|---:|---:|---:|---:|
| 5 | 0.7310756972111554 | 0.7310756679221413 | 2.93e-8 |
| 6 | 0.6169717258562177 | 0.6169717115171807 | 1.43e-8 |
| 7 | 0.6107192864887748 | 0.6107192783410937 | 8.15e-9 |

These are floating diagnostics, not interval-certified digits. The uniform proven interpolation bias bound for D_n at order 8 is much wider, 0.0078125. The weight sum at order 8 is 2,228,225; cancellation and node precision are real costs. No empirical error estimate replaces the theorem's worst-case bound.

### 10.3 Synthetic monitored-trajectory test

A four-spin full-state simulation used r=0.3, lambda=1 and 16,000 independent synthetic trajectories. The exact regularized response was about 0.131164; the sample mean was 0.170000, standard error about 0.02223 and valid Hoeffding 99% radius about 0.10294. There were 4,866 global measurements. The fixture tests the preparation/sign/measurement normalization and the stochastic unraveling, not high-precision performance. The nonzero discrepancy is retained, not presented as exact agreement.

### 10.4 A resource calculation that prevents overclaiming

With n=8, requested kappa accuracy 0.01, t=1,U=4,V=1,d=2 and the self-contained conservative inverse bound, the proof budget gives:

- m=9 and W_m=16,807,935;
- node tolerance about 1.49e-10;
- Rcal about 1.62e7;
- lambda about 1.41e-25;
- more than 10^74 samples **per node** under (25).

These are sufficient proof budgets, not lower bounds or predictions for an optimized implementation. They demonstrate that a polynomial theorem is not a practical technological advantage. No such sample count was executed. Sharper inverse estimates, better extrapolation nodes, variance reduction or deterministic monitored solvers may help, but are not silently credited with an unproved improvement.

## 11. Inputs, calibration, robustness and physical cost

The main algorithm is classical and **model-supplied**. Its required information is the O(n) fixed-range local coefficients, hopping, and actual physical dephasing model. The earlier single statistic Xi does not provide this entire input. The extra information requirement is explicit; it is not an equilibrium distribution or an inaccessible many-body spectrum.

No Gibbs-state preparation, quantum coherence time, device energy or experimental sample cost is hidden in the classical calculation. On hardware, the global measurement process would be an additional nonlocal control; the theorem does not require implementing it physically. Numerical sampling of that process is charged instead.

For calibrated parameters within the same number-conserving, local dephasing model class, a finite-volume transfer bound follows from resolvent subtraction. Let both inverse norms be at most a common Rcal and put a_max=max(||J||^2,||J'||^2)/n. Then

\[
|\kappa_n(B,J)-\kappa_n(B',J')|
\le a_{\max}\mathcal R^2\|B-B'\|
+\frac{\mathcal R}{n}(\|J\|+\|J'\|)\|J-J'\|.
\tag{26}
\]

For uniform hopping, the second term is at most Rcal (|t|+|t'|)|t-t'|/2. Also

\[
\|B-B'\|\le2\|H-H'\|+\frac n2|d-d'|,
\quad \|H-H'\|\le\sum_X\|h_X-h'_X\|.
\]

Thus inverse-polynomial coefficient accuracy is sufficient in this restricted class, although the conservative required accuracy can be severe. Acquisition of such intervals is a separate experimental task with state preparation, calibration, timing and measurement costs. It is not supplied free by the previous Ramsey detuning experiment. Local support and adequate controls may permit local parameter learning, but no new universal calibration algorithm is proved here.

Unknown long-range terms, memory, additional dissipation, leakage, coherent control errors outside the structural model, or arbitrary distant defects are not certified by (26). The physical model must be justified and tested. Translation invariance is not required for the finite model algorithm, but is required by the previous particular infinite-chain statement.

## 12. Prior art, matched comparison and research capital

### 12.1 What is established prior work

[R1] T. J. Osborne, *The Dynamics of 1D Quantum Spin Systems Can Be Approximated Efficiently*, quant-ph/0508031v2 (16 August 2006), published as *Efficient Approximation of the Dynamics of One-Dimensional Quantum Spin Systems*, PRL 97, 157202 (2006). The actual proof supplies the constructive logarithmic-time one-dimensional propagator representation used in Section 7, including time-dependent interactions. The matrix-product representation and locality theorem are imported established tools, not inventions here. https://arxiv.org/html/quant-ph/0508031v2

[R2] D. Fang, J. Lu, Y. Tong, *Mixing Time of Open Quantum Systems via Hypocoercivity*, arXiv:2404.11503v2; PRL 134, 140405 (2025). Separation of dissipative kernels, Hamiltonian stirring and coercivity is established. Section 5 instead gives the elementary inverse bound actually used, with all constants charged. https://arxiv.org/html/2404.11503v2

[R3] K. Temme, S. Bravyi, J. M. Gambetta, *Error mitigation for short-depth quantum circuits*, arXiv:1612.02058; PRL 119, 180509 (2017). Added-noise extrapolation and its statistical overhead are prior concepts. The present continuation is not generic successful zero-noise extrapolation; it uses a proved, volume-independent half-plane for a constrained transport functional, leaving physical dephasing in place. https://arxiv.org/abs/1612.02058

[R4] C. von Keyserlingk, F. Pollmann, T. Rakovszky, *Operator backflow and the classical simulation of quantum transport*, arXiv:2111.09904; PRB 105, 245101 (2022). This is a close transport-specific comparator. Its operator-backflow approach conjectures exponential suppression with a support cutoff and reports a quasipolynomial-in-inverse-accuracy memory scaling under that mechanism, with tests on random circuits and ergodic spin chains. The new derivation does not assume sparse-operator closure, but its worst-case constants are substantially less practical than small-system experiments suggest. https://arxiv.org/abs/2111.09904

[R5] A. Angrisani, R. Puig, Y. Teng, Z. Holmes, *Dissipation accelerates quantum and classical simulation of open-system dynamics*, arXiv:2609.40174v1 (30 September 2026). Its classical Pauli-propagation result is already polynomial at fixed noise, and covers infinite-temperature correlation estimates. Its Section II.1 explicitly requires damping of every local nonidentity Pauli mode and explicitly excludes single-axis dephasing. Thus it does not directly provide the pure-dephasing finite-transport guarantee derived here. It is not legitimate to describe all existing noisy simulation as merely exponential. https://arxiv.org/html/2609.40174v1

[R6] Z.-L. Zhou, J. Noronha, *Diffusivity in Dissipative Quantum Transport from an Exactly Solvable Krylov Chain*, arXiv:2609.16559v1 (15 September 2026). The actual model uses symmetric **incoherent nearest-neighbour exchange**, not pure on-site dephasing. It exactly calculates a leading density-dependent correction in a strong-dissipation expansion. That is a different noise model and different precision target. The earlier generic label 'noisy XXZ' should not obscure this distinction. https://arxiv.org/html/2609.16559v1

### 12.2 What advantage has and has not been established

Under matched known local inputs and finite-ring scalar outputs, the derivation gives a worst-case randomized polynomial resource guarantee for the stated pure-dephasing interacting class. It does not show that its constants beat tensor-network, backflow, Krylov or direct numerical methods on feasible instances. Its qualitative guarantee is not supplied by the precise versions of [R4]–[R6] inspected; this is a scoped literature comparison, not an exhaustive priority claim or a lower bound against competing algorithms.

No general quantum-computation or ground-state hardness result is bypassed. The theorem is restricted to one dimension, fixed positive physical dephasing, bounded-range specified interactions, finite-volume tracial current response, and additive accuracy. Inverse accuracy may itself be exponential if the requested error is exponentially small. Exponentially weak hopping or vanishing dephasing are excluded from the fixed-bound theorem, not treated as unit-cost inputs.

### 12.3 Repository provenance

Astra was read at revision **ac6ce52c80d55173ca38f9cb99cd3ba7f50fb132**. N747 preserves the previous balanced-transport source as source-derived and unreviewed. The attached complete 705-line note was read, including its exact G1 and finite-size limitations. No new result is assumed merely because a repository card calls it complete.

At openai/math revision **fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb**, the actual source `preprints/Radial-transfer-estimates-and-polygon-length-laws-for-honeycomb-walks-September-26-2026/build/sections/pressures.tex`, lines 1–180, was inspected. Its analytic transfer branches and weighted-convolution accretivity have model-specific prerequisites and a different task. None of its theorem claims is imported. The present quotient and contour estimates are proved directly above. No Lean build or formal verification was run.

Neither repository was modified. Literature and repository searches do not establish historical novelty or independent correctness of this combined algorithm.

## 13. The precise remaining scientific theorem

### T1 — quantitative thermodynamic transfer

For the translation-invariant subclass at the fixed nonperturbative physical bounds, prove an explicit, computably uniform rate such as

\[
|D_n-D|\le C n^{-p},\qquad C<\infty,\ p>0,
\tag{27}
\]

with constants acquired from the specified local model class, or prove an alternative quantitative regularized/infinite-volume procedure with polynomial total cost in inverse target error.

This is **not** implied by the finite-volume algorithm, the previous existence of D, or a few observed finite-ring values. The previous proof deliberately takes infinite volume at positive Laplace parameter before removing that parameter. Equation (27) must justify the finite-volume DC order of limits or replace it. A nonconstructive convergence statement is insufficient for a polynomial-accuracy claim.

If (27) holds uniformly with constructive constants, select n polynomial in epsilon^{-1}, apply Theorem 3 at error epsilon/2, and obtain a full polynomial-cost high-precision macroscopic scalar prediction. This is the precise next capability, not another detuning certificate.

### T2 — practically useful resource bounds

Replace the conservative polynomial exponents and sample counts by bounds or algorithms usable on physically relevant sizes and errors, with matched comparisons to specialised numerical methods and a complete calibration budget. The present sufficient count above 10^74 for a small example does not constitute practical advantage.

### Separate obligations retained

Gaussian hydrodynamics, general finite-temperature transport, closed-system limits and arbitrary inverse design remain separate. The original deterministic rational witness-output version of G1 also remains open; the scalar prediction task has instead been addressed by a different algorithmic output and probabilistic certificate.

## 14. Evidence ledger

| Claim | Evidence/status |
|---|---|
| Exact constrained coherence quotient and analytic half-plane | Full finite-dimensional proof in Section 3; exact block and floating physical checks |
| Uniform interpolation and charged statistical amplification | Contour proof and exact rational weights |
| Polynomial finite-volume inverse bound | Self-contained permutation-path proof and accretivity estimate |
| Restartable positive-rate sampler | Exact unraveling; derived logarithmic intervals; established constructive 1D simulation input |
| Randomized polynomial additive finite response | Complete combined algorithm/error/cost derivation in Section 8; not independently audited |
| Implemented production polynomial simulator | Not implemented; only small full-state diagnostics executed |
| Exact failure of a Markov Schur interpretation | Rational four-site counterexample executed |
| High-precision numerical extrapolation | Small floating tests; observed digits are not certified enclosures |
| Thermodynamic high precision | Open T1 |
| Practical or experimental superiority | Not established; conservative budget impractical |
| Historical novelty / independent proof validation | Not established |
| Repository publication | Not performed |

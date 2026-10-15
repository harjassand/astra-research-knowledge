# Independent audit of arbitrary-dependent Pauli MH noise costs

Date: 2026-10-15. This packet appends a new audit without changing the completed independent-noise packet. Scope: internal analytic and exact-rational certificate audit; no external mathematical review or formal verification. The exact dependent optimum remains unresolved.

**Verdict for the frozen inputs: no fatal mathematical gap found.** Quotient disintegration, arbitrary centering, optimizer attainment, the older radial lower bound, its strictness argument, finite-support SOC duals on the full infinite lattice, free-mean quadratic interpolation, and the explicit infinite geometric-tail upper laws all survive the audit.

The frozen certificates support the substantially tighter interval

\[
\boxed{\frac{19854624776291}{6250745000000}
\le v_*
\le\frac{3911259954946061065911894562429}
{1231364609261368746876606814187}.}
\]

Numerically these endpoints are 3.1763613419346015 and 3.1763621639996797. In outward-rounded readable form,

\[
\boxed{3.1763613\le v_*\le3.1763622.}
\]

The readable interval has width 9×10⁻⁷. This is an enclosure, not an exact optimizer or equality theorem. The upper certificate is `certified_upper_N10_mixture.json`; its final rational table, not its numerical discovery history or mixture name, defines the audited law. `DEPENDENT_SNAPSHOT_MANIFEST.json` freezes every byte used. `verify_dependent_snapshots.py` independently checks the rational certificates using only the standard library; it does not import an author verifier or optimizer.

## 1. Contract, units and cone

In unit scales A=σz and B=σx. A Borel probability law ν on ℝ² with finite covariance is admissible when the finite operator measure

\[
T*\nu,\qquad
T=\frac14\sum_{\epsilon,\tau=\pm1}
(I+\epsilon\sigma_z+\tau\sigma_x)\delta_{(\epsilon,\tau)},
\]

is positive. Fourier uniqueness makes this equivalent to the all-real-frequency scalar-multiplier contract; it does not require a density, exponential moments or analytic continuation. Translation of ν translates the output and preserves positivity and covariance. Thus

\[
v_*:=\inf\operatorname{tr}\operatorname{Cov}\nu
\]

can be studied with centered laws.

For ν supported on u+2ℤ², let qᵢⱼ≥0 be its masses. At output u+(2i+1,2j+1), write p=qᵢⱼ, q=qᵢ₊₁,ⱼ, r=qᵢ,ⱼ₊₁ and s=qᵢ₊₁,ⱼ₊₁. The effect is

\[
\frac14(SI+X\sigma_z+Y\sigma_x),\quad
S=p+q+r+s,\ X=p+r-q-s,\ Y=p+q-r-s.
\]

Its eigenvalues are (S±√(X²+Y²))/4. Hence the exact local condition is the second-order cone

\[
S\ge\sqrt{X^2+Y^2}. \tag{D1}
\]

The normalization of the noise is ∑qᵢⱼ=1. Finite-angle LP conditions alone do not establish (D1). By contrast a rational direction (α,β) with α²+β²≤1 always supplies the valid necessary inequality αX+βY−S≤0, which is enough for a certified lower dual.

For A=aσz and B=bσx, a,b>0, scale by D=diag(a,b). All displayed bounds concern the **normalized trace** tr(D⁻¹CovνD⁻¹). They are not automatically bounds for every physical weighted trace. The symmetric upper law scales to covariance (U/2)diag(a²,b²). Its physical trace is U(a²+b²)/2; comparison with the independent physical optimum 4ab depends on a/b. The unit or normalized cost improvement is rigorous.

## 2. Arbitrary continuous and singular laws reduce exactly

Choose the standard Borel quotient representative u∈[0,2)². Let π be the law of N modulo 2ℤ². Disintegration provides conditional probability arrays qᵢⱼ(u), with

\[
\nu(E)=\int\sum_{i,j}q_{ij}(u)1_E(u+2(i,j))\,\pi(du).
\]

All four corner translations in T induce the same quotient translation u↦u+(1,1) modulo 2. That quotient map is a bijection. Consequently there is no cancellation or mixing of distinct noise cosets in the positivity condition: the conditional output atoms are exactly the matrices in (D1), integrated against the same quotient measure after this bijection.

Necessity can be made explicit using matrix-valued Radon–Nikodym derivatives. On each countable cell and each measurable quotient subset, positivity of the output measure forces the conditional matrix to be positive almost everywhere. A countable dense set of vectors in ℂ² and countably many cells give one common null set. Conversely positive conditional matrices integrate to a positive measure. Thus (D1) holds for π-almost every conditional array if and only if ν is admissible.

Finite global second moments imply finite conditional second moments almost everywhere by Tonelli. Therefore all subsequent conditional centering and covariance formulas are legitimate. This argument includes absolutely continuous, singular continuous, atomic and mixed laws. It does not assume that the global law was supported on a preferred coset.

## 3. Free means are covered, not fixed at an integer site

For a law on u+2ℤ², the covariance equals that of 2K, where K has probability array q. Its relevant centering vector is c=E(2K), which need not be an integer vector or equal to the coset representative. Integer index translations change c by 2ℤ². Separate reflections of the index axes preserve (D1), changing the signs of X and Y as appropriate. They also reflect c. Thus the centered cost can always be represented with

\[
c\in[0,1]^2.
\]

This is an invariance reduction for a potentially asymmetric array, not an assumption of reflection symmetry of the optimizer. Coordinate interchange also preserves the cone and quadratic trace, so a certificate at (c₁,c₂) supplies one at (c₂,c₁).

For a general ν, the law of total covariance gives

\[
\operatorname{tr}\operatorname{Cov}\nu
=\int\operatorname{tr}\operatorname{Cov}(\nu_u)\,\pi(du)
+\int|E\nu_u-E\nu|^2\,\pi(du).
\]

The second term is nonnegative. A bound valid for all finite-covariance arrays and all c∈[0,1]² therefore gives the same bound for every Borel law. No centering of individual fibers can erase an uncharged negative cost.

## 4. Exact duals cover the entire infinite lattice

Fix a rational center c and a finite collection of rational multipliers λₖ≥0 on cell-direction pairs. Each direction has αₖ²+βₖ²=1. For an admissible array,

\[
h_k(q):=\alpha_k X_k+\beta_k Y_k-S_k\le0.
\]

Let dᵢⱼ=|2(i,j)−c|², and let aᵢⱼ be the coefficient of qᵢⱼ in

\[
\sum_{i,j}d_{ij}q_{ij}+\sum_k\lambda_k h_k(q).
\]

If aᵢⱼ≥L for every integer node, normalization yields

\[
\sum d_{ij}q_{ij}
\ge\sum d_{ij}q_{ij}+\sum_k\lambda_k h_k(q)
=\sum a_{ij}q_{ij}\ge L. \tag{D2}
\]

Only finitely many cone terms are used, so there is no infinite dual summation or exchange problem. Finite second moments ensure the quadratic expectation exists.

The saved certificates restrict multiplier cells to [−K−1,K]². They affect nodes only in [−K−1,K+1]². The independent verifier checks every coefficient in that complete affected box using exact fractions. At any remaining node, aᵢⱼ=dᵢⱼ. At least one coordinate then has absolute index ≥K+2, giving

\[
d_{ij}\ge\min_{r=1,2}(2K+4-|c_r|)^2\ge L.
\]

The checked centers satisfy |cᵣ|<2K+4, so the triangle lower bound is nonnegative before squaring. This is the analytic exterior argument that converts a finite-support dual into a genuine infinite-lattice certificate. It is not a claim that an optimizer has finite support. Rational rounding and the minimum exact coefficient account for the numerical guide's residuals; those residuals are not accepted as positivity evidence.

## 5. Exact quadratic interpolation over all unknown means

For any fixed array q, define

\[
C_q(c)=\sum|2(i,j)-c|^2q_{ij}.
\]

Take a rectangle with lower corner c₀ and side length h=1/4. Write c=c₀+h(t,u), t,u∈[0,1]. Let B denote bilinear interpolation of the four corner costs. Direct expansion of the quadratic gives the **identity**

\[
C_q(c)=B[C_q(\text{corners})](t,u)
-h^2\{t(1-t)+u(1-u)\}. \tag{D3}
\]

The bilinear weights are nonnegative, so each corner cost may be replaced by its independently valid dual lower bound L₀₀,L₁₀,L₀₁,L₁₁. Therefore the exact lower polynomial is

\[
P(t,u)=L_{00}+(L_{10}-L_{00}-h^2)t
+(L_{01}-L_{00}-h^2)u
+(L_{11}-L_{10}-L_{01}+L_{00})tu
+h^2(t^2+u^2). \tag{D4}
\]

The verifier minimizes this polynomial exactly on every one of the 16 rectangles covering [0,1]². It checks all edge minima and corners. An interior minimum is possible only with a positive definite Hessian, in which case its rational stationary point is checked if it lies in the square. An indefinite Hessian gives a saddle; a singular positive semidefinite Hessian has a minimizing flat line reaching an edge. Thus no interior minimum is omitted.

For the frozen certificates the minimum of these exact rectangle minima is

\[
L=19854624776291/6250745000000.
\]

It occurs in the first rectangle at c₁=c₂=213/1250149 **for the interpolating bound**. This does not identify the mean of the actual optimum. Equations (D2)–(D4), followed by the quotient/total-covariance argument, prove trCovν≥L for every admissible finite-covariance law.

## 6. Infinite upper certificates and complete tail variance

The tighter upper laws have unnormalized masses

\[
w_{ij}=\rho^{|i|+|j|}
p_{\min(|i|,N),\min(|j|,N)},\qquad i,j\in\mathbb Z,
\]

where 0<ρ<1 and p is a nonnegative symmetric rational table indexed up to N. Reflections map any cell to the nonnegative quadrant, possibly changing signs of X,Y; coordinate interchange merely swaps them. For a nonnegative cell (i,j), factoring the strictly positive common power ρⁱ⁺ʲ leaves the four corner weights

\[
p_{a,b},\quad \rho p_{a',b},\quad
\rho p_{a,b'},\quad \rho^2p_{a',b'},
\]

where a=min(i,N), a'=min(i+1,N), b=min(j,N), b'=min(j+1,N). If i≥N the same capped expression repeats forever; similarly for j. Checking 0≤j≤i≤N consequently checks **every infinite cell type**, including both strips and the double tail. Each check uses S≥0 and S²−X²−Y²≥0 exactly, which is the full SOC condition (D1).

The all-tail sums are also exact. A capped coordinate contributes multiplicity

\[
d_0=1,\quad d_i=2\ (0<i<N),\quad d_N=\frac2{1-\rho},
\]

after factoring ρⁱ. Its squared-index sum is

\[
s_0=0,\quad s_i=2i^2\ (0<i<N),\quad
s_N=2\left\{\frac{N^2}{1-\rho}
+\frac{2N\rho}{(1-\rho)^2}
+\frac{\rho(1+\rho)}{(1-\rho)^3}\right\}.
\]

Hence

\[
Z=\sum_{i,j=0}^N\rho^{i+j}p_{ij}d_id_j,
\quad
v=\frac{4\sum_{i,j=0}^N\rho^{i+j}p_{ij}(s_id_j+d_is_j)}Z.
\]

Separate reflections imply zero means and zero cross covariance; coordinate interchange makes both variances v/2. The independent verifier checks Z, the unnormalized second moment, their ratio, all cell types and exact nonproduct dependence. It never drops a tail moment. For the best frozen table N=10 and ρ=1/5, the displayed exact upper fraction follows. The geometric tails also supply all polynomial moments and a finite exponential neighborhood; all-exponential noise is not asserted.

The older `dependent_order_noise_sol` construction has a different cap convention, using q^{(|i|−3)₊+(|j|−3)₊} times its 4×4 integer table. Its nine core, three strip and one double-tail checks pass independently. Its exact total trace is 5949040524880/1857425454953≈3.2028421431483687. This remains a valid simpler upper construction, superseded numerically by the stronger certified table.

## 7. Analytic radial lower bound and optimizer existence

The older bound is independently valid. Let p=trM/2 and write M=pI+mzσz+mxσx. The finite convolution gives p as the law of N+S, with S uniform on the four corners and independent of N, and gives ∫x dmz=∫y dmx=1. The matrix |y|I−y₁σz−y₂σx is positive; its trace pairing with M is integrable under finite covariance. Thus E|N+S|≥2.

For a vector z with u=|z|², concavity of

\[
\phi_c(v)=\sqrt{2c+2\sqrt{c^2-4v}},\quad c=u+2,
\]

applied to (x+y)² and (x−y)² gives

\[
E_S|z+S|\le h(u)=\sqrt{(u+2+\sqrt{u^2+4})/2}.
\]

The exact affine majorant √2+K₀u, with \(K_0=\sup_{u>0}(h(u)-\sqrt2)/u\), yields trCovN≥(2−√2)/K₀. Substitution h=√2t gives the stated unique critical root 2t³−3t−2=0 and algebraic lower bound L₀≈2.66217523319253. Strict angular concavity and the unique positive maximizing radius force any equality law onto the origin plus four axial points. A finitely supported nonzero noise law is inadmissible: take its maximal first-coordinate atom and then maximal second coordinate on that face; at that atom plus (1,1), only one corner translate contributes a multiple of I+σz+σx, which is not positive.

The infimum is attained. Translate a minimizing sequence to mean zero. A uniform second-moment bound gives tightness and uniform integrability of first moments, so a weakly convergent subsequence has centered limit. Its second moment is bounded by lower semicontinuity. Convolution with finite T is weakly continuous; nonnegative continuous scalar tests against its quadratic forms show that positivity is closed. Normalization and finite covariance persist. The resulting law attains v*.

Disintegrating this optimizer, total covariance and conditional admissibility show that almost every conditional centered fiber has cost at least v*. Since the global cost already equals v*, the between-fiber mean variance vanishes and almost every fiber attains the same infimum. Some optimizer therefore lies on a single translated 2ℤ² coset. The same proof works for any positive definite quadratic covariance cost. Neither an integer center nor separate symmetry of an optimizer follows.

Together attainment and impossibility of the radial equality law imply v*>L₀. This strictness result is correct but much weaker than the certified dual lower bound. No strictness or equality conclusion at the new rational lower endpoint is asserted.

## 8. Operational distinction from the independent-noise packet

The dependence improvement over the independent normalized minimum 4 is a proved improvement **within the fixed scalar-convolution reporting contract**. It is not a demonstrated physical advantage over arbitrary unbiased joint measurements, whose ordinary trace benchmark is 2. No matched implementation, calibration, norm acquisition, preparation, finite-bit sampler, energy, error, reset or throughput comparison has been acquired.

The independent packet's equivalence to four sign effects must not be transferred automatically. For the dependent cap tables, normalized effects generally vary with the core cell indices. Taking only the two signs can therefore discard state information. No four-outcome equivalence has been proved for these constructions.

There is a finite-type realization: retain the two output signs and the two capped cell indices min(i,N),min(j,N). Within each such type, all effects are positive scalar multiples of one fixed effect. Summing each type gives a normalized POVM with at most 4(N+1)² outcomes. Conditional on a tail type, the remaining length is a state-independent geometric draw with parameter ρ; core lengths are fixed. Thus the exact upper reports are equivalent to this finite-type measurement followed by ancillary tail sampling. For N=10 the count is at most 484 outcome types, rather than four. This is an upper count for a mathematical realization, not a lower bound or an acquired instrument.

The law has unbounded exact output support. Clipping reports would alter the scalar-multiplier identity and require a new approximation error calculation. The covariance certificate alone supplies neither an optimal estimation decoder nor a universal copy-count comparison. Historical priority and exceptional significance remain unresolved, and worker agreement is not an additional proof premise.

## 9. Status and remaining obligations

Accept the displayed interval as an internally audited universal enclosure for the arbitrary-dependent unit Pauli noise trace. Preserve the exact optimum as unresolved. Keep finite LP/search values explicitly diagnostic even though their rationalized dual and tail certificates now support nearby rigorous bounds.

The first certificate snapshot was taken while the dual author's prose proof was still being written. The audit above independently reconstructs the analytic quantifier chain from those frozen data. The completed `PROOF.txt` was subsequently read in full and frozen as `author_dual_PROOF.snapshot.txt`; `AUTHOR_PROOF_RECEIPT.json` records SHA256 `11fa987c40790dd11a0ed5497fec6621d9f1059f73d7bdee0a3791ab0a1d7f59`. Its main claims match this audit and the frozen certificates.

The author's additional six-weight construction with N=2 and ρ=1/5 also passes independently: normalization 153/80, second-moment numerator 2819/400, and trace 2819/765<4. Its six exact cell-type determinants are 7/400, 151/1000000, 73/250000, 41/1562500, 41/1562500 and 9/9765625. Its optional radial formula agrees algebraically with the older L₀ formula; only the last few digits of its printed decimal need correction to approximately 2.66217523319253. This display issue does not affect the main interval.

The earlier independent-noise audit and its artifacts remain untouched.

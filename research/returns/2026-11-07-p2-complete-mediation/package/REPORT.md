# Complete classical mediation for noncommuting spin networks

Research construction, 7 November 2026. No historical-priority claim. No physical experiment.

## Outcome and scientific endpoint

The selected question is: **for a network with arbitrary two-body qubit interactions and arbitrary correlated Markovian noise linear in one-site Pauli operators, exactly when can its evolution be reproduced, to arbitrary accuracy, by local operations and classical communication without shared entanglement?**

This report resolves that question at the stated generator contract. A single matrix inequality characterizes the entire class. Its feasible side supplies a finite binary measurement-and-feedback protocol. Its infeasible side supplies a finite-time entanglement witness using one local reference qubit per system qubit. A convex optimization gives the minimum extra uniform local Pauli noise and certified numerical answers without enumerating the many-body Hilbert space.

The decisive distinction is complete preservation of separability, including local references. Ordinary preservation of separability of the system alone is strictly weaker. An explicit two-qubit family has an exact factor-two gap between the two thresholds.

The classical simulation consequence is polynomial in numerical time, coefficient scale and inverse accuracy, for specified product inputs or efficiently sampled separable mixtures and local measurements. There is no fast-forwarding claim in binary time, no generic Lindbladian solver, no computational-hardness conclusion outside the feasible cone, and no claim that a laboratory can implement the necessary controls cheaply.

The thermal local-response information theorem and every earlier predecessor retain their earlier scopes. In particular, unrestricted exact QUBO, the full fixed-temperature two-dimensional nucleation predictor, and the earlier exact elliptic sensitivity endpoint remain unresolved.

## 1. Input, normalization and access

There are explicitly counted qubits indexed by i=1,...,n. Put K=3n and label a=(i,alpha), alpha in {X,Y,Z}. Let A_a be that Pauli operator at site i. Within a site these operators need not commute. Across sites they commute.

The input consists of rational local fields, a real symmetric K by K matrix U with zero 3 by 3 diagonal site blocks, and a rational Hermitian positive-semidefinite matrix C=R+iJ, where R is real symmetric and J is real antisymmetric. All integers, denominators, site labels and coefficient lengths count toward the input length B. The generator is

\[
\mathcal L(\rho)=-i[H_{\rm loc}+\tfrac12\sum_{a,b}U_{ab}A_aA_b,\rho]
+\sum_{a,b}C_{ab}\bigl(A_a\rho A_b-\tfrac12\{A_bA_a,\rho\}\bigr).
\tag{1}
\]

The order A_b A_a in the anticommutator is essential. Using A_a A_b without changing the coefficient convention is incorrect for noncommuting local Pauli families. Units are fixed, with hbar=1 and the supplied time unit used throughout.

This class contains every two-body qubit Hamiltonian, arbitrary local Hamiltonians, all one-site Lindblad jumps, and collective jumps that are linear combinations of one-site Pauli operators. It includes amplitude damping. It excludes arbitrary jumps that are products of operators on several sites, higher-body Hamiltonians and non-Markovian environmental memory.

The digital requests are an additive noise-rate tolerance zeta>0, and where a channel or sample is requested, rational time t>=0 and error 0<epsilon<1. Confidence alpha is an additional input for statistical estimation or optional witness acquisition. Coefficient optimization and certificate construction are deterministic; trajectory sampling is randomized and explicitly pays for independent uniform random bits. The microscopic generator coefficients are supplied. They are not inferred from the predecessor's scalar imaginary-time observation channel. A physical witness further requires trusted local Bell preparation and measurement, fresh trials and validity of the stated model during the test.

Classical mediation means membership in the diamond-norm closure of finite-round LOCC, with no pre-existing shared entanglement. It does not mean exact realization in a fixed finite number of communication rounds. That distinction is necessary because LOCC is not closed [2].

## 2. Complete characterization

Let D and S range over real symmetric block-diagonal matrices, with one 3 by 3 block per site. Define

\[
\Sigma(D,S)=
\begin{pmatrix}
D&-\tfrac12(U+S+J)\\
-\tfrac12(U+S-J)&R-D
\end{pmatrix}.
\tag{2}
\]

### Theorem 1

For (1), the following are equivalent:

1. For every finite t>=0, exp(t L) is in the diamond-norm closure of finite-round LOCC.
2. For every t>=0, exp(t L) is a separable channel, equivalently it preserves full separability after arbitrary local reference systems are adjoined.
3. Starting with a product of n local system-reference Bell pairs, the output is fully separable across the enlarged sites for a sequence of positive times tending to zero.
4. There exist D,S as above with Sigma(D,S)>=0.

The matrix has size 6n and there are 12n free real variables. Local Hamiltonians do not enter the condition. They remain part of the simulation and its time cost.

This equivalence is about this generator class. It does not identify separable channels with LOCC for general channels, and it does not solve separability of arbitrary many-body states.

### 2.1 Necessity: locally prepared references resolve every Pauli direction

At each site prepare

\[
|0_i\rangle=|\Omega_i\rangle=(|00\rangle+|11\rangle)/\sqrt2,
\qquad |\alpha_i\rangle=(\sigma_\alpha\otimes I)|\Omega_i\rangle.
\]

These four vectors are orthonormal. Each reference is local to its site, so the total initial state is a product across parties. Define a_{i,alpha}=|0_i><alpha_i|, and for an arbitrary enlarged-system state define

\[
M_{ab}=\langle a_b^\dagger a_a\rangle,
\qquad N_{ab}=\langle a_a a_b\rangle\quad(i(a)\ne i(b)).
\tag{3}
\]

Leave each local symmetric block N_ii unspecified.

**Moment completion lemma.** Every fully separable state admits such a completion with

\[
\Gamma(M,N)=\begin{pmatrix}M&N\\N^*&M^*\end{pmatrix}\succeq0.
\tag{4}
\]

To prove the lemma, condition on a product-state decomposition and let z_i be the vector of local means <a_i>. Cross-site normal and anomalous moments are the classical moments E z_i z_j^dagger and E z_i z_j^T. The difference M_ii-E z_i z_i^dagger is positive semidefinite. This follows from the local density-matrix Schur complement, or from the variance inequality. Add independent proper complex random vectors at each site with these covariances and zero anomalous covariance. The full random vector then has normal covariance M and the required cross-site anomalous moments. Its augmented covariance is (4). The random vectors here prove a matrix fact; they are not supplied physical instruments or sampled data.

A direct differentiation of (1) at the initial Bell product gives

\[
M'(0)=C,
\qquad N'_{ab}(0)=-R_{ab}-iU_{ab}\quad(i(a)\ne i(b)).
\tag{5}
\]

The first identity comes from A_a rho_0 A_b. The second comes from the two-site vacuum-to-double-excitation matrix element of the Hamiltonian and anticommutator. Local Hamiltonians and the local noncommutative products contribute only vacuum/single-excitation coherences to these derivatives.

If the evolved state is separable along times t_j down to zero, divide its completions by t_j. Positivity bounds every entry of N/t_j by the geometric mean of diagonal entries of M/t_j. Since M/t_j tends to C, a convergent subsequence exists. In the limit there is an augmented covariance with normal block C and off-site anomalous block -R-iU.

Write its underlying complex random vector as z=x+iy. Then

\[
Ezz^\dagger=R+iJ,\quad
Exx^{\mathsf T}=D,\quad
Eyy^{\mathsf T}=R-D,\quad
Exy^{\mathsf T}=-\tfrac12(U+S+J).
\tag{6}
\]

The off-site real anomalous conditions force D to be block diagonal. The remaining imaginary anomalous freedom is precisely a block-diagonal symmetric S. Thus (6) is (2). No Gaussian-unravelling assumption or restriction on the possible separable decomposition was used.

The implications 1=>2=>3 are standard: LOCC channels have product Kraus operators, separable channels form a closed set in finite dimension, and the local Bell product is their Choi test. The remaining implication is constructed next.

## 3. A finite binary LOCC construction

Suppose (2) is feasible. Factor its real covariance in block form:

\[
x=V\xi,\qquad y=F\xi+G\eta,
\quad VV^{\mathsf T}=D,\quad VF^{\mathsf T}=B_0,
\quad FF^{\mathsf T}+GG^{\mathsf T}=R-D,
\tag{7}
\]

where B_0=-(U+S+J)/2 and V is block diagonal. The vectors xi and eta have independent reference Rademacher components. There are at most K components of each; zero columns can be omitted. PSD block factorization supplies (7), including singular cases. It does not require a bounded inverse of a singular D. A small regularization will provide a well-conditioned numerical construction below.

For each column k of V, let B_k=sum_a V_ak A_a. It acts on one site only. Because it is a real linear combination of the three Pauli matrices,

\[
B_k^2=b_k^2 I,\qquad b_k^2=\sum_a V_{ak}^2.
\]

For a real step parameter s, apply sequentially the two-outcome local instruments

\[
M_{k,\xi_k}(s)=\frac{I+s\xi_k B_k}{\sqrt{2(1+s^2b_k^2)}},
\qquad \xi_k\in\{-1,1\}.
\tag{8}
\]

Their effects sum exactly to I. The outcomes have their Born probabilities. Treating them as unweighted fair physical outcomes would give the wrong dynamics. The fair signs in (7) specify the Kraus reference measure, not the observed outcome distribution.

Broadcast the measured signs xi. Generate and distribute the additional fair signs eta, compute y=F xi+G eta, and apply at site i the rational Cayley rotation

\[
U_{i,y}(s)=
\frac{(1-s^2|y_i|^2/4)I+i s\,y_i\cdot\sigma}
{1+s^2|y_i|^2/4}.
\tag{9}
\]

This is exactly unitary for real coefficients. Apply also the local Cayley approximation to exp(-i s^2 H_loc,i). Everything is local except the transmission of classical bits. No continuous pointer, unbounded outcome, Gaussian random-number oracle or exponential list of Kraus branches is required.

For a gate-level realization of (8), one local ancillary qubit suffices. Since M_+ and M_- are commuting Hermitian matrices with M_+^2+M_-^2=I, the block matrix [[M_+,-M_-],[M_-,M_+]] is an explicit four-dimensional unitary. Preparing the ancillary qubit in |0> and measuring it after this unitary implements the instrument. Its entries are algebraic functions of the supplied rational coefficients. Approximating each such fixed-dimensional local unitary to the allocated error is a separate local gate-synthesis task. A specified universal local gate model permits standard finite synthesis; actual pulse time, native control accuracy and reset performance must be supplied by an apparatus. The classical trajectory algorithm below requires no physical apparatus.

Let Phi_s be this complete finite channel. Expanding at s=0, its first-order Kraus noise is

\[
\sum_a(x_a+i y_a)A_a,
\quad E(x+i y)(x+i y)^\dagger=C.
\]

The average second-order Kraus drift before the local Hamiltonian is

\[
-\tfrac12\sum_{a,b}R_{ab}A_aA_b
+i\sum_{a,b}(B_0)_{ba}A_aA_b
=-\tfrac12\sum_{a,b}C_{ab}A_bA_a
-\tfrac i2\sum_{a,b}(U+S)_{ab}A_aA_b.
\tag{10}
\]

The S contribution is a scalar multiple of the identity: S is symmetric within each Pauli block, so the cross terms cancel and only its trace remains. It has no effect on the channel. Consequently

\[
\Phi_s=I+s^2\mathcal L+O(s^4).
\tag{11}
\]

Odd powers vanish because changing every reference sign changes s to -s without changing the Kraus average. The noncommuting local measurement order creates no unwanted first-order generator: cross products of distinct reference signs have zero mean. The Cayley rotation has the same first two Taylor coefficients as the corresponding exponential.

Repeated finite LOCC steps converge in diamond norm to exp(t L). This proves 4=>1 and completes Theorem 1.

## 4. Explicit discretization and digital costs

These estimates intentionally favor a transparent global bound over practical constants.

Let ell=Tr R, and let H_0 be the sum of absolute local-field coefficients, an upper bound on the sum of local Hamiltonian norms. Define

\[
W=8+8K(1+\ell)+2H_0.
\tag{12}
\]

All quantities are numerical values in the fixed input units. PSD covariance implies

\[
\sum_k b_k\le\sqrt{K\ell},\quad
\max_{\xi,\eta}\sum_i|y_i|\le\sqrt2 K\sqrt\ell,
\quad \sum_k b_k^2\le\ell.
\]

Thus W exceeds the linear and square-root bounds needed below, independently of the Hilbert-space dimension 2^n.

### Lemma 2: finite-step bound

For h=s^2<=1/(32 W^2),

\[
\|\Phi_s-e^{h\mathcal L}\|_\diamond\le4096 W^4h^2.
\tag{13}
\]

Here is a bound proving the constant. Analytically continue the Kraus formula in the scalar s, with the adjoint replaced by coefficientwise adjoint so the resulting superoperator is analytic. On |s|=r=1/(4W), each measurement factor is bounded by exp(|s|b_k+|s|^2 b_k^2). The product of local feedback Cayley rotations is bounded by exp(2|s| sum_i |y_i|), and the local-field rotations by exp(2|s|^2 H_0). Each analytically continued Kraus factor therefore has norm at most exp(5/16); the superoperator has diamond norm below 3. Its even Taylor coefficients have norm at most 3 r^(-2j). For h<=r^2/2, the remainder after I+hL is at most 1536 W^4 h^2. The same Cauchy estimate gives ||L||_diamond<=48 W^2. Complete positivity and trace preservation give

\[
\|e^{hL}-I-hL\|_\diamond\le\tfrac12h^2\|L\|_\diamond^2
\le1152 W^4h^2.
\]

The sum is below 4096 W^4 h^2. Telescoping between channels gives

\[
\|\Phi_{\sqrt{t/m}}^m-e^{tL}\|_\diamond
\le4096 W^4t^2/m
\tag{14}
\]

whenever m>=32 W^2 t. In particular, m>=8192 W^4 t^2/epsilon allocates at most epsilon/2 to this error. For a complete end-to-end construction with coefficient approximation and rounding, use

\[
m\ge\max\{1,\lceil32W^2t\rceil,
\lceil32768W^4t^2/\epsilon\rceil\}.
\tag{15}
\]

### 4.1 Rational factors and a rational clock

Approximate the factor matrices V,F,G by rational matrices preserving the block structure of V. These matrices define an exactly valid generator by

\[
\widetilde R=VV^{\mathsf T}+FF^{\mathsf T}+GG^{\mathsf T},\quad
\widetilde J=FV^{\mathsf T}-VF^{\mathsf T},\quad
\widetilde U=\operatorname{offblock}[-VF^{\mathsf T}-FV^{\mathsf T}].
\tag{16}
\]

Its complete positivity and feasible covariance are automatic. An exact rational upper bound on the generator error is

\[
\Delta=2\sum_{a<b}|\widetilde U_{ab}-U_{ab}|
+2\sum_{a,b}(|\widetilde R_{ab}-R_{ab}|+|\widetilde J_{ab}-J_{ab}|).
\tag{17}
\]

The semigroup error is at most t Delta. Require Delta<=epsilon/[8(1+t)]. Local fields can be retained exactly.

Choose a dyadic s no greater than sqrt(t/m), by integer square root. With a rational upper bound Lambda on the diamond norm of the generator actually compiled (including its verified coefficient approximation), it suffices to choose

\[
2^{-p_s}\le\frac{\epsilon}{64m(1+t)(1+\Lambda)}.
\]

The resulting total clock difference m|(t/m)-s^2| produces less than epsilon/8 additional channel error. The step parameter has only O(log m+log(1+t)+log(1+Lambda)+log(1/epsilon)) fractional bits. The work still pays for m actual steps.

### 4.2 A fixed-budget classical sampler

For product input states given by rational Bloch vectors r_i, the conditional state remains a product at every step. It needs O(n) local state entries, not 4^n density-matrix entries. For a measurement direction b at a site, the exact probability of sign xi is

\[
p_\xi=\frac{1+s^2|b|^2+2s\xi b\cdot r}{2(1+s^2|b|^2)},
\]

and the exact updated Bloch vector is

\[
r'_j=\frac{(1-s^2|b|^2)r_j+2s\xi b_j+2s^2(b\cdot r)b_j}
{1+s^2|b|^2+2s\xi b\cdot r}.
\tag{18}
\]

The step restriction makes both probabilities exceed 1/4. For rational s,b,r these are rational operations. The feedback is also rational: writing U=aI+i c dot sigma as in (9),

\[
r'=(a^2-|c|^2)r+2c(c\cdot r)-2a(c\times r).
\tag{19}
\]

To bound precision uniformly, round each Bloch coordinate to a multiple of delta=2^(-p), then divide the rounded vector by 1+3 delta. This preserves positivity and changes the state by trace norm at most 5 delta. A p-bit uniform integer samples each rational branch probability rounded down to a p-bit probability; its probability error is at most delta. These operations have a fixed budget, including unlikely branches. Choose

\[
2^{-p}\le\frac{\epsilon}{1024 n(m+1)}.
\tag{20}
\]

Trace-norm contraction of the full classical-quantum instrument makes the accumulated error linear in the number of local operations. It is unnecessary to multiply worst-case conditional normalization factors over all steps. Equations (17), (15), the rational clock and (20), with the displayed slack, produce total output-distribution error below epsilon for product measurements at the end. A supplied efficiently sampled separable mixture is handled by sampling its classical label first and paying that sampler's cost.

There are K weak measurements and at most K extra shared random signs per step, at most two local rotations per site, and O(K^2) arithmetic operations to form dense feedback. At most 2nKm classical bits must be delivered if each sign is individually sent to every site; an ideal broadcast model charges at most 2Km broadcast bits instead. Shared randomness is generated and distributed, not free. Digital branch sampling uses at most (Km+n)p fair coin bits, in addition to the shared signs.

In a physical implementation, the weak measurements also pay for Km ancillary preparations/resets and their specified control accuracy. To retain a total physical channel-error budget epsilon, the implemented local instruments and rotations need errors of order epsilon/(Km) or smaller. This is an accuracy requirement on the apparatus, not a performance guarantee. The generator parameter t is simulated time. The implementing protocol takes m sequential communication rounds plus its local operations; with a nonzero communication latency it need not finish in laboratory time t. The theorem does not provide instantaneous communication or a bounded-bandwidth real-time mediator.

Let b_* bound the bit length after clearing coefficient denominators and including p,p_s and log K. Rounding after each operation prevents denominator growth with m. A conservative elementary rational-arithmetic cost for one output sample is

\[
O(mK^2 b_*^3)
\tag{21}
\]

plus the polynomial coefficient-discovery and factor-construction work described below. Memory is O(K^2 b_*+np). Estimating a bounded output observable to additive eta with failure probability alpha multiplies the trajectory cost by O(eta^(-2) log(1/alpha)). Relative accuracy for exponentially rare outcomes is not implied.

This is a genuine classical algorithm on the specified input. Its time dependence is polynomial in numerical t and coefficient scales, not uniformly in their binary lengths. For arbitrary entangled initial states, the LOCC channel construction remains valid in diamond norm, but this product-trajectory classical sampler is not asserted.

## 5. Optimal extra noise, with discovery paid

Adding lambda times every one-site Pauli dissipator replaces C by C+lambda I. Define the signed threshold

\[
\theta=\min_{\lambda\in\mathbb R,D,S}
\left\{\lambda:\Sigma(D,S)+\frac\lambda2I_{2K}\succeq0\right\}.
\tag{22}
\]

The shifted variable in the upper-left block represents the actual measurement covariance. The original generator is classically mediated exactly when theta<=0. The minimum extra nonnegative uniform Pauli noise is max(0,theta). Negative theta measures removable uniform noise; no physical negative dissipator is being prescribed independently of the final PSD condition.

Write a real symmetric dual variable as Y=[[P,Q],[Q^T,T]]. Then

\[
\theta=\max_Y\{\langle Q,U+J\rangle-\langle T,R\rangle\},
\tag{23}
\]

subject to

\[
Y\succeq0,\quad\operatorname{Tr}Y=2,\quad
(P-T)_{ii}=0,\quad(Q+Q^{\mathsf T})_{ii}=0
\quad\text{for each site block }i.
\tag{24}
\]

All inner products are entrywise real Frobenius inner products. Equation (24) annihilates the free D and S directions, while Tr Y=2 normalizes the lambda coefficient.

There is no weak-infeasibility loophole in the fixed-data feasibility test. Every Sigma has the fixed trace Tr R. A sequence approaching the PSD cone therefore has bounded matrices and bounded D,S, and has a feasible limit. For (22), the objective is bounded below by -Tr R/K. Taking D=S=0 and lambda>||U+J|| gives strict primal feasibility because R>=0. The dual has the strictly positive feasible point Y=I/K. Standard SDP duality therefore applies; the primal and dual optima are attained [6].

### 5.1 A uniform finite discovery algorithm

The SDP is an explicit convex problem, not a relaxation oracle assumed as an input. The following supplies the requisite bit contract using established rational ellipsoid machinery.

Set

\[
A=1+\sum_{a,b}(|R_{ab}|+|J_{ab}|+|U_{ab}|).
\]

Then -A<=theta<=A. At an optimum with lambda in this interval, positivity and the trace bound imply |D_ab|<=(K+2)A and |S_ab|<=(2K+3)A. Work in the larger rational box |D_ab|,|S_ab|<=8(K+1)A and |lambda|<=2A. Its bit length is polynomial in B+K.

For any zeta>0, increasing an optimal lambda by zeta makes the matrix strictly positive with eigenvalue margin zeta/2. A parameter ball of radius at least zeta/(64K), when necessary also moving the enclosing box slightly outward, stays feasible. The known strictly feasible point D=S=0, lambda=A supplies the starting geometry. On the dual side, Tr Y=2 bounds the matrix norm and Y=I/K supplies an interior point relative to its explicitly listed linear subspace.

A separation query is constructive. Test the rational candidate PSD matrix by diagonal-pivot Schur complements. If it is not PSD, the same elimination supplies a rational negative quadratic-form vector, and its outer product gives the separating affine cut. Box and linear-subspace tests are rational linear inequalities. All query arithmetic has polynomial bit cost. A standard rounded rational ellipsoid algorithm, or equivalent bit-controlled SDP algorithm, consequently produces rational primal and dual bounds of width at most zeta in

\[
\operatorname{poly}(K,B,\log(1+1/\zeta))
\tag{25}
\]

bit operations, using the weak separation/optimization machinery of [9]. The explicit outer bound and the zeta-dependent inner radius are what justify this application; no unquantified feasibility margin is omitted. Mixing a dual approximation slightly with I/K, then rounding in its rational linear subspace, yields an exactly checkable PSD dual certificate with a controlled loss in the objective.

If a feasible generator lies exactly on the boundary, add known uniform noise delta=epsilon/[128K(1+t)]. This changes the channel by at most 2K delta t. The shifted covariance has a controlled positive margin. Cholesky factorization with rational interval square roots then supplies approximations to (7). Its pivots are bounded below by the chosen margin; no hidden inverse-gap advice is needed. Round the factors and verify (17) exactly. Choose the noise and factor-error budgets jointly to retain the displayed epsilon allocation. The factor computation has polynomial bit cost in K,B,log(1/epsilon),log(1+t).

Thus a promise that the original generator is in the feasible cone gives a uniform arbitrary-accuracy compiler, including boundary points, without an exact singular SDP decision. For arbitrary inputs, (25) gives certified noise thresholds and either positive or negative certificates when their margins exceed the requested tolerance.

An exact sign decision at theta=0 is a separate operation. It is decidable for rational input by expressing PSD through all principal minors and applying real-algebraic quantifier elimination [10]. That is a finite generally exponential or worse procedure; a coarse cylindrical-algebraic-decomposition bound is doubly exponential in n. No exact polynomial-bit boundary decision is claimed. The structural theorem itself covers the boundary without ambiguity.

### 5.2 Robustness to supplied coefficient uncertainty

If two coefficient triples differ by Delta R,Delta J,Delta U, their signed thresholds satisfy

\[
|\theta'-\theta|\le2\|\Delta R\|+\|\Delta U+\Delta J\|.
\tag{26}
\]

Indeed the fixed part of Sigma changes by a matrix of norm at most ||Delta R||+||Delta U+Delta J||/2; an identity shift twice that large restores feasibility in either direction. The uncertainty bounds must actually be supplied or acquired. Equation (26) does not identify the generator from an unrelated record.

## 6. The infeasible side gives a finite witness

Let a rational dual certificate Y satisfy (24), with

\[
\kappa=\langle Q,U+J\rangle-\langle T,R\rangle>0.
\]

For the moments (3), define

\[
F_Y(\rho)=\tfrac12\langle P+T,\Re M\rangle
-\langle Q,\Im M\rangle
+\tfrac12\langle P-T,\Re N_{\rm off}\rangle
+\langle Q,\Im N_{\rm off}\rangle.
\tag{27}
\]

The constraints remove all dependence on the unspecified local N blocks. The completion lemma makes F_Y>=0 on fully separable states. It is the expectation of an explicit Hermitian witness W_Y supported termwise on at most two enlarged sites. At the Bell-product input,

\[
F_Y(\rho_0)=0,\qquad \frac{d}{dt}F_Y(e^{tL}\rho_0)\bigg|_{t=0}=-\kappa.
\]

A computable witness norm bound is

\[
M_Y=\sum_{a,b}(|P_{ab}|+|T_{ab}|+2|Q_{ab}|)
\le2K\operatorname{Tr}Y.
\tag{28}
\]

Take a rational bound

\[
\Lambda=2\sum|\text{local field coefficients}|
+2\sum_{a<b}|U_{ab}|
+2\sum_{a,b}(|R_{ab}|+|J_{ab}|)
\ge\|L\|_\diamond.
\tag{29}
\]

Since e^{tL} is CPTP, a Taylor integral bound gives

\[
F_Y(e^{tL}\rho_0)\le-\kappa t+\tfrac12 M_Y\Lambda^2t^2.
\tag{30}
\]

Thus any 0<t<=kappa/(M_Y Lambda^2) gives a certified negative expectation at most -kappa t/2. In particular, infeasibility implies entanglement at every sufficiently small positive time, not merely at one unspecified asymptotic time.

### Actual acquisition contract

Expand W_Y into Pauli strings on the physical system and reference qubits. Each term involves at most four qubits, so there are O(K^2) terms with a fixed constant factor. If S_W is the sum of their absolute coefficients, one can measure a randomly chosen string with probability proportional to its coefficient magnitude and return a score in [-S_W,S_W]. A bound is S_W<=16M_Y. With a certified true gap d=kappa t/2, thresholding the mean score at -d/2 needs

\[
N\ge\frac{8S_W^2}{d^2}\log\frac2\alpha
\tag{31}
\]

independent trials to bound each false-positive and false-negative probability by alpha. Preparation and measurement errors must have a separately justified total score-bias budget; for example a per-trial record TV bound eta causes bias at most 2 S_W eta.

Each trial requires n fresh local Bell pairs, evolution for time t, local measurement settings and readout. There are 2n physical qubits, O(n) preparation/control operations per trial and the corresponding repeated laboratory time. Neither these resources nor their calibration are supplied by the matrix theorem. No experiment was conducted here.

## 7. Exact separation between system-only and complete preservation

Consider two qubits with

\[
L\rho=-i[JZ_AZ_B,\rho]
+\gamma\sum_{P\in\{X,Y,Z\}}
\bigl(P_A\rho P_A-\rho+P_B\rho P_B-\rho\bigr).
\tag{32}
\]

Thus gamma is the coefficient of EACH Pauli dissipator; an isolated qubit's Bloch vector decays at rate 4 gamma.

### Theorem 3

For gamma>=0:

- Every separable two-qubit system input stays separable for all times if and only if gamma>=|J|/2.
- The dynamics has the complete classical-mediation property if and only if gamma>=|J|.

For the complete threshold, the augmented covariance has the fixed anomalous element N_{A,Z;B,Z}=-iJ and normal diagonal elements gamma. Its 2 by 2 principal minor requires gamma^2>=J^2. Conversely, D=gamma I/2,S=0 is feasible exactly when gamma>=|J|.

For the ordinary threshold, take an arbitrary pure product |a b>. On the orthogonal complement of its partially transposed projector, the derivative of the partial transpose has one zero direction and the block

\[
\begin{pmatrix}2\gamma&z\\\bar z&2\gamma\end{pmatrix},
\qquad |z|=|J\langle a_\perp|Z|a\rangle
\langle b_\perp|Z|b\rangle|\le|J|.
\tag{33}
\]

For gamma<|J|/2, the input |++> makes this block have a negative eigenvalue, proving immediate entanglement.

To prove sufficiency for ALL times, it is not enough to inspect one state's first derivative. For two qubits the PPT cone equals the separable cone [4], and its dual consists of P+Q^Gamma with P,Q>=0. At a boundary separable state rho, any active such dual functional vanishes separately on each pure-product member of a decomposition. Complete positivity makes the P contribution to its derivative nonnegative; (33) makes the Q contribution nonnegative whenever 2 gamma>=|J|. The generator is therefore cross-positive on the entire separable cone. The finite-dimensional cross-positive semigroup theorem [5, Theorem 3] proves invariance for every time, including equality at the threshold. This global argument is the reason the marginal first-derivative caveat in [3] does not invalidate the claim.

### An exact finite witness inside the gap

Set J=1 and gamma=3/4. At each enlarged site use the Bell basis |0>,|X>,|Y>,|Z>. Define

\[
|v\rangle=(|Z,0\rangle-i|0,Z\rangle)/\sqrt2,
\qquad W=(|v\rangle\langle v|)^{\Gamma_B}.
\]

This is nonnegative on all separable enlarged-site states, has ||W||=1/2, and its initial slope is gamma-J=-1/4. Equation (29) gives Lambda=11. At the rational time t=1/256,

\[
\boxed{\operatorname{Tr}(W\rho_t)
\le-\frac1{1024}+\frac{121}{262144}
=-\frac{135}{262144}<0.}
\tag{34}
\]

The physical four-qubit Pauli expansion has 16 nonzero terms and absolute coefficient sum 1. It is recorded exactly in REFERENCE_WITNESS.json. With trusted i.i.d. preparations and measurements, (31), using log(200)<6, gives the conservative bound **180,989,569 trials** for each error probability below 0.01. Those trials were not performed. Calibration bias would consume part of the gap and increase the budget.

This family falsifies the claim that system-only non-entangling dynamics must admit classical mediation. It does not prove classical computational intractability of simulating the channel.

## 8. Earned consequences

**A complete process classification across a broad interacting class.** Arbitrary noncommuting pair interactions and correlated linear local noise can be classified without expanding a 4^n density matrix. The local-reference test is complete for the semigroup question because it resolves every Pauli direction and the positive binary construction closes the converse.

**Optimal noise design.** The minimum extra uniform local noise is given by (22)-(24). More general nonnegative site-dependent Pauli-noise budgets and linear costs remain explicit SDPs. This yields a global noise-design calculation rather than an independent sufficient bound for each edge. Its source model is the supplied generator.

**Transfer through later local interventions.** Diamond-norm error composes under arbitrary finite adaptive local preparations, measurements, local gates and classical control between evolution intervals. Allocate an error to each interval and add the bounds. An efficiently described local-control experiment on a product input therefore has a classical trajectory sampler whenever the relevant generators satisfy the criterion. The number of interventions, record size, local-control computation and each interval's simulation cost are paid. Arbitrary nonlocal measurements or arbitrary entangled input descriptions are not silently included.

**A quantitative boundary for operational quantum behavior.** The factor-two family shows that adding only local reference systems can reveal a nonclassical process that never entangles initially separable systems by themselves. The stronger preparation/measurement interface must be explicit; it is not interchangeable with an ordinary system-only record.

**Robust finite witnesses.** A dual certificate produces a finite physical time, an observable with polynomially many local terms, a confidence budget and calibration requirements. The confidence digit cost is logarithmic, while the inverse witness-gap and preparation costs can be large.

**A precise limit on the conclusion.** Falling outside this cone rules out LOCC mediation of the specified process. It does not rule out an efficient classical numerical algorithm exploiting other structure. Being inside the cone does not promise cheap rare-event relative estimation, huge-time prediction, inexpensive physical feedback or an inexpensive identification experiment.

## 9. Relation to the governing capital and primary work

The governing Astra source used here is **N1686**, pinned at repository commit 54547cf3271092507c89ae393eaaa411d3cb3845. Its normally visible structural section states and constructs the commuting one-observable-per-party criterion, moment completion, outcome-weighted Gaussian implementation and dual witnesses. Only the complete cited structural section within its native PARTIAL prefix, lines 44-145, was used as the proof-bearing original. The held P3 package, proofs, code, data and audits were not acquired. No live peer operation was solicited. Other packet excerpts are not used as extra premises.

The present construction uses that covariance architecture at its actual scope. The added steps are the local-reference completion for noncommuting Pauli families, the finite binary/Cayley realization, its bit and clock accounting, the complete-separability distinction, and the resulting exact threshold separation. This is not a claim that covariance methods, continuous measurement feedback or reference-assisted channel tests originated here.

Diosi and Tilloy [1] explicitly construct continuous LOCC feedback with families of noncommuting local observables and discuss arbitrary pair potentials with added decoherence. Their construction and the underlying measurement-feedback literature receive credit. Their paper treats these as sufficient constructions and does not state the full converse proved in Theorem 1 for the present network class. Benatti, Liguori and Nagy [3] supply the primary short-time partial-transpose framework and its important marginal-case warning. Horodecki et al. [4] and Schneider-Vidyasagar [5] supply the all-time two-qubit cone argument. Standard Choi/product-Kraus, covariance, semidefinite-optimization, rational approximation and concentration machinery are credited rather than claimed anew.

The strong-noise generic sampling question considered during selection was set aside after checking Trivedi-Cirac [8], whose work already establishes a strong-noise simulability transition. That result is not relabeled as a new achievement here. The selected endpoint is the exact operational mediation boundary and its two-sided construction.

No claim of historical priority, laboratory realization, demonstrated practical speedup, P=NP or P!=NP is made.

## 10. Reproducibility and executed scope

Run `python validate_mediation.py` in this directory. It uses the existing NumPy/SciPy installation for small matrix diagnostics and custom exact rational-complex arithmetic for the certificates. The production rational trajectory kernel in mediation.py uses only Python's standard library.

The run completed 107 assertions: 102 exact algebraic/positivity checks and five explicitly floating small-channel diagnostics. It verified the noncommuting drift identity, every entry of the normal reference derivative, the cross anomalous derivatives, binary-instrument normalization, rational-unitary normalization and Bloch action, rational PSD separation including singular candidates, exact primal and dual certificates, the general dual-witness formula with asymmetric correlations, the finite witness and its Pauli expansion, the four ordinary tangent-threshold cases, and positivity of a short rounded rational trajectory. Four small-channel diagnostics exhibit the predicted O(h^2) one-step behavior; they are checks, not the proof of the general bound.

The short trajectory run used 12 steps and 36-bit rounding. It has no assigned continuum accuracy under the conservative global theorem. For illustration, the exact-factor compiler budget at n=2, Tr R=6, H_0=0, t=1/100, epsilon=1/100 already exceeds 10^12 steps. That budget was not executed. Neither numerical checks nor an asymptotic polynomial establish practical performance.

The executable artifact includes a certificate checker and a rational trajectory kernel. It is not a packaged general-purpose SDP optimizer. Uniform discovery is the explicit reduction with separation and radius bounds in Section 5, using established bit-controlled convex optimization; no result of an unconstructed physical or relaxation oracle is assumed.

## References

[1] L. Diosi and A. Tilloy, *On GKLS dynamics for local operations and classical communication*, Open Systems & Information Dynamics 24, 1740020 (2017), arXiv:1710.04565. https://arxiv.org/abs/1710.04565

[2] E. Chitambar, D. Leung, L. Mancinska, M. Ozols and A. Winter, *Everything You Always Wanted to Know About LOCC (But Were Afraid to Ask)*, Communications in Mathematical Physics 328, 303-326 (2014), arXiv:1210.4583. https://arxiv.org/abs/1210.4583

[3] F. Benatti, A. M. Liguori and A. Nagy, *Environment Induced Bipartite Entanglement*, Journal of Mathematical Physics 49, 042103 (2008), arXiv:0805.4790. https://arxiv.org/abs/0805.4790

[4] M. Horodecki, P. Horodecki and R. Horodecki, *Separability of Mixed States: Necessary and Sufficient Conditions*, Physics Letters A 223, 1-8 (1996), arXiv:quant-ph/9605038. https://arxiv.org/abs/quant-ph/9605038

[5] H. Schneider and M. Vidyasagar, *Cross-Positive Matrices*, SIAM Journal on Numerical Analysis 7, 508-519 (1970), Theorem 3. https://people.math.wisc.edu/hans/ssagar.pdf

[6] L. Vandenberghe and S. Boyd, *Semidefinite Programming*, SIAM Review 38, 49-95 (1996). https://web.stanford.edu/~boyd/papers/sdp.html . Standard rounded rational ellipsoid bit complexity is used with the explicit separation, boundedness and inner-radius data stated in Section 5.

[7] O. Gittsovich, O. Guhne, P. Hyllus and J. Eisert, *Unifying several separability conditions using the covariance matrix criterion*, Physical Review A 78, 052319 (2008), arXiv:0803.0757. https://arxiv.org/abs/0803.0757

[8] R. Trivedi and J. I. Cirac, *Simulability transitions in continuous-time dynamics of local open quantum systems*, arXiv:2110.10638. https://arxiv.org/abs/2110.10638

[9] M. Grotschel, L. Lovasz and A. Schrijver, *Geometric Algorithms and Combinatorial Optimization*, Springer (1988). https://link.springer.com/book/10.1007/978-3-642-97881-4 . Earlier primary paper: *The Ellipsoid Method and Its Consequences in Combinatorial Optimization* (1981), https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1981b.pdf .

[10] G. E. Collins, *Quantifier elimination for real closed fields by cylindrical algebraic decomposition*, Lecture Notes in Computer Science 33, 134-183 (1975). https://doi.org/10.1007/3-540-07407-4_17

[Astra N1686] Governing packet: https://github.com/harjassand/astra-research-knowledge/blob/54547cf3271092507c89ae393eaaa411d3cb3845/knowledge/current/packets/N1686.json . Proof-bearing visible structural section: https://github.com/harjassand/astra-research-knowledge/blob/54547cf3271092507c89ae393eaaa411d3cb3845/research/2026-11-04-p3-classical-mediation-visible/source/p3/NATIVE_RESPONSE_PREFIX_PARTIAL.txt#L44-L145 . Source SHA-256 e93dcc8df73b14174f30fd98d3509d4a28a23a2658ee04ffbab623d64aabeab9. The native source is a partial prefix; the used structural section is complete within that prefix. Held supplements were not used.

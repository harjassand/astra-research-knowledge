# CRAY: A bounded-field mixture compiler for positive low-rank Ising interactions

Date: 12 October 2026

**Status.** This note supplies a new proof candidate and a complete algorithmic reduction, with explicit finite-bit interfaces to established algorithms. The algebraic envelope and approximation bounds have proofs below. The general end-to-end algorithm has not been implemented, independently reviewed, or formally verified. A rank-one product-base prototype is supplied with explicitly uncertified numerical weights. Historical priority is unresolved. The accompanying programs are finite diagnostics, not implementations of the general complexity theorem.

## 1. Computational result and its limits

Given rational data

\[
J_0\in\mathbb Q^{n\times n},\quad A\in\mathbb Q^{r\times n},\quad
K\in\mathbb Q^{r\times r},\quad h\in\mathbb Q^n,
\]

assume

\[
0\preceq J_0\preceq(1-\gamma)I,
\qquad K\succ0,
\qquad 0<\gamma\le1.
\]

The target is the discrete probability law

\[
p(x)=Z^{-1}\exp\left\{\frac12x^TJ_0x+
\frac12(Ax)^TK(Ax)+h^Tx\right\},\qquad x\in\{-1,+1\}^n.
\tag{1}
\]

Let B denote total rational input bit length, including a supplied rational gamma. Let 0 < epsilon < 1/2 and 0 < delta < 1/2.

**Compiler theorem, proof candidate.** A randomized preprocessing algorithm constructs a finite mixture of bounded-field Ising laws with common interaction J0. With probability at least 1-delta, it provides (i) a discrete sampler within epsilon total variation of (1), and (ii) a rational estimate of log Z with additive error epsilon. Its total bit cost is

\[
\left[\frac{n^2\{\sqrt n+\log(n/\epsilon)\}}{\epsilon}\right]^{O(r)}
\operatorname{poly}\bigl(B,n,\gamma^{-1},\epsilon^{-1},\log(1/\delta)\bigr).
\tag{2}
\]

The polynomial has an absolute degree; no numerical norm of A, K, h or A^TKA, inverse Gaussian cell probability, or global metastable mixing time appears. Rank r can be reduced to rank(A) <= n by rational row-basis elimination. The r=0 case is elementary and can be handled separately. Polynomial-time terminology requires fixed r and inverse-polynomial (in the input parameters) gamma; arbitrarily tiny binary-encoded gamma is not free.

The bound is deliberately conservative. It composes old convex-volume algorithms with a simple annealing estimator for the base partition function; it does not assert a practical runtime advantage. Exponential dependence on rank remains. The strong interaction is positive low rank; the residual interaction stays in the stated high-temperature regime. This is not a theorem for cooling an arbitrary full-rank system.

After preprocessing, a draw requires only selecting one mixture component and sampling an n-spin bounded-field base law. It requires no continuous latent-variable output, no phase tunnelling and no rejection. For an unconditional TV statement, set the preprocessing failure probability to at most epsilon/8 and allocate the remaining tolerance internally. The log-partition statement retains an independently selectable confidence parameter delta.

A second, constant-resolution version has a grid independent of epsilon and an exact ideal rejection identity, with acceptance at least 3 exp(-1/4)/4. It is preserved below as a stronger algebraic primitive, but the rejection-free version is the main finite-bit compiler because it avoids an additional continuous-sampling interface.

## 2. Search selection and research-capital separation

Three different computational settings were screened: non-Markovian quantum-impurity evolution, high-frequency wave propagation, and equilibrium spin-system sampling. In the first two, a decisive advance would require, respectively, an acquired and uniformly controlled influence-functional compression, or an output representation and resonance/stability certificate compatible with an actual high-frequency solver. No such new theorem was established during this run. These were screens, not completed research investigations.

The selected task is full-distribution sampling and relative partition estimation for finitely specified spin models, not thermodynamic-limit free energy, local observables only, or a variational objective with extensive additive error.

The Astra repository was inspected at revision `f12638af678bb8f3cc4039f10de78a55476a3a0c`, including its entry instructions, branch registry and relevant concept routing. The registry records N726 finite Gaussian crossings, N727 interchange rate saturation, N728 active prediction, N729 strain geometry and N730 infinite-spectrum/relative transfer. This result uses none of their proof claims. N726 and N730 are retained unchanged for independent verification, not silently certified or used as premises. The published registry does not rule out unpublished concurrent work.

The OpenAI mathematics repository README and selected catalogue entries were also inspected. Its asymptotic spin-pressure/cavity and geometric results were not imported as finite-input algorithms. Publication in either repository is not independent verification.

## 3. The operation: clip the sampler field, retain its excess energy

Write

\[
E_0(x)=\tfrac12x^TJ_0x,
\qquad \ell(y)=h+A^Ty,
\qquad C_K=(2\pi)^{r/2}(\det K)^{1/2}.
\]

The standard Hubbard--Stratonovich identity gives

\[
F(y,x)=\exp\{-\tfrac12y^TK^{-1}y+E_0(x)+\ell(y)^Tx\},
\qquad \sum_x\int F(y,x)\,dy=C_K Z.
\tag{3}
\]

This identity is inherited machinery, not the invention. Alone, it leaves a multimodal latent distribution.

Set

\[
R=\max_i\sum_{j\ne i}|(J_0)_{ij}|\le\sqrt n.
\tag{4}
\]

The last inequality follows from the row Euclidean norm bound implied by ||J0||op <= 1 and Cauchy--Schwarz.

Choose a threshold L > R and partition the interval [-L,L] into equal intervals of width Delta. The hyperplanes

\[
h_i+a_i^Ty=t
\tag{5}
\]

at their endpoints partition latent space into full-dimensional cells C. Here a_i is column i of A. On a cell let c_C be a constant vector: +L above the positive threshold, -L below the negative threshold, and the midpoint of the occupied interval otherwise. Thus, for unsaturated coordinates,

\[
\sum_{i:\,|\ell_i(y)|<L}|\ell_i(y)-(c_C)_i|\le b:=n\Delta/2.
\tag{6}
\]

Define the retained excess

\[
D(y)=\sum_i(|\ell_i(y)|-L)_+.
\tag{7}
\]

On each C, D(y)=d_C^Ty+e_C is affine, even when the original fields and coupling parameters are enormous. The envelope joint weight is

\[
Q(y,x)=\exp\{-\tfrac12y^TK^{-1}y+D(y)\}
        \exp\{E_0(x)+c_C^Tx\},\qquad y\in C.
\tag{8}
\]

The essential distinction is between replacing a field in the base sampler and deleting its energetic contribution. The first is safe after the second contribution is retained analytically; the second alone is false.

## 4. Exact envelope theorem

Put rho = n exp[-2(L-R)] and assume rho < 1.

**Theorem 1.** For every latent point outside irrelevant cell boundaries,

\[
(1-\rho)e^{-b}
\le
\frac{Z_0(\ell(y))}{e^{D(y)}Z_0(c_C)}
\le e^b,
\qquad
Z_0(c)=\sum_x e^{E_0(x)+c^Tx}.
\tag{9}
\]

Moreover

\[
a(y,x)=\exp\{(\ell(y)-c_C)^Tx-D(y)-b\}\in[0,1]
\tag{10}
\]

is an acceptance function satisfying

\[
Q(y,x)a(y,x)=e^{-b}F(y,x),
\qquad
\mathbb E_{X\sim\mu_{0,c_C}}a(y,X)
\ge (1-\rho)e^{-2b}.
\tag{11}
\]

**Proof.** For a saturated coordinate, write ell_i=s_i(L+t_i), t_i>=0 and s_i in {-1,+1}. Its contribution to (ell-c)^Tx-D is

\[
t_i(s_ix_i-1)=
\begin{cases}0,&x_i=s_i,\\-2t_i,&x_i=-s_i.\end{cases}
\]

The sum of the contributions of unsaturated coordinates lies in [-b,b]. This proves a<=1 and the pointwise identity in (11).

Under the base law at field c_C, conditioning on all other spins gives local field

\[
(c_C)_i+\sum_{j\ne i}(J_0)_{ij}x_j.
\]

For a saturated coordinate this has the correct sign with magnitude at least L-R. Its conditional, hence unconditional, wrong-sign probability is at most exp[-2(L-R)]. No independence assumption is used. By a union bound, every saturated spin is aligned with probability at least 1-rho. On that event the exponent in (10) is at least -2b. This proves the acceptance lower bound. Integrating the same exponent before the subtractive b proves (9). QED.

Let Q_tot be the total mass of (8) and let q denote its normalized joint law. Its ideal accepted law has spin marginal p. Coupling a proposal to its accept/reject decision shows

\[
\|q_X-p\|_{TV}
\le 1-\alpha
\le 1-(1-\rho)e^{-2b}
\le \rho+2b,
\tag{12}
\]

where alpha is the mean acceptance. One can also see this from q = alpha p_joint + (1-alpha) r_joint and then take spin marginals.

Integrating (9) gives

\[
(1-\rho)e^{-b}Q_{\rm tot}\le C_K Z\le e^bQ_{\rm tot},
\]

and therefore

\[
\left|\log Z-\{\log Q_{\rm tot}-\log C_K\}\right|
\le b-\log(1-\rho).
\tag{13}
\]

### Constant-resolution form

Choose

\[
L=\lceil R\rceil+\lceil\log_2(4n)\rceil,
\qquad \Delta=1/(4n).
\]

Then b=1/8 and rho<=1/4, so alpha>=3 exp(-1/4)/4 > 0.5841. The expected number of ideal proposals is below 1.713. This is independent of the spike strength, external field, number or separation of phases, and Gaussian cell mass. The exact partition identity is

\[
\log Z=\log Q_{\rm tot}+1/8+\log\alpha-\log C_K.
\tag{14}
\]

Implementing this variant needs a controlled internal conditional-Gaussian sampler. It is not necessary for the following compiler.

## 5. Rejection-free finite mixture

For the main epsilon-accurate algorithm choose

\[
L=\lceil R\rceil+\left\lceil\log_2\frac{8n}{\epsilon}\right\rceil,
\quad
N=\left\lceil\frac{16nL}{\epsilon}\right\rceil,
\quad
\Delta=2L/N.
\tag{15}
\]

Then b<=epsilon/16 and rho<=epsilon/8. Equations (12)--(13) imply

\[
\|q_X-p\|_{TV}\le\epsilon/4,
\qquad
\left|\log Z-\{\log Q_{\rm tot}-\log C_K\}\right|<\epsilon/2.
\tag{16}
\]

There are at most

\[
m=n(N+1)=O(n^2L/\epsilon)
\]

proper hyperplanes. Their arrangement has at most

\[
M\le\sum_{j=0}^r {m\choose j}
\tag{17}
\]

full-dimensional cells. This follows by the usual insertion recurrence for hyperplanes; degeneracies only reduce the number. Constant-field hyperplanes are handled without splitting. Ties on genuine boundaries have zero latent Gaussian measure.

Define

\[
G_C=\int_C\exp\{-\tfrac12y^TK^{-1}y+d_C^Ty+e_C\}\,dy,
\quad W_C=G_C Z_0(c_C).
\tag{18}
\]

Then

\[
q_X(x)=\sum_C\frac{W_C}{\sum_DW_D}\,\mu_{0,c_C}(x).
\tag{19}
\]

This is a finite mixture of already tractable bounded-field spin laws. Latent points do not have to be drawn to sample (19).

**Algorithm.** Enumerate cells; compute their c_C,d_C,e_C; approximate log G_C and log Z0(c_C); store approximate log weights and a finite categorical sampler. Output the log-sum of weights minus log C_K as the partition estimate. To draw spins, select a cell and run the bounded-field base sampler.

A direct incremental arrangement implementation makes O(mM) rational LP feasibility calls. Each cell needs only the current interval for each of the n field coordinates, hence at most 2n linear inequalities. Standard exact LP implements strict-feasibility tests using a slack variable; full-dimensionality is decidable. Coefficient bit lengths are polynomial in B,n,r,log(1/epsilon). The number of cells depends on the number of field thresholds, not on their spacing in Euclidean latent coordinates.

## 6. Gaussian masses without inverse-event-probability cost

It would be invalid to leave (18) as an uncharged Gaussian rejection oracle. This section constructs a different interface from classical convex-volume approximation.

Write H=K^{-1}, mu=Kd_C and

\[
q_C(y)=\tfrac12(y-\mu)^TH(y-\mu),\quad
y_*={\rm argmin}_{y\in C}q_C(y),\quad
\phi(y)=q_C(y)-q_C(y_*).
\]

The minimizer exists and is unique on the closed cell. It is rational with polynomial bit length. To acquire it, one may enumerate sets of at most r active constraints, solve their rational KKT systems and test primal feasibility and nonnegative multipliers. A conic Caratheodory argument guarantees one such set; dependent sets can be discarded. This takes (2n+1)^{O(r)} polynomial-bit operations. Polynomial-time convex QP is another valid implementation.

Then

\[
G_C=e^{e_C+d_C^TKd_C/2-q_C(y_*)}\,I_C,
\qquad
I_C=\int_C e^{-\phi(y)}dy.
\tag{20}
\]

The large exponent is rational and computed exactly. Its exponential is never expanded. It is added to log I_C.

### 6.1 Relative truncation with no unknown mass

For t>=0 define

\[
V(t)={\rm vol}_r\{y\in C:\phi(y)\le t\}.
\]

Convexity about y_* gives V(t)<=t^r V(1) for t>=1. Also I_C>=e^{-1}V(1). Layer-cake integration gives

\[
I_C=\int_0^\infty e^{-t}V(t)\,dt,
\quad
\frac{\int_T^\infty e^{-t}V(t)dt}{I_C}
\le e\int_T^\infty e^{-t}t^r dt.
\tag{21}
\]

This is a bound on the positive layer-cake tail, not an estimate obtained by dividing by an unknown tiny Gaussian event probability.

To approximate I_C to log error eta, use a rational mesh s=eta/16 and choose an integer cutoff, for example

\[
T=4(r+1)^2+4\lceil\log_2(32/\eta)\rceil,
\quad J=\lceil T/s\rceil.
\]

The positive sum

\[
S_J=(1-e^{-s})\sum_{k=1}^J e^{-(k-1)s}V(ks)
\tag{22}
\]

approximates I_C without subtracting nearby estimated volumes. For the infinite sum S_inf, integrating each point's geometric series yields I_C<=S_inf<=e^s I_C. Moreover

\[
S_{\infty}-S_J
\le e^s\int_{Js}^{\infty}e^{-t}V(t)dt.
\]

For t>=4r^2, t^r<=e^{t/2}; hence the relative omitted tail is at most 2 exp(s+1-Js/2). The stated T makes it smaller than eta/16. Approximating every V(ks) to log error eta/16 and evaluating the positive weights at adequate precision therefore approximates log I_C within eta. This takes

\[
O((r^2+\log(1/\eta))/\eta)
\]

relative convex-volume calls. More efficient logconcave integration algorithms can replace this construction, but they are unnecessary to the existence theorem.

### 6.2 Acquiring the volume-oracle guarantees

Each body K_t={y in C:phi(y)<=t}, t>0, has rational linear constraints and one rational convex quadratic constraint. It has a rational separation oracle: use a violated linear constraint or the gradient separation inequality for the quadratic.

First-order optimality of y_* gives

\[
\phi(y)\ge\tfrac12(y-y_*)^TH(y-y_*),\qquad y\in C.
\tag{23}
\]

Thus K_t has an explicit outer radius whose logarithm is polynomial in the rational data length and log t.

Full-dimensional rational C has a strict rational feasible point z with polynomial-bit coordinates and positive rational slacks bounded below by 2^{-poly(B')}, obtainable by LP. Move a rational fraction lambda toward z from y_*. For lambda at least 2^{-poly(B'+log(1/t))} and chosen sufficiently small, the new point has phi<t/4 and strictly positive slacks. Rational bounds on the Hessian, gradient and constraint norms give a ball of radius at least 2^{-poly(B'+log(1/t))} inside K_t. This supplies an inner ball as well as an outer ball with polynomial encoding length.

Classical polynomial-time convex-volume approximation for well-guaranteed rational separation oracles now applies. Its rounding stage handles the numerical aspect ratio; the input cost depends on the encodings of the radius bounds. The original Dyer--Frieze--Kannan approach uses a discrete grid walk and explicitly finite random choices, so this reduction does not require outputting a continuous variable in total variation. Its enormous polynomial degree is acceptable for the complexity-existence claim, not evidence of practical performance.

Consequently log G_C is approximable in (2n+1)^{O(r)} poly(B',r,eta^{-1},log(1/zeta)) bit operations, where zeta is its failure probability. No reciprocal Gaussian mass appears. The construction also handles far-off-centre cells and exponentially thin cells; their coordinate and slack *bit lengths*, rather than their inverse widths, are charged.

## 7. An explicit bounded-field base engine

The only non-geometric sampling input is an established high-temperature Ising theorem. Eldan--Koehler--Zeitouni prove a Poincare gap at least 1-||J0||op for continuous-time single-site heat bath with total rate n. Random-site discrete heat bath therefore has gap at least gamma/n. The result holds for every external field. We use it only at ||c||infinity<=L.

Since 0<=E0(x)<=n/2,

\[
\log(1/\mu_{0,c}(x))\le n\log2+n/2+2nL.
\]

A conservative independent restarted base sample with TV error tau needs

\[
t_0(\tau)=O\left(\frac n\gamma
\{n(L+1)+\log(1/\tau)\}\right)
\tag{24}
\]

heat-bath updates. One dense update costs O(n) rational arithmetic operations plus a bounded-accuracy logistic evaluation and random-bit draw. Each operation uses polynomially many bits in B,log(1/tau) and the logarithm of the total update count. Coupling per-update errors with total budget tau controls the implemented chain. Sharper published mixing results may replace (24); they are not required.

For partition estimation, interpolate J0 by kJ0/n, k=0,...,n. At stage k,

\[
Z_{(k+1)J_0/n,c}/Z_{kJ_0/n,c}
=\mathbb E_{kJ_0/n,c}\exp(E_0(X)/n),
\]

whose integrand lies in [1,e^{1/2}]. The initial partition is product-form, Z0,c=product_i 2 cosh(c_i). Hoeffding estimation with per-stage tolerance O(eta/n) uses O(n^2 eta^{-2} log(n/zeta)) independent restarted samples per stage. Thus O(n^3 eta^{-2} log(n/zeta)) base samples suffice in total.

One conservative arithmetic bound is

\[
T_{Z_0}(\eta,\zeta)
=O\left(
\frac{n^5}{\gamma\eta^2}
\{n(L+1)+\log(n/\eta)\}\log(n/\zeta)
\right),
\tag{25}
\]

multiplied by polynomial bit-arithmetic overhead. Sampling biases and finite arithmetic are budgeted below the per-stage tolerance. For J0=0, the base partition and independent spin sampling are directly product-form, and this annealing overhead disappears.

## 8. Full resource and error ledger

Use eta=epsilon/256, with smaller fixed constants if desired. Estimate both log G_C and log Z0(c_C) to error eta for every C, allocating failure delta/(2M) to each estimate. Their sum gives every log W_C to error 2eta. Uniform log-weight error gives at most O(eta) error in the normalized categorical law and at most 2eta error in the log-sum; errors do not multiply by M. The union bound affects confidence through log M, not required relative accuracy.

The representation bias is at most epsilon/4 in TV and below epsilon/2 in log partition. Allocate epsilon/8 to base-sampler error and epsilon/8 to categorical/evaluation error. Together with the stated log-weight errors, these remain below epsilon on the preprocessing-success event. For an unconditional sampling guarantee, include preprocessing failure in the TV budget. A batch of k draws with joint-TV epsilon can use epsilon/k internal tolerances; individual marginal guarantees alone do not imply an unlimited independent target stream.

A fully charged decomposition is

\[
T_{\rm prep}\le T_{\rm arrangement}
+M\,[T_{Z_0}(\eta,\delta/(2M))+T_G(r,2n,B',\eta,\delta/(2M))]
+\operatorname{poly}(M,n,r,B',\log(1/\epsilon)),
\tag{26}
\]

where T_arrangement makes O(mM) exact LP calls and T_G is constructed in Section 6, including the QP mode and all volume calls. This proves (2) by composition with the credited algorithms.

Post-preprocessing, each draw uses O(log M) categorical-tree work, one base draw, and O(n) output writing. There is no latent Gaussian draw. A dictionary occupies M poly(n,r,B,log(1/epsilon),log(1/delta)) bits, in addition to the base matrix storage. Gaussian integration workspace can be reused cell by cell. Random bits, LP/QP preprocessing, annealing samples, categorical normalization and actual output are included in (26), rather than treated as free oracles.

All potentially enormous weights are stored in logarithmic form. For categorical sampling, subtract the largest log weight and discard terms below a log(M/eta) cutoff, bounding the discarded total mass. The retained exponentials need only polynomial precision. The prefactors in (20) are evaluated by exact rational arithmetic before adding the approximated logarithmic integral, avoiding cancellation between poorly resolved large floating-point quantities.

The output is log Z or a compact scientific-notation approximation to Z. Printing the fully expanded decimal digits of an exponentially large Z is not claimed to take polynomial time. A log Z of magnitude 2^{poly(B)} has only polynomial integer-part bit length; additive epsilon precision costs O(log(1/epsilon)) additional fractional bits.

The theorem assumes supplied, exact rational A,K,J0,h. Rational symmetry, positive definiteness and semidefinite inequalities can be verified with exact linear algebra. A hidden or experimentally learned factorization is not granted for free. If one starts from approximate parameters, a separate sufficient transfer condition is

\[
\sup_x |E(x)-\widehat E(x)|\le u,
\]

which gives density ratios between exp(-2u) and exp(2u). For aggregate J and h, n||J-Jhat||op/2+||h-hhat||1<=u is sufficient. Acquiring such absolute accuracy may be experimentally costly when factors are large. No measurement-efficiency claim is made.

## 9. Counterexamples and operations investigated

**Gaussian lifting alone.** Equation (3) is familiar but does not acquire the weights of disconnected or sharply concentrated phases. It does not by itself solve sampling.

**A uniform Euclidean latent grid.** Large A or K forces a fine grid or enormous domain in this representation. The field-hyperplane arrangement changes the representation: only the bounded interval of relevant *sampler fields* is resolved, while outside contributions are affine and integrated analytically.

**Naively discarding large fields.** For n=1,A=1,h=0,K=beta, the exact partition is 2 exp(beta/2). Replacing the latent field by its clip, without D, gives at most 2 cosh L. At beta=100,L=4 the true log partition is 50.693..., while that approximation is at most 4.00034. This is an exponential error, not a harmless saturation.

**Piecewise linearization for independent spins.** Piecewise-affine approximations to log cosh give a related route when J0=0. It does not immediately handle a correlated base partition. The joint envelope and wrong-sign conditional bound replace that scalar-function approach and work without independence. This precursor is not separately claimed as a novel theorem.

**Large negative rank-one spikes.** This obstruction is already established in the literature, not a new result of this run. The elementary reason is visible in p_a(x) proportional to exp[-4n(a^Tx)^2] for integer a. A perfect partition, if one exists, carries almost all the mass; a sufficiently accurate polynomial-time sampler would find a verifiable zero with constant probability. Hence a uniform analogous negative-spike theorem would imply RP=NP. A sign-free version of the present claim is therefore not justified.

**Growing positive rank.** The arrangement can have m^{Theta(r)} cells. That is a real cost of this construction, not a lower bound for the underlying sampling problem. No polynomial-in-r theorem is proved. In fact, adding a sufficiently large rational diagonal to the hard negative-spike interaction leaves its spin law unchanged and makes the matrix positive definite. Thus a polynomial algorithm for unrestricted positive full rank would inherit that hardness. A credible escalation must retain a rank-dependent cost or add substantive structure.

## 10. Matched comparison and significance

Koehler--Lee--Risteski's COLT 2022 theorem already supplies full-TV sampling and relative partition estimation for approximately low-rank Ising models. For positive semidefinite interactions, its displayed bounds include a factor (n||J||op)^{O(d_++1)}. Its approach uses the Hubbard--Stratonovich transform, grid partitioning and tempering. Therefore none of those task definitions or the Gaussian lift can be claimed as new here.

The proposed advance is replacement of *numerical* dependence on the strength of the positive spikes by dependence on their rational encoding length, at fixed rank and fixed residual gap. A strength of 2^B is a genuine complexity difference between the two displayed guarantees. This is a comparison of guarantees, not a lower bound on the older algorithm and not proof that no later method has obtained the same result.

For homogeneous Curie--Weiss-type cases, grouping by total magnetization already gives an n+1-state computation; this compiler is not a speedup over that elementary specialized representation. Its intended scope includes heterogeneous real/rational pattern columns, arbitrary inconsistent fields, and a correlated high-temperature residual. When the interaction norms are moderate, high-temperature samplers or specialized approximately-low-rank methods may be substantially faster than the present many-cell preprocessing.

The result is a meaningful fixed-rank computational capability candidate, not evidence of a universal Ising solver, a historical breakthrough, or practical superiority. A targeted literature search found the closely related specialized theorem but did not settle priority for this bounded-field construction.

## 11. Reproducibility and exact remaining gates

`verify_compiler.py` checks the constant-resolution envelope on 240 random small fixtures, with 16,732 enumerated spin configurations, and checks full rank-one masses on a four-spin rational fixture for K in {2^-40,1/4,1,16,2^40}. Its 611 cells are independent of K. All assertions passed. The smallest pointwise mean acceptance in those random tests was approximately 0.81517, above the proved universal 0.58410 bound. The rank-one ideal acceptance ranged from about 0.87719 to 0.88239.

`verify_discrete_mixture.py` checks the complete eight-outcome spin law for a three-spin rational fixture at epsilon=1/4. It uses 4,290 cells for each of K=2^-30,1,2^30. Observed TV errors are approximately 4.262e-4,4.209e-8,2.422e-7, respectively. The derived ideal-TV upper bound for that fixture is about 0.03077. Observed absolute log-partition errors are approximately 4.786e-4,1.388e-5,2.422e-7.

`verify_integral_layers.py` separately checks the positive-volume-sum formula on central, far-shifted, thin-interval and narrow-Gaussian rank-one fixtures. It computes one-dimensional sublevel lengths explicitly, not with a generic volume FPRAS. All four checks passed.

The spin programs enumerate the small base state space, use 90-digit mpmath Gaussian interval masses, and are not interval-certified. They do not execute the polynomial base engine or general convex-volume algorithm. They test algebra and small-instance output correctness, not large-scale performance or the full theorem.


A further executable, `rank_one_product_compiler.py`, implements the rank-one, J0=0 mixture without enumerating spin configurations during compilation or sampling. It updates the field arrangement and product partition incrementally. In the captured run, an 8-spin K=1/8 fixture passed a separate exhaustive partition check, with log error about 2.0184e-5. Two 20-spin fixtures at K=1/20 and K=2^60 each used 63,297 cells. Preprocessing took approximately 4.17 and 6.96 seconds, respectively; 256 draws took approximately 0.125 and 0.101 seconds. These are descriptive single-run measurements, not matched performance benchmarks. The strong-coupling mixture was about 9.076e-4 in TV from its two-ground-phase limit; a direct energy bound makes the target's non-ground-state mass negligible on that particular fixture. This especially simple cold limit is not evidence of superiority to a specialized two-phase method.

The first all-mpmath moderate-coupling attempt exceeded both 45-second and 120-second execution caps. The delivered prototype instead uses a hybrid Gaussian interval routine: SciPy double precision at moderate standardized endpoints and mpmath for extreme tails, with 90-digit outer arithmetic. This accelerates the experiment but does **not** implement the theorem's certified, uniform input-bit accuracy contract. It also does not implement general rank or a correlated residual. These failures and distinctions are recorded in `IMPLEMENTATION_LOG.md` and the result files.

Outstanding validation and escalation tasks:

1. Independent proof review of the bounded-field approximation and the rational convex-volume compilation, including degenerate arrangements and numerical error bookkeeping.
2. Implement the generic Gaussian-cell weight engine with certified log errors, replacing exhaustive base enumeration with the stated sampler/annealer or a stronger established engine; benchmark at matched TV/log-partition tolerance against specialized methods.
3. Resolve historical priority beyond the targeted search.
4. For a substantially broader computational consequence, investigate whether the cell-weight distribution admits f(r) poly(n,B,epsilon^{-1}) acquisition, or comparably efficient aggregation on a precisely specified structured growing-rank class, while retaining the same discrete output guarantee. Parameterized hardness must also be checked; such an improvement is not assumed possible. This is the exact mathematical obstruction to high-rank escalation in the current representation. Simply refining the grid does not address it.

No repository changes were made by this run. The archive is a local handoff, not a published checkpoint.

## References and provenance

1. F. Koehler, H. Lee, A. Risteski, *Sampling Approximately Low-Rank Ising Models: MCMC meets Variational Methods*, COLT 2022, PMLR 178:4945--4988. Theorem 1.1 (matched sampling/counting baseline), Theorem 1.2 (negative rank-one hardness), Lemma 2.2 (Gaussian transform). https://proceedings.mlr.press/v178/koehler22a.html ; https://proceedings.mlr.press/v178/koehler22a/koehler22a.pdf
2. R. Eldan, F. Koehler, O. Zeitouni, *A Spectral Condition for Spectral Gap: Fast Mixing in High-Temperature Ising Models*, PTRF 182 (2022), 1035--1051. Theorem 1. https://arxiv.org/abs/2007.08200 ; https://arxiv.org/pdf/2007.08200
3. M. Dyer, A. Frieze, R. Kannan, *A Random Polynomial-Time Algorithm for Approximating the Volume of Convex Bodies*, JACM 38(1) (1991), 1--17. DOI 10.1145/102782.102783. Author-hosted manuscript inspected, especially well-guaranteed oracle rounding and discrete grid implementation: https://www.math.cmu.edu/~af1p/Texfiles/oldvolume.pdf
4. R. Kannan, L. Lovasz, M. Simonovits, *Random walks and an O*(n^5) volume algorithm for convex bodies*, Random Structures & Algorithms 11 (1997), 1--50. DOI 10.1002/(SICI)1098-2418(199708)11:1<1::AID-RSA1>3.0.CO;2-X. Stronger convex-volume machinery; not essential to the conservative bound.
5. Y. Kook, S. Vempala, *Sampling and Integration of Logconcave Functions by Algorithmic Diffusion*, arXiv:2411.13462. An alternative, more sophisticated integration route considered, not needed by the positive-volume-sum proof. https://arxiv.org/abs/2411.13462
6. G. Park, N. Ng, D. R. Reichman, G. K.-L. Chan, *Tensor network influence functionals in the continuous-time limit*, arXiv:2401.12460. Screening context, not a proof dependency. https://arxiv.org/abs/2401.12460
7. Astra research memory: https://github.com/harjassand/astra-research-knowledge/tree/f12638af678bb8f3cc4039f10de78a55476a3a0c ; OpenAI mathematics catalogue: https://github.com/openai/math . Only selected routes were inspected. No new theorem in this note depends on an unverified repository claim.

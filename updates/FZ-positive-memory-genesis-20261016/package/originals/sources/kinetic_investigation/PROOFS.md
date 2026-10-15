# Committor accuracy, path likelihood, and kinetic work

Research note, 16 October 2026. Derived in this invocation. Historical originality and independent mathematical review are unresolved. Standard importance-sampling and Markov-chain machinery is explicitly credited below. This note is not a claim to have solved an empirical scientific problem.

## 1. The question being tested

Suppose a learned positive approximation to a hitting probability is uniformly accurate in relative error. Does turning it into a biased trajectory generator give a uniformly reliable rare-event estimator, without reconstructing the full evolving probability distribution?

The answer is no over unrestricted finite kinetic networks. Two independent obstructions are likelihood-moment instability and the cost of generating long successful trajectories. The results below concern eventual hitting before absorption, unless a finite horizon is explicitly stated. They do NOT establish infinite variance for the separate eight-site, finite-horizon splitting experiment.

## 2. Exact second-moment operators

Let a finite continuous-time Markov chain have transient states C and absorbing states A (failure), B (success). Write q_ij for off-diagonal original rates, q_i for their total, and r_ij, r_i for proposal rates. The proposal must support every successful original trajectory. Removing all edges into A is allowed when estimating success, as long as the original successful-path measure is absolutely continuous with respect to the proposal. Let W be its likelihood-ratio estimator.

A successful trajectory with holding times t_l and jumps i_l -> i_(l+1) has original density proportional to the product of q_ij exp(-q_i t), and proposal density proportional to the analogous product with r. Its contribution to the proposal second moment is the original density squared divided by the proposal density. Consequently define

\[
M_{ij}=q_{ij}^2/r_{ij}\quad(i\ne j),\qquad
M_{ii}=r_i-2q_i,\qquad b_i=q_{iB}^2/r_{iB}.
\]

Then

\[
\mathbb E_{r,i}W^2=\int_0^\infty (e^{Mt}b)_i\,dt.
\]

This follows by integrating the density over each holding time and summing successful path skeletons, or equivalently by the first-jump renewal equation. M is Metzler, not a Markov generator. If M is irreducible and b is strictly positive, this integral is finite exactly when its spectral abscissa is negative. To see the divergent direction, a strictly positive left Perron eigenvector turns the integral into a positive multiple of the integral of exp(alpha(M)t). Irreducibility then propagates divergence to every starting state. In the stable case the integral is -M^{-1}b.

For a discrete-time or embedded chain with original transition probabilities P and proposal probabilities R, the corresponding operator is

\[
K_{ij}=P_{ij}^2/R_{ij},\qquad b_i=P_{iB}^2/R_{iB},\qquad
\mathbb E_R W^2=\sum_{n\ge0}K^n b.
\]

With the same irreducibility and positivity conditions, the moment is finite exactly when rho(K)<1. These operators are established machinery, not the proposed novelty of this note. See Kuruganti and Strickland (1996).

## 3. A sharp two-state continuous-time example

Take two transient states with q_12=q_21=1. From each state, exit to B at rate kappa*p and to A at rate kappa*(1-p), where kappa>0 and 0<p<1. Both exact committors equal p: terminal absorption happens at a state-independent total rate kappa, with state-independent success fraction p.

For 0<delta<1 and p<=1/(1+delta), set

\[
\hat h_1=p(1+\delta),\qquad\hat h_2=p(1-\delta),\qquad
\hat h_B=1,\quad\hat h_A=0.
\]

The relative committor error is exactly delta. Use the ordinary approximate Doob prescription r_ij=q_ij hhat_j/hhat_i. Thus

\[
r_{12}=\frac{1-\delta}{1+\delta},\quad
r_{21}=\frac{1+\delta}{1-\delta},\quad
r_{1B}=\frac{\kappa}{1+\delta},\quad
r_{2B}=\frac{\kappa}{1-\delta}.
\]

There are no proposed failure exits. This finite proposal chain hits B almost surely and has finite expected duration. W is nevertheless capable of having infinite second moment.

For its second-moment matrix,

\[
\det M=\frac{(\kappa+2)[\kappa-4(\kappa+1)\delta^2]}{1-\delta^2},
\]

\[
\operatorname{tr}M=\frac{-2-2\kappa+(6+4\kappa)\delta^2}{1-\delta^2}.
\]

The off-diagonal entries are positive, so both eigenvalues are real. When delta^2<kappa/[4(1+kappa)], the determinant is positive and the trace is negative. At equality the larger eigenvalue is zero. Above equality the determinant is negative and the larger eigenvalue is positive. Therefore

\[
\boxed{\mathbb E_rW^2<\infty\iff
\delta^2<\frac{\kappa}{4(1+\kappa)}.}
\]

At kappa=10^-6, delta=0.01 and p=10^-12, the unbiased estimator has infinite variance despite a one-percent uniform relative committor approximation. Its second-moment spectral abscissa is approximately 0.000399040304, used only as an illustration: the determinant identity gives the exact conclusion. For any fixed nonzero relative error, sufficiently long trapping causes failure. Arbitrarily small delta can fail; there is no positive uniform error threshold independent of kappa.

This does not contradict zero variance at the exact committor. It says the neighborhood around that optimum can collapse as trapping becomes longer.

## 4. Clock removal repairs this example, not the general problem

For eventual hitting probabilities, the holding times can be integrated out. The original embedded-chain transition between the two transient states is 1/(1+kappa), and its success probability is kappa*p/(1+kappa). Normalizing the approximate Doob routing gives

\[
R_{12}=\frac{1-\delta}{1-\delta+\kappa},\quad
R_{21}=\frac{1+\delta}{1+\delta+\kappa}.
\]

The squared spectral radius of the embedded second-moment matrix is

\[
\rho(K)^2=\frac{(1+\kappa)^2-\delta^2}
{(1+\kappa)^4(1-\delta^2)}.
\]

After factoring the numerator of 1-rho(K)^2,

\[
\boxed{\mathbb E_R W^2<\infty\iff
\delta^2<\frac{(1+\kappa)^2}{(1+\kappa)^2+1}.}
\]

The allowed squared error tends to 1/2 rather than zero. Solving the two linear second-moment equations also yields, for either starting state,

\[
\lim_{\kappa\downarrow0}\frac{\mathbb E_R W^2}{p^2}
=\frac{1-\delta^2}{1-2\delta^2},\quad\delta^2<1/2.
\]

For the numerical parameters above, the normalized second moment is about 1.0001000199 instead of infinity. This is a valid repair, but embedded-chain conditioning is longstanding prior art. It is not a new operation. For a finite physical deadline one cannot simply discard elapsed holding times; they must be retained or integrated with the deadline constraint.

## 5. A sharp branching example defeats clock removal

Replace the two transient states by a triangle: q_ij=1 for each distinct pair i,j in {1,2,3}, with the same exit rates kappa*p and kappa*(1-p). Again h_i=p. Use relative multipliers a=(1+delta,1,1-delta), and normalize the approximate Doob rates to an embedded chain.

For i!=j the second-moment operator is

\[
K_{ij}=\frac{\sum_{\ell\ne i}a_\ell+\kappa}{(2+\kappa)^2a_j},\qquad K_{ii}=0.
\]

Its determinant at the stability boundary factors exactly:

\[
\det(I-K)=\frac{(\kappa+3)^2
[\kappa(\kappa+2)^2-(\kappa^3+4\kappa^2+7\kappa+4)\delta^2]}
{(\kappa+2)^5(1-\delta^2)}.
\]

A strictly positive off-diagonal, zero-diagonal 3x3 matrix has characteristic polynomial x^3-Ax-B with A,B>0. There is exactly one positive root by Descartes' rule, and that root is the Perron root. Accordingly the sign of det(I-K) decides whether this positive root lies below or above one. Thus

\[
\boxed{\mathbb E_R W^2<\infty\iff
\delta^2<\frac{\kappa(\kappa+2)^2}
{\kappa^3+4\kappa^2+7\kappa+4}.}
\]

The critical squared error is asymptotic to kappa. At kappa=10^-6 and delta=0.01, variance is infinite even after all holding times have been removed. As an additional exact certificate, take

\[
v=(100000017/100000000,\ 125006261/125000000,\ 1)^T.
\]

The script verifies K v-v>0 coordinatewise using rational arithmetic. The displayed floating Perron root, 1.0000495037255566, is not needed for that conclusion. The positive boundary source makes the second moment diverge from every transient starting state.

The difference from the two-state example is genuine routing uncertainty: the triangle offers two distinct possible destinations, whose relative probabilities the inaccurate committor changes. A two-state alternating path has no such internal choice.

## 6. General routing-instability theorem

Let S be an irreducible finite row-stochastic matrix with zero diagonal. Regard S_ij as continuous-time internal rates, so the total internal rate is one at each state. Add state-independent success and failure exits of rates kappa*p and kappa*(1-p). Let a>0 and hhat_i=p*a_i, with p small enough that hhat_i<=1. The exact committor is p.

After approximate Doob tilting and clock removal,

\[
R^{\kappa}_{ij}=\frac{S_{ij}a_j}{(Sa)_i+\kappa},\quad
R^{\kappa}_{iB}=\frac{\kappa}{(Sa)_i+\kappa},
\]

\[
K^{\kappa}_{ij}=\frac{S_{ij}[(Sa)_i+\kappa]}{(1+\kappa)^2a_j}.
\]

Suppose some state i has two possible internal destinations j,l with a_j!=a_l. Then the clock-marginalized likelihood estimator has infinite variance for every sufficiently small positive kappa.

**Proof.** At kappa=0,

\[
(K^0\mathbf1)_i=(Sa)_i\sum_j S_{ij}/a_j\ge1
\]

by Cauchy-Schwarz. Equality holds exactly when a is constant on the support of that row. The hypothesis gives strict inequality in at least one row. K^0 is irreducible and has a strictly positive left Perron vector ell. Therefore

\[
\rho(K^0)\ell^T\mathbf1
=\ell^TK^0\mathbf1>\ell^T\mathbf1,
\]

so rho(K^0)>1. Spectral continuity implies rho(K^kappa)>1 for all sufficiently small kappa>0. The success source is strictly positive, proving divergence. The proposed finite chain still absorbs almost surely because every state's success probability is positive. Hence this is a variance failure, not failure to terminate. QED.

This proves the obstruction for arbitrary internal topology satisfying the branching condition, rather than relying only on one three-state fixture.

### Local error-versus-escape law

Let a=1+delta*f, with fixed S and f, and let pi be S's stationary distribution. Write

\[
\sigma_S^2(f)=\sum_i\pi_i\left[(Sf^2)_i-(Sf)_i^2\right]
=\sum_i\pi_i\operatorname{Var}_{j\sim S(i,\cdot)}f_j.
\]

Analytic perturbation of the simple eigenvalue one gives

\[
\rho(K^{\kappa,\delta})
=1-\kappa+\delta^2\sigma_S^2(f)
+O(\kappa^2+\kappa|\delta|+|\delta|^3).
\]

For completeness: at kappa=0 the row sum expands as

\[
(1+\delta Sf)_i\left[S\left(\frac1{1+\delta f}\right)\right]_i
=1+\delta^2[(Sf^2)_i-(Sf)_i^2]+O(\delta^3).
\]

Thus the first-order matrix perturbation annihilates the right eigenvector 1. The first eigenvector correction can be normalized to zero, and the second eigenvalue coefficient is pi times the displayed second-order row coefficient. At delta=0, K=S/(1+kappa), giving derivative -1 in kappa. This proves the expansion. The constants are for fixed S,f; no dimension- or mixing-gap-uniform remainder is asserted.

When sigma_S^2(f)>0, the implicit-function theorem gives a local critical escape scale

\[
\kappa_{\rm crit}(\delta)=\sigma_S^2(f)\delta^2+O(|\delta|^3).
\]

For the triangle with internal total rate normalized to one, f=(1,0,-1), sigma^2=1/2. Restoring internal total rate two recovers the exact triangle's kappa_crit~delta^2. For deterministic alternating routing, sigma^2=0 and this particular second-order obstruction disappears. Neither statement grants an efficient way to acquire pi or the committor.

## 7. Even finite variance is not complete work accounting

Let P* be the original full trajectory distribution conditioned on success, whose probability is p>0. Let Q be any proposal supporting P*, and W=p*dP*/dQ. Let C>=1 be the actual cost of explicitly producing that trajectory, such as its number of simulated primitive jumps. Then

\[
\boxed{\mathbb E_Q C\;\frac{\mathbb E_Q W^2}{p^2}
\ge \left(\mathbb E_{P^*}\sqrt C\right)^2.}
\]

**Proof.** The right-hand square root expectation equals E_Q[sqrt(C) W/p]. Apply Cauchy-Schwarz. Infinite expectations are interpreted in the extended sense; the finite case immediately yields the inequality. QED.

For C>0 and integrable C^(1/2) and C^(-1/2) under P*, the bound is sharp over unrestricted full-path proposals: use dQ/dP* proportional to C^(-1/2). This proposal is only a mathematical optimizer. Acquiring and sampling it is not free and need not be implementable by a simple Markov policy.

In the two-state example, successful trajectories have jump count N distributed geometrically on {1,2,...} with termination probability q=kappa/(1+kappa). Consequently E N=(1+kappa)/kappa and

\[
\left(\mathbb E\sqrt N\right)^2\sim\frac\pi{4q}
=\frac{\pi(1+\kappa)}{4\kappa}.
\]

To justify the asymptotic, qN converges in distribution to an Exp(1) variable. The square roots are uniformly integrable since E(qN)=1 and E[sqrt(qN) 1_{sqrt(qN)>R}]<=1/R. Hence E sqrt(qN)->Gamma(3/2)=sqrt(pi)/2.

Any bounded-normalized-second-moment proposal that explicitly generates every successful path must therefore retain expected per-path work of order 1/kappa. A perfect committor removes rarity variance, but not these primitive jumps.

**Important limitations.** The inequality uses the normalized SECOND MOMENT, not just variance. It is not a lower bound for every estimator, for control variates, for analytic solvers, or for algorithms that integrate out paths. It is not a total sample-complexity theorem and says nothing by itself about the cost of acquiring the input model. Exact zero-variance output can be obtained trivially when the answer is already known; the oracle cost must not be concealed. The Cauchy-Schwarz principle is elementary, and cost-aware importance sampling has prior literature.

## 8. A different operation: contract entire excursions

For a transient block C of a known finite generator Q, let Q_C,partialC collect its exit rates. The joint exit-time and destination density is

\[
H_C(t)=e^{Q_{CC}t}Q_{C,\partial C}.
\]

Its Laplace transform is

\[
F_C(s)=(sI-Q_{CC})^{-1}Q_{C,\partial C},\qquad s\ge0,
\]

provided C is transient at s=0. This follows by integrating the finite-dimensional semigroup. It preserves timing, unlike merely discarding clocks. It also sums arbitrary internal recrossings without simulating them individually.

For our examples, Q_CC=G-kappa I with G1=0, and the success exit column is kappa*p*1. Thus

\[
F_{C,B}(s)=\frac{\kappa p}{s+\kappa}\mathbf1,
\]

so the success probability is exactly p, the exit time is Exp(kappa), and success-by-T is p(1-exp(-kappa T)). The script checks this identity on a nonuniform three-state internal generator as well as the symmetric examples.

This defeats both of our deliberately small adversarial examples with ordinary algebra. That is an essential strongest-incumbent check: the examples are NOT intrinsically difficult computational problems. They prove that an alleged uniform guarantee for an algorithm family is false. Block resolvents, lumpability, phase-type laws and graph transformation are existing operations; see Trygubenko and Wales (2006), Woods et al. (2023), and Woods and Wales (2024).

For a huge reaction configuration graph, writing this resolvent does not establish efficient access to it. Explicitly forming every state, inverting a dense matrix, learning only typical exits, or certifying absolute errors much larger than a rare exit probability would each fail the intended scientific task. No compressed, acquisition-complete, relatively accurate excursion operator for the full eight-site model was constructed here.

## 9. Scientific and novelty boundaries

The full spatial benchmark and the exact small-network theorems are different parts of the investigation. The small models diagnose an algorithmic assertion; they do not replace the spatial simulation or establish its conditional trajectory law. Finite-state fixed-horizon likelihood estimators have finite second moments under positive bounded rates, even when the eventual-hitting moment diverges. No infinite-variance claim is made for fixed-horizon splitting, and the observed replicate dispersion is not attributed to the preceding likelihood instability.

General sensitivity of importance sampling to inaccurate proposals is already studied by Hartmann and Richter (2024). Hartmann, Jöster, Schütte, Sikorski and Weber's September 2026 revision specifically addresses unbounded stopping times, trajectory duration, and formulations without long likelihood reweighting. The general observation that variance and duration both matter is not new. The exact thresholds, branching criterion and perturbative coefficient are the scoped derivations retained here; priority is not cleared. No strongest-method advantage on a consequential calibrated scientific system is established.

## References

1. I. Kuruganti and S. Strickland, *Importance Sampling for Markov Chains: Computing Variance and Determining Optimal Measures*, Winter Simulation Conference (1996), https://www.informs-sim.org/wsc96papers/036.pdf.
2. C. Hartmann and L. Richter, *Nonasymptotic Bounds for Suboptimal Importance Sampling*, SIAM/ASA J. Uncertainty Quantification (2024), arXiv:2102.09606, https://arxiv.org/abs/2102.09606.
3. C. Hartmann, A. Jöster, C. Schütte, A. Sikorski and M. Weber, *Importance sampling with unbounded random stopping times: computing committor functions and exit rates without reweighting*, arXiv:2601.01489v2 (4 September 2026), https://arxiv.org/html/2601.01489v2.
4. S. A. Trygubenko and D. J. Wales, *Graph Transformation Method for Calculating Waiting Times in Markov Chains*, J. Chem. Phys. 124, 234110 (2006), https://arxiv.org/abs/cond-mat/0603830.
5. E. J. Woods et al., *Analysing ill-conditioned Markov chains* (2023), https://pmc.ncbi.nlm.nih.gov/articles/PMC10200351/.
6. E. J. Woods and D. J. Wales, *Analysis and interpretation of first passage time distributions featuring rare events*, PCCP 26, 1640–1657 (2024), https://pubmed.ncbi.nlm.nih.gov/38059562/.
7. V. Waeselynck et al., cost-optimized importance-sampling study, Fire 7(12),455 (2024), https://www.mdpi.com/2571-6255/7/12/455. Search located a cost-aware prior; full-text retrieval returned HTTP 429, so no exact theorem comparison was completed.

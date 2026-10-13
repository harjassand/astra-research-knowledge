# ASTRA FRONTIER — Finite-dependency sampling of a nonlinear collision law

**Date:** 13 October 2026.  
**Status:** Research construction with proofs and executed numerical diagnostics. Historical novelty and independent correctness have not been established. The exact-sampling theorem is an ideal-arithmetic theorem, not a certification of the floating-point executable. No civilization-scale technological capability is claimed.

## 1. Scientific question and result

Can a particle velocity at a specified, arbitrarily large collision time be generated without constructing its exponentially large collision ancestry, without substituting equilibrium, and without a time or series truncation?

This note gives an affirmative construction for a restricted family: the normalized, spatially homogeneous, isotropic-cutoff Maxwell collision equation in three dimensions, initialized by a centered Gaussian scale mixture with scalar variance supported in a known interval [a,b]. For the exact rejection construction, 0<a<b<3a/2. Only independent draws from the initial mixing distribution are required; its moments, its evolved law and its equilibrium mean are not supplied.

The operation has three parts:

1. An order-k query is evaluated using a shared marked genealogy with at most k-1 effective splits, independently of elapsed time.
2. A randomized Laguerre expansion converts this finite dependency into a globally bounded, signed estimator of a density ratio.
3. Huber's existing linear Bernoulli factory converts that signed estimator into an exact rejection decision, with an explicitly integrable expected-work bound.

The third component is credited prior work, not an invented Bernoulli factory. The candidate contribution is the particular combination and its all-time sampling bound. Priority remains unresolved. For arbitrary 0<a<b, a simpler full-distribution approximation has a time-uniform total-variation error of order 1/n with at most n-1 effective splits per output.

These are actual sampling constructions rather than energy-monotonicity certificates. Nevertheless, the initial-data and collision restrictions are substantial, and strong existing deterministic moment methods perform very well in this family. The results do not establish a new general-purpose molecular simulator or the original civilization-changing objective.

## 2. Input, output and cost contract

Inputs are a finite t>=0, known constants 0<a<b, and a procedure producing independent V_0 with law nu_0 supported in [a,b]. Let c_0 bound the expected cost of an initial draw. The explicit finite mixtures used in the executable satisfy this contract. Arbitrary measured gas data do not automatically provide this latent-variable sampler or a certificate that this representation is correct.

The target is one velocity with the one-particle density f_t. Independent executions give independent one-particle samples. This does not produce a correlated N-particle state, a physical particle trajectory, a path-dependent reaction event, or a spatial transport solution.

The main cost result counts ideal real-arithmetic operations, initial draws, and standard random primitives, including Bernoulli-factory work. It is uniform in the numerical value of t. Reading the input, representing t, variable-precision arithmetic, exact real comparisons and production of finite output bits are separate costs. Worst-case runtime is unbounded; the theorem is about expected work.

## 3. Collision model and scalar closure

Write

\[
G_s(v)=(2\pi s)^{-3/2}\exp[-|v|^2/(2s)],\qquad
f_0(v)=\int_a^bG_s(v)\,\nu_0(ds).
\]

We fix the normalized Fourier collision equation

\[
\partial_t\phi_t(k)=\int_{S^2}
\{\phi_t(k^+)\phi_t(k^-)-\phi_t(k)\}\,\frac{d\sigma}{4\pi},
\qquad k^\pm=(k\pm |k|\sigma)/2.
\]

This is the constant-rate, isotropic-cutoff Maxwell model. The normalization sets one unit of time to the corresponding mean collision-time scale. Maxwell collision models and their moment hierarchies are prior work [1,2].

For radial scale mixtures, let z=|k|^2/2. Since |k^+|^2+|k^-|^2=|k|^2 and (1+cos(theta))/2 is uniform on [0,1] under uniform three-dimensional angular measure, the equation closes as

\[
\phi_t(k)=\mathbb E e^{-zV_t},\qquad
\partial_t\nu_t=\mathcal Q(\nu_t,\nu_t)-\nu_t,
\]

where Q(nu,nu) is the law of B V_1+(1-B)V_2 for independent V_1,V_2~nu and B~Uniform[0,1]. Convex averaging preserves [a,b]. The bilinear map is Lipschitz on probability measures in total variation, giving uniqueness for this bounded-measure evolution by its integral equation. Thus the scalar mixing law determines the specified collision solution.

V_t is a latent mixing variable, not the time history of one physical particle's temperature. The construction is a distributional representation.

A backward realization branches each active lineage at rate one. At a split it attaches weights B and 1-B. At time zero it draws independent initial variances. The root variance is

\[
V_t=\sum_{j=1}^{N_t}w_jV_{0,j},\qquad \sum_jw_j=1.
\]

The complete binary genealogy has E N_t=e^t in this normalization. Enumerating this particular exact representation is expensive at large t. This is not a lower bound on every solver.

## 4. Finite marked genealogy theorem

Normalize P_t=(b-V_t)/(b-a) in [0,1], and let m_k(t)=E P_t^k. Then

\[
m_0=1,\quad m_1'=0,\qquad
m_k'=-\frac{k-1}{k+1}m_k+\frac1{k+1}\sum_{j=1}^{k-1}m_jm_{k-j}
\quad(k\ge2).
\]

Indeed, the coefficient of m_j m_{k-j} in the gain term is

\[
\binom kj\int_0^1 u^j(1-u)^{k-j}\,du=\frac1{k+1}.
\]

### Algorithm

Start with a block containing k marks and remaining horizon t. A block of size one is terminal. A block of size q>=2 waits an exponential time with rate (q-1)/(q+1). If its waiting time exceeds its remaining horizon, it is terminal. Otherwise choose j uniformly from 1,...,q-1 and replace it by two independent descendants with sizes j and q-j and the same reduced horizon. At each terminal block of size q draw a fresh P_0, and multiply P_0^q across blocks. For k=0 return one.

Call the product H_{k,t}.

### Theorem 1

For every k>=0 and t>=0,

\[
0\le H_{k,t}\le1,\qquad \mathbb EH_{k,t}=m_k(t).
\]

For k>=1 the procedure has at most k-1 effective splits, at most 2k-1 visited nodes and at most k initial draws. Its arithmetic cost can be implemented as O(1+k), independently of t.

### Proof

Conditioning on the first effective split gives exactly the triangular differential equation displayed above and the initial value E P_0^k. The terminal product is bounded by one. Induction in k and uniqueness of the scalar inhomogeneous linear equations prove equality of expectations. Each effective split increases the number of positive-size blocks by one while their sizes sum to k. There can therefore be at most k-1 splits. A full binary tree with at most k terminal nodes has at most 2k-1 nodes. Evaluating all powers by repeated multiplication uses at most k multiplications in total. This proves the work bound.

There is also a useful coupling interpretation. Put k independent mass-biased marks on the leaves of the complete weighted genealogy. At a binary split, integrating the binomial allocation against uniform B makes the mark count uniform on {0,...,k}. Cases 0 and k do not separate any marks and can be integrated out. The effective separation rate is (k-1)/(k+1). A singleton never needs its unobserved future ancestry. Crucially, the marks share one genealogy; replacing them by k independent initial draws gives the wrong law.

## 5. Bounded unbiased observable estimators

For z>=0, draw K~Poisson(z(b-a)) and return

\[
Y_z=e^{-az}H_{K,t}.
\]

Then E Y_z=E e^{-zV_t}, 0<=Y_z<=e^{-az}, and E K=z(b-a). This follows by expanding exp(z(b-a)P_t). There is no time cutoff or random series truncation bias. The estimate is for an absolute characteristic-function query; it does not supply a uniform relative-error algorithm for rare events.

A density query follows by randomized Fourier inversion. Draw xi~N(0,a^{-1}I_3), set z=|xi|^2/2, draw K conditionally Poisson((b-a)z), and return

\[
Z_v=(2\pi a)^{-3/2}\cos(\xi\cdot v)H_{K,t}.
\]

Gaussian integrability justifies Fubini, and Fourier inversion gives E Z_v=f_t(v). Its absolute value is at most (2pi a)^(-3/2), while E K=3(b-a)/(2a). This is a signed density estimate, not a positive density and not yet a sample. The distinction motivates the next construction.

## 6. Exact sampling in ideal arithmetic

Assume 0<a<b<3a/2. Choose

\[
r=1-a/b,\quad r<\rho<2a/b-1,\quad g=b(1+\rho),
\]

and define

\[
C=\frac{((1+\rho)/(1-\rho))^{3/2}}{1-r/\rho},\qquad
I=\left[\frac{ab}{g(2a-g)}\right]^{3/2}.
\]

The interval for rho is nonempty precisely under this sufficient bracket condition, and g<2a. Let q=G_g be the proposal density.

### 6.1 A bounded signed relative-density estimator

The generalized Laguerre generating function is a standard identity [3]:

\[
(1-u)^{-3/2}\exp[-xu/(1-u)]
=\sum_{k=0}^\infty L_k^{1/2}(x)u^k.
\]

With x=|v|^2/(2b), it gives

\[
f_t(v)=G_b(v)\sum_{k=0}^\infty r^kL_k^{1/2}(x)m_k(t).
\]

For |u|=rho, |1-u|>=1-rho and

\[
\min_{|u|=\rho}\Re\frac{u}{1-u}=-\frac{\rho}{1+\rho}.
\]

Cauchy's coefficient estimate consequently gives

\[
|\rho^kL_k^{1/2}(x)|\le(1-\rho)^{-3/2}
\exp[x\rho/(1+\rho)].
\]

This also proves absolute convergence after multiplying by r^k, since r<rho and 0<=m_k<=1.

Draw K with P(K=k)=(1-r/rho)(r/rho)^k for k=0,1,..., and draw an independent H_{K,t}. Define

\[
W(v)=\frac{G_b(v)}{G_g(v)}
\frac{\rho^K L_K^{1/2}(x)H_{K,t}}{1-r/\rho}.
\]

The geometric law cancels the randomized-series weights, so

\[
\mathbb EW(v)=R(v):=f_t(v)/G_g(v).
\]

Since G_b/G_g=(1+rho)^(3/2) exp[-x rho/(1+rho)], the exponential factors in the coefficient bound cancel exactly. Thus

\[
|W(v)|\le C
\]

for every v and t, not merely on a finite grid. The average query degree is E K=r/(rho-r).

### 6.2 Exact acceptance using an existing Bernoulli factory

Every s in [a,b] satisfies G_s(v)>=(a/b)^(3/2) G_a(v). Therefore

\[
R(v)\ge\ell(v):=(g/b)^{3/2}
\exp[-|v|^2(1/a-1/g)/2]>0.
\]

A fresh W(v), followed by an independent uniform random variable, supplies a coin of mean

\[
p(v)=\frac{1-R(v)/C}{2}
\]

by using the conditional probability (1-W(v)/C)/2. Although W is signed, this conditional probability lies in [0,1]. We have

\[
2p(v)\le1-\ell(v)/C.
\]

Huber's linear Bernoulli factory [4] takes independent p-coins and a known positive margin epsilon with A p<=1-epsilon, and returns an A p-coin using at most 9.5 A/epsilon input coins in expectation. This is a load-bearing imported theorem. Applying it with A=2 and epsilon=ell(v)/C, then complementing its output, gives an acceptance coin with mean R(v)/C.

Propose v~G_g, make this acceptance decision, and repeat on rejection. The accepted density is proportional to

\[
G_g(v)\frac{f_t(v)}{C G_g(v)}=f_t(v)/C.
\]

Since f_t integrates to one, the proposal acceptance probability is 1/C and the output law is exactly f_t in the ideal model. No deterministic approximation tolerance is present.

### 6.3 Integrated expected work

The expected number of signed-estimator calls conditional on one proposal v is at most 19 C/ell(v). Moreover,

\[
\int_{\mathbb R^3}\frac{G_g(v)}{\ell(v)}\,dv
=\left[\frac{ab}{g(2a-g)}\right]^{3/2}=I<\infty.
\]

The Gaussian integral is finite because g<2a. Independent proposal cycles form a renewal experiment with success probability 1/C. Consequently:

### Theorem 2

Under the stated model and input contract,

\[
\boxed{\sup_{t\ge0}\mathbb E N_{\mathrm{signed}}\le19C^2I.}
\]

The expected number of proposals is C. With initial-draw expected cost at most c_0, an ideal-arithmetic implementation has

\[
\mathbb E[\mathrm{work}]
=O\!\left(C+19C^2I\left[1+\frac r{\rho-r}\right](1+c_0)\right),
\]

uniformly in t. The three-term Laguerre recurrence costs O(K), as does the marked genealogy. Each stage of the published Bernoulli-factory repeat-until algorithm makes at least one input-coin call, so its auxiliary arithmetic is charged as well. Integer and real bit lengths are not treated as unit-free physical resources; they remain outside this ideal-operation bound.

The cost of a query can be correlated with its outcome. This does not invalidate the expectation bound: the event that a fresh query is requested depends only on preceding outcomes. Conditional on the proposal, each newly requested query has the same mean degree and fresh randomness. Summing nonnegative costs, or applying the corresponding stopping-time identity, justifies the accounting. The same renewal argument accounts for the correlation between a proposal's cost and its eventual acceptance.

The condition b<3a/2 is sufficient for this envelope and integrated-cost proof. It is not an impossibility theorem for wider temperature distributions.

## 7. A broader bounded-error full sampler

For any 0<a<b, start n marks. Let terminal block sizes be q_j, draw independent V_{0,j}, and set

\[
\widehat V_{n,t}=\frac1n\sum_jq_jV_{0,j},\qquad
\widehat X_{n,t}\mid\widehat V_{n,t}\sim N(0,\widehat V_{n,t}I_3).
\]

Every execution uses at most n-1 effective splits. To analyze the law, condition on the complete weighted genealogy and its initial leaf variances. The n marks then select leaves independently by weights. Their empirical average is conditionally unbiased for V_t. Also

\[
\operatorname{Var}(V_t)=e^{-t/3}\operatorname{Var}(V_0),
\]

by the second-moment equation, so

\[
\mathbb E(\widehat V_{n,t}-V_t)^2
=\frac{\operatorname{Var}(V_0)(1-e^{-t/3})}{n}.
\]

For the Gaussian kernel, with U=|v|^2/s,

\[
\partial_s^2G_s(v)=\frac{G_s(v)}{4s^2}(U^2-10U+15).
\]

Under G_s, U has the chi-square law with three degrees of freedom and E(U^2-10U+15)^2=120. Hence

\[
\|\partial_s^2G_s\|_1\le\sqrt{15/2}/s^2.
\]

Taylor expansion about V_t cancels the first-order term after conditional expectation. Integrating the remainder and using TV=half the L1 distance yields

\[
\boxed{
 d_{\mathrm{TV}}(\mathcal L(\widehat X_{n,t}),f_t)
 \le\frac{\sqrt{15/2}}{4a^2n}\operatorname{Var}(V_0)(1-e^{-t/3})
 \le\frac{\sqrt{15/2}}{16n}\left(\frac{b-a}{a}\right)^2.}
\]

The bound is exact in its independence from elapsed time, but it is not a claim of a sharp constant. At t=0 all marks share one initial draw, and the output law is exact. At very large t, the residual mixing variance of this approximation is Var(V_0)/n. One must not mistake this approximate sampler for Theorem 2's rejection construction.

### Initial-data robustness

If two supplied mixing laws on the same [a,b] differ by at most eta in Wasserstein-1 distance, use a common genealogy and coupled initial draws. Convex averaging gives E|V_t-tilde V_t|<=eta for all t. Since ||partial_s G_s||_1<=sqrt(3/2)/s,

\[
d_{\mathrm{TV}}(f_t,\widetilde f_t)\le\frac{\sqrt{3/2}}{2a}\eta.
\]

This charges a specified initial mixing-law error. It does not solve recovery of that law from measured velocities or errors in the collision model.

## 8. Executed diagnostics

All checks use fixed seeds and floating-point arithmetic. They are finite consistency tests, not general proof validation or exact-real certification. The JSON files record all reported cases, including deviations exceeding two standard errors; no pass claim is based on every sample lying in a nominal 95% interval.

### Broad-family tests: a=1, b=3, equal endpoint weights

An independently coded triangular moment ODE through degree 96 was solved by DOP853 at times 0,1,3,10,30,100. It took about 0.012 seconds in the recorded run and matched the analytic second moment to 3.61e-15. This is a strong, very inexpensive deterministic comparator, not evidence of sampler dominance.

A finite-state partition generator at n=8,t=3 supplied a separate matrix-exponential reference. Across 32,000 marked-tree draws the empirical PMF had TV discrepancy 0.004461 from that finite reference. This number is sampling error against the finite reference, not TV against the Boltzmann solution.

Numerical radial integration of the full approximate output law against the moment/Laguerre reference at t=3 gave:

| n | Numerical TV | Uniform proven upper bound |
|---:|---:|---:|
| 1 | 0.0737363 | 0.684653 |
| 2 | 0.0373629 | 0.342327 |
| 4 | 0.0185434 | 0.171163 |
| 8 | 0.00921596 | 0.0855816 |
| 16 | 0.00459200 | 0.0427908 |

The analytic truncation contribution in this reference is bounded separately, but the ODE and quadrature are not interval-certified. The approximately 1/n behavior is consistent with the proof, not its justification.

At n=64, no execution exceeded 63 splits or 127 nodes. The mean split count increased from zero at t=0 to 63 at t=100 and t=10^6. For these parameters the uniform ideal-law TV bound is 0.0106977. A negative control that incorrectly used independent initial draws for all marks at t=0 produced latent variance 1/64 rather than the correct value 1.

### Exact-extension tests: a=1, b=1.1, rho=0.2

Here g=1.32, C=3.3680484, I=1.35664045, E K=5/6, and the theorem bounds the expected signed-estimator calls per output by 292.3985 for every t.

The final executable was aligned with the initialization order and repeat-until structure in Huber's pseudocode before this table was regenerated. Each row uses 4,500 outputs.

| t | Mean proposals | Mean signed-estimator calls | Mean effective splits | Runtime, seconds |
|---:|---:|---:|---:|---:|
| 0 | 3.3700 | 82.4640 | 0 | 2.366 |
| 3 | 3.3656 | 79.8673 | 16.3587 | 2.592 |
| 100 | 3.3422 | 83.5309 | 31.7833 | 2.687 |
| 1,000,000 | 3.4136 | 75.2431 | 28.7864 | 2.389 |

Separate factory checks used 12,000 samples at each of four input probabilities. Energy and fourth-moment checks are stored in exact_results.json. Their deviations were consistent with the scale of Monte Carlo noise, but 4,500 samples do not resolve the very small transient fourth-moment change in this narrow mixture. The large-time cases test implementation work saturation; by themselves they do not show that a tiny non-equilibrium departure was measured.

## 9. Comparison with existing operations

The uncompressed Wild genealogy uses the same model, initial sampler and one-particle output contract, and its expected leaf count is e^t. The present ideal construction eliminates that dependence in the restricted class. This is a proved comparison with a specified algorithm, not an information-theoretic lower bound or a comparison with every established method.

Time-relaxed Monte Carlo already uses recursive Wild constructions and equilibrium treatment of high-order terms to address collision stiffness [1]. Some recursive formulations remove time-step errors; their other approximations must be identified rather than treating all variants as naive time stepping. Deterministic Maxwell moment hierarchies are also established [2]. The numerical reference here demonstrates their strength for moment and approximate density queries. No compute-matched experiment establishes practical superiority of the new construction over these strongest relevant alternatives.

During independent exploration, exact local repair of generative molecular samples led to substantial overlap with partial rejection sampling [5]. Stabilized chaotic sensitivity through spring coupling and change of measure led to close overlap with Fang and Giles [6]. Those mechanisms were not retained as new inventions.

Selective examination of the two user-specified repositories did not supply a theorem used in this proof. The openai/math Boltzmann results surfaced in that examination concerned a different nonuniqueness problem. Keyword searches returning no Astra match do not prove absence of related work. Neither repository's existence nor internal verification status is used as independent validation of this note.

## 10. Precision, physical access and limits

**Finite computation.** NumPy/SciPy draws and arithmetic are floating-point. A discrete floating-point output distribution has TV distance one from a continuous density when compared literally on all measurable sets. Accordingly, the mathematical continuous-law TV bound must not be attached directly to the executable. A proper finite-machine specification would compare to a quantized target, or to a stated observation-noise model. Certified random-bit/interval decisions and their full expected bit complexity have not been implemented or bounded here. The code checks inputs and raises on several numerical failure modes; that is not an interval proof.

**Acquisition.** A sampleable bounded mixing law is an actual assumption. Finite mixture tables make it explicit. General experimental velocity data require model fitting and validation, with possible inverse-problem costs. The initial-law robustness bound does not certify the representation.

**State preparation and actuation.** This is a classical computation. It does not prepare a physical gas at f_t, cool a system, enact a new collision kernel, or require an unprovided quantum device. No physical actuator advantage is claimed.

**Energy, timing and calibration.** The reported runtime is local prototype timing, not a calibrated engineering energy budget. Operation counts include random genealogy and factory work but not a new hardware implementation. Constants worsen as rho approaches either endpoint of its allowed interval. A worst-case time cap changes the output contract unless a failure outcome is retained.

**Scientific reach.** Spatial transport, anisotropic initial states, velocity-dependent hard-sphere rates, chemical reactions, path observables and interacting quantum systems are outside this proof. The scalar closed family and integrable Gaussian envelope are essential. Simply giving a different material a variance parameter would not establish applicability.

**What changed.** The computation no longer constructs every ancestor merely to deliver one sample. It first limits the sampled dependency to a random observable degree and then turns the resulting signed information into an exact acceptance decision. The proof supplies a concrete example of this operation, but not evidence that it generalizes to a technologically decisive model.

The decisive unresolved questions are historical priority, a quantized-law implementation with charged bit costs, a fair comparison against high-quality moment/spectral and time-relaxed solvers, and extension beyond this closed isotropic family. These are specific missing requirements, not a claim that a long-standing problem is intrinsically inaccessible. The original civilization-changing completion standard remains unmet.

## References and provenance

[1] L. Pareschi, S. Trazzi and B. Wennberg, *Adaptive and Recursive Time Relaxed Monte Carlo methods for rarefied gas dynamics*, arXiv:1009.2768v1. https://arxiv.org/html/1009.2768v1

[2] A. Santos, *Solutions of the moment hierarchy in the kinetic theory of Maxwell models*, Continuum Mechanics and Thermodynamics 21 (2009), 361–387; arXiv:0903.1054v2. https://arxiv.org/html/0903.1054v2

[3] NIST Digital Library of Mathematical Functions, Section 18.12, Laguerre generating functions, especially equation 18.12.13. https://dlmf.nist.gov/18.12

[4] M. Huber, *Nearly optimal Bernoulli factories for linear functions*, Combinatorics, Probability and Computing 25 (2016), 577–591; arXiv:1308.1562v2. Theorem 1 supplies the 9.5 A/epsilon input-coin bound; Section 2.2 supplies the implemented factory. https://arxiv.org/html/1308.1562v2

[5] M. Jerrum, *Fundamentals of Partial Rejection Sampling*, Probability Surveys 21 (2024), 171–199; arXiv:2106.07744v2. https://arxiv.org/abs/2106.07744

[6] W. Fang and M. Giles, *Importance Sampling for Pathwise Sensitivity of Stochastic Chaotic Systems*, SIAM/ASA Journal on Uncertainty Quantification 9 (2021), 1217–1241; arXiv:2005.12160. https://arxiv.org/abs/2005.12160

Repository context inspected selectively on 13 October 2026:
- https://github.com/harjassand/astra-research-knowledge — entry file 00_START_HERE.txt, blob 6dc62596be2c65f5cd99668bbd57fae0dc2cf535; scoped keyword searches. No full-archive or priority clearance is claimed.
- https://github.com/openai/math — README and scoped searches; search result revision 1581d4cbdd69a0faf34b2089614fe2a814316a6a. No theorem from that repository is a proof premise here.

All third-party results are credited; no third-party full paper is bundled. Numerical scripts and results were produced in this investigation. The package manifest records their final hashes.

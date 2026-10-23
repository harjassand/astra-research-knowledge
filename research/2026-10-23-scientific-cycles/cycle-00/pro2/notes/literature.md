# Primary literature boundary for the PRO2 spectral-CDF operation

Prepared 2026-10-21 by the bounded literature subagent. This is a source and novelty check, not a claim of exhaustive priority search. The main investigator owns the construction and numerical work.

## Closest established result: CTU 2021

Tyler Chen, Thomas Trogdon, Shashanka Ubaru, *Analysis of stochastic Lanczos quadrature for spectrum approximation*, ICML 2021, PMLR 139:1728–1739.

- Official paper: https://proceedings.mlr.press/v139/chen21s.html
- Main PDF: https://proceedings.mlr.press/v139/chen21s/chen21s.pdf
- Full paper with appendices: https://arxiv.org/html/2105.06595v2

Let F_A be the empirical spectral CDF, and let Psi_i(x)=v_i^T 1[A<=x]v_i for independent uniform unit-sphere probes in R^n. For m probes, Theorem 2 gives

`Pr(sup_x |F_A(x) - mean_i Psi_i(x)| > t) <= 2*n*exp(-m*(n+2)*t^2)`.

For sorted Gaussian quadrature nodes theta_j and weights d_j, Corollary 1 gives, on the support interval,

`L(x) = sum_{j=1}^{k-1} d_j 1[theta_{j+1} <= x]`,

`U(x) = d_1 + sum_{j=2}^{k} d_j 1[theta_{j-1} <= x]`,

with `L <= Psi <= U`. Theorem 3 bounds the averaged quadrature's KS error by `mean_i max_j d_ij`. Combining these already yields simultaneous CDF confidence bands and post-selected interval counts; the numerical outlook demonstrates eigenvalue-count uses.

Remark 4 derives the bounds in exact arithmetic. Appendix D discusses Greenbaum's nearby-problem interpretation and cluster weights qualitatively, without an explicit computable rounding allowance in the displayed CDF bands. Clustered eigenvalues can cause stagnation. Full reorthogonalization costs `O(m*k*(T_mv+n*k))` arithmetic and `O(n*k)` storage.

**Decision:** CMS envelopes plus stochastic simultaneous CDF confidence is established, not a new operation by itself.

## CTU unified analysis: finite precision remains scoped

Chen, Trogdon, Ubaru, *Randomized matrix-free quadrature: unified and uniform bounds for stochastic Lanczos quadrature and the kernel polynomial method*.

- Full primary manuscript: https://arxiv.org/html/2204.01941v3
- Journal DOI: https://doi.org/10.1137/23M1600414

Section 3.1 and Lemmas 9–11 improve Wasserstein/function-class bounds via concentration of finitely many Chebyshev moments, replacing the earlier dimension-prefactor union bound by a moment-count prefactor. This should not be represented as a new KS/CDF bound.

Section 4.2.1 discusses finite-precision Lanczos, Greenbaum, and Knizhnerman's accurate modified moments. It explicitly leaves a full finite-precision analysis outside scope, giving numerical illustration and interpretation. This is evidence for a particular missing explicit numerical contract, not evidence that finite-precision quadrature theory is absent.

## Chen–Trogdon stability: an important competing mechanism

Chen and Trogdon, *Stability of the Lanczos algorithm on matrices with regular spectral distributions*.

- Full primary manuscript, v3: https://arxiv.org/pdf/2302.14842
- Publisher: https://www.sciencedirect.com/science/article/pii/S0024379523004202

Definition 2.2 controls recurrence error, normalization, local orthogonality, and spectral extension by an epsilon_lan parameter. Theorem 3.1 constructs a nearby measure matching computed quadrature moments through degree 2k-1. Corollary 3.2, for sufficiently small epsilon_lan, gives the same matrix A and a nearby probe b* whose exact Lanczos output matches the computed one, with

`||b-b*|| <= 2*sigma*D*k^4*M_k(mu_N;[a,b])^2*epsilon_lan`.

Here sigma=max(1,2||A||/(b-a)), D is an absolute constant, and M_k controls reference orthogonal polynomials. Regularity hypotheses make this useful; general inputs need not have a favorable M_k. Forward stability additionally requires appropriate regular reference densities.

This is a meaningful prior finite-precision route, capable in principle of vertical CDF error through probe perturbation. A new residual-checkable arbitrary-input construction must be distinguished by hypotheses, computability, constants, and actual costs, rather than by claiming no existing stability theorem.

## Earlier perturbation mechanisms

- Anne Greenbaum, *Behavior of slightly perturbed Lanczos and conjugate-gradient recurrences*, Linear Algebra and its Applications 113 (1989), 7–63. DOI https://doi.org/10.1016/0024-3795(89)90285-1 . Publisher access to the full original failed; mechanism above was checked in the primary CTU/CT follow-up papers, not independently against the full original. The nearby problem may have a larger dimension; eigenvalue proximity alone is not the complete statement, because weights also matter.
- Chandler Davis and W. M. Kahan, *The Rotation of Eigenvectors by a Perturbation. III*, SIAM Journal on Numerical Analysis 7(1) (1970), 1–46. DOI https://doi.org/10.1137/0707001 . Publisher abstract checked. Gap/residual control of spectral subspaces is established. The main investigator must supply its exact one-sided projection lemma and constants; the broad rotation principle is not new.

## Stronger Wasserstein algorithms are already available

Bhattacharjee, Jayaram, C. Musco, C. Musco, Ray, *Improved Spectral Density Estimation via Explicit and Implicit Deflation*, SODA 2025, 2693–2754.

- Primary preprint: https://arxiv.org/abs/2410.21690
- Publisher: https://doi.org/10.1137/1.9781611978322.88

Abstract verified, full proof not examined: explicit deflation plus Chebyshev moment matching achieves Wasserstein-1 error epsilon*sigma_l(A) in `O(l*log(n)+1/epsilon)` matvecs, with an `Omega(l+1/epsilon)` lower bound; SLQ essentially matches this adaptivity implicitly. This is relevant to performance comparisons, but is not itself a finite-precision CDF-band theorem.

## Elementary counterexample to a tempting invalid transfer

This calculation is ours; it is **not** an allegation that the cited authors make the invalid inference.

Take `A=diag(-1,1)`, `B=R_theta A R_theta^T`, where R_theta is the planar rotation, and `v=(1,1)/sqrt(2)`. Their eigenvalues coincide, yet at x=0 their weighted CDFs are

`Psi(A,v)(0)=1/2`,

`Psi(B,v)(0)=1/2 + sin(2*theta)/2`.

Also `||B-A||=2*|sin(theta)|`. For 0<theta<pi/6, both shifted thresholds `+/- ||B-A||` remain inside (-1,1), so horizontal movement alone leaves Psi(B,v) unchanged there. The proposed inequality `Psi(B,v)(x-delta) <= Psi(A,v)(x)` fails even when delta=||B-A||. A vertical rotation allowance is necessary, and its leading size can be linear in the matrix perturbation divided by the gap.

## Scoped continuation boundary

The potentially distinct object is an explicit, independently checkable numerical certificate for arbitrary finite symmetric A that transfers each probe's computed quadrature to the original operator, including probe-dependent backward operators and orthogonality defects. Concentration must remain attached to the true A and the original random probes. This combination is not established as novel by this bounded search.

A valid contribution should state the actual residual/rounding verification contract and compare costs with ordinary fully reorthogonalized SLQ. A lower log-dimension concentration term would be a separate improvement requiring an exact theorem, not an assertion inferred from the 2024 Wasserstein result. Numerical band narrowing must survive quadrature uncertainty; small backward error alone cannot fix CMS stagnation at atoms or clusters.

## Web reference IDs for the parent to retrieve before final citation

- CTU 2021: turn27view0 (HTML); earlier main PDF turn13view0; supplement turn16view0.
- CTU unified: turn14view0; finite precision turn16view2 / turn18view2.
- Chen–Trogdon: turn27view1; earlier exact theorem read turn25view1.
- Greenbaum publisher: turn24search0; author publication page turn24search1.
- Davis–Kahan DOI: turn24search12.
- Deflation: turn26academia36; official publisher turn26search0.

The parent must open or search/find these sources itself before citing them in its final response. No source is claimed unread or stronger than inspected above.

## Follow-up: aggregate Gaussian normalization and Dirichlet/DKWM

The main investigator subsequently supplied the independently proved bound for even s=2m real Gaussian probes:

`H(t) = (sum_l g_l^T 1[A<=t] g_l)/(sum_l ||g_l||^2)`,

`Pr(sup_t |H(t)-F_A(t)| > epsilon) <= 2*exp(-(n*s-2)*epsilon^2)`.

This is a different weighting from averaging separately normalized sphere probes. Its proof uses Dirichlet(m,...,m) weights, grouped uniform spacings, and DKWM. The endpoint comparison `(r*m-1)/(n*m-1) <= r/n <= (r*m)/(n*m-1)` removes the need for an additional inverse-sample-size allowance. The proof extends immediately to partial sums of arbitrary positive-integer Dirichlet parameters. This paragraph records the supplied construction, not a literature attribution.

### Closest direct proof mechanism located

Seongmin Kim, Jeunghun Oh, Hungkuk Ko, Jeongmin Park, Jaeyong Lee, *Bayesian Bootstrap based Gaussian Copula Model for Mixed Data with High Missing Rates* (2025), Appendix, manuscript pp. 23–24.

- https://arxiv.org/pdf/2507.06785
- Web refs: turn33view2, turn34view1.

The appendix explicitly represents cumulative Dirichlet(1,...,1) weights as order statistics of n-1 independent uniforms, and applies DKWM to their empirical KS statistic. Its subsequent comparison also involves randomness of the observed-data CDF versus the population CDF and retains an extra 1/(n-1) term. The inspected proof does not state the grouped integer-Dirichlet spectral theorem above. The Dirichlet/spacings/DKWM mechanism is nevertheless explicit prior art. No assertion is made here about the validity of every conditional-probability statement in this unrelated application.

### Older primary posterior-process treatment

Kolyan Ray and Aad van der Vaart, *On the Bernstein-von Mises theorem for the Dirichlet process*, Electronic Journal of Statistics 15(1) (2021), 2224–2246.

- https://arxiv.org/pdf/2008.01130
- https://doi.org/10.1214/21-EJS1821
- Web refs: turn36view0; author-uploaded full text turn35view1 / turn36view1.

Theorem 2 gives a finite-sample coupling of the centered Dirichlet posterior CDF to a Brownian bridge with universal constants. In its proof, equation (2.10) expresses the Bayesian bootstrap CDF through n-1 uniform order statistics; equation (2.12) compares it with the quantile process. The representation is valid for fixed observations, including repeated values, so integer grouping is already implicit. The paper's DKWM use controls observed empirical CDF deviation from the population CDF; I did not find the exact simple grouped Dirichlet tail inequality above displayed there.

### Follow-up decision and limits

**Exact novelty status: unknown.** Three targeted search batches found no primary paper stating this exact aggregate-normalized spectral theorem. That negative search result is not evidence of priority. The probability mechanism is established and the proposed inequality is a short consequence of classical spacings and DKWM. Present it as an explicit corollary used in the new calculation, with independent proof, rather than as a newly discovered concentration principle. Its removal of the n-prefactor improves the *displayed CTU 2021 bound for a changed estimator*, not a demonstration of superior estimators or algorithms generally.

Anton, Roy, Tourky, https://arxiv.org/html/2312.01265v3, was screened as a broader monotone-process concentration result; no exact Dirichlet theorem was located. A PMLR 2026 conformal-prediction/spacings search hit could not be retrieved and was not relied upon. Follow-up resource accounting: three batched search calls plus four retrieval/find calls; reported tool-call elapsed times sum to approximately 23.9 seconds, excluding investigator reasoning and file writing. No new numerical experiment or benchmark was run.

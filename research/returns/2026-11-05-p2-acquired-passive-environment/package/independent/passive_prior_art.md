# Passive memory: primary comparisons and the precise bridge

This is a comparison of the inspected primary sources and accepted Astra texts. It establishes neither historical priority nor practical superiority. Positive exponential approximation, passive realization, data-driven GLE fitting, and no-reset randomized response acquisition all have substantial antecedents.

## 1. The approximation and finite-information capital is old

**Braess and Hackbusch, 2009.** Their primary preprint proves positive exponential interpolation of completely monotone functions and links exponential approximation to rational approximation. Combining Lemma 2.2 and Theorem 3.7 gives, for bounded completely monotone \(f\),

\[
\inf_{u\in E_m}\|f-u\|_{L^\infty[a,b]}
\le 8f(0)\rho^{-2m},\qquad
\rho=\exp\!\left[
\frac{\pi\,\mathsf K(a/b)}
{\mathsf K(\sqrt{1-(a/b)^2})}
\right].
\]

Since \(\log\rho\) is of order \(1/\log(b/a)\) for a wide interval, cutting a small initial interval already yields the familiar \(O(\log^2(1/\epsilon))\) positive-mode count. This scaling must not be called a new discovery. Their Theorem 2.1 also supplies exact nonlinear exponential interpolation at prescribed positive nodes.

Primary source: [On the Efficient Computation of High-Dimensional Integrals and the Approximation by Exponential Sums](https://webdoc.sub.gwdg.de/ebook/serien/e/MPI_Math_Nat/preprint2009_3.pdf). Koyama restates the approximation bound as Theorem 1.4 in [Exponential sum approximations of finite completely monotonic functions](https://arxiv.org/pdf/2301.08931).

**Gao, Li and Wellner, 2010.** Theorem 1.1 gives \(L^p\) bracketing-entropy bounds for bounded completely monotone functions; the \(L^2[0,1]\) metric entropy is sharply of order \(\log^3(1/\epsilon)\). The constructive upper bound uses dyadic time blocks. Thus logarithmic-squared local approximation complexity times logarithmic coefficient precision is already natural in the known theory.

Primary source: [How many Laplace transforms of probability measures are there?](https://arxiv.org/pdf/1001.0200).

A useful consequence, stated here as an inference, is that the same order holds for \(L^1[0,1]\). For functions in \([0,1]\),

\[
\|f-g\|_2^2\le\|f-g\|_1.
\]

An \(L^1\) \(\epsilon\)-cover therefore gives an \(L^2\) \(\sqrt\epsilon\)-cover; combine the known lower bound with the \(p=1\) upper bound. Consequently a uniformly valid encoded representation for the entire class needs order \(\log^3(1/\epsilon)\) bits in the worst case. The model encoding in the companion construction meets that order, apart from supplied scale/input bits. This is a consequence of known entropy, not a priority claim.

**Koyama, 2023.** This work treats positive exponential sums using Gaussian quadrature and analytic variable transformations, with geometric approximation estimates for a finite positive interval of rates. It is a strong structured approximation comparator, but it does not make that bounded rate interval or its integration data physically acquired.

Primary source: [Exponential sum approximations of finite completely monotonic functions](https://arxiv.org/pdf/2301.08931).

The companion construction's contribution relative to these approximation statements is an explicit robust route from finite interval-valued reports to a positive encoded model, including clock rounding, coefficient errors, sparse extraction, and a total-data-error certificate. The known approximation mode count is not its distinctive element.

## 2. Existing GLE identification and passive realization

| Primary method | What the source supplies | Comparison with the present construction |
|---|---|---|
| Bockius, Shea, Jung, Schmid and Hanke, 2021 | From equidistant velocity-autocorrelation samples, a modified Prony procedure and positive-real realization produce an extended Markov model. The paper tests molecular-dynamics data and noise; its algorithm can fail positivity checks and changes model size in examples. | This is a direct, strong data-to-passive-model comparator. Our narrower positive-mixture class permits a uniform interval-data certificate with no mode-count or gap parameter. It does not establish that the resulting fit is practically superior or that the prior method cannot use a similar certificate. |
| Lang and Lu, memory-kernel learning, arXiv 2402.11705 | Regularized Prony estimates of correlations feed Sobolev-loss/RKHS kernel regression. Theorems 4.1–4.2 relate weighted \(L^2\) kernel error to correlation errors. The inspected Assumptions 1–2 impose smooth exponential decay and Laplace-line coercivity bounds. | Our target is finite-horizon \(L^1\) identification of bounded completely monotone kernels including zero rates and unbounded high-rate support, with reports obtained by active control. The information interface and theorem class differ. Their method directly addresses trajectory-derived correlation data and is a stronger practical baseline than an unregularized inverse Laplace transform. |
| Baczewski and Bond, 2013 | Extended-variable integrators for positive-Prony GLE kernels. | A finite positive exponential model already has an established Markov realization and execution literature. Merely writing auxiliary ODEs is not new. |
| Lang and Lu, error analysis, arXiv 2512.10256 | Quantitative stochastic GLE trajectory comparisons under strongly convex potentials and weighted kernel controls. Theorems use specified smoothness and damping/comparison conditions; they include synchronized stochastic coupling and decay analysis. | The accepted Astra deterministic derivative-memory energy inequality uses passivity to avoid a small-kernel requirement in its narrower setting. It is not a general replacement for the stochastic theory and does not by itself acquire the kernel or initial force. |
| Peherstorfer, Gugercin and Willcox, time-domain Loewner | Reduced models inferred from time-domain trajectories, via recovered frequency-response information and the Loewner framework. | Black-box, data-driven model reduction is established. The desired additional item is the uniform calibrated error statement over the admitted no-gap positive-mixture class, not the idea of fitting a reduced model from trajectories. |

Primary links:

- [Bockius et al., full paper](https://arxiv.org/pdf/2101.02657), especially Section 3.3 and Appendix C for the positivity checks and algorithm.
- [Lang and Lu, Learning Memory Kernels in Generalized Langevin Equations](https://arxiv.org/pdf/2402.11705), especially Section 4.
- [Baczewski and Bond, original preprint](https://arxiv.org/abs/1304.6446); [Sandia publication record](https://www.sandia.gov/research/publications/details/numerical-integration-of-the-extended-variable-generalized-langevin-equatio-2013-01-01/).
- [Lang and Lu, Error Analysis of Generalized Langevin Equations with Approximated Memory Kernels](https://arxiv.org/pdf/2512.10256), especially Theorems 3.1–3.2 and 4.1–4.2.
- [Peherstorfer, Gugercin and Willcox, primary author-hosted paper](https://kiwi.oden.utexas.edu/papers/data-driven-model-reduction-Peherstorfer-Gugercin-Willcox.pdf).

The inspected sources do not establish the entire specific conjunction sought here: finite moving-trap control on one retained apparatus, bounded physical reporting errors, unrestricted positive-mixture rates, an unfiltered finite-horizon kernel certificate, separately acquired old-force behavior, nonlinear deterministic prediction, and finite encoded execution. That is a statement about this inspection, not proof that no earlier work contains the conjunction.

## 3. Astra N1688 is the strongest internal comparator

The governing local source is:

\`/workspace/scratch/ff43c8405441/output/bridge_programme/N1688_ACCEPTED_SOURCE.txt\`

Public governing response:

[COMPLETE_VISIBLE_RESPONSE.txt](https://github.com/harjassand/astra-research-knowledge/blob/76f6a7ce78867b927680ba3b9cd5eb407ce61ccd/research/2026-11-04-p2-acquired-thermal-feedback-simulator/source/p2/COMPLETE_VISIBLE_RESPONSE.txt)

N1688 already acquires response through fresh random signs on a retained nonstationary apparatus. It does not reset microscopic modes between experiments. It also treats noise-covariance acquisition, unknown fixed gains, conditional future noise, previous-probe remnants, arbitrary bounded causal feedback, and finite-bit simulation of encoded complete records. Those are accomplished interfaces, not speculative baselines.

Its completed-cell matched pulse has three vanishing moments. Those cancellations yield a uniform normalized response-tail bound despite arbitrarily slow or frozen hidden modes. The chosen operational interface suppresses the slow directions that defeat a direct short-history truncation.

The present proposal has a different operational target:

| Interface | Accepted N1688 | Present finite-horizon deterministic target |
|---|---|---|
| Observable | Matched completed-cell pulse-weighted record | Unfiltered observed coordinate and its nonlinear driven trajectory |
| Action | Prescribed completed-cell pulse family | Finite moving trap during acquisition, then admitted ordinary forcing |
| Memory treatment | Physically suppress slow directions; retain a short discrete response tail | Retain a compressed continuous positive kernel, including its zero-rate component |
| Physical dynamics | Reciprocal linear thermal apparatus and encoded stochastic records | Passive linear hidden bath coupled to a strongly convex nonlinear observed potential |
| Noise guarantee | Conditional future encoded record law in total variation | Acquisition confidence plus deterministic trajectory error |
| Initial state | Conditional nonstationary future-noise and previous-probe bounds | Separate acquisition/bounding of the old deterministic hidden force |
| Feedback | Arbitrary bounded causal policy selected after calibration | Common admitted forcing; extra feedback stability is needed if plant and predictor receive different actions |
| Unknown gains/noise | Explicitly addressed by the accepted acquisition | Must be supplied or separately acquired in the new protocol; no automatic inheritance |
| Mode number and gap | Neither supplied | Neither supplied |
| Finite execution | Executed encoded Gaussian future-record simulator | Positive kernel fit is executed; full nonlinear trajectory execution is the backward module's obligation |

This is not an across-the-board improvement over N1688. The present target retains DC/slow response and admits a nonlinear observed coordinate, while its stochastic and feedback guarantees are weaker. N1688's random-sign/no-reset primitive cannot be relabeled as new.

## 4. The precise full-chain claim that can be earned

A correct combined theorem should say, in substance:

1. A specified finite actuator and sensor protocol, under supplied mass, initial-force, calibration, and noise bounds, produces the simultaneous rational kernel report intervals.
2. Those reports determine an encoded positive model with a certified finite-horizon kernel \(L^1\) error. The companion construction proves this step.
3. A separate finite late-time force measurement bounds the old hidden force over the deployment horizon. It need not reset a zero-rate state.
4. An executable, enclosed numerical implementation produces a trajectory and bounds its equation residual.
5. The accepted nonlinear passivity inequality converts all these errors into the stated observed-trajectory guarantee for the admitted forcing class.

The kernel module cannot close items 1, 3, or 4 by changing its notation. Conversely, once the forward and backward modules establish their displayed interfaces, no microscopic mode reconstruction or relaxation gap needs to be inserted between them.

The smallest honest significance statement is a finite, reusable, physically acquired deterministic predictor for this specified nonlinear/passive class, with its actual costs. Whether a valuable scientific task makes that capability consequential, and whether it outperforms the best identification methods at realistic costs, remain separate questions.


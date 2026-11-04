# Completed companion: a finite certificate for every first-failure deadline

## What is now complete

The earlier full-CDF proposal was explicitly unfinished. This directory supplies its new finite-confidence and finite-arithmetic closure, together with a changing-invariant-law theorem and one executed diagnostic. The old completed sensitivity proofs and old unfinished notes are preserved separately; this does not retroactively label the earlier proposal as acquired.

**Mathematical endpoint.** For succinct reversible local dynamics on a known all-terminal network, with product invariant law, a certified spectral-gap floor, explicitly priced static rare-failure counting/sampling, and equilibrium-safe initialization, construct one finite certificate of the entire first-failure CDF. On one event of probability at least \(1-\delta\), every positive rational deadline has a containing interval with relative width at most \(1+\epsilon\). Binary deadline queries use only the finite certificate. No trajectory of mean-lifetime duration or computation proportional to the inverse global failure probability is required.

The continuous theorem uses genuine Poisson uniformization of a continuous-time generator. The discrete theorem predicts an actual positive-semidefinite reversible endpoint kernel. It does not substitute one clock for the other.

### Files

- **PROOF.md:** full model, static conditional sampler, boundary-Palm identity, stronger spectral tail bound, bounded-observable estimates, finite Poisson tables, simultaneous confidence allocation, capped execution, finite query arithmetic and complexity.
- **CALIBRATION_AND_PHYSICAL_SCOPE.md:** new uncertain-invariant-law theorem, explicit oriented auxiliary conductances, unknown-support calibration, real local exposure costs, initialization and implementation limits, and rational confidence-factor composition.
- **finite_arithmetic.py:** implemented rational outward exponential/power queries, finite integer Poisson tables, fixed-denominator grids, and a deterministic certificate-query interface.
- **diagnostic.py / results.json:** exact rational finite-path checks and an executed synthetic rare-event experiment, with its numerical-reference and implementation limits stated.

## Why this supplies more than a mean or sensitivity bound

A mean alone does not specify mission-time failure probability. The preceding sensitivity theorem propagated uncertainty in a CDF but did not compute that CDF. This construction supplies a finite function representation spanning arbitrarily small probabilities, the transition through the lifetime scale, and late deadlines.

The three time regions use different justified operations:

1. At tiny deadlines, a relative linear bound uses the stationary boundary flux. There is no grid accumulating at zero.
2. Over a finite intermediate range, a boundary-Palm path sampler estimates a bounded observable. When failure is already common enough, ordinary safe-start simulation supplies a bounded-mean alternative.
3. Beyond a finite gap-scale horizon, a short reverse no-return experiment estimates the isolated slow decay mode. A proved relative remainder bound covers every later deadline.

The spectral refinement is
\[
\lambda\ge g[p+(1-p)r],
\qquad
\frac{F(u)-(1-e^{-\lambda u})}{1-e^{-\lambda u}}
\le\frac{2}{gu}.
\]
Here \(r\) is fast spectral mass and \(u=Rt\) is actual uniformized time. This improves the previous proposal's \(g^{-2}\) tail horizon.

The sampler and arithmetic are finite. A Poisson law is replaced by its conditional law on a finite explicitly bounded range, using integer weights proportional to \(u^k/k!\). Its omitted tail is charged as a mean bias. Conditional-failure sampler bias, rounding bias, confidence, rejection caps and random-bit caps each have stated allocations. Tail queries use outward rational Taylor or repeated-squaring operations.

## Unknown invariant weights are covered with paid calibration

For killed conductances \(L_0,L_1\) and diagonal invariant masses \(M_0,M_1\), the continuous theorem proves
\[
e^{-\eta}L_0\preceq L_1\preceq e^\eta L_0,\quad
e^{-\Delta}M_0\preceq M_1\preceq e^\Delta M_0
\quad\Longrightarrow\quad
e^{-(\eta+2\Delta)}F_0(t)\le F_1(t)\le e^{\eta+2\Delta}F_0(t).
\]
The missing operation is a mass comparison: unnormalized heat content is coordinatewise increasing in the diagonal masses at fixed killed Laplacian. Scalar mass scaling and time concavity then give the factor \(e^\Delta\); safe normalization supplies another.

Under the accepted P2 product-energy, refresh and unknown-support bands, the acquired continuous CDF log-radius is \(3\Delta+b+\log(1+\rho)\). The auxiliary conductance construction is explicitly reversible under the fitted law and retains the same fitted backbone. No true reverse rate is simply reused with incorrect weights.

Local uncertainty still costs real information. Learning a rare local equilibrium probability by sampling pays its inverse probability. A direct energy measurement is useful only if its physical access and error are independently supplied. The computational theorem removes inverse **global** rarity, not these local exposure costs.

## Executed diagnostic

The synthetic system has 24 parallel components with local failure probability \(1/10\). A mixture of single-component and paired heat-bath refreshes preserves the product law. Failure means all 24 components are failed:
\[
\pi(B)=10^{-24}.
\]
The full binary state space has \(2^{24}\) states, but permutation symmetry reduces this particular example to 25 states. An ordinary lumped finite-state solver is the better method for this example; it is used as the reference.

The diagnostic actually performed **2,926,345 ordinary kernel draws**, with 12,000 trials for each sampled observable. It did not merely report analytically requested shot counts. There were no laboratory measurements.

| Uniformized deadline | 120-digit reference failure probability | Sample-derived containing interval |
|---:|---:|---:|
| \(0.25\) | \(1.1811478801\times10^{-25}\) | \([1.1001161256,1.2251977030]\times10^{-25}\) |
| \(2\) | \(9.4448811003\times10^{-25}\) | \([8.7983083547,9.8015816238]\times10^{-25}\) |
| \(20\) | \(9.4367254503\times10^{-24}\) | \([8.7908207838,9.8015816238]\times10^{-24}\) |

A reverse window of length 448 produced a killed-rate interval
\[
[4.5107681720,\,5.0654328023]\times10^{-25},
\]
containing the numerical reference \(4.7175393061\times10^{-25}\). The reference mean first-failure time is \(2.1197491639\times10^{24}\) uniformized units. These are model units, not laboratory seconds.

Using the sampled rate interval, the deadline \(u=10^{24}\) gives a containing failure-probability interval \([0.3630580878,0.4013993353]\), with reference \(0.3760929816\). A 646-bit rational deadline was queried without simulating its duration.

Additional completed checks:

- The actually forced path distribution and inverse-crossing identity agree **exactly in rational arithmetic** for one through four endpoint updates; the largest enumerated check contains 460 forced paths.
- Eleven outward arithmetic cases span an exponential argument \(10^{-100}\), arguments of more than 1,000 bits, and a discrete deadline \(2^{512}\).
- A 1,333-point finite grid satisfies the required adjacent-ratio bound and uses at most 44 bits per grid node in this example.
- A separate noncommuting changing-mass example obeyed the new bound at 40 tested times. This is a double-precision diagnostic, not a directed-arithmetic proof.

The spectral reference uses 120-digit numerical diagonalization. Its weight sum differed from one by approximately \(3.29\times10^{-120}\); the reference weights were normalized and the result clipped to the probability range. This resolved a saturation assertion in the reference calculation. It did not alter the rational query intervals or the theorem. Numerical eigensystem results are not claimed to be machine-certified enclosures.

## Actual limits of the software and costs

The executed paths and intervals above are a diagnostic of the new operations. They are **not** a run of the theorem's generic whole-curve preprocessing, and the three sampled middle deadlines are not themselves an all-deadline relative certificate.

Generic Karger counting is imported published machinery and **is not implemented here**. It is charged in the theorem at the actual requested accuracy for every prefix call. The diagnostic's parallel-system static probability and conditional failure state are elementary, so no generic counting run occurred.

The literal conservative preprocessing bound is large. On this same model, requested \(\epsilon=0.1,\delta=0.01\) gives:

| Resource in the proved conservative allocation | Bound |
|---|---:|
| Finite intermediate horizon | 25,600 |
| Grid nodes | 6,418 |
| Bounded trials per observable | 188,743,680,000 |
| Total bounded trials | 1,211,734,425,600,000 |
| Per-boundary-trial attempt cap | 7,680 |
| Path updates before boundary/factory work | 62,068,672,482,508,800,000 |

These quantities were calculated, **not executed**. Static-oracle work, boundary rejection, rational tables, initialization and physical calibration are additional priced terms. The theorem is a polynomial-complexity consequence, not a demonstrated practical speedup.

## Physical and comparative boundaries

The exact model must supply its architecture, failure rule, local reach, reversibility/product-law structure and active refresh backbone. The accepted acquisition interface learns admitted unknown support and keeps positive uncertainty for observed-zero channels. It does not discover arbitrary undeclared common causes.

Finite conditional-TV implementation errors are explicitly transferred for equilibrium-safe starts. In a continuous process, an initialization error that puts any mass directly in failure can dominate arbitrarily small deadlines. A physical result therefore requires exact or multiplicatively controlled safe initialization, or a stated minimum deadline. Arbitrary small common-cause intensity errors can also dominate very early probabilities at an all-working start; the equilibrium-safe bound is not exported to that start.

For a fixed-tick device, the guarantee is indexed by completed ticks. Uncertain tick duration may prevent relative wall-time accuracy near a tick boundary. A genuine CTMC theorem is not obtained by dividing a collision kernel by its service time.

The relevant strong alternatives remain:

- **Static all-terminal FPRAS methods:** already solve the static rarity problem and are a necessary ingredient here. Newer static algorithms may improve the chosen backend where their assumptions apply.
- **Nakayama–Shahabuddin regenerative transient-unreliability methods:** already combine short-horizon simulation and large-horizon regenerative bounds, including broader dynamics and all-working starts.
- **Reversible spectral/exponential approximation:** supplies important spectral machinery; an additive approximation alone does not establish relative accuracy for arbitrarily tiny deadline probabilities.
- **Explicit finite-state solvers:** preferable when the state space or a symmetry reduction is manageable, as in this diagnostic.

The completed additional consequence is the nonasymptotic finite uniform relative certificate under the stated succinct-model, gap and static-access promises, together with acquired-model uncertainty transfer. Historical firstness, broad superiority and civilisation-changing practical impact have not been established.

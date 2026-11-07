# Review of the invariant test-weight and finite-program deltas

7 November 2026. Independent machinery review. No principal file was edited.

## Exact files and verdict

| File | Bytes | SHA256 |
|---|---:|---|
| `../principal/INVARIANT_WEIGHT_LIFT.md` | 4993 | `518f72e0eedf3127ba326fc13f8d85e1d38760ebfdb68addf99467481cb14189` |
| `../principal/SUCCINCT_POISSON_CORRECTOR.md` | 6070 | `4037e791b9cceaa3971167bf33373cee47ca71fc3baf3fe55112d1bf7a48cfe7` |

**PASS at the stated finite-system scope.** The invariant-weight pressure estimate, deterministic approximate-invariance cost, height example and finite-program Poisson lemma are valid. A minor implementation clarification for the Poisson sample bound was repaired during review and is recorded below. These results do not complete an effective finite-N hydrodynamic forecast or change the microscopic rates.

**Priority assessment:** the pressure method is established conditional Dirichlet-form/Feynman–Kac nongradient replacement machinery. The invariant-weight step is an immediate conditional-variational extension. I did not verify a published theorem stated in exactly the same global exterior-dependent, time-dependent form. That literal-source distinction does not support a novelty claim. The height estimate is an elementary explicit oscillation budget. The Poisson program uses spectral mixing, bounded sampling and a finite union bound; no historical novelty is established.

## 1. Exact invariant weights

Let a closed block's count and exterior be fixed. The positive-rate path exchange graph connects each nontrivial count sector. Invariance under its internal exchanges is therefore equivalent to measurability with respect to that sector label and exterior. On this conditional space, `a_x(t,eta)` is a scalar even if its dependence on those labels is nonlinear or involves the entire exterior.

For a centered conditional observable `W`, multiplying by this scalar preserves centering and multiplies the resolvent variance by its square. With gap `g`, bound `|W|<=B`, and variance at most `V`, the earlier finite-dimensional spectral inequality gives the same estimate with tilt `s=b a_x(L-1)/(NL)`. The denominator is at least one half under the stated condition `b A B/(N g)<=1/2`.

Integrating the conditional quadratic-form estimates and using `sum_x G_x=(L-1)G_N` is valid for overlapping blocks. No independence is required. The exact block counting produces a factor `(L-1)/L^2`, bounded by the displayed `1/L`. Thus

`lambda_max[-N^2 G_N + (bN/L)sum_x a_x W_x]/N <= 2b^2 A^2 V/L`

is correct. Measurable prescribed time dependence is permitted by the time-dependent operator norm bound. Entropy inequality against the same stationary Bernoulli-1/2 reference and `H(mu_0|pi)<=N log 2` then gives

`|E integral_0^T (1/L)sum_x a_x(t,eta_t)W_x(eta_t)dt|`

`<= log(2)/b + 2b A^2 T V/L`.

The absolute value is correctly outside the expectation. The estimate does not give `E|integral|`, a path supremum, or an arbitrary history-dependent test selected from the realized trajectory. The functions are prescribed functions of current state and time. The state-dependent quantity occurs only in a potential/observable; the transition rates remain those of the specified microscopic generator.

The finite-system theorem may admit very complicated exterior functions. If an operational use requires evaluating such a function, its representation and evaluation cost must be specified. No algorithm for discovering arbitrary sufficient macroscopic weights follows from the measurable-function statement.

## 2. Approximate invariance and height calculation

If `|a_x-abar_x|<=e_a` uniformly and the approximant is invariant on the corresponding block fiber, then at every state and time

`|(1/L)sum_x(a_x-abar_x)W_x| <= N B e_a/L`.

Its integrated expectation costs at most `T N B e_a/L`. No probabilistic independence or small-rate perturbation argument is needed. The two-state example `a=W=+/-1` is a valid obstruction to omitting invariance: `aW=1` has nonzero first-order pressure.

For the displayed height, the centered coefficients sum to zero, so its spatial mean vanishes. Shifting the index gives exactly

`h_(x+1)-h_x = (e_x-mean(e))/N`.

On a forward `L`-site block, the constant part of the coefficient cancels because count is fixed. The prescribed `u` contribution is unchanged. Uniform canonical averaging therefore gives

`h_x-abar_h_x = N^(-2)sum_(j=0)^(L-1) j[eta_(x+j)-k/L]`.

Consequently `|h_x-abar_h_x|<=L(L-1)/(2N^2)<=L^2/(2N^2)`. The resulting deterministic pressure-replacement error is at most `T B L/(2N)`, as stated. Indexing by offsets relative to the block's first site also makes this valid for wrapping blocks. The distinct-site/range condition in the file avoids ambiguity in the source block geometry.

The height itself is linear in the microscopic occupations. The extension also genuinely allows nonlinear weights: for a known Lipschitz function `Phi`, `Phi(h_x)` has invariant approximant `Phi(abar_h_x)` and error at most `Lip(Phi)L^2/(2N^2)`, with the corresponding amplitude bound. This is a precise optional way to formulate a nonlinear example; calling the displayed linear height itself “nonlinear” is only a wording imprecision.

The general Lipschitz-kernel bound is valid for a prescribed kernel (or one invariant on the same fiber). Subtract its value at the block's first site and use count conservation; spatial Lipschitz constant `C_K` yields a bound no larger than `C_K L^2/N^2`. Spatial smoothness alone would not suffice if the kernel were itself permitted arbitrary additional state dependence.

## 3. What the inspected primary literature already supplies

The closest fully inspected source is [Funaki–Gu–Wang, 2404.12234v3](https://arxiv.org/html/2404.12234v3), **Lemma 7.11** and **Appendix C.3**, especially **(C.15)–(C.19)**. Its displayed test field `J(t,v)` is deterministic. Its proof conditions on count and exterior, takes uniform conditional resolvent bounds, applies an entropy/Feynman–Kac estimate and a Rayleigh–Schrödinger spectral bound, and then controls the finite-size remainder. Its application already incorporates nonlinear functions of the block density into the centered local observable and the compensator.

That proof gives exact predecessor pointers to Funaki–Uchiyama–Yau: **Lemma 6.1**, **(6.3)**, the expression at **page 28, line 4**, and **Theorem 6.1** for the spectral perturbation bound. FGW describes Lemma 7.11 as a combination of essentially known results. Its Appendix C.3 identifies where its quantitative remainder refines the earlier limiting argument.

A second inspected full primary source is [Funaki, 2404.18364v2](https://arxiv.org/html/2404.18364v2), **Lemma 4.2**, **(4.5)–(4.6)** and **Section 9.3**, particularly **(9.18)–(9.21)**. This is the Glauber–Kawasaki version of the same conditional-resolvent method; its conservative Kawasaki component and count/exterior conditioning are the relevant predecessor here. The Glauber contribution must not be silently imported as if it preserved the present stationary law.

The original chapter is [Funaki–Uchiyama–Yau, *Hydrodynamic Limit for Lattice Gas Reversible under Bernoulli Measures*, IMA Vol. 77 (1996), pages 1–40](https://link.springer.com/chapter/10.1007/978-1-4613-8468-7_1). The publisher confirms the chapter and scope, but the full chapter was subscription-gated in this audit; the PDF URL redirected to the subscription page. Accordingly, the internal FUY theorem/page pointers above are **verified as exact pointers given by inspected primary successor proofs**, not falsely described as a fresh direct reading of the 1996 pages. No theorem from the unavailable chapter is needed as a black box for the elementary finite-dimensional proof here.

The exact arbitrary bounded global exterior dependence and arbitrary prescribed index/time dependence are not literally the deterministic smooth `J` statement printed in FGW Lemma 7.11 or Funaki Lemma 4.2. They follow immediately when the already uniform conditional proof is repeated with a sector scalar. Therefore the defensible characterization is **a routine finite-system conditional-variational specialization/extension of established replacement machinery**, with explicit constants and measured variance inputs. It should not be presented as discovery of nonlinear nongradient replacement or a new hydrodynamic principle. Whether some earlier source states this exact full version remains unverified, and is immaterial to claiming historical priority, which remains UNKNOWN.

## 4. Optional finite-program Poisson lemma

The lemma's analytic part is correct. For a reversible chain and centered `j`, spectral contraction gives

`|P_tj(x)| <= J p_*^(-1/2)e^(-gt)`.

The chosen `tau` makes the resolvent tail at most `e/4`. The random-time score is bounded by `tau J`; the stated sample count supplies error `e/2` uniformly over `P` parameter values and at most `2^m` inputs. Reuse of the same tapes defines one deterministic finite function after the tapes are drawn. Different inputs need not be independent, and no table of their exponentially many outputs is constructed.

The cap is sufficient: `Kcap>=2 exp(1)R tau` implies the standard Poisson upper-tail bound is at most `2^(-Kcap)`, and the additional logarithmic constraint fits the omitted-score budget. The categorical threshold, Poisson-category and time-grid errors have the stated polynomial coupling budget. Computing a capped Poisson distribution to additive bit precision by elementary exponential/series bounds has polynomial cost in these numeric parameters. The proposal and score evaluation oracles, detector/rate acquisition and bit costs remain actual hypotheses.

**Repaired finite-precision clarification:** the first-read 5848-byte version, SHA256 `0d7e8332871fac07b89aaf2b56e22565b403d62f1fedfa12eabf14c47f10cfdc`, needed an explicit score-range convention. The pinned 6070-byte version now clips the approximate `j` evaluation to `[-J,J]` and the final score to `[-tau J,tau J]`. Clipping preserves approximation error from the true bounded score and makes the stated `M` formula valid verbatim for the digital scores. I inspected this repair. No finite-precision range objection remains.

The support/energy comparison is correct under its common norm cap. At most `2m_F` translates affect a bond, giving `|pi Gamma(F-Fhat)|<=4m_F||F-Fhat||`. The product-of-sum-and-difference bound gives exactly the displayed linear energy perturbation estimate. The all-density Bernoulli derivative bound, endpoint cutoff, conductivity normalization and acquired-rate inflation agree with the earlier independently checked corrector-residual construction. A density-uniform coefficient interval is sufficient for the cellwise lower conductivity; no derivative of the unknown diffusivity is being assumed.

The stagewise summable confidence schedule and class-dependent algebraic convergence justify adaptive correctness and polynomial eventual work at fixed physical class. The algorithm does not need a numerical convergence constant to recognize its returned residual bound. These facts are elementary spectral/Monte Carlo consequences combined with the explicitly imported source gluing construction; they are not a novel general Poisson-solver theorem or a finite-N hydrodynamic certificate.

## 5. Final boundary and source pins

Approved: the exact invariant-weight pressure estimate, its explicit approximate-invariance loss, the height/kernel calculation, and the finite-program corrector lemma with the inspected rounded-score range repair.

Not approved by this review because not proved in these files: microscopic-current decomposition to a full nonlinear density prediction, all corrected-reference/profile errors and large-deviation cancellations with numeric constants, arbitrary force or rate feedback, a growing-control uniform theorem, physical apparatus performance, historical novelty or matched practical advantage. The explicit unclosed-operation paragraph preserves this boundary correctly.

Source pins:

- `source/2404.12234v3.html`: SHA256 `18350f0690e9bb0bb58ce3068f3407b752edc6c98dafc84ccb16b7c5d53252d2`.
- `source/2404.18364v2.html`: 2434948 bytes, SHA256 `df25539854dfa0d80e37ef9a3feae30680cfe46a3455a5f5e6bb985f23c7a1c4`.

Any later substantive delta requires its own exact file/hash review.

# FJ nonlinear correction audit

**Scope.** Cold audit of the pinned nonlinear source package, independent exact checks, bounded code replay, the infinite-degree sinh sampler, and the closest primary literature. All new artifacts are confined to this assigned directory. No source or capital files were edited.

## Finding

The finite-polynomial theorem is algebraically sound under its stated global bounds and ideal exact-arithmetic/randomness model. The event probabilities are nonnegative and sum to at most one; the offspring mean is uniformly subcritical; the signed first-event recursion is the resolvent fixed-point equation; the output is bounded; and Hoeffding gives the stated pointwise confidence bound. The proof also correctly distinguishes the enclosure condition from the finite-work condition. Exact rational checks support both supplied predictor certificates and reject the two stated adversarial radii.

The strongest result added in this audit is an exact killed-tangent variant. Killing the underlying Markov path at rate `V(X_t)` instead of uniformizing at a constant upper rate `Λ` changes the tree-node bound from `Λ/(λ−Γ)` to `λ/(λ−Γ)`. It retains bounded samples, unbiasedness, almost-sure tree termination, and the same Hoeffding bound. This improves the mathematical node-count certificate, but it is not yet an algorithmic speedup: exact state-dependent killing can be expensive, and ordinary thinning at envelope `Λ` gives up to `Λ/λ` candidate path events per tree node. In the worst-case bound those factors cancel back to `Λ/(λ−Γ)` total candidate events.

Prior art substantially narrows any novelty claim. Branching-diffusion representations and supersolution-based moment bounds are established by Agarwal–Claisse; nonlinear sinh branching for Poisson–Boltzmann equations is already explicit in Bossy et al.; and inference-time surrogate defect correction by stochastic PDE simulation is established by SCaSML (ICLR 2026). The reusable distinction here is the certificate-directed local tangent-resummed construction with bounded point-query returns and a directly stated expected-work/Hoeffding contract, plus the residual-to-damping sinh eligibility condition. Priority for that exact package remains `UNKNOWN`; the argument does not establish a breakthrough or practical advantage over FFT or modern MLP solvers.

## Cold reconstruction of the supplied sampler

Write `e=u−v`. The supplied Taylor model gives

`(-L+V)e = r − Σ_{m≥2} c_m e^m`,

where `V=F_u(x,v)`, `|r|≤R`, `|c_m|≤B_m`, and the series and its derivative converge uniformly and absolutely on `||e||∞≤h`. With `λ≤V≤Λ`, define `P(h)=ΣB_m h^m` and `Γ(h)=Σm B_m h^(m−1)`. The certificates `R+P(h)≤λh` and `Γ(h)<λ` imply that `G_Λ f=E[f(x+sqrt(2Dτ)G)]`, `τ~Exp(Λ)`, gives a contraction

`T(e)=G_Λ[r/Λ+(1−V/Λ)e−Σc_m e^m/Λ]`

on the radius-`h` sup-norm ball, with contraction factor at most `q=1−λ/Λ+Γ(h)/Λ<1`. The event masses in the source implementation encode this same first-event equation. Their return multipliers have magnitude at most one, so the normalized tree return is in `[-1,1]`. The spatially varying continuation probabilities do not invalidate the generation estimate: conditional mean children are bounded uniformly by `q`, hence `E[G_n]≤q^n`, `E[N]≤1/(1−q)=Λ/(λ−Γ)`, and `N<∞` almost surely. Conditioning on the first event identifies the tree expectation with the unique fixed point. Bounded returns then give

`P(|v+(h/M)ΣZ_j−u|>ε) ≤ 2 exp(−M ε²/(2h²))`.

This is a mathematical-law result. It assumes exact coefficient evaluations, valid event probabilities, and exact random draws. The copied implementation uses ordinary floating-point arithmetic and does not validate those conditions with interval arithmetic.

The fixed-rate sampler is also a specialization of the established signed branching-diffusion form. For the normalized defect `z=e/h`, choose lifetime rate `Λ`, coefficients `a₀=r/(Λh)`, `a₁=1−V/Λ`, and `a_m=−c_m h^(m−1)/Λ`. A fixed offspring law can be chosen as `p₁=1−λ/Λ`, `p_m=B_m h^(m−1)/Λ`, and `p₀=(λh−P(h))/(Λh)`. The enclosure implies `|a₀|≤p₀`; tangent bounds imply `0≤a₁≤p₁`; and `|a_m|≤p_m`. The branch weights `a_l/p_l` are therefore bounded by one wherever the denominator is positive, and zero-mass cases are omitted. Its offspring mean is `1−λ/Λ+Γ/Λ<1`. This embedding places the construction close to Agarwal–Claisse’s established representation and moment criteria; the source package's local event allocation is a convenient certificate-preserving specialization, not a new branching principle.

## Stronger killed-tangent theorem

Let `X` be a conservative Markov process with generator `L`, and let measurable `V≥λ>0` have finite path integral on bounded intervals. For an independent `E~Exp(1)`, set

`ξ=inf{t:∫₀ᵗV(X_s)ds≥E}`, `Y=X_ξ`.

The hazard identity gives `P(ξ∈dt | X)=V(X_t)exp(−∫₀ᵗV(X_s)ds)dt`, and therefore

`G_V f(x)=E_x[f(Y)/V(Y)]=E_x[∫₀∞ exp(−∫₀ᵗV(X_s)ds)f(X_t)dt]`,

with `||G_V f||∞≤||f||∞/λ`. Under the same Taylor and enclosure assumptions, the contraction

`Φ(e)=G_V[r−Σc_m e^m]`

has constant `Γ/λ<1` and maps the tube into itself. At endpoint `Y`, use source probability `abs(r(Y))/(hV(Y))`, m-child probability `abs(c_m(Y))h^(m−1)/V(Y)`, and the remaining mass for zero. Their sum is at most `(R+P)/(hλ)≤1`; mean offspring is at most `Γ/λ`. Thus `|Z|≤1`, `E[hZ]=e`, `E[N]≤λ/(λ−Γ)`, almost-sure termination, and the same Hoeffding bound follow. The proof and assumptions are recorded in [KILLED_TANGENT_THEOREM.md](KILLED_TANGENT_THEOREM.md).

For the exact two-state rational CTMC in [exact_cases.py](exact_cases.py), the killed kernel is `(-Q+diag(V))⁻¹diag(V) = [[64/67,3/67],[4/67,63/67]]`. Exact Fraction recursion returns `e/h=(1/2,2/5)` and certifies `E[N]≤10/9`; constant-rate uniformization on the same instance returns the same expectation with the bound `5/3`. This is an exact finite-state algebra check, not a measured path-simulation speed comparison.

## Countably infinite sinh branching

For `F(u)=κ²sinh(u)`, tangent `V=κ²cosh(v)`, and `A=abs(tanh(v))`, the normalized coefficient sums satisfy

`Σ abs(c_m)h^m/V = A(cosh(h)−1)+sinh(h)−h`,

`Σ m abs(c_m)h^(m−1)/V = A sinh(h)+cosh(h)−1 ≤ exp(h)−1`.

Thus `abs(r)/V≤δ`, `0<h<log(2)`, and `δ≤2h+1−exp(h)` give a valid event law and subcriticality. The killed-tangent expected-node bound becomes `1/(2−exp(h))`; the original fixed-rate bound is `Λ/[λ(2−exp(h))]`. An admissible radius exists for `δ<2log(2)−1≈0.3862943611`.

The infinite-degree selection is well-defined in the ideal real model. Conditional on a nonlinear event, accumulate the positive even/odd factorial weights in increasing degree against the known total mass `[A(cosh(h)−1)+sinh(h)−h]/h`. The partial sums increase to the total; every uniform variate below one is crossed at a finite degree, so selection terminates almost surely. The conditional mean degree is a mass-weighted average of `h coth(h/2)` and `h(cosh(h)−1)/(sinh(h)−h)`, each below four when `h<log(2)<1`. The even bound follows from `tanh(h/2)≥h/4`; the odd bound follows by expanding

`4(sinh(h)−h)−h(cosh(h)−1) = h³/6 − Σ_{k≥2}(2k−3)h^(2k+1)/(2k+1)! > 0`.

The script [sinh_degree_audit.py](sinh_degree_audit.py) tested 12 `(h,A)` pairs and five fixed unit variates per pair, including `A=0` and `h=log(2)−10⁻⁶`. All selector loops crossed and all stated float-tolerance assertions passed. At `h=0.01`, direct `cosh(h)−1` / `sinh(h)−h` evaluation differed from the degree-100 factorial sum by up to `8.4×10⁻¹⁵`, and the computed worst-case event mass was `1+2.1×10⁻¹⁴`; the script allows these ordinary-float residuals and does not outward-round them. These checks do not provide finite-bit exact categorical sampling, outward-rounded transcendental bounds, or an exact killed diffusion implementation. The source sinh extension is analytical; the supplied code only implements a finite quartic case.

## Representation-specific uncentered separation

For the supplied model, the uncentered identity is `u=(-d²+1)⁻¹(s−25u⁴)`, with `s=26+10g≥16`. In the specified independent-product signed branching expansion, a uniformly finite absolute first moment `m` would have to satisfy `m=(-d²+1)⁻¹(s+25m⁴)`. Positivity and preservation of constants by this resolvent imply, for `w=inf_x m(x)`, `w≥16+25w⁴`. This first forces `w≥16`, after which `25w⁴>w`; contradiction. The source's separation is correct for that representation. It does not exclude centered/tangent-resummed samplers, Newton, MLP, alternative branching laws, or deterministic solvers.

## Independent checks and implementation boundary

- The copied exact-rational verifier passed both supplied certificates. At predictor A, its exact enclosure slack is `327/4096` and `Γ=5425/128<101`; at predictor B, the exact slack is positive and `Γ≈3.841152025655375<λ≈80.56267184225563`. Radius `1/20` fails enclosure; radius `3/10` passes enclosure but fails `Γ<λ`.
- The independent CTMC case in [exact_cases.json](exact_cases.json) uses only rational arithmetic and asserts the exact sampler recursions, endpoint kernels, categorical validity, subcriticality, work bounds, and the uncentered contradiction.
- The copied source was run for a bounded 2,000 samples per predictor after removing only the Numba import and its two decorators. Both sample means landed inside the ideal Hoeffding widths relative to the converged FFT number: predictor A estimate `1.0217001789450373`, difference `+0.00082919`, ideal half-width `0.00759202`; predictor B estimate `1.0208431240656965`, difference `−0.00002787`, ideal half-width `0.00066810`. The FFT reference is not interval-certified, the simulation uses floating random variates, and this was not a Numba execution or a coverage test.
- Exact rational certificate arithmetic succeeds, but the runtime float constants are not outward-rounded. In predictor B, the reported binary-float `amp`, residual envelope, tangent upper bound, `B₂`, and `B₃` each fall slightly below their exact rational expressions (largest listed gap about `2.55×10⁻¹⁴`); the runtime proposal rate is therefore not itself a rigorous certificate. The independent exact certificate has positive margin, and no actual path-level probability violation was observed in the bounded replay.
- The copied source accepts `p₁` down to `−10⁻¹²` and an event total up to `1+10⁻¹²` before raising. A static predicate probe shows that a synthetic invalid total `1+5×10⁻¹³` passes that guard. A direct run with deliberately supercritical synthetic branch parameters was interrupted; it is not evidence about either supplied valid certificate. The tolerance can silently turn a small invalid categorical mass into a finite-precision law different from the proved one, so an interval-validated implementation should reject or outwardly certify these boundaries.

## Literature and novelty boundary

**Agarwal & Claisse (2020).** Their accepted 2020 manuscript gives the standard branching diffusion representation (Section 2.2; Section 3.1) and explicit `L^q` integrability conditions in Section 3.3. Proposition 3.4 uses a nonnegative supersolution satisfying `Lw+β(Σ |c_l|^q/p_l^(q−1) w^l−w)≤0`; its `q=1` constant-supersolution criterion is a majorant-based first-moment bound. This is particularly close to the source's probability-majorant mechanism. It is elliptic with bounded-domain absorption and its theorem is not automatically a proof for the source's periodic setup, but it rules out novelty claims for branching, signed weights, or supersolution-certified integrability as ideas. [Accepted primary manuscript](https://eprints.gla.ac.uk/210343/7/210343.pdf), DOI [10.1016/j.spa.2020.02.009](https://doi.org/10.1016/j.spa.2020.02.009).

**Bossy et al. (2015; v3 consulted).** Their nonlinear Poisson–Boltzmann section explicitly represents a `sinh(u)` bulk equation with odd offspring probabilities `p_(2k+1)=1/(2k+1)!`, `p₀=2−sinh(1)`, and mean offspring `cosh(1)−1<1`, giving almost-sure extinction. They explicitly caution that expectation integrability can fail to be easy to establish for larger boundary data, and state that variance is not fully analyzed. This is direct prior art for countably infinite sinh branching; it does not establish the present residual-to-tangent eligibility or bounded local returns. [Primary arXiv version](https://arxiv.org/html/1411.2304v3).

**Fan, Sun, Yang & Lu (ICLR 2026, SCaSML).** Their Fact 2.3 derives a semilinear parabolic PDE for the error around a pretrained surrogate; Sections 2.3–2.4 use MLP at inference time, and Theorem 2.5 bounds global `L²` error by a product of simulation error and surrogate error. Their problem is finite-horizon parabolic and the correction estimator differs from this stationary pointwise bounded tree, but the high-level “surrogate then stochastic correction” idea and defect-PDE derivation are already published. [Official ICLR proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/cf8353a0efc3644454a5591a7cb55c17-Paper-Conference.pdf), [OpenReview copy](https://openreview.net/pdf?id=d2pUyiXwcm).

**Beck, Gonon & Jentzen (2024).** Their Theorem 1.1 and refined Theorem 3.16 prove polynomial dimension and accuracy cost for a class of semilinear elliptic PDEs with a globally controlled Lipschitz remainder around a stabilizing slope, using an MLP fixed-point scheme. It is a needed comparator for claims about high-dimensional elliptic capability. Its stated class is not identical to the source's periodic quartic/sinh setting and it is not a matched implementation comparison. [Publisher article](https://link.springer.com/article/10.1007/s42985-024-00272-4), DOI [10.1007/s42985-024-00272-4](https://doi.org/10.1007/s42985-024-00272-4).

Taken together, these papers make the narrow theorem package the only defensible candidate novelty. Historical priority has not been established. No baseline-comparable timing, physical instance, acquisition cost, or certified implementation is available. The supplied one-dimensional test itself says a Fourier solve is much faster.

## Discarded capital route

Repository navigation using the literal search terms `branching` and `defect` led to N783, a retained-repair/carrier-reward dossier about hBN rather than nonlinear PDE sampling. Its dossier and notices explicitly concern a different physical state space and keep correctness/physical validation open. It supplies no applicable lemma or data for this theorem and is recorded only as a rejected lexical collision.

## Validation scope and next decisive test

The exact Fraction checks verify finite-state algebra and supplied rational certificate inequalities. The bounded replay checks code-path behavior against a numerical reference. The degree audit tests an ordinary-float inverse-series routine over a small deterministic grid. None validates arbitrary real-input exact sampling, interval-rounding, path-simulation cost, theorem priority, physical applicability, or superiority to deterministic/MLP baselines.

The next research gate is to provide a rigorously implementable killed-endpoint sampler with a total expected path-cost bound, interval-certified residual and tangent envelopes, and a matched high-dimensional benchmark against MLP and deterministic baselines that includes predictor construction and certificate acquisition. Without those, the killed-tangent improvement is a useful mathematical refinement, not an end-to-end performance claim.

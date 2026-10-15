# Zero-free Fourier factor and conditional sampling cost

This is a separate corollary of the independently frozen plateau construction and the subsequently audited sharpness proof. It does not change the frozen proofs.

## Exact scalar Fourier factor

Let G=1 on [0,2] and `2(s−1)G'=−G−G(s−2)` beyond 2, with `c=(2∫sG)^−1`. The scalar noise radius density is `2csG(s)`. Its radial characteristic function is

`φ(k)=(2c/k)∫[0,∞)G(s)sin(ks)ds`.

G is absolutely continuous, constant on [0,2], and strictly decreasing beyond 2. Its derivative has finite L1 norm, with `∫₂∞−G'=1`. Integration by parts therefore gives, for k≠0,

`φ(k)=(2c/k²)∫₂∞[−G'(s)](1−cos(ks))ds`.

The integrand is nonnegative, and `−G'(s)>0` on every interval above 2. For any nonzero k the zeros of 1−cos(ks) are discrete, so the integral is strictly positive. Also φ(0)=1 by probability normalization. Thus **φ has no real zeros**.

The Riemann–Lebesgue lemma applies to the L1 density −G', yielding

`k²φ(k)→2c` as |k|→∞.

Consequently `1/φ(k)=O(1+k²)` globally. This is a Fourier inverse of order two, rather than an inverse obstructed by real zeros. This is an elementary consequence of the constructed profile; it is not asserted to be a historically new Fourier criterion.

## An explicit global bound

On [2,4], `−G'(s)=(s−1)^(-3/2)≥1/(3sqrt(3))=:m`.

If 0<|k|≤π/4, the elementary inequality `1−cos x≥2x²/π²` for |x|≤π gives

`φ(k)≥224c/(9sqrt(3)π²)`.

For |k|≥π/4,

`∫₂⁴(1−cos ks)ds =2−[sin(4k)−sin(2k)]/k`

`≥2−2|sin k|/|k|≥2−4sqrt(2)/π=:D>0`.

Here sin(k)/k decreases on [π/4,π], while |sin k|/|k|≤1/π beyond π. It follows that

`φ(k)≥a/(1+k²)` for every real k,

where `a=2cD/(3sqrt(3))>0`. The small-k bound above is larger than a. A simple upper bound is `φ(k)≤min(1,4c/k²)`.

For |k|≥2 the sharper lower bound `φ(k)≥2c/(3sqrt(3)k²)` follows from the same interval integral and `2−2/|k|≥1`.

## Matched estimation comparison

The raw unbiased Fourier estimator `exp(i t·X)/φ(|t|)` has squared magnitude `1/φ(|t|)²`. Its asymptotic growth is `|t|⁴/(4c²)`, with an explicit global bound `(1+|t|²)²/a²`.

This improves the mathematical raw inversion behavior compared with the supplied Dickman law's real zeros. It does not improve the available qubit information. The output direction n is exactly recoverable, and the usual bounded report 3n estimates the Bloch vector. Then `tr[ρ exp(i t·σ)]=cos|t|+i sin|t| (t/|t|)·r` can be estimated from that same decoder without a frequency-growing deconvolution factor. Therefore the polynomial inverse is a representation property, not a quantum-information or matched-sample advantage.

Adding independent Gaussian smoothing of covariance εI preserves positivity and produces smooth scalar density with variance v_*+ε, but multiplies φ by `exp(−εk²/2)`. The zero-free property survives; the quadratic asymptotic inverse does not. This charge must be retained if smooth approximation is used.

## Ideal radius rejection sampler with an evaluation oracle

This paragraph gives a conditional classical cost, not a finite-bit implementation certificate.

Let `B_j=1/(2j−1)!!`, j≥0, with (−1)!!=1. Monotonicity and the renewal inequality give `G(2j)≤B_j`. On the interval `I_j=[1+2j,3+2j]`, the unnormalized target radial density

`q_0(r)=r[G(r−1)+G(r+1)]`

is at most `e_j(r)=2rB_j`. Its envelope interval mass is `w_j=8(j+1)B_j`. The total envelope mass E is finite and obeys E≤38, because `B_j≤3^(−j+1)` for j≥1. Sample j with probabilities w_j/E, sample r in I_j with density proportional to 2r, and accept with probability `[G(r−1)+G(r+1)]/(2B_j)`.

The target mass is `∫q_0=2J1=1/c`. Since `J1>∫₀⁴sG(s)ds=8sqrt(3)−28/3>9/2`, the acceptance probability is greater than 9/38. Thus the expected number of proposals is less than 38/9, **if exact G evaluations, continuous randomness and exact arithmetic are provided**.

The discrete envelope tail is factorial and has a conservative geometric upper bound O((j+1)3^(−j)). Hence a tail cutoff logarithmic in the inverse tolerated truncation error is sufficient. Numerical evaluation of G, interval comparisons in acceptance, random-bit generation, normalization of the envelope series, rounding, and control errors are separate unresolved implementation costs. Common output rounding is required for a meaningful finite-bit total-variation comparison with the continuous model.

The quantum part is unchanged: one input qubit, a uniform random measurement axis, and one projective spin measurement per shot. All added radius work is classical and state-independent. No hardware advantage follows from the conditional rejection bound.

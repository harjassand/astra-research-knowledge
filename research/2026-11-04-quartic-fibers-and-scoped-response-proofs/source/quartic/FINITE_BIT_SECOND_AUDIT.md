# Second independent audit: fixed-depth compilation and rounded sampling

Audited source: PROOF.md, SHA256 `4ccf075981c93b856d683a7d38c290341a861315fbae868de6bce3cfc64aff63`.

Date: 4 November 2026. Scope: sections 4.1–4.2, with the earlier algebra inspected for the hypotheses these sections require. Verdict: the stated fixed-depth Turing bound and finite-grid total-variation guarantee are supported. No blocking counterexample was found. This is a mathematical review, not an independently implemented sampler benchmark or novelty clearance.

## 1. Exact input and conditioning

Assume n >= 1, 0 < epsilon < 1, integer p >= 0, dense exact rational coefficients, and a fully successful certificate. A certificate that stops at a nonconstant residual is not covered. Depth d counts nonempty maximal Gaussian blocks; it is fixed for the polynomial-in-original-input claim.

Each stage can be implemented with determinant ratios or fraction-free elimination, followed by direct fixed-degree polynomial substitution. The matrices may have polynomially many rows but at most n columns; relevant nonzero minors have order at most n. Clearing polynomially many denominators and expanding bounded-degree substitutions therefore gives a one-stage height bound polynomial in n times the current coefficient height plus log(n+1). Iterating d times proves n^(O(d)) height growth. It would not prove a uniform polynomial bound for arbitrary d.

A small positive pivot does not create an omitted real-condition-number parameter. A positive rational determinant or LDL pivot of height polynomial in n,H is at least 2^(-poly(n,H)); matrix norms are at most 2^(poly(n,H)). Thus all needed inverse and covariance-factor magnitudes have logarithms polynomial in certificate height. This does not imply practical good conditioning or tolerance to noisy coefficients. It only bounds the bit precision needed for exact rational input.

## 2. Square roots and complete transport evaluation

For Q = L D L^T with positive rational diagonal D, a covariance factor for (2Q)^(-1) is L^(-T) diag((2D_ii)^(-1/2)). Positive rational square roots and reciprocal square roots can be enclosed by rational bisection or integer-root methods. The lower bounds above ensure polynomial bit cost for any prescribed absolute accuracy. There is no hidden exact-real square-root oracle.

Here is a conservative way to make the transport-evaluation claim explicit. Let s be the number of arithmetic operations in the unexpanded transport; s is polynomial in n and d. On the enlarged latent cube, use the draft's recursive magnitude bounds to choose U >= 2 bounding every exact intermediate value and every primitive coefficient. The same fixed-degree structure gives log U <= 2^d poly(n,H,log(G_0+2)). Replace square-root constants by sufficiently narrow rational intervals and round every arithmetic result outward. By enlarging U by a constant factor, local errors at most zeta propagate through addition and multiplication with total error at most s(4U)^s zeta. Hence choosing

zeta <= delta/[2s(4U)^s]

is sufficient for delta/2 coordinate error. The required precision is

O(log(1/delta) + log s + s log U),

which is polynomial in n,H,2^d,p,log(1/epsilon). Divisions by variable intermediate quantities are unnecessary: rational inverses are computed first, and the transport itself consists of affine maps, quadratic shears and Gaussian scaling. Large cancellation is therefore handled by absolute interval precision, not an unstated relative-error assumption.

This bound is deliberately loose. It establishes bit complexity, not an efficient numerical implementation.

## 3. Tail truncation and rounding boundaries

The target must remain Round_Delta(X), with Delta=2^(-p). A finite-bit law has TV distance one from the original absolutely continuous law; the proof does not make that mistake.

On the latent cube the transport produces ||X||_infinity <= R. Because the fully accepted transport is a global bijection and its positive quadratic coordinates can all be zero simultaneously, min V=c. Thus the maximum normalized density is indeed exp(-c)/Z, with the cancellation of exp(-c) leaving the stated determinant product. Its logarithm is bounded from rational heights; the constant c need not be numerically exponentiated.

The number of coordinatewise rounding hyperplanes crossing the output box is bounded by n N_grid. Their delta-neighbourhoods have total volume at most 2 delta n N_grid (2R+2)^(n-1). Multiplication by a global density bound is a valid, albeit potentially very pessimistic, probability estimate. No independence of output coordinates is assumed. N_grid and the box-volume bound can be represented and multiplied in binary; the algorithm does not enumerate exponentially many grid cells.

If the latent approximation error is at most delta/(4L) and transport-evaluation error at most delta/2, the final coordinate error is at most 3delta/4. Outside the true sample's delta rounding-boundary neighbourhood, the exact and numerical outputs therefore round identically. Gaussian-tail, numerical-generation and boundary events are separately charged. The coupling inequality gives the claimed TV bound, with the stated slack.

Adversarial checks do not invalidate this argument. A Gaussian centred exactly on a grid boundary can have substantial boundary mass at a fixed numerical tolerance, but the global density bound forces delta to decrease with its inverse width. A huge translated mean increases log R and the bit count, not the number of cells the algorithm visits. Near-singular rational covariance increases the required precision only polynomially in H. None of these cases permits a fixed machine-precision implementation, which is not claimed.

## 4. Finite rejection and worst-case runtime

For G_0 >= 1, a uniform proposal on [-G_0,G_0] accepted with probability exp(-y^2/2) has acceptance probability greater than 1/(2G_0). A cap B = ceil(2G_0 log(64n/epsilon)) therefore makes the union of exhausted-coordinate events at most epsilon/64. Deterministic fallback after the cap is permitted only because this event is included in the error budget.

Couple dyadic proposal and acceptance uniforms to exact uniforms. Proposal positions differ by at most 2G_0 2^(-b). The derivative of exp(-y^2/2) has absolute value at most one, so threshold perturbation, uniform quantization and elementary-function rounding alter a decision only in an interval of probability O((G_0+1)2^(-b)). A union bound over nB proposals is sufficient. For example, taking b larger than both log_2(2G_0/eta) and log_2(1024 nB(G_0+1)/epsilon), plus a fixed safety margin, provides the required location and decision budgets. These are logarithmic precision requirements.

The exponential is evaluated only on arguments of magnitude O(G_0^2), with G_0 = O(log(n/epsilon)). Standard range-reduced series with rigorous remainder bounds therefore use polynomial bit work. The capped proposal count, random-bit count, elementary-function evaluations, transport evaluation, rounding and output length are all polynomial in the listed parameters. No unbounded retry loop or hidden grid traversal remains.

The coupling to the full Gaussian law additionally pays the truncated-normal tail. Conditioning each independent coordinate on the interval is legitimate and differs from the full joint Gaussian by at most the union tail probability. It does not require computing the Gaussian normalization constant in the sampler.

## 5. Output size and established baselines

The rounded output length is O(n(p+log(R+2))) on successful generation, and fallback output is finite. This explains why fixed depth is essential for ordinary positional outputs. The draft's iterated-squaring example correctly leaves unbounded-depth fixed-point sampling outside the uniform polynomial claim. The runtime is polynomial in p, not necessarily in the binary encoding length of p; writing p fractional bits already makes that convention necessary.

Existing supplied-representation methods are strong baselines. Pagani et al.'s Hybrid Rosenbrock distribution has known normalization and direct efficient independent sampling, explicitly established in the primary article: https://doi.org/10.1111/sjos.12532 . Thus Gaussian conditional sampling after a triangular model is given is not a new operation.

Welch, Zhang and Uhler already study hidden additive-Gaussian causal factors under linear mixing and layer-wise recovery from observational information, with a score-based quadratic-program method: https://arxiv.org/abs/2410.23620 . Carlini provides effective essential-variable reduction for homogeneous polynomials: https://arxiv.org/abs/math/0507531 . These primary sources support the draft's narrow positioning. This audit does not establish that their full algorithms are or are not equivalent to the proposed exact coefficient interface on every overlapping instance.

The defensible result is exact coefficient-to-transport compilation for the accepted class, with polynomial Turing compilation and a specified rounded-output sampler at fixed depth. It is not generic quartic sampling, robust learning from noisy observations, uniform polynomial runtime at arbitrary depth, or a demonstrated scientific workload advantage.

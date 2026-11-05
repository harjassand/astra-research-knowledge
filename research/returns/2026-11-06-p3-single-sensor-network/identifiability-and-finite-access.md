# Exact-law identification and a separate finite acquisition contract

These are claims visible in the [incomplete P3 prefix](P3_SINGLE_SENSOR_NETWORK_20261106_RETURN.txt). The complete return and research package are unavailable; no new Capital proof check or original-literature review was performed.

The impulse profile from physical coordinate `j` is `h_j(t)=e₁ᵀ exp(At)e_j 1_(t≥0)`. The supplied proof credits **Kabluchko–Stoev's uniqueness theorem for minimal spectral representations of infinitely divisible processes**, then reports verifying its conditions for the local source model. Causal analytic profiles fix onset within the exact-law representation, and observability makes coordinate profiles linearly independent. Matching profile directions gives monomial similarity of drifts. Derivatives and source onsets occur in this identifiability argument; they are not observation oracles or event labels supplied to the finite algorithm.

For reciprocal drifts, the monomial scale matrix must commute with the drift through its squared diagonal scales. Nonzero edges force adjacent scales to agree; the source uses observability to obtain connectivity. A common scale cancels from similarity, and positive couplings remove relative signs. This is a drift-law conclusion under the stated physical-coordinate source structure, without identifying arbitrary nonlinear causality or the full hidden stochastic generator.

The finite reconstruction is **narrower** than the exact-law theorem. It uses independent symmetric compound-Poisson jumps `±a_j` at unknown rates `λ_j`, on a specified compact parameter class:

| Supplied promise | Role |
|---|---|
| Symmetric positive-coupling drift, `−R I ≤ A ≤ −α I` | Known stability and size bounds |
| `O_AᵀO_A ≥ s² I` | Quantitative sensor observability |
| `0<a_- ≤ a_j ≤ a_+`, `0<λ_- ≤ λ_j ≤ λ_+` | Nonvanishing source amplitudes/rates with upper bounds |
| `0≤GGᵀ≤qI`, independent Gaussian read noise with bounded unknown variance | Forward model and nuisance-parameter fitting |
| `E‖X₀‖≤B₀`, independent of future increments | Nonstationary start; no known reset or equilibrium preparation |

The record does not certify an arbitrary apparatus's source independence, locality or read-noise law from the same scalar data. These are acquisition assumptions.

Measurements are bounded features `cos(Σ θ_l Z(t_l))`. Their stationary means are computed from candidate parameters using the Lévy characteristic exponent, Gaussian covariance and read-noise term. Matrix exponentials, cosines and finite integrals are evaluated with certified finite-bit error, with explicit bounds on the infinite tails. This is forward modelling, not access to the unknown plant's impulse response.

The procedure enumerates rational time packets and Fourier coefficients. Rational parameter boxes, real-algebraic feasibility decisions, interval feature bounds and continuity estimates eventually certify a finite list of `J` features and a positive margin `Δ` separating drift orbits at the requested accuracy. Exact-law identifiability plus compactness supplies termination. **The inverse modulus and margin are constructed rather than assumed as free input**, but the search and final candidate net can be enormous. No polynomial-time general inverse is claimed.

One physical trajectory supplies the measurements. In the proof, auxiliary truncated-history packets on disjoint driving intervals are independent; the physical system is never reset. Stability controls history error by a term proportional to `exp(−αL)`. The prefix gives a conservative sample count `N≥2048 Δ^−2 log(8J/δ)` for the bounded-statistic estimates, with history length, feature packets, numerical evaluation and ADC/clock budgets also paid. This is not a claim that `N` alone is the total cost for every feature list.

Finite ADC range/resolution, clipping probability and bounded exogenous clock error are included. Read noise stays fixed rather than becoming an exact-data oracle. A finite candidate fit then estimates the drift up to hidden-node permutation. The general reconstruction is constructively specified; the reported implementation is the explicit two-hypothesis assay on the [cost page](assay-costs-and-obstructions.md), not an end-to-end implementation of every compact-class inverse problem.

[Overview and collection boundary](README.md)

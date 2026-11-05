# Targeted prior-art and source-runtime check

Date: 5 November 2026. Scope: an exact, size-independent local-channel preimage for all fixed-temperature 1D Gibbs states; uniformly full-rank bounded-block mixtures; and physically noisy global-state preparation. This is a targeted check, not an exhaustive priority determination.

## Search performed

Both available search engines were used, including primary-source restricted queries and unrestricted queries followed by primary full-text inspection. Representative query families were:

- “Gibbs states” “preimage” noise “one-dimensional”
- “Gibbs states” “full-rank” “block” mixture
- “thermal states” “inverse depolarizing”
- “Gibbs” “local noise” “inverse” positivity
- “Gibbs states” “interior” separable block
- “thermal state” “local noise” “preimage”
- “one-dimensional” “Gibbs” “full rank” “mixture”

The retrieved primary literature did not contain a statement of the precise uniformly interior block-mixture / all-temperature local-channel preimage theorem proved in the companion note. That observation supports presenting the construction and consequence; it does not justify a claim of exhaustive priority.

## Closest mathematical comparisons

### 2609.35973 and 2602.13386

Pilatowsky-Cameo, Styliaris, Bakshi and Malz, *One-dimensional quantum Gibbs states in constant circuit depth*, https://arxiv.org/pdf/2609.35973 . Exact all-temperature pure bounded-block mixture and polynomial classical sampler are already established. The proof has full-rank intermediate QPI factors, but its final block construction introduces rank-one spectral factors. The new proof preserves a floor through that step; this is the exact point at which it goes beyond the quoted source theorem.

Bakshi, Choi and Pilatowsky-Cameo, *Entanglement in quantum spin chains is strictly finite at any temperature*, https://arxiv.org/pdf/2602.13386 , v2 of 2 November 2026. This earlier source supplies the local invertible dressing and a polynomial sampler for bounded-bond MPS mixtures. Its general all-temperature statement is not a uniformly full-rank block mixture.

### 2607.28536v2 — stronger high-temperature comparator than BLMT alone

Putterman, Zlokapa and Cotler, *When quantum thermal states look classical*, https://arxiv.org/pdf/2607.28536 , v2 of 5 October 2026.

Theorem 2 covers long-range Pauli Hamiltonians of locality k and bounded total absolute strength s at every site. For beta<=1/(4096 e s k), it samples pure product stabilizer states whose mean approximates the Gibbs state. The stated runtime is approximately

    n |A| k + k n^11 epsilon^(-5) log |A|

up to logarithmic factors. The separability threshold is tight in its s,k scaling; the paper improves the older BLMT temperature regime and removes bounded-degree geometric restrictions. It still concerns high-temperature pure product preparation, not an all-temperature 1D uniformly full-rank block theorem. Its coefficient bounds are potential raw material for improved high-temperature robust palettes. No new claim about that extension is needed for the present all-temperature construction.

Primary full-text locations: Theorems 1–2, equations (22), (24), (28)–(31); Sections 3 and 6.

### Generic precompensation and quasi-local noisy steady states

Zhang et al., https://arxiv.org/pdf/2309.01434 , give general known-channel precompensation and SDP optimization. They do not prove a size-independent positive inverse for every 1D finite-temperature Gibbs state or a polynomial algorithm exploiting bounded blocks.

Arad, Firanko and Gurevich, https://arxiv.org/pdf/2408.08672 , study local channels whose steady-state logarithms admit local perturbative expansions. The generic exponentially controlled coefficient bound needed for full quasi-locality is additional, and their constructive local-observable results do not invert a specified many-body target. This is related machinery, not the same operation.

## Strongest ideal 1D preparation comparator found

Rouzé and Stilck França, *Rapid mixing of Gibbs samplers via quantum Dobrushin–Shlosman conditions*, https://arxiv.org/pdf/2610.03578 , 2 October 2026.

This is stronger than comparison only to high-temperature samplers. Theorem 5.1 proves logarithmic trace-norm mixing at every fixed finite temperature for finite-range 1D noncommuting systems. It builds exactly Gibbs-preserving block channels from local Gibbs resets, quantum belief propagation and KMS completion. Normalized mixing bounds have single-exponential dependence on beta times interaction strength. Theorem 3.11 supplies a digital circuit with

    C N(1+t)[1+log(2N(1+t)/epsilon)]^a

elementary gates and classical bit operations. For Gibbs preparation t=O(log(N/epsilon)), this is N polylog(N/epsilon). The circuit-cost prefactor is doubly exponential in beta times interaction strength, as the theorem and Remark 3.12 explicitly acknowledge.

Its implementation inputs include bounded local terms, prescribed block rates/durations and construction parameters supplied to the required precision. Appendix B simulates each of polynomially many localized updates to error epsilon/(2K). Its perturbation-stability theorem concerns changes in the target Hamiltonian; it is not a theorem of exact target preservation under a fixed uncontrolled physical noise channel, nor a local-noise preimage construction. An ordinary FT controller may use this ideal sampler, but still receives its noisy raw output boundary. The new inverse-state representation may be used by an ordinary compatible controller too; no exclusive algorithmic or total-resource advantage is claimed.

## A genuinely noisy thermalization comparator

Brunner et al., *Lindblad engineering for quantum Gibbs state preparation under the eigenstate thermalization hypothesis*, https://arxiv.org/html/2412.17706v3 , Quantum 9, 1843 (2025).

The full noise analysis is relevant and should not be dismissed based on its abstract. Section 6 assumes an ideal convergence bound ||rho_M-sigma_beta||_1<=B exp(-alpha M), interleaves a probabilistic noise channel of total strength lambda, and proves the asymptotic bound

    ||rho_tilde_infinity-sigma_beta||_1
       <= B lambda / [1-(1-lambda) exp(-alpha)].

This establishes useful resilience and a noise-dependent residual error; it does not yield arbitrary global accuracy at fixed lambda. Its efficiency relies on ETH conditions. Section 7 further studies algorithmic errors and local depolarizing gate noise numerically. It is a meaningful preparation alternative with a different guarantee.

Granet and Dreyer, https://www.nature.com/articles/s41534-026-01320-0 , explicitly distinguish their locally thermal preparation objective from an exact Gibbs state on the entire system. Their noise-resilient energy-temperature curves and hardware results are relevant to local-observable objectives, not a proof of the present global endpoint.

## Source sampler and bit-complexity accounting

The all-temperature block source must not be labeled near-linear. Its Appendix B inherits the first-stage sampling/backtracking procedure from Section 9 of 2602.13386 and promises polynomial(N,1/epsilon). Only the final fixed-alphabet forward-backward sampling phase is O(N) at fixed physical parameters.

Section 9 of 2602.13386 truncates QPI shells at a length logarithmic in N/epsilon. The resulting candidate space is polynomial, and its backtracking sampler invokes BLMT Theorem 5.8 through constant-factor distortion estimates, leaf-weight evaluation and base-weight sampling. The distortion estimates use positive boundary operators and Gibbs/MPO trace approximations. The source's “exact leaf weight” wording describes its mathematical oracle; the papers do not separately display a tight Turing bit-complexity theorem for that first stage.

Accordingly, retain an opaque source cost P_(beta,r)(N,1/epsilon,ell_in), polynomial under the source's supplied computable/digital-input convention, rather than replacing it with the linear cost of the last stage. The new superblock matrices are constant-dimensional and the companion note gives their explicit finite-precision error rule. Their additional precision is O(log(N/epsilon)) plus fixed beta,r constants. This does not assert the same precision or near-linear work for the full inherited sampler.

The target H is supplied as a digital specification. It is not inferred from a fabricated holding Hamiltonian. Any approximation of digital coefficients must be charged as a separate input error; the Gibbs trace-norm derivative bound is at most 2 beta ||Delta H||, so N local coefficient errors can be budgeted directly. This is independent of acquisition of the physical output-noise parameters.

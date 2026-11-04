# Independent adversarial audit: arbitrary-graph current receiver

4 November 2026. Reviewed PROOF.md SHA-256: bc079e779e9dc3bc4584b2918ed79bf19370d1a3749f77e5491be5b5d7a1bd35.

## Verdict

The scoped partition-response approximation and coarse-current sampling result survives this independent review. No counterexample was found to the source-sector perturbation bound, exact-factor mixing argument, finite-trajectory comparison, annealing construction or counting constants. The proof does not require clipped empirical factors to be windable or their chains to mix. Avoiding that false inference is essential.

The result applies to finite hidden ferromagnetic planar blocks with the promised boundary identity, joined by a supplied arbitrary ferromagnetic assembly. It does not recover physical spin samples, unknown bulk normalization factors, an infinite-volume model, or a validated physical data/control interface. The polynomial bounds have large unoptimized overhead. Priority and practical advantage remain unestablished.

## 1. Normalization, ghost fields and defect sources

The final explicit definition of Z removes a possible ambiguity in hard identifications: each original block port remains a distinct spin, each assembly vertex has its own uniform spin, and attachments have factors 1+x_i y_v. Such a factor is twice a normalized equality indicator. Multiple ports attached to the same vertex therefore have known, not hidden, normalization factors. Converting to another convention must carry those factors. The stated Fourier contraction has empty-current contribution one.

A common ghost spin represents consistent positive fields. Summing it uniformly gives the same partition response as fixing it positive because the unperturbed assembly is globally spin-flip symmetric. This does not give the same unrestricted interpretation for mixed-sign fields.

Once active-side bits and a defect-wire set are fixed, every parity-side bit is determined. A defect flips the source parity at its spin vertex. Consequently a specified zero- or two-defect sector is the zero-source partition sum times a physical source correlation. If both defects touch the same spin, the source cancels and the sector equals the zero-defect total. Otherwise it is a two-spin source. Its nonnegative high-temperature expansion and bounded spin product imply a sector ratio in [0,1]. Summing over R=1+choose(H,2) sectors gives the asserted polynomial lower bound on the probability of no defects.

Tempering only active incidences has the claimed physical interpretation: block-port attachments acquire activity tau and each known two-leg factor acquires activity a tau². This preserves the source identity. Tempering parity incidences as well would be a different construction and cannot be substituted without a new analysis.

## 2. Exact-factor winding theorem and support

The cited result was checked directly in McQuillan's paper, including its even-windable circuit closure and the near-assignment chain. True block source signatures have finite nonnegative high-temperature realizations. Normalizing a signature by a positive scalar preserves its pairing witness. Coordinate activity multipliers preserve the witness because their product on two inputs is unchanged by exchanging differing coordinates. Tensor products also preserve it.

These statements apply to the TRUE signatures, not their empirical approximations. They give a witness at the coarse interface without requiring it to be constructed or supplied to the algorithm. Hidden volume therefore does not enter the invoked coarse-chain gap bound. Finite real-valued physical couplings are legitimate in the analytic witness and spectral argument even though the actual implementation uses rational approximations. On fixed finite graphs, zero activities and hard-coupling limits can be retained; no infinite-volume result is required.

The proof's distance-two proposal 1/L² is one-half of the cited 2/L² proposal. The half-lazy gap bound pi(Omega_0)²/(2L⁴), hence 1/(2L⁴R²), is conservative and correct. The source theorem works on positive support and supplies the needed connectivity when the perfect sector is nonempty. Here the all-zero assignment has weight one, so that sector is always nonempty. Zero-weight states can be assigned self-loops in a common ambient state space without changing the true supported chain.

For a start dominated pointwise by 3pi, its squared L2 relative-density error is at most two. Standard reversible L2 contraction therefore gives the stated TV upper bound exp(−gamma T). No minimum positive stationary mass is needed for this warm-start estimate.

## 3. The decisive empirical-error lemma

The absolute matching derivative of a Pfaffian minor at the true matrix is the residual true even moment, provided all selected endpoints occur in that minor; otherwise it is zero. Its sign can depend on the remaining subset, but its absolute residual moment is nonnegative. Repeated selected endpoints give zero. The finite Taylor expansion uses these derivatives only at the true matrix.

For each defect sector the proof introduces W_tau, the nonnegative environmental attachment-and-edge weight averaged over assembly spins, and V_tau, the same average with the defect-source product. Both have nonnegative Fourier coefficients. Pointwise |V_tau|≤W_tau because the inserted source is ±1 under a nonnegative weight.

Let U contain the selected derivative endpoints, and average all other port spins under their true block marginals. The sum of absolute derivative contributions is exactly the Fourier sum selecting U at those removed endpoints. Equivalently it is the expectation of the uniform-U projection E_U[x_U V_tau]. Its absolute value is at most the expectation of E_U W_tau. Finally uniformizing U removes Fourier terms whose coefficients and true block moments are nonnegative, so this is at most the true zero-defect partition Z_0(tau). This reasoning includes repeated port identifications and all tempering factors. It neither assumes independence within a block nor falsely treats a signed reconstructed neighbor as a physical environment.

Clipping a scalar approximation to [0,1] cannot increase its error relative to a true moment in that interval. Expanding the product error around the true nonnegative factors, then bounding each selected factor error by its full Taylor envelope, yields the joint matching expansion. Its total coefficient envelope is at most exp(D)−1, with D counted over all block occurrences. Thus each defect sector has the displayed L1 weight bound, and all R sectors have E/Z_total≤R(exp(D)−1).

This is substantially stronger than merely asserting closeness of one normalized partition function. It controls the entire state-weight discrepancy on the augmented chain space used by the algorithm.

## 4. Why clipping cannot justify a mixing claim

The four-port counterexample is valid. Keeping only the two crossing pair entries A13=A24=d makes the fourth Pfaffian negative. Clipping leaves positive values only on the empty set and those two pairs. For the two crossing-pair inputs, every pairing of their four differing coordinates contains a swap leading to a zero product. Nonnegative pairing-witness invariance would then force their positive product to vanish. Hence the clipped signature need not be even-windable.

The proof explicitly avoids applying the true-chain theorem to that signature. Nor does it claim spectral-gap continuity or rapid mixing for the empirical chain. A clipped chain could have extra components or traps; the finite-horizon comparison pays for their true-weight effect.

## 5. Robust kernels, zeros and annealing

The average kernel bound was independently derived. For a common symmetric substochastic proposal, the off-diagonal acceptance difference weighted by the true w_x is bounded by q_xy times 2|w_x−v_x|+|w_y−v_y|. Summing uses both row and column proposal bounds. The diagonal error is controlled by the off-diagonal sum, giving average TV at most 3E/Z. If v_x=0<w_x, the empirical self-loop still obeys the bound. States with w_x=0 have no true stationary weight. Thus deleted or newly introduced support is covered.

For a B-warm start, the TRUE trajectory stays B-warm. Telescoping the two T-step kernels and contracting all later empirical kernels yields 3BT E/Z. An approximate initial distribution contributes its existing TV discrepancy additively. Crucially, TV closeness is never promoted to pointwise warmness of the approximate trajectory. At each annealing stage, a conceptual exact previous stationary law is used for the comparison, while prior implementation error is carried in TV.

At tau=0 the base support is precisely all active bits zero with either no defects or two defects at the same parity vertex. Its size B0=1+sum_v choose(deg(v),2) and uniform weights are correct. The weight outside this support at tau_start is bounded by R[(1+tau_start)^H−1], using at most R completions of every active pattern and true factor values at most one. The chosen start makes this at most zeta/8.

Adjacent annealing values multiply every positive state's weight by a number between one and three. Their normalized laws therefore have the required 3-warm relation. The selected T satisfies exp(−gamma T)≤zeta/(16S), since its base-two logarithm upper-bounds the needed natural logarithm. The training budget D≤zeta/(288STR) makes each empirical trajectory error at most zeta/(16S). Adding initialization, mixing and comparison errors gives the stated zeta/4 before random-bit caps. Zero-stage calls and targets below the nominal start are explicitly covered.

## 6. Counting and perfect-current rejection

The counting ratios r_j are exactly known functions of active Hamming weight, in [1,3). Their true expectations telescope the augmented partition sum. The final perfect-sector probability is at least 1/R. The small-start approximation by B0 incurs at most epsilon/32 relative error.

Sampler error zeta=a/12 gives expectation bias at most a/4 using the conservative range-three bound. The stated 18/a² logarithmic sample count is more than sufficient for the remaining Hoeffding budget and the union bound over K+1 quantities. Each ratio's relative error is at most a, and the perfect-sector estimate's relative error at most Ra. Their product, including the initial approximation, has the claimed logarithmic error below epsilon/2. For epsilon≤1/2 this implies the stated multiplicative guarantee. A zero estimate cannot occur on the successful event. Independent fresh sampler calls justify concentration conditional on the common training event; correlated chain frames were not silently substituted for independent observations.

Perfect-current rejection is also valid: exact calls fail to hit the perfect sector after J attempts with probability at most exp(−J/R), while J approximate-call errors add by coupling. Returning the all-zero perfect current on total failure costs only that failure probability. The sampled objects remain COARSE currents, not physical spin assignments or hidden-bulk currents. No spin-sampling reduction is supplied by the proof.

## 7. Exact independent tests

An independent rational test used a four-port physical star marginal and a two-port physical ferromagnetic marginal. Two ports of the first block were hard-identified at one assembly vertex; the two blocks shared two other vertices. A known edge and a hard ghost-field edge completed the test. The empirical fourth Pfaffian of the first block was −7/10000, and an empirical pair in the second block was negative, so clipping genuinely changed both signatures.

At tau=1, 1/2 and 1/10, all 138 zero/two-defect sector cases were independently enumerated. Direct spin summation with the explicit equality attachments agreed exactly with the coarse source identities. Every sector bound, the clipped product-error envelope and three selected mixed matching-derivative bounds passed, including a derivative crossing both blocks. These tests specifically address the repeated-identification and multiblock joins. They complement the author's nonplanar K5 and finite-kernel checks; they are not substitutes for the uniform argument.

## 8. Statistical and bit-resource audit

The iid pair-estimation bound follows from Hoeffding for {−1,+1} variables and a union bound. Reusing a block summary requires counting its error at every occurrence. Assembly-dependent training precision is real: this theorem does not give one fixed-data interface for assemblies of unbounded size at fixed accuracy.

Exact empirical Pfaffians, clipping decisions, factor products, rational schedules and rational acceptance probabilities have polynomial bit lengths in the supplied parameters. The implemented algorithm never evaluates an inaccessible tiny true factor. Coordinate and subset choices, initialization and acceptance coins can all be bounded by capped unbiased-bit rejection. The deterministic total number of draws is polynomial, so a union-bound coupling controls their aggregate deviation using logarithmic caps. The runtime claim is therefore a bit-complexity statement with bounded execution time, not just an expected-time sampler or a real-arithmetic oracle.

This does not certify fixed machine-precision arithmetic; floating-point implementations would require their own rounding analysis. More importantly, the conservative polynomial exponents are large. Data collection, physical mixing and independent equilibrium preparation remain uncharged by the abstract iid oracle. Hidden-volume independence refers to interface computation and the conditional number of independent snapshots, not to the cost of producing those snapshots in a physical bulk.

## 9. Strongest baseline and significance

[McQuillan's winding construction](https://arxiv.org/abs/1301.2880) is the decisive exact-factor baseline. The matching decomposition, positive-support gap and near-assignment simulation are established. [Jerrum and Sinclair's ferromagnetic approximation algorithm](https://doi.org/10.1137/0222066) already handles specified arbitrary ferromagnetic graphs. The present proof does not establish a new classification of tractable explicit Ising models.

Approximate-kernel Monte Carlo is also established; see [Alquier, Friel, Everitt and Boland](https://arxiv.org/abs/1403.5496). A further relevant modern comparator is [Gaitonde and Mossel, On Algorithmic Robustness of Corrupted Markov Chains](https://arxiv.org/abs/2507.15176), which studies recovery under corruption using a restart distribution and spectral information. Thus robustness to an imperfect chain is not itself a new general principle. The finite-time lemma used here is elementary and proved directly; this audit does not assert priority for it.

The matched-data distinction is an unknown hidden block accessed only through noisy boundary samples. Its empirical Pfaffian factors can be signed and non-windable, so exact-factor winding is not immediately an implementable oracle. The specific sectorwise error bound and warm true-trajectory comparison bridge that gap without constructing a positive hidden realization. This is the earned end-to-end extension beyond the earlier planar contraction receiver.

An existing winding implementation equipped with the same empirical factors and perturbation argument could implement the same operation. No benchmark or lower bound establishes practical superiority over the strongest adaptation of existing methods. Priority for the assembled noisy-boundary result remains unresolved. Its legitimate conclusion is a conditional polynomial approximation scheme for relative partition response and coarse-current sampling on arbitrary supplied ferromagnetic assemblies, subject to the full stated structural and acquisition promises.

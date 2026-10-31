# Independent whole review: retained damped bosonic reservoir compiler
31 October 2026. Reviewer: independent mathematical review.

## 1. Verdict, meaning and exact source binding
PASS at constructive mathematical-existence level, after the explicit Dyson-phase repair described below. The finite-bit compiler receives the already reviewed canonical infinite-Fock vacuum process, and the separately received finite thermal-mode reduction, without assuming a source-path oracle, a Kraus oracle, a coherent stationary Perron state or an exponentially large reservoir matrix.

The complete actual author body was read at 21,159 bytes and SHA-256 ac4ff25cc9baa4d5eb1f53a9ed8321694064c9e1c4465a68308a4a261cbbdbe6. I then read the actual changed Sections 2 and 7, verified the final byte count and hash, and bind:
- damped_bosonic_reservoir_opening_20261031/BOSONIC_FINITE_BIT_COMPILER_RECEIVING.md
- 21,801 bytes
- SHA-256 494742b2ddddac34e4ef280aa7f8b0fd0996abf56a62d11b224e4c5a47f721bd.

I also read the complete root central construction IMMIGRATION_BRIDGE_FIRST_EVENT_COMPILER_CANDIDATE.md at 10,416 bytes, SHA-256 9800d44ae6bedc4ad3efa7abcf189331ec84372615e81a4f6fc9ca48882d7051. That precursor's unstated virtual Dyson phase is superseded by the final receiving body's explicit correction. No uninspected revision is silently included.

Binding received sources:
- INFINITE_FOCK_CONTROLLED_LIMIT.md: a250c6ff320d19e86f28406d432c698c54f4ff71c9cab5dfaa0b2681f04501a2.
- THERMAL_VACUUM_CONTROLLED_REDUCTION.md: 61085d944aa7d27aaea552582fb13eb02f26b50d42f847e31bd34296373c2403.
- Domain/thermal independent receipt: 1f88af1848bd3ad8587f5977da016a5c66e9ae746219c4a565146ecbd33f70ba.
- THINNING_IMMIGRATION_DEATH_BRIDGE.md: beb4cfb5a5ae77b096d712d12c7ebdbce1ad2a73de16ffebd1fab65bd444a458.
- Direct-bridge independent receipt: f72f88ccd27da4fe5e2679aa8fcc6a78069c16a2b0e8d22709d354022f0b7589.

The earlier finite-mode Chebyshev amplification and private-clock constructions are received as algebraic tools, not as automatic acceptance of this bosonic conjunction. The new finite-dimensional majorants, source and arithmetic bounds, error conversions and physical composition were checked here.

## 2. Exact model and controlled guarantee
After scaling physical time T to one, the finite model is
H_L = T H0 + sum omega_i n_i + sum sqrt(b_i ell_i)(U_i a_i^dagger + U_i^dagger a_i),
J_i = 2 sqrt(ell_i) a_i,
with b_i=Gamma_i T, ell_i=lambda_i T>0, omega_i=Omega_i T, and G=sum b_i. Each U_i is a contraction with actual controlled block-encoding access; it may be non-Hermitian, and different U_i need not commute. Its adjoint is obtained from the supplied inverse block encoding. Positive supplied normalizations can be conservative.

The process guarantee is uniform over system inputs, reference systems, retained records and arbitrary system instruments at prescribed intervention times. The reservoir and internal time/path records remain private. Actual instrument costs are external or added, not absorbed into a free-control oracle. Arbitrary adaptive intervention times and normalized rare postselection are not covered.

Zero-coupling modes initialized in vacuum are removed exactly. Positive coupling with zero damping is outside this parameterization. Small positive parameter scales are charged through their finite descriptions and precision requirements.

The reviewed domain theorem supplies a normal canonical infinite-Fock process, not a formal claim of uniqueness for every unbounded GKSL extension. Its sharp vacuum cutoff error is
2 sqrt((L+1) sum b_i ell_i) exp(G/8) 2^(-L/2).
Selecting L with this below the assigned budget requires L polynomial in G and logarithmic in rates and inverse error. The L-dependent logarithm in the prefactor is absorbed by an ordinary larger constant. There is no enumeration of the joint dimension (L+1)^r.

## 3. Necessary repair: interaction insertion phases
The initial receiving and central texts described U_i/U_i^dagger insertions, H0 intervals and number phases but did not state the factor -i for each Hamiltonian interaction insertion. Without it, the proposed no-jump block is wrong already at first order.

The final author source explicitly repairs this: SELECT applies (-i)^V, with V the number of RETAINED virtual birth and death events. Both raising and lowering contribute -i. Discarded candidate immigrants and padded slots contribute nothing. The final actual damping jump J_i contributes no additional -i. Computing V modulo four implements this phase exactly.

This repair is load-bearing, not cosmetic. The final receipt does not accept the earlier uncorrected word as written. The separate known-frequency phase still uses the virtual PRE-JUMP endpoint in an event arm, not the physical post-jump occupation.

## 4. Positive no-jump representation and finite entries
For each mode M_i=-2 ell_i n+g_i(a+a^dagger), g_i=sqrt(b_i ell_i), is a displaced negative number operator plus a scalar. Its positive exponential is well defined and has the stated normal-ordered formula. The finite endpoint sum follows by first lowering to an intermediate k, damping there, then raising:
E_i(m,n)=exp(c_i_exact) sqrt(m!n!) sum_{k<=min(m,n)}
 alpha_i^(m+n-2k) exp(-2 ell_i t k)/[(m-k)!(n-k)!k!].
The coefficients alpha_i and c_i_exact in the source have the correct factors of two.

The Perron transform has immigration b_i/2 and per-particle death 2 ell_i. Its endpoint-conditioned law is exactly the normalized positive Dyson path law. Independent per-mode paths, chronologically merged, give the shuffle expansion; noncommuting system insertions are never reordered. Ladder factors and damping intervals belong to the positive scalar weights. H0 interval evolutions, the corrected (-i)^V and the number phases form the selected contraction word.

A virtual path that crosses L is assigned zero, including paths that later return below L. This extracts the finite-cutoff Dyson series from the untruncated majorant without conditioning or resampling. Fresh block-success work for contraction products is projected only at the final good block; intermediate success is not asserted or postselected.

Normal ordering bounds compressed row and column sums by exp(c_i_exact+2 alpha_i sqrt(L)), and alpha_i is at most sqrt(b_i t/2). The supplied c_i therefore bounds every local row and column for t<=tau. C=product c_i<2 on the stated windows.

Finite factorial sums, stable expm1/series, nonpositive exponential differences and absolute term budgets give polynomial arithmetic. Large ell_i t does not require a loop of that size. Small entries do not require relative preparation precision.

## 5. Product row/column access without joint-state enumeration
The right and left local preparations have O(L) possible occupation values each. Their products prepare the required sqrt(E_i/c_i) amplitudes. Both sides include a global accepted amplitude sqrt(C/R), R=2, so the overlap is E/R, not E times an erroneous square-root normalization.

Left and right failure spaces have distinct tags and zero selected good block. Endpoint basis copying is reversible coherent arithmetic. Both sides append the SAME endpoint-conditioned bridge seed/transcript; independent seeds would give a different operator.

Local preparation errors are absolute isometry errors and telescope over r. For mean-word errors, if every endpoint block error is bounded by eta times its positive scalar weight, the vector-of-component-norms argument gives a weighted Schur bound controlled by the positive matrix's row and column sums. There is no union over exponentially many joint endpoints. These two error arguments must not be interchanged.

## 6. Physical jump factors and full first-event normalization
For a jump on mode i, B_i(m,n)=2 sqrt(ell_i) sqrt(m+1) E_i(m+1,n) for m<L, and the top output row m=L is zero. The bridge endpoint is m+1; the physical output is m. The ladder lowering factor is already in the matrix weight and must not be applied twice or omitted.

The identity aE_i=exp(-2 ell_i t)E_i a+alpha_i E_i gives both compressed row and column bounds. In the E_i a term the factor is at most sqrt(L); the alpha term contributes at most sqrt(b_i) after the physical jump prefactor. Hence the displayed local d_i and global w_i are safe.

The integrated squared envelope obeys
sum_i integral w_i^2 <=1024 r(L+1)+4096 G tau.
Adding R^2 and selecting the padded power-of-two A gives polynomial normalization. No factor exponential in r or L is hidden here.

The ideal object amplified is the COMPLETE first-event isometry: no-event K0(tau) together with all J_i K0(t) sqrt(dt) arms. Finite-cutoff Kraus completeness holds on arbitrary system/Fock inputs, not merely on vacuum. The physical post-jump state and all no-event reservoir coherences are retained.

Outer event times are drawn from the explicit uniform/truncated-exponential mixture proportional to w_i^2. Keeping mixture/type/uniform labels is a legitimate Kraus refinement. Only inner bridge work is unprepared. The common-uniform coordinate realizes the correct integral measure; it is not an assertion of total-variation proximity between continuous and discrete timestamps.

## 7. Direct source and finite precision
The accepted direct bridge supplies exact initial-survivor posteriors and independent dead-immigrant thinning. Its endpoint-free cap is 2rL+2 Poisson(Gt/2). The chosen Hcap/Kcap and finite CDF scans therefore have uniformly priced overflow, with no tiny endpoint denominator and no microscopic-rate event loop.

All posterior lists use stable relative log weights. Probability-list and CDF errors are allocated absolutely, with clipping and normalization to genuine finite distributions. Uniform-tail, retention-strip, endpoint and ordering cuts are explicitly paid. Candidate own birth/death correlations use their lifetime density; cross-particle and cross-mode pairs use the independent density bounds.

The lower outer duration t0 is derived from priced outer-uniform cuts and t_min. It is not an assumed minimum physical waiting time. All inner source draws use one fixed finite outer duration, avoiding recursive bridge-conditioning precision loss.

On the retained set, event ordering and cutoff flags are stable. On its complement, an arbitrary contraction or zero changes the INNER operator mean by at most twice the bad seed probability. In contrast, outer retained Kraus records require L2/square-root mass control. The author budgets use this distinction correctly.

The normalized outer event amplitude F_i=J_i K0/w_i has derivative bounded using ||J_i||, the finite no-jump generator norm, w_i>=64 sqrt(b_i), and |w_i'/w_i|<=2 ell_i. The stated bound is conservative. Small b_i and large rates/frequencies increase required precision logarithmically through the explicit bound, not the number of physical steps.

## 8. System and frequency timing
The occupation integral equals n_final t minus sum of signed virtual event times. In an event arm n_final is the PRE-JUMP occupation. Number phases are computed modulo 2pi with charged precision. Internal time rounding is bounded by the finite event cap times max |omega_i|; external duration changes are separately bounded through the full amplitude/future generator.

H0 interval errors telescope through contractions. Each coherent variable duration is compiled by binary controlled fixed-time evolutions, with all controls, slots and synthesis precision charged. A sum-of-path-durations observation is not used to claim an unearned additive coherent simulation cost. Selected U_i access pays the actual supplied selection cost; scanning r blocks is allowed and charged.

Known diagonal number phases admit arithmetic compilation with logarithmic magnitude dependence. This is not generic fast-forwarding of arbitrary system Hamiltonians. The resource statement still pays ordinary H0 evolution and supplied operator access.

## 9. Complete amplification and private-time composition
For B=V_first/A, B^*B=I/A^2. Attenuation by A sin(pi/(4A+2)), followed by A oblivious Grover iterations, exactly amplifies the ideal isometry. The rectangular-block selfadjoint dilation and noncommutative Chebyshev polynomial bound give good-block perturbation O(d_A^2 beta), d_A=2A+1. Unitarity gives leakage O(d_A sqrt(beta)). This is an operator argument, not a scalar singular-value derivative claim.

The deliberately small beta and the finite error-group allocations suffice. All O(A) base calls, inverses, attenuation synthesis and source work are included. The actual implementation remains unconditional CPTP, with failure/overflow fallback, rather than a normalized successful branch.

For the global comparison, augment the EXACT finite-L process with its emission counter and freeze after M jumps. Its generator norm is bounded by the displayed Lambda up to a fixed constant, independently of counter dimension. Thus its exact remaining-window channel is Lipschitz in elapsed time. A backward hybrid charges each local isometry error, representative-time error and skipped short window, then later prescribed instruments contract trace distance.

This comparison retains the physical reservoir but hides internal timestamps. It does not expose rounded time records to a consumer and then incorrectly assert diamond closeness. It also does not assume an emission MGF for the approximate algorithm: the exact process MGF pays the count cap. At most M plus the prescribed no-event window count controls the iteration cap.

## 10. Thermal receiving and scope
Thermal finite modes are first received through the reviewed doubled-vacuum representation. Its factor 2 nbar+1, doubled mode count, positive/negative known frequencies and adjoint raising operators are paid. The sharp cutoff and count estimate apply to that virtual vacuum model. They are not bounds on physical thermal heat or detector records.

The physical thermal receiving used full Gaussian thermal channels and the separately justified virtual splitting/domain limit. It did not compare finite heated physical cutoffs, assume finite physical M3, or suppress the actual total interaction-piece duration in the coarse splitting estimate. Those qualifications remain binding here.

## 11. Final resource claim and exclusions
The resulting simulator overhead is polynomial in
r, 1+G+h+p, supplied input/encoding/register lengths,
log(2+sum ell_i), log(2+sum |omega_i|), log(1/epsilon),
with small positive input scales, thermal factors, actual operator encodings, H0 simulation and consumer costs explicitly paid. Local occupation lists, capped marked-event arithmetic, tensor row/column preparations and amplification are polynomial; the joint Fock state space is not enumerated.

Adding sharp infinite-cutoff, exact-process count-cap, finite initialization, arithmetic, synthesis and private-clock errors gives the stated uniform controlled-output trace error after fixed safety allocations.

This is a mathematical-existence theorem, not executed code, an optimized gate count, a practical crossover, a general continuum bath-fitting theorem or an originality claim. It does not supply arbitrary adaptive intervention times, public bath trajectories, physical thermal heat statistics, unpriced nonstationary infinite-energy preparations, normalized rare-postselection guarantees or a free access model.

Ordinary ingredients include marked-Poisson bridges, normal ordering, positive majorants, factorized row/column block encoding, LCU, isometry amplification, finite-precision coupling and contractive channel hybrids. The accepted contribution here is their checked receiving conjunction for this stated retained-process interface; no claim of literature novelty follows from this correctness review.

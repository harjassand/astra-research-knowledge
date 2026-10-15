# N610 active audit: subgroup absorption over finite abelian groups

**Disposition: conditional mechanism supported by an independent reconstruction and exhaustive finite checks; practical capability gain NOT_ACHIEVED.** This note separates the capital's theorem from the derived extension and from executable checks. The extension is a candidate change to the sampler's representation and resource bound, not a new output law or a verified practical speedup. Novelty and independent external review remain open.

## Pinned source and audited claim

The source card `N610-rank-absorbing-stratified-exact-local-stationary-sampling` is marked `source_derived_unreviewed`. In capital snapshot `work/astra-capital-scientific-power-20261015` at `25fc24509a59aabee340b36b588c9e59a144253d`, the theorem and model are in `updates/CP/package/stratified_noise_absorption_research_package_2026-10-10/stratified_noise_absorption_research_2026-10-10.md`, SHA-256 `72e51b3a71b5ed01f54a0c602f027f86889ef9495fcfbde51119214588b9bc0b`. Lines 11–69 state the finite-field model, joint local stationary sampler, category-query bound and local-observable scope; lines 78–119 give rank absorption and exactness; lines 121–160 give complexity and tail details. The exact extracted proof ranges are `frontier/proof_ranges/91d9466cb528f1d467aeb99e.txt` (source lines 11–69) and `frontier/proof_ranges/cec139a105635d2ebc036205.txt` (source lines 78–161). The associated open gate is `G-CP-N610`.

The theorem's contract is essential: one category per site-time is shared across all layers and memoized; conditional on `Haar`, each layer receives an independent uniform state; same-layer dependence is affine and strictly one time-step causal; nonlinear forcing at layer `ell` depends only on strictly lower layers; parent, coefficient, residual, forcing-description, forcing-evaluation, address and random-bit interfaces are acquired and charged. Exact category probabilities require an exact sampler (rational probabilities suffice with ideal random bits). This is not a physical-randomness claim, full-state sampler, generic nonlinear network result, or full-system mixing bound.

### Independent reconstruction of the masking step

The same-layer pending coefficient at a site-time is fully aggregated before it is processed: all dependencies move from time `t` to `t-1`, and the resolver processes pending times in descending order. Thus when a Haar reset at time `t` is exposed, every still-unresolved same-layer source is at an earlier time. Conditional on the complete shared category field, that Haar value is independent of those older same-layer states. It is also independent of the entire lower-layer process: lower updates cannot read an upper-layer Haar value. The adaptive address sequence depends on exposed categories and deterministic coefficients, never on Haar values, so conditioning on that sequence does not bias them.

This independence is the decisive premise. A uniform summand alone is insufficient if it is correlated with the discarded term. With the premise, a uniform random element `U` of a subgroup `V` satisfies `U+Z \stackrel{d}= U` for any `V`-valued `Z`, even if `Z` depends on the shared categories or lower-layer states. The category field is not redrawn layer by layer: cached categories are reused, and Haar values remain independent across layers conditional on that field. A non-Haar cached category is processed using its original residual or gate meaning. This reconstructs the source's distributional erasure; it is not a pathwise equality or coupling.

## Derived finite-abelian-group theorem

Let `G` be a finite abelian group in additive notation, with composition length

\[
\lambda(G)=\sum_{p}\sum_j a_{p,j}=\Omega_{\rm arith}(|G|)
\quad\text{when}\quad
G\cong\bigoplus_{p,j}\mathbb Z/p^{a_{p,j}}\mathbb Z.
\]

Replace each scalar field state by an element of `G`; replace each same-layer scalar coefficient by a supplied endomorphism `A:G\to G`; retain a common site-time category across layers, independent uniform-`G` Haar resets per layer, sitewise residuals, and deterministic lower-layer forcing `G^{k\ell}\to G`. For any batch of `m` requested coordinates at arbitrary specified times and fixed layer count `c`, the same backward algorithm samples exactly the joint stationary output law. Its expected number `Q` of distinct fresh site-time categories obeys

\[
\boxed{\mathbb E Q\le
\frac{\lambda(G)m}{s}\sum_{j=0}^{c-1}
\left(1+\frac{\lambda(G)kc^2}{s}\right)^j.}
\]

Here `\Omega_{\rm arith}(n)` means the number of prime factors counted with multiplicity, not asymptotic big-Omega notation. For `G=Z/MZ`, `lambda(G)=\Omega_{\rm arith}(M)`. For `G=Z/p^aZ`, the rank multiplier is `a`; the displayed bound is polynomial in `a=log_p|G|` for fixed `c,k,s`. This is a bound for the direct subgroup representation. It is not a lower bound on other algorithms, and the source's more conservative generic finite-field bound is not shown to be tight.

**Proof sketch.** At one layer, a batch of `r` outputs takes values in `G^r`. A currently unresolved source `z` contributes through a homomorphism `phi_z:G\to G^r`; for the cyclic ring prototype this is `x\mapsto v x` for a coefficient vector `v`. Maintain the additive subgroup `V\le G^r` generated by the images of exposed independent Haar values.

* If `im(phi_z)\subseteq V`, erase the dependency without querying its category: its contribution is always in `V`, so the independent uniform `V` summand masks it.
* At a Haar category, `phi_z(U_G)` is uniform on `im(phi_z)`; adding it to an independent uniform `V` gives a uniform element of `V+im(phi_z)`. The subgroup strictly grows because the query was not already masked.
* At a residual category, add the known image of its fixed value. At a gate, retain the lower-layer forcing term and propagate each endomorphism-composed coefficient to the parent at `t-1`.

Every strict subgroup chain in `G^r` has length at most `lambda(G^r)=r lambda(G)`. Thus fresh Haar discoveries at a layer are bounded by the number of Bernoulli-`s` category trials required for at most `r lambda(G)` successes. The source's lower-prerequisite count gives `r_ell <= m+kc^2 sum_{j>ell} F_j`; iterating the resulting negative-binomial means yields the box bound. Conditioning on the full shared category field and applying the temporal/layer independence above proves exact jointness inductively. The proof uses no inverse of a nonunit.

For a finite `N`-site chain, identify the output law with the unique stationary law by starting the forward process from an arbitrary state `T` updates before the earliest requested time. A certificate that closes within that horizon makes the requested conditional law independent of the starting state; the negative-binomial recursion has a finite exponential moment for fixed `c,k,s,lambda(G)`, so the probability of a certificate reaching past the horizon decays exponentially. The finite-horizon output laws are uniformly Cauchy on every fixed batch and converge to a stationary marginal. Since simultaneous Haar reset of all `N` sites has positive probability `s^N`, the finite chain has a unique stationary law, which is that limit. This argument does not make separate sampler invocations a pathwise-consistent finitary realization of one global process.

For `Z/MZ` and a batch of `r` outputs, the prototype represents a subgroup as a lifted integer lattice `M Z^r <= L <= Z^r` with a full-rank HNF basis `B`. Membership is exact because `v` is in the represented subgroup iff `B^{-1}v` is integral. Adding a Haar image adjoins its generator and recomputes HNF. A uniform subgroup draw is `Bz mod M` for uniform `z in (Z/MZ)^r`: the map is a surjective homomorphism onto `L/MZ^r`, hence has equal-size fibers. The checked-in prototype implements this cyclic-ring specialization only; a normal-form implementation for arbitrary finite abelian `G` remains to be built.

### Relation to the producer's digit sampler

For `Z/p^aZ`, base-`p` digits convert a ring update into `a` field-valued triangular levels per original level. At digit `d`, multiplication by a fixed coefficient contributes `(A mod p)` times the parent digit `d`; lower digits and the strictly lower original-layer forcing determine the carry. Therefore the original N610 field sampler already samples the same output interface. The new construction is a direct subgroup representation with a different upper bound, not an operation inaccessible to digit expansion.

Applying the source theorem mechanically to `a c` digit levels and `a m` digit targets gives

\[
\mathbb E Q_{\rm digits}\le
\frac{a m}{s}\sum_{j=0}^{ac-1}
\left(1+\frac{k(ac)^2}{s}\right)^j,
\]

whereas the direct subgroup theorem gives

\[
\mathbb E Q_{\rm subgroup}\le
\frac{a m}{s}\sum_{j=0}^{c-1}
\left(1+\frac{a k c^2}{s}\right)^j.
\]

For fixed `c`, the latter is polynomial in `a`; the former is only the source theorem's loose generic bound and may be sharpenable by a digit-aware proof. The direct bound is the only mathematical gain established here. It does not prove that the subgroup method uses fewer actual queries on every input, beats an optimized digit implementation, or is optimal.

## Executable prototype and comparison

`n610_ring_sampler.py` is a local prototype for `G=Z/MZ`; it uses exact integer HNF through SymPy. `ModularModel.check()` is metadata-only O(1). Parent lists, layer coefficients and residual states may be supplied as callables and are validated only when touched; the sampler does not enumerate or retain an `N`-site model. `implicit_model()` is a succinct deterministic local oracle for `N=1,000,000`. The callback example measures local query count, not real-world acquisition or network latency.

The matched finite instance is `n=2,c=2,M=4,k=3,s=1/3,r=1/6`, with shared ancestors, nonunit coefficients, residual resets and nonlinear lower-layer forcing. The exact reference is independently built by the forward update rule on all `4^(2*2)=256` states and solved numerically; its stationary residual is `1.11e-16`. The target is the joint law of three distinct same-time coordinates. Each sampler uses 3,000 reproducibly seeded draws.

| Sampler | Empirical TV to matrix reference | Mean fresh categories | Parent incidences | Forcing/carry callbacks | Time |
|---|---:|---:|---:|---:|---:|
| Direct subgroup HNF | 0.0387 | 5.760 | 12.824 | 4.275 original forcing calls | 2.731 s |
| Pinned N610 base-2 digit expansion | 0.0501 | 7.013 | 29.357 | 9.786 digit callbacks; 3.253 original forcing evaluations after memoization | 0.476 s |
| Full causal dependency cone | 0.0464 | 7.907 | 11.795 | 7.863 | 0.064 s |
| Exhaustive pathwise global CFTP | 0.0529 | 6.439 | 2,496.768 | 1,664.512 | 9.151 s |
| Global CFTP using all-sites-Haar certificate | 0.0436 | 18.091 | 27.081 | 18.054 | 0.113 s |

The pathwise CFTP baseline samples the same per-site random maps and stops only when exhaustive propagation of the image of **all 256 initial states** gives a singleton. Its random-map coalescence is almost sure because an all-sites-Haar time is a constant map; it can also stop earlier. Its reported state-map evaluations average 824.149, with 63.919 additional image-composition lookups. The all-sites-Haar version is a weaker but cheap certificate. The exact source N610 digit sampler is the meaningful local incumbent: on this tiny case it is about 5.7x faster than the unoptimized HNF prototype; the plain causal cone is faster still. The subgroup code reduces some query counts but loses in measured wall time. **No practical speedup is established.** Empirical TV values are finite-sample diagnostics, not proof of exactness.

The implicit `N=1,000,000` callable-oracle example sampled two coordinates 60 times in 0.189 s, with means 14.633 fresh categories, 26.300 parent incidences and 8.767 forcing calls. This supports only the local software access pattern: each descriptor is generated from a short formula. It does not include a remote acquisition interface, nonconstant circuit-description costs, or hardware randomness.

## Acquired versus supplied resources; precise cost boundary

The mathematical theorem assumes supplied local access to `N`, a queried site's parent list and endomorphisms, its residual state, category probabilities, and a complete forcing circuit plus an evaluator. Each touched descriptor's access and bit length, every forcing-circuit acquisition/evaluation, category/address random bits, and group arithmetic must be charged. With a uniform bound on each such local cost, the expected query expression above gives a corresponding fixed-`c` polynomial expected operation-cost bound. With unbounded, site-dependent circuit sizes or oracle latencies, the expected *bit* cost may be unbounded even though `E Q` is finite. Site addresses cost `O(log N)` bits. No full input scan is part of the theorem or local prototype, but external descriptor acquisition is not free.

The prototype uses `random.Random` for reproducibility, not ideal physical randomness. Its subgroup arithmetic uses HNF and exact inverses over integers/rationals; these bit operations are included in wall time but not separated in a portable bit-cost profile. On the matched `Z/4` case they dominate and make the implementation slower than the digit sampler. The prototype's success does not demonstrate a useful device, a practical large-`a` speedup, or a new stationary-sampling capability.

## Reproduction, provenance and gates

The comparator is a byte-identical local copy of the pinned producer implementation: source `work/astra-capital-scientific-power-20261015/updates/CP/package/stratified_noise_absorption_research_package_2026-10-10/stratified_entropy_sampler.py`; copied to `dependencies/stratified_entropy_sampler.py`; both SHA-256 `22a1b2f5108b6c5e42a3b941ae9a974b03e890b3391ac909789adafc6ca2519c`. It is loaded relative to this worker folder, so the benchmark can replay from a disposable copy without the capital checkout. The local sampler and benchmark are separate files: `n610_ring_sampler.py`, `n610_ring_benchmark.py`; benchmark output receipt is `BENCHMARK_2026-10-15.txt`.

From the repository root, replay with:

```sh
python3 research/2026-10-15-foundational-capability-v1/workers/capital_routes/n610_ring_benchmark.py
```

Required runtime libraries are NumPy for the small numerical stationary reference, SymPy for exact HNF, and the Python standard library. Local source hashes at freeze: `n610_ring_sampler.py` SHA-256 `6c164a5b0f75236d04735b26df828ff4fb20d1311f55d0d459d7a6fb5a390286`; `n610_ring_benchmark.py` SHA-256 `9099e9a6051006f52cb88806daff138a78da8b3b313d093b51c37da8b213c074`; byte-identical dependency SHA-256 `22a1b2f5108b6c5e42a3b941ae9a974b03e890b3391ac909789adafc6ca2519c`; final benchmark stdout is saved in `BENCHMARK_2026-10-15.txt`.

### Independent audit and remaining gates

The separate, independent reconstruction and tests are recorded in `../abelian_sampler_audit/REPORT.md`. The auditor derived the masking argument before reading this implementation, then compared an independently written backward resolver with forward rational enumeration: 1,296 exact conditionals for one-time outputs and 3,888 exact conditionals for joint outputs across times, with zero mismatches; the exact averaged law also satisfies `pi P = pi`. Separately, 160 HNF subgroup extensions across moduli 4, 6, 8, and 12 passed 10,368 exhaustive membership comparisons. An instrumented `N=1,000,000` callable-oracle run made exactly the descriptor reads reported by the local counters. These results support the specified finite model and local-access correction; they are not an external proof of the general theorem, a scaling result, or novelty evidence.

The remaining gates are: independent external review of the generalized theorem; novelty and prior-art search for this composition-length absorption analysis; a sharper digit-incumbent bound and matched tests as `a,m,c,k` grow; optimized subgroup normal forms; and a complete acquired-interface/bit-cost ledger. The benchmark shows no practical speedup against the pinned digit sampler. Keep `G-CP-N610` open; the capital source card remains `source_derived_unreviewed`, the extension is a candidate result with internal audit support, novelty `UNKNOWN`, and campaign status `NOT_ACHIEVED`.

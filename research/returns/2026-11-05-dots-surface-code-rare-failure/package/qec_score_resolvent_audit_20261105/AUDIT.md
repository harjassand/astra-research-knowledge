# Independent audit: score-folded killed-resolvent proposal

## Verdict

The score-folded proposal, finite rational supersolution, exact sampler and final interval construction are valid for the fixed projected graph and integer-cost decoder, assuming ideal independent random bits and the stated exact minimum-weight decoder contract. No in-scope counterexample was found. This audit does not establish new statistical principles, general efficient scaling, or superiority over optimized splitting.

The sampler uses rounded dyadic independent graph probabilities. Its explicitly computed total-variation conversion budget is added to the final interval on both sides. The prior circuit projection audit remains necessary: this is one selected detector basis plus L0, uniform circuit depolarization/X flips at exact rational p=1/1000, with a fixed integer-cost decoder.

## Exact proposal proof

For edge e and marked fault bit b, let c_e be its integer decoder cost and let

w(e,b) = Pr(e=b) 2^[c_e(2b−1)].

A state records the oriented incoming edge, its fault bit, and cumulative score modulo N. The automaton forbids backtracking and strictly suboptimal clean-clean triangle segments. Those exclusions retain every simple canonical residual witness of a minimum-cost correction.

For a marked path, let S be its true cumulative score and r=S mod N, where 0≤r<N. At a right terminal, the desired terminal weight is t(r)=2^−r. Other boundaries have no terminal weight. Let T be the nonnegative transition matrix, including the next edge's marked weight and its score-residue update.

Suppose a positive finite rational table H satisfies H≥t+TH. Define:

- Initial state weight w(start)H(start), normalized by Z=Σstarts w(start)H(start).
- Transition probability w(next)H(next)/H(current).
- Terminal probability t(current)/H(current).
- Remaining probability is a null rejection.

For a completed marked path, the H factors telescope. Its probability before any further rejection is

Pr(path bits) 2^(S−r) / Z.

Reject S<0. Otherwise S−r is a nonnegative multiple of N, so thinning with probability 2^−(S−r) is valid and yields precisely Pr(path bits)/Z. This is why the true score must be retained in addition to its residue. No folded alias is silently identified with a different true score.

After drawing independent off-path noise and accepting only when the path equals the deterministic canonical witness, each failing full error configuration has one accepted representation, with probability Pr(error)/Z. Hence one trial is a Bernoulli experiment with mean P_failure/Z for the rounded graph law. Null killing changes acceptance efficiency, not the identity.

## Witness cover and deterministic stopping

A failure residual has an LR path. The deterministic selector gives a simple path P. Minimum-cost correction implies the weighted score on P is nonnegative by comparing the correction with its symmetric difference along P.

If two consecutive path edges are clean, both lie in the correction. A strictly cheaper triangle shortcut would improve that correction, so such a marked transition cannot occur in a canonical witness. Equal-cost shortcuts must not be pruned.

The sampler immediately rejects a repeated vertex. Every canonical witness is simple, so this removes no accepted representation and bounds every trial by the finite graph vertex count. There is no unaccounted finite-length truncation tail.

A mere finite supersolution does not universally guarantee stopping: T=[1], t=[0], H=[1] is a counterexample with an infinite closed walk. The actual implementation additionally has early-repeat rejection and an exact scalar certificate W≥1+TW. Here max W=17, giving weighted-norm contraction at most 16/17 independently of floating eigenvalue estimates.

## Independent certificate verification

`check_certificate.py` rebuilds every allowed transition directly from the graph, checks the probability quantization, and uses Python arbitrary-precision integers to verify the certificate independently of its C++ uint128 checker.

Results in `certificate_audit_results.json`:

- 24,340 oriented-edge/fault-bit states; modulus 64.
- All 1,557,760 folded-state inequalities checked.
- All 420,444 transitions checked against the graph and strict triangle rule.
- Every scalar supersolution inequality checked.
- Exact normalizer reproduced:
  2818187113480842400929869436333 / 1329227995784915872903807060280344576.
- Normalizer approximately 2.1201683401324154e−6.
- Conversion TV budget reproduced, approximately 8.790945194916001e−17, including original projection enclosures and rounding each merged edge probability to 2^−64.
- Largest intermediate product requires 118 bits; largest checked sum including terminal and rounding requires 122 bits. Thus uint128 arithmetic is safe on this actual input.

The table uses a 2^−52 grid and its certificate rounds terminal values upward when r>52. This is safe for constructing a supersolution only. The sampler correctly uses the exact terminal probability 2^−r/H: for r>52 it draws uniformly below U·2^(r−52) and succeeds only at zero. Using the rounded terminal weight without correction would introduce bias.

The generated graph and certified table hashes are checked by the sampler. The audit also reconstructs the automaton structure rather than assuming that the metadata describe the correct transition graph.

## Independent finite end-to-end tests

`finite_exact_audit.py` constructs a five-edge cyclic graph and an exhaustive deterministic minimum-cost decoder. It solves exact rational supersolutions with deliberate positive null slack, then enumerates the entire killed/repeat-rejected proposal tree and every underlying error pattern.

For N=1,2,4, with and without triangle pruning:

- Total proposal mass, including null and repeated-vertex rejection, is exactly one.
- Every completed marked path has the telescoping probability stated above.
- Z times acceptance is exactly the independently enumerated failure probability 53/1250 in all six cases.
- Negative scores, positive scores crossing residue periods, cyclic proposal paths, null killing, off-path noise and canonical selection are included.
- Deliberately substituting rounded terminal weights without their correction produces a biased answer, confirming that this is a real failure mode avoided by the production implementation.

Results are in `finite_exact_results.json`.

## Confidence helper

`confidence_fast.py` uses floating beta quantiles only as proposals. It then verifies each endpoint with exact integer binomial-tail inequalities, falling back to exact bisection if needed. A proposed endpoint need not be the closest grid point to remain valid; an inaccurate proposal can only make the verified interval wider or trigger fallback.

The finite audit performs 102 adversarial tests with beta quantiles replaced by NaN, zero, one, one-half and out-of-range values. All returned intervals retain the required exact outward inequalities.

For fixed n trials, outward Clopper–Pearson bounds [l,u] on acceptance imply [Zl,Zu] for the rounded model. Expanding both sides by the verified TV budget gives the stated original exact-rational circuit-model interval. Fixed sample size and seed are recorded before production. The seeded PRNG is reproducible, not a proof of independent physical entropy.

## Remaining boundaries

- Trusted exact integer-cost MWPM remains an implementation contract, independently checked on exhaustive smaller instances rather than formally verified for every large execution.
- The circuit projection does not preserve the discarded detector sector, and the decoder uses costs 4/5 rather than exact log-likelihood costs.
- The tiny projection/quantization TV budget is for exact rational circuit p, not the distinct literal binary64-noise simulator law.
- A finite certificate establishes correctness, not uniformly good acceptance. Known canonical-overlap counterexamples remain relevant.
- Pilot and production evidence should be distinguished; this report does not treat a pilot count as a precommitted confidence experiment.

## Reproduction

MPLCONFIGDIR=/tmp/mpl_qec_audit matched_decoder_runtime_recovery_20261018/venv/bin/python qec_score_resolvent_audit_20261105/check_certificate.py

MPLCONFIGDIR=/tmp/mpl_qec_audit matched_decoder_runtime_recovery_20261018/venv/bin/python qec_score_resolvent_audit_20261105/finite_exact_audit.py

## Completed production verification

The fixed 100,000-trial production run passed an independent instrumented replay. It reproduces every category exactly: 1,249 accepted; 15,559 nonsimple; 88 negative-score; 280 fold rejections; 49,495 nonfailures; 33,329 other witnesses; zero null outcomes. Mean path steps 17.0567, maximum steps 43 and maximum true score 74 also match.

All 84,073 decoder calls were independently checked for zero residual detector syndrome and original L0 parity, not merely the implementation's gauged cut. There were 34,578 original-L0 failures before canonical-path rejection. Every resulting witness satisfied the required nonnegative weighted score.

Reverse integer binomial sums verify the outward 24-bit acceptance bounds, including one-grid-unit sharpness. Multiplication by exact Z and expansion by the complete conversion budget reproduce the exact fractions and displayed **99.9% interval [2.409810660133688e−8, 2.902079702096728e−8]**. Results and all runtime dependency hashes are in `production_audit_results.json`; the replay is `verify_production.py`.

Verified frozen main sampler SHA-256:

7aeaf05c689488fc6c7809aaca746e19bb39e1414a9c8aa65286ea0c0ace2bcc

Verified certified table SHA-256:

05a1d6c6e4bd9f8d4a842dcfd9d9f820cffa22bb7a49ea52b4b319d4af7681d3

Verified graph SHA-256:

e7fba390da626d9698ab858502031f6099199b59ab297364fb4675a185f27a0d

The independently inspected fresh setup rebuilt the exact graph and table byte-for-byte. It took 16.0596 seconds; the recorded loaded production run took 54.0326 seconds. Their sum is 70.0922 seconds of separately timed work, not a single uninterrupted benchmark. Production peak RSS was 170,476 KiB. Fresh setup includes acquisition, floating-table construction, compiler invocation and integer certification. A later portable replay can still verify the production law and counts without the original host's temporary rebuild directory; the historical setup timing remains an explicitly recorded benchmark rather than a new measurement.

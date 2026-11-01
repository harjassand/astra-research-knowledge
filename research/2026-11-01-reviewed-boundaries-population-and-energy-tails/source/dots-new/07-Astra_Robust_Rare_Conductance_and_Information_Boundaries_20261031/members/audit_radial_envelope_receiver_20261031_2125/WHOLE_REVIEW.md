# Independent whole audit: acquired radial-envelope conductance receiver

## Verdict and immutable binding

**PASS at the declared mathematical/raw-program interface.** The global radial-envelope theorem, acquired complete rational-potential premises, exact finite numerical implementation, and externally tasked receiving join are sound. No frozen source correction was required. This is an executable whole-conjunction acceptance, not merely the pre-existing theorem-only receipt.

Inputs are bound to:

- `robustness_dilation_capacity_20261031/FROZEN_SHA256.json`: `0708f30e620bb4f4015eb292a9b76ec5ac005e345af027e38e7a2d63ca3c7cb5`.
- `receive_robustness.py`: `40b1460b03bc1ce3da7d5b95eaf828b9c4cd7b764961bbec17caf365ee46f032`.
- `check.py`: `334e8d2a08622e21dc03778bc74b24801ddfd7d27919d4e2ab7fec46d60e0fbd`.
- `PROOF_CANDIDATE.md`: `a1b8176f77befb08ea1c842c9c26775ede41ad166d517e409dd099d9b7b944ea`.
- Runtime dependency `dilation_partition_free_20261031/receive_dilation.py`: `d760c77b7efaa81bdb3ee424fd818359840d1da767fba4398c177a63f93bf4e8`.

All **40 explicit files and three inherited dependencies** match their frozen hashes and sizes. The complete current proof, sensitivity, local-probe companions, source/scope and cost declarations, new executable, author tests, inherited runtime and proof/review, and separate theorem receipts were inspected. Obsolete attempt sources/results were hash-verified and their recorded terminal states inventoried, not accepted as current runs. Original package and prior archives remain unchanged.

The accepted observable is

    cap_mu,M({y <= -1/2}, {y >= 1/2}) / mu({y <= -1/2}),

for every finite constant SPD transverse M with unit longitudinal mobility, zero cross mobility and matched reversible drift/noise. This is a common-family **equilibrium conductance outer interval**, not an exact rate, actual mobility identification, arbitrary-start latency, committor, sampler, or physical membership certificate. No latency companion outside this freeze is silently inherited.

## Executed result, not merely saved arithmetic

The clean copied-tree run `python -B check.py` completed successfully: **7,856 author assertions**, actual recomputation of **all five saved cases**, both 513D requested TOTAL ratios, and the saved nonfirst-axis raw/certificate pair. The regenerated `check_results.json` is **byte-identical** to the frozen report. Replay wall time was 3m8.589s (diagnostic, not a controlled complexity comparison).

A separate independently written suite passed **2,298 exact assertions**. Three supplemental checks confirm dependency-byte tampering fails before import and document normal Python API signature errors. A separate static cost ledger independently reconstructs every saved scalar-evaluation and fixed-multiplication count. Tests supplement the global proofs below; sampled numerical tests are not substituted for infinite-domain claims.

| Physical dimension | Shape | delta | Raw terms | Recomputed outer ratio | Scalar evaluations |
|---:|---|---:|---:|---:|---:|
| 3 | critical-flat | 1/100 | 117 | 1.059902110685917 | 4,100 |
| 17 | critical-flat | 1/100 | 1,111 | 1.176624269154324 | 12,292 |
| 129 | critical-flat | 1/500 | 9,063 | 1.028619306452425 | 98,308 |
| 513 | critical-flat | 1/500 | 36,327 | 1.008445231520649 | 786,436 |
| 513 | well-sensitive | 1/100000 | 36,327 | 1.008927885202765 | 786,436 |

The two 513D exact rational comparisons satisfy `high/low <= 101/100`. Their displayed intervals are respectively

- `[2.411013290922435e-152, 2.431374856363636e-152]`;
- `[2.4104381462919487e-152, 2.431958261350409e-152]`.

The exact strings, not these rounded displays, are received. Each 513D run scans 18,635,751 exponent entries, uses N=131072, T=2 and P=2688, and pays 15,204,428 directed fixed multiplications. Unknown partition cancellation does not mean the raw coefficient scan or verification replay was free.

## 1. Global variational and process joins

Let C_F be the unnormalized slab Dirichlet infimum and M_F the unnormalized left-basin mass. The actual normalized global partition cancels exactly: `cap_mu,M / mu(A) = C_F/M_F`. Since `U(l(y)z) <= F(y,z) <= U(u(y)z)`, density ordering gives

    C_U(u) <= C_F <= C_U(l),
    Z_U MA(u) <= M_F <= Z_U MA(l).

The variational ordering is valid on a common local-H1 trace class with extended infinite energy, or by finite-energy class inclusions; clipping to [0,1] preserves traces and lowers energy. Only the slab enters capacity, whereas the entire basin and its infinite tail enter mass. The comparison must not silently use differently normalized Gibbs capacities.

A scalar trial gives `C_U(l) <= Z_U/(beta R0(l))`. For the lower bound, set G(z)=U(u0 z), with u0 at least the slab maximum of u. Fixed-fiber Cauchy gives the reciprocal of `integral_slab exp(beta U(u(y)z))dy`. Relative to the density proportional to exp(-beta G), Jensen bounds the mean reciprocal below by the reciprocal mean. For each nonnegative homogeneous component of degree d<=p, concavity gives

    2-r^d >= (2-r^p)^(d/p),  r=u/u0 <= 1.

Thus the remaining exponential integral is bounded by a spatial dilation of the same U. Its partition is the same Z_U, not a supplied new angular normalizer. This yields

    Rplus(u) = integral_slab [u0^(2p)/(2u0^p-u^p)]^(m/p),
    1/(beta MA(l) Rplus(u)) <= k_F <= 1/(beta MA(u) R0(l)).

All signs, beta factors, reference powers and the one-basin factor are correct. There is no missing factor of two: both resistance half-slab integrals are doubled, while one basin is represented by the single right tail using evenness. Dropping transverse energy and choosing a transverse-constant trial earn the common fixed-SPD quantifier; no transverse mixing estimate or actual inverse mobility is executed.

For both scalar shapes, the exact derivative identities in the proof and the condition `0 <= delta <= kappa/(2(1+kappa))` establish positivity and monotonicity globally. Each profile decreases on [0,1] and increases on [1,infinity); u0=1+kappa is valid. The critical-flat maximum is 1/16 via v(1-4v), v=t/(1+t)^2, and the sensitive maximum is 1/4. These are mathematical bounds, not inferred from the author test grid.

The full finite-Gibbs and global-process join is also valid. Put `h=min(1/8,kappa/2)*(1-delta sup e)`. The identity `(1+t)^2 <= 2(t-1)^2+8` gives a uniform lower polynomial profile bound. For each atom, the acquired positive anchor and global envelope yield

    N_j >= c_j h^d (1+t)^(16+2d).

With L the normalized coefficient absolute sum and D its degree, `|2t N'_j/N_j| <= 2DL/h^d`; differentiating the denominator contributes the correctly retained 32. The code's `K=max(1,1+(2DL/h^d+32)/d)` over all profiles therefore gives, for `V=1+y^2+K z^T M^-1 z`,

    LV <= 2(1+Km)/beta.

V is coercive for every fixed finite SPD M and the actual rational drift is smooth/local-Lipschitz, so the stopped Lyapunov argument supplies nonexplosion. Finite Gibbs mass and matched reversible noise give the global process used by the capacity. K is not a relaxation bound and does not enter interval width.

## 2. What the raw finder really acquires

The input is a complete in-memory exact rational program `N(x)/(1+x_axis^2)^16`, not observations of an unknown potential. The code validates strict dictionary/list schemas, dimension, every full exponent vector, total degrees, duplicate and zero terms, canonical coefficients, individual and aggregate coefficient-bit budgets, and total exponent-entry budget. BOOL aliases are rejected for dimensions, exponents and numerical limits. The denominator is authenticated syntax with an everywhere-positive interpretation.

The positive pure-quadratic part must have exactly one absent physical axis; it must match the denominator. Every transverse atom is a positive-anchor pure quadratic, pure quartic, or square-square quartic. All quadratic directions are required. The first quadratic leading/base ratio proposes an exact rational square root and kappa; this is only a proposal, never admission by a few matching coefficients. Every remaining profile must pass the complete global inequalities.

After c_j=N_j(0)/(1+kappa)^d is acquired, the exact denominator-cleared inequalities are checked globally on t>=0. The projective transform has Bernstein coefficients a_j/binom(D,j). Exact de Casteljau subdivision covers [0,1]; nonnegative coefficients on every admitted leaf imply nonnegativity on the whole half-line. Negative endpoint/midpoint witnesses and finite depth/node/coefficient budgets refuse with Unknown. A true nonnegative polynomial can legitimately be Unknown at this sufficient interface.

Normalized-profile reuse is sound only after each raw coefficient and exponent has been read. The canonical hash binds dimension, axis, denominator power and every sorted exact term. Reordering raw records leaves acquisition invariant; changing an otherwise valid raw model is refused by receiving even if its scalar interval happens to agree. The test fixture really has nonconstant relative quadratic profiles, so a single common spatial dilation cannot explain the actual potential. An author test also admits a polynomial perturbation outside the fixture's linear-radius factorization. This is genuine inequality admission, not an exact-geometric identity renamed as robustness.

## 3. Exact arithmetic, tails and termination

For a positive rational x and S=2^P, initial floor/ceiling division gives an outward dyadic interval. Positive interval multiplication with downward/upward shifts and a nonzero-remainder correction preserves enclosure. Binary exponentiation therefore encloses every integer power; negative exponents use the exact reciprocal first. The rational exponent m/p is reduced before selecting roots. Integer square roots, or nested integer square roots for degree four, with exact upper-power equality testing, produce outward root bounds. All repeated-multiplication error remains in the endpoint interval; no false one-ulp assertion is made.

The independent tests compare these endpoints to exact rational powers, including negative exponents, underflowing bases, near-one rationals, exact dyadic boundaries, and exponents 511,512,513. For integer m/p they independently construct all four rational integrands and their exact endpoint Darboux sums; separate polynomial integration at delta=0 checks the resistance integral against an analytic exact answer.

The inherited integrator forms lower/upper Darboux sums on separately monotone pieces. The four integrands are `l^-m`, `u^-m`, `l^m`, and the Jensen expression. Mass uses [1/2,1] plus dyadic pieces through T; both resistances use [0,1/2] and are doubled. For y>=T>1, `s(y) >= kappa*y^4*(1-T^-2)^2`, giving the stated full analytic tails with denominator 4m-1. The lower-profile mass tail includes `(1-delta sup e)^-m`, while u>=s needs no such factor. Each analytic tail upper is rounded upward to scale S before addition, never down or omitted. The extra rounding is charged in the numerical product test.

A positive lower seed is required before the cutoff loop. Strict finite cutoff, precision, grid, evaluation and Bernstein budgets bound every loop. Necessary final-grid counts are checked before refinement, and the actual cache guard includes seed and intermediate-refinement points. At T=2^J the four-type final count is `(2J+4)N+4`; for every saved N>=128, the nested final grids include all earlier and seed points, so this equals the paid total cache count. Each type has its own cache key even when scalar profiles are shared.

For n>0, a fixed-power call pays `2*(popcount(n)+floor(log2(n)))` directed multiplications. Combining the three exponent-m types and the reduced exponent `m/gcd(m,p)` for Jensen independently reproduces every saved multiplication count. This is a paid exact ledger, not an assertion that timing, diagnostics or every process intermediate is authenticated.

The refinement condition charges the PRODUCT of all four upper/lower integral ratios. The final exact endpoints are

    low  = 1/(beta MA(l)_upper Rplus(u)_upper),
    high = 1/(beta MA(u)_lower R0(l)_lower).

`high/low` is then independently checked against the external TOTAL request. Intrinsic profile uncertainty and Jensen slack are not confused with quadrature tolerance. Equality at an exact requested width is admitted; a stricter total target is refused even when the numerical tolerance has already been met.

## 4. Costs and receiver binding: exact limits of the claim

The raw program costs O(Rn) to scan, with sorting costs for length-n exponent keys; every atom coefficient is supplied. Profile degree is bounded by 24, but unique normalized profiles consume the global Bernstein node budget. This is not arbitrary multivariate positivity, a learned useful basis, or a general polynomial bound in desired rate accuracy.

The power guards precede tracked large products, shifts, exact powers and root operands. They are not a universal peak-memory or all-Fraction-intermediate cap. Low-degree profile arithmetic, coefficient normalization, temporary Bernstein additions, exact sums, final reciprocals, serialization and repeated receiving still have paid ordinary finite costs. The source documents these limitations instead of mislabeling the tracked maximum as total process memory. Precision/conditioning, non-dyadic zeros, intrinsic width or serialization can cause Unknown; arbitrary accuracy is not promised.

Receiving calls `certify(raw, **original_external_task)` afresh. It recursively and type-strictly binds task, model, mobility family, observable, basins, acquisition (except seconds), exact endpoints, total ratio, N,T,P and exact tails. Independent attacks covered every proof-bearing task/acquisition/kinetic field and every interval endpoint, including None/BOOL/float substitutions. Changing only certificate-selected budgets cannot override the original task.

There are two deliberate boundaries:

1. Timing, scalar-work diagnostics and display floats are not proof-bearing. Additional outer certificate keys and interval display keys are ignored. A caller must use the authenticated exact endpoint and declared model fields, not an arbitrary extra field or modified display. The independent attack suite confirms this behavior rather than calling the whole dictionary authenticated.
2. The public interface is a Python callable, not a claimed hostile JSON-stream service. Missing mandatory `delta` or unknown keywords cause ordinary Python `TypeError`, outside the admitted signature. Malformed admitted raw/task values use Unknown. A runtime dependency hash mismatch raises `RuntimeError` before import. All are fail-closed; no false PASS is produced. An isolated harmless dependency-byte modification was actually tested and refused.

## 5. Fair comparison and scope companions

The ordinary unnormalized Dirichlet/mass comparison with the same localized envelopes and Jensen certificate reproduces this receiver. There is no proprietary algorithmic separation or new priority conclusion. The comparison is not against only the naive approximately1.29 global-width penalty.

On the actual critical-flat fixture, the negative perturbation radius ranges from 1-1/16000 to 1, and that full range occurs in both the slab and basin. Even after arbitrary static per-atom re-anchoring, the global constant radial ratio is at least 16000/15999; this is achievable. Hence that specifically restricted global-radial comparison pays at least `(16000/15999)^1024 > 1.066`, independently checked rationally. This is not a lower bound for all variational, free-energy, sampled or analytic methods. A method retaining location information can reproduce or improve the local comparison.

The sensitivity proof correctly distinguishes actual exponential-in-m amplification for the well-sensitive profile from the finite limiting outer-width penalty of a critical-flat profile. Its asymptotics do not certify the finite 513D intervals; actual exact receiving does. Uniform angular rescaling belongs inside the anchor and is not spuriously charged as a shape defect. Generic rotations still need conditioning/envelope information.

The deterministic transcript-compatible hidden barrier, fixed-alternative randomized hidden barrier and uniform-coverage corollary have their separately bound theorem receipts. Their quantifiers and global-process arguments are consistent with the executable scope. They concern unrestricted finite local value/jet information, not exact bounded-degree raw coefficients, trajectory observations, equilibrium sampling, fixed derivative bounds or richer global oracles. They are not executable model-acquisition services. The separately accepted latency theorem mentioned in task history is outside this manifest and is not an output upgrade here.

No external source retrieval, denied-source retry, outreach, publication, chemistry/biology operation, physical simulation, equipment or purchase occurred. Historical bibliography inspection is recorded by earlier trusted source ledgers; this whole audit is based on the supplied self-contained mathematics and exact execution, not a new priority search.

## 6. Preservation and reproducibility

All work is in `audit_radial_envelope_receiver_20261031_2125/`. The clean source-relative copy contains the frozen receiver/test/results and pinned backend. Run `python -B check.py` inside its `robustness_dilation_capacity_20261031/` subdirectory to replay the full suite; it writes only the copied report. Run `python -B independent_audit.py` and `python -B binding_boundary_audit.py` from the receipt directory for the independent checks. The deliberately altered dependency tree is separately labeled `dependency_tamper/` and is not the clean runtime.

The first attempted command used absent `/usr/bin/time` and exited127 **before Python execution**. Its empty stdout and exact missing-binary stderr are preserved. A materially different invocation using Bash's built-in `time` then executed the single full replay successfully. No uncertain execution was repeated.

The historical first two attempts each preserve three completed rows and an interrupted 513D attempt, not a proved budget rejection. The pre-tail-rounding archive preserves four rows and the sound well-sensitive serialization Unknown. None was overwritten, relabeled successful, or counted as a final accepted run.

Primary receipt artifacts are `hash_verification.json`, `independent_audit.py`, `independent_results.json`, `binding_boundary_audit.py`, `binding_boundary_results.json`, `independent_cost_ledger.json`, `preserved_attempts_inventory.json`, the full author replay stdout/stderr and regenerated report, and the final immutable-input recheck. The receipt manifest hashes them separately from the author's freeze.

**Conclusion:** the frozen package earns an exactly received, complete-raw-input, non-geometric radial-envelope conductance capability for its declared common fixed-SPD family. It does not earn physical microscopic acquisition, arbitrary-start latency, general model recognition, arbitrary precision guarantees, or a novelty/complexity separation.

# PR105 fixed-slot singleton minimax: independent receiving audit

Date: 2026-10-16. Repository: harjassand/astra-research-knowledge.
Merged revision: `2688d7a383502df4fc1e64001d04bb76e6ec05e5`.
PR: https://github.com/harjassand/astra-research-knowledge/pull/105

## Result

No substantive defect was found in the exact singleton fixed-slot minimax theorem under its literal ideal-control, known-envelope, private-sign-independent, arbitrary-finite-bath contract. Its sharp bound, finite-bath attainment and equal-action optimizer can be derived without any repository checker or aggregate receipt.

Three separate corrections/qualifications are warranted:

1. **Endpoint wording:** FIXED_REFRESH_MINIMAX.md Section 6 includes `a=0` in a strict comparison, which then reads `0<0`. Replace its range by `0<a<=pi/4`, and state equality at zero if wanted. The same pin's root reconstruction already has the correct positive-action range. This does not undermine the singleton theorem, which explicitly handles zero action correctly.
2. **Reproducibility/accounting:** the replay wrapper accepts mandatory `ENVIRONMENT_BLOCKED` rows in aggregate `PASS`, probes dependencies in the launching interpreter rather than `--python`, and produces aggregate `FAIL` merely if launcher openpyxl is installed because its intentionally unrun producer row becomes `NOT_RUN`. These are wrapper defects, not mathematical counterexamples.
3. **Prior-art wording:** the Wang comparator is a weighted complete-record error, not the unweighted terminal error optimized by this theorem. This needs a precise citation correction, not withdrawal of the minimax proof.

The meaningful mathematical advance over the prior packet is the finite-action singleton endpoint minimax with a finite absorbing/sink-bath witness. Fixed-slot random pulse/identity DD is established prior art. No new microscopic operation, finite-width controller qualification, hardware advantage, or historical-priority result has been established.

## Evidence and method

Eight source files were retrieved through the read-only GitHub connector at the immutable merged SHA. Their exact received UTF-8 bytes were preserved, and all eight computed Git blob SHA-1 values match the connector's source blob IDs. `SOURCE_MANIFEST.json` records URLs, byte lengths, SHA-256 values and blob checks. `retrieved_evidence.json` preserves the source responses and PR merge metadata.

The previous audit and peak-cap proof were read from `../pr104_bath_audit`. No repository code, wrapper, notebook, or producer checker was executed. `independent_checks.py` is newly authored bounded checking code; it imports only installed standard scientific libraries and its own source. Its full outputs, random seed, runtime versions and script hash are in `independent_results.json`. No canonical edits, PR comments or external communications were made.

Load-bearing pinned sources:

- [Fixed-refresh theorem](https://github.com/harjassand/astra-research-knowledge/blob/2688d7a383502df4fc1e64001d04bb76e6ec05e5/updates/GC-peak-stability-genesis-20261016/package/derived/workers/gc_peak_genesis/FIXED_REFRESH_MINIMAX.md), Sections 1–6.
- [Root reconstruction](https://github.com/harjassand/astra-research-knowledge/blob/2688d7a383502df4fc1e64001d04bb76e6ec05e5/updates/GC-peak-stability-genesis-20261016/package/derived/root/IDEAL_REFRESH_MINIMAX_RECONSTRUCTION.md), especially its final positive-action comparison.
- [Poisson minimax bridge](https://github.com/harjassand/astra-research-knowledge/blob/2688d7a383502df4fc1e64001d04bb76e6ec05e5/updates/GC-peak-stability-genesis-20261016/package/derived/workers/gc_peak_genesis/PEAK_AND_POISSON_MINIMAX.md), Sections 2–3.
- [Replay wrapper](https://github.com/harjassand/astra-research-knowledge/blob/2688d7a383502df4fc1e64001d04bb76e6ec05e5/updates/GC-peak-stability-genesis-20261016/package/derived/root/replay_public_evidence.py), lines 828–833, 873–879, 1007–1021 and 1036.

## Independent derivation

Let P and R=I-P be the two parity sectors, and let the time-dependent Hamiltonian be H0+V with H0 sector preserving, V sector changing and ||V(t)||<=j(t). Internal updates are exact complete parity pinches. There are m=N+1 gaps with envelope actions a_k.

### Uniform one-gap lower survival bound

Transforming away H0 preserves P, R and the norm of V. For a normalized initial vector in P, set p(t)=||R psi(t)||^2. Cauchy–Schwarz on the off-diagonal interaction gives

`|p'(t)| <= 2 j(t) sqrt(p(t)(1-p(t)))`.

Up to angle pi/2 this implies `arcsin(sqrt(p)) <= integral j`. The continuation beyond pi/2 is the trivial bound p<=1. Thus, for every initial joint bath/reference vector in P,

`||P U_k P v|| >= c_k ||v||`, where `c_k=cos(min(a_k,pi/2))`.

This is a lower bound on the smallest singular value of the compressed survival operator. It is stronger than an average-state check and does not assume a product bath input.

### Compose the all-surviving branch

Retain the internal pinch outcomes as mathematical records and include the final parity measurement. The Kraus operator for retaining P at every gap is

`G=(P U_m P)...(P U_1 P)`.

The previous bound gives `G†G >= (product c_k^2)P`. The final wrong-sector event is disjoint from this all-surviving record, so its positive effect E obeys

`E <= [1-product c_k^2]P`.

This proof uses a single unnormalized branch and operator inequalities. There is no division by a conditional success probability and no assumption that bath outcomes are independent.

### Finite adversary attaining equality

Use a memory qubit and bath basis u,d_1,...,d_m. On gap k, use the allowed interaction

`V_k(t)=j(t) X tensor (|d_k><u|+|u><d_k|)`,

stopped after action pi/2 if necessary. Start in |0,u>. The only still-unflipped component rotates between |0,u> and |1,d_k>. Previously produced |1,d_l>, l<k, are dark for every later gap. Consequently every first mismatch remains a final mismatch. Its probability is exactly

`Q(a_1,...,a_m)=1-product cos^2(min(a_k,pi/2))`.

The bath dimension m+1=N+2 suffices. Exact equality is over the arbitrary-finite-bath class, or a separately fixed bath at least this large. The universal upper survives if the bath is smaller, but this argument does not establish equality there.

Private sign changes alter only phases of the sink amplitudes. Every final d_k amplitude is odd in the initial sign, and the u amplitude is even. Hence the original initial-seed odd-Walsh effect has the same Q weight on this witness, for every internal private toggle realization. This gives an admissible lower witness inside the stated sign interface without identifying arbitrary Walsh labels with physical faults.

### Optimize the fixed schedule

When every a_k<pi/2, strict concavity of log cos gives

`sum log cos(a_k) <= m log cos(a/m)`, with `a=sum a_k`.

Equal action therefore minimizes Q. If a/m>=pi/2, every partition contains a saturated gap and the minimax is one. At a=0 every schedule has zero error. For nonnegative integrable j with positive total action, continuity of the cumulative action gives strictly ordered equal-action cut times; plateaus do not obstruct those positive action increments.

Thus `Q_N(a)=1-cos^(2(N+1))(min(a/(N+1),pi/2))`. Its small-action expansion matches the source, including the fourth-order coefficient. The earlier quadratic certificate a^2/(N+1) is the exact leading minimax term, rather than the finite-action value.

## Poisson comparison and the zero-action correction

For the admissible actual qubit witness H=j(t)X, a telegraph Z-kick rate gamma=lambda/2 yields physical final error `p=E sin^2(S)`, with `S=integral j(t)xi(t)dt`. The covariance is `E xi(t)xi(s)=exp(-|u(t)-u(s)|)`, so the old sufficient certificate is exactly `C=E S^2` for this witness. Since |S|<=a and sinc is positive decreasing on [0,pi],

`sinc^2(a) C <= p <= C` for 0<=a<pi, using sinc(0)=1.

Taking the infimum over deterministic schedules and supremum over the permitted unknown Hamiltonians correctly gives `sinc^2(a) C_star <= W_star <= min(1,C_star)`. The lower witness is a member of the adversarial class; it is not a lower bound on every Hamiltonian's error. This supplies actual-error asymptotic minimax content that the previous peak-cap certificate optimization alone did not have.

At constant envelope, latent Poisson budget N and fixed grid N slots both correspond to mean N/2 interior physical telegraph/frame flips. The cap-free Poisson certificate optimum is `2a^2/(N+2)`, so for N>=1 and 0<a<=pi/4,

`Q_N <= a^2/(N+1) < sinc^2(a) 2a^2/(N+2) <= W_Poisson_star`.

The strict step is valid because `sinc^2(a)>=8/pi^2>3/4>=(N+2)/(2(N+1))`, and the cancelled factor a^2 is positive. A fully rational check of the strict constant is `pi<22/7`, hence `8/pi^2>98/121>3/4`. At a=0 every risk is zero and that strict comparison is false. The source worker theorem line 111 omits this qualification; root reconstruction line 43 supplies it already.

These are different timing classes. Instantaneous grid updates do not obey a bounded continuous dephasing-rate cap. Fair bits, slots, initial/final wrappers, privacy, pulse width, ramp noise, energy and resets have not been put on a common physical cost model. The comparison is mathematically operational inside the ideal model only.

## Decisive independent checks

- **Exact saturation and Walsh check:** three gaps with (cos,sin)=(4/5,3/5), (12/13,5/13), (15/17,8/17), bath dimension four. Exact matrix propagation gives final error `28105/48841`; the exact odd-Walsh norm is the same rational for each of all four internal toggle paths. Wrong-memory/even-Walsh and right-memory/odd-Walsh components vanish exactly.
- **Uniform finite-bath effects:** 144 instances, bath dimensions 1–5, 1–6 gaps, three noncommuting Hamiltonian pieces per gap, arbitrary sector-preserving bath blocks and normalized off-diagonal couplings. The largest initial-sector endpoint-effect eigenvalue obeyed Q in every case. Maximum observed ratio actual/Q was 0.6259530221. The smallest singular-value survival bound was checked separately. These numerical cases are diagnostics, not a universal proof.
- **General qualified Fourier identity:** 24 unrelated noncommuting physical-system examples explicitly enumerate every initial sign and internal toggle path, then compare the averaged K_odd†K_odd operator with the virtual-seed pinched endpoint effect. Maximum operator-norm difference was 1.36e-15. This tests the original positive-effect normalization, not only one initial state.
- **Scheduling:** 1,680 randomly sampled partitions never improved on the equal-action Q. Zero action and saturation cases were included separately.
- **Poisson lower witness:** 120 random piecewise rate/envelope schedules were checked by direct Bloch-matrix exponentials against an independently integrated covariance-moment ODE. All obeyed sinc^2(a)C<=p<=C. Fifteen positive-action matched-count examples obeyed the claimed strict comparison.
- **Concrete endpoint:** at a=pi/4, N=1, fixed-grid Q is 0.2714466094, versus Poisson minimax lower bound exactly 1/3. The physical constant-drive error for the certificate-optimal Poisson schedule is 0.3361347630. This is a strict ideal-model separation, not an implementation result.
- **Finite-action objective distinction:** for the source's known H=3.1X example, direct evolution gives physical errors 0.3089149095 for the certificate optimizer and 0.0027137433 for its admissible narrow-rate competitor. Their certificates order oppositely (4.805 versus 5.4043). This confirms the warning that finite-action known-H optimization is a different problem.
- **Assumption boundary:** if a forbidden adversary reads and cancels the private sign, a=0.6 and N=3 give coherent error 0.3188211228, above the allowed-independent-adversary Q=0.0863790773. This deliberately violates privacy and demonstrates why the assumption must remain explicit.

## What is actually new relative to the prior packet and inspected prior art

The previous sharp shared-bath result used an exact Poisson-pinch unraveling, deletion-null mixed Duhamel bounds and scalar gap averaging to obtain an all-subset product of quadratic action certificates. Its peak-cap addendum exactly optimized that certificate under integrated/peak intensity constraints. Neither alone gave exact finite-action endpoint minimax.

Switching from Poisson update times to deterministic public slots with independent fair private toggle decisions is a different ideal timing class, but the protocol itself is old random DD. Viola–Knill establishes tracked random control and bounded time-dependent joint coupling; Santos–Viola explicitly has fair pulse/identity choices at fixed slots, initial randomization and cumulative toggle signs. The fixed-cut joint-effect import reuses the old deletion-null argument without Poisson averaging.

The specific new mathematical step in the inspected packet is the exact cosine survival bound plus an absorbing finite bath that turns every first-mismatch probability into terminal wrong-sector probability. Equal-action minimization then follows directly. The Poisson physical witness adds the stated actual-risk sandwich. A universal finite-action **joint** upper bound product Q_i is explicitly not proved; the existing quadratic joint upper and product sink lower still leave that stronger finite-action question open.

The bounded primary-source audit is in `prior_art/PRIMARY_EVIDENCE_AUDIT.md`, with direct links and observable distinctions. In particular [Wang v2, Section V.2, Eq. (29)](https://arxiv.org/html/2610.01521v2) has complete retained-record error `varpi [1-cos^(2K)(gh)]` for a static bath mixture 0<varpi<1. Unit prefactor is a boundary specialization. Its terminal wrong-X error instead permits repeated flips to cancel. Therefore `PRIMARY_PRIOR.md` should say “weighted complete-record error,” rather than leaving the benchmark unqualified. Wang also has a general integrable-envelope complete-record upper bound, so “uniform envelope bound” alone is too broad a novelty distinction.

This finite primary-source set does not establish historical priority of the precise endpoint minimax theorem. External review remains unresolved.

## Replay-wrapper findings and recommended semantics

### Verified source behavior

1. Lines 830–833 call `importlib.util.find_spec` in the wrapper's current process. Subprocesses later use the separate `python_executable` argument. Consequently the launcher may block a checker whose selected interpreter has its dependency, or admit one whose selected interpreter lacks it. Runtime reporting also pairs launcher `sys.version` with the selected executable path.
2. The aggregate predicate at line 1014 accepts `ENVIRONMENT_BLOCKED`, `INPUT_EXCLUDED` and `INSPECTED_NOT_RUN` alongside `PASS`. Thus absent NumPy/SymPy can remove mathematical replay rows without preventing aggregate PASS, assuming the remaining work passes. PASS is not evidence that all listed mathematical checks ran.
3. The original catalysis checker is never run by this code path. At line 1007, absent launcher openpyxl gives `ENVIRONMENT_BLOCKED`, which is accepted; installed launcher openpyxl gives `NOT_RUN`, which is rejected. An independent truth table reproduces PASS versus FAIL solely from that installed-library change, with every executed result held fixed.

These conclusions come from static inspection and an original truth table. The acquired wrapper was not executed. The preserved published receipt was not treated as validation of mathematical correctness.

### Precise recommended status contract

- Fix and publish an explicit set of **mandatory** receiving checks before execution; identify optional producer checks separately.
- A row may be `PASS` only after that checker actually ran under the declared interpreter, exited successfully and its expected assertions/output were independently accepted. A failed execution/output is `FAIL`; unmet prerequisites are `BLOCKED`; deliberately omitted work is `NOT_RUN`; unavailable unpublished input is `INPUT_EXCLUDED`.
- Mandatory aggregate: `FAIL` if any mandatory check fails; `INCOMPLETE` if any mandatory check is not an executed PASS; `PASS` only if all mandatory checks actually pass and mandatory input-integrity checks pass. Use a nonzero exit for FAIL or INCOMPLETE (for example 1 and 2 respectively).
- Optional producer rows do not silently gate or certify mandatory qualification. An unattempted optional producer should remain `NOT_RUN` regardless of dependency installation; any dependency diagnostic belongs in a separate field. Optional outcomes must remain plainly visible.
- Probe dependencies using the exact selected interpreter in a bounded subprocess. Record both launcher provenance and checker provenance, including the selected interpreter's own version and dependency versions. Do not pair one interpreter's version with another's path.
- Separate byte-integrity status, required replay completeness and mathematical/hardware qualification. A replay PASS is not external proof review, historical novelty, or physical validation.

These are recommendations only. No canonical changes were made.

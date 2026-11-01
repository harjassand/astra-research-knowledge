# Independent whole review: uniform autonomous survival/CDF receiver

## Verdict and exact frozen boundary

**PASS — whole theorem/code/receiving scope**, for the original
`uniform_survival_receiver_20261031/FROZEN_SHA256.json`, SHA-256
`51bf3b23073d2b85727d36d94a9191a26b8dd4d2d0faaca4cab78152e437b4e7`.
All 13 explicit files and eight dependency bindings were verified before copying
and again after execution. No candidate correction was needed. Frozen candidate,
inherited source and previous audit bytes remain unchanged.

The accepted operation constructs one acquired rational exponential reference
rate and a **uniform absolute autonomous passage-time CDF error certificate** for
the declared ordinary constant-mobility Langevin model from **EXACT FULL Gibbs
conditioned on A={Y<=-1/2}**. It optionally encloses CDF values at original external
nonnegative rational times. This is not a clamped kinetic query, a capacity label,
an exact exponential law, a relative extreme-tail approximation, or a physical
preparation/calibration certificate.

Principal bindings:

- Wrapper `receive_survival.py` (7,876 bytes):
  `626bed8d61d951a34c49cfd9489b46fb36d3e7f14c0a39a8e9122c2382c0aeb6`.
- Candidate finite-rate corollary (5,172 bytes):
  `e20a54e822d6d7012d0c1ec687c488488f7bab528b5d25cad48009f4e34f9d71`.
- Frozen root spectral theorem (6,109 bytes):
  `2414f104c0b74b59796af2f24c9a93ac5300a1a6eee7bd1137e0adef1dbfee67`.
- Inherited constant-SPD MFPT code:
  `7c3a732589bec0aa4240c3970c84be2079421343f791ce68b2e4e92bd65b81ca`;
  accepted corrected v2 manifest:
  `61ace87427769d160cc0c6121377298f02b914059f5018eafe8bc0e30614c298`.
- Inherited autonomous scalar MFPT code:
  `607f90e242e47de87d217ca8e19aa16115780eeb10bdfc83a1e3d2dbf915cff0`.
- Inherited exact parser/directed exponential primitive:
  `b4b75f4eb063e13a8c4fe49a34af5c55f182df87317a1cde4c0c14b3aefdf8cb`.

The prior root-theorem receipt was separately read and verified: its manifest
`constant_spd_mfpt_20261031/audit_survival_theorem_20261031_2256/AUDIT_SHA256.json`
has SHA `dfa4ada5025508497b405a96ffdba65d3a21bb38c641612737ea2658eaa7ec7d`.
That receipt was theorem-only, with 1,124 exact checks, and did not previously
accept this executable or numerical KS value. The present whole review supplies
that missing boundary. Its separate trial-function corollaries, subsequent
trial-v2/separate-source variants and any later well-current construction are
**not substituted into this wrapper**. The wrapper uses the valid root 2414f104
and candidate corollary e20a54e8 exactly as frozen.

## Executions and independently extracted result

A clean source-relative audit copy ran the supplied `check.py` with Python `-B`.
It passed **3,809 author assertions**, actually recomputing all **four** saved
cases. The regenerated `check_results.json` is byte-identical to the frozen
report. Diagnostic shell time: 10.071 seconds.

The independently written `independent_audit.py` passed **2,003 checks**,
including all four further literal-original-task recaptures and **209 explicit
UNKNOWN refusals**. Its slower exact-rational reference calculations took
123.453 seconds wall time; this is audit cost, not a production benchmark.
`targeted_output_guards.py` passed **nine additional checks**. Total new independent
checks: **2,012**. The independent calculations do not replace the analytic
all-time proof with a finite sample of time points.

Actual acquired outputs (m is transverse dimension; full dimension is m+1):

| m | Actual transverse mobility | KS upper, diagnostic decimal | Reference rate, diagnostic decimal |
|---:|---|---:|---:|
|128|64 I|0.008688152253218354|4.656353637571968e-9|
|256|64 I|0.004655690256033425|2.188884873017223e-18|
|512|64 I|0.004925673926521221|2.384062482990607e-37|
|512|diag(64,128,...,32768)|0.004925673926521221|2.384062482990607e-37|

The last model also changes the angular coupling from 20 to 10^100. The raw
hashes differ; the **outer certificates** agree exactly. Equality of actual
passage-time distributions is not asserted.

For either 513-dimensional saved case, the actual CDF at t=4*10^36 is enclosed by

    [0.6097326982654544, 0.6195840461184968].

At t=10^38 the interval is approximately [0.9950743260292049,1], so residual tail
probabilities below the absolute error remain unresolved. Exact rational
endpoints, not these decimals, govern acceptance.

The 128-fiber case is accepted at its literal external KS request 1/100 and CDF
width 1/50; adopting default KS 1/200 does NOT pass. Unit transverse mobility
also fails the small KS request, even when its broader MFPT interval has first
been received at full_ratio=13/10. These are honest UNKNOWN outcomes of the
sufficient bound, not proofs of impossibility or intrinsic physical error floors.

## 1. Root theorem and the actual current join

I rechecked the frozen scalar spectral lemma. For X>0, EX<=1 and E(1/X)<=1+e,
Jensen gives the lower exponential envelope. Taylor's integral remainder around
one is bounded by (4/Euler^2)(x-1-log x), then by
(4/Euler^2)(x-1)^2/x using log x>=1-1/x. Cauchy gives
1-EX<=e/(1+e) and E[(X-1)^2/X]<=e. The uniform remainder plus mean correction
is at most e because 1/Euler+4/Euler^2<3/8+9/16<1. This holds at all real
nonnegative times; no gap, second inverse moment or bounded spectral support is
introduced.

For the actual killed reversible semigroup, the source-current construction
already earns finite zero-resolvent forms Q_A<=B_A and Q_S<=rho^2 B_A. Positivity
and source Cauchy imply Q_h<=B_A(1+rho)^2 for the equilibrium committor h.
M<=||h||^2<=M(1+rho), and its energy is at most C0=1/(beta R). Consequently
X=lambda/k0, k0=C0/M, has the required first/inverse moments with

    e0=(1+rho)^2 B_A/(beta M^2 R)-1.

These are finite source inverse forms, not a globally bounded inverse operator.
The existing full-current/tail proof earns finiteness before taking the zero
resolvent limit. A spectral gap is neither assumed nor inferred.

The actual survival numerator is <1_A,P_t1_D>. Writing h=1_A+e and 1_D=h+d,
the difference from <h,P_th> is <1_A,P_td>-<e,P_th>. Both terms are nonnegative,
so contraction bounds their absolute difference by their maximum,
sqrt(||h||^2 S), not by an invalid cancellation or density-ratio estimate.
Normalization adds at most rho, giving rho+sqrt(rho(1+rho)). This is the
comparison to FULL Gibbs|A, not to a fixed angular ray or only a shared energy
marginal.

The critical receiving join is preserved: the inherited finite T_hi bounds the
**specific current expression** (1+rho)B_A/M, not merely some unrelated upper
bound on the actual mean. Its retained slab, near-basin, far-tail, coercivity,
least-mobility and cross-source factors establish that fact. Hence

    (1+rho)^2 B_A/(beta M^2 R)
       <=(1+r) T_hi/(beta M_lo R_lo).

This validates the wrapper's spectral error. It does not infer a survival law
from a mean alone or identify the mean with inverse capacity. The unchanged
ordinary constant-SPD proof supplies the same full process, source, coercivity,
tails and initialization required by the spectral theorem.

## 2. Single acquired rate, outward arithmetic and absolute time

The code reads the recomputed M/R interval and sets

    k_lo=1/(beta M_hi R_hi), k_hi=1/(beta M_lo R_lo),
    k_star=(k_lo+k_hi)/2,
    e=(1+r) T_hi/T_lo-1,
    delta=e+r+sqrt_upper(r(1+r))+(3/16)(k_hi/k_lo-1).

All operations here are exact Fractions except the explicitly upward dyadic
root, whose squared inequality is checked. The lower interval endpoints are
positive. The spectral error is required nonnegative. No display float controls
an endpoint or a tolerance decision.

For any true k0 in the acquired interval, the mean-value theorem yields
|exp(-k_star*t)-exp(-k0*t)| <= [(k_hi-k_lo)/2] t exp(-k_lo*t).
Its all-time supremum is at most (k_hi/k_lo-1)/(2*Euler), hence the 3/16 penalty.
An arbitrary midpoint is therefore not being treated as an exact physical rate.
The penalty is included in the same total external KS inequality as structural,
initial-law, quadrature/tail and root uncertainty.

For the 513-dimensional case the contributions are approximately:

- spectral error: 0.004780005556792939;
- slab ratio: 1.973778717895864e-24;
- complete initial-law comparison: 1.4049123523912124e-12;
- acquired-rate penalty: 0.00014566836832336988;
- total: 0.004925673926521221.

At each t>0 the inherited directed exponential routine encloses exp(-k_star*t).
The code then clips [1-E_hi-delta,1-E_lo+delta] to [0,1] and checks the complete
outward interval width against the original request. At t=0 the CDF is exactly
zero because A is separated from B and the original diffusion has continuous
paths. Empty query lists correctly return the all-time certificate without an
exponential evaluation.

Independent reference calculations used exact alternating Taylor remainders on
[0,1/2] followed by separate outward dyadic repeated squaring. They enclose all
240 independently chosen primitive tests, including zero, tiny arguments,
range-reduction boundaries and huge arguments, and all 17 nonzero query points
across the cheap model and four actual saved cases. The actual certificate's
intervals contain those stronger reference intervals after adding delta.

The beta/mobility scaling test changed beta to 9 and actual transverse mobility
to one third. The current corrections and KS certificate remain equal, the
acquired reference rate divides by nine, and querying at nine times the original
times yields exactly the same outer CDF. Absolute time and beta are not lost in
normalization.

## 3. Full model, original task and output receiving

The wrapper re-executes the hash-pinned MFPT receiver, including its complete
raw program scan. The actual executable grammar is positive homogeneous quartic
energy with every pure coordinate term present, integer alpha=m/4>=4, and exact
positive **constant isotropic or diagonal** transverse mobility. The minimum of
all diagonal entries is acquired; no implicit first-axis minimum is assumed.
Unit longitudinal mobility and zero cross-mobility are fixed by the model.
The broader arbitrary-SPD mathematical theorem does not expand this executable
input grammar. No engineered radial/tangent tensor or energy Markov closure is
silently imported from the parser's historical use.

Declared exact task values must have native Fraction type, not int, bool, float,
NaN or subclasses. Resource controls must be native positive ints, not bool or
subclasses. Query lists must be native lists, within the external count budget;
all query times must be nonnegative exact rationals within their bit budget.
Missing required keywords or unrecognized keywords are Python signature errors,
not admitted tasks. Within the declared signature, tested invalid values and
unmet sufficient bounds return UNKNOWN.

`verify` recomputes from the supplied original raw model and external task. It
does not read time, tolerance, precision or budget controls from the certificate.
It compares the entire normalized proof record, including nested mean proof,
source hashes, model/initialization/observable strings, rate interval, all error
contributions and every query. Reordered original times, additional times,
weakened initialization, altered raw order/hash, modified mobility, corrupted
proof fields, unknown extra claims and numeric bool substitutions cannot reuse
an old certificate. The original standalone fixture also replays successfully.

Native cyclic nested-mean certificates are explicitly depth-guarded. Tested
cyclic malformed query/task objects are refused finitely by schema/type
comparison; oversized output query lists do not pass the exact conjunction.
The verifier does not promise a separate certificate-byte budget or an O(1)
malformed-input parser: supplied records still have to be read. No acceptance
uses malformed certificates as sources of arithmetic budgets.

`seconds`, `work` and interval `display` are deliberately diagnostic. They can
be absent or altered without changing the proof. This is sound because actual
work is rerun and the original budget is enforced before comparison; a forged
work counter cannot create more query budget. Those diagnostic fields are not
authenticated measurements and should not be advertised as such.

## 4. Costs, exact guard boundaries and source integrity

The complete energy/mobility read, hash, scalar quadrature and infinite tails are
paid again for every receiving operation. Runtime is standard-library only;
the author's test suite also uses SymPy. No downloaded physical data, sampler,
committor or spectral decomposition is supplied as a free input.

For either m=512 case, acquisition scans 1,023 energy terms and 523,776 exponent
entries, plus one isotropic value or all 512 diagonal values. Canonical raw input
sizes are 1,079,872 and 1,134,383 bytes. The MFPT stage uses N=32768, T=2,
precision 512 bits, 98,306 scalar points, 98,310 integer powers and 1,671,270
fixed products. Its two roots happen to be exact rationals at these parameters.
The wrapper uses precision 256 bits, one additional root (tracked integer bound
1,482 bits), and four exponentials with 170 total Taylor terms, 706 extra fixed
products and largest tracked product bound 2,615 bits. Total shared fixed
products are **1,671,976**.

The extra product count was independently derived per nonzero query as
4*(Taylor terms)+1+2*(squarings), then summed. All extra products consume
max_operations minus the **recomputed** mean-stage product count. Exact total
budget admission and one-below refusal passed. Exact maximum guarded-integer
admission and one-below refusal also passed. No-query and zero-time cases retain
one paid root but need no exponential products. Lower root precision retains its
larger initial-law error rather than discarding it. Exact KS and final-query-width
boundary tests pass at equality and refuse just below it.

The operation budget is explicitly a **guarded fixed-product** budget. It is not
a count of all Python/Fraction additions, divisions, gcd reductions, exact rate
arithmetic, isqrt internals, parsing, hashing, allocation or serialization.
Those costs and complete input size remain real. Root-call counts are fixed;
operand bit sizes depend on the acquired data, dimension and precision. Neither
the corrected parent package nor this wrapper claims dimension-free bit cost,
constant input cost, bounded peak memory from these counters, or a benchmark
victory over an optimized ordinary implementation.

The wrapper checks the inherited MFPT code hash before importing it, and that
code transitively pins its two inherited code dependencies. An isolated altered
copy was refused before import. The root and corollary proof texts are bound by
the package manifest and exact certificate identities; runtime code does not
parse or re-prove those text files. Whole-package hash verification is therefore
part of this source-bound receipt, not an inferred theorem-text runtime check.

## 5. Limits and strong ordinary comparators

The all-time statement is mathematical under the exact full model and full
Gibbs|A law. It does not identify a measured physical generator, prepare that
continuous law, authenticate calibration or establish model validity over a
physical horizon of 10^38 units. Tiny TV error in preparation can be separately
added to bounded CDF errors only if independently earned; none is received here.
It does not control the earlier unbounded mean.

Uniform absolute CDF accuracy cannot be integrated over an infinite time horizon
to prove a mean bound, nor does it imply relative extreme-tail accuracy, finite
exponential moments, relative accuracy of every quantile, a hazard-rate law,
all-start exponentiality or a killed/global spectral gap. The separate mean
certificate has its own current proof. The previously proved zero-gap behavior
is compatible with this source-specific spectral-measure estimate.

The retained primary-source comparison to Aldous–Fill's completely monotone
spectral mixtures and quantitative exponential approximations is relevant and
strong. The retained Fernández–Manzo–Nardi–Scoppola recurrence-based approach
also prevents treating absence of a global gap as a novel generic principle.
Their distinct quantitative premises cannot be supplied free. An ordinary
spectral/variational implementation given this full raw input and the same
constructed form/current certificates reproduces the conclusion. No historical
priority, proprietary separation, optimized runtime superiority or rare-crossing
experimental achievement is established. Prior primary-source reads are recorded
in the separately verified theorem receipt; no new web retrieval was needed.

## 6. Audit artifacts and execution exceptions

`input_verification.json` and `final_source_recheck.json` record all 21 bindings.
`prior_spectral_receipt_verification.json` separately binds the earlier theorem
receipt. The clean copied tree, original results, actual author replay logs,
independent scripts/results and targeted guard results are retained. The
`dependency_tamper` directory is intentionally invalid and is not a clean
runtime distribution. `REVIEW_NOTES_IN_PROGRESS.md` is preserved interim history,
not the final verdict.

Two audit-launch errors are retained, neither a candidate failure. First, shell
redirection used the parent scratch directory because the working directory was
wrong; it was denied **before Python execution**. The denied target was not
retried or escalated. The author check was then run only inside the intended
copied candidate directory. Second, creation of the independent script used a
duplicated relative directory prefix; the subsequent Python launch reported the
script missing and did not run any audit assertions. Its stdout/stderr are saved
as `initial_missing_script_*`; after creating the script at its intended audit
path, the successful independent suite ran once. These events have known
nonexecution, no uncertain write state, and no pending blocker.

All accepted source hashes were rechecked unchanged after tests. This receipt
accepts only the stated original wrapper freeze; future well-current or
alternative-source laws, new models, new receivers and new tolerances require
separate receiving. No helpers or frozen-source edits were used.

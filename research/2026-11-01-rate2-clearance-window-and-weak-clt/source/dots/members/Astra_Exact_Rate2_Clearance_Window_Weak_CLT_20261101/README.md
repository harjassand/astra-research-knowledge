# Exact rate-2 clearance: an explicit finite-N window and a separate weak CLT

**Completed, independently received results for one restricted count-chain model.**
This is not a general-network theorem, a novelty claim, a practical simulation
speedup, a hardware/preparation operation, or a security certification.

## Model and the two different claims

Species are `(A,B,C,D,E)`. Reactions are `0 <-> A`,
`2A <-> AC, AD, AE`, `AE <-> CD`, and `CD <-> AB`.
Every coefficient is one except **CD -> AE has coefficient two**.
Each 2A propensity is `A(A-1)`, not `A²/2`. The rate-1 product-form model is
not substituted. For the corner results, start at `(0,N,1,1,0)` and put

    S=A+B+C+D+E,  T=N^(1/5),
    tau=inf{t: S(t)<=15(N+2)/16}.

1. **Explicit finite-N confidence window.** The accepted induction clock,
   dyadic continuation, and explicit harmonic removal service pay the actual
   full-channel path, immigration, stopping exits and unused waiting time.
   The unchanged numerical receiver verifies all size/error/bit-work tests.
   At the encoded fixture `N=10^1300, K=10^40, a=1/20`, it certifies

       P{1.056580521912579472 <= tau/T <= 1.156580521912579663}
         >= 1 - 0.000000064007275958.

   The error is below the requested `10^-6`. The interval retains the scalar
   rational endpoints, beta, dyadic delay and physical-service corrections.
   This huge-input mathematical capability is **not physical preparation or
   practical advantage**. It does not admit arbitrary N or yield a CDF rate.

2. **Actual weak Gaussian law, separately proved.** As N tends to infinity,

       (tau - s_* T)/sqrt(T)  ==>  Normal(0,Sigma²).

   The center is the mathematical `s_*`, **not a fixed rounded decimal**.
   Received deterministic acquisitions give

       s_* in [1.106580521912579472, 1.106580521912579663],
       Sigma² in [0.5677211094, 0.5687113183].

   The CLT identifies the previously deterministic variance integral with the
   limiting normal parameter. It proves **no finite-N normal/CDF error rate,
   no mean or variance convergence, no uniform integrability, no finite-noise
   variance formula, and no arbitrary-start CLT**. The finite-N receiver does
   not implement the CLT. The original numerical variance receipt retains
   its deterministic-only scope; the separate CLT supplies the identification.

## Explicit receivers and exact dependencies

The harmonic full-generator service removes the old numerical interior-constant
acquisition gate in two independently accepted joins:

- Corner induction: `m0=delta/2`, `h=1600 delta^-2`, `delta=10^-100`, with all
  finite-level and `KT<=delta N` tests retained.
- All-start reduction: for **every** actual state of total `N>=10^40`,
  `P[S(1+10^8 sqrt(N))>15N/16] <= 32 exp(-sqrt(N)/10^6)`.
  This replaces only the service interface in the received all-start prefix;
  adverse exits and one original immigration counter remain paid.

The CLT is deliberately still bound to its **old accepted interior +5** supplier,
not silently rewritten to use the harmonic join. Its accepted weighted-cone
and task-observable-corrector dependencies are included with their exact receipts.
Unreceived/future cone, fraction/readout and new polynomial-corrector proposals
are excluded. `PROOF_INDEX.md` locates the controlling exact sources/receipts.
Old author files containing “pending” are preserved byte-for-byte: later exact
source-bound receipts, not edited historical headers, determine acceptance.

## Reproduction

From this extracted directory:

    python -B verify_portable.py

Requires Python 3 and **already installed SymPy** for the CLT's exact algebra
checker; no installation is performed. The unchanged receiver itself and the
new saved-arithmetic checks use only the Python standard library.
For hash/source/saved-arithmetic checks without child execution:

    python -B verify_portable.py --integrity-only

The default verifier checks every delivered source byte and all 159 runtime
pins, replays only unchanged `admit.py` on its exact saved input, and compares
**all non-timing output fields**. It also invokes the accepted CLT verifier,
which runs its two ordinary exact checkers in temporary directories and checks
38 original source pins plus 63 deterministic numerical pins. The portable
closure adds two existing source-readback-bound FINAL_VERIFICATION snapshot
JSONs omitted by the historical 54-file audit manifest; see
`PORTABLE_CLOSURE_ADDENDUM.json`. No original manifest or source is changed. Package bytes
are verified unchanged afterward. No scalar or variance solver is rerun.

`PORTABLE_SCIENTIFIC_ALLOWLIST.json` is the new explicit delivered source set;
`PACKAGE_MANIFEST.json` binds all delivered payloads. The old numerical
`AUTHOR_FREEZE.json` and `RECEIVING_MANIFEST.json` are retained as **historical
identities**, not as controlling portable allowlists. Their full historical
test closures are **not reproduced**. Crafted loading/cache experiments and
the blanket receiver author/history verifiers that traverse them are omitted.
The exact 159 runtime rows include inert old ordinary meter source texts and
plain loading/cost records: the unchanged receiver **hashes**, but never imports
or executes, them. No silent repinning or adaptation of the accepted receiver
has occurred. Do not run arbitrary historical helper files merely because
some are present as frozen dependencies; this package's supported entrypoint is
`verify_portable.py` only.

## Costs, ordinary methods, and limits

Three already completed scalar acquisitions remain separately charged, including
the final corrected-loader run: **92,474,955 rational operations** in total.
The sample's conservative abstract cold-work bound is
`3002000000000000770888957952` schoolbook bit operations, below its input budget
`10^30`; it is not CPU instructions, practical elapsed cost, or physical cost.
The loading defect/repair is plain provenance, not a security assessment;
old acquisitions are not retroactively called corrected-loader executions.
Prior discovery/research effort is not advertised as fully metered complexity.

All mathematical components use ordinary full-generator identities, stopped
martingale estimates, exact rational algebra, deterministic inverse-flow bounds,
interval Taylor integration and ordinary martingale weak convergence. The
operation acquired here is the **source-bound, paid actual-path interface**
from the corner entrance through removal, plus the separately justified growing
cutoff CLT bridge—not a replacement for SSA/ODE/LNA or a new general solver.

`BASELINE_COMPARISON.md` preserves empirical ordinary-method wins, losses, costs
and failures. Those pilots are a separate evidence appendix, **not proof
inputs**, and were not rerun while packaging. Original scalar/variance solve
receipts are received without another acquisition. No external retrieval,
upload, publication, installation or hardware action was performed by packaging.

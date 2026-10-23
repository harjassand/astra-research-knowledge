# Astra Amplification Cycle 2 — PRO3

**22 October 2026, Australia/Brisbane.**

This is a source-complete mathematical checkpoint on proposal-start sampling.
It accepts the received optional-prefix obstruction within its exact scope,
proves a sharp robustness theorem for a structurally controlled local kernel,
and proves a finite-space tempered-screen extension. It does not claim a
practical sampler speedup, historical priority, or external acceptance.

## Start here

1. Read REPORT.md for the result, mechanism, actual calculations and costs.
2. Read SAFE_LOCAL_THEOREM.md for the full arbitrary-measurable-space theorem
   under a fixed common qL<=Lambda q bound.
3. Read TEMPERED_SCREEN.md for the finite-space construction, zero-floor theorem
   for every eta>0, sufficient sharp-K interval and unresolved interval.
4. Read the corresponding actual-source bindings in reviews/. They identify
   precisely which proof bytes were reviewed.
5. CONTINUATION_SEED.md is the latest next-question statement. It supersedes
   only the future-question paragraph of the unchanged main proof.

The strongest new result is

    log(n) sup TV(q C^n,pi) -> K,
    epsilon log T(epsilon) -> K,

for fixed K>0, alpha in (0,1), common finite Lambda>=1,
C=(I+alpha G+(1-alpha)L)/2, q initialization, fixed pi-reversible L,
D(pi||q)<=K and qL<=Lambda q. A standard delayed-acceptance local move
implements Lambda=2 without the target normalizer. Pure IMH already has K.

The extension fixes a finite positive class and symmetric Q. Every eta>0 gives
zero uniform error floor. Eta>1-alpha exp(-K)/2 gives coefficient K. The
threshold is sufficient, not necessary; the sharp rate below it is open.

## Verify the delivered source

Only Python 3 and its standard library are required. The producer used
Python 3.12.14 on Linux. No installation, network, credentials or paid service
is needed for verification or the new computational replay.

After extraction, from this directory:

~~~~bash
python3 verify_manifest.py
python3 replay.py --receipt /tmp/astra_pro3_cycle2_receiver_replay.json
~~~~

The first command checks all manifest payload identities, the immutable old
owner ZIP identity and CRC, and the two reviewed proof hashes. It does not
rerun science. The second executes only the four NEW diagnostic configurations
in isolated temporary directories and compares their scientific JSON to the
included results, ignoring measured runtime fields. It leaves original sources
and receipts unchanged. Its output is a receiving replay, not a theorem proof.

To check a ZIP directly without extraction:

~~~~bash
python3 verify_manifest.py --zip /absolute/path/Astra_Amplification_Cycle2_PRO3_20261022.zip
~~~~

To reproduce a particular principal calculation in a disposable working copy:

~~~~bash
python3 safe_local_calculations.py --precision 80 --output /tmp/astra_pro3_80.json
python3 safe_local_calculations.py --precision 120 --output /tmp/astra_pro3_120.json
~~~~

The main implementation uses exact Fraction kernels and Decimal matrix
calculations. Full memoization, current-state caching, all component proposals
and actual threshold bracketing are explicit. The frozen input is in
EXPERIMENT_CONTRACT.md; COST_CONTRACT_ADDENDUM.md documents the stronger cache
comparison added after the independent cost challenge. No empirical holdout or
trajectory-discovery claim is made.

build_archive.py records a deterministic manifest and archive using fixed
member metadata. It requires an output path outside the source directory.
The delivered archive SHA256 is recorded externally in the delivery receipt
and private Page to avoid a self-referential digest. Rebuilding from unchanged
payloads with the same zip implementation is intended to reproduce those bytes;
payload hashes remain the authoritative portable identity check.

## Source map

| Location | Purpose |
| --- | --- |
| REPORT.md | Self-contained scientific report and matched comparisons |
| SAFE_LOCAL_THEOREM.md | Main theorem, finite certificate, lower bound and inversion |
| TEMPERED_SCREEN.md | Weaker-screen proofs and precise remaining question |
| RECEIVED_PREFIX_ACCEPTANCE.md | Owner's one-time assessment of supplied proofs |
| EXPERIMENT_CONTRACT.md | Preserved pre-output diagnostic contract |
| COST_CONTRACT_ADDENDUM.md | Explicit full-memoization strengthening |
| FAILED_APPROACHES.md | Counterexamples, rejected shortcuts and comparison failures |
| CONTINUATION_SEED.md | Latest owned state and next construction |
| SOURCES.md | Primary literature and inherited mathematical dependencies |
| PRESERVATION.md | Exact historical identities and closed operations |
| results/ | Principal outputs, precision check and isolated replay receipt |
| reviews/ | Distinct independent challenges, exact code, results and proof bindings |
| sources/ | Unchanged previous native owner ZIP and received prefix source |
| authority/ | Actual latest prompt and inherited private handoff protocol |
| RESOURCE_RECEIPTS.json | Observed work intervals and executable costs, with unknown totals |
| STATUS.json | Internal correctness, novelty, efficiency and delivery-status separation |
| MANIFEST.json | Every payload identity, excluding the manifest itself |

## Receiving and integration instruction

Max owns programme integration. The evaluator may inspect the same source.
Use the private Page and exact native references in the external delivery
receipt. The accompanying UTF-8 base64 transport decodes to the exact ZIP;
it is not a separately rebuilt archive. No public-sharing change is authorized.

Record any receiving check or mathematical acceptance separately from the
producer's upload and readback. Do not interpret a delivered file as read,
accepted or integrated. Preserve both old native source bytes and the new
source binding. No user relay or administrative action is required.

The active continuation is the sharp rate for the fixed tempered family in
the unresolved positive-eta interval. The old J>K, fixed-prefix and restricted
uniform-null optional-prefix questions are closed internally. The B3 pISO
correction and failed full inference, metadata rejection and R3/anMC rejection
remain within their original scopes. Other protected scientific owners remain
independent.

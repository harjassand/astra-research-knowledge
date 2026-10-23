# Resource and unsuccessful attempt accounting

## Accounting rule

The producer calculation, construction of its representation, rejected
certificate attempts, envelope optimization, ordinary comparator, and
independent replay are all charged. Nested timers are not added twice.
Process CPU, process peak RSS and observed wall time are different quantities;
peak RSS values are not summed across sequential stages. External service
latency, analytical development and model inference are not fully observable.
Their absence from a process receipt is not a claim that they cost nothing.

## Actual matrix operation

The authoritative receipt is results/experiment_resources.json, supplemented
by input_construction.json and per-probe resource entries inside
krylov_certificates.json. The complete producer body is 59.441511705001176 s
wall, 59.430268817 s process CPU, peak RSS100147200 bytes. It includes both
depths32/64, candidate/classical/stored-probe envelopes, and the dense comparator.
The total is not the sum of separate repeated headline benchmarks.

| Component | Wall s | Accounting relation |
| --- | ---: | --- |
| Exact-input construction | 0.2587475740 | Included in producer total |
| Bit/probe/coupling construction | 0.4594056700 | Included |
| Eight64-step Lanczos proposals | 0.0299058760 | Included; k32 is a prefix |
| All16 integer Krylov residual checks | 0.4106008360 | Included |
| All16 Jacobi node/weight constructions | 27.6004404200 | Included |
| Eigh dense proposal | 0.1709384680 | Included |
| Full dense integer verification | 1.5049099450 | Included |
| All exact envelope analyses | 27.9854925680 | Included |
| Remaining producer bookkeeping/serialization | 1.0210703480 | Difference to measured total |
| Full independent saved-witness replay | 33.1438115650 | Additional, not in producer total |
| Saved-witness error-mechanism calculation | 0.0535070140 | Additional |

The matrix-vector proposal count is512. There are1024 full reorthogonalization
passes, one complete dense eigendecomposition, and16 Krylov residual block
products. Gram checks and sparse block products have their full actual runtime
included. Bit generation draws68736 bytes once for4296 Box–Muller pairs.

The small-J weight target1e-28 led to18 unsuccessful intermediate precision
attempts totaling17.9024035730 s. This is a subset of27.6004404200 s, not an
additional charge. All attempts and final settings are retained in each
certificate. Six k64 probes completed after three attempts, two after four.
The32-step certificates completed on their first attempt. Final settings are
164/196 Decimal digits and204/236 root-fractional bits at k64;100 digits and140
bits at k32. Root bits refer to the integer-J coordinate before division by2^32.

Exact envelope optimization costs by depth and estimator are stored inside
cdf_results.json. At k64: candidate5.9841130240 s; classical8.6601622290 s;
deterministic stored-probe5.4032619330 s. At k32:2.4394229230,3.1672096860 and
2.1518073450 s respectively. They are subsets of the envelope-analysis stage.
The literal rational implementation is not presented as optimized.

The replay receipt records33.137147331 s CPU and84217856 bytes peak RSS.
It performs no eigensolve or random draw. It re-evaluates the whole exact
envelope, so receiver verification is charged rather than assumed free.

## Distinct local proof and implementation challenges

All raw receipts are included. These measured script bodies are additional to
the full matrix experiment unless explicitly marked as nested fixtures.

| Local question or challenge | Recorded wall s | Where recorded |
| --- | ---: | --- |
| Projection-transfer algebra and counterexamples | 0.18681 | results/projection_lemma_checks.json |
| Residual completion, moments, sharpness | 0.13953 | results/residual_construction_checks.json |
| Uniform Gaussian/Dirichlet diagnostics | 0.42445 | notes/uniform_probe_diagnostics.json |
| Two bounded Jacobi checker suites | 5.04186 | results/certified_jacobi_development_costs.json |
| Initial repaired-input adversarial probe | 0.001324 | results/exact_residual_initial_adversarial_probe.json |
| Full integer/source-boundary audit | 0.080959 | results/exact_residual_projection_agent_audit.json |
| Finite-bit Gaussian tests | 0.351134 | notes/gaussian_bits_diagnostics.json |
| Independent integrated CDF/floor/count audit | 0.07545 | results/integrated_cdf_audit_receipt.json |

Some wall timers exclude interpreter/library imports. Where a whole command
duration was available it is retained in the corresponding cost file: e.g.
0.841865104 s for the complete integer audit invocation and0.388217128 s for the
Gaussian test process. Nested fixture generation/replay timings must not be
added again to their enclosing tests. Earlier Gaussian smoke fixtures are
retained with their own generation receipts. Plot creation has a separate
figure_resources.json and is presentation work, not a new scientific run.

## Rejected premises and repaired implementation attempts

1. Horizontal eigenvalue shifts alone for probe-weighted CDF transfer: rejected
   by exact isospectral rotation counterexample. The valid theorem adds
   projection leakage. Its proof/test cost is in the projection receipt.
2. Original triangle bound sqrt(2r^2+z^2)+r: valid but loose. Independent proof
   removed double counting and established the sharp function used here. No
   full matrix run used the weaker formula; analytical cost is unmetered.
3. Claim that uniform SLQ bands were new: rejected on reading primary CTU2021.
   Dirichlet/DKWM priority remains unknown. No false novelty claim retained.
4. Decimal abs under a low-precision ambient context: corrected by exact
   copy_abs before the first Jacobi test execution. Both bounded suites passed.
5. Unchecked standalone residual-checker dtypes/symmetry, negative tau and
   silent integer truncation: found by source audit, repaired with strict
   validation. Dynamic tests ran after repair; no pre-patch test success is
   claimed. Malformed inputs and overflow candidates are explicitly rejected.
6. Replay Gaussian block dimensions/denominator/count binding: repaired before
   delivered replay. The actual producer already used the intended dimensions.
7. Insufficient intermediate small-J interval precision:18 charged attempts as
   above. Original proposal coefficients were not changed; no new probes drawn.
8. Small-depth lag/lead CMS operation as an economical uniformly accurate
   spectrum estimator on this input: defeated by complete comparator and
   proved saved-envelope floor. No larger depth or new target was tried.

## Source retrieval and external tools

The supplied restoration ZIP and original owned Page were read privately;
neither original archive was changed. The exact requested source was recovered
without a user relay. Primary literature was searched and read; the dedicated
follow-up novelty check records three batched searches plus four retrieval/find
calls, approximately23.9 s of returned tool latency. Earlier search/retrieval
latency and reasoning are not fully metered and are not included in that figure.

Data retrieval attempted the official SuiteSparse route (HTTP redirect to an
HTTP host, then403; HTTPS upgrade returned503 after approximately30 s) and the
official NIST gzip links. Default restricted network calls failed immediately.
Escalated Python urllib NIST requests returned403; the same official URLs via
curl with a browser User-Agent succeeded, downloading44011 bytes for K and6743
for M. Failed requests were not authorization-review rejections and did not
lead to permission or account changes. Initial failure receipts are in
sources/dataset_download.json; source URLs/hashes and successful route are in
SOURCES.json. Exact total transfer/service latency is unknown.

Two primary arXiv PDFs were downloaded for reading (1455514 and786588 bytes),
with exact hashes in SOURCES.json. They are not bundled as full texts. Reading,
search, source preparation, patches, agent mathematical work, tool startup,
compression/private-upload transfer, model inference, monetary charges and
energy cannot be reconstructed exactly from the available process receipts.
They remain explicit unknowns. The package does not equate its archive size or
number of agents with scientific progress and does not claim a fully metered
programme-wide compute total.

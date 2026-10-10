ACQUIRED PROBABILITY AND SAMPLING OPERATIONS
Unpublished research checkpoint — 2026-10-10

The requested historic 9–10/10 breakthrough has NOT been established.
The strongest retained result is a constructive algorithm for a specified
class of globally coupled stochastic systems. Its general proof is internal;
historical originality and strongest-baseline advantage remain UNKNOWN.

THE EXECUTED CAPABILITY

Given rational independent local chains, additive state-dependent hazards,
and product laws for global resets, acquire stationary event probabilities
from local killed heat kernels and a small reset-channel matrix. Refine
prefix probabilities to sample a whole stationary configuration. The written
construction claims polynomial bit cost for probabilities and expected
polynomial bit cost for exact sampling, without simulating global mixing.

Read research/reset_sampler/REGENERATIVE.txt, then RESULT.txt. The implemented
case has two-state local components and a positive total-hazard floor. It
uses classical renewal rewards and positive Markov-tree normalization;
it does not establish an advantage over renewal methods. The broader
nonreversible multistate construction remains unimplemented.

Concrete results:

* 64 heterogeneous components, 2^64 implicit configurations: the stationary
  all-ones probability is enclosed in
  [2201937448628,2201937448629] / 2^75.
  This is approximately 5.82847989619e-11, with relative interval width
  below 4.55e-13. It used 42,544 positive nodes, 328-bit arithmetic, about
  391 seconds and 39,485,440 bytes peak RSS on this macOS host. The code
  never builds the full transition matrix. See regenerative_large_receipt.json.
* Four small stationary event enclosures contain independently computed
  exact rational probabilities, including a three-channel case with
  deterministic reset laws. See regenerative_verification.json.
* The uncapped acquired-probability sampler completed a three-coordinate
  path in about 8.5 seconds. The receipt preserves its random bits and
  certified comparisons for replay. The mathematical exact-distribution
  guarantee assumes independent ideal fair bits; the executable uses
  software randomness. One path is not a distributional validation.
* A separate 32-component first-hit Laplace transform was enclosed to
  width 2^-48 without enumerating 2^32 states. It certifies that primitive,
  not a complete first-hit CDF implementation.

ACQUISITION AND ADDITIONAL CONSTRUCTIONS

research/reset_sampler/ACQUISITION.txt derives relative rare-cylinder and
TV stability from local parameter errors. Its costed calibration requires
known structural zeros, isolated local clock probes, and forced labelled
reset draws. Passive observation does not supply those controls for free;
physical unknown parameters yield an approximate true-law guarantee.

Other internal constructions include arbitrary-start and nonreversible
first-passage queries, acquired signed-product surviving-state representations,
and adaptive sparse-detector Bayesian experiment selection. Their exact
interfaces and incomplete implementations are separated in CLAIM_LEDGER.json.
Known or narrower measurement, algebraic and nonlinear routes are preserved
under preserved_routes/ and are not being elevated into breakthrough claims.

REPRODUCE AND HAND OFF

Run: python3 REPLAY.py
This uses only the Python standard library, works in a temporary copy, and
checks small exact comparators, recorded sampler bits, interval arithmetic,
and finite state/posterior diagnostics. It preserves the supplied receipts.
Run: python3 REPLAY.py --large
This also repeats the 32- and 64-component runs (the latter took 6.5 minutes).
Run: python3 REPLAY.py --integrity-only
Hashes establish byte integrity, not scientific correctness.

REPLAY_RESULTS.json records the actual portable replay. PROVENANCE.json and
MANIFEST.json map source bytes. SOURCES.json records primary literature and
standard ingredients. REPO_HANDOFF.txt and DRAFT_CHECKPOINT.json prepare the
existing repository workflow. The repository checkout remains unchanged:
no commit, push, PR, merge or scientific publication has occurred.

The landmark objective remains open. The scope and known renewal baseline
are substantive limitations, not missing wording or presentation. Further
work should pursue a different mechanism rather than repeat audits of these
narrow candidates or inflate the implicit state count into significance.

# Executed correlated static acquisition: exact model, finite sampling and honest costs

The supplied [implementation guide](package/static_execution/README.md), [results](package/static_execution/results.json) and [recorded transcript](package/static_execution/run_stdout.txt) demonstrate the static operations used by the [correlated theorem](README.md). The acquisition core receives explicit rational local factors and pinned heat-bath samples, **not enumerated probabilities or exact reference partitions**. The [reference enumerator](package/static_execution/exact_reference.py) is separate.

The fixture has six vertices, ten nonsymmetric edge-failure variables, ten pair interactions and 31 full cuts. Five very reliable edges form a spanning tree. Certified logarithmic contrast is `c=3`, Dobrushin coefficient about `.3731187291`, and ordinary odds contrast about `1.8325e12`. A small global state space of 1024 configurations permits exhaustive reference checks; this is not a large-network benchmark.

| Quantity | Producer-recorded result |
|---|---:|
| Exact correlated disconnection probability | `3.7252956888856366e-28` |
| Acquired estimate | `3.800863790182855e-28` |
| Point relative error | `+2.0285%` |
| Executed probability interval | `[2.894287567127758e-28,4.754035930511187e-28]` |
| Same-marginal independent-edge probability | `1.979382140288482e-28` |
| Correlated/independent ratio | `1.8820497634` |

The interval contains the reference but is wider than ten percent. Its ideal-bit failure budget is at most `.02` plus explicit cap failures. The 2.03% point error is not a 10%-confidence execution of the parent theorem.

## Actual operations, including unused proposals

The engine acquired 32 partition estimates with 32 sampled marginal stages and 12,904 draws per sampled stage, plus exact local envelopes/cached prefixes. All 32 intervals contain their exact reference partitions. It used **437,504 independently restarted pinned draws and 35,080,166 heat-bath updates**. The conditional phase generated 16,384 proposals in batches and consumed 8192; unused proposals are counted. The record includes 70,160,332 heat-bath integer random operations, 97,645,560 native PRNG words, Python random-bit work and finite rejection caps.

Every conditional output is failed/disconnected. Empirical histogram TV is `.0184463`, but the per-output analytic acquired-weight bound is about `.145675` plus mixing contribution, and the simple joint 8192-output TV bound is vacuous. Empirical distance is not a guarantee for the output law. Seeded PRNGs reproduce the execution; theorem probability statements use independent fair bits. Caps abort explicitly without a biased fallback.

Reported total wall time was about 2.992 seconds including compilation/reference validation on the source environment, one run rather than a general performance claim. Capital did **not** execute or compile anything. [Original Python core](package/static_execution/gibbs_static.py), [C++ source](package/static_execution/pinned_heatbath.cpp), [supplied binary](package/static_execution/pinned_heatbath), [runner](package/static_execution/run_demo.py).

## What this implementation does and does not establish

The fixture belongs to the theorem's direct-enumeration branch: all 31 cuts lie below the supplied cutoff. Scalable weighted contraction is not implemented. Observed proposals all had multiplicity one because additional failures were extremely rare. The inverse-multiplicity identity is implemented and verified on all reference states, including intersections, but this is not an empirical overlap stress test. No time-dependent CDF experiment was run.

The code uses exact rational **random-scan** transitions, capped integer rejection and arbitrary-precision Python fallback beyond its native limits. The parent proof separately supplies a systematic dyadic implementation with deterministic bit budget. The local-table construction costs `sum_i 2^d_i`; this fixture has maximum neighborhood degree three and 46 entries. The general theorem takes certified influence bounds as input, not a magically efficient procedure to discover them at unbounded degree.

The conservative parent allocation for `epsilon=.1`, `delta=.01` and this query count is separately calculated as 26,214,400,000 pinned draws and at most 6,291,456,000,000 heat-bath updates. It was not executed. Model factors, topology, exact sampler access, physical rate measurements and physical safe initialization are supplied or separately paid. The result is a real finite static-acquisition diagnostic with scoped confidence, not a deployed reliability predictor or a full general-algorithm performance claim. [Complete execution checkpoint](package/static_execution/TO_ROOT_RESULTS.md), [original package and hashes](SOURCES.json).

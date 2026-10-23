# Observed work and the boundary of the resource claims

Astra PRO 2, Cycle3, 22 October 2026 Australia/Brisbane.

## Distinct computation bodies

All new certificate arithmetic is Python standard-library integer/Fraction
arithmetic. There was one producer invocation and one initial invocation of
each checker listed here. No optimizer, precision sweep, external package
installation, GPU or purchased compute was used. These are observed body
timings, not a total investigation time or an end-to-end application speedup.

| Body and receipt | Wall seconds | CPU seconds | Process peak RSS bytes |
|---|---:|---:|---:|
| Five witness constructions, serialization and symbolic sizes; results/producer.json | 0.639518112 | 0.639480692 | 23703552 |
| Independent five-witness checker and four negative controls; results/independent_new_witnesses.json | 0.884272505 | 0.883769656 | 36524032 |
| Classical coloring, actions and noisy decoder on two supports; results/classical_upper.json | 0.501814641 | 0.501677026 | 44331008 |
| Failed recursive frame construction check; results/fan_port_checks.json | 0.025995729 | 0.025995013 | 13631488 |
| Independent interface failure check; results/interface_challenge_checks.json | 0.010813079 | 0.010811112 | 10878976 |
| Sum of the five distinct bodies | **2.062414066** | **2.061733499** | **44331008 maximum** |

Per-case timers inside these bodies overlap their enclosing timer and are not
added again. RSS is the process high-water mark, not incremental allocation;
adding RSS values would misrepresent memory. Producer imports before its timer
are excluded; loading its inherited tent module inside the timer is included.
The checker and comparator bodies also have interpreter/import costs outside
their internal timers. The separate receiving replay includes subprocess
startup in its outer timing.

The two unsuccessful-design diagnostics are charged. Their analytic failures
are retained in FAILED_APPROACHES.md and the contributor notes. No failed
numerical parameter runs were omitted. This is not a claim that proof search,
discarded mathematical ideas or authoring cost zero.

## Source, proof, research and delivery overhead

The exact common/owned archive hash and byte comparison took 0.095637879 seconds
in its observed local scope. The bounded primary-literature contributor made
14 calls with 44.0 seconds of reported source-access latency; its complete
scope and failed retrievals are in notes/literature_cycle3.md. Root also read
primary sources. Root access, reading, proof development, review, reasoning,
code authoring and service/inference overhead were not instrumented as a
complete additive total. These unknown costs are additional, not zero.

The first recorded UTC clock was 2026-10-21 17:57:25. At 18:28:41, at least
1876 seconds of this investigation's wall interval had elapsed, including
overlapping contributors and authoring. This is not CPU time, a sum of agents,
or a measure of scientific productivity. Later packaging/delivery adds time.
The final private delivery receipt records its own observed boundaries.

One receiving replay was performed in a relocated copy, without regenerating
the five frozen witnesses and without replaying previous science. Its exact
outer wall/CPU/resource receipt is results/receiving_replay.json; the per-script
receipts are in results/receiving_replay/. They are verification overhead in
addition to the original five bodies, not a second discovery. Archive creation,
hashing, persistent upload, text transport and readback are separate delivery
work. The external immutable delivery receipt records them after the archive
identity exists; it cannot be included retroactively without changing that
identity.

The replay passed on Python3.12.14/Linux with outer wall1.748051015 seconds,
parent CPU0.023017387 seconds, children CPU1.723011 seconds, parent peak RSS
14024704 bytes and children peak RSS44322816 bytes. All substantive outputs
matched the original frozen records. Its outer timer includes payload hashing,
relocation, subprocess startup, output comparison and receipt preparation up
to the timer. It checked39 payload files before adding its own records.
results/pre_receiving_manifest.json preserves that exact pre-seal manifest;
the final MANIFEST.json additionally binds the receiving records and final
documentation. The ZIP seal checks every final manifest entry without rerunning
any scientific calculation.

No money or energy meter was available. No spending, hardware-credit use,
external outreach, public disclosure or sharing-permission change occurred.

## Mathematical construction versus implemented operation

PROOF.md specifies finite universal hard graphs for every fixed t and target R.
They are not all materialized. Their recurrence is evaluated exactly:

    h=t(t+1)/2, m=t(t-1)(t+2)/2+2, b=1+t^2(t+1)/2,
    n_0(R)=1,
    n_t(R)=b + m*4(t+1)*b*R^4*h*n_(t-1)(2hR).

Already n_2(1)=62,708,695, and n_2(2)=16,052,698,375. These are symbolic
counts, not experimental instances. The universal existence proof chooses
eigenspaces, nullspaces and normalized matrices over exact reals. It supplies
a complete mathematical operation but does not claim a fast certified
implementation of all these steps on arbitrary floating inputs. Large
coefficients in the coning lift do not invalidate the action estimate;
representing/certifying them can still cost substantial work.

The actual fixtures exercise both branches and the coning operation using
explicit rational inputs. Their complete input blocks and supported matrices
are saved. Exact equality checks avoid uncharged floating backward error, but
the bit cost of integer arithmetic is included in the timings rather than
treated as unit cost. The largest fixture has 9223 vertices, 18059 support
edges, five action columns and 6151 nonzero stored matrix coefficients. The
checker verifies the full action and finds squared norm exactly 1/3072, with
an entry/principal-submatrix certificate of operator norm at least one.

These fixed-design examples do not measure the optimal all-design lower
constant. No optimization of graph size, divergent rate or conditioning was
performed. Their role is to check that the proof's cancellation and input-error
operations survive exact executable use.

## Positive comparator and its acquisition costs

The matching positive operation is established star-color/direct-read recovery.
src/classical_star.py implements it on chordal inputs, finding and validating
a perfect elimination ordering. It includes heap-based maximum-cardinality
search, later-neighbor clique/width validation, coloring and verification of
distinct isolated action cells. Preparation uses O((n+m)log n+n t^2) elementary
set/heap work on a chordal width-t support, apart from the implementation's
edge sorting. A supplied general tree decomposition can be completed and
colored; obtaining that decomposition is an additional cost not implemented
or timed here. One must not silently infer a fast decomposition oracle.

There are K_t physical matrix actions in the general upper guarantee, even
when the seed is stored compactly as one coordinate label per vertex. For an
explicit sparse matrix, a straightforward block action costs O(q(n+m)) work
and O(nq) output storage. An implicit physical operator may have a different
and dominant action cost. The direct decoder selects one action cell per
diagonal/edge, O(n+m) reads and output coefficients, with each offdiagonal
copied symmetrically. It gives ||Dhat-D||_F<=sqrt(2)||E||_F for arbitrary E.

The actual comparison simulates both exact and deterministic noisy actions
on the same 9223-vertex support using six queries, and on the 1651-vertex
treewidth-three fixture using eight (at most K_3=10). Both recover exactly
when E=0 and satisfy the exact squared error inequality with the saved E.
Those computations are explicit sparse operations, not an implicit-action
performance benchmark. The latter fixture's eight-query success underscores
that it is a bad saved nine-column design, not a graph requiring ten queries.

For a finite-precision use, graph construction, query generation, acquired
action error, arithmetic in preparation and recovery, and any downstream
spectral estimate must all be charged. This capsule makes no such practical
speed claim. The new theorem's significance is the sharp distinction between
exact identification and a uniform noisy inverse.

## Historical comparison remains unchanged

The exact-decimal NIST n=1074 dense verified calculation remains the original
incumbent: 1.675848413 seconds before shared input conversion, with width9/1074.
The old common completion took39.019276241 seconds plus separate review/replay,
and the earlier full fixed experiment took59.4415 seconds with maximum width
0.6288212904932393. They are historical recorded results, not rerun timings.
The new theorem does not reverse those defeats or establish a downstream
spectral gain. The molecular family remains closed at its recorded width and
proved family floor. All original proof, input, comparator and failure records
are preserved unchanged through sources/Astra_Amplification_Cycle2_PRO2_20261022.zip.

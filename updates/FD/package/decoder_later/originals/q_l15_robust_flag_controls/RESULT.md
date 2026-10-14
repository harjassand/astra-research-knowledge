# Matched persistent-source RM controls

## Result

The strongest direct standard-RM control tested here is full-cube RM(2,16)
coordinate-flat checksum majority. It is correct on the same source fixture,
but it does not reduce acquisition cost relative to q_s09's sampled shifted-ball
decoder: it used 57.7% more logical comparator requests, 63.5% more distinct
external directed pairs, and 2.17 times the acquisition time. Standard random
affine-cube local RM correction also returned the exact model, with lower peak
RSS, but took 12.3 times as long and used 76.4% more distinct external pairs.
For this fixture, the local decoder's checksum/parity work is the main
bottleneck.

These are one seeded finite replay per method, not an empirical success-rate
claim. Each returned model was checked only after return against all 65,536
ranks, all 65,536 sampler points, all 16 coefficients, the promised partial
flag, and 64 inverse targets; the checker found zero errors.

## Matched source and access

Every run used n=16, r=2, epsilon=1/32, beta=.05, fixture seed 960162,
learner seed 1060162, and the same `asymmetric_hash` source. Its fixed bad set
contains exactly 2,048 items (density 1/32), sampled once from seed 1660162.
The learner receives only original-directed `C(x,y)` answers. On clean pairs
the answer is the hidden teacher's strict rank comparison; on pairs incident
to the fixed bad set it is a persistent arbitrary directed hash answer. No
reverse answer is inferred. The bad set, ranks, and labels remain inside the
source/test harness; truth checks happen after acquisition.

All three use the same q_s09 acquisition and sequential matching validator,
the same confidence budgets and candidate cap, and an exact source-ordered
pair memo capped at 250,000 entries. A decoder's random draws can change the
subsequent candidate and validation path, so these are matched by source,
parameters, and initial seeds, not by an identical candidate transcript.
Repeated calls to an ordered pair are cache hits while retained; after the
cache fills, repeated pairs again reach the source. The exact unique-pair
column below was measured by logging every external ordered pair and sorting
the IDs, not inferred from the cache size.

| Body decoder | Result | Logical comparator requests | External source calls | Distinct external ordered pairs | Acquisition seconds | Peak RSS |
|---|---:|---:|---:|---:|---:|---:|
| q_s09 shifted-ball RM majority | exact model | 2,796,822 | 2,796,630 | 2,360,723 | 6.700 | 63.0 MB |
| Full-cube RM(2,16) checksum majority | exact model | 4,410,123 | 4,409,984 | 3,860,253 | 14.559 | 72.8 MB |
| Random affine-cube local RM correction | exact model | 4,613,734 | 4,613,509 | 4,164,005 | 82.108 | 48.2 MB |

External source calls include repeats after the memo cap. Those repeated calls
number 435,907, 549,731, and 449,504, respectively. Acquisition time includes
decoder setup/preprocessing and excludes source construction (under 0.001 s in
each run) and post-return exhaustive checks (3.3–3.5 s, with no source
comparisons). The timings are single-run measurements. Process peak RSS
includes Python and the source/test harness, so it is not a decoder-only
space bound.

## Decoder costs

The q_s09 decoder processed 35 bodies using 244,545 shifted-ball raw-label
requests, 1,785 sampled rounds, and 227,675 coefficient votes. Its matching
validator used 2,526,705 comparison requests over 27,857 batches.

Full-cube RM decoded 26 bodies and requested all 65,536 raw labels per body:
1,703,936 raw-label requests, 66,453,504 checksum tests, and 233,439,232
parity-input reads. The matching validator used 2,444,043 requests over
26,721 batches. Its decoder holds a 65,536-byte truth table per body, in
addition to the RM checksum masks.

Local RM decoded 31 bodies. For the raw-label error promise rho=2epsilon=1/16,
it uses l=10, K=1,024 points per random affine cube and R=51 independent cubes
per each of M=137 unisolvent anchors. The decoder counted 221,795,328 raw
callback accesses, 216,597 cube decodes, 3,825,969,408 checksum tests,
12,420,538,368 parity-input reads, and 34,655,520 random bits. Per-body raw
label caching means these callback accesses are not all source comparisons;
the whole acquisition made 4,613,734 logical comparator requests. The matching
validator used 2,319,974 requests over 25,326 batches. The local corrector's
truth table is 1,024 bytes per cube, but its repeated checksum/parity work
dominates elapsed time.

The raw label for a true toggle v is `g_v(x)=1 xor C(x,x xor v)`. For any fixed
bad set and arbitrary answers on incident pairs, its error support is
contained in `B union (B+v)`, hence has density at most 2epsilon=1/16. Both
RM controls get labels only through the comparator callback. Full-cube RM is
deterministic within the RM(2,16) unique radius 1/8; local RM uses the pinned
random-cube correction with the same global raw-error promise. The tested
benchmarks therefore establish finite correctness, while the work and cost
comparison point against these RM controls as replacements in this
implementation.

## Receipts and replay

The no-logging acquisition receipts are `../q_s09_robust_flag_implementation/receipt_n16_r2_hash_directed_bounded.json`,
`full_cube_rm_n16_r2_hash_directed.json`, and
`local_rm_full_learner_n16_r2_hash_directed.json`. Exact distinct-pair audit
receipts are `unique_pairs_s09_n16.json`, `unique_pairs_full_cube_n16.json`,
and `unique_pairs_local_rm_n16.json`.

Replay the two controls and exact unique-pair audits from this directory:

```sh
python3 rm_controls.py --case full-cube --n 16 --r 2 --seed 960162 --epsilon 0.03125 --beta 0.05 --mode asymmetric_hash --bad-count 2048
python3 rm_controls.py --case local-full --n 16 --r 2 --seed 960162 --epsilon 0.03125 --beta 0.05 --mode asymmetric_hash --bad-count 2048
python3 unique_pair_replay.py s09
python3 unique_pair_replay.py full-cube
python3 unique_pair_replay.py local-full
```

The exact distinct-pair audit writes a temporary ordered-pair log, externally
sorts/deduplicates it, and removes the temporary files. That logging overhead
is not included in the primary acquisition-time column; the audit receipts
report their instrumented replay time and sort time separately.

## Scope

This is a source-model finite control, not an external acquisition experiment
or asymptotic comparison. No theorem about optimality or superiority follows.
The local-cube lane separately tested 16 target labels and one full body, but
those harness-only diagnostics supplied a true direction and are not used as
full learner results here.

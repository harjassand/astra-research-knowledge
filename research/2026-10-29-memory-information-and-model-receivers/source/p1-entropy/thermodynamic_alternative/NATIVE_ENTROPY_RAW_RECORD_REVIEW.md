# Independent raw-record and confidence review

29 October 2026, Brisbane. Reviewed the native producer, the original
one-window consumer, and the two-score reuse consumer. The audit first
froze a complete certificate reconstruction using ONLY public inputs,
raw records, consumer sources and their saved outputs. Only after that
PASS was saved were the producer and private source inspected. No source
was redrawn, and neither root consumer was rerun or overwritten.

## Verdict and exact scope

**PASS at the stated ideal independent native-trial and instrument contract.**
The raw counts, hashes, finite confidence calculation, outward arithmetic,
units and source-factory correspondence agree. The stronger reuse certifies

    E/R >= 0.22322364980255016 nats per native departure,
    sigma >= 0.14297416604265997 nats per native clock unit,

with simultaneous failure at most 1/1000 for its two fixed scores and one
mean bound. The earlier separately preserved one-window certificate gives
sigma>=0.08206251553031438 at failure at most 1/1000. The two separately
reported certificates are not automatically a joint 1/1000 event; the
reused two-score certificate carries its own full union-bound allocation.

This is a synthetic numerical source. There is no complete proof that
NumPy floating samples have the exact ideal CTMC distribution, no physical
assay, and no independent acquisition of the supplied calibration, reset,
tail or time-reversal premises. Those limits are already disclosed in the
producer and consumers and remain applicable to this review.

## 1. Raw bytes and counts

The retained record is a 2,044,454-byte NPZ containing four individual
arrays of length 262,144: start port, return port, upper native-hold ticks,
and upper interior-duration ticks. No aggregate Binomial counts substitute
for the individual records. Its SHA256 is

    10167bbe38d5f5a8ed902763c834402a78ed35d9e4ea3a6948d624344a954e7a.

Both consumers and the producer receipt bind that exact hash. Contract,
consumer, helper and producer source hashes also match their receipts.
The public audit independently reconstructs all 25 endpoint counts and
all 25 definitely-in-window counts. The score sums are exactly

    (0,1] duration window: -10380,
    all positive durations: -16678.

There are 122,733 self returns, zero direct-jump markers, zero ambiguous
window timestamps, and zero observed nonneighbor endpoints. The latter
zeros are descriptive counts, not certified graph-support zeros. The
consumer scores all pairs, including a positive Horn score for nonneighbor
transitions if they had appeared, so it does not require exact support
inference from absence.

The tick sums are

    native holds: 128652859852,
    interior durations: 274530739041,
    scale: 1048576.

Therefore the raw interval contract alone places total elapsed time in

    [403183074605/1048576, 403183598893/1048576].

The later-read producer total 384505.59294931183 lies inside. Its separate
hold/interior totals and maximum interior duration lie in the corresponding
raw intervals. Original unrounded arrays were not retained; their exact
floating sums were not independently regenerated. The audit does not
claim more timing information than the retained intervals and receipt.

## 2. Timestamp and direct-atom handling

A positive excursion is warranted to lie between (u-1)/scale and u/scale,
with a separate zero-tick marker for direct port jumps. The window consumer
forms a pathwise UPPER score: use the Horn sign when definitely in (0,1],
zero when definitely outside, and max(sign,0) when the interval straddles
the endpoint. This is correct for either sign, including the lower-bound
equality at duration 1. A separately resolved positive-duration flag handles
the possible lower interval endpoint zero.

The all-duration score includes exactly u>0 and excludes direct atoms.
This is essential to the copositive kernel theorem. Positive intervals are
not silently treated as direct jumps, and direct atoms are not smuggled
into a hidden-excursion Gram matrix.

Truncated duration is upper-rounded as min(u/scale,24), which dominates
the true min(tau,24). The confidence proof may be applied to the ideal
bounded underlying score or duration and then use this pathwise domination.
It does not need an additional independence assumption for the rounding
errors themselves, provided every reported interval is valid.

## 3. Confidence and exact outward arithmetic

For an independent bounded score in [-1,1], the one-sided Hoeffding radius
is sqrt(2 log(1/delta)/N). For duration truncated into [0,24], it is
24 sqrt(log(1/delta)/(2N)). The original consumer assigns delta=1/2000
to each of score and mean. The reuse assigns 1/3000 to each of two fixed
Horn scores and their shared mean, then selects the stronger score after
forming simultaneous bounds. Correlation between scores or with the mean
does not invalidate the union bound. No score matrix was fitted to the
record; additional unreported adaptive score searches would need their
own selection accounting.

The independent audit reconstructs the logarithms using 96 rational
atanh-series terms, rather than the consumer's 60 terms. Both endpoints
of the independent log bracket round to the same upward 80-bit dyadic.
It verifies each reported square root by the exact inequalities defining
the smallest upward dyadic square-root grid point.

For exp(-12), the audit uses alternating Taylor partial sums of degrees
200 and 201, with signs certified by Taylor's remainder, rather than the
consumer's reciprocal positive Taylor series. Both interval endpoints
round to the same upward dyadic as the consumer. Thus the tail allowance,
radii, empirical quantities, sums and final ratios agree as exact fractions,
not merely as printed decimals. The printed floats are only display values.

## 4. Flux weighting, mean tail and physical-time conversion

The public contract supplies equal stationary native departure fluxes,
port weights proportional to one, and rates 32/15. Uniform reset-port
selection is consequently the required flux-weighted Palm selection.
The record itself does not establish that calibration. Independent exact
resets are also a supplied access premise.

The bounded endpoint/bin certificate gives E/R with no tail assumption.
For a time rate the consumer uses the separately supplied per-port tail

    P(tau>t)<=exp(-t/2).

Its residual first-moment allowance above 24 is correctly
integral_24^infinity exp(-t/2)dt=2 exp(-12). The initial native hold mean
is 15/32 from the calibrated rate. Thus the reuse obtains

    mean full cycle <=1.5612866014965647,

and divides its positive per-departure entropy lower bound by this cycle
upper bound. The renewal identity W/R includes the native port hold and
the entire interior excursion. No holding-time cost is omitted. The
original source's exact mean is not used by either consumer.

## 5. Source factory, read only after the public certificate PASS

The producer executes six arrays of individual random variates: reset
labels, neighboring-edge choices, initial holds, hidden-star choices,
interior holds and exit choices. It charges 1,572,864 scalar variates,
262,144 resets/trials and 524,288 native jumps. No aggregate draw replaces
the sampled paths. The jump count is deterministic for this supplied
two-jump-per-excursion source and agrees with its verified factory.

An independent exact generator reconstruction confirms the correspondence:
two mirror stars per C5 edge, each of weight 16/15, incoming fractions
(5/8,3/8), reversed exit fractions, rate-one hidden holds and rate-32/15
native port holds. Given a chosen incident edge, the producer's primary-star
probability is 5/8, and its self-return probability is 3/8. The other star
reverses these. This yields self-return probability 15/32 and each-neighbor
probability 17/64, exactly the independently constructed CTMC law.

The ideal interior duration is Exp(1), so the supplied exp(-t/2) tail is
valid and conservative. Source weights give W=47/3 and R=32/3. These
facts were checked only after the public certificate was frozen and were
used for comparison, never for its confidence inputs.

The source's exact all-even entropy rate is

    (16/47)log(5/3)=0.1738980846862947006657... .

Both acquired lower certificates lie below it. The same abstract generator
obeys generalized detailed balance if the two hidden stars on each edge
are swapped under an odd-state involution, with every port fixed. The
independent exact flow check verifies that parity qualification. Therefore
the positive physical entropy interpretation remains conditional on the
supplied all-even physical reversal; observations do not identify that
convention, and no odd-state native device is claimed.

## 6. Strong conventional comparison retained

For exact full endpoint population input, the hidden-star entropy
optimization of the established Skinner-Dunkel type attains the source
rate (16/47)log(5/3). The complete-endpoint linear copositive population
certificate gives 8/47=0.1702127659574468. The conventional optimum is
strictly stronger. The preserved agent proof reduces the C5-supported
hidden components to binary stars and applies the exact scalar minimum.

This population comparison does not become a finite-data optimum by
assuming unobserved transitions have zero probability. No such finite-data
support claim is made in the acquired certificate. Both approaches are
entitled to the same retained endpoint records. No computational or sample
speedup over the strongest equally informed method is established here.

## Audit artifacts

audit_native_record.py and NATIVE_RECORD_PUBLIC_AUDIT.json preserve the
public-only reconstruction. audit_native_source_after_certificate.py and
NATIVE_SOURCE_POSTCERTIFICATE_AUDIT.json preserve the later source/factory
and truth comparison, bound to the already frozen public audit hash.
All source redraw counts are zero, and the root records remain unchanged.

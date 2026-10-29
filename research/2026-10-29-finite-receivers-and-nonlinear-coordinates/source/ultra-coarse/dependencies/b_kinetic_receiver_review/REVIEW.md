# Independent intake: coarse intervention receiver

**ACCEPTED at its declared computational / ideal-law mathematical scope.**
Whole-read: C's governing PROOF.md §§1–7, PRIOR_AND_DECISION.md,
COARSE_CONTRACT.json, receive_coarse.py, coarse_only.py,
bounded_confidence.py, COARSE_RESULT.json, acquisition/replay/access
receipts, package/replay/run scripts, native histogram Gillespie logger,
native model compiler and catalog check. Also whole-read root's graph
PROOF.txt/acquire_envelope.py/ENVELOPE.json and the supplied controlling
Maurer–Pontil theorem and likelihood/sensitivity literature passages.

The positive claim that survives is **interval prediction of three fixed
finite-exposure adsorption interventions from a coarse baseline record,
without background rates or microscopic pair activity at the receiver**.
It is not point identification, a learned hidden generator, stationary
turnover prediction, a physical control/detector calibration, or an
advantage over the equally informed ordinary methods.

## 1. Change of measure and what partial observation permits

Let the full marked baseline process have two controlled intensities
lambda_1,lambda_2 and arbitrary unchanged background dynamics. On the
same initial law, multiplying the controlled intensities by a,b in(0,1]
and retaining their destination rules gives the ordinary path ratio

    W=a^N1 b^N2 exp((1-a)A1+(1-b)A2),  Aj=integral lambda_j dt.

I independently reconstructed the survival-factor sign and jump factors.
The native finite-state model has bounded intensities, so there is no
strict-local-martingale or explosion loophole in the unit-mean likelihood.
The general proof's bounded-controlled-intensity premise is essential;
arbitrary unqualified changes of initial law, destinations or background
mechanisms are not covered. Its observed variables need not be Markov.

If activity brackets are measurable from the coarse record, downward
controls make the exponential increasing in each activity. Therefore
W_minus <= W <= W_plus pathwise. For a SUPPLIED observed reward F in[0,1],

    E0(F W_minus) <= Eab(F) <= E0(F W_plus).

The unobserved exact pair activity never needs to be imputed. Equivalently,
the coarse-law likelihood is E0(W | coarse record), which lies between
the same measurable bounds. It is not generally equal to either bound.
No self-normalization by an empirically estimated weight is used.

The count-uncertainty extension has the right direction: for a<=1 larger
counts reduce a^N, so upper count bounds belong in the lower likelihood.
Reward brackets must also be actually acquired and nonnegative. Neither
this extension nor an algebraic rate formula supplies a physical detector.

## 2. Native activity / graph / reset scope

The source instance has32sites and36directional rules from the stated
pinned kmcos catalog. The actual computational controls scale ONLY the
CO and O2 adsorption families. Both single-site CO coefficients coincide;
all64undirected O2 pair edges have one common coefficient. Thus

    A_CO=k_CO sum v H_v,
    k_pair sum E_min(v)H_v <= A_O2 <= k_pair sum E_max(v)H_v.

The native indexing really gives an8-by4 degree4 torus. Independently,
E(S)-E(S_complement)=4|S|-64, E(S)<=2|S|, and bipartition subsets prove
E_min(v)=max(0,4v-64). I checked the max-table DP recurrence analytically:
all within-column edges and all cuts are counted once; fixed first mask,
last mask and vacancy total retain precisely the information needed for
future transitions and periodic closure. This proves all-v optimality.
The independent consumer checks all66native witness counts/scores and the
rate/degree relations. I did not rerun root's DP acquisition or dynamics.

These are sharp POINTWISE per-v extrema, not sharp constraints on every
temporally compatible vacancy path. The histogram is genuinely additional
coarse information, not obtainable from one preexisting integral of v.
The baseline replay paid for its acquisition and correctly counts ZERO
new independent episodes. Every original11field is preserved bitwise.

The generator-rank argument in C §1 also checks: fixing the O subset leaves
a pure-birth block of rank2^m-1, and summing blocks gives3^M-2^M. This
excludes the proposed one/few microscopic-source representation for this
native actuator. It does not establish hardness, rule out compressed
query-specific operations, or solve the original N744 stationary task.

All runs reset the COMPUTATIONAL configuration to a clean surface and
use T=1.1196731372603374e-5s. Same initial law and repeated preparation are
load-bearing. A changed stationary initial distribution needs its own
likelihood factor, and no such acquisition is supplied here. The actual
rate-family intervention is not silently upgraded to a physical pressure
change; source constant/thermochemistry conventions and the tiny literal
pressure/desorption discrepancy remain explicitly qualified.

## 3. Confidence, intersections and all57statistics

The deterministic range is B=exp(T[(1-a)Lambda_CO+(1-b)Lambda_O2]). Counts
give factors at most1, and supplied activity envelopes are at most their
global rate bounds. Hence F times either weight is genuinely in[0,B],
regardless of the hidden background. The actual B values are about1.6231,
2.0455 and2.2255. No unseen variance or pair-activity oracle enters a bound.

For each bounded statistic, the unbiased sample variance is the one in
Maurer–Pontil Theorem4. Setting its one-sided delta=2exp(-t) gives the
stated radius sqrt(2s²t/n)+7Bt/[3(n-1)]. Applying it in both directions
costs4exp(-t). Hoeffding costs2exp(-t). For X/B in[0,1], the chord bound
on exp(sX/B) proves the two bounded-KL tails, costing2exp(-t); this does
not require Bernoulli observations. Intersecting these three confidence
intervals therefore costs at most8exp(-t), rather than treating the
smallest radius as an uncharged choice among estimators.

There are3baseline statistics and3targets*3outputs*(2degree-envelope
statistics +2DP-envelope statistics +1rich +1direct)=54additional ones.
Thus the57-stat comparison has ideal joint failure at most

    8*57*exp(-14)=0.00037917709591122695 <0.000380.

Dependence across functions of the same baseline records is harmless for
this union bound. Duplicate lower-envelope functions make it conservative.
The printed mean weight and ESS are diagnostics without extra claimed
coverage. The bound does not cover an unrestricted adaptive pressure search.
For each coarse output the code uses the lower confidence limit for the
lower-weight statistic, the upper limit for the upper-weight statistic,
and the target's known[0,1] range. Those intersections and signs are right.

CRITICAL QUALIFICATION: this is a theorem for exact records of IID ideal
reset Gillespie episodes. The actual seeded binary64 mt19937 execution is
not proved to generate that law or IID samples. The final source says so
explicitly; neither our replay nor the close held-out means changes it.
No formal random-bit/roundoff or physical-data confidence is inferred.

## 4. Material findings, corrected and actually consumed

The original receive_coarse.py unconditionally opened the rich AO2 and
held-out files. Although its coarse formulas did not use those values, it
could not run at its claimed access boundary. I raised this as a substantive
executable-contract issue. C fixed it by exposing coarse_only.py and a
data-free confidence helper, retaining the former program as a labeled
rich/direct audit wrapper.

I independently executed the new CLI in a temporary directory whose ONLY
five initial files were the two code files, coarse contract, coarse records
and graph envelope. No MODEL, rich activities or held-out records were
available there. All18coarse query suboutputs and all baseline outputs
agreed recursively with the wrapper. ISOLATED_ACCESS_REVIEW.json records
the execution. This is a meaningful access check, not an adversarial
filesystem sandbox theorem. The code itself contains no rich-file access.

Two other necessary qualifications were incorporated before acceptance:
CO2hit is an ADDITIONAL supplied reaction path flag, not generally derivable
from histogram/counts/terminal coverages; and the actual logger resets the
configuration while consuming one continuously seeded PRNG stream, rather
than warranting IID by resetting independent streams. Current PROOF §4 and
contract state both points explicitly. No dynamics or numeric fields changed.

## 5. Independent numerical receiver and useful scientific query

independent_receiver.py imports no producer code, reconstructs activities
from the declared coarse inputs, uses separate fsum-based mean/variance
and interval routines, and opens richer files only for its labeled audit.
All57statistics and endpoints agree to within2.78e-17 with the saved output.
The residence-time sum error in the actual binary64 records is at most
8.48e-21; these are numerical checks, not directed interval arithmetic.
The independent saved-record consumer cost1.095s; the additional isolated
CLI consumption cost0.289s. No paths, model fixtures or extra data were run.

On the SAME conditional joint event, the coarse receiver bounds baseline
oxygen coverage below by.15865131017. The three target upper bounds are
.15687990708,.14267227705,.14347997216. Thus oxygen coverage decreases
relative to baseline by at least.0017714,.0159790,.0151713, respectively.
Among the three target controls, (.8,.9) also has its oxygen lower bound
above both competing upper bounds, by at least8.86724e-5. This finite-set
surface-coverage statement needs no new statistics or independence premise.
The CO2-hit intervals overlap; neither a product-yield winner nor a physical
recommendation is certified. Agreement with direct numerical means is a
useful control, not independent validation of physical source rates.

## 6. What operation survives against ordinary methods

The source-sized positive operation is real: under explicit invariant
marked-intensity semantics, a coarse baseline plus known adsorption
geometry/calibration yields nonvacuous partial-observation finite-pulse
counterfactual intervals without learning the hidden background generator.
It explicitly retains the vacancy-pair ambiguity instead of fitting a
false scalar Markov closure. This is a constructive acquisition/interface
result at its declared model scope, not merely a file/hash certificate.

The underlying likelihood and bounded-statistic methods are ordinary.
An equally informed partial-likelihood/graph method reproduces this
receiver. With the complete public model, ordinary direct KMC is stronger:
the three target batches cost about0.75845s sampling/writing, less than
this complete source/compiler/baseline/replay/DP/receiver cycle. No practical
computation advantage or exclusive new discovery capability survives.

Costs retain the1000preview episodes,80000main episode positions, same-seed
20k replay,964975main events plus270908replayed events, both compilations,
graph acquisition/verification and receiver processing. Neither the replay
nor different functions of one baseline increase n beyond20000. Physical
exposure sums are not lab wall time: detector bandwidth,81000clean-surface
preparations, transients, control invariance, graph/rate calibration, reward
readout and model discrepancy are not acquired. For fixed exposure the
conservative B grows exponentially in surface activity; the short-pulse
choice does not solve long-time/bulk catalysis or establish a universal
information barrier for other methods.

No substantive mathematical or executable-access objection remains at
the stated scope. Novelty, physical applicability and civilisation-level
leverage are separate, unacquired claims; they are not conditions being
added to withhold this substantive internal acceptance.

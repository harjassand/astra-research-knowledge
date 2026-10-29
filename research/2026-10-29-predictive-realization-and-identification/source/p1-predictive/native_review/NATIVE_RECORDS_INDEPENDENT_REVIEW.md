# Independent review of acquired boundary mean certificates

29 October 2026, Brisbane. Reviewer: `different_foundational_opening`, reassigned
to the native-record challenge after completing the distinct opportunity test.

**Verdict: PASS at the stated conditional mathematical and synthetic scope.**
The mean identity, native excursion reconstruction, finite confidence event,
positive-form propagation and both frozen consumers are sound. The six-port
consumer correctly handles whole absorbing regions under the supplied
separator contract. No redraw, producer import, consumer import, private
parameter-based narrowing or new source call was used in this review.

This is an ordinary mathematical and literal-record review. It is not a
formal proof-assistant certificate, physical acquisition, full distributional
floating-point simulation audit, novelty determination or resource advantage.

## Reviewed inputs and version scope

I read `CONSEQUENCE_COMPLETE_BOUNDARIES.md` in full at SHA256
`6a1c86f3743fb2bfb41ddb63d6715ada6dc17e2d01132e8078eb384e0e200937`.
The review below covers its explicit mean, derivative, acquisition and
interval formulas. The separate passive-equivalence minimality theorem and
its hazard/attachment distinction are the other reviewer's scope; I do not
promote their acceptance by co-location.

The frozen four-port record/certificate/raw hashes are respectively
`9b4a4c8c8fa00b3d9494ffa51be4ac30f8c48d00ff18cdbd9b8929973e4c3d3c`,
`96b23d2b010d280332a737289b0420e7bf9af93d4263b6ac30a54a306423b9bf`,
`89e32b56b02e73c82b11ca48dc64d089c1feb49295693d42a8dbbd8d0fac9490`.

The frozen six-port record/certificate/raw hashes are respectively
`57d66dc6e6db1de046ce175c04db3ad6304a7999dbae1d569ac77dbd3f8f6df3`,
`9cb74b25688f20031158bbffec1d679e5acfd98c2605fd8d2a34ff1d818c05d8`,
`838157871d261d593c31b4ee7c4a251f16f81691667700a64311c0905d43e63f`.

The final generalized consumer hash is
`5842a87505c29c92db94a779446dc1676dddb5cfc4d50b686acd9d08686c73d8`.
The original four-port certificate was produced before this generic extension
and remains byte-unchanged. Earlier tree-only source/certificate remain in
`first_consumer/`; no older result was overwritten by a different guarantee.
Machine-readable receipts include sizes and UTC modification timestamps.
Those timestamps establish artifact ordering, not human blinding or source
independence. The consumer's literal code only reads the public record.

## 1. Exact mean and memory contractions

For reversible weights w, L=-diag(w)Q, hidden interior I and retained ports
B, block elimination of the killed equation L_CC h=w_C gives exactly

    T_A = [c+b_R^T S_RR^(-1)b_R]/[sum(b)-sum_{a in A}w_a],
    S=L_BB-L_BI L_II^(-1)L_IB,
    b=w_B-L_BI L_II^(-1)w_I,
    c=w_I^T L_II^(-1)w_I.

Here A is a nonempty retained target, R=B\A, and the denominator is positive.
The quadratic term vanishes when R is empty. The interior inverse exists
because every interior component reaches B. All terms scale consistently
with an arbitrary common scale for w. The numerator's c is essential; it is
not obtained by replacing a singleton target vector with a coarse indicator.

The row-sum identities L_IB 1_B=-L_II 1_I and their transpose also verify

    K(0)=S,       K'(0)1=b,       -1^T K''(0)1/2=c.

Only contractions of derivatives are needed, not the full dynamic transfer
kernel. This is a task-specific consequence of standard reversible block
elimination. The review does not claim Schur complementation is new.

## 2. Native excursion reconstruction

Let s_i be the stationary distribution of the port return-event chain,
lambda_i the calibrated departure rate and sigma the time after departure
until the next port. Direct port jumps have sigma=0; self-return excursions
are retained. Reversibility implies s_i is proportional to w_i lambda_i,
so the public reconstruction

    w_i=s_i/lambda_i,
    S=diag(s)(I-P),
    b_i=s_i(1/lambda_i+E_i sigma),
    c=(1/2)sum_i s_i E_i sigma^2

has one common arbitrary scale.

I independently checked the last identity using the interior Poisson
equations. With t=L_II^(-1)w_I, the interior second-hitting-time vector is
2 L_II^(-1)D_I t. Summing its incoming boundary flux and using detailed
balance gives 2 w_I^T t. This is the equilibrium residual-life contribution;
an arrival-conditioned mean excursion alone does not replace it.

Initial port holding time is deliberately excluded from sigma and restored
through 1/lambda_i in b and w_B. Including that holding time a second time in
the moment v would be wrong. The executed records follow this convention.
This predicts a specified equilibrium-conditioned mean; it does not prepare
that physical initial ensemble or assert the same mean from an arbitrary
initial state.

## 3. Finite confidence event

The supplied tail Pr(sigma>t)<=exp(-t/2) gives E sigma^2<=8 and
E sigma^4<=384. With H=24 and x=12, the consumer bounds endpoint indicators
by Hoeffding and the truncated first/squared moments by two-sided Bernstein.
The radii sqrt(2 v x/n)+2 H x/(3n) and its H^2 analogue are conservative.
The recorded timestamp allowance a is added as a for the first moment and
2Ha+a^2 for the second; source precision is not supplied by the trial count.

The exact Taylor check e^3>20 proves e^-12<1/160000. Missing endpoint mass is
at most this amount. Missing first moment is at most 2/160000 and missing
second moment at most 104/160000. These are the differences between sigma
and min(sigma,H), not a bound on E[sigma 1_{sigma>H}], which would require an
additional H term.

There are m endpoint probabilities plus two moments per port. Therefore the
joint failure bound is

    2 m(m+2)e^-12 < 2m(m+2)/160000.

For m=4 this is 3/10000, and for m=6 it is 3/5000. No extra union bound over
the later target subsets is required. The confidence event covers primitive
information from which all releases follow. This is a frequentist false-
certificate bound under the supplied sampling contract, not a posterior
probability conditional on a successful release.

The row-simplex tightening is valid. I reconstructed exact feasible endpoint
minima/maxima from the original rectangular confidence box plus sum P=1 and
checked every released probability interval against them.

## 4. Reversible weight recovery and Loewner propagation

The four-port tree bounds are sound monotone Markov-chain-tree polynomials.
For an independent implementation, I enumerated undirected spanning trees
and oriented each toward its root, instead of copying the producer's parent
assignment enumeration.

Detailed balance bounds s_j/s_i by P_ij^upper/P_ji^lower on each usable edge.
I independently enumerated all simple paths, taking the smallest product,
and recovered every stored multiplicative shortest-path bound exactly.
Normalizing those ratios gives sound component intervals for s. A populated
path can determine the relative weight even when a rare direct edge has a
zero lower bound. The six-port consumer correctly uses this method without
an unnecessary spanning-tree enumeration.

Intersecting both directed estimates gives positive undirected conductance
intervals. Summing their edge forms implies S_lo<=S<=S_hi. Grounding and
inverse order reverse these inequalities. Every grounded inverse is an
entrywise nonnegative M-matrix inverse, so increasing nonnegative b can only
increase its quadratic form. The positive c bounds and positive denominator
bounds then give exactly the released endpoints. My independent rational
LDL^T solves reproduced all endpoints, including the all-port target whose
remaining boundary problem is empty. No floating eigenvalue was used to
certify definiteness or coverage.

## 5. Whole absorbing regions: the new load-bearing extension

The six-port interface supplies modules [[0,1],[2,3],[4,5]] and the separator
contract that every cross-module edge has both endpoints retained. Hidden
excursions remain in their departure module. This contract is **not learned**
from the observed absence of cross-module hidden excursions.

When entire modules are absorbing, remove both their ports and interiors.
Let R be the surviving ports. The surviving interior blocks are unchanged,
and the grounded S_RR includes boundary conductance into the absorber. The
correct formulas become

    c_live=(1/2)sum_{i in R}s_i v_i,
    W_live=sum_{i in R}b_i,
    T_regions=[c_live+b_R^T S_RR^(-1)b_R]/W_live.

The consumer implements these formulas. Retaining the absorbed modules'
residence term or their stationary population would be incorrect. Dropping
the separator premise would also invalidate this local removal rule.

I checked the true source's block separation exactly and solved the full
eighteen-state killed equations independently for all six proper nonempty
unions of modules. Each mean equals the boundary formula exactly and lies
inside its released interval. This is a real extension from point targets
to specified whole regions, not an unqualified theorem about arbitrary
macroscopic labels or unknown interfaces.

## 6. Literal execution and post-freeze truth controls

The review reads and verifies every stored endpoint/timestamp array, dtype,
range, censor mark, individual-row SHA256, endpoint count, integer tick sum
and squared-tick sum. It does not regenerate or replace any record. Public
confidence and endpoint reconstruction occurs before the private truth
comparison in the review program.

The private twelve-/eighteen-state generators are independently assembled
from the inspected rational specification; no private-source function is
imported. Exact full killed solves check every port target and every declared
whole-region target. Exact P,u,v,stationary weights and conductances also lie
inside their public intervals. This finite truth comparison is supporting
evidence; simultaneous coverage is established by the confidence proof.

| Frozen record | Trials verified | Port sets checked | Whole-region sets checked | Safe upper/lower factor |
| --- | ---: | ---: | ---: | ---: |
| Four ports | 4,194,304 | 15 | 0 | <1.384681 |
| Six ports | 6,291,456 | 63 | 6 | <1.702809 for ports; <1.700920 for regions |

The earlier tree-only four-port consumer's factor was approximately
2.517734644816658. The path consumer's approximately 1.3846809801407594 uses
the same frozen counts and supplied reversibility; this is an ordinary
same-information improvement, not a new acquisition advantage.

The records charge respectively 8,369,305 and 12,559,287 native jumps, and
about 8,099,867.6447 and 12,173,956.9842 elapsed native clock units. Reset,
initial-departure and terminal/pending-report counts are each one per trial.
I verified cost aggregation and the consistency of logged elapsed time with
initial-hold totals and raw rounded excursion durations. Hidden jump totals
are backend instrumentation preserved in the record; they cannot be
independently reconstructed from coarse endpoint/timestamp data alone.
The operation/preparation cost of implementing exact physical port resets
has not been demonstrated or priced. Python wall time is not native time.

The source backend generates individual trajectories using PCG64 and float
exponential/categorical primitives, rather than aggregate count draws. The
proof assumes ideal independent native trials, exact calibrated clock and
tail promises, and the timestamp error allowance. This review does not prove
a complete distributional roundoff bound for the PRNG/float simulator; it
therefore preserves the existing ideal-source synthetic scope. No equipment
operation, physical calibration or real-source measurement occurred.

## 7. Accepted addition and remaining limits

The accepted positive statement is that this acquired record suffices for a
declared family of equilibrium mean consequences, including the whole-region
extension under resolved separator access. An equally informed conventional
milestoning, positive killed-system or Schur solver can adopt the same record
and certificate. No exclusive algorithmic speedup, globally optimal sample
cost or practical superiority follows from the large number of target sets.

The port mass w_B remains required for target-subset denominators and for
fixed-native-hazard attachments. A conductance-calibrated attachment R and a
native hazard kappa with R=diag(w_B kappa) are different input interfaces.
Unknown relative scale between separately acquired modules must be calibrated
before composition. This review does not erase either requirement.

The independent code is `review_native_records.py`; its complete result is
`NATIVE_RECORDS_INDEPENDENT_REVIEW.json`. Runtime was about 3.07 wall seconds.
All frozen input hashes were rechecked after truth controls and remained
unchanged. A changed producer/certificate source requires a scoped delta
review; this receipt does not automatically apply to altered releases.

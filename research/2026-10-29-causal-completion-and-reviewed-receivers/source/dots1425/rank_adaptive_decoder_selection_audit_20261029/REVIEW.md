# Independent review: rank-adaptive fresh-block decoder selection

2026-10-29. Reviewer `producer-workspace/review_history_program_bounds`.

**ACCEPT model-free soundness, and promised completeness/expected query cost with the frozen least-integer schedule clarification.** Candidate completeness depends on the corrected compressed mixed-encoder recovery receipt. This is validation of a fresh whole-block averaged channel, not reuse of a gauge-dependent calibration program or proof of the source's rank/correctability.

## Whole-block interface

For fixed stationary memoryless N, each fully specified candidate j defines a CPTP logical channel M_j, including all of its training calls, random choices, measurements and fallback/abort completions. A sacrificial logical Bell input with its trusted retained reference has a binary failure probability exactly `ell_j=1-F_e(M_j)`. Fresh source uses, controller states, random choices and training programs make the complete validation runs independent. The real service payload is not used in selection.

After j is selected, **the entire service training block is restarted**. Conditional on the validation transcript and the selected j, the service channel is therefore still M_j. This is the mechanism that makes confidence transfer valid despite the joint-compression construction's newly randomized frame. The accepted classical index specifies an algorithm and budget; it is not a recovered frame or a reusable Petz matrix.

Resetting only some state would not suffice. For example, a candidate that chooses identity with probability.8 and Z with probability.2 has fresh-service entanglement infidelity.2. Reusing one favorable hidden realization for all validation tests makes every test pass with probability.8, irrespective of sample size. This is outside the theorem's fresh-whole-block premise and explains why that premise is essential.

## Soundness and the rare-failure sample count

Set `alpha=epsilon²/k²`, `delta_j=delta 2^(-j-1)`, and use `m_j=ceil(32 b_j/alpha)`. For a bad candidate with `ell_j>alpha`, acceptance at empirical loss at most `3alpha/4` is contained in a lower deviation by at least1/4 from its mean. The multiplicative Bernoulli bound is at most `exp(-m_j ell_j/32)<=exp(-m_j alpha/32)`. Since `m_j alpha/32>=b_j` and `exp(1)>2`, this is at most `2^-b_j<=delta_j`.

The same bound holds conditional on reaching j because all its tests are fresh. Summing over the countable stages gives probability at most delta of ever selecting a candidate with true averaged infidelity above alpha. On the complementary event, the normalized-Choi/pure-target inequality gives

`halfdiamond(M_j,id)<=k sqrt(ell_j)<=epsilon`.

This applies to arbitrary service payload/reference states, provided service is fresh and uses the same stationary source/candidate. It does not assert that every internal service realization is close to identity. Nor is it a pass certificate of rank or exact correctability: a mildly noisy nonreversible channel can pass if its actual averaged logical error is small enough. An unpromised channel can cause indefinite search. No uniform worst-case stopping bound is claimed.

Preparation of the logical test Bell pair and its Bell readout must be trusted at the asserted accuracy. Candidate implementation error is already inside M_j; unbudgeted validation-readout bias is not. If that external test has error, thresholds/sample counts need an explicit amended analysis rather than inheriting these constants automatically.

## Completeness

For a correctable mixed encoding of junk rank r, put `j*=ceil(log2 r)`. The received candidate theorem can be run at sufficiently small target error to give `ell_j<=alpha/4` for every j>=j*. Known padding handles `kR_j>D`; it is not additional source access. The candidate remains a finite CPTP processor off-promise, because joint compression has a CPTP completion and tomography has a physical fallback.

For a good candidate, the Bernoulli moment generating function at parameter ln3 gives

`Pr[reject]<=exp[m_j alpha(1/2-(3/4)ln3)]<=exp(-m_j alpha/4)<=delta_j^8`.

The integer rejection threshold causes no problem: bounding the event above the real threshold is conservative. Therefore probability of not having stopped by j* is at most `delta_(j*)^8`. Infinite continuation has probability zero under the promise. Combining availability and soundness yields stopping by j* with a certified-good selected channel except on probability at most `delta+delta_(j*)^8`; an earlier bad acceptance helps availability but not quality.

## Required schedule clarification and expected calls

Soundness permits any larger b_j, but the claimed polynomial expected-cost conclusion does not follow for arbitrarily oversized stage sample counts. The frozen clarification correctly chooses the least integer, giving `b_j=b_0+j`, with `b_0=ceil(log2(2/delta))`. This is also the choice actually implemented by the author's code. Without a growth restriction on b_j, a later astronomically oversized validation stage can overwhelm prior rejection tails.

For s stages beyond j*, the reach bound is exactly

`product_(l=0)^(s-1) delta_(j*+l)^8 = [delta 2^(-j*-1)]^(8s) 2^[-4s(s-1)] <=2^[-4s²-4s]`.

If `q_j<=C 2^(pj) P(j,1/epsilon)`, then after factoring out polynomial dependence on r,1/epsilon and log(1/delta), the expected tail is bounded by a series of the form

`sum_(s>=0) (s+1)^w 2^[-4s²+(p-4)s]`.

This converges with a constant depending only on fixed p,w: successive term ratios are at most `2^(p-8s-8+w)`, so eventually at most1/2. The finite pre-j* sum is also polynomial in r and1/epsilon, with logarithmic-confidence factors, because `2^j*<2r` for r>1. This proves finite polynomial **expected source-query cost**. One fresh service block adds a cost no larger than the same style of bound. The root candidate's h^6 query dependence allows a fixed rank exponent6 with polynomial stage factors; candidate accuracy can be set conservatively to half-diamond at most alpha/4 to obtain the needed fidelity completeness.

The explicit high-probability validation budget through j* remains `sum_(j=0)^j* m_j(q_j+1)` and the controller need not know r. Every sacrifice and service payload encoding call is counted, and service pays new training calls. The fixed-rank Schur/GT gate bound is not uniform polynomial in rank. This receipt does **not** establish polynomial expected gate/runtime cost, or even a finite expected runtime for an arbitrarily fast-growing candidate compiler family. Each stage is finite; source-query expectation and physical runtime are separate statements.

## Reproduction and scope

`independent_checks.py` uses direct binomial-coefficient sums, rather than the author's recurrence, for12 additional rational sample/threshold fixtures. It also proves/checks12 explicit infinite-tail majorants, closed-form reach products, and the whole-block-reset counterexample. A useful exact controller simplification is `floor(3alpha m_j/4)=24 b_j` for `0<alpha<1` and the specified m_j. The author's18 binomial and9 cost-tail fixtures replay exactly.

Accepted: stationary memoryless CPTP-source soundness; complete fresh-block validation/service; trusted Bell tests; the least-integer schedule; and mixed-encoding promised completeness with expected query cost. Excluded: source drift/memory, reuse of validation realizations, rank identification, perfect-correctability certification, guaranteed stopping for arbitrary channels, gate-runtime upgrades, practical performance, outer coding or rate claims. The separate joint-payload batch theorem has its own receipt and is not silently incorporated here.

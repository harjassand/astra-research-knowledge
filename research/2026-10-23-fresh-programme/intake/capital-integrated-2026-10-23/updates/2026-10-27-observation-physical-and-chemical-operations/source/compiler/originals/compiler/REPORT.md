# Completed charged observation-replacement construction

An accepted all-reference conditional-entropy comparison is not an exact
simulator. This continuation constructs the stronger, explicit operation that
is available when an **already classical** raw symbol can be disclosed at a
charged cost: a rational channel pair is compiled into a locally exact causal
replacement module, an optimal one-step read-rate certificate, and a sharp
minimax read-count tail at the declared local-module scope. A hard-budget
truncation then has a certified upper trace-distance error. The general proof
is in [PROOF.md](PROOF.md), not inferred from finite tests.

The current work does **not** establish a new advantage over the strongest
ordinary generalized subchannel-packing/Blackwell/Doeblin method. The acquisition
is ordinary rational LP, implemented with ordinary exact simplex; the stochastic
count argument uses standard coupling and LP duality. Historical priority of
this particular integrated interface and exact local-module tail statement
remains UNKNOWN. No civilisation-scale, physical or global simulation advance
is claimed. The delivered scientific result is the complete scoped operation
and an exactly certified entropy/simulation separation.

## Shortest consequential chain

1. Supply exact classical K,L and a real, charged raw-X disclosure service.
   The L record and internal cost flags are private to the simulator. No new
   quantum measurement, hidden label oracle, or physical data acquisition is
   supplied by the theorem.
2. Solve the packing LP U>=0, column sums<=1, UL<=K, minimizing
   max_x[1-sum_z L_zx sum_y U_yz]. Its rational primal/dual certificate gives q*.
3. On observing z, output y without a read with probability U_yz; otherwise
   disclose X and sample from the normalized residual K-UL. This exactly
   reproduces K for each classical input, so it composes inside arbitrary
   admissible feedback and with every finite quantum side reference.
4. For T rounds, Pr[N_T>B]<=Pr[Bin(T,q*)>B]. A dual least-favorable fresh input
   proves equality in the minimax count-tail problem among modules required
   to be exact at every full private pre-round history for every possible x.
5. Stop before read B+1 to obtain an approximation within that tail in total
   variation / half trace norm. This final bound is not claimed to optimize
   hard-budget error, nor to give an unbiased conditional-success record.

This removes an actual interface gap between one-step entropy control and
feedback-safe channel replacement. It does so by charging the extra raw
classical access, rather than deriving that access from an entropy inequality.
In an application with costly raw disclosure, it gives an explicit implementable
access budget. No actual application's source/calibration or economics was
acquired here, so practical value beyond this operation is not measured.

## Two exact inputs, with different conclusions

The root supplied the released H03 input. Direct exact inversion found

    K L^{-1} = 1/5080621 *
      [[1209652,2166756,1908573],
       [2346980, 807654,3054426],
       [1523989,2106211, 117622]].

Every entry is positive and each column sums to one. H03 is already stochastically
degraded, so q*=0 and its exact adaptive replacement is ordinary postprocessing.
It is not evidence for paid-query benefit or a new algorithmic advantage.
[H03_COMPILED.json](H03_COMPILED.json) is the checked acquisition output; the
read-only original source path is retained in the earlier H03 certificate.

To exercise the missing interface, a separate rational family was constructed.
At epsilon=1/20, set

    L = [[2/3,1/6,1/6], [1/6,2/3,1/6], [1/6,1/6,2/3]],
    K = [[2/15,49/120,49/120],
         [13/30,71/240,71/240],
         [13/30,71/240,71/240]].

K is positive but singular, which the accepted N1038 theorem permits; L has
determinant 1/4. Its unique signed postprocessor is

    K L^{-1} = [[-1/20,1/2,1/2],
                [21/40,1/4,1/4],
                [21/40,1/4,1/4]].

The negative entry proves that no zero-query stochastic replacement exists.
Nevertheless the accepted N1038 three-LMI criterion certifies the complete
conditional-Umegaki bound C_cond(K,L)<=3/4, using center z=(1/3,1/3). The exact
2-by-2 center blocks have diagonal/determinant triples

    (17/1800,1187/7200,221/144000),
    (31/225,4187/28800,2201/144000),
    (31/225,4187/28800,2201/144000).

All are strictly positive. This is a sufficient subunit upper bound, not an
acquired exact optimum for C_cond. Full matrices and the signed postprocessor
are in [ENTROPY_SEPARATION_CERTIFICATE.json](ENTROPY_SEPARATION_CERTIFICATE.json).
Thus even all-finite-reference subunit entropy order has strictly positive
exact observation-replacement cost at this interface.

Root independently supplied a direct bounded decision witness, rechecked here
with exact fractions. With uniform prior, acting earns (-6,1,1) across the
three raw inputs and declining earns zero. Under L every record has negative
joint expected act payoff: (-11/9,-1/18,-1/18), so the optimal payoff is zero.
Under K, acting only at its first output earns 1/180>0; its other outputs have
negative act payoff. Thus the subunit entropy order also fails to preserve
this explicit decision task. Rescaling all rewards by 1/6 puts them in [-1,1]
without changing the strict comparison. See DECISION_WITNESS.json. The witness
is an operational illustration of the established entropy/Blackwell
distinction, not a historical novelty claim or a quantum-reference advantage.

The new packing LP has the exact solution

    q*=3/40,
    U=[[0,2/5,2/5],
       [2/5,11/40,11/40],
       [21/40,1/4,1/4]],
    K-UL=[[0,3/40,3/40], [3/40,0,0], [0,0,0]].

Its column sums are 37/40, so the query probability is 3/40 for every z and
x. A queried raw x=0 outputs y=1, while x=1 or 2 outputs y=0. The exact dual
puts weight 5/2 on output constraint (y,x)=(0,0), weight 1/2 on each of
(1,1),(1,2),(2,1),(2,2), and pi=(0,1/2,1/2) on input query constraints. Its
objective is exactly 3/40. [NONDEGRADED_COMPILED.json](NONDEGRADED_COMPILED.json)
contains the full independently checkable result. The initial proposal
NONDEGRADED_CERTIFICATE.json uses the other equally optimal output-row
permutation (the last two K rows coincide); it is retained as exploratory
provenance, not confused with the final compiled runtime table.

This is not a one-fixture conjecture: for 0<epsilon<1/4, replace the signed
postprocessor's first column by (-epsilon,(1+epsilon)/2,(1+epsilon)/2) and
keep its other columns as displayed. Put K_epsilon=R_epsilon L. The same
primal/dual pattern gives q*=3epsilon/2 exactly, with

    U_epsilon=[[0,1/2-2epsilon,1/2-2epsilon],
               [1/2-2epsilon,1/4+epsilon/2,1/4+epsilon/2],
               [(1+epsilon)/2,1/4,1/4]].

All channel entries are positive in this range. The entropy upper bound 3/4
was certified only at epsilon=1/20 here; it is not silently transferred to the
whole family. The family is a mechanism illustration, not a claimed novel
channel family or benchmark win.

For the displayed epsilon=1/20 module, the raw-read count is exactly Bin(T,3/40)
even for adaptive inputs because its internal query probability is constant.
At T=1000, expected raw disclosures are 75, and B=117 is the smallest budget
certified to have binomial tail at most 10^-6; the exact tail is approximately
9.801491040876202e-7. The exact rational tail, rather than that floating display,
is stored in [CHECKS.json](CHECKS.json). Output, cheap records, flags, raw-symbol
bit sizes and calibration costs are additional to those read counts. The exact sampling claim is relative to an independent fair-bit
service; an arbitrarily seeded finite-state PRNG does not establish that
service for an unbounded execution.

## Exact executable and verification

- [compiler.py](compiler.py) builds the rational certificate from arbitrary
  finite rational stochastic matrices with a common input alphabet.
- [exact_simplex.py](exact_simplex.py) is the standard-library Fraction simplex
  backend with a supplied feasible slack basis and Bland's anti-cycling rule.
  It has no polynomial pivot-runtime guarantee.
- [verify_certificate.py](verify_certificate.py) checks primal and dual without
  importing a solver or reusing its matrix construction.
- [runtime.py](runtime.py) implements exact rational sampling, a raw callback,
  budget-before-access abort, and exact binomial tails/quantile search.
- [verify_entropy_separation.py](verify_entropy_separation.py) evaluates the
  accepted N1038 certificate formula using exact rational matrix arithmetic.
- [check_construction.py](check_construction.py) checks the exact one-step law,
  the entire four-round record law of a changing-input feedback policy, its
  count distribution, callback isolation, abort-before-raw-access, endpoint
  acquisition and rejection of corrupted primal/dual certificates.

The finite checks passed. They verify implementation interfaces; the general
adaptive/quantum-reference conclusions rest on PROOF.md. Root subsequently completed a substantive independent mathematical review of
the entire general PROOF.md and independently reconstructed the exact example,
N1038 criterion, primal/dual and decision witness without importing worker
code. No mathematical error was found at the stated local-module, private-flag,
already-classical-input scope. The reviewed proof version/hash and exclusions
are saved in INDEPENDENT_REVIEW_SCOPE.json. This is a completed internal review
at that actual scope; it is not a code audit, physical validation, historical
priority clearance, or an optimal hard-budget approximation theorem.

From this folder, for example:

    python3 compiler.py NONDEGRADED_INPUT.json output.json
    python3 verify_certificate.py output.json
    python3 verify_entropy_separation.py
    python3 check_construction.py

## Strong ordinary comparison and boundaries

At q*=0 this is exactly Blackwell stochastic postprocessing. With uninformative
L it reduces to the established Doeblin factorization

    q*=1-sum_y min_x K_yx.

A constant record permits the common no-query mass min_x K_yx at each output;
no protocol can assign more common mass. The side-record version is generalized
subchannel packing, an ordinary rational LP at exactly the same input/access
contract. An equally informed ordinary competitor gets K,L, the raw service,
all retained work and the same source promises; it can solve this identical
LP and use the same residual sampler and sequential coupling. No advantage
relative to that competitor is proved or measured. A comparison only against
no-side-information Doeblin or against forced blind query decisions would be
weaker and is not our success claim.

Known Doeblin/noisy-to-random-probing work already supplies optimal erasure
factorizations and adaptive uses. Relevant primary sources are:
[Makur and Singh, On Properties of Doeblin Coefficients](https://japneet644.github.io/files/DoeblinCoef.pdf),
[Beguinot et al., Formal Security Proofs via Doeblin Coefficients](https://eprint.iacr.org/2024/199),
and [Blackwell, Equivalent Comparisons of Experiments](https://doi.org/10.1214/aoms/1177729032).
The ePrint metadata/abstract and primary indexed excerpts were available; its
full PDF fetch was denied (403), and the author's indexed PDF URL returned 404.
No unread theorem there is asserted to prove the exact side-record/tail
statement. Conversely, absence of that exact statement in the inspected
material is not evidence of historical novelty. Quantum Doeblin generalizations
also exist; this construction's actual input and runtime remain classical.

Locally exact minimax count tails, globally exact hidden-state simulation,
known-source optimization, and hard-budget approximate error are distinct
optimization problems. For a known persistent X, paying once and caching it
may beat the stationary compiler. A source promise, previous raw acquisition,
controller access to Z/flags, retrospectively accessible records, physical
coherent input, or a quantum memory correlated with the L noise changes the
contract and must be charged/reproved. The theorem supplies no privacy
protection for its internal read flag. Exposing the flag can reveal more than
Y and can change feedback.

## Accepted prior, provenance and costs

The selected accepted prior is N1038 at knowledge commit
f9558b967f5014eced96f229cf89cc4aa7f3490b. Its
[pinned governing proof](https://raw.githubusercontent.com/harjassand/astra-research-knowledge/f9558b967f5014eced96f229cf89cc4aa7f3490b/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-method-redesign/source/channel/PROOF.md)
and the finite-reference argument and full governing review were read before
reuse. Downloaded bytes match their accepted packet SHA256 values; the manifest
is in sources/SOURCE_MANIFEST.json. The accepted theorem gives a small complete
certificate for positive rational 3x3 classical channels with denominator
injectivity, including singular numerator K and arbitrary finite complex
quantum references. Its existing free-SOS comparator and historical scope
limits remain intact. Here it is used solely to certify the displayed entropy
upper bound; the paid-access compiler is proved independently and applies to
other channel shapes without invoking that theorem.

The exact compiler and checker now require only existing Python 3.14.3 standard
library software. SymPy 1.14.0 is used only to evaluate the entropy certificate.
An initial numerical proposal used previously retained SciPy 1.18.1/NumPy 2.5.3,
with its prior setup retained; those dependencies are not needed by the final
acquisition/runtime. Exact matrix output and dual checks, not residual floats,
are the acceptance criteria.

The first symbolic exact-LP backend returned an infeasible endpoint candidate
for K=I_2,L=[1,1]; the independent verifier rejected it. It was replaced, not
counted as an exact negative or success. Initial scalar-decoding failures and
that failed backend are retained in FAILED_RUNS.md; exploratory proposal work
is not hidden. Research, source discovery and failed-work total time were not
instrumented and remain UNKNOWN. Exact certificate bit sizes, pivot counts,
selected construction times and fresh-process replay costs are reported
separately, without calling them a full discovery/acquisition advantage.

The final selected replay completed all six fresh processes: two acquisitions,
two independent certificate verifications, the entropy-certificate evaluation,
and the bounded implementation checks. FINAL_REPLAY.json records 0.376343957
seconds aggregate fresh-process wall time and 0.265801 seconds child CPU on
this machine with ordinary warm caches. These measurements include process
startup/import/input/checking/output for those processes only; they are not
full research or calibration costs, and no timing advantage is inferred. The
compiled exact LPs used 15 pivots for H03 and13 for the new pair, with maximum
tableau integer bit lengths34 and10 respectively. No uniform runtime claim
follows from these two inputs.

Reviewed general proof SHA256:
`33007e1215fd91118e35be36b07b50ea3096b936b3c33c8e519b058d50ad4eb9`.
Root's completed independent review is retained verbatim at
[sources/ROOT_SEQUENTIAL_REVIEW.md](sources/ROOT_SEQUENTIAL_REVIEW.md), with the
separate exact example review at
[sources/ROOT_EXAMPLE_REVIEW.md](sources/ROOT_EXAMPLE_REVIEW.md). Implementation
replay passed after reconciling the two equally optimal output-row choices;
FAILED_RUNS.md retains that stale test expectation and the rejected backend.

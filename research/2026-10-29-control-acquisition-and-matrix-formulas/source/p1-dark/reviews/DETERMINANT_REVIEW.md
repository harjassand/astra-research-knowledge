# Scoped determinant-tail and hypograph implementation review

28 October 2026. Internal mathematical/code review of the exact versions
below. This is not an independent whole-proof audit, a hardware test, or a
certification of unspecified source physics. No broad experiment suite was
rerun. A targeted historical counterexample and three small hull/root branch
checks were executed and saved reproducibly.

## Outcome and explicit correction

The positive determinant representation, one-sided truncation identity,
rational H_r bound, stated truncation sharpness, support cancellation and
log-Poisson coupling are sound under the displayed source and exact
face-equality premises. The finite-coefficient acquisition discussion
properly remains a proposed outer family, not an executed noisy learner.

One display-level defect was found in the original equation (14). With

    A=[q^k/k!]/[1-q/(k+1)],

the original chain `exp(-q)*A<=min(1,A)` is false in general. At q=9/2,
k=4, A=10935/64 and exp(-q)*A is approximately 1.8980762054. The existing
exact rational exponential enclosure proves this quantity is greater than
one without relying on a floating-point comparison.

The source display was corrected, with an explicit dated correction note, to

    T_k(q)<=min(1,exp(-q)*A)<=min(1,A).

The final rational bound and main determinant theorems remain unchanged.
The failed form and its exact counterexample are preserved in the review
receipt. No other mechanism change was made.

The actual `hypograph_control.py` has the correct hull orientation, root
endpoints, finite-command rounding and certificate directions. Its caller
was checked to ingest J=R-r0, so compliance utility is applied to J.

## Exact version scope: SHA-256

Paths are relative to `p1_dark_acquisition/`. Later edits are outside this
hash-specific code review unless separately checked.

| File/version | SHA-256 |
|---|---|
| selection/inference_determinant_tail_theorem.md, before review correction | `9893646398a7d644a2997d28f68ff0ef13b2fa23b467023bf2c2f614534c2084` |
| selection/inference_determinant_tail_theorem.md, corrected display and dated note | `07c78b79cf150dce546666654259f443c1b38e4337f5e40bf26397dc1206bf4d` |
| selection/inference_determinant_tail_checks.py | `b49a82bed4b98d74445bd248b96e4184ddf7f5800702a3f241172b31482628ee` |
| selection/inference_determinant_tail_results.json | `0a1ea2f1ce4aedafc5b06e48d88010d3659ffb94a6321e1149e668177879d488` |
| code/hypograph_control.py | `3416567cd6079ef387bed376b5ac46742782fe2a6b96bd2edc8d14c0652294e9` |
| code/simplex_law.py | `2ac69c52818d31b741f165bf6cb50fba5d990f14cd2ae6cedef5b4be1043505d` |
| code/run_lattice_experiments.py | `037ad3c7582d71ad258f8e87dc59749e8d86af2c97a16b2e6b9122a6f6c0dcdb` |
| results/LATTICE_RESULTS.json, saved status summary read | `2b045fbf9162bbbe03fe0cd357829094418eba7cd0ef9b68a2a13d92f73563a3` |
| reviews/determinant_review_checks.py | `5ebc6f80c3259f953e116aa82a6af63a6080de3adf52b68cffdc6c73e8545899` |
| reviews/DETERMINANT_REVIEW_CHECKS.json | `bb17fa698d850e4c2edcd62f095031bd122b5779444f5fe639404e2e74184f4a` |

The corrected theorem alone changed. Code and saved experiment hashes were
unchanged by the Eq. (14) correction.

## 1. Determinants, positivity and the one-sided identity

For fixed u>=0, K=sqrt(U)B sqrt(U)>=0 and x=sqrt(U)g. The determinant
lemma gives det(I+K+xx^T)=det(I+K)*(1+x^T(I+K)^-1x), which is N/D=F.
Transferring determinants between I+B U and I+sqrt(U)B sqrt(U) is valid.
All denominator principal minors are nonnegative. Numerator coefficients
are g_S^T adj(B_SS)g_S>=0, including singular B_SS by continuity. Hadamard
on diagonal cofactors and PSD Cauchy on the adjugate give the displayed
coefficient boxes. The kappa=0 and singleton cases are properly separated.

For eigenvalues lambda_i, coordinates z_i and total-degree truncation r,
write A_i=sum_(j=0)^(r-1)e_j(lambda without i), e_i=e_r(lambda without i).
Then

    D_r=(1+lambda_i)A_i+e_i,
    N_r=sum_i z_i^2 A_i,
    F=sum_i z_i^2/(1+lambda_i).

Consequently

    F-N_r/D_r=sum_i [z_i^2/(1+lambda_i)]e_i/D_r.

Every term is nonnegative. At r=0, A_i=0 and e_i=1 give F_0=0. At r>=n,
the excluded-list e_i vanishes, so truncation is exact. The same global
multiaffine coefficient truncation works at every u: no different model
is fitted on each ray. This establishes the asserted one-sided allowance.

## 2. Rational H_r bound and its precise sharpness

Counting products of nonnegative eigenvalues with sum <=q gives
(j+1)e_(j+1)<=q*e_j. If e_r,q>0, backward iteration yields
e_j>=e_r*r!/(j!*q^(r-j)). Since D_r>=sum_(j=0)^r e_j for each excluded
list, e_r/D_r<=H_r(q). Zero cases follow directly. The error identity's
weights sum to F<=L. H_r is increasing in q because its reciprocal is a
positive sum of nonpositive powers of q. For finite q and r>=1, H_r<1;
the relative enclosure follows by rearrangement. Its conditioning can
still be poor when H_r is near one.

The projector family is PSD with diagonal kappa=q/delta. At the uniform
command, x lies in K's zero eigenspace and its n-1 other eigenvalues equal
q/(n-1). Thus F=L and the exact error fraction is the last retained
binomial term divided by the retained binomial sum. At fixed r,q those
terms converge to q^j/j!, giving H_r(q). This proves dimension-uniform
sharpness for THIS determinant truncation and THESE L,q specifications.
It does not lower-bound alternative rational approximants, query policies,
or further restricted physical apparatuses.

H_r(q)<=T_r(q) is correct: for a,b,c denoting probabilities of Y<r, Y=r,
Y>r, respectively, (a+b)(b+c)-b=ac>=0. The q=0 and r=0 conventions agree.

## 3. Support cancellation and log-Poisson coupling

Two sources equal on every admissible support-<=k command have the same
c0. Cross multiplication gives A-C=N D'-N'D. On each face with support
S of size <=k, this polynomial vanishes on a relatively open positive
set. Hence every coefficient supported in S vanishes, so all coefficients
of support <=k agree. This requires complete exact face equality, not a
finite set of equal noisy readings.

A,C have nonnegative coefficients. Removing the matching low-support
terms leaves A_high,C_high>=0, giving |A-C|<=max(A_high,C_high). Support
greater than k entails total degree at least k+1, even though products
may have individual coordinate degree two. The total-degree tail therefore
upper-bounds the support tail.

After division by DD', N(tu)D'(tu) is a nonnegative mixture with weights
z_i^2/(1+lambda_i), summing to F, and one leading factor t. Remaining
factors are Bernoulli generating polynomials with p=lambda/(1+lambda),
excluding i from the first source. The coupling

    X=1{Y>=1}, Y~Poisson(log(1+lambda))

has exactly that success probability. Independent Y variables give the
required independent X variables and sum X<=sum Y pointwise. Their total
parameter is at most the trace; an additional independent Poisson variable
provides domination at any larger parameter. Combining two sources gives
q_u+q'_u. The leading t shifts the required tail to count >=k, as stated.

Domination at parameter sum p would be false. The saved Bernoulli(1/2)
guard correctly demonstrates that failure. These auxiliary variables are
algebraic tools, not a detector-noise or photon model.

The all-sparse-record bound is therefore sound at its ideal-information
scope. Equality at a finite lattice does not imply the exact face premise.
The sign-twin examples establish that stronger equality algebraically for
their particular saved matrices; they do not turn it into an acquired
property of arbitrary sources.

## 4. Scope of the supplied exact checks

The saved determinant results report 28 fresh native-source fixtures,
140 associated truncations, 40 larger diagonal aggregate checks,
45 projector sharpness aggregate checks, two small projector native-source
fixtures, and seven sparse sign-twin cases. The source and assertions were
read; the full suite was not rerun here. Large aggregate cases evaluate
their exact spectral formulas, not acquired observations or a dense
1000-state native experiment.

The exponential helper uses a positive Taylor lower sum and a geometric
majorant for the remaining positive series. Its degree selection makes
the ratio strictly below one. Inverting positive endpoints and computing
1-partial/exp(q) gives the Poisson interval with correct directions. Some
finite assertions compare against the LOWER tail endpoint, deliberately
stronger than using the upper endpoint. This is a valid finite pass test,
not a replacement for the general proof.

Small-source checks compare determinant ratios against source-native solves
and determinant/cofactor responses. Proper-support coefficient equality in
the twins proves their proper-face identity. The separate 12 ray-amplitude
checks remain a finite illustration; this review does not infer an
unrestricted adaptive-query lower bound from those 12 observations.

No finite-noisy coefficient learner or verified LP is executed by this
suite. The true truncated coefficient vector is contained in the proposed
linear constraints. Relaxed PSD/common-Gram conditions mean a feasible
polytope point need not itself be a physical source. Verified LP duals or
outward arithmetic remain required before numerical LP results are claimed
as certificates.

## 5. Actual hypograph implementation

`lower_cost_hull` keeps the least cost at each duplicate conductance, sorts
exact rational conductances, and retains increasing slopes using the
positive cross-product test. Popping nonpositive cross products removes
concave/collinear middle points from the LOWER cost chain. Original node
indices are retained for physical command mixtures.

`optimize_hull` includes every hull vertex. Its compliance branch tests
interior-root membership exactly, uses the LOWER sqrt(slope) endpoint in
the upper value -2*slo-intercept, and uses 1/shi for a candidate before
clamping to the segment. The latter is a feasible proposal, not an assertion
of exact optimality. For positive slope, shi>0 even if finite root precision
leaves slo=0. Linear conductance utility requires only endpoints and is
handled accordingly. A one-point hull is also covered.

`certify_task` raises lower node values only to a supplied warranted
positive baseline. Both outer control-point lists are raised to that
baseline if needed. It optimizes the two upper hulls separately and takes
the minimum of their global upper values, avoiding the invalid operation
of taking coordinatewise minima of upper coefficient lists.

Each proposal is a convex mixture of two feasible lattice nodes. The DAC
routine floors nonnegative rational coordinates to the selected dyadic
grid, preserving nonnegativity and the total-dose bound. The code subtracts
an outward Lipschitz allowance from the Jensen lower conductance, takes
the maximum with independently valid lower bounds, and recomputes prices
at the ACTUAL rounded command. Those are the correct directions for the
candidate objective lower bound. Global upper minus candidate lower is
therefore a full continuous-simplex regret certificate.

No source is passed into the optimizer. The saved caller subtracts r0=3/2
before ingesting node intervals and derives the positive baseline from
the acquired zero node and warranted c0>=1/2. It therefore handles the
raw-R versus J distinction correctly. Other callers must preserve that
semantic input contract; the object cannot infer it from its name.

The targeted review script executes an interior compliance-root case,
duplicate-conductance/negative-slope dominance, a collinear chain, and an
inward DAC command using Fraction assertions. These checks pass. They are
small branch checks, not a broad new suite or a local-optimizer convergence
argument.

## 6. Saved lattice status and remaining obligations

The read status summary reports five passing lattice cases with source
reaction counts 15, 84, 210, 455, 210, each plus two calibration standards,
and zero later source reactions. The driver checks exact raw/calibration
containment, held-out response intervals, candidate lower bounds and
held-out upper objectives. Its exact two-control conductance case also
checks regret against a known analytic optimum. General global coverage
rests on the envelope proof, not the held-out list. This review did not
reexecute the five-case suite or re-audit the entire native instrument.

Source class, G/kappa/c0 bounds, calibration, source stability, receiver
behavior, settings, settling, reset and apparatus realization remain
physical obligations. This review supports the displayed mathematical
claims and inspected code paths. It creates no universal photon/statistical
advantage, free coefficient acquisition, or independent whole-proof audit.

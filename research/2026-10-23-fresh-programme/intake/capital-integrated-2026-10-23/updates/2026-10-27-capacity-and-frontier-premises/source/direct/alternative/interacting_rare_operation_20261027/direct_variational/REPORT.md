# Direct deterministic capacity for the actual nonquadratic chain

The new operation succeeded at its supplied-model scope. Exact sparse
Galerkin bounds now compute the specified 24-site nonquadratic excursion
probabilities directly, replacing the earlier 5% and 50% transferred model
envelopes with relative numerical widths below 0.014%.

| Outside-occupation multiplier | Direct p_exc interval, units 10^-15 | Relative endpoint width |
|---|---:|---:|
| delta=0, reference | [5.1601047580, 5.1605692620] | 0.009002% |
| delta=1/20, actual | [5.4180434142, 5.4185520421] | 0.009388% |
| delta=1/2, actual | [7.7393498216, 7.7403854830] | 0.013382% |

The table is rounded outward. ACTUAL_M24_CASES.json stores exact rational
endpoints, capacities, every degree, input parameters and resource receipts.
The reference interval overlaps the frozen Gaussian certificate. Both actual
intervals lie wholly inside their earlier proved envelopes.

The question is the probability of reaching full wall occupation before
returning to vacuum, averaged under the true vacuum departure law. It is
not a single-start committor. The actual local generator multiplies each
pair-flip rate by 1+delta*eta_j, where eta_j is an unchanged outside
occupation indicator.
It preserves the exact nonuniform Gibbs law. For positive delta it is not
quadratic in the established occupation-fermion representation; this method
uses no Gaussian structure.

## What changed and why it closes

The prior operation computed a positive reference potential-kernel integral,
then used conductance comparison to cover a specified nonquadratic model.
That left model ranges about 5% and 50% wide. Here the full exact actual
local rate law, already supplied in that example, generates a low-degree
trial for the actual inverse operator. The trial need not be an accurate
committor oracle. Its FULL residual and an independently derived global gap
give a rigorous, a posteriori error bar.

Let H=-Q be the backward generator, w the unnormalized Gibbs weights,
rho=w(full)/w(vacuum), and u=rho*1_vacuum-1_full. For any trial y, ordinary
completion of the square gives

    I=<u,H^+u>_w/rho,
    L=[2<u,y>_w-<y,Hy>_w]/rho,
    L <= I <= L+<u-Hy,u-Hy>_w/(rho*g0).

The true excursion probability is rho/(R_a*I); normalized capacity is
rho/(Z_even*I). The analytic gap g0=2*min(reference creation rate) remains
valid for the actual one-sided same-Gibbs rate multipliers. No attractiveness
assumption is imposed on the actual dynamics.

Exact degree-3 Galerkin uses span{u,Hu,H^2u}. Adjacent pair flips are single
coordinate changes in the equivalent spin hypercube, so the full residual
is confined to two radius-3 balls. At this size it has 4,096 states, while
the full even-parity state space has 8,388,608. All reverse edge rates,
neighbors, support overlaps and the tiny vacuum source component are retained.

PROOF.md derives the capacity bridge, gap, variational bound, integer scaling,
support/bit costs and ordinary comparators. sparse_galerkin.py implements
the construction with exact integers and rational FLINT solves.

## Validation and measured cost

check_direct.py separately assembles complete small backward generators
from Gibbs weight ratios, without the candidate rate table. Independent
killed equations and full Poisson equations agree exactly. Nine 4/6-site
models at delta=0,1/20,1/2 pass 27 proposed degree intervals. Dense versus
sparse operator orientation, full residual/Gram equality, Galerkin
orthogonality, weighted mean zero and arbitrary constant trial shifts pass.

Root independently reconstructed EVERY full backward residual and weighted
norm at degrees 1,2,3 for all three 24-site models, using separate Fraction
rates/weights and direct Q*y. All nine raw bounds and final probability
intervals match exactly. The reconstruction costs about 0.535 seconds per
case. It takes the trial vectors/coefficient choices only as proposals and
does not trust the candidate operator, transitions, inner products or gap
implementation. Root's pinned receipt is
/Users/harjas/Documents/Codex/2026-10-23/astra-fresh-ultra-20261023/work/sol3_molecular_manufacture_20261026/parent/local_capacity_operation_20261027/SPARSE_LARGE_CHECK.json.

Each candidate certificate uses 554 cached source transition rows, 12,742
local edge evaluations, and 4,096 weighted states. Largest Gram integers
have at most 1,410 bits; coefficient denominators at most 1,698 bits. Core
wall time is 0.019-0.022 seconds per case, including source-table/LCM setup,
power generation, all moments, rational solve and final bounds. Python
startup/import and separate independent validation are outside that timer.
The complete three-case shell process took about 0.585 seconds. Process
peak RSS was about 32.1 MB, including shared imports; electrical energy was
not measured. Existing read-only python-flint 0.9.0 was reused; no new
installation, physical source, paid service or public action was used.

The three requested degree-3 accuracy targets all pass, so no degree-4
large run was needed. This does not claim degree 3 works uniformly. The
small tests honestly retain degree-3 widths from about 2.8% to 34.8% and
fail the requested 0.1% target. State balls may grow to exponential size
as the required degree grows; a small gap or extreme input conditioning
can make the certificate expensive or uninformative.

## Ordinary comparison and source limits

This is the ordinary Galerkin/CG construction proposed by root. An equally
informed ordinary solver receives the exact same rates, weights, gap,
trial construction and preprocessing; it can produce the same result.
There is no claimed superiority over it. The earlier 281-second Gaussian
reference run has different precision, implementation and output scope;
no speedup factor against it is claimed.

Under the same source/gap promises, a generic finite-horizon potential-kernel
Monte Carlo estimator also has sample/event cost polynomial in inverse
accuracy and inverse gap, with no inverse-global-rarity factor. PROOF.md
derives that comparator. A wasteful large Monte Carlo run was unnecessary.
The completed contribution here is a deterministic exact actual-model
certificate at the executed finite resource cost, not a new rarity
tractability class or a new CG algorithm.

All parameters are supplied exact rational source data. Direct calculation
does not acquire physical reversibility, locality, Markov memory or the
absence of hidden jumps. The prior conditional acquisition theorem and its
large exposure/mixing costs remain applicable. With uncertain Gibbs/rate
boxes, source uncertainty still widens the output; an acquired 5% rate
envelope does not become an exact actual law through computation.

The prior Gaussian/transfer unit's substantive parent review is COMPLETED at
its pinned scope, as recorded in parent/interacting_rare_review_20261027/
REVIEW.md. Its old frozen files still describe the earlier envelope-only
calculation. This new child records the direct continuation separately.
For the new scope, root's exact large residual review is completed; whole-
proof final acceptance is recorded only when explicitly returned by root.

The mathematical/computational operation is achieved for these models.
Physical source acquisition, historical novelty and practical advantage
remain unestablished. The civilisation-level mission remains
100/100 NOT_ACHIEVED.

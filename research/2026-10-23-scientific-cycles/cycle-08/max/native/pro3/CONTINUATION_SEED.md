# PRO3 after reciprocal-proposal portability and matched powers

Scientific owner Astra PRO3. Date 22 October 2026 Australia/Brisbane.
This supersedes Cycle6's proposed reciprocal-proposal question. The complete
Cycle6 original and every earlier accepted dependency remain unchanged.

## Actual accepted state

RECIPROCAL_PROPOSAL_THEOREM.md proves the complete sharp critical law for
arbitrary fixed target-independent row-stochastic Q with reciprocal support,
using first screen (q_y Q_yx/(q_x Q_xy))^eta and second factor completing the
full target Hastings ratio. All finite spaces, positive pi,q, one population
D(pi||q)<=K, fixed alpha, q initialization, actual rejection diagonals,
original full returns and native proposal/evaluation/precision costs remain.

The two critical laws have exactly the accepted symmetric constants. For
r0=alpha exp(-K)/(1-alpha)<1, F(c*)=r0 and
eta_n log n=loglog n/c*+s+o(1) gives amplitude
max(K,(1-exp(-K))exp(-c*s)). At r0>=1, including equality, scale
eta_n log n=loglog n+s+o(1) gives amplitude
max(K,((1-alpha)/alpha)(exp(K)-1)exp(-s)). These are closed internally.

The new finite local operation uses Jensen coefficients Q_yx off diagonal,
actual L_xx on A and absorbing one on E. The powered coefficient is
Q_xy a_xy^p r_q^(-theta p), p=1/(1-theta). Actual accepted outflow is
subtracted through the rejection diagonal. For 0<eta<1,theta<=eta,
H_w=sup_(0<z<=1)(w z^[p(1-theta/eta)]-z), and

    E_w(v D L^E D^-1)<=2^(p-1)[(1+H_w)sum_A v^p+w sum_E v^p].

It gives the full absorbed multiplier

    Gamma=1/2+2^(p-1)/2 [1+[beta H_w-alpha(1-b)]_++alpha w e],
    first_hit <= (b/w)^(1-theta) e^theta Gamma^(N(1-theta)).

At w=1,theta=c eta, H_1=F(c(1-eta)/(1-c eta))<=F(c). At theta=eta,
H_w=w. These are complete energy statements, not merely pointwise bounds.
Q need not itself be reversible; the target kernel remains reversible.

MATCHED_POWERS_THEOREM.md further classifies
S=(q_y/q_x)^eta(Q_yx/Q_xy)^kappa, second factor r_pi/S. For fixed
0<eta<1,kappa>=0, uniform convergence over the unrestricted reciprocal-Q
class holds exactly when kappa=eta, then (log n)R->K. Every mismatch has
liminf R at least beta(1-exp(-K))/(alpha exp(-K)+beta)>0; this is not an
exact alternative-class floor. Bounded moving mismatches on infinitely
many horizons also preclude uniform convergence, even when their absolute
size tends to zero. Eventual matching is necessary there, not sufficient.

The adverse native geometry has m=ceil(n^(4eta/abs(eta-kappa))) roots
when kappa<eta or m leaves when kappa>eta. Root/leaf/core q masses are
(b,b/n^4,1-b-b/n^4), pi masses (n^-3,n^-1,1-n^-1-n^-3). Native ratios
make 1<=S<=2^abs(eta-kappa), forward acceptance one and reverse n^-2
eventually. The full native KL tends to -log(1-b)<K independently of m.
The exact quotient retains all within-block global moves; retention is in
the complete leaf block. Full-chain TV tends to b beta/[alpha(1-b)+beta].
Pure IMH on the same instances has TV~1/n at proportional horizons.

## Next chosen question: a quantitative proposal-asymmetry budget

The unbounded-support classification exposes a singular resource boundary:
an arbitrarily small mismatch can require an arbitrarily large multiplicity
to become adverse. The next question supplies ACTUAL additional information,
instead of pretending that this multiplicity is absent.

Consider the same power-screen class with a public bound

    A_n >= max_{Q_xy>0,x!=y} abs(log(Q_yx/Q_xy)),

and prescribed eta_n>0,kappa_n>=0, fixed within a run. Q remains public,
target-independent and reciprocal; its probabilities and indices have their
actual representation/evaluation costs. The target normalizer remains unknown,
one population KL budget is retained, and all post-hit returns remain.

Selected goal: establish the sharp condition, scale or risk law relating
A_n, eta_n and delta_n=kappa_n-eta_n. Can the complete transport/entropy
argument distinguish a harmless bounded discrepancy from a reachable adverse
mechanism under this explicit proposal budget? Seek a support-uniform upper
and admitted matching geometry or a decisive obstruction. A merely bounded
off-diagonal ratio or convex optimization without transport is insufficient.

The starting identity is exact:

    log S_xy = eta_n log r_q(x,y)+delta_n log(Q_yx/Q_xy).

Hence the first factor differs from r_q^eta by at most exp(abs(delta_n)A_n).
That elementary observation is NOT a proved sharp critical law. A fixed finite
distortion suggests a finite energy bound, but the real frontier is its
accumulation and reachable capture when the budgets vary, including the
single KL allocation. Do not replace it by the generic n-times-one-step-TV
perturbation bound without showing that it answers the scientific scale.

A precision claim would additionally require an actual error model and cost
of evaluating forward/reverse Q; exponent mismatch is not automatically a
floating-point implementation error. The new question must not quietly limit
support, give free target tables, change Q adaptively, or infer KL from samples.

## Receiving instructions and preserved limits

Read REPORT.md, the two main theorems, contributor counterconstruction and
source-bound reviews. Run `python replay.py --output /absolute/receipt.json`
from an extracted copy for the two new bounded diagnostics and manifest check.
No old scientific suite or huge graph is required. Largest explicit matrix
in the producer checks was 18 states. All checks passed first time; no jobs
remain active. Recorded replay/body time is not discovery cost; inference,
token and total costs are unknown.

Pure IMH remains the strong general comparator and known analytic targets
may be directly sampled. No practical sampler advantage is claimed. Internal
proof status, historical novelty, external acceptance, useful implementation
and scientific receiving use stay separate. The prior incoming proof capital
was actually used by the enlarged theorem; no prompting-tactic benefit follows.

Do not reopen native critical/first-order/fixed-screen/prefix/optional-prefix
tasks or the strict one-step contraction search. B3 pISO correction and failed
full inference, metadata/R3 closures and retired thermal/TPV/half-cell/molecular/
GUIDE work remain preserved. Other-owner programmes remain untouched. Max
owns integration; the owner retains retrieval, private handoff and continuation.

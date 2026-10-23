# Astra PRO3 Cycle10 scientific checkpoint

23 October 2026, Australia/Brisbane.

## Strongest result

The critical transport problem now has a complete amplitude law whenever the
optimal crossing needs positive attenuation, including the joining point where
that attenuation first reaches zero. The globally dominated, one-crossing
branch is also closed. In the remaining regime, this checkpoint proves the
exact unrestricted limsup and an admitted native family with a periodic depth
penalty. The unrestricted liminf is still open.

The scientific distinction is whether a fractional final crossing can be paid
by a small change in acceptance. That adjustment costs o(1) at an interior
optimum. Once fully accepted crossings are strictly optimal, integer depth
leaves an order-one cost in the attaining family. An exact finite control
theorem shows that randomizing or retuning forward crossing choices inside
that representation cannot remove it. A more general native graph might.

The full arguments are in CRITICAL_TRANSPORT_THEOREM.md, with complete bounded
upper and native-construction notes in contributors/. The unchanged original
Cycle9 archive and exact finite-energy dependency are included. This is a new
endpoint construction and proof, not a replay of the closed logarithmic law.

## Contract and notation

Use the original finite positive pi,q class with one population
D(pi||q)<=K, fixed alpha in (0,1), beta=1-alpha, q initialization, and
target-independent reciprocal row-stochastic Q. At each horizon n the public
A_n,eta_n,kappa_n remain fixed within that run. The actual proposal asymmetry
is at most A_n. Local acceptance is the specified two-stage Hastings rule,
and C=(I+alpha G+beta L)/2 retains every rejection and return.

Fix d=|kappa_n-eta_n| A_n>0 exactly, and write

    ell=log n, L=log ell, u_n=eta_n ell,
    r=alpha exp(-K)/beta, b0=1-exp(-K),
    gamma=log(1+r), t=r/(1+r), d_star=gamma/t,
    c(d)=inf_{a>=0} log(1+r exp(a))/(d+a).

The critical policy is c(d)u_n=L+s+o(1), for fixed real s. No convergence of
A_n or fixed sign of mismatch is assumed. All results are exact-real; support,
target/proposal calls, reverse probabilities, labels, caching and precision
retain their costs. The normalizer is unavailable to the sampler.

## New theorem and exact remaining gap

| Regime | New conclusion for the unrestricted risk R_n |
| --- | --- |
| r>=exp(d), including equality | ell R_n -> max(K, b0 exp(d-s)/r) |
| r<exp(d), d<=d_star, including equality | ell R_n -> max(K, b0 exp(-s)) |
| d>d_star | limsup ell R_n = max(K, b0 exp(-s)); the liminf bound below holds |

For d>d_star, define the continuous phase penalty on the unit circle

    Psi(x)=min{(d t-gamma)x, gamma(1-x)},
    phi_n={u_n/d}.

An actual admitted native family has full-law amplitude

    ell TV(q_n C_n^n,pi_n)=b0 exp(-s-Psi(phi_n))+o(1).

Therefore

    liminf ell R_n >=
       max(K, b0 exp[-s-gamma(1-d_star/d)]).

If b0 exp(-s)<=K, the unrestricted limit is K even in this last regime.
Otherwise the phase profile is an attained lower and the uniform upper is
max(K,b0 exp(-s)). The gap is not closed. An oscillating witness family does
not establish an oscillating class supremum.

Every fixed phase is approached along a subsequence of integer horizons,
despite the allowed o(1) critical-policy perturbation. This is why the
all-class limsup is exact without claiming a matching upper at each phase.

## What actually changed in the proof

First, the accepted weighted first-hit operation is used at its endpoint with
its complete finite multiplier. The bound Gamma(e)^N=1+o(1) is established
from N=O(loglog n) and N eta_n=o(1); Gamma(e)->1 alone would be inadequate.

Second, a three-cell log-sum inequality couples the low-W source mass and the
high-W information tail. With k=-log(1-q(W<hcut)) and a=pi(W>R), it gives
k+(log n)a<=K+o(1). This yields a MAX allocation. No two adverse mechanisms
spend K independently in the same instance.

Third, the clipped branch uses the new proof weight
w=max(1,alpha(1-b)exp(-d)/beta). It spends actual global killing on boundary
energy, yielding the reciprocal coefficient exp(d)/r. The equality case pays
its finite cutoff deficit and never divides by a positive margin.

Fourth, a moving-slack native tree construction computes the original law to
relative error o(1), not only a first-hit lower. Its core hazard is uniformly
positive. Before reaching core or terminal, exceptional global off-level and
local reverse moves have total probability O(z+n^-2), explicitly paid.
After a genuine core hit the ORIGINAL kernel controls every remaining return
by contraction. Terminal retention uses the actual escape probability.

Finally, the exact restricted control value

    exp[-min_{J>=1} J log(1+r exp((U/J-d)_+))]

holds even for history-dependent choices after holds. A bounded
super-solution proves that mixed outgoing actions cannot exceed a pure path.
This supplies a useful obstruction to a specific method. It does not supply
the missing reduction of arbitrary reciprocal graphs.

## A transparent numerical illustration

For K=1, alpha=1/2, d=3, s=-1, the proved formulas give

    d_star = 1.164795240251424,
    exact unrestricted limsup = 1.718281828459045,
    proved unrestricted liminf lower = 1.418630176071266.

The ordinary IMH minimax amplitude is 1. The largest native phase penalty is
at phase approximately 0.38826508. These are evaluations of proved formulas,
not asymptotic estimates from finite matrix powers. The figure and its exact
parameter record are in evidence/critical_profile/. The shaded region remains
unresolved for the unrestricted minimax problem.

## Strong ordinary comparison and practical meaning

Ordinary independence MH has the same permitted proposal and target-ratio
information. Its general minimax amplitude remains K. On the SAME new native
tree families, its error at j/n->t0>0, including j=floor(alpha n/2), is
O((log n)^-4); the hybrid error is order 1/log n. Analytic direct sampling
remains admissible when the complete analytic target is supplied.

This is a robustness result with an adverse comparison for the hybrid. It is
not a wall-time, target-call or useful-sampler improvement. Delayed acceptance
can reduce per-step computation in other settings, but this investigation has
not measured or established such a receiving advantage.

The structural contribution is to locate the limit of the current reachable
transport representation. It closes exact amplitudes where attenuation can
pay a fractional crossing, proves an exact worst-case limsup elsewhere, and
excludes several easy ways to erase the residual phase cost. It does not
borrow the broad importance of MCMC as evidence for the importance of a decimal.

## Preserved failures and bounded alternative

The original expansion_native32 fixture is admitted with K=1. The unchanged
coalescence_native5462 fixture fails its frozen K=1 admission and remains an
algebraic fixture only. Neither was retuned or scientifically rerun. The
evaluator's changed subset query was not rerun; complete-level lumping here
does not assert correctness for arbitrary within-level observation events.

The rejected proof shortcut is an all-native lattice upper obtained by scalar
convex optimization without proving its transport premises. The exact control
theorem closes that restricted model only. Another inadequate shortcut is
using arbitrary ceiling depth at d=d_star; the floor construction repairs the
actual lower obligation.

A bounded precision assessment was also completed. It distinguishes
target-preserving screen error with exact correction from coherent target
evaluation error. The latter has sharp stationary bias tanh(B/4) for log-error
oscillation B, with an exact two-state full-law diagnostic. This is an explicitly
changed oracle contract and an elementary boundary, not a new precision
campaign or a premise of the native amplitude theorem.

## Verification and observed resources

Input bytes and hashes were matched to the supplied source identity. The
common-packet integrity verifier checked 452 payload files; the full original
Cycle9 verifier checked 62 payload hashes and the preserved admitted/failed
pattern. These were integrity checks with new scientific checks disabled.

A distinct contributor completed an independent challenge of the new weighted
boundary, full-return law, phase quantifiers and control-model scope and accepted
the proof without mathematical repair. The source-bound review and its status
are in reviews/ and STATUS.md. Internal review is not external acceptance or
formal verification.

The new exact two-state precision diagnostic used approximately 0.000896 CPU
seconds, with reported peak RSS 9,856 KiB. Formula plotting used 3.023384381 CPU
seconds in the first export and 3.303816998 in the repaired export, with peak
RSS 83,196 KiB. The first PNG was structurally truncated despite a successful
renderer return; its failure record is preserved. Rendering to memory and
checked small writes fixed the artifact, and the final image was inspected.
This was an artifact repair with unchanged scientific parameters.

No native large graph, long chain run, historical scientific suite, protected
programme, spending or external outreach was run. No numerical job remains
active. Inference/token, design and total discovery costs are unknown; short
replays and integrity checks are not discovery costs.

## Scientific decision and receiving use

Continue the native transport question only at its genuinely unresolved
interface: either prove an upper for arbitrary reciprocal geometries that
retains the discrete crossing cost, or construct an admitted heterogeneous
geometry that fills a trough while preserving q-weighted initial mass, native
proposal row budgets, actual rejection, every return and the one KL budget.

The accepted Cycle8 weighted energy/full-return operation and Cycle9 two-sign
proposal realization were actually used to prove the new results. Their reuse
changed a logarithmic rate into complete amplitudes in two regimes and an
exact limsup in the third. This is a concrete scientific dependency. It does
not identify a causal benefit from a prompt style, agent count, archive delivery,
or a preceding numerical instrument.

Max receives source for integration through the existing private route. The
evaluator can read the same source. The external delivery receipt records exact
bytes, hashes, readback and transport status; it does not assert either party's
reading, scientific acceptance or integration. The research mission remains
active beyond this checkpoint.

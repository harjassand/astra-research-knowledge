# A sharp rate law beyond the public-asymmetry convergence criterion

The Cycle9 investigation closes the logarithmic-rate question throughout the
convergent public-budget class. The complete proof shows that the previously
established convergence scale v_n is insufficient to describe the rate. An
explicit second quantity, the discrepancy budget D_n, determines how much
proposal mass can be transported before a global move interrupts it.

The result has passed a focused independent internal mathematical challenge.
Historical priority, external mathematical acceptance and practical sampler
advantage remain unestablished. Ordinary independence MH remains the stronger
general control under the same population-KL promise.

## The theorem

Keep the original native finite positive model: D(pi||q)<=K, proposal start q,
fixed alpha in (0,1), beta=1-alpha, and a fixed target-independent reciprocal
row-stochastic Q. At horizon n its public edge-asymmetry bound is A_n. The
local screen is (q_y/q_x)^eta (Q_yx/Q_xy)^kappa, followed by the factor
completing the target Hastings ratio. The actual diagonal and lazy mixture
C=(I+alpha G+beta L)/2 are unchanged. Policies are fixed within each run.

Let R_n be the supremum of the original full-chain TV error, and write

\[
 D_n=|\kappa_n-\eta_n|A_n,\quad u_n=\eta_n\log n,
 \quad v_n=\frac{u_n}{1+D_n},\quad r=\frac{\alpha e^{-K}}{1-\alpha}.
\]

Define

\[
 c(d)=\inf_{a\ge0,\ d+a>0}
             \frac{\log(1+r e^a)}{d+a}.
\]

For **every policy sequence with v_n tending to infinity**,

\[
 \boxed{\frac{-\log R_n}
  {\min\{\log\log n,\ u_n c(D_n)\}}\longrightarrow1.}
\]

The parameters need not converge. The proof includes oscillating mismatch
signs, arbitrarily small public A_n with large positive mismatch, and growing
finite supports. This is a logarithmic equivalent. It does not determine
the multiplicative risk at a critical boundary.

The coefficient has an explicit description. Set
F(c)=c(1-c)^((1-c)/c) and d_*=(1+r)log(1+r)/r. Then c(d)=1 when
r>=exp(d). Otherwise it solves F(c)=r exp(-d) for d<d_*, and equals
log(1+r)/d for d>=d_*. The formulas agree at their boundaries.

If D_n->d and v_n/loglog n->lambda>0, the risk exponent is
min(1,lambda(1+d)c(d)). When D_n diverges, the coefficient per unit v_n
approaches log(1+r). This recovers a whole regime, not a fitted constant.

## An explicit same-v separation

At K=1, alpha=1/2, set ell=log n, L=log ell, and use the SAME public bound
A_n=ell/L-2 for all three policies below, at sufficiently large horizons.

| Policy | eta_n | kappa_n | D_n | Exact exponent of log n in the risk |
|---|---|---|---|---|
| Matched | L/ell | eta_n | 0 | c(0), with F(c(0))=exp(-1) |
| Fixed nonzero discrepancy | (log4)L/ell | eta_n+(log4-1)/A_n | log4-1 | log2 |
| Growing discrepancy | 1/2 | 0 | ell/(2L)-1 | log(1+exp(-1)) |

Every row has **exactly v_n=L**. The respective exponents are approximately
0.6484195274, 0.6931471806 and 0.3132616875. The proof supplies elementary
strict inequalities between them; rational brackets are also executable.
Thus the growing-discrepancy risk divided by the matched risk diverges as
(log n) to the power 0.3351578399+o(1).

This is a comparison of class-supremum laws under explicit policies, not an
implementation benchmark or a claim that changing a power improves every
individual chain. The theorem also states a positive sufficiency fact: once
u_n and D_n are supplied, the separate A_n and mismatch do not introduce
another leading logarithmic parameter over this unrestricted native class.
That conclusion need not hold for fixed support, fixed graph, finite time,
or multiplicative constants.

![Coefficient from the proved formula](evidence/rate_figure_final/rate_function.png)

The figure evaluates the theorem's scalar formula at K=1, alpha=1/2 and
v_n=loglog n. It contains no fitted chain data. Its ordinary-IMH reference
has exponent1 and remains above all three displayed examples.

## Why the rate is attainable

The inherited upper operation is substantive receiving capital. It bounds
first hits using reverse-proposal weighted Jensen, subtracts actual accepted
outflow, retains the global killing mass, and propagates every first hit
through the original chain. Cycle9 uses that finite operation with a different
asymptotic scaling. For finite distortion, its limiting scalar envelope is
sup_z[exp(dc)z^(1-c)-z]. For diverging distortion, its exact finite branch
is exp(gamma p)-1, where gamma=log(1+r). The finite positive part and all
accumulated multipliers are paid explicitly.

Attainability requires a new native construction. A tree edge uses proposal
probabilities 1/(M+R_A) toward a child and R_A/(M+R_A) toward its parent,
where R_A=exp(A_n). The two outgoing row budgets sum exactly to one at an
internal vertex. Expansion handles positive mismatch; coalescence handles
negative mismatch. Choosing the integer multiplicity relative to R_A makes
the aggregate forward proposal probability tend to one while respecting
the public edge bound.

The per-vertex q ratios are selected so the actual first acceptance is a
fixed exp(-a), and the actual reverse aggregate is smaller by n^-2. The
depth grows with v_n. Its terminal importance ratio is at least
n(log n)^2, while every preceding level has importance ratio below1.
This proves that global proposals to the core are accepted. The relevant
competition is therefore the true out-of-level hazard, not every global
attempt; rejected and within-level global moves remain holds.

Each forward crossing competes against an accepted global exit and has
logarithmic survival cost log(1+r_b exp(a)). It pays a proposal-mass drop
of approximately (D_n+a)/eta_n. Optimizing the ratio of these two proved
native quantities gives c(d). Deterministic waiting windows, all terminal
within-union movement and full-chain retention are controlled. One complete
KL calculation tends to -log(1-b)<K. No information budget is spent twice.

The principal then joins finite distortion, diverging distortion, the exact
symmetric subclass at zero distortion, and the ordinary information-tail
lower. Compactified subsequences cover arbitrary moving policies. The
independent reviewer specifically checked the thin regime
v_n/loglog n->0 rather than extrapolating from a positive-ratio theorem.

## Actual finite evidence and its failure

Two fixtures were frozen before execution. They check the changed native
proposal rows, per-vertex acceptance, actual rejection diagonal, level
lumping, global hazards, full terminal escape and finite lower versus the
original law. Rational arithmetic decides all identities and inequalities;
KL uses explicit rational logarithm enclosures.

| Frozen fixture | Structural checks | KL | Conservative TV lower | Original full-law TV |
|---|---|---:|---:|---:|
| Expansion,32 native states | All pass | 0.7871982549, rigorously below1 | 0.0215347753 | 0.0491738358 |
| Coalescence,5462 native states | All pass | 1.1038363510, rigorously above1 | 0.0041085289 | 0.0423732589 |

**The coalescence fixture failed its frozen K=1 admission gate.** It remains
an algebraic check and is not an admitted empirical evidence point. Its
inputs were not tuned. The check process deliberately exits1 to preserve
that outcome. The theorem's asymptotic admission proof is separate and
uses z_n->0, which this small fixed coalescing example does not approximate
well enough for its budget.

The expansion fixture materializes a32-state native matrix and checks its
first four laws against the quotient. The coalescence fixture enumerates
all10,920 directed native proposal edges and uses the proved8-state quotient
for the finite horizon; it does not materialize a dense5462-state matrix.
No finite matrix power establishes the asymptotic theorem.

## Comparator and resource boundary

On the same newly constructed transport instances, ordinary IMH satisfies

\[
 TV(qG^j,\pi)\le p_T/(1-n^{-2})+
       bz/[(1-b)(1-z)]+b^{j+1}.
\]

For j/n approaching a positive constant this is O((log n)^-4), while
transport can make the hybrid much slower. The general ordinary minimax
amplitude remains K. Deterministic transition counts do not equate target
calls or elapsed time. An analytically known target can also be sampled
directly when that information is actually available.

The native support is 1+sum_{i=0}^J M^i. An implicit tree avoids enumerating
it but retains label bits, proposal selection, forward/reverse Q evaluation,
target and q evaluation, precision and cache costs. No free normalizer,
target table, KL estimator or absorbed sampler is introduced. This is an
exact-real theorem, not a floating-point error model.

The frozen rational check body used5.2622 CPU seconds,5.2662 wall seconds
and19,968KiB peak RSS. Constants/initial figure and the subsequent layout-only
correction are separately recorded. These measurements are not discovery
costs. Total inference, design, token and monetary costs are unknown. No paid
compute, hardware, outreach, public sharing or other owner's programme was used.

## Scientific decision and continuation

Accept the universal logarithmic law and same-v separation internally and
close this rate question at that scope. Preserve the completed convergence
criterion and every earlier native result. The absorbed first-hit operation
has now been used to prove a genuinely new rate law with a matching reachable
native construction; receipt or replay alone would not establish that use.
No causal claim about a prompting method or agent count follows.

The next selected question is the multiplicative critical risk at fixed
nonzero distortion, especially d>d_* where the optimum has fully accepted
local progress. At u_n c(d)=loglog n+O(1), integer depth and a partial final
crossing can affect amplitude even though they are negligible in this
logarithmic theorem. Determine whether a limit exists and depends only on d,
or whether an admitted geometry reveals additional information. There is
no candidate amplitude asserted by this return.

The complete proof, exact original source, contributor obligations, independent
review, failed attempts and executable evidence accompany this report.
Private delivery to the established handoff is recorded separately from
Max's reading, scientific acceptance and integration.

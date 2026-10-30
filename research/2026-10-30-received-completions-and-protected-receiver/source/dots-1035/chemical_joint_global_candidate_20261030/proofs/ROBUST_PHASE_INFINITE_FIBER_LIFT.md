# Robust phase certificates lift through arbitrary conservative infinite fibers

Status: core theorem passed child adversarial review in INDEPENDENT_ROBUST_INFINITE_FIBER_AUDIT.md; the stated homogeneous global corollary passed separately in INDEPENDENT_GLOBAL_COMPARABILITY_COROLLARY_AUDIT.md. No general recurrence claim. This is a new representation for the coupled cone, not a global boundary-gluing theorem.

## 1. Finite-policy common-resolvent lemma
Let a finite rectangular family of Metzler matrices be specified by finitely many admissible rows at each index. A policy chooses one row at each index. Assume EVERY resulting policy matrix G_pi is Hurwitz. Put v_pi=(-G_pi)^(-1)1>0 and choose a policy pi maximizing sum_i v_pi,i.

Then this one v=v_pi satisfies

    G_rho v <= -1

for EVERY policy rho, and hence for every rowwise convex combination of allowed rows.

Proof: if an alternative row at i gave (G'v)_i>-1, keep all other rows of pi. With w=(-G')^(-1)1,

    w-v=(-G')^(-1)(1+G'v)>=0.

The right-hand vector has one strictly positive coordinate; the corresponding positive diagonal inverse entry makes at least one coordinate of w-v strictly positive. This contradicts maximality of sum v_pi. No common quadratic Lyapunov function or switching stability is assumed.

This is a standard independent-row-uncertainty/policy-improvement mechanism; comparison literature includes Kozyakin, arXiv:1507.00492. The lemma above is proved directly, so no unverified external implication is needed.

## 2. Uniformity of the earned phase theorem
Take the finite-phase weakly reversible mass-action network from UNIVERSAL_HALF_FACTORIAL_PHASE_EXTENSION.md, on a projected phase component with at least one nonzero residual increment. Permit each positive reaction coefficient independently to range over a fixed compact positive interval. Fix rational alpha in (0,1/2) and the same fixed inflation factor2.

The stationary phase-tree polynomial degrees are independent of coefficient choices: each relevant tree coefficient is positive, so changing coefficients never cancels a leading term. Thus the same integer offsets beta_j and residual increments delta_e are used for every policy.

There are finitely many endpoint coefficient policies. Each retains exactly the same weakly reversible complex graph with positive coefficients, so the existing half-factorial theorem makes its inflated tilted matrix G_pi(r) Hurwitz for all sufficiently large r. Take the largest of the finitely many thresholds. The family of all interval rows lies in the convex hull of these endpoint rows.

Apply the common-resolvent lemma at each r. Moreover every v_pi(r) is rational in r^(1/q), where alpha=p/q. The finitely many sums sum_j v_pi,j(r) have eventually fixed pairwise order: a nonzero rational-function difference has only finitely many large positive zeros. Hence ONE fixed policy pi_* maximizes for all sufficiently large r. Its vector v(r) is positive rational-Puiseux and obeys fixed-shift ratios1+O(1/r).

Set

    V(n,j)=Gamma(n+beta_j+1)^alpha v_j(n+beta_j).

The existing fixed inflation absorbs the Gamma and v shift errors for every nonzero delta edge; delta=0 edges have no shift error. Therefore this ONE V satisfies

    L_kappa V <= -Gamma(n+beta_j+1)^alpha

for every permitted state-dependent coefficient choice kappa at every sufficiently large state. Coefficients may vary arbitrarily with hidden variables or time; no derivative or slow-variation hypothesis is used. The positive lower interval bounds and fixed finite graph are essential.

All-delta-zero projected components are NOT covered by the Hurwitz claim. They require the separate conserved-residual/killed-boundary treatment already recorded in the halo theorem.

## 3. Actual infinite-fiber lift
Let a physical process have any number of unbounded internal populations x, a finite phase j, and an integer aggregate n=N(x). Suppose every nontrivial projected transition is a reaction of the earned finite-phase graph: it changes (n,j) by the prescribed increment, and its actual rate is

    kappa_e(x,j) (n)_(a_e),
    0<kappa_e^- <= kappa_e(x,j) <= kappa_e^+<infinity

on the region in question. There may additionally be arbitrary transitions preserving BOTH n and j. Their contribution to V(N(x),j) is EXACTLY ZERO, regardless of their rate, mixing, metastability, or fiber size.

The common certificate therefore gives the stated physical generator inequality throughout that region. It is not an average over the fiber. The finite-background premise has been replaced, for this scope, by an explicit projected rate-comparability test.

This statement does not by itself establish nonexplosion of arbitrary added invisible dynamics; only the displayed generator inequality is claimed locally. In the mass-action application each fixed total-population fiber is finite.

## 4. Concrete coupled-cone application
For the hard network, choose n=N=A+C and the consecutive phase corner J={0,...,K}, K>=3, with its exact complete-linkage halo. Project the connector complexes to

    (B=0,order0), (B=1,order1), (B=4,order3)

and their translated phase copies. The complete lifted graph is weakly reversible and its phase projection is connected. It has a nonzero residual increment: if every delta were zero, the four retained immigration edges B=0→1→2→3→4 would force beta_4=beta_0−4, while clearing B=4→0 forces beta_4=beta_0−3, a contradiction. This explicit corner choice avoids invoking the nontrivial theorem on a neutral halo. Fast A/C reactions preserve N and B, so their generator contribution to this V is identically zero, including their multistable composition dynamics.

On A>=epsilon N, for sufficiently large N,

    AB = (A/N) B (N)_1,
    (A)_3(B)_4 = [(A)_3/(N)_3] (B)_4 (N)_3,

with ratios in fixed positive intervals depending only on epsilon. Immigration has coefficient1. Thus the actual physical cone receives a common certificate V(N,B), with exact halo agreement on the chosen B-corner. C need not be macroscopic because all C-dependent reactions are invisible to (N,B).

There is no stationary phase assumption, no frozen A, no spectral gap, and no supplied Lyapunov barrier. This attacks the balanced-cone composition obstruction in a genuinely different way from shell-profile inversion.

## 5. Exact remaining obligations
The certificate is local to the region where coefficient lower bounds hold and to the physical corner on which the halo agrees. The process may leave both. It does NOT solve:
- A/N→0, where projected coefficient lower bounds vanish;
- outgoing feedback at the outer finite-halo phase boundary;
- global matching with the separately earned exact low-phase function F;
- neutral projected components without the separate killed solve.

In particular, having local certificates covering regions is not yet a global recurrence proof. The policy construction is finite but may be exponentially large; no efficient algorithm claim is made.

## 6. Genuine global corollary when projected comparability is structural
For a TIME-HOMOGENEOUS physical CTMC with finite total rate at every state and finitely many species, suppose the phase alphabet is truly finite and closed (not a truncated halo), N is the total count of all unbounded populations, and the projected rate bounds hold everywhere outside a finite N set, Then the same certificate is globally normlike. Each fixed-N physical fiber is finite. Standard stopped Foster arguments therefore give nonexplosion and positive recurrence of every closed irreducible physical class, with all exponential N moments. Neutral projected components have conserved N+beta_j and therefore finite physical fibers; handle them directly. If the physical network is weakly reversible, its communicating classes are closed.

A concrete rate-level condition earns the global bounds without exact lumpability. For each projected edge e of source total order a, suppose EVERY source composition y with |y|=a is represented, and the total rate coefficient of its channels projecting to e lies between

    c_e a!/(product_i y_i!) and C_e a!/(product_i y_i!),

with fixed 0<c_e<=C_e. The multivariate falling-factorial identity

    (N)_a = sum_(|y|=a) [a!/(product_i y_i!)] product_i(x_i)_(y_i)

then bounds the actual aggregate projected rate between c_e(N)_a and C_e(N)_a at every composition, including all population boundaries. Target composition and internal conservative dynamics may vary arbitrarily subject to the stated projected transitions; no fast equilibrium is required.

This is a dimension-independent structural corollary, not general chemical recurrence: source-completeness is a substantial explicit restriction. It supplies projected rate comparability, not an assumed Lyapunov function. Removing source-completeness at boundary strata remains the main unresolved question.

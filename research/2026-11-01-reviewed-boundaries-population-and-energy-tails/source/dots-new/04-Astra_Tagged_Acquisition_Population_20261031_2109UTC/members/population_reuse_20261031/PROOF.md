# Acquired local knowledge for population service-level planning

New unreviewed construction. Earlier accepted archives are unchanged. This is
an ordinary finite-population/mean-field construction joined to an acquired
local certificate, not a claim to invent mean-field control or to simulate an
N-fold transcript with N-independent error.

## P1. Existing interface and task

There are N software workers. Each has a named microscopic local state in a
finite set of size n. The same unknown stochastic actions A_1,...,A_m govern
all workers. Initial states are independent with the specified law mu, and all
subsequent worker noises are independent across workers and times, conditional
on chosen actions. This factorization is part of the software interface, NOT
learned from a single row sampler and NOT inferred for a physical fleet.
Fresh deployment states/noises are independent of acquisition. All comparators
receive exactly these premises and all source-row metadata.

Acquisition obtains a partition Z into r blocks, uniform block averaging W,
P=ZW, and stochastic coarse actions B_a. The initial law must satisfy mu P=mu;
its actual microscopic preparation is specified and charged. At deployment a
controller observes the vector of current block occupancies and may choose a
broadcast table pi:{1,...,r}->{1,...,m}. Each worker reads its own block and
applies pi(g). A common action is the special case of a constant table.
Controllers may depend on the entire prior occupancy/action history and use
independent randomization. They may NOT distinguish workers by hidden local
state or individual unrecorded history. The executable chooses a deterministic
time/block table; it does not implement an arbitrary adaptive comparator.

The later tasks are explicit linear terminal service utility w.x, 0<=w<=1,
and service-level questions x(S)>=theta with a checked strict mean margin.
The statement also covers any explicitly supplied utility F:[simplex]->[0,1]
with a derived TV Lipschitz bound kappa, but no efficient nonlinear planner is
assumed. For piecewise-affine min/max/clipped expressions, osc(w)=max w-min w
bounds each affine leaf's TV Lipschitz constant and max/min/clipping preserve
the largest such constant. Discontinuous threshold indicators are NOT covered
by boundedness alone; the service-level assertion uses the margin separately.

## P2. Deterministic acquired-model event

Suppose the received local event certifies simultaneously for every action:

 c >= max_(i in g) TV((A_a Z)[i,:],(W A_a Z)[g,:]),
 e >= max_g ||(W A_a Q)[g,:]||_(H^-1), H=I/n,
 d >= max_g ||(W A_a Z)[g,:]-B_a[g,:]||_1.

The tagged-row construction acquires these numbers, the partition, and its
confidence from actual observations; they are not supplied coordinates or
planning oracles. It retains row->destination-block metadata jointly with
pooled microscopic destination counts. Its source/protocol assumptions and
all failed prefixes/costs remain dependencies of this result.

For any table pi, A_pi[i,:]=A_pi(g)[i,:] and B_pi[g,:]=B_pi(g)[g,:]. Because
pi is constant within each acquired block, W row selection, Z lifting and P
commute with the appropriate block selector. Thus precisely the SAME c,e,d
bound A_pi. No sqrt(m) spectral assertion is used. Stochasticity gives, for
q=Qq, ||Q A_pi q||_infty <= (1+e)||q||_infty. For 0<=f<=1,
||Q A_pi P f||_infty <= c. Also ||q||_H<=||q||_infty.

Let z_0=0, z_(j+1)=min(1,c+(1+e)z_j) and

 E_t = t d/2 + e sum_(j<t) z_j.                         (1)

Backward induction for any terminal block indicator gives the uniform word
bound TV(mu A_pi0...A_pi(t-1) Z, mu Z B_pi0...B_pi(t-1))<=E_t.
The fine factor 1/2 uses probability-row zero sum and [0,1] continuation.
This assertion is simultaneous for ALL table words and subsets; no union over
words is added to acquisition confidence. The stronger full-record/history
proof is useful capital, but only this marginal-word corollary is needed here.

## P3. Finite-class population concentration, without ambient n

Condition on all acquisition information on its valid event. Put J=m^r for
table broadcasts (J=m for common actions). On a PROOF-ONLY space give every
worker independent initial randomness and independent uniform transition
noises. The inverse-CDF interpretation defines every fixed action-table word
counterfactually. It is not an acquired common-random-number simulator and
requires no execution of counterfactual paths.

For each FIXED prefix w of length t and subset S of r blocks, the N terminal
membership indicators are iid Bernoulli with true word-law p_w(S). Hoeffding's
one-sided inequality and the identity TV(x,p)=max_S[x(S)-p(S)] give

 P(exists t<=L,w in [J]^t: TV(hat p_w,p_w)>eta)
 <= (L+1) J^L 2^r exp(-2 N eta^2).                       (2)

No independence between different words/subsets is required. On the common
good event an actual adaptive global controller follows one of these words,
and its actual worker trajectories equal the coupled trajectories for that
word. Hence (2) covers the realized path WITHOUT conditioning on its observed
history or dividing by a rare-history probability. This works even if the
controller knows the learned model and adaptively selects its tables.

Take eta >= sqrt([r ln2+L lnJ+ln((L+1)/delta_pop)]/(2N)). Combining (1),(2),

 TV(actual empirical block occupancy at t, coarse law of realized word)
 <= min(1,E_t+eta), for all t<=L, with failure <=delta_pop.       (3)

Finite-bit implementation uses K=.7*(r+L*ceil(log2 J)+ceil(log2((L+1)/delta_pop)))
and an outward dyadic square root eta>=sqrt(K/(2N)). Since .7>ln2 this is
conservative. The executable forms log2 J as r*ceil(log2 m) without enumerating
J. Rounding, integer denominators, policy storage and all N L actual worker
updates/map lookups are charged. Large n is absent from (2), but remains in
acquisition and partition storage. Small/rare initial blocks still require an
actual allowed preparation; independence does not make that preparation free.

## P4. Ordinary Bellman planning and adaptive population competitors

For linear terminal w.x, standard r-state finite-horizon Bellman iteration
V_0=w, V_(j+1)(g)=max_a sum_h B_a(g,h)V_j(h) returns a time/block table and
coarse optimum V*. It maximizes over all fixed table words without enumerating
m^(rL): induction dominates every table choice componentwise. It costs
L m r^2 scalar products. If B has a common denominator D and w denominator F,
exact integer DP uses denominator F D^j, O(log F+L log D) value bits plus input
and arithmetic overhead; the prototype measures actual peak integer bits.

Let a generic coarse planner have certified gap gamma, and F have Lipschitz
constant kappa and range [0,1]. On the good population event every adaptive
controller's actual utility <= coarse OPT+kappa(E_L+eta), because its realized
word is one of the deterministic words defining OPT. The selected fixed word
has utility >= coarse OPT-gamma-kappa(E_L+eta). Consequently its expected
regret against ALL allowed adaptive broadcast-table controllers is at most

 gamma + 2 kappa (E_L+eta) + 2 delta_pop.                  (4)

This is conservative and clipped to 1. For linear tasks Bellman earns gamma=0.
For nonlinear tasks gamma must actually be earned; no polynomial nonlinear
planning conclusion follows merely from small r. A simplex grid with mesh
1/K has binomial(K+r-1,r-1) states, per-step TV rounding at most (r-1)/K,
and potentially m^r table actions. Those costs are real and can be prohibitive.
Strong retained grid, interval-MDP, reachable-set and POMDP planners are proper
baselines; n^N enumeration is not the primary comparator.

## P5. Rare collective failure and distinct probabilities

For a chosen fixed table word, if its exact coarse terminal service mass v
satisfies v-(E_L+eta)>theta, then with acquisition confidence at least
1-delta_acq the true deployed failure probability P(hat p(S)<theta) is at most
delta_pop. The acquisition statement concerns whether the certificate is
valid, not a posterior confidence after observing PASS. Unconditionally the
joint bad event is at most delta_acq+delta_pop, NOT delta_pop alone. Q fresh
executions cost Q N L updates and a union budget Q delta_pop+delta_acq unless
an explicit alternative risk accounting is supplied. A current .001 learning
confidence cannot be relabelled as an unconditional 10^-9 safety guarantee.

For a FIXED chosen policy, the population bound can be sharpened using its
single word (J=1), and a scalar terminal goal uses only one Bernoulli tail,
eta_goal=sqrt(ln(1/delta_pop)/(2N)), with no r/L/word union. We report this ordinary
improvement separately. It does not provide an adaptive-policy regret bound.
A fresh single-worker policy Monte Carlo lower mean plus this scalar tail is
a strong, usually cheaper one-goal baseline. Retained policy/goal evaluations
and count metadata must be cached; acquisition is amortized only if actual
future task diversity and all comparisons justify it.

## P6. Informative failures and prior scope

Shared worker noise destroys the N^-1/2 conclusion: if all workers share one
Bernoulli(1/2) state, occupancy is always 0 or 1 and deviates by 1/2 from its
mean for every N. A discontinuous threshold at the mean is not controlled by
arbitrarily small mean error. A local full-record TV error e can yield N-fold
transcript TV 1-(1-e)^N; (3) deliberately certifies a weaker aggregate task.

Gast and Gaujal (2009), Sections 2--3, already formulate independent-particle
controlled systems and prove convergence of optimal finite-population value
to deterministic mean-field value, including optimal policies and a grid-
computing application: https://arxiv.org/pdf/0903.2352 . This is a direct prior
match for the population-control headline. Our present derivation makes an
explicit finite-class finite-N confidence join to an empirically acquired,
robust local quotient; it is NOT a historical novelty or practical superiority
claim. The component is available equally to ordinary retaining planners.

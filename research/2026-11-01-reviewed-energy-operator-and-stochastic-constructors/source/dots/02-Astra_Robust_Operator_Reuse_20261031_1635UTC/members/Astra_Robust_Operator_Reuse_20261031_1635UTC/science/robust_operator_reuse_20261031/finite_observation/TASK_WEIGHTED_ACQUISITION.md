# Paying for observations where future tasks can actually expose them

Separate author extension, 31 October 2026; not independently reviewed.
This closes a limitation of the full-entry frontend, not a claim to invent
model-based exploration, the simulation lemma, or reward-free RL.

## The important acquisition distinction

Uniform entry confidence over n^2 entries may cost far more than the learned
small replay saves. More importantly, it inspects every state even when the
fixed initial task distribution can expose only a small part of the system.
The following sound incomplete certificate discovers useful observation
locations rather than taking a useful probe set as input. It replaces the
worst-row uncertainty term in PROOF.md; all ordinary retained methods receive
the same refinement.

Let ell=mu be a known initial probability distribution (signed ell is handled
by replacing it with |ell|). Assume only stochastic kernels, bounded b, and
generative row sampling by a named state/action. The state-label universe can
be large; b(label) is a supplied bounded task function whose evaluation cost
is paid. No shared equilibrium or small reachable set is promised. Maintain
finite-support stochastic center rows C_a(i,.) and certified bounds

    ||A_a(i,.)-C_a(i,.)||_1 <= r_a(i) <= 2.

For a never-observed row take C_a(i,.)=delta_i and r_a(i)=2. This is a valid
statement about EVERY stochastic row, not an optimistic assumption. It needs
no observation of that row.

Define v_0=0 and the finite-horizon Bellman upper envelope

    v_(t+1)(i) = min(2, max_a [r_a(i) + sum_j C_a(i,j)*v_t(j)]).

Let osc(b)=max b-min b. For every length-l word, including words later chosen
adaptively,

    |mu^T A_w b-mu^T C_w b| <= (osc(b)/2)*mu^T v_l.

**Proof.** Subtract the midpoint of the range of b; stochasticity makes this
shift cancel from the difference, leaving ||b||_infinity=osc(b)/2=M. For any
word write A_a x-C_a y=(A_a-C_a)x+C_a(x-y), where x is a true shorter-word
value vector. Its infinity norm is at most M. Entrywise absolute error is
therefore at most M*r_a+C_a times the previous error. Every true and center
value is in [-M,M], so their difference is also bounded by 2M. Induction gives
the displayed Bellman envelope, which permits the action to depend on state
and is therefore an upper bound on every open-loop word. Multiply by mu.
For signed ell use |ell| in the final multiplication. QED.

This is not solving the hard optimal-word verifier: state-feedback choices
form a deliberately larger class. Its dynamic program is polynomial in the
finite center graph and L. It may overestimate error and fail admission.

The DP only needs the center states reachable from supp(mu) in at most L
steps. Unknown rows self-loop, so the default for a completely unseen state
is known symbolically. Sampling a selected row can reveal new labels and
expand that graph. A rare true transition to an unseen state is NOT silently
deleted: its possible mass is already paid in the preceding row's r_a(i).
The proof uses the center on the left of the error recurrence precisely so
that unknown true occupancies are not treated as supplied information.

## Acquiring sparse row confidence without scanning the label universe

At an adaptively selected row, use prior data and a training batch to choose a
finite label set S, including the current state as an anchor. Then draw a
FRESH independent validation batch of N next-state samples. Let hat p_j be
the validation frequency for j in S and hat q the fraction outside S. Define
the center by C_j=hat p_j+hat q*1_(j=anchor) on S and zero elsewhere.
For a chosen rational zeta>0, simultaneous Hoeffding bounds on these |S|+1
bins hold with failure at most delta_call when

    N >= log(2*(|S|+1)/delta_call)/(2*zeta^2).

On that event,

    ||A_i-C_i||_1 <= min(2, (|S|+1)*zeta + 2*hat q).

Indeed the known-label deviations contribute at most |S|*zeta+hat q, and the
unknown-label mass is at most hat q+zeta. Unknown destinations do not have to
be enumerated. This support-sensitive but conservative bound may use many
more samples than optimal distribution estimators; no optimality is claimed.

Call t may use delta_call=delta/2^(t+1), or the executable's telescoping
allocation delta/[(t+1)(t+2)]; either sums to delta. Conditional on the past and chosen
S, the fresh validation batch is independent. A union bound covers every
adaptively selected call, geometry, rank, stopping decision and later query.
Earlier validation labels may become future training labels, but cannot be
reused as an independent validation batch after that change without a new
argument. All training/validation samples, failed calls and discovered labels
are charged. A rational conservative implementation may replace the logarithm
by K=ceil(log2(2*(|S|+1)/delta_call)) and use N>=K/(2*zeta^2), since ln(2)<1.

## A concrete acquisition policy, not a promised planner

Compute the Bellman envelope and a maximizing state-feedback policy for the
uncapped expression. Propagate mu under that center policy to obtain explicit
state/action occupancies. Prioritize a row by its uncertainty times occupancy,
refine it with fresh validation, and recompute. A fairness rule can revisit
all active rows. Stop only when the numerical certificate meets its allocated
observation budget, or return INCONCLUSIVE at a declared sample/work budget.
No fast termination or small active graph is asserted for every input.

For a fixed finite center graph, one Bellman pass costs O(L*m*E) rational
arithmetic up to representation conventions, where E counts stored/default
row edges per action (equivalently O(L times the total state/action-edge
count)). The planner is not free. An acquired common denominator D for all
center probabilities and radii has bit length no more than the sum of their
individual denominator lengths. Values through horizon L have denominator
dividing D^L after using a common radius denominator in D; their numerator
length grows polynomially with L*log(D) and the bounded value range. Thus the
exact comparisons have paid polynomial bit complexity, not a hidden
worst-open-loop-word oracle. The executable includes every repeated Bellman
pass in acquisition time but does not instrument all individual bit operations.

After this observation admission, restrict the center computation to its
reachable finite graph, CLOSED under all stored center transitions, and acquire the task-sensitive stable replay of
PROOF.md there. Add its compression and finite-execution errors to the
Bellman observation budget. As the active graph was obtained from observed
labels and paid confidence bounds, it is not a supplied good decomposition.
If the learned center already has a cheap sparse implementation, ordinary
retained on-demand computation may still be best; it gets the same graph.
The executable composition indeed retains all seven acquired center states:
its replay rank is seven. It demonstrates sound end-to-end admission, NOT an
extra dimensionality-reduction benefit over that ordinary sparse baseline.

## A lower bound showing exactly when global admission cannot be cheap

Give the learner a known binary routing tree with K leaves, starting at its
root. Binary letters route to any chosen leaf in ceil(log2 K) steps; one extra
letter tests that leaf. At leaf j the test goes to a success state with
unknown probability p_j, otherwise to failure. Let b be the success
indicator. Every future routed test word asks for one p_j. All routing is
provided for free in this lower bound, making the learner strictly stronger.

Compare the null model p_j=0 for every j with the K alternatives in which
exactly one p_j=3eps (0<eps<1/6). A universally eps-accurate admitted model
must distinguish the null from every alternative. If it succeeds with
probability at least 1-delta on every model, with 0<delta<1/2, then, under the null,

    E[N_j] * log(1/(1-3eps)) >= kl(1-delta,delta)

for each j. This is the ordinary likelihood-ratio/data-processing testing
bound: only samples at row j have different laws. Summing gives
Omega(K*log(1/delta)/eps) row samples at small eps, even though the null task
function is identically zero and has a zero-dimensional useful output model.
The claim assumes a successful, accurate admission with probability 1-delta;
an algorithm allowed always to say INCONCLUSIVE is not subject to that cost.

Thus small task rank alone cannot guarantee cheap uniform acquisition. If only
D distinct leaves will ever be queried, a lazy admitted-task interface needs
to inspect only those D, retaining each result with a valid confidence
allocation. That is ordinary strong on-demand learning, not a new capability
to be excluded from comparison. The proper tradeoff is task coverage versus
amortized later execution, not exact algebra dimension versus learned rank.

## Primary antecedents and limits on the claim

Simulation and explore-or-exploit arguments are established in Kearns--Singh,
https://web.eecs.umich.edu/~baveja/Papers/ICML98_KS.pdf . Reward-free exploration
explicitly targets coverage of significant states:
https://arxiv.org/abs/2002.02794 . Task-agnostic reuse and strong sample
complexity baselines include https://arxiv.org/abs/2006.09497 and
https://proceedings.mlr.press/v247/li24a.html .

The contribution of this package is a transparent, composable observation /
compression / finite-replay certificate and an honest conditional acquisition
route. The Bellman frontend is an application of established simulation and
exploration machinery. Neither a new general learning theory nor an advantage
over the best equally informed retained methods has been demonstrated.

# Candidate extension: all block-observation history policies

New investigation, NOT covered by the accepted feedback receipt/archives.
This is a uniform finite-horizon approximation theorem, not a general POMDP
solver. It must be independently checked before any accepted-scope upgrade.

## Interface and acquired inputs

The true A_a are stochastic matrices on explicitly labelled states. A learned
partition has averaging projection P=ZW, Q=I-P, and block masses pi_g=n_g/n.
A policy sees only the sequence of acquired block labels, its past actions,
and independent private randomness; it may depend on the entire history.
Initial law is block-uniform, terminal reward is block-constant in [0,1].
The same forward-simulator/map observation interface and its costs remain.
Microscopic-state policies and unobserved physical sensing are not included.

Use the SAME simultaneous operator event already received in the feedback
work: global action observation ||A_a-C_a||2<=t; incoming ||QA_aP||_H<=e_in;
outgoing max_g ||(WA_aQ)[g,:]||_(H^-1)<=e_out; stochastic coarse action B_a
with infinity row error <=d; and acquired local bounds

    U_gh >= max_a ||Q_g C_a[g,h] Q_h||2,
    H=I/n, Q_g=I_g−1_g 1_g^T/n_g.

All quantities come from the previous sampled/finite-bit acquisition, not
from the true unknown matrices. No new statistical union is required for
a deterministic implication of this already uniform event.

Define the conservative local-history constants

    c = max_g e_in/sqrt(pi_g),
    kappa = max_g [sum_h sqrt(n_h/n_g) U_gh + t/sqrt(pi_g)].

Outward rational square-root bounds suffice. Kappa need not be below one.
Let z_0=0 and z_(j+1)=min(1,c+kappa*z_j). Define

    E_hist(L)=L*d + e_out*sum_(j<L) z_j.

## Backward policy-tree induction (ordinary proof)

At a node whose observed current block is g, its action a is fixed after
conditioning on the observed history and private randomization. For each
possible next block h there is a possibly different continuation tree. Let
f_h be that tree's true expected terminal-reward function on block h. Patch
these functions into a vector f on the microscopic state space. Each entry
of f lies in [0,1]. Write f=P f+q, with block q_h=Q_h f_h.

Suppose every depth-j continuation obeys ||q_h||_(I_h/n_h)<=z_j, uniformly
over all histories and trees. Then ||q||_H<=z_j. The new current-block
residual is

    Q_g A_a f = Q_g A_a P f + Q_g C_a q + Q_g(A_a-C_a)q.

The incoming term has local norm at most e_in/sqrt(pi_g), since ||Pf||_H<=1.
The observed residual term has local norm at most
sum_h sqrt(n_h/n_g) U_gh z_j. This bound permits unrelated continuation
vectors in every child block; it does not reuse one global value vector as
if the policy were Markov. The observation-error term has local norm at
most t/sqrt(pi_g) z_j. Finally, a [0,1]-valued function has centered local
norm at most one. This proves the capped recurrence for every policy tree.

No step conditions on a history's probability or divides by it. Continuation
value functions are defined counterfactually on every state of their current
block, even for histories or microscopic states that happen to have zero
probability under the chosen initial law. Intermediate block averages are
algebraic decompositions, NOT claims that the true posterior given a history
is uniform within its block. The actual expected payoff is recovered only
by the original initial-law averaging of the backward root value.

Let v_h be the true block-average of f_h and let vhat_h be the coarse value
of the SAME child tree. At the current node,

    true_average = sum_h (WA_aZ)[g,h] v_h + (WA_aQ)[g,:] q,
    coarse_value = sum_h B_a[g,h] vhat_h.

The outgoing term is at most e_out*z_j. Replacing the coarse row costs at
most d because every v_h lies in [0,1]; propagating child errors costs at
most their maximum because B_a is stochastic. Thus the worst tree error
satisfies E_(j+1)<=E_j+d+e_out*z_j, proving E_hist. Initial block averaging
preserves that error. Randomized policies follow by conditioning or convexity.
The event is uniform over the entire finite policy-tree class, so data-
dependent choices of a policy or compatible future task require no extra
probability union. It is not posterior confidence conditional on PASS.

## Polynomial planning and restricted optimality

On the coarse MDP, ordinary finite-horizon Bellman induction is optimal even
among randomized history policies: conditioning on current coarse state and
remaining time leaves the same transition law, and the inductive optimum
bounds every child tree. Hence its ordinary Markov policy pi_hat satisfies

    true_value(pi_star_history) - true_value(pi_hat)
       <= E_hist + E_chosen,

where E_chosen is any already valid error certificate for pi_hat (for example
the tighter accepted Markov-feedback bound). Alternatively 2E_hist suffices.
No true hidden-state history optimization is executed or assumed. The cost
is acquiring and receiving this sufficient uniform certificate, then ordinary
coarse Bellman DP, not enumerating a policy tree or solving a general POMDP.

## Initial saved-fixture calculation, not yet independently reviewed

For the accepted n4096/r4/m2/L24 record, acquired U has maximum row sum about
0.531439662 and t=1/4, giving kappa about1.031439662, c about0.011183495.
The capped recurrence gives E_hist about0.042102998. Combining with the
accepted chosen-policy E about0.014402306 gives regret about0.056505304
against all block-observation history policies, IF this extension checks.
This is not an epsilon .02 history certificate; a caller must request and
receive a suitable new history tolerance, e.g. .05 for value error.
The original accepted files and archives remain unchanged.

## Why microscopic policies remain excluded

`check_microscopic_limit.py` constructs four states with two blocks,
p=(1,1,-1,-1)/2, q=(1,-1,1,-1)/2, and
A_±=J/4 ± delta(pq^T+qp^T), delta=1/10. With block-constant terminal
reward (1,1,0,0) and a uniform initial law on the first block, every
one-step block-history policy has value1/2 and its coarse model is exact.
A controller choosing action according to the microscopic q sign instead
has value11/20. Thus even a zero history-class error at horizon1 cannot
be promoted to microscopic-policy optimality. The eleven exact checks
also verify stochasticity and zero complement action for every block policy.

## Receiving and provenance boundary

The prototype `receive_history.py` receives the original n4096 task and
all accepted count/probe arithmetic through the unchanged full polynomial
receiver, then checks the deterministic local-history implication. A new
requested history tolerance is bound separately from the old acquisition
tolerance. The stored chosen policy remains the ordinary Markov table; no
exponential history policy is output or implicitly optimized. The stronger
comparison class comes from uniform policy-tree induction. All original
source sampling, failed rounds, old norm attempts, packed map, sensor/lookup
and exact-arithmetic costs remain. There is no new probability union, but
there is a paid repeat of full receiving and Bellman arithmetic.

The executable fixes the accepted original source/task artifact, and its
callable receiver additionally requires caller-supplied terminal indicator,
initial numerator mask and normalizing denominator, plus external horizon,
action-count, confidence and new tolerance. It rejects changed reward/initial
tasks rather than silently receiving a different easier one. The generic
proof covers compatible block tasks, but arbitrary new-task execution is
not claimed for this fixed-task prototype. `fixture_task()` supplies the
public original task from a separately hash-pinned source record for the CLI.

## Finite-bit recurrence backend

`integer_history_trace.py` acquires the lcm D of denominators of c, kappa,
e_out and L*d. If z_j=znum/D^j, the next numerator before capping is
cnum*D^j+knum*znum and the cap is D^(j+1). The cumulative residual sum is
kept at the same denominator. This executes the recurrence using ordinary
integers and exactly agrees with the received rational expression. On the
fixture D has78 bits, the recurrence costs99 scalar products, and its
largest measured integer has1948 bits. Lcm/input conversion, comparisons,
gcd/serialization and the inherited full receiving are additional. This
small constant-computation cost is not a replacement for the original
billions-call acquisition or for the279,363,350 replayed norm products.

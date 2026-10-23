# Ordinary comparator and closest primary results

## Pure independence MH remains the strong general control

The entire theorem uses proposal initialization q and one supplied
population D(pi||q)<=K. Under those same premises the preserved ordinary
IMH minimax law has amplitude K at scale 1/log n. Equation (28) of the
new principal proof gives the matching two-state lower inside the
hybrid class itself with Q=I, independent of every mismatch policy.

The new theorem therefore restores or delimits robustness of an added
local mechanism. It does not improve the general ordinary sampler.
The sufficient regime v_n/loglog n->infinity yields exactly amplitude K,
not a smaller coefficient.

On each new multilevel lower family, put s_q=sum_{i=1}^J q_i and
pi_tree=sum_{i=0}^J pi_i. The same-input, full-return comparison is

TV(q G^j,pi) <= pi_tree + s_q/(1-b) + b^(j+1)
             <= p/(1-n^-2) + bz/[(1-b)(1-z)] + b^(j+1).

This tends to zero for every j->infinity, including deterministic j/n->t>0,
while the actual hybrid's liminf TV is at least
b[beta/(2alpha+beta)]^J>0 on the adverse subsequence.
The proof first reaches the core and uses ordinary total-variation
contraction afterwards, retaining all returns.

For fully disclosed analytic fixtures, direct target sampling by level/core
mass and uniform within-level indexing is also allowed. Full enumeration
is legitimate when the actual input size makes it affordable. The theorem
does not hide those options.

## A law comparison is not a computational speed comparison

The hybrid makes local and global proposals, evaluates target/q ratios and
forward/reverse Q probabilities, and pays for indices, precision and caches.
Pure G has its own global target evaluations. A deterministic fraction of
n global steps is a mathematical comparator, not an assertion of equal
wall time or equal evaluation cost. No end-to-end speed benchmark is claimed.

The exact finite fixtures also compute the matched-screen local control
on identical q,pi,Q. Some small-horizon hybrid errors happen to be smaller
than pure G and others larger. These observations are not used to infer
a universal ordering or an asymptotic rate.

## Closest primary mathematical context

Chris Sherlock and Anthony Lee, *Variance bounding of delayed-acceptance
kernels*, arXiv:1706.02142v4, Section 4.1 and Corollary 2:
https://arxiv.org/html/1706.02142v4

They give acceptance comparisons based on bounded log-error discrepancy
and show inheritance of variance bounding when a surrogate-to-target
density ratio is bounded above and away from zero. Example 3 exhibits an
independence-sampler delayed-acceptance modification that loses geometric
ergodicity and variance bounding.

Those are important precedents: factorization can hurt, and bounded
discrepancy can preserve qualitative properties. The current claim is
different in its explicit premises: a moving-horizon, support-uniform
proposal-start TV criterion for a fixed lazy mixture, one forward KL
budget, and a genuine public reverse-proposal asymmetry bound. The
reciprocal edge factors need not arise from one surrogate density.
The new condition quantifies how rapidly the public budget may grow.

Christophe Andrieu, Anthony Lee, Sam Power and Andi Q. Wang, *Comparison
of Markov chains via weak Poincare inequalities with application to
pseudo-marginal MCMC*, Annals of Statistics 50 (2022), 3592-3618,
DOI 10.1214/22-AOS2241, Lemma 25 and Proposition 27:
https://awllee.github.io/papers/AOS2241.pdf

These results give the ordinary IMH Dirichlet representation and
weight-tail weak-Poincare control. They are the closest inspected
ordinary functional-inequality context for the smoothing part. That
part is accepted inherited capital. The new work addresses reachable
transport from proposal-heavy, target-light states through actual
reciprocal proposal budgets and retains the full original law.

The targeted primary check does not establish historical priority.
Internal proof acceptance, external mathematical acceptance, useful
implementation, and scientific significance remain separate.


# Next candidate: control reuse without predictive aggregation

Unreviewed first algebraic construction, outside the frozen contrastive package.
No new observations, fixture, novelty, or consequential advantage claimed.
This is a possible constructive response to the nonreducing-background failure,
not a further routing benchmark or a promise that acquisition is cheap.

## Task and precise algebraic foothold

Many discounted, block-compatible reward tasks on a named-state process with
ordinary iid forward row access. A baseline action A0 may have arbitrary
full-rank dynamics and need NOT preserve the acquired block partition P=ZW.
Assume, initially exactly, that action DIFFERENCES satisfy

    A_a - A0 = Z D_a W,       D_0 = 0,

where Z is an acquired partition, W uniformly averages its blocks. This is a
control-effect condition, not low rank of the transition kernels themselves.
Fix rational 0<gamma<1. Set

    G=(I-gamma A0)^(-1),  R=W G Z.

For any new reward r=Zg (same reward for all actions), Bellman optimality gives

    v* = G Z(g+y*),
    y*_h = gamma max_a [D_a R(g+y*)]_h.

Hence consider this r-variable, mr-constraint LP, not policy enumeration:

    minimize h^T y,
    y_h >= gamma [D_a R(g+y)]_h   for every h,a,
    h^T = (1/r) 1^T R.

The baseline constraint is y>=0. Any feasible y induces v=GZ(g+y) satisfying
v>=Zg+gamma A_a v for every a, hence v>=v*. The true y* is feasible. The
objective differs by a constant from the uniform-microscopic initial value
when blocks are balanced. That initial law has full support, so a minimizer
must induce v*. (For unequal blocks use their positive size weights instead.)
The greedy action depends only on the observed block. This is pointwise optimal
even among microscopic/history policies, although the block process need not
be Markov. Subsequent LPs have only r variables and mr constraints; ordinary
polynomial LP and exact/interval receiving must be paid, not assumed as an
unbounded oracle. For an initial law uW the value is u R(g+y*).

The tempting reduced FIXED-POINT iteration need not be contractive: D_a is
signed and R can have norm 1/(1-gamma). The LP, not an asserted inherited
contraction, is the proposed efficient consumer.

## Honest acquisition opening

(1-gamma)R is stochastic: sample a uniform microscopic state from each acquired
block, run BASELINE A0 until an independent geometric stopping time
Pr(T=t)=(1-gamma)gamma^t, and retain the final block. The expected number of
actual transitions per episode is gamma/(1-gamma). Thus baseline successor
features are acquired by an ordinary real forward interface, without learning
all n^2 entries. Nonnegative row data can be retained by every comparator.
Discovery of Z and acquisition/validation of D_a remain substantial costs.
The contrastive theorem is a possible class-specific proposal, not yet a cheap
end-to-end mechanism or a statistical certificate of this exact factorization.
All failures, finite-time truncation, confidence, finite precision, LP condition
sensitivity and adaptive goal receiving remain open construction obligations.

The key hard step is an APPROXIMATE version that can be checked from finite
observations without entrywise learning and without assuming low norm of the
common background. It must prove a uniform near-optimal policy guarantee for
all admitted goals, not just certify baseline values. A residual check restricted
to the acquired resolvent feature space may suffice, but is not proved here.

## Strong comparators and prior work to examine first

Ordinary successor representation/features, generalized policy improvement,
value equivalence, exact/approximate linear programming and linear successor
feature models get the same partition, difference data, geometric episodes,
retained R and precision. A single-baseline successor representation does not
by itself prove optimality after arbitrary policy changes, but the present LP
may already be a known specialization of those theories. Do not infer novelty
from absence in an initial search or exclusive advantage by withholding R.

Primary starting points inspected only at search/abstract level in this pass:
- de Farias/Van Roy approximate LP and generalized reduced LP:
  https://arxiv.org/abs/1409.3536
- Low-rank MDP representation acquisition (different full-kernel assumption):
  https://papers.neurips.cc/paper_files/paper/2020/hash/e894d787e2fd6c133af47140aa156f00-Abstract.html
- Basis refinement/value-function spaces:
  https://www.cs.mcgill.ca/~prakash/Pubs/nips2015.pdf

This page is a concise future foothold, not a reviewed theorem/package. The
accepted contrastive freeze and all older archives remain unchanged.

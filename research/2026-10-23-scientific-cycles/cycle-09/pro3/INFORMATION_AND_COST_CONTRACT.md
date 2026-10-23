# Information and cost contract

## Unchanged native class

The theorem fixes K>0 and alpha in (0,1), with beta=1-alpha. Each horizon
has public finite A>=0,0<eta<1,kappa>=0. The target and proposal are positive
on a finite labelled space with one supplied population D(pi||q)<=K.
Q is target-independent, row-stochastic and reciprocal, with actual maximum
edge log asymmetry bounded by A. Every kernel and policy is fixed during
the run; support may grow across instances and horizons. Initialization is q.

Local acceptance is exactly
min(1,(q_y/q_x)^eta(Q_yx/Q_xy)^kappa)
times min(1,(pi_y Q_yx/(pi_x Q_xy))/S_xy).
The actual rejection diagonal and C=(I+alpha G+beta L)/2 are retained.
The theorem controls the original full-chain TV, half l1.

## Available information and charged operations

The sampler may draw from q, evaluate q, draw a native Q proposal, and evaluate
both required directed proposal probabilities at their actual costs. Ratios
of unnormalized target evaluations suffice; the normalizer is not supplied
free. Full caching is permitted, with lookup, storage and precision charged.
The population K and the full-edge A promise are input assumptions, not
estimated from sampled evaluations, training losses or visited edges.

The proof can describe normalized tables and geometric labels. That does not
give the operational sampler a free full target table or an index oracle.
When an actual recipient has an analytic target formula or complete finite
table, direct sampling or enumeration remains legitimate. No information
is artificially suppressed to favor the hybrid.

An actual C step chooses identity, G, or L with probabilities1/2,alpha/2,
beta/2. A global attempt uses a q proposal and the required target/q ratios;
a local attempt uses Q and its forward/reverse probabilities. Rejections and
holds count. No deterministic horizon is replaced by an optional attempt
count or its expectation.

## Proof operations are not access privileges

The absorbed first-hit process is a mathematical counter with killed mass,
not a normalized conditional simulator. Every upper first hit is propagated
by the original C for its remaining time. The lower selects a subset of
actual trajectories and retains the whole terminal union. Global moves
within levels and the terminal union count as actual holds/movement.
Discarding unselected trajectories from a lower bound does not delete them
from the chain.

The level quotient has a proved native lumping map. It represents a law and
a verification calculation. It is not an assumption that a sampler can
execute one enormous native proposal or target call for the cost of a small
quotient step.

## Size and exact-real boundary

The new tree has 1+sum_{i=0}^J M^i native states. Up to
J ceil(log2 M)+O(log J) label bits are needed. Its atom magnitudes involve
J(V+log M) for q and 2J log n+J log M+4loglog n for pi. Implicit generation
avoids listing the full graph but retains those label and precision costs.
Computing exp(A), an exact ceiling, arbitrary real powers and very small
probabilities can require unbounded precision. No uniform finite-word
implementation or floating-point instability is asserted.

The public asymmetry bound is a property of exact Q, not an error budget for
approximate reverse-proposal evaluation. Such a precision interpretation
would require a separate computational error model and actual operation costs.

## Comparison and exclusions

Pure IMH uses the same pi,q,K and natural access. Its minimax amplitude K
and same-input O((log n)^-4) bound remain visible. Deterministic j/n->t>0
comparisons are distributional comparisons, not equal wall time, target
calls, memory or arithmetic precision. No end-to-end speed claim is made.

The theorem excludes within-run adaptation, deterministic LG/GL scheduling,
nonreversible target kernels, noisy/unbiased target estimators, empirical KL
certification, free full tables, fixed-support refinements and finite-arithmetic
acceptance errors. Its logarithmic equivalent does not assert a critical
amplitude. Historical originality and external acceptance remain unknown.

All measured Python times/RSS are in RESOURCE_RECEIPTS.json. Total inference,
token, design and discovery costs are unavailable. No spending, paid compute,
hardware, outreach, public disclosure or permission change occurred.

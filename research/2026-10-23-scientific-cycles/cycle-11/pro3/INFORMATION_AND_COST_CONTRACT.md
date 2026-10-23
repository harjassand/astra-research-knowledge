# Information, operations and costs

The native sampler contract is unchanged from the exact predecessor:
finite labelled positive pi,q; one population D(pi||q)<=K>0; fixed alpha;
q initialization; target-independent reciprocal row-stochastic Q under
the public asymmetry promise; fixed-within-run eta,kappa and actual
two-stage Hastings correction. Supports and policies may vary between
horizons, not within a run.

The sampler can draw from q, propose from Q, evaluate the q values and
forward/reverse Q probabilities required by its acceptance rule, evaluate
the target up to an unknown common normalizer and use its actual caches
and random uniforms. It receives no free normalizer, complete target table,
proposal-label oracle, population-KL estimator, inverse index, arbitrary
precision or absorbed simulator.

The new labels, reverse reference matrix and clipped-progress process are
proof representations. They are not observed by the sampler and do not
change C. All actual diagonal stays, rejection decisions, global moves,
local reversals and later returns are retained in the full-law theorem.
The deterministic N in the proof is a fixed analytical cutoff, not an
optional number of proposals substituted into a fixed-time formula.

The wider theorem for S=r_q^eta exp(xi) explicitly adds a fixed,
target-independent antisymmetric edge function xi with |xi|<=d to the
mathematical class. Its representation and evaluation cost must be paid.
Antisymmetry is necessary for the stated simple target-reversibility
argument. This is not permission to corrupt the target, independently
perturb forward/reverse values or adapt the screen during a run.

Native actions, target and proposal evaluations, forward/reverse
probabilities, random sampling, support preparation, labels, indexing,
memory, caching and precision retain their real costs. The huge support
of an asymptotic native witness is not free because a quotient can be
analyzed on paper. There is no useful implementation claim here.

The new exact rational diagnostic is a four-state original kernel at
N=5 with K=24 certified before evaluation. It tests path identities and
event containment; it does not estimate the critical law. The historical
admitted and failed fixtures remain frozen and are not rerun.

Observed diagnostic and figure resources are recorded separately.
Inference, token, design, total discovery and useful-implementation costs
are unknown. No purchases, paid compute, hardware operations, external
outreach, public hosting or visibility/access changes were performed.

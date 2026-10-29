# Primary sources inspected and useful failures

29 October 2026. Source search and abstract inspection, not an exhaustive
priority determination.

## Sources actually retrieved

1. Peter Buchholz, Exact and ordinary lumpability in finite Markov chains,
   Journal of Applied Probability31(1),59--75,1994.
   DOI https://doi.org/10.2307/3215235 . The Cambridge result explicitly says
   it extends lumpability to near lumpability and gives aggregation bounds.
   Search-returned publication date2016 is the online-host date, not1994.
2. Gaoang Bian and Alessandro Abate, On the Relationship between Bisimulation
   and Trace Equivalence in an Approximate Probabilistic Context, arXiv
   https://arxiv.org/abs/1701.04547 , v3 dated27 April2017. Abstract read.
   Pointwise approximate bisimulation implies a tight finite-trace TV bound;
   finite and uncountable state spaces are covered.
3. Fabian Michel and Markus Siegle, Formal Error Bounds for the State Space
   Reduction of Markov Chains, https://arxiv.org/abs/2403.07618 , v3 dated
   6 August2024. Abstract read. Bounds increment of transient-distribution
   error in discrete time and derivative in continuous time, compares several
   lumpability/aggregation notions. Related publication DOI
   https://doi.org/10.1016/j.peva.2024.102464 .
4. J. Tian and D. Kannan, Lumpability and Commutativity of Markov Processes,
   https://people.nmsu.edu/jtian/publications/2006-3.pdf . Search-extracted
   theorem2.3 states the Kemeny--Snell constant block-row-sum criterion.

## Useful failed/simple routes

A. The KL chain-rule route directly using actual hidden occupancy needs a
   density or occupancy contract. Per-call equilibrium L2 residual alone does
   not license replacing adaptive deployment occupancy by equilibrium.
   With a coarse transition floor tau and occupancy bound B_t it gives an
   ordinary sum_t B_t residual_energy/tau bound. General feedback can inflate
   B_t, so this is not automatically an improvement.
B. Replacing T by PTP is positive, but changes hidden transitions drastically
   even at zero visible leakage. Comparing full hidden paths to PTP would
   therefore lose the exact zero-defect limit. This led to repairing only
   flux marginals while retaining as much microscopic flow as possible.
C. The repaired kernel is not assumed implementable. It can add transitions
   across forbidden supports and mix frozen variables. It serves only as a
   positive mathematical comparison process. A claim that it is a physical
   reset or actuator would be false without additional access.
D. The L1-to-L2 step loses a square root. It is valid but may be quantitatively
   poor. No lower bound proving optimality of sqrt(nDelta) is supplied.
E. The proof needs a positive partition projection. An arbitrary small-rank
   future-feature space does not have this property; no result here turns it
   into a finite positive realization for free.
F. The exact fixture tests population matrices, not samples. It verifies all
   depth3 feedback policies and all record events, not all depths. The depth40
   comparison is evaluation of a proven certificate, not enumeration.

## Root-mechanism challenge supplied

For a fixed hidden variable H and conditional visible Markov kernels, marginal
H density control can replace the entire retained-history cardinality cost:
compare joint(H,Z,Y0,record) laws sharing initial distribution, apply KL chain
rule, and bound history-selected nonnegative residual costs by a sum over the
finite macro/label menu. H never changes, so its unconditional marginal never
changes even under feedback. Merely assuming each operation preserves H's
stationary marginal is insufficient; if H evolves, feedback can move its
actual distribution. Exact compiled output rows do not need to be reversible,
but preparation toward a specific pi requires the compiled matrix preserve pi.

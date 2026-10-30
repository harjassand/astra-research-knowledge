# A second exact consequence of real onsite regeneration

2026-10-29. New, unreviewed. This note proves simultaneous projector bounds, not an all-record coherent memory theorem.

Let Q_h be the full-Hilbert forest-frame good-history projector for owner h, and B_h=I-Q_h. These are controller-only. Nominal no-creation, including each resolved instrument Kraus, implies L0*(B_h)<=0. One way to see this is that a CPTP semigroup preserving Q_h has 0<=E_t*(B_h)<=B_h; differentiate at zero.

Add the actual unconditional complete hub replacement of ONSITE_RESET_CUSHION.md at rate mu. Its output is good for h regardless of locks and workspace, so its adjoint contribution on B_h is exactly -mu B_h. Replacements at other hubs preserve h's good sector and give nonpositive contributions. Suppose added continuous local perturbations satisfy an incident adjoint-norm budget eta on B_h's support. Then

    L*(B_h) <= -mu B_h + eta I.

This inequality is uniform in the quantum state, including an arbitrary retained bath. Integrating the CP comparison gives

    E_t*(B_h) <= exp(-mu t) B_h
                   + (eta/mu)(1-exp(-mu t)) I.

In particular, a good initial h has bad probability at most eta/mu at every time, without any independence assumption.

For a buffered set S such that every nominal or perturbation term meets at most one of the disjoint B_h supports, put B_S=product_h B_h. The exact local product rule and commuting complementary positive factors give

    L*(B_S) <= -mu |S| B_S + eta sum_(h in S) B_(S minus {h}).

The same inequality holds for time-dependent perturbations with the uniform budget. With every selected h initially good, induction through the scalar differential inequalities yields

    Tr[B_S rho(t)] <= [(eta/mu)(1-exp(-mu t))]^|S|.

For arbitrary initial input the completely bounded operator version is

    E_t*(B_S) <= [exp(-mu t)+(eta/mu)(1-exp(-mu t))]^|S| I.

For example, prove the latter by induction on |S| using the variation-of-constants formula and the binomial differential identity. The former follows by the same expectation recursion and the zero initial values for every nonempty subset.

Consequently inserting the simultaneous orthogonal projector B_S at time t in a Stinespring evolution has amplitude norm bounded by the square root of the corresponding UNIFORM operator bound. For a fixed initially good system subspace, use the good-input bound restricted to that subspace, with arbitrary reference and bath. This is not a positive interpretation of arbitrary Pauli branches.

## Limits that matter

1. Coloring/packing must include the actual noise support hypergraph. A support-cardinality bound alone does not guarantee a fixed coloring.
2. The inequality is for simultaneous selected projectors. Several nearly identical times cannot be counted as independent tests. Multiple-time terminal instruments need their own chronological proof and reset bookkeeping.
3. Actual terminal source selection can correlate with B_h. Replacing its probability by an independent reset rate is not justified; bounded-intensity integrals may be used only with the full unnormalized instrument.
4. Good-sector continuous perturbations Q_h K_e Q_h can directly act on DATA and are not detected by B_h. They remain genuine coherent fault locations.
5. Summing unselected good/bad projector choices at amplitude level restores the original Stinespring operator. Measuring and then discarding all those flags generally does NOT restore the original coherent evolution. Inclusive fault-mask manipulations must respect this distinction.
6. This result controls controller goodness under the physically regularized generator. It is not the missing complete linked-cluster/SSF composition theorem.

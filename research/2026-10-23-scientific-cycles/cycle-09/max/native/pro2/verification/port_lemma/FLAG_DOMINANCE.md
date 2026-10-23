# Flag dominance: a sound simulation, not exact-state equality

Focused independent addendum, Cycle8 PRO2, 22 October 2026. This uses the exact
S/P/U interface and the proved SAT4 quotient. No experiment or family search
is performed here.

## Preorder

The base of a projected two-port profile consists of its SAT4 positions and,
for each active port, the actual terminal color and the entire neighbor-color
count vector. Write sigma <= tau when the bases agree literally and every
active far-end flag of sigma is at most the corresponding flag of tau. SAT4
has no flags. Thus sigma has no more flagged incident color classes than tau,
while all actual colors, counts and degree budgets visible to a context agree.

The relation refers to actual fixed labels. For color orbits, domination means
that some explicit permutation of the four labels aligns the bases and gives
the flag inclusion. Merely forgetting correspondence between count coordinates
and colors is unsound. Comparing only a single canonical full-state
representative with literal equal bases may conservatively miss domination
when the base has color symmetries; it does not justify asserting that no
orbit domination exists.

## Transition simulation theorem

Suppose an admitted S/P/U transition accepts child profiles tau_i. Replace
each with a realizable sigma_i <= tau_i and use the same operation and, for
U, the same new-terminal color. The transition still accepts. Its output
sigma satisfies sigma <= tau, where tau was the original output.

For S, the joined colors and count sums are unchanged. Every bad-edge
rejection has the form summed_count>=2 AND (F_1 OR F_2). Reducing flags cannot
turn an accepted condition into a rejection. The output inherits the outer
records, so their flags only decrease. For P, the same argument applies at
both ports, and componentwise OR is monotone. Any newly saturated output
is projected to the same SAT4 marker because its degree depends on counts,
which agree. For U, properness and its degree cap depend only on the base.
The condition F(A)=0 stays true when flags decrease. The new port's flag is
[n(A)>0], identical in the two outputs; flags at the opposite active port
only decrease. This proves the theorem.

Induction on a finite continuation gives contextual simulation at arbitrary
depth: every accepted completion of tau is also accepted after replacement
by sigma, with the same visible color/count decisions and possibly smaller
remaining flags. This is not equality of attainable exact signatures.

## Complete attainable sets: safe antichain pruning

Let T be the complete set of projected signatures actually attainable on a
particular module. A retained set R is a realized downward cover when

    R is a subset of T, and
    for every t in T there exists r in R with r <= t.       (1)

Deleting a profile dominated by another retained realized profile preserves
(1). A finite antichain of minimal elements is one possible cover; keeping
additional states is harmless.

Suppose child sets R_i are realized downward covers of their complete
attainable sets T_i. Every valid exact transition using t_i in T_i is
simulated by suitable r_i <= t_i, by the theorem. Therefore the transition
outputs from R_i cover all exact outputs from T_i downward. Every retained
output is itself an actual coloring signature because it came from actual
child realizations and an exact accepted transition. Pruning outputs again
under (1) preserves both facts. Induction proves that this exact propagation
with dominance pruning preserves nonemptiness for every finite input
expression, without preserving the complete exact-signature set.

Thus an empty result is a genuine graph noncolorability certificate only if
this contextual completeness invariant has been maintained: complete leaf
coverage, all admitted operations/choices, exact degree constraints, and a
realized dominating representative for every pruned profile. A truncated
search, a smaller sufficient family, or an unrecorded pruning rule does not
inherit that conclusion.

## Sufficient guarantee families: downward realization semantics

A family F may instead mean the following guarantee for a module:

    for every requested target f in F, some actual profile sigma <= f
    is realized on that module.                            (2)

Counts and visible colors in (2) are still exact; only flags are upper bounds.
If A covers B in the sense that every b in B has some a in A with a <= b,
then a module satisfying (2) for A also satisfies it for B, by transitivity.
This is the correct direction of family coverage.

A closed family construction can use witnesses as follows. For every parent
target b, choose child target profiles from their guaranteed families such
that the abstract transition accepts and its computed output a satisfies
a <= b. The actual child realizations may have smaller flags. Transition
simulation proves that the actual parent realization also has profile <= b.
This supplies an all-depth induction when all admitted family/operation cases
are explicitly covered and the leaf guarantees are realized. Require each
claimed existence family to be nonempty; an empty family has a vacuous
universal guarantee and supplies no coloring.

For executable reconstruction, witnesses must be interpreted using (2), not
as equality promises. The reconstructed child's actual flags may be lower
than its requested target. Its visible counts and colors must agree exactly,
and its actual flags must be verified as subsets. Propagate this invariant
through the witnesses or check the resulting actual graph coloring directly,
while retaining the all-depth argument. Color-permutation witnesses must
record consistent label alignments. SAT4 remains existentially uncolored
until the introduction step described in SATURATION_QUOTIENT.md.

Failure to cover one of these sufficient families still rejects only that
family template. It becomes a graph obstruction only under the separate
complete-set invariant (1).

## Scope and cost

The proof uses the exact count/flag transition formulas, nonadjacent terminals,
disjoint children, positive actual terminal loads and degree cap four. It does
not apply to contexts demanding exact far-end flags, imposed hidden saturated
colors, arbitrary overlapping pieces, or general acyclic mass signatures.
No all-size star-four existence result follows from monotonicity alone.
No new enumeration was performed; reasoning and authoring costs are unknown.

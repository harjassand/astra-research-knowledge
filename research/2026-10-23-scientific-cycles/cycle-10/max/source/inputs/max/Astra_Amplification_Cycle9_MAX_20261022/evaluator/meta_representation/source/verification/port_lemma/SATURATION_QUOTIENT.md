# Saturated-port projection is lossless for the admitted context language

Focused independent addendum, Cycle8 PRO2, 22 October 2026. Requested after the
exact higher-load S/P/U interface lemma. No universal family search is performed
here. The result below concerns information retained by an interface; it does
not establish a star-four coloring for every uncolored expression.

## 1. Setting and quotient

Use the exact module and star-signature contract of PROOF.md: distinct,
nonadjacent terminals, disjoint child occurrences, positive terminal degrees,
all vertex degrees at most four, four colors. Allowed operations are ordinary
series S, ordinary parallel P, and a one-sided terminal extension U_L/U_R by
one fresh leaf. Every identification pays the actual combined degree budget.
Only graph-admissible operations are considered.

The full signature is (R_s,R_t), with R_v=(a_v,n_v,F_v). Call a terminal
*saturated* when its actual degree is four. Define

    pi(R_v) = R_v       if 1 <= deg(v) <= 3,
    pi(R_v) = SAT4      if deg(v) = 4.

The marker contains neither the terminal color nor its neighbor counts or
far-end flags. It does retain the exact load four. Apply pi componentwise.

**Theorem.** On star-realizable signatures, pi is an exact quotient of the
partial S/P/U transition algebra. The projected output state and transition
admissibility are determined by the projected child states and the chosen
extension color, with the formulas below. Therefore exact attainable projected
state sets can be propagated without retaining any saturated-port record.
No information relevant to any future admitted context is lost.

This is an existential boundary theorem. A marker does not promise that its
terminal can be assigned an arbitrary externally requested color.

## 2. Why saturated ports cannot become active again

Every other port has positive degree. Identifying a degree-four terminal with
another terminal would create degree at least five; this is forbidden. Thus a
SAT4 port cannot be a joined port of S and cannot occur in either port position
of a child of P. Extending that terminal by U adds an edge and also exceeds
the degree cap. The only permitted subsequent uses are:

* it persists as an outer terminal of a series composition at the other port;
* it persists as the opposite terminal of a one-sided extension.

Its physical vertex, degree, incident edges, and all of its neighbors' colored
adjacency lists are unchanged by those operations. To see the last assertion,
a neighbor of the saturated terminal cannot be the other terminal, by
nonadjacency. The only vertex whose adjacency list changes under S or U is the
other terminal. An interior common neighbor of both terminals merely retains
the old terminal, possibly renamed, with the same color. It gains no neighbor
and loses no neighbor.

Consequently neither star validity at a saturated port nor any of its original
far-end flags can change in a future admissible context. Its record can never
be consulted by a legal merge or extension condition.

## 3. Exact projected transitions

### Series

For projected children (L1,R1),(L2,R2), the joined ports R1,L2 must both be
active full records. Require their terminal colors to match, their degree sum
to be at most four, and the exact count/flag merge test from PROOF.md. The
output is simply (L1,R2), including any inherited SAT4 marker.

The joined vertex may itself reach degree four, but is now internal. Its star
validity was checked before it was forgotten. No outer port newly reaches
load four in a series operation.

### Parallel

Both ports of every child must be active: even one SAT4 child port would make
the combined load exceed four. Full input records are therefore present on
both sides. Apply both exact full-record merge tests, calculate both full
merged records, and **only then** apply pi to each output port.

In particular, a port newly reaching degree four is checked with its actual
color, full counts and flags at this step. Projection must not be used to
skip the saturation-producing validity test.

### One-sided extension

The extended port must be active and hence its entire full record is known.
For a chosen new-leaf color A, apply the exact rule A!=a and F(A)=0; the old
port degree is at most three. Compute the new degree-one record as in
PROOF.md. Keep the opposite record or SAT4 marker unchanged. The old port
may become an internal degree-four vertex, whose validity was checked by
that exact extension rule.

## 4. Proof of exactness and contextuality

Take two full realizing child signatures with the same projected signatures.
For S, the only transition tests concern the joined ports. They must be active,
so their full records agree between the realizations. All tests therefore have
the same outcome. The output's visible active records are the unchanged outer
records; a hidden saturated outer record remains SAT4 regardless of its
particular realization.

For P, no input port can be saturated. The full input signatures are known,
so both the acceptance decision and the projected output agree exactly.
For U, the affected port is active and known; the opposite projected record is
unchanged. Again acceptance and projected output agree.

These observations prove that each operation descends to a well-defined
partial transition on projected states. They prove more than a sufficient
rule: whenever the projected transition is admitted, **every** choice of
realizing full child signatures with those projections can be glued using
the specified visible colors, because the full transition tests depend only
on the retained records. Conversely a star-colored output restricts to
realizing child states satisfying those same tests.

Induction on any finite expression context now proves contextuality. Replacing
a child state by another realizing state with the same projection never
changes future projected transitions or realizability of their outputs. The
induction has no depth bound. At a complete root, a projected state is
attainable if and only if at least one full star coloring realizes it. Thus
emptiness of a **complete** projected attainable-state set is an actual
noncolorability statement. Emptiness in a smaller sufficient guarantee family
still has only its original template-specific meaning.

No remote bichromatic connectivity information is needed because the local
bad-edge criterion characterizes star coloring exactly. This addendum does
not claim the analogous quotient for general acyclic bounded-mass colorings.

## 5. Reconstruction and color symmetry

Projected witnesses suffice for recursive construction, but a SAT4 marker
must be treated as an unresolved actual color, never as a fifth palette color
or an arbitrary prescribed one. Propagate its physical terminal vertex identity
through S and opposite-side U. Leave its color unspecified until reaching the
transition at which it became saturated, or a stored realizing leaf module.

At a saturation-producing P, all incoming ports are active. The witness gives
an actual common terminal color, so that step assigns the color of the marked
parent vertex consistently to its child occurrences. Child witnesses then
continue with actual colors. If the marker originated in a supplied leaf,
that leaf needs a stored full realizing coloring. Under path leaves and S/P/U,
all terminal saturation is introduced by P and therefore has such a concrete
step.

If both root ports are SAT4, neither is assigned a color until its own introducing
transition is reached. This is harmless because all ancestor uses merely
propagate those distinct vertices; no legal operation compares their hidden
colors. If a shared physical vertex obtains a visible color from a more
specific witness, normal equality checks should enforce that assignment.

Every permutation of the four colors commutes with pi and all projected
transitions. Canonicalization may ignore hidden colors. A bijection prescribed
on the visible colors extends to a permutation of the whole four-color palette;
apply such an extension to the entire stored realization, including its hidden
colors. Consequently color-orbit witnesses remain valid without retaining an
otherwise unused saturated-terminal color.

## 6. Scope and counterfactual failures

This quotient is invalid for a language which later imposes the color of a
saturated terminal, compares its color with another marker, recolors existing
vertices, or attaches a new external edge despite the degree cap. It is also
not justified for adjacent terminals: extending the opposite port could then
change the far-end repeat condition of an edge incident to the saturated port.
Such cases need additional data and different transition formulas.

Positive terminal loads are part of the theorem. Allowing zero-load ports
would make some formal merges with a saturated port degree-admissible; their
color-compatibility rules would need separate treatment. Shared child interiors
are excluded for the same reasons as in the full interface lemma.

For fixed terminal color, active degree-one/two/three records have respectively
6,15,23 syntactically valid choices. Thus there are at most 4*(6+15+23)=176
labeled active records plus one SAT4 marker, and at most 177^2=31329 labeled
projected two-port states before realizability or color symmetry. This reduction
is genuine but does not bound the number of complete reachable state sets or
prove that a practical universal family closure will finish.

## 7. Resource record

This is a deductive addendum using the independently proved full interface.
No new enumeration or closure search was performed by this reviewer. Total
reasoning/authoring cost is unknown. The main search must retain actual costs
for constructing its projected tables, failed attempts and any independent
certificate verification.

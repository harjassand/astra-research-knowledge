# Exact support/degree quotient and support-dominance simulation

Focused independent addendum, Cycle8 PRO2, 22 October 2026. This is a further
proved change of boundary representation. Actual neighbor multiplicities
remain properties of each realizing graph/coloring and are still checked
there. They are not replaced by a different graph, action oracle, resource
bound, or matrix class.

## 1. Exact quotient of already valid child states

Start from the full exact port record R=(a,n,F) in PROOF.md, where a is the
terminal color, n(c) is its actual number of neighbors of color c, and F(c)
is the OR of the far-end repeat flags on those edges. The module coloring
is already star-valid. Replace that record by

    Q(R) = (a,d,N,F),
    d = sum_c n(c),
    N = {c:n(c)>0}.

Here d is the exact actual terminal degree. F is a set of colors, a subset
of N. A proper realizing coloring has a not in N. The color and exact
degree remain; only the per-color multiplicities are projected out. One may
then replace degree-four ports by SAT4 using SATURATION_QUOTIENT.md.

**Theorem 1.** On star-realizable signatures under the nonadjacent-terminal,
disjoint-child, positive-load S/P/U grammar and degree cap four, this is an
exact transition congruence. It determines acceptance and the compressed
output independently of the forgotten per-color multiplicities.

## 2. Exact merge rule

For ports (a1,d1,N1,F1),(a2,d2,N2,F2), require a1=a2 and d1+d2<=4. Then the
ordinary merge is star-admissible exactly when

    N1 intersect N2 intersect (F1 union F2) is empty.        (1)

The output record is

    (a1, d1+d2, N1 union N2, F1 union F2).                  (2)

To prove (1), consider any color c. If it appears on both sides, the actual
combined multiplicity is at least two, regardless of its exact numerical
value. A bad incident edge is then created exactly when c belongs to
F1 union F2. If c appears on only one side, its actual multiplicity and all
its far-end flags are unchanged from that child. Those were already safe
because the child was star-valid. If c appears nowhere, there is no edge
in that color. These exhaustive cases prove (1). Equation (2) records the
actual degree sum, actual neighbor-color support, and actual OR flags.

The disjointness and nonadjacency hypotheses ensure the child neighbor sets
at a merged port are disjoint, so these are actual degree sums; no duplicate
neighbor or edge has silently been counted twice. Internal common neighbors
of the two terminals of one child cause no problem: the two terminal
vertices remain distinct, retain their colors, and every such interior
neighbor retains its color-labelled adjacency list. This is the same
load-bearing fact proved for the full interface.

For binary series, test only the two joined active ports and retain the outer
compressed records. For parallel, test both terminal pairs and use (2) at
each end. If an output reaches degree four, check (1) first and only then
project to SAT4. Higher arities can be processed in binary order; once a
repetition violates (1), adding more children cannot repair it.

## 3. One-sided terminal extension

Let (a,d,N,F) be the port being extended. Require d<=3. Giving the new leaf
color A is admissible exactly when

    A!=a and A not in F.                                  (3)

The new port record is

    (A,1,{a},{a} if A in N else empty).                    (4)

Only membership A in N is needed to decide whether the old terminal has an
old neighbor of the new leaf's color. The opposite port record is unchanged.
The full-interface proof already establishes that neither a shared interior
neighbor nor the opposite nonadjacent terminal acquires a changed adjacency
list. Thus (3)-(4) are exact compressed formulas.

## 4. Restriction, realizability and all-depth meaning

Every output star coloring restricts to star colorings of its child copies.
Their actual multiplicities yield compressed child records satisfying the
rules above. Conversely, choose any actual star-valid child realizations
with the stated compressed records. The proof of (1) uses only those
records, so it accepts or rejects identically for every choice of their
forgotten multiplicities. Accepted children glue to an actual star coloring,
and (2)-(4) give its actual compressed output record. This proves both
inclusions for complete attainable compressed state sets and contextual
congruence at arbitrary finite depth.

Already-valid children are an essential premise. A record with degree three,
support {1,2} and flag {1} could describe counts n(1)=1,n(2)=2 in a valid
port, but counts n(1)=2,n(2)=1 with the same flag would already be invalid.
The quotient does not license the latter. It identifies actual valid
realizations; it does not turn syntactic bit patterns into a proof of star
coloring. Leaves require actual realizing colorings and each composing
transition preserves their validity.

At final reconstruction, obtain colors on the actual expanded graph, compute
all actual per-color neighbor counts, and check the original bad-edge
criterion. No equality with a formerly requested numerical count vector is
promised: that vector is no longer part of the quotient. The exact degrees,
realized support and flags, and original graph/action data retain their stated
roles. This is lossless for the admitted continuation language, not for a
context that asks for particular per-color multiplicities.

## 5. Further support-and-flag dominance

On the compressed profiles, hold fixed the active terminal colors, exact
total degrees and SAT4 positions. Define sigma <= tau when, at every active
port,

    N_sigma is a subset of N_tau,
    F_sigma is a subset of F_tau.                         (5)

**Theorem 2.** Replacing already realizing child profiles by smaller profiles
in (5) preserves every accepted S/P/U continuation and yields an output
smaller in (5). This is an existential simulation; it is not exact-state or
exact-support equality.

The merge rejection set in (1) is monotone in every N and F argument.
Reducing any supports or flags cannot turn an empty rejection set into a
nonempty one. Its output unions are likewise monotone; exact total degrees
and color-compatibility tests are unchanged. Series retains the outer
profiles. In U, condition (3) remains true when F decreases, the singleton
new neighbor support in (4) is unchanged, and the new flag can only decrease
when N decreases. The opposite profile is inherited. Saturation occurs at
the same actual degree and gives the same marker. These facts prove the
one-step simulation; induction proves it for any finite admitted context.

A smaller neighbor support at fixed degree may concentrate more edges in
one color. This is safe here precisely because the substituted child is an
actual **star-valid** realization. Its more repeated colors already have
zero far-end flags. Formula (1) proves that no other numerical count effect
can become relevant in a later join. It would be unsound to infer validity
from support inclusion without that realizing-child premise.

## 6. Complete pruning versus sufficient family guarantees

The completeness and family arguments of FLAG_DOMINANCE.md extend verbatim
with preorder (5):

* For complete attainable sets, retain actual realizing profiles which
  downward-cover every removed profile. Every exact continuation is simulated
  by a retained choice, so exact propagation plus this pruning preserves
  nonemptiness. Genuine graph noncolorability from an empty result requires
  complete leaf coverage, every admissible transition/choice and a valid
  domination justification for every discarded state.
* A sufficient family target now promises exact visible terminal colors and
  exact degrees, with **upper bounds** on neighbor-color support and far-end
  flags. For every target, some actual realization must satisfy (5). Its
  actual per-color multiplicities are not prescribed. If family A supplies
  such a realization below every target of B, an A guarantee implies the B
  guarantee. Nonempty families and explicit transition witnesses are needed
  for an existence theorem. A failed family template is still not a graph
  obstruction.

Every comparison must use a single consistent four-color relabeling across
both active ports. Supports and flags at one port cannot be independently
permuted while the other is held fixed. Color-orbit canonicalization and
pruning need explicit global alignment witnesses, or an exact enumeration
of the relevant four-color permutations. SAT4 colors remain existentially
unspecified as in the saturation addendum.

For reconstruction from upper-bound targets, verify the actual degrees and
terminal colors exactly, and the actual supports and flags as subsets of
the requested bounds. Do not mistakenly require old count-vector equality.
The resulting complete graph must still pass properness and the exact
multiplicity-based star test, and the full original actions are used by the
unchanged inverse.

## 7. Finite alphabet and limits

For a fixed terminal color, a locally possible compressed record of degree d
has 1<=|N|<=min(3,d), F subset N, and if d>|N| then F must be a proper subset
of N (some color must carry the extra multiplicity and cannot be flagged).
There are respectively 6,15,20,19 such records at degrees 1,2,3,4. These are
only port-local possibilities, not an assertion of whole-module realizability.
With SAT4, active records number 4*(6+15+20)=164, plus one marker. The
syntactic projected pair alphabet is at most 165^2=27225 labeled states.

Neither this finite alphabet nor the simulation theorem proves that a
nonempty universal guarantee-family closure exists or is computationally
cheap. No conclusion about arbitrary-real four-query recovery follows from
a star-family failure. The grammar restrictions and original inverse/error
contract remain unchanged.

No new enumeration or closure experiment was performed for this deductive
addendum. Reasoning and authoring costs remain unknown.

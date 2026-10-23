# Exact terminal signatures for star coloring under series and stubbed parallel composition

Independent bounded interface check for Cycle7 PRO2. This note proves only
compositional exactness of the proposed state. It does not assert that every
grammar expression has a nonempty set of four-color states, nor supply the
owner's all-depth closure or reconstruction theorem.

## Hypotheses and state

A module is a finite simple graph with two distinct, nonadjacent ordered
terminals s,t, each of degree one. Its coloring is proper and star: no path on
four distinct vertices is bichromatic. Different children have disjoint vertex
sets before the explicitly specified terminal identifications. Let u_s and
u_t be the unique terminal neighbors. They may coincide, as on path2.

For any finite palette, use the signature

    (a,b,p,q,f,g)

where a=c(s), b=c(t), p=c(u_s), q=c(u_t), and

    f = [u_s has a neighbor other than s of color a],
    g = [u_t has a neighbor other than t of color b].

Thus a!=p and b!=q. Equal terminal colors are permitted; their actual
constraints remain represented by the attainable states. Flags are Boolean
existence statements, not counts. No terminal-neighbor identity flag or
distance information is needed for the two productions below.

## Local star criterion

In a proper colored graph, call an edge uv bad if u has another neighbor
u' of color c(v), and v has another neighbor v' of color c(u).
Then the coloring is star if and only if it has no bad edge.

Indeed, a bichromatic path u'-u-v-v' has a bad middle edge. Conversely, the
two witnesses to a bad edge form such a path. The four vertices are distinct:
the witnesses are other neighbors, and u'=v' is impossible because properness
gives c(u)!=c(v), whereas that common vertex would need both colors.

## Exact series transition

Take signatures sigma1=(a1,b1,p1,q1,f1,g1) and
sigma2=(a2,b2,p2,q2,f2,g2), with b1=a2, and identify t1=s2=w.
The union is star exactly when

    NOT (q1=p2 AND (g1 OR f2)).                         (S)

When admitted, its outer-terminal signature is exactly

    (a1,b2,p1,q2,f1,g2).                              (S-out)

Proof. Only the identified vertex w gains neighbors. Its two neighbors are
distinct, because the child interiors are disjoint and the terminals were
nonadjacent. Every edge not incident with w has unchanged endpoint colors and
unchanged neighbor-color multiplicities. For w-u_t1, the flag at the far end
is g1; the new flag at w is [q1=p2]. The other new junction edge similarly
uses f2 and the same equality. This proves (S).

The neighbors of the outer terminals are not w: that would contradict the
nonadjacency of the terminals in the relevant child. Their adjacency lists
have the same neighbor colors after the identification. This remains true
when a child's two terminal neighbors coincide. Consequently their flags
remain f1,g2, giving (S-out). The output terminals remain distinct,
nonadjacent and of degree one.

## Exact stubbed parallel transition

Take b children, each with signature

    (C,D,p_i,q_i,f_i,g_i).

Identify their left terminals at a and their right terminals at z. Keep a,z
distinct. Add fresh outer terminals s,t and stub edges sa,zt, with colors
A,B respectively. Require A!=C and B!=D for properness. The union is star
exactly when every child i satisfies

    NOT [ f_i AND (p_i=A OR exists j!=i: p_j=p_i) ],    (P-left)
    NOT [ g_i AND (q_i=B OR exists j!=i: q_j=q_i) ].    (P-right)

When admitted, the output signature is exactly

    (A,B,C,D, [exists i:p_i=A], [exists i:q_i=B]).      (P-out)

Proof. Only the joined vertices a,z gain neighbors. The absence of an edge
between each child's terminals ensures that no child edge becomes an a-z
edge, and no parallel edge is created. All child interior vertices remain
distinct. Their adjacency colors are unchanged: in particular, even if one
interior vertex was adjacent to both terminals, those terminals become the
two distinct vertices a,z and keep their original colors C,D.

For edge a-u_s,i, the far-end flag stays f_i. At a, another neighbor has
color p_i exactly when the new outer terminal has that color or some other
child's left neighbor has it. This proves (P-left). The same argument at z
proves (P-right). New stub edges have a degree-one endpoint, so cannot be
bad. Every other edge retains its previous two flags. These conditions are
therefore necessary and sufficient, not merely a sufficient test.

For the new edge s-a, the recorded outer flag asks whether a has another
neighbor of color A; its child neighbors supply exactly the disjunction in
(P-out). The right flag is analogous. The output terminals are fresh, distinct,
nonadjacent and degree one. If children have maximum degree four and b<=3,
the internal joined vertices have degree b+1<=4, so the degree contract is
preserved; a series junction has degree two.

## Exactness for attainable state sets

Let F(G) be the set of signatures realized by all star colorings of a module
G from the chosen palette. Its series or stubbed parallel output set is
exactly the set obtained by applying the preceding transition formulas to
the child sets, with every compatible assignment of terminal/outer colors.

For sufficiency, choose a realizing child coloring for each selected state.
Disjoint interiors allow these colorings to coexist, and the transition
conditions prove their glued coloring star with the stated output signature.
For necessity, restrict an actual output star coloring to each child. Star
coloring is hereditary under vertex/edge restriction, so these restrictions
realize child signatures; the local argument forces precisely the transition
conditions. Thus no realization information beyond the signature is lost.

Induction gives exact signature propagation for every finite expression. This
is an exact interface theorem, not yet a proof of nonempty output sets at every
expression depth. Such a proof needs a closed realizable state family or an
exhaustively checked closed set automaton with an all-size induction.

## Shared-neighbor and equal-terminal cases

For path2 with distinct terminal colors, the shared neighbor has neither
terminal color on its other incident edge, hence both flags are false. For
path2 with equal terminal colors, both flags are true. These are the two
canonical base-state types. The same vertex can supply both flags without
invalidating the formulas: the parallel operation preserves two distinct
endpoint neighbors, and the series operation never identifies that interior
vertex with a boundary vertex.

In particular, a repeated child-neighbor color at an equal-colored parallel
join is caught by the flags, including the familiar bichromatic C4. The state
does not license arbitrary equal-terminal assignments. It checks their actual
feasibility through the realized child states and the two multiplicity tests.

If terminals were adjacent, identified with one another, or child interiors
overlapped, the proof would no longer apply without additional state and
intersection accounting. Those cases are excluded explicitly, not silently
treated by these formulas.

## Scope of the check

This argument is self-contained and uses the elementary forbidden-path
definition of star coloring. It makes no historical-priority claim. Root's
focused literature contributor separately identified the classical local
orientation formulation. The supplied independent diagnostic compares exact
transition sets with exhaustive proper-color assignments on small concrete
modules. Those finite checks supplement the universal interface proof; they
do not prove a universal four-color existence theorem.

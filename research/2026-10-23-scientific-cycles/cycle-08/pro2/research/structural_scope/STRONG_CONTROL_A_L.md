# An explicit three-query control for every A_L

Contributor: `/root/cycle8_structural_scope`, 22 October 2026.
This strengthens the comparator on the owner's new receiving atoms. It does
not solve the general loaded-interface problem.

## 1. Actual support and color construction

For L>=2, the support A_L has branch vertices a,b,c, two internally disjoint
length-two paths a-b, two such paths a-c, and one length-L path b-c. All path
interiors are disjoint. It has n=L+6 vertices and m=L+8=n+2 edges.

Color a by 0, b and c by 1, and all four interiors of the doubled a-b/a-c
paths by 2. For the ordered b-c path choose the unique k in {2,3,4} with
L congruent to k modulo 3. Start with its base word

    k=2:  1 0 1
    k=3:  1 0 2 1
    k=4:  1 0 2 0 1

and append the three-letter block (2,0,1) exactly (L-k)/3 times. The result
has length L+1 and endpoint colors 1,1, so it is a coloring of the original
path and graph. No edge or vertex is subdivided, deleted, or supplied with a
known coefficient by this operation.

## 2. All-length proof of the star condition

A proper coloring of a path is a star coloring exactly when no four consecutive
letters have the alternating form x,y,x,y. Each base word is proper and has
no such four-letter window.

The possible three-letter suffixes immediately before appending a block are

    101, 021, 201.

After appending (2,0,1), every case has suffix 201. The three new four-letter
windows in each case are respectively

    1012, 0120, 1201;
    0212, 2120, 1201;
    2012, 0120, 1201.

Each window contains all three colors. The newly added adjacent pairs are
also unequal. Thus one append preserves proper star coloring, and induction
proves this for every L>=2, without a size-dependent search.

It remains to check the full graph rather than just the path. For a proper
coloring, a bichromatic four-vertex path exists exactly when some edge uv
has another neighbor of color c(v) at u and another neighbor of color c(u)
at v. Use this local edge criterion.

Every edge on one of the four doubled paths has its degree-two midpoint as
an endpoint. That midpoint's two neighbors have distinct colors 0 and 1,
so this endpoint never supplies the required repeat. Such edges cannot be
middle edges of a bichromatic P4, regardless of repeats at a,b,c.

The first edge of the b-c path has colors 1,0. Its color-1 endpoint b has
only this one neighbor of color 0; its other two neighbors have color 2.
Therefore that edge cannot be the middle of a bichromatic P4.

At the c end, the last internal vertex has color 0 in every constructed word
except the unextended k=3 base word 1021. In the color-0 case, c again has only
one neighbor of that color, so the edge is safe. In the exceptional word,
the last edge has colors 2,1, but the color-2 vertex's other neighbor has
color 0. Thus it has no repeat of 1 and that edge is also safe. All remaining
path edges are controlled by the four-letter-window proof. This proves a
star-three coloring of the entire original A_L for every L>=2. QED.

## 3. Recovery consequence and matched query comparison

Set the three-column design row X_v=e_{c(v)}. Every row has Euclidean norm one.
For arbitrary symmetric D supported on A_L with free diagonal, use the inherited
star least-squares decoder on all original actions Y=DX+E. The support is
triangle-free, so the received Cycle7 operator argument gives

    ||Dhat-D||op <= sqrt(3/2) ||E||F,
    ||Dhat-D||F  <= sqrt(2) ||E||F.

These are the same uniform stability bounds that a star-four coloring would
provide, with one fewer action on this particular family. No numerical timing
advantage or historical priority is claimed.

Two real columns cannot even identify all supported symmetric matrices on
A_L: the coefficient space has dimension n+m=2n+2, whereas the linear action
map has only 2n output entries. This holds for every graph-adapted real
two-column design, with or without a row cap. Hence three is the exact and
dimension-independent stable query minimum for the family A_L under the
unchanged model.

Construction is O(L) arithmetic and storage to write the explicit graph/color
data; the word can be streamed in O(1) auxiliary space. The existing star
decoder is O(n+m) arithmetic/storage on supplied colors. Actual three actions,
expanded output, arithmetic precision, acquisition/assembly error, and any
inexact-decoder residual remain charged. This lemma supplies a mathematical
ordinary control, not an application benchmark.

## 4. What this changes

A_L remains a valid strict graph-interface receiving example: the old grammar
cannot represent it, and the loaded grammar can. But coloring A_L with four
coordinates alone cannot be described as a query improvement or new recovery
capability over this explicit three-coordinate control. A new loaded-interface
theorem must obtain its significance from uniform closure over its genuinely
broader admitted family, or from another consequential structural result.

The only finite checks below concern the three base words and three append
suffixes. The all-L conclusion is the induction above, not a numerical sweep.

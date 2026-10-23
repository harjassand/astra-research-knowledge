# Exact implications and gaps of the inspected representations

These are bounded local deductions for the literature receiving task. They
are not a second full construction programme or claims of historical novelty.

## A. What bounded tree-partition width does immediately provide

Suppose a graph has a supplied tree-partition with bags of size at most w.
Give the vertices inside each bag distinct indices from 1,...,w. Root the
quotient tree and give every vertex the pair

    (depth of its bag modulo 3, its index in that bag).

This uses at most 3w colors and is a star coloring. Indeed, two colors with
the same depth residue occur together only within individual bags, with at
most two selected vertices per bag. For two different residues, at most one
selected vertex occurs in each bag. The relevant quotient-tree components
are stars under depth modulo three, and selecting at most one vertex per
bag preserves that property.

The 2026 partition's w<=87 therefore gives an explicit **261-color** bound.
For the actual degree-four graph, all these bichromatic stars have at most
five vertices. This deduction is far weaker in query count than the owner's
already established ordinary comparators and is not proposed as an operation.

A tree-partition of width w is equivalently an embedding in T strong-product
K_w: the bag index gives the second coordinate. The complete product contains
K_(2w) across any adjacent pair of bags. Consequently, a coloring argument
that merely colors this complete supergraph cannot obtain four colors from
w=87. This supergraph is not in the owner's treewidth-two, degree-four class;
it is **not a counterexample to q4**. It shows which original sparsity has
been discarded by that attempted inference. A four-color argument must use
the actual subgraph and control its interfaces.

## B. Independent short proof that P7 squared is not star four-colorable

Let vertices 1,...,7 be adjacent exactly when their distance in the order is
one or two. Suppose a star four-coloring exists. Write colors at 3,4,5 as
a,b,c and the fourth color d. Properness gives color(2) in {c,d} and
color(6) in {a,d}.

- If these are c,a, the path 2–3–5–6 is bichromatic.
- If they are d,a, vertex 1 must be b or c. Respectively, 1–3–4–6 or
  1–3–5–6 is bichromatic. The c,d case follows by reversal.
- If they are d,d, vertex 1 cannot be b because of 1–2–4–6, hence is c.
  Vertex 7 cannot be b because of 2–4–6–7, hence is a. Then 1–3–5–7 is
  bichromatic.

Every case contradicts star coloring. All listed paths are actual P4s.
This independently checks the source's seven-vertex obstruction, without
enumeration. It only rejects the stronger star requirement.

## C. CAI plus an arbitrary forest three-coloring can fail exact injectivity

Take K2,3 with bipartition {u,v} and {z,a,b}. Set A={u,z,v} and I={a,b}.
Then G[A] is the connected induced path u–z–v, and I is independent: this
is a valid CAI partition. Root A at z and color by depth modulo three.
Vertices u and v receive the same color. Give I a fourth color.

The cycle u–a–v–b–u is now bichromatic. Alternating signed edge coefficients
around it give the usual exact coordinate-action kernel. The graph itself
is triangle-free, treewidth two and maximum degree three. A different
admissible coloring can work, so this is **a composition-rule failure**, not
a graph or all-design obstruction. The missing obligation is to control
the common-neighbor incidence between I and the three forest colors.

Distance-two independence of I would avoid this failure, because no vertex
outside I could have two neighbors in I. Mere independence, as provided by
the CAI theorem, does not.

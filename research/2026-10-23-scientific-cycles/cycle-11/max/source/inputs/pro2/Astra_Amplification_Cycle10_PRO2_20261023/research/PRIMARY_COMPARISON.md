# Strong comparators and historical boundary

Primary sources were consulted on 23 October 2026 after the new construction
had a concrete mathematical form. The narrow search did not establish
historical priority for the exact block-reset theorem. No survey-completeness
or new sparse-Hessian methodology claim is made.

## Established recovery machinery

Gebremedhin, Pothen, Tarafdar and Walther, *Efficient Computation of Sparse
Hessians using Coloring and Automatic Differentiation*, INFORMS Journal on
Computing 21(2), 2009. [Author PDF](https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf).

Sections 2-3 relate star coloring to direct Hessian recovery and acyclic
coloring to substitution. Their recovery algorithms exploit two-colored
structures, and Section 3.3 / Theorem 3.1 gives an entrywise error bound
depending on a rooted subtree size. Thus nonstar substitution, reduced color
counts and numerical-error analysis are established machinery. Our absolute
Frobenius-action-to-operator contract and projected LS estimate have their
stated scope; they do not negate that paper's differently formulated
stability result. The new contribution relative to our checkpoint is the
specific globally stable coloring construction from one-root atom profiles.

## Restricted bichromatic structures are established graph notions

Aravind and Subramanian, *Bounds on vertex colorings with restrictions on the
union of color classes*, 2010 author manuscript.
[Author PDF](https://people.iith.ac.in/aravind/Files/jgt-gvc.pdf).
Definition 1.2 uses proper colorings in which each component induced by a
fixed number of colors has bounded size. The general maximum-degree bounds
do not themselves specify four colors for the exact class proved here.
We do not claim to introduce bounded bichromatic component colorings.
Our abstract theorem also works with arbitrarily large short-arm spiders;
its inverse proof pays arm structure rather than using size alone.

Wood, *Acyclic, Star and Oriented Colourings of Graph Subdivisions*, DMTCS 7,
2005, 37-50. [Journal PDF](https://dmtcs.episciences.org/articles/344/download).
This treats star/acyclic colorings of subdivisions, including the graph
obtained by subdividing every edge once and longer-subdivision results.
The present native graph is not freely replaceable by a subdivision:
adjacent cut vertices and all original action cells must remain. These
established controls apply when their actual graph hypotheses hold; they
do not justify subdividing an unknown matrix support for free.

## Ordinary operations under the SAME recovery model

| Operation | Scope | Queries / conditioning | What this checkpoint changes |
| --- | --- | --- | --- |
| Forest coordinate recovery | Forest supports | 3, Frobenius bound sqrt(2) | Remains stronger on its class; no extra-query benefit claimed there |
| Inherited A_L operation | That specifically proved atom family | 3 under its established guarantee | Not displaced by an A_L-only four-query example |
| Inherited atom star recovery | One chordless width-two degree-four atom | At most 4; triangle-free operator sqrt(3/2), Frobenius sqrt(2); C3 separately constant 1 | Rooted copies now compose into a stable connected nonstar operation |
| Cycle9 complete-bipartite block parity | C_p with middle incidence two | p+2, operator and Frobenius sqrt(3+sqrt(5)) | General bridgeless chordless degree-four blocks are now admitted when p=2 is no longer a complete-bipartite description |
| Full-class five-query design | Every maximum-degree-four support, hence the full selected class | Fixed full-spark R5 palette on a 17-coloring of G squared; finite size-independent inverse constant | Still the full-class upper control; this checkpoint does not solve arbitrary-real four-versus-five |
| New one-message gluing | Bridgeless chordless tw<=2, Delta<=4, nontrivial connected supports | 4, operator and Frobenius sqrt(3+sqrt(5)) | All-depth simultaneous attachment control and actual original-action inverse |
| New explicit theta operation | Theta block trees with unshared hubs and degree-two cuts in two blocks | 4, same constant; arbitrary branch arity and length | A direct construction without the inherited finite atom table on this subclass |

The five-query comparison remains under whole-row energy at most one and
absolute Frobenius noise. Its fixed palette is full spark, so every closed
neighborhood of size at most five has a uniformly bounded row inverse;
symmetrizing the recovered rows preserves a Frobenius bound. Graph-square
coloring, row-system preparation, all five original actions, precision and
output work are charged. We have not run or retuned this old comparator,
nor declared four-query total-cost dominance over it.

The exact receivers here store explicit rational D. In that fixture, direct
entry assembly is already available in O(n+m) work. The compressed operations
therefore check the theorem and its original-action interface; they do not
prove an application runtime advantage. For a true action source, acquisition
cost and accuracy must be supplied. No expensive opaque oracle is invented.

Historical originality, internal proof/check status, implementation efficiency,
and downstream physical usefulness are separate. The old NIST incumbent and
the closed molecular/physical comparisons are untouched.

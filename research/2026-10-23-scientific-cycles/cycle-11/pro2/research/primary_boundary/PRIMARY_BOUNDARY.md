# Cycle11 primary boundary: bridge-inclusive chordless supports

Date: 2026-10-23. Scope: a bounded source check for the Pro2 bridge-composition investigation. This is not a new coloring construction, scientific benchmark, proof review of the bridge theorem, or a claim of historical priority.

## Decision-relevant finding

The inspected primary sources do not provide a matched theorem giving four coordinate colors, acyclicity, and uniformly bounded bichromatic component size or cut balance for all chordless supports of treewidth at most two and maximum degree four, including arbitrary bridges. This is a bounded-search conclusion, not proof that no such theorem exists.

The classical six-color star upper bound for treewidth two remains an applicable published coordinate-coloring comparator among the inspected results. The owner's five-action full-spark operation remains the stronger action-count control on the full maximum-degree-four class. The two controls differ in conditioning and representation. The accepted Cycle9 no-star-four support already precludes a universal star-four theorem on the target class; it does not preclude bounded nonstar components or arbitrary real four-column designs.

## A genuinely relevant chordless theorem, with a different interface

Basavaraju, Hegde and Kulamarva, *Acyclic Chromatic Index of Chordless Graphs* (2023), Theorem 1: a connected chordless graph of maximum degree Delta has acyclic **edge** chromatic index Delta unless it is a cycle; a cycle needs three. Corollary 2 gives linear arboricity ceil(Delta/2), with the stated degree-two cycle exception. In particular, maximum-degree-four chordless graphs admit an edge decomposition into two linear forests. The proof explicitly handles cut vertices by permuting edge colors on components at the cut, and gives a polynomial-time construction.

Primary full text: <https://arxiv.org/html/2302.01638v1>. Inspected locations: Theorem 1, Corollaries 1–2, and the proof's non-two-connected reduction.

**Receiving boundary.** These are edge partitions, not vertex query colors. The linear forests may contain arbitrarily long paths. Their existence alone neither supplies the owner's four-action design nor bounds its inverse under absolute Frobenius action noise. Separate forest actions are not available from the original action without an additional proved operation. The edge-color cut-vertex permutation cannot be imported as a vertex-color mass-reset argument.

## Bounded bichromatic components are established coloring objectives

Aravind and Subramanian, *Bounds on vertex colorings with restrictions on the union of color classes*, J. Graph Theory 66 (2011), 213–234, author manuscript Theorem 1.3: for integers j<=k there is a constant C(j,k) such that every graph of maximum degree d admits a proper coloring with at most C(j,k)d^(k/(k+1-j)) colors, and each component induced by any j color classes has at most k vertices. Definition 1.2 states the component-size requirement. Their further forbidden-subgraph framework permits simultaneous restrictions.

Primary author manuscript: <https://people.iith.ac.in/aravind/Files/jgt-gvc.pdf>. Inspected pp. 3–5, especially Definition 1.2 and Theorem 1.3.

**Receiving boundary.** The existence of a bounded-component coloring with some degree-dependent number of colors is prior work. The theorem does not give four colors at d=4, does not by itself forbid a bounded bichromatic cycle, and does not state the owner's original-action inverse norm. A new contribution must identify its exact color count, acyclicity, component geometry or cut balance, constructive cost, and recovery consequence.

### Search correction: Bradshaw is not an independent novelty source

The arXiv record for Bradshaw's *Graph colorings with restricted bicolored subgraphs: I. Acyclic, star, and treewidth colorings* is withdrawn. The author explains that the main result and method had already appeared in Aravind–Subramanian. The publisher still displays a 2022 article record and abstract. The withdrawal concerns priority as stated in the record; this note does not infer a false theorem or a journal retraction. Use the earlier primary source for this boundary.

Primary records: <https://arxiv.org/abs/2008.13274> and <https://onlinelibrary.wiley.com/doi/10.1002/jgt.22827>.

## Ordinary star-color comparators and scope

Albertson, Chappell, Kierstead, Kundgen and Ramamurthi, *Coloring with no 2-colored P4's*, Electronic J. Combinatorics 11 (2004), R26, proves the treewidth-t star-color upper bound binomial(t+2,2); for treewidth two this is six. The broad treewidth sharpness is not a lower bound restricted to maximum degree four. A star coloring constrains every bichromatic component to be a star, which is stronger than the current recovery objective.

Primary article: <https://www.combinatorics.org/ojs/index.php/eljc/article/download/v11i1r26/pdf>. Inspected abstract, definitions, and the description of the treewidth result. This is inherited comparison, not new receiving science.

Bu, Cranston, Montassier, Raspaud and Wang, *Star coloring of sparse graphs*, J. Graph Theory 62 (2009), 201–219, Theorem 2(i), gives star four when maximum average degree is below 26/11. It does not cover K_(2,4), whose average degree is 8/3; K_(2,4) is already inside the owner's native class. The primary result therefore cannot replace the bridge-composition obligation. Its forest-plus-distance-separated-set sufficient mechanism is stronger than an arbitrary cut-vertex decomposition.

Primary author version: <https://arxiv.org/pdf/2105.06641>. Inspected Theorem 2(i) and the forest-plus-separated-set discussion. DOI: <https://doi.org/10.1002/jgt.20392>.

## Hessian recovery comparison preserved

The owner's already-read primary comparison remains applicable: Gebremedhin, Pothen, Tarafdar and Walther, *Efficient Computation of Sparse Hessians Using Coloring and Automatic Differentiation* (INFORMS J. Computing, 2009), connects star coloring to direct recovery and acyclic coloring to substitution, and treats subtree-dependent roundoff in Section 3.3, Theorem 3.1. No new claim that coloring-based compression, tree substitution, or roundoff analysis originates here is warranted.

Preserved primary URL: <https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf>. This check read the owner's existing comparison note rather than rerunning its historical source audit. Direct entry assembly or AD must remain a control when the actual receiving problem provides it.

## Consequence for Cycle11 claims

An all-depth bridge-inclusive four-coordinate construction with a proved global inverse would expand the accepted covered class. The contribution should be stated as the actual rooted/bridge interface, its global propagation invariant, and the original-action error theorem. It should not be described as a first use of nonstar substitution, a first bounded-component coloring objective, an arbitrary-real four-query lower/upper on the full nonchordless class, or a practical speedup. This bounded literature check leaves historical originality unresolved.

## Work limits

No scientific calculations, benchmark jobs, old theorem replays, or new graph searches were run. Source research and authoring costs were not fully timed. The note records what was inspected and what was not; absence of a retrieved matching theorem is not an exhaustive literature claim.

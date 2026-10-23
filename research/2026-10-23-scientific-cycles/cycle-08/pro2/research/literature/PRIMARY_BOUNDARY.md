# Focused primary-literature boundary: Cycle8 loaded ports

This is a bounded comparison for the proposed nonadjacent-terminal star-four
interface on chordless series-parallel supports of maximum degree four. It is
not a survey and does not prove historical novelty. No matched published
star-four existence theorem or counterexample for that exact intersection was
located in the recorded searches. This negative search result must not be
converted into a claim that none exists.

## What the strongest checked sources actually establish

### Exact and long subdivisions: Wood (2005)

David R. Wood, *Acyclic, Star and Oriented Colourings of Graph Subdivisions*,
Discrete Mathematics & Theoretical Computer Science 7 (2005), 37–50.
Primary original PDF: https://dmtcs.episciences.org/344/pdf
DOI: https://doi.org/10.46298/dmtcs.344

Lemma 3 proves chi_star(G') <= max(chi(G),3), where G' replaces **every** edge
of G by a two-edge path. The proof colors original endpoints properly and
colors each subdivision vertex differently from both endpoints. Lemma 11
proves star-four colorability when **every** original edge is replaced by a
path of at least three edges. Lemma 10 gives star-three when those replacement
paths have at least three edges and none has five edges. These are explicit
constructive comparators. The first is not a theorem for arbitrary mixed
replacement lengths, and the latter two exclude unsubdivided and once-subdivided
edges. Their hypotheses must be checked on the actual support; adding division
vertices changes the original recovery problem.

Relevant inspected locations: original pp.40,45–46; Lemmas 3,10,11.
Browser source references: turn206view1, turn208view0, turn208view1.

### Bounded-treewidth existence/decision: Albertson et al.; Shalu–Antony

Michael O. Albertson, Glenn G. Chappell, H. A. Kierstead, Andre Kuendgen,
Radhika Ramamurthi, *Coloring with no 2-colored P4's*, Electronic Journal of
Combinatorics 11 (2004), R26.
Primary PDF:
https://www.combinatorics.org/ojs/index.php/eljc/article/download/v11i1r26/pdf

The paper supplies the established star-color/in-color-orientation machinery
and the general treewidth-t star-color upper bound binomial(t+2,2), hence six
colors for treewidth two. Its general sharpness statement is not a matched
lower for the bounded-degree chordless class. This six-color coordinate
operation is an ordinary structural upper; it is weaker in query count than
the owner's established five-query arbitrary-real full-spark control.
Inspected abstract/introduction and prior source-bound Section6 capital.
Browser source: turn211view2.

Shalu M.A. and Cyriac Antony, *Star colouring of bounded degree graphs and
regular graphs*, Discrete Mathematics 345(6) (2022),112850.
DOI: https://doi.org/10.1016/j.disc.2022.112850
Author preprint: https://arxiv.org/html/2309.04291v1

Its introduction explicitly records that fixed-k star colorability is MSO1
expressible and therefore fixed-parameter tractable in treewidth or cliquewidth.
Thus an existence-of-a-finite-state-decider claim on supplied width-two graphs
is not a new algorithmic frontier by itself. A new explicit small interface
can still be useful for constructive uniform existence, proof certificates,
or practical constants, but those additional consequences require proof.
The paper's hardness results for bipartite maximum-degree-k graphs do not
restrict their inputs to treewidth two or chordless graphs; they cannot refute
the owner's smaller class. Browser source: turn211view0, lines53–55 and50–52.

### Density-based star-four sufficient condition

Yuehua Bu, Daniel W. Cranston, Mickael Montassier, Andre Raspaud, Weifan Wang,
*Star coloring of sparse graphs*, Journal of Graph Theory 62 (2009),201–219.
DOI: https://doi.org/10.1002/jgt.20392
Author preprint: https://arxiv.org/pdf/2105.06641

Theorem2(i) gives star-four when maximum average degree is strictly below
26/11. Lemma6 derives a vertex partition into a forest and a set whose distinct
vertices are pairwise distance greater than two, which supplies the fourth
color after star-three coloring the forest. This sufficient density hypothesis
is not automatically true for the current grammar: K2,4 is an admitted
degree-four chordless SP example with average degree 8/3 >26/11. Thus that
theorem does not settle the proposed whole class. Figure5 presents a graph
with maximum average degree18/7 and star number>4; its additional graph
hypotheses were not authenticated here, so it is **not** used as an obstruction
inside the owner's support class. Browser source: turn206view0, turn207view4.

## Recovery comparison remains classical sparse-Hessian compression

Assefaw H. Gebremedhin, Alex Pothen, Arijit Tarafdar, Andrea Walther,
*Efficient Computation of Sparse Hessians using Coloring and Automatic
Differentiation*.
Primary author PDF:
https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf

The paper treats the full workflow: determine support, construct a coloring
seed S, acquire the compressed Hessian HS, and recover entries. Direct recovery
uses star coloring; substitution uses acyclic coloring. It analyzes linear
recovery work and rounding behavior. Thus coordinate compression, star direct
readout, acyclic substitution and sparse-Hessian applicability are established
machinery. The owner's absolute Frobenius-noise to operator-error theorem and
an all-depth coloring-existence certificate should be stated separately from
that machinery, and no runtime improvement follows without a matched receiving
calculation. Browser source: turn211view1, pp.1–3.

## Disambiguations and remaining originality limit

Several search hits concern star **edge** coloring or acyclic edge coloring,
whose colors are assigned to edges and whose forbidden path conventions differ.
Other series-parallel hits use the older term "star coloring" for circular
coloring. None establishes the vertex-star invariant needed here. Ordinary
three-colorability of chordless graphs also does not establish the invariant.

The checked primary sources give strong controls and an explicit novelty
boundary. They do not authenticate a new historical-priority claim for loaded
ports, nor do they certify the producer's finite transitions or all-depth
nonemptiness. Internal mathematical verification is a separate obligation.

## Costs

`CALLS.json` records each of ten web calls, query/open/find/screenshot scopes,
and elapsed wall time waiting for that call, totaling **31.444 seconds**.
There were six search calls with
20 total query strings, eight requested locations in three open-bearing calls
(seven succeeded; one unrelated recent chordal-paper open failed),
six find patterns, and one PDF screenshot. Calls are not a model-inference or
discovery-time measure. Reading, reasoning, source selection and note authoring
were not individually metered and remain unknown. No old scientific calculation
or performance benchmark was rerun, no paid resource used, and no outreach made.

## Follow-up: intrinsic two-connected chordless width-two class

After reading the contributor's
`research/structural_scope/ALL_CHORDLESS_ATOMS.md`, the comparison target was
strengthened to all finite simple two-connected chordless graphs of treewidth
at most two and maximum degree four, with C3 treated separately. Three focused
searches on minimally two-connected/chordless star coloring did not locate a
matched star-four theorem or counterexample. This remains a search limitation,
not a historical-priority finding. The previous comparators still apply.

Raphael C. S. Machado, Celina M. H. de Figueiredo and Nicolas Trotignon,
*Edge-colouring and total-colouring chordless graphs*, primary author preprint
https://arxiv.org/pdf/1309.1842, Section2, is a close structural antecedent.
It recalls the theorem of Leveque, Maffray and Trotignon that every
two-connected chordless graph is either 2-sparse or has a proper two-cutset.
Its Theorem3 chooses an extremal split whose marked block is 2-sparse, with
both cut vertices having at least two neighbors on that side. These are
established chordless decomposition principles; they do not establish a
vertex-star extension invariant at the shared vertices. The paper's optimal
edge and total colorings color different objects from the vertex query design.
Browser source: turn215view0, pp.4–5, Theorems2–3.

Manu Basavaraju, Suresh Manjanath Hegde and Shashanka Kulamarva,
*Acyclic Chromatic Index of Chordless Graphs*, primary author preprint
https://arxiv.org/html/2302.01638v1, strengthens chordless graph structure for
acyclic EDGE coloring and determines its optimum, including four edge colors
when maximum degree is four. No conversion from that edge coloring to a
four-color vertex-star design is supplied by the inspected result. The
coincidence of the number four must not be treated as subsumption. Browser
source: turn215view1, abstract, Section1 and Theorem1.

The intrinsic-class consequence therefore has a clear comparison: standard
series-parallel/chordless decomposition supplies structural ingredients,
while realizable loaded-port transitions must discharge the stronger
vertex-star boundary obligations. Whether that combination has historical
priority is still unverified. This follow-up made two web calls (three query
strings and two primary opens); exact additional tool-wait costs are in
`INTRINSIC_CLASS_FOLLOWUP_CALLS.json`. Proofs and scientific code were not edited.

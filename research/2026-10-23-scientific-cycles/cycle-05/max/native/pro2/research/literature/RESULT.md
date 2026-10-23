# Focused primary-literature and comparator checkpoint

Contributor: `/root/bounded_degree_literature`.
Scope: four versus five real row-capped probes for symmetric known-support
recovery, free diagonal, absolute Frobenius action noise, operator error,
treewidth<=2 and maximum degree<=4. This was a bounded comparison obligation,
not a second complete investigation.

## Main finding

No inspected primary source supplies a dimension-independent four-probe
inverse for the entire stated graph class. This limited search establishes
neither historical novelty nor an open-problem claim about the literature.

The search changed the concrete comparator in a useful way. Squared paths
need five colors for classical star/direct coordinate recovery. However,
four coordinate colors with uniformly bounded bichromatic components suffice
for stable acyclic recovery. The explicit period-nine construction and full
noise argument are in `PERIOD9_LEMMA.md`, with exact finite-period checks and
rational pseudoinverses in `check_period9.py`. It gives

    ||Dhat-D||_2 <= sqrt(3+sqrt(5)) ||E||_F

using four unit-row coordinate probes, O(n) preparation and O(n) decoding
under a supplied bandwidth-two ordering. The proof applies to every
subgraph of a squared path. It does not apply to every partial two-tree.

This means a new signed four-probe construction on squared paths should be
compared against the four-query bounded-component operation, not only the
five-query star-color comparator. The newly supplied period is new relative
to the inherited checkpoint; the acyclic recovery mechanism is established.

## 1. Classical direct/star lower on actual degree-four graphs

A. H. Gebremedhin, A. Pothen, A. Tarafdar, A. Walther,
*Efficient Computation of Sparse Hessians Using Coloring and Automatic
Differentiation*, INFORMS Journal on Computing21(2)(2009),209-223.
Author PDF:
https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf

Section4 defines band graphs. Theorem4.4's proof explicitly invokes the
condition n>=3 beta+1 for the classical equality between star and distance-two
chromatic numbers on band graphs. Consequently P_n^2 needs five star colors
when n>=7. Theorem4.3 supplies three acyclic colors for this chordal family,
but exact substitution alone supplies no uniform action-noise estimate.
Section3 distinguishes direct/star and indirect/acyclic recovery and gives
an error bound growing with the relevant two-color subtree.

Use only this band-graph specialization here. In particular, the size
condition in the proof must be retained; the theorem's displayed broad
wording would be misleading on small complete band graphs.

The paper credits T. F. Coleman and J. J. More,
*Estimation of sparse Hessian matrices and graph coloring problems*,
Mathematical Programming28(1984),243-270. The original1982 report record was
opened at https://hdl.handle.net/1813/6374; its linked PDF failed retrieval.
Thus the exact old attribution is verified through the2009 primary paper,
not by pretending to have read the unavailable original PDF.

Useful retrieved refs: turn114view0, turn115view0, turn115view1,
turn125view3, turn117view0.

## 2. Recent 2-path result confirms the scope distinction

G. Benitez-Bobadilla, F. E. Contreras-Mendoza, C. Hernandez-Cruz,
C. Linhares Sales, A. Trujillo-Negrete,
*Star Coloring on Some Subclasses of Chordal Graphs*, arXiv:2606.25168.
https://arxiv.org/pdf/2606.25168

Proposition4.4/Figure13 gives minimal non-star-four-colorable 2-paths H1,H2;
Theorem4.6 characterizes the star-four-colorable 2-paths by excluding them,
and Theorem4.10 provides five star colors for every 2-path. H1's associated
degree sequence is(2,2,2); its canonical description matches P_7^2. The older
band-graph theorem above provides a cleaner independent source for the
particular squared-path barrier.

The definition paragraph contains the same nonconsecutive-triangle wording
inconsistency flagged in the inherited note. This review does not rely on
resolving it or on accepting all claims of the new paper. A star-color lower
is not an all-dense-design lower, and it does not exclude bounded-component
acyclic recovery.

Refs: turn110view0, turn111view0, turn111view1, turn112view0.

## 3. Stronger direct covers already exist

S. Hossain and N. H. Mithila, *Pattern graph for sparse Hessian matrix
determination*, Optimization Methods and Software33(4-6)(2018),1250-1263.
https://doi.org/10.1080/10556788.2018.1458849

Detailed primary predecessor: N. H. Mithila,
*On the determination of sparse Hessian matrices using multi-coloring*,
University of Lethbridge,2016, Section4.1.2, Theorem4.5, printed pp31-36.
https://opus.uleth.ca/bitstreams/2e847d06-b3f9-459f-beb4-a13df9596fef/download

The thesis allows a column to enter multiple binary seed groups while
requiring every coefficient to have an isolated endpoint read. Its explicit
six-vertex, four-query example has all diagonals free and is supported on
the triangular-prism graph, rather than a squared path. No four-query
pentadiagonal theorem appears in the inspected text. This does not prove
that none exists elsewhere.

The inherited note proves the elementary normalization conversion: if a
binary direct-cover seed has maximum row weight r, scaling by1/sqrt(r)
gives row cap one and error constant sqrt(2r). That remains a valid stronger
comparison class than single-coordinate star coloring.

Refs: turn118view1, turn120view4. The2018 journal record and original thesis
were already preserved in the owner's preceding literature note.

## 4. Current banded recovery uses the ordinary periodic-identity seed

T. Park and Y. Nakatsukasa,
*Approximating Sparse Matrices and their Functions using Matrix-vector
products*, arXiv:2310.05625.
https://arxiv.org/pdf/2310.05625

Section3.1, equation(10), recovers a banded matrix with upper/lower bandwidths
k1,k2 using the periodic identity seed with1+k1+k2 columns. The pentadiagonal
specialization uses five. Section3.2 extends this to approximation with
off-diagonal decay. These are useful operations with different approximation
questions; their decay error bound is not itself a four-query action-noise
theorem. The elementary five-query symmetric specialization is isometric
in Frobenius norm, so full least-squares averaging yields error constant one.
That last normalization/noise statement is our direct deduction.

Refs: turn122view0, turn125view0, turn125view2.

## 5. Other focused checks and non-applicability

D. Halikias and A. Townsend, *Structured matrix recovery from matrix-vector
products*, arXiv:2212.09841v2, Section2.1.3.
https://arxiv.org/pdf/2212.09841

The paper gives exact two-query recovery for symmetric tridiagonal matrices
and three queries for general tridiagonal matrices. The inspected section
does not give the sought uniform four-query pentadiagonal inverse. Its
error-prone HSS/HODLR discussion concerns another structure and includes
Gaussian perturbation experiments. Those observations do not transfer an
adversarial absolute Frobenius guarantee to this fixed query count.

Refs: turn121view0, turn122view1, turn122view3.

M. A. Shalu and C. Antony, *Star Colouring of Bounded Degree Graphs and
Regular Graphs*, Discrete Mathematics345(6)(2022),112850;
https://arxiv.org/abs/2309.04291.
The primary abstract studies lower bounds/structure on regular graphs and
complexity of star-color testing. It supplies no applicable four-star-color
upper for the partial-two-tree degree-four class. The regular-degree-four
structure is not automatically available in finite two-degenerate graphs.

Luksan-Matonoha-Vlcek's2010 *Band preconditioners for the matrix free truncated
Newton method* was opened after a targeted search; it concerns preconditioner
construction and does not supply a matched theorem in the inspected material.
https://www.cs.cas.cz/matonoha/download/V1079.pdf

Searches for bounded bichromatic components, signed banded seeds and four
pentadiagonal queries found no precise matching prior result. Wrong-object
hits on star EDGE coloring, inverse eigenvalue reconstruction, and numerical
solutions of pentadiagonal systems are not used as evidence.

## Receiving use and decision

The period-nine proof changes a concrete comparison immediately: root's
signed-period candidate on squared paths has a same-query classical-mechanism
comparator with an explicit noise constant and local decoder. If retained,
its scientific contribution should be a more general structural mechanism,
a stronger bound or implementation, rather than four versus five on that
family alone. General TW2,Delta4 still needs a proof or obstruction beyond
these sources and this narrower construction.

The primary-source check itself does not certify the root construction and
is not a historical-priority search sufficient for a novelty claim.
Parent must open a source personally before citing a child web reference in
the root final response. Exact source URLs and hypotheses above are the
durable handoff; retrieved source IDs are convenience metadata.

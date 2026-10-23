# Follow-up: bounded bichromatic components and four queries

Requested by root after accepting the period-nine bandwidth-two comparator.
This is a bounded source check, not another construction programme.

## Conclusion

I found a relevant established **four-linear-color theorem for outerplanar
graphs of maximum degree four**, but no inspected primary theorem providing
uniformly bounded bichromatic component size or path length at that same
budget. I found no matched theorem resolving the entire TW<=2,Delta<=4 class.
This statement describes the inspected sources and search scope; it is not
evidence of historical novelty or a literature-wide open-problem claim.

Two terminology cautions are consequential:

1. Ordinary clustered coloring controls **monochromatic** components. It
   does not supply the two-color component bound required here.
2. Proper four-coloring with bounded two-color components is itself
   insufficient for coordinate probing unless bichromatic cycles are also
   excluded. A bicolored C4 has an alternating edge-coefficient kernel.

The useful sufficient condition is **acyclic four-coloring with uniformly
bounded bichromatic components**. Its linear-coloring specialization asks
for uniformly bounded bichromatic path length.

## Closest four-color theorem: linear choosability of outerplanar graphs

L. Esperet, M. Montassier, A. Raspaud,
*Linear choosability of graphs*, Discrete Mathematics308(2008),3938-3950.
Primary author report, June7,2007:
https://oc.g-scop.grenoble-inp.fr/esperet/publications/RR-1382-06.pdf
Publisher identity:
https://www.sciencedirect.com/science/article/pii/S0012365X07005936

The introduction and Section4/Theorem3 state that every outerplanar graph G
is linearly ceil(Delta/2)+2-choosable. Therefore four colors suffice for
Delta<=4, even for arbitrary lists of size four. Here linear means that
each bichromatic induced subgraph is a forest of paths. Their convention
calls the neighborhood condition 3-frugal, meaning no color occurs more
than twice; other sources call this 2-frugal.

The theorem does not state a path-length bound. The initially retrieved
primary text exposed the introduction and exact theorem description;
subsequent requests for the proof pages timed out. No inference that the
proof secretly supplies a bound is warranted. Outerplanarity also excludes
K2,3, so this scope is strictly smaller than the root's partial-two-tree
class. The theorem is useful capital toward an extension, not a stable
four-query result as currently stated.

Root-open references: turn130view0, turn134search2, turn134search13.

## Exact terminology for bounded two-color components

N. R. Aravind and C. R. Subramanian,
*Bounds on vertex colorings with restrictions on the union of color classes*,
primary author manuscript dated March25,2010:
https://people.iith.ac.in/aravind/Files/jgt-gvc.pdf

Definition1.2 calls a proper coloring in which every component induced by
any j color classes has at most k vertices a **(j,k)-coloring**. Thus the
component-size part of our question is a four-color(2,L)-coloring for an
absolute L, with acyclicity additionally imposed. Theorem1.3 and the explicit
Proposition2.2 bound the required number of colors in terms of maximum
degree; the constants do not specialize to four at degree four. The paper's
Section5 permits simultaneous forbidden-subgraph requirements, but the
inspected bound again does not give the needed four-color theorem.

This is a precise existing framework for the desired combinatorial
condition. It does not make a new name such as clustered acyclic coloring
necessary, and no exact match for that phrase was located in this check.

Root-open refs: turn128view1, turn132view1, turn131view4.

## Related primary results that do not close the gap

D. W. Cranston and G. Yu, *Linear Choosability of Sparse Graphs*,
arXiv:1007.1615v1:
https://arxiv.org/html/1007.1615v1

Theorem1 gives three regimes: mad<12/5 with Delta>=3; mad<3 with Delta>=9;
and planar girth>=5. None supplies four bounded-path colors for all
TW<=2,Delta<=4. The introduction explicitly identifies K2,3 as requiring
four linear colors. Linear colorability alone permits arbitrarily long
components and therefore does not certify the required noise inverse.

C. Greenhill and O. Pikhurko,
*Bounds on the generalised acyclic chromatic numbers of bounded degree graphs*,
Graphs and Combinatorics21(2005),407-419:
https://web.maths.unsw.edu.au/~csg/papers/acyclic-bound.pdf

Their generalized acyclic parameter requires each cycle of length k to use
at least min(k,r) colors. It is not a bound on bichromatic path length or
component size. Its asymptotic maximum-degree results do not settle the
present four-color condition.

The term linear coloring is also used in a different recent literature for
colorings where every path has a uniquely occurring color, and in linear
arboricity for **edge** colorings. Those are different objects. Search hits
for low-treewidth linear arboricity were not imported as vertex-query
theorems.

## Why the missing bounds cannot be suppressed

These are self-contained applicability checks, not new lower theorems.

For a proper coordinate coloring, a bichromatic cycle of even length has a
nonzero edge vector with alternating coefficients +1,-1. At every cycle
vertex the two incident contributions cancel, so DX=0. Bounded component
size alone therefore does not establish injectivity.

For a bichromatic path P_l, its unsigned incidence matrix has least positive
singular value2 sin(pi/(2l)). As l grows, the full coefficient-Frobenius
inverse grows. Even in operator norm the problem remains: choose alternating
edge signs with a slowly varying sine envelope. The action is controlled
by discrete differences of the envelope, of total norm O(l^(-1/2)), while
the matrix operator norm is at least its largest edge coefficient, which
stays bounded below. Hence a fixed linear coloring containing arbitrarily
long bichromatic paths cannot furnish a dimension-independent operator
inverse under the root's action-noise norm.

Ordinary clustered coloring cannot replace the two-color condition. The
alternating two-coloring of a path has singleton monochromatic components
but one bichromatic component containing the whole path. A proper acyclic
coloring and a separate clustered coloring also cannot be combined without
charging the resulting palette and checking cross-class components.

## Search scope, access limitations and cost

Nine further web calls had reported outer latencies:

    2.1,4.6,2.0,4.3,2.1,2.4,2.3,1.9,3.8seconds.

Total scoped access latency: **25.5seconds**, in addition to the preceding
46.9seconds, giving26calls and72.4seconds cumulatively for this contributor.
These remain access times, not discovery cost. Reading, inference, authoring
and coordination are additional and unmetered. No numerical experiment,
optimization, benchmark replay or graph enumeration was performed in this
follow-up.

Exact phrases included bounded bichromatic components, clustered acyclic
coloring, two-coloured components, component size, (2,k)-coloring,
linear coloring/colouring, outerplanar, series-parallel, maximum degree4,
and bounded path length. Independent searches and reads were batched.
The stronger search engine was used when routine search returned irrelevant
or wrong-object results.

Failures included a Citeseer PDF403, an inaccessible conference download,
and repeated author-PDF follow-up timeouts after its initial successful
opening. A survey on ordinary clustered coloring was inspected for
terminology and references, not used as a primary theorem establishing the
desired inference. Its monochromatic guarantees are not the target
hypothesis. No unavailable source is treated as having been read.

## Handoff consequence

The precise useful literature bridge is now:

    outerplanar Delta<=4 -> four linear colors [established],
    bounded bichromatic path length -> stable local four-query inverse
        [elementary incidence calculation],
    four linear colors + uniform path-length bound on all target graphs
        [not supplied by this check].

The root's next construction may try to establish that missing bound or
use a global inverse that does not require it. A failure of this coloring
ansatz would still not be an obstruction to arbitrary graph-adapted real
four-direction designs.

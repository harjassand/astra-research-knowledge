# Cycle10 result: one-message composition gives stable four-action recovery

Pro2, 23 October 2026. Scientific checkpoint; source delivery is recorded in
the external receipt, after this archive is frozen.

## Strongest result

Every connected **bridgeless chordless** finite simple graph with at least
one edge, treewidth at most two and maximum degree at most four admits a
constructive four-coordinate design and canonical least-squares inverse with

\[
\|\widehat D-D\|_{\rm op}\leq\|\widehat D-D\|_F
\leq \sqrt{3+\sqrt5}\,\|E\|_F.
\]

The support is known before the design. D is any original supported real
symmetric matrix, including a free diagonal. Each WHOLE probe row has norm
one; all original observations Y=DX+E are used; E is arbitrary absolute
Frobenius noise. No altered-support action, favorable noise law, known
coefficient or free numerical precision is assumed.

All bichromatic components are spiders with arms of length at most two.
This permits nonstar components. Block size, block depth, branching, path
length and adjacent actual attachment vertices are unrestricted. The result
includes all the selected theta-block frontier and also non-theta atoms,
cycles and triangles. It is an intrinsic edge-list operation, not merely a
supplied-expression promise. Coverage is proved on this stated graph class;
the implementation is not advertised as a full chordlessness recognizer on
arbitrary graphs outside it. Its actual accepted coloring and component
certificates are checked separately.

Four is the worst-case uniformly stable **coordinate** minimum on this
class, including signed unequal one-coordinate amplitudes, by the retained
Cycle9 K_(2,4)-chain lower bound. This is not an arbitrary-real three-query
lower bound for this subclass. The full arbitrary-real four-query problem
on treewidth-two, degree-four supports remains open.

The isolated single vertex has a trivial one-action inverse separately.
Bridges and nonchordless blocks are not included in the new coverage theorem.

## What makes the composition work

The received one-mark atom theorem supplies a real star-four coloring at
one actually specified degree-two root: its two neighbor colors differ,
and at most one neighbor color has a far-repeat flag. It does not prescribe
independent profiles at multiple attachment vertices.

The new gluing algorithm uses that guarantee only once per block. A global
color permutation makes the child share at most one color channel with its
parent; if one is shared, the child's component in that pair is an isolated
edge r-u. When u is another cut, one message requires the next child to
avoid color(r). This request is always realizable by the same one-root
guarantee. It constrains the new child, not a second root of the already
colored block.

Consequently a bichromatic component consists of a local star with at most
one pendant extension at each vertex. No inherited component can propagate
through another generation. In a bridgeless degree-four graph, every cut
automatically belongs to exactly two nontrivial blocks and has local degree
two in each, which supplies the incidence hypotheses intrinsically.

This is the receiving use that changes the old scientific boundary:
Cycle9's one-root theorem becomes a complete simultaneous-attachment
operation on an unbounded class. Separate local star colorings had not
provided that implication. The old no-star-four 16-vertex example is not
contradicted: the new global coloring permits nonstars.

The recovery constant follows from the anchored two-edge-arm quadratic,
not from bounded diameter. Its matrix [[2,-1],[-1,1]] has least eigenvalue
(3-sqrt(5))/2. Summing the arm inequalities bounds each incidence inverse;
the factor two for symmetric off-diagonal output gives 3+sqrt(5).
PROOF.md gives the complete argument and numerical residual allowance.

## Actual full-action receiving operations

All free diagonals, edges, exact rational noise, original observations,
outputs and residuals are saved in results/RECEIVING.json. The two theta
operations use the SAME exact D and the SAME E, with different designs.
The error column is squared matrix Frobenius error divided by squared
absolute Frobenius action noise; it is an observation, not a fitted theorem.

| Original support | Construction | Blocks | Largest bichromatic order | Exact observed error/noise ratio |
| --- | --- | ---: | ---: | --- |
| 57 vertices, 73 edges; adjacent marks and mixed theta paths | Main block reset | 7 | 5 | 8673097/12312000 |
| Same 57-vertex support, same D and E | Explicit theta construction | 7 | 5 | 1246573/2052000 |
| 30 vertices, 39 edges; original non-theta atom, theta, C4 and C3 blocks | Main block reset | 7 | 5 | 132977/260496 |

All three are exact when noiseless. In the noisy calculations the projected
numerical residual is exactly zero; the raw observation residual is nonzero
and saved. Every actual bichromatic component is a certified spider. The
mixed support exercises an actual stop message: incoming edge (6,11),
outgoing cut 11, forbidden color 3, receiving child block 5.

An independent standard-library-only verifier reconstructs the blocks by a
different algorithm, checks original support and actual local profiles,
enumerates cycles on the small native blocks, supplies width-two bags,
checks all global component shapes, reconstructs full actions and solves
exact Fraction normal equations instead of using producer subtree sums.
All three operations passed. This verifies the realized examples; the
proof establishes the all-size conclusion. Internal verification is not
external scientific acceptance.

## A second, simpler operation on theta blocks

research/theta_explicit/ contains a separate table-free construction for
theta-block trees, even with arbitrarily many internally disjoint paths
per theta. Hubs are unshared; actual degree-two interior cuts belong to
two blocks; branch lengths are at least two. Remove one selected hub per
block and color the resulting tree with three colors, adding a constrained
endpoint correction when the incoming root lies on a length-two branch.
Give the removed hubs the fourth color. Both ordinary and special color
pairs are spiders with arms at most two, so the same inverse applies.

The complete proof and native code are included. This is not needed for
the broader bridgeless theorem and is not a claim that the theta subclass
is the whole intrinsic graph class. It provides an implementation that
avoids the fixed H8 certificate table on its own useful domain.

## Decisive failures and corrections

1. **An isolated, unflagged incoming edge alone does not reset depth.**
   A chain of b four-cycles has local star colorings with exactly these
   properties but a global bichromatic path on b+1 vertices. A middle cut
   of sizes a,d gives inverse squared constant at least ad/(a+d), which
   diverges. The saved b=8 original-action witness has action norm squared
   9/20 and unit cut coefficient. The complete message rule colors the
   same graph with largest component three. This rejects a rule, not all
   four-coordinate designs on those graphs.
2. **Plain depth coloring after hub deletion also fails.** A theta chain
   has unbounded special-color cut mass without the endpoint correction.
   The retained 12-block example has a cut 18/18, unit cut coefficient,
   action norm squared 1/9, and inverse squared lower bound nine.
3. The first theta diagnostic incorrectly chose a graph center when a
   diameter-three spider had unequal arms. The shape checker was corrected
   to use its unique branching vertex. The failed source and receipt are
   preserved; its unmeasured execution cost remains unknown.
4. Review clarified the main theorem's nontrivial-graph scope: K1 is handled
   separately. No receiving operation changed or was rerun for this wording.

FAILED_APPROACHES.md preserves these scopes and the older retired premises.

## Cost and comparison

The reference intrinsic preparation has O(n+m log m) comparison work with
canonical sorting, O(n+m) storage and one fixed certificate load. Coloring,
decoding and sparse output take O(nq+m) arithmetic/storage with q=4. Graph
preparation, action acquisition, bit complexity and numerical residual are
not free. The two-arm error constant is about 2.28825; it is a sufficient
operator constant, not a claim of sharp operator conditioning.

Seven distinct newly measured computation/checking bodies total about
0.15448 seconds wall and 0.15445 seconds process CPU. The maximum recorded
process RSS is 22,806,528 bytes. These figures exclude proof discovery,
inference, authoring, source inspection, integration, transport and an
unmeasured failed diagnostic. They are not the total cost of this research.
COSTS.md and results/COST_LEDGER.json give the exact boundaries and receipts.

Ordinary sparse-Hessian coloring and acyclic substitution already provide
the recovery machinery and earlier error analysis. Forest three-action
recovery, A_L's three-action operation, stronger star-color conditioning
when available, and the five-action full-class control remain serious
comparators. Cheap native entry assembly/AD may be preferable to queries;
the saved explicit matrices do not establish an application speedup.
No NIST, molecular, physical-performance or historical-priority claim follows.
The focused primary comparison is in research/PRIMARY_COMPARISON.md.

## Owned continuation decision

The next boundary is a bridge attached at an actually specified degree-three
vertex of a chordless atom, using its real residual degree-one budget.
The current degree-two one-root lemma does not cover this interface. The
next question is whether a realizable unflagged incoming channel can be
guaranteed there, or a different paid component invariant is needed.
This is the concrete step toward removing the bridge restriction. The
broader arbitrary-real four-versus-five problem remains open; the completed
construction and its constants will not be retuned as a substitute.

This checkpoint preserves the independently owned programme. No background
research, monitoring, external acceptance or repository integration is
asserted by producing or delivering the archive.

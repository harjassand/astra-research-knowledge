# A source-grounded challenge to proof-compression taste as Astra's selector

## Decision

The paper supplies a serious proposal-generation signal, not an established
replacement for Astra's autonomous scientific judgment. This audit identifies
two exact boundaries beyond the generic observation that a metric is imperfect:

1. The premise-expansion label rule described in the paper can assign different
   labels to the same conditional theorem problem solely because shared
   dependencies are expanded in a different order. Ordinary shared-DAG
   memoization removes this defect on the tested construction.
2. Even true shortest-proof savings can exhibit both complementarity and
   substitution. A theorem-by-theorem score is not automatically a sound
   acquisition policy for a scientific library. Charging acquisition and using
   a strong conventional joint-proof control removes an apparent benefit in
   the exact example tested here.

These results do **not** show that the paper's reported model measurements are
false or that its intrinsic metric is useless. They do not measure errors in
its actual training dataset, for which the needed raw expansion walks were
unavailable in this task. Nor do they establish a better scientific selector.
The exact tests are synthetic semantic countermodels, not fake Astra outcomes.

## Primary source and the claim actually challenged

Patel et al., *Learning to Discover Interesting Mathematics*, arXiv:2609.28603v1,
https://arxiv.org/html/2609.28603v1, especially Sections2–3, AppendixB.1 and
Discussion. The official HTML and recovered TeX were read. The relevant TeX is
preserved by the separate source investigator under
`../deep_hypothesis/taste_signal/paper_source/`.

The paper deliberately studies an intrinsic mathematical proxy, excludes
physical/social significance, and acknowledges that usefulness of its newly
generated theorems for future results is not yet clear. Its conjecturer emits
theorems, with creation of new definitions left for future work. This audit
respects those boundaries. The inference under examination is the proposed
use of such a signal as Astra's autonomous question selector, not a claim that
the paper promises civilisation-changing discoveries.

No shared-factor correlation calculation was repeated here; that is a distinct
analysis. No paper model was trained, evaluated or downloaded, and no scientific
owner's experiment was rerun.

## Result 1: expansion-order labels need not be conditional proof costs

### Exact construction

Consider an acyclic formal dependency system with primitive premise p and a
shared lemma L. Its proof from p has cost ell. There are m distinct lemmas
A_1,...,A_m, each with a one-step proof from L. The target T has a one-step
proof from all the A_i. The initial visible frontier is {A_1,...,A_m} and the
initial cost is one. Definitions are fixed and identical in every schedule.

Use exactly the described frontier update: remove an expanded lemma, insert
its dependencies, and add its proof cost. Shared frontier entries are sets,
but no already-expanded-node cache appears in the stated algorithm.

If all A_i are expanded first and L last, the terminal frontier is {p} and
the label is

    C_min = 1 + m + ell.

If A_1,L,A_2,L,...,A_m,L are expanded in that order, every later A_i reintroduces
L into the frontier. The terminal frontier is again exactly {p}, but the label
is

    C_max = 1 + m + m ell.

Every intermediate value 1+m+r ell, r=1,...,m, is attained by grouping the
A_i into r nonempty expansion batches. The shared proof DAG pays L once and
has cost 1+m+ell. For this formal system with these inference rules that is
also the shortest proof: each required node has a unique derivation.

Consequently the ratio of possible labels for an identical conditional task
is unbounded over this family. For ell>=m+1,

    C_max/C_min >= m/2.

This is not newline padding, exotic notation, an alternative theorem or a
change of available information. It occurs with a single fixed source DAG,
fixed legitimate proof costs, and shared dependencies. Replacing weighted
rules by unit-cost chains produces the same phenomenon with only unit steps.

### Executed exact check

`exact_tests.py` exhaustively enumerates all legal schedules by dynamic
programming over frontier states; it does not sample a few convenient orders.
With ell=20:

| Shared dependents m | Legal schedules | Terminal labels | Conventional shared-DAG cost |
|---:|---:|---|---:|
| 2 | 4 | 23,43 | 23 |
| 4 | 192 | 25,45,65,85 | 25 |
| 8 | 5,160,960 | 29,49,69,89,109,129,149,169 | 29 |

The eight-dependent case requires only758 dynamic-program states; the millions
of schedules are an exact combinatorial count, not millions of model runs.

### What follows, and what does not

As described, this expansion procedure measures the cost of a selected
materialization history, which need not be a function of the displayed target
and premises alone. The ideal shortest-proof value is a state function.
Training a model to predict archived labels can still be a useful and
well-defined statistical task, but accurate prediction of those labels is
not automatically accurate prediction of incompressible proof difficulty.

The paper already distinguishes source-code costs from ideal shortest proofs.
Our construction makes a further consequence precise: even on one fixed
shared dependency DAG, expansion scheduling can matter. An implementation
with an unreported visited-node cache, hoisting convention or extra history
in the input could avoid this specific example. We did not inspect such code
or raw records, so there is no claim that the paper's actual dataset contains
these inconsistent pairs or an estimate of their prevalence.

**Strong conventional correction:** preserve shared proof DAGs and memoize
each expanded declaration once, with context-aware proof costs if alternative
proofs are considered. This is an established representation discipline, not
an invented intelligence-amplification method. It fixes the demonstrated
accounting issue. It does not make proof length equal mathematical importance,
nor show a better learned conjecturer.

## Result 2: exact downstream savings are neither generally submodular nor supermodular

Let c(P) be the exact minimum proof cost for target T when premises P are
available, and define savings F(S)=c(P)-c(P union S). These costs obey premise
monotonicity and the usual proof-composition inequality. Yet neither of the
two familiar set-selection regularities follows.

### Complementarity

From primitive p, A and B each cost four. T has a direct proof costing five,
and a one-step proof from A and B together. Then

    c(empty)=5, c(A)=5, c(B)=5, c(A,B)=1,
    F(empty)=0, F(A)=0, F(B)=0, F(A,B)=4.

The second lemma has zero benefit alone and benefit four after the first. Thus
F(A)+F(B)<F(empty)+F(A,B), violating submodularity. A greedy singleton-savings
criterion can miss a useful complementary pair.

### Substitution

Keep the four-step A and B and five-step direct target proof, but give T a
one-step proof from either A or B. Then

    F(empty)=0, F(A)=4, F(B)=4, F(A,B)=4.

The second lemma is redundant. This violates supermodularity. Summing individual
savings double-counts the value of substitutes.

`exact_tests.py` computes both tables independently by Dijkstra search over
sets of derived facts, where derived lemmas can be shared. All rule costs are
positive and the systems are acyclic. These are exact finite proof-planning
examples, not intuition about hypothetical mathematical significance.

The point is not that a scalar estimate can never be useful. The point is that
the paper's conditional-proof axioms do not imply a reliable theorem-by-theorem
acquisition rule, and no standard greedy approximation guarantee follows from
those axioms alone. A future selector must confront actual complementary and
redundant scientific dependencies or accept this limitation.

## Acquisition costs and the strong conventional comparator

The complementary example can be misleading if A and B are handed over free.
Their acquisition costs eight. For one target, acquiring both then proving T
costs nine, whereas direct conventional proof costs five.

For n distinct targets with the same two-lemma construction, acquisition plus
continuation costs 8+n. A weak baseline separately pays five per target and
would suggest a growing 'amplification' advantage. Ordinary globally memoized
proof-DAG planning on the SAME known tasks and rules costs min(5n,8+n):

| Targets | Learn A,B then continue | Repeated direct proof | Strong conventional shared-DAG plan |
|---:|---:|---:|---:|
| 1 | 9 | 5 | 5 |
| 2 | 10 | 10 | 10 |
| 3 | 11 | 15 | 11 |
| 5 | 13 | 25 | 13 |

Every number is from the exact executed search. The proposed library-first
strategy never beats the strong comparator. This is a useful rejected
demonstration, not a failure of libraries: the comparator already recognizes
and preserves their ordinary reuse.

The model knows every inference rule and future target, so it does not measure
the difficulty of inventing A, B or their application. Actual scientific
invention may change the available rule graph; nothing here says its value is
captured by routine memoization. It does show why a claimed amplification
experiment must not manufacture gains by making its conventional baseline
forget discovered lemmas or by omitting acquisition cost.

## Consequences for Astra's actual mathematical capital

Pro1's new full-prefix dual, guarded-word mechanism and uniform nonlinear
transfer are complementary: the coefficient lower alone is not the reliable
rate theorem. Pro2's new coloring grammar needs both separation/connectivity
and bounded mass, with distinct inherited recovery and noise interfaces.
Their returns demonstrate those dependency structures, without providing a
calibrated numerical future-utility function. This audit assigns no numerical
interest or utility scores to them.

Both programmes also created useful mathematical objects and operations:
the selected input-word family and the recursively generated boundary-state
family. A theorem-only proposal system in a fixed vocabulary might assist
their proofs but does not yet reproduce that object-creation capability. This
is a scope difference explicitly acknowledged by the paper, not an empirical
failure inferred from its training setup.

The previous zero-use exclusion in the paper's correlation study also cannot
be turned into a deletion rule for Astra: a fresh foundational result may have
no recorded users before a later construction is conceived. Conversely high
recorded degree need not imply that future tasks still need the same route.
This observation supplies no alternative unmeasured relevance score.

## What to adopt, what not to claim

It is defensible to test a proof-difficulty/description-length signal as one
proposal feature, with the authors' stated intrinsic scope, a fixed proof
representation, shared-DAG accounting and a strong equally informed control.
It is not yet defensible to use it to override autonomous Pro question
selection or equate optimized interestingness with scientific significance.

A corrected objective based on expected future proof savings would require
actual future-task probabilities, joint dependencies, costs of finding and
formalizing useful lemmas, and the possibility of creating new formulations.
Those quantities are not measured here. Naming that objective does not solve
them or establish a superior selector. It simply makes the missing scientific
obligation explicit.

The decision-changing result of this audit is therefore a bounded **adoption
restriction and measurement correction**, not a new positive discovery method.
The strongest next positive test would ask whether an acquired operation
creates a new admissible route in an independent investigation that a strong
same-information control could not construct within the same budget. It must
measure the new route and its receiving consequence, not merely count proof
nodes or reward a larger intrinsic score. No such advantage was executed here.

## Reproducibility and cost

Run `python exact_tests.py --output /tmp/astra_taste_adversarial_results.json`.
This requires only Python's standard library and writes no owner source.
The original result is `EXACT_RESULTS.json`; its SHA256 is
56c9c2fa24d64b6579256e35b60a684bea265cda9be4029a1af844287db884eb.
The first run passed in approximately0.005 seconds of measured script-body
wall time. This excludes source reading, mathematical analysis, authoring and
review. No inference-cost advantage is inferred from that number. No paid
compute, hardware, outreach, downloads of model weights, new platform or
scientific-owner rerun occurred.

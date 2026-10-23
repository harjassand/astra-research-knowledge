# Independent semantic audit and all-context lift

## Scope and verdict

I read the frozen `meta_learning/learn_semantics.py`, its protocol, the native exact-count `active_ports.py`, the saved full transition and inference tables, and the result record. I did not execute the learner or the historical closure. A separate read-only calculation checked every saved transition against the literal count equations, the fixed-point conditions of the saved relations, and their agreement with the independently characterized maximal relations. `semantic_table_audit.json` records the resulting PASS and source bindings.

The implementation supports its stated result: ordinary finite partition refinement and greatest safety simulation recover the old occupancy congruence and support/flag order from the supplied exact count semantics. Changing the observation to include exact active counts refines the learned result appropriately. No code or mathematical defect was found at this scope.

The principal limitation is substantive: the scientifically useful port language, validity condition, available commands, degree cap, saturation rule and connection to actual graph colorings were supplied by earlier research. The learner reduces that language; it does not invent it from a raw graph or a scientific problem statement. The finite run is a mechanistic conventional-baseline test, not a hard general-invention success.

## 1. The exact finite algebra

An active port is

\[
s=(a,n,F),\qquad a\in\{0,1,2,3\},\quad n\in\mathbb Z_{\ge0}^4,
\]

with `1 <= d(s)=sum(n) <= 3`, `n(a)=0`, and `F` a subset of the colors with count exactly one. There are 24 degree-one, 60 degree-two and 92 degree-three labelled ports. Add one SAT4 marker, for a total of 177 states. Rejection is encoded separately as `-1`, not as an accepted state.

The command set consists of four extensions, 176 merges with active context ports, and 24 color permutations. Its 204 commands produce a 177-by-204 table with 36,108 cells. Omitting a merge-with-SAT4 column loses nothing: such a command always rejects and is already excluded by the source's admissibility rule.

Merge first requires equal terminal colors. It adds count vectors and unions flags, rejects degree above four or any flagged color whose combined count is at least two, and only then projects degree four to SAT4. Extension by color `x` requires `x != a` and `x notin F`; it creates a degree-one port of color `x`, with sole neighbor color `a`, flagged precisely when `n(x)>0`. Every command touching SAT4 rejects except color permutation, which fixes SAT4.

The native safety observation is `(a,d)` on active states and a separate label on SAT4. The changed observation is `(a,d,n)` on active states. This is explicitly an **active-port multiplicity query**; it does not purport to recover counts erased at an already saturated port.

## 2. Implementation inspection

The two inference functions receive only observations and transitions. Historical occupancy or subset predicates appear only in the post-inference comparison. The investigation knew the expected historical answer, so the procedure is not a blind discovery contest; nevertheless the inference algorithm itself is not supplied that relation.

The count enumeration is exhaustive because each individual count is at most three when total active degree is at most three. Flags range over all four-bit masks and native validity excludes flags on absent or repeated colors. The saturated state is added once.

The extension adapter fills an untouched second port with a dummy. Reading the actual native `extend` body confirms that its left action never inspects that port; it only copies it through. Consequently no hidden realizability property of the dummy affects the local transition. Its graphical interpretation still depends on the original module-interface proof, addressed below.

Partition refinement starts with observation equality and repeatedly separates states according to the complete vector of successor classes, keeping rejection distinguished. The finite sequence refines monotonically and its fixed point is the coarsest observation-preserving deterministic congruence. Class labels are assigned in fixed state order, so equality of label vectors is a valid termination condition.

Safety simulation starts with observation equality. In each synchronous round it removes `(s,t)` if a command successful from `t` fails from `s`, or if the successor pair has already been removed. This is a descending iteration of the standard monotone safety operator and computes its greatest fixed point. The relation direction is “`s` can replace `t` whenever `t` succeeds.”

The independent table audit verified all 36,108 transitions without importing the producer's native oracle or learner. It also checked successor-class equality inside each saved class and the simulation condition on every saved pair. All frozen protocol, learner and native-oracle hashes match. The full-pair comparison against the analytic characterization below has zero mismatches.

## 3. Concrete native realizers

### Rooted realizer

For every active `(a,n,F)`, create a root of color `a` and `n(c)` distinct neighbors of color `c`. For each `c in F`, the unique neighbor of color `c` receives one further leaf of color `a`. For unflagged neighbors, add no such leaf. This is a finite simple graph with root degree at most three, all other degrees at most two, and exactly the requested count vector and flags.

It is star-valid. For any pair `{a,c}`, either there are repeated root neighbors of color `c` and no flagged continuation, giving a star, or the color occurs once and may form a path of length two. Other bichromatic components have no edges. Thus no two-colored path of length three occurs.

### Genuine H8 module realizer

One can also realize each active local record at one terminal of an admitted connected two-terminal module, rather than rely on dangling rooted trees.

Use the prescribed root and neighbors. Along each arm choose the next vertex color to be `a` precisely for a flagged neighbor; otherwise choose it different from `a` and that neighbor's color. Extend the arms to one common remote terminal of color `a`. Give the remote terminal pairwise different neighbor colors and ensure that the preceding vertex of each arm has color different from `a`, making all remote flags zero.

The interior of each arm can be filled so that every successive triple has distinct colors. The directed graph of ordered pairs of distinct colors, with `(r,s) -> (s,t)` whenever `t` differs from `r,s`, is strongly connected on four colors. It has a three-cycle through every ordered pair, so paths can be lengthened while preserving prescribed endpoint pairs. Therefore the chosen starting and finishing pairs can be joined by sufficiently long paths.

Every arm is internally star-valid. At the first terminal, a potentially bad path crossing two arms would require a flagged color to repeat there, which native validity forbids. At the remote terminal, distinct neighbor colors and zero flags prevent such a path. Thus the entire coloring is star-valid.

With one, two or three internally disjoint sufficiently long arms, the underlying module is respectively a path, a chordless cycle or a chordless theta. It is generated by parallel composition of paths of length at least two, has nonadjacent terminals and disjoint branch interiors, has width at most two, and keeps terminal degree at most three. It is a native H8 module. This realizes every local record while retaining a legal remote port; it does not claim arbitrary **pairs** of local records can be simultaneously realized in one fixed module.

## 4. Exact maximality of the inferred relations

Let `N(s)={c:n_s(c)>0}`. For active ports with the same color and degree, define

\[
s\preceq t\quad\Longleftrightarrow\quad
N(s)\subseteq N(t),\qquad F(s)\subseteq F(t).
\]

SAT4 relates only to itself.

### Sufficiency

The source's native merge equation can be written, on valid children, as the hazard

\[
N_1\cap N_2\cap(F_1\cup F_2).
\]

Shrinking either support or flags cannot create a hazard. Exact terminal colors and degrees remain fixed, so color compatibility and degree admission also remain fixed. The output supports and flags are unions, hence preserve the relation. A degree-four result is checked before both sides become SAT4.

For extension, an accepted color remains outside a smaller flag set. The new neighbor support is the same singleton on both sides. A new flag is present when the added color lay in the old support, so shrinking support cannot create a flag. Permutations preserve subset relations. Therefore `preceq` is a successful-command safety simulation.

### Necessity by genuine one-command contexts

Suppose active states have the same observed color `a` and degree `d`.

If `x in F(s) \ F(t)`, extension by `x` is accepted from `t` and rejected from `s`. Any safety simulation is therefore required to preserve flag inclusion.

If `x in N(s) \ N(t)`, merge with the native context port

\[
u_x=(a,e_x,\{x\}).
\]

This context is an endpoint of a path2 whose endpoint colors are both `a` and midpoint color is `x`. Its color matches, and total degree becomes `d+1<=4`. From `t`, color `x` has combined count one, so the flagged merge is valid. From `s`, that color has combined count at least two and is flagged, so the merge rejects. Any safety simulation is therefore required to preserve support inclusion.

These native commands prove that no strictly larger observation-preserving safety relation is possible. The learned 973-pair relation is the greatest one. Mutual simulation forces both support and flags to agree; consequently the coarsest congruence is exactly the occupancy/degree/flag quotient, with 165 classes.

These single-command probes also explain why the saved refinement and simulation stabilize immediately after one proper refinement. The difficult scientific information was already encoded in a language where ordinary legal-context queries expose each retained feature directly.

### Changed exact-count observation

When `(a,d,n)` is observed, related states must already have exactly equal count vectors. Flag inclusion remains sufficient and is necessary by the extension probe. Mutual inclusion then forces equal flags as well. Therefore the greatest safety relation has exactly the native flag order at fixed counts, and congruence is identity on the 177 enumerated states. The saved relation has 349 pairs, matching this characterization.

The witness `(0,(0,2,1,0),0)` versus `(0,(0,1,2,0),0)` is a valid concrete query failure of the old quotient: it identifies the states, but the specified colored port has respectively two or one color-one neighbors. Both have the native realizers constructed above. The changed query restores this information without any change to the inference algorithm.

## 5. Lift to the actual module grammar

For two-port profiles, take the local relation at **both** ports, with active colors and degrees exact and saturated positions respected. The profiles must come from actual complete colorings of their modules. A single common color permutation acts on the entire two-port profile.

Extension changes only its selected port; the other is retained. Local simulation therefore lifts directly.

For a merge, first replace one operand while holding the other fixed. The learned safety relation preserves acceptance and the output relation. Then replace the other operand, using symmetry of merge. Transitivity combines the two steps. This proves the joint two-operand property without assuming that the learner was handed a binary monotonicity formula.

Series tests only its joined ports and leaves the two outer port records intact. Parallel tests the two pairs of endpoints. The original native-interface proof ensures these local tests are exact for disjoint child interiors and nonadjacent terminals, including modules whose two terminals have a shared internal neighbor. The relation therefore lifts to both operations, conditional on that source theorem.

The native algebra is equivariant under common color permutations. The unique greatest simulation and coarsest congruence are consequently equivariant. The experiment additionally includes all 24 relabelings as commands. Canonicalization must use one permutation of the whole profile and retain its witness; separate left and right relabelings would destroy correlations.

Induction on an admitted finite grammar expression now proves: replacing each child by an **actual realizing whole profile** that is smaller in the learned relation preserves every accepted continuation and produces a smaller output profile. It does not assert that the two endpoint projections can be realized independently.

## 6. Lift to sufficient family guarantees

A family guarantee has the form: for every target whole profile `t`, some actual whole child coloring has a profile `s` below `t`, possibly after one permitted common color relabeling. The same coloring must meet the requirements at both ports. The all-context argument preserves such existential guarantees when concrete transition witnesses identify compatible child profiles and relabelings.

This is the justification for antichain replacement of sufficient obligations. It is not automatic evidence that a nonempty universal family closure exists. The old closure certificate and its reconstruction obligations remain separate.

Nor does a failed pruned sufficient-family search prove graph noncolorability. That conclusion requires complete attainable leaf sets, complete choices through every admitted operation, and a valid dominance justification for every discarded realization. The finite local learner has not supplied these global completeness premises.

The Cycle9 three-`K_(2,4)` obstruction illustrates the distinction: each designated middle individually admits a good local state, while the central block cannot supply those states simultaneously at two different middles. No local simulation theorem repairs that failure by taking a product of separate marginal guarantees.

## 7. What raw native-graph refinement would require

The 177-state experiment does not start with raw graphs. It begins with a carefully chosen finite interface whose semantics were already proved. Replacing it by exhaustive graph samples would not automatically strengthen the result: agreement on bounded samples cannot establish all-depth continuation equivalence without a structural theorem.

For this particular star-coloring problem, a conservative raw-graph compiler is conceivable. Star validity forbids a two-colored path of length three. Given the degree-four bound and two boundary vertices, a colored joint radius-three boundary neighborhood has at most

\[
2(1+4+12+36)=106
\]

vertices before overlaps. A compiler could retain that entire joint neighborhood, exact boundary degrees and vertex-identification information, check the actual gluing operation, and then refine or minimize the resulting semantics. The degree bound and forbidden-pattern radius supply a finite starting alphabet. One must prove that every new forbidden path crossing a join is visible in the retained neighborhood, and that each operation can reconstruct the next retained neighborhood. The joint graph representation must preserve shared vertices between boundary neighborhoods and cannot replace them by two unrelated marginal neighborhoods.

This is a credible conventional upstream baseline, not a performed experiment or a cheap implementation. The conservative alphabet can be enormous, and deriving the correct locality/composition theorem is an additional scientific obligation. The supplied 177-state oracle has already compressed away most of that burden.

For other current Astra questions there is no comparable demonstrated small locality bound. Uniform incidence stability can depend on arbitrarily large cut mass despite short diameter. Simultaneous marked states require whole-module correlations. Sharp minimax rates quantify over moving supports, native multiplicities and full-return probabilities. A context learner must be given an appropriate finite or symbolic semantic contract before ordinary finite refinement can be applied. The current test has not shown how to construct those contracts automatically.

## 8. Cost and claim boundary

The saved result reports 165 classes and 973 simulation pairs for native safety, and 177 classes and 349 pairs for exact active counts, with no historical-relation mismatch. The approximately 0.0541 CPU seconds measure the body inside `main` through table construction, inference and adjudication. They exclude interpreter startup before `main`, final JSON serialization and printing, as well as inference, oracle invention, source retrieval and proof integration. This is not whole-process cost.

The 0.0541-second body and the preceding 149.250-second closure solve different obligations. Their ratio is not a speedup. No new closure was run, no improved graph theorem was proved, and no total research-cost improvement was measured.

The fair positive conclusion is that the specific reduction underlying the prior representation benefit can be recovered and query-refined by an ordinary finite semantic procedure once the scientifically adequate language has been supplied. The fair strategic implication is to place the next invention question upstream: constructing and validating useful scientific languages and operations from native models, or transferring such a capability to a genuinely new receiving obligation. The present result does not establish that capability.

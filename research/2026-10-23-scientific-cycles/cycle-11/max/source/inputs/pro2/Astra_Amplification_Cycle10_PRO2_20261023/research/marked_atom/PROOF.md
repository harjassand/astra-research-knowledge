# Cycle10 native specified-degree-two atom adapter

This is a bounded implementation contribution to Pro2's main gluing theorem.
It uses the unchanged Cycle8 grammar certificate and the unchanged Cycle9
66-family marked-midpoint projection. No closure search or old science suite
was rerun. Historical novelty is not asserted.

## 1. Exact interface

`prepare_marked_certificate(certificate_path, projection_path)` verifies the
two exact source hashes, loads the finite table, and indexes its transitions
ONCE. Reuse this object for all blocks.

`color_marked_atom(n, edges, mark, certificate_bundle)` takes an actual original
finite simple atom with IDs `0,...,n-1` and an actual degree-two vertex. It
returns its complete original edge list, four-coordinate color design, native
normal-form evidence, actual marked neighbor colors and actual far-repeat
flags. A containing graph can remap each block's actual IDs bijectively to this
local range, then map the returned colors back. This remapping neither chooses
a different attachment vertex nor changes the support.

Promised all-size coverage is the accepted Cycle9 class: two-connected,
chordless, treewidth at most two, maximum degree at most four. The present
code validates its actual returned star coloring and one-mark profile, so an
accepted output is usable even if a caller did not separately certify every
promised structural property. A failed suppression outside the promised class
is not claimed to be a complete recognition result for that wider input.

## 2. Correct preparation

Let the specified mark be v, with actual neighbors a,b. C3 is handled directly:
the three vertices receive distinct colors; v has two distinct neighbor colors
and no far-repeat flag.

For a nontriangle promised atom, a,b are nonadjacent. Delete v and its two
incident edges and add a **formal** edge ab in a temporary representation.
The marked-midpoint theorem proves this auxiliary graph two-connected and of
width at most two. Protect a,b while repeatedly suppressing another degree-two
vertex. Each current edge carries an ordinary edge/series/parallel expression
for exactly its original support. Its endpoints are never identified. If a
suppressed path meets an existing edge, the two expressions are placed in
parallel. This is the inherited exact width-two reduction with a changed,
actually specified protected edge.

The formal edge has only parallel ancestors because neither endpoint is ever
suppressed. Walk those ancestors and collect **all** their other siblings.
Remove the formal edge itself and join those siblings in parallel. This is
exactly H=G-v, with original terminal IDs a,b. There may be several siblings:
the auxiliary graph can be chorded even though G is chordless. Imposing the
old unmarked normalizer's one-sibling condition here would reject valid input.

Every a-b path of H closes through the original a-v-b path, hence is induced
by original chordlessness. The accepted normalization converts its ordinary
expression to H8: edge+edge gives path2, edge+module gives a left extension,
module+edge gives a right extension, and module/module joins retain their
series/parallel kind. An edge child of a parallel node is rejected. Every
module occurrence retains its original vertex IDs. The executable validator
expands the normal form's edge occurrences and checks equality with the exact
original edge list minus av,bv; putting back those two original edges must
recover exactly G. The formal edge is absent from this final form and never
enters a matrix action.

The two H-port loads are deg_G(a)-1,deg_G(b)-1, in {1,2,3}. Classification by
the accepted finite table therefore yields one of the saved 66 active-load
families. No new family or transition is searched for.

## 3. Actual color realization

For the classified H family, select the literal target and midpoint color
stored in Cycle9's saved projection. Check the selected target against the
unchanged certificate. Traverse the normal-form tree top-down, using only
the accepted literal child witnesses and their global four-color permutations.
Each port assignment is checked for consistency on its actual original ID;
the midpoint v receives the saved root color. Saturated internal ports are
resolved by their realizing children, exactly as in the inherited operation.

The selected target has distinct actual H-port colors A,B and a midpoint
color Z different from both. Its port support/flag bounds exclude Z from
both flags and allow Z in at most one port support. Consequently the restored
full original graph is star-four colored and v has neighbor support {A,B},
with at most one far-repeat flag. This is precisely the accepted one-mark
projection; it does not provide independently realizable profiles at multiple
marks of one block.

The implementation does not infer the actual profile just from a target mask.
After realizing the full original coloring, it computes every actual
neighbor-color multiplicity. An edge uv fails the star check when u has a
second neighbor of color(v) and v has a second neighbor of color(u), which
is equivalent to an actual bichromatic simple four-vertex path in a proper
coloring. At v it computes flags directly from the neighbors' actual other
neighbors and requires two distinct neighbor colors and at most one flag.

## 4. New load-bearing diagnostic

`run_diagnostic.py` calls the new adapter on six explicitly saved cases:

* a triangle with mark 2;
* C7 with mark 4;
* theta(2,3,4,5), marked on a length-two branch and in the long branch;
* A5, marked on a doubled short branch and in the long b-c connector.

These are new specified-root normalization operations, not a rerun of the old
finite closure or full benchmark. The short theta realization collects THREE
parallel siblings of the formal edge; the short A5 realization collects TWO.
Thus the changed context is exercised rather than merely copied in prose.
Both of these realizations have an actual one-flag marked profile, so the
new gluer must handle one-flag witnesses rather than silently assume D0.

A separate diagnostic check enumerates each actual simple four-vertex path,
then computes the marked profile from explicit adjacency. It does not use the
producer's multiplicity star-test or the inherited masks for these checks.
Every check passes. The diagnostic is authored by this same contributor;
it is an independently formulated check, not an independent human review.

## 5. Costs and limitations

The reference adapter sorts canonical edges and validates sorted expanded
support, costing O(n+m log m) comparisons with O(n+m) storage. Under the
degree-four cap the suppression queue and neighbor inspection, expression
normalization, classification, realization and actual-color checks each take
O(n+m) word/arithmetic operations. The fixed certificate's load/index/hash
cost is separate and must be paid once per receiving operation or charged
again if a caller unnecessarily reloads it per block. The interface supports
correct reuse; no graph recognition or input normalization is free.

The recorded six-case execution, including one-time fixed source loading,
took 0.025471879001997877 wall seconds, 0.025469771999999995 CPU seconds;
peak process RSS was 21,594,112 bytes. Included certificate preparation took
0.02339193399893702 wall seconds. These are body measurements only, excluding
authoring, proof discovery/review, source reading, tool latency, and packaging.
Those totals remain unknown. No unsuccessful new scientific run occurred in
this adapter contribution before the recorded pass.

This contribution alone is one-mark construction, not an all-depth gluing or
stable-recovery theorem. Pro2's principal line supplies the global argument,
full original actions, decoder and original absolute-noise accounting.

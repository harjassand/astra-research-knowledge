# Independent review of the all-depth finite certificate

This records the first, path2-leaf stage. The later arbitrary-path extension
has a separate final gate in GENERAL_CERTIFICATE_REVIEW.md; both stages and
their observed costs are preserved.

## Verdict

The 92-row constructive certificate passes every local obligation. Combined
with the exact port-interface lemma proved in this directory, it proves a
proper star-four coloring for every finite expression built from path2,
binary series composition, and two-/three-child parallel composition with
fresh outer stubs. Arbitrary series arity follows by binary association.
The larger 17-type closure table was independently verified first and is
retained as discovery evidence; the final upper theorem needs only the
smaller two-family certificate for that path2-leaf statement.

These are source-informed independent checks, not blind reviews. No root
producer module is imported by either verifier. There is no numerical solver,
optimization tolerance or inference from larger sampled graphs.

## The finite induction

Family L contains two canonical port signatures and family N contains nine.
A module has a family label when it realizes **every** signature in that family,
and hence every relabeling of those signatures. This is a guaranteed subset
of its attainable states, not a claim that the family is its exact state set.
In particular, an L-labeled module need not be a two-edge path.

The base path realizes L. The complete parent-label table is:

| Operation | Child labels | Guaranteed parent label | Requested rows |
|---|---|---|---:|
| S2 | LL, LN, NL, NN | N in every case | 36 |
| P2 | LL, LN, NN | N in every case | 27 |
| P3 | LLL, LLN, LNN | N | 27 |
| P3 | NNN | L | 2 |

There are 11 cases and 92 requested-state witnesses. Parallel child order is
irrelevant to the graph union; assigning the corresponding listed witnesses
back to actual children covers every ordering. Series order is retained.

For each requested parent state, its certificate row gives actual colored
child signatures. Each child's canonical signature belongs to its guaranteed
family. The rows satisfy the precise terminal-color matching, properness and
new-edge collision conditions in the interface proof, and their calculated
output colors and flags equal the requested parent signature exactly.

Thus, for any finite expression, compute its label bottom-up. To realize a
selected parent signature, use its row, apply the necessary global color
permutation, and recursively realize those child signatures. The child
induction hypotheses apply independently on disjoint interiors. The interface
lemma proves that the assembled graph is star colored. This closes the
all-depth obligation and handles both series parities.

The hypotheses still require distinct, nonadjacent degree-one terminals,
disjoint child interiors and exactly the specified identifications/stubs.
The degree bound is explicit: P_b creates joined degree b+1, and S2 creates
degree two. No assertion about all chordless atoms or arbitrary prescribed
boundary colors follows. The equal-terminal states in the certificate are
realizable states, not arbitrary assignments licensed without checking.

## Exact checks

`verify_two_family_certificate.py` independently pins both family lists and
checks all 11 cases and 92 rows. It minimizes over all 24 color permutations
to check canonical family membership. Its first execution passed, bound to
the 48,810-byte `star_four_certificate.json`, SHA256
105b5132564b4cd116d758644d1d08ace06cfd9d4e83ea95b8e4d493e87b78d9.

The earlier `verify_closed_table.py` independently checks 28 possible canonical
proper signatures and the exact 17 nonempty signature-set types. It validates
all 289 ordered S transitions, 153 P2 transitions and 969 P3 transitions,
with no missing/duplicate cases or discarded empty type. Every type is
reachable from path2. The first execution passed, bound to the 182,721-byte
`star_closure_attempt1.json`, SHA256
b5d28c716d18162cf6d23faa2599731862eba8b8d5e021cb9129e78e7fd2add4.

## A distinct lower within the star representation

The supplied graph expression

    L=path2; A=S2(L,L); C=P2(L,L); B=P3(L,A,C); G=P2(A,B)

has 17 vertices, 20 edges and maximum degree four. Independent direct
enumeration of all 49,320 labeled proper three-colorings finds zero star
colorings. Independent exact signature DP agrees, with raw state counts
L:12, A:30, C:24, B:24, G:0. The graph and all edges are retained in
THREE_STAR_OBSTRUCTION_RESULT.json. The positive theorem gives this same
grammar member a star-four coloring, so its star chromatic number is four.

This finite graph obstruction is exhaustive for star-three vertex colorings.
It is not an acyclic-three or arbitrary-real three-query obstruction. The
larger full tw<=2, Delta<=4 four-versus-five question remains separate.

## Recovery consequence and its boundary

For a proper star coloring, every bichromatic component is a star or a single
vertex. In each star choose the leaf action cell to recover its edge; a
two-vertex component can use either endpoint by a fixed rule. All chosen
edge cells are distinct, and the diagonal cells are separate because the
coloring is proper. Hence a direct supported symmetric reconstruction obeys

    ||Dhat-D||F^2 = sum(diagonal errors squared)+2 sum(edge errors squared)
                 <=2 ||E||F^2,

and therefore ||Dhat-D||op<=sqrt(2)||E||F. Every coordinate query row has norm
one. This argument applies to arbitrary free diagonals and all real noise,
using complete original actions. It is the ordinary star-color direct decoder;
the new finite graph construction supplies its admitted input. A numerical
implementation must additionally account for acquisition/assembly and any
uncertified arithmetic. The owner's receiving calculation is separate from
this mathematical interface verification.

Internal certificate validity and the graph-specific lower do not establish
historical novelty, external acceptance or practical application speedup.

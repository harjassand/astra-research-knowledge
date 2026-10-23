# Final independent gate: arbitrary path leaves and both series parities

## Verdict

The final four-family, 200-witness certificate passes. It establishes the
proper star-four coloring induction for arbitrary path leaves of length at
least two, arbitrary finite series arity at least two, and the retained
two-/three-child parallel production with new outer stubs. The terminal
degree-one, nonadjacency and disjoint-interior hypotheses of the port lemma
remain essential. No coverage of all chordless degree-four atoms is inferred.

This is a substantive extension of the separately preserved two-family/path2
certificate. The prior scope warning was correct: a path3 leaf realizes neither
entire old family L nor entire old family N. Root added its true leaf family
and a fourth guarantee family; the new complete table supplies the additional
transitions. This review checks the delivered witnesses directly, not the
invariant-search method or a claim that every possible boundary state works.

## Exact finite obligation

The families A,B,C,D have sizes2,4,9,15. A is the old two-state leaf family;
C is the old nine-state guarantee family. Independent enumeration of actual
path colorings confirms:

| Leaf | Proper labeled four-colorings | Star labeled four-colorings | Canonical port states |
|---|---:|---:|---:|
| Two-edge path | 36 | 36 | A, exactly2 |
| Three-edge path | 108 | 96 | B, exactly4 |

For each module, its assigned family means every listed port signature is
realizable, including every color permutation. It need not be the exact full
set of signatures, and a family label does not denote a syntactic graph kind.

The certificate has all16 ordered binary-series label cases, all10 unordered
P2 cases and all20 unordered P3 cases:46 cases total. Every case chooses one
nonempty parent family and provides one row for each of its requested states,
200 rows overall. The independent checker pins all four family lists, checks
that every case appears exactly once, and checks that every required row occurs
exactly once with no omitted output. Every colored child signature belongs to
the appropriate family orbit. Every row satisfies the exact interface lemma's
properness, identification and bad-edge conditions, and computes the parent
colors and flags exactly as recorded.

All four labels are reachable from the actual A/B leaves. No empty family was
discarded, and the proof does not assume the truth of a solver success flag.

## All-depth and arbitrary-length consequences

Induct on a finite expression over path2,path3,S2,P2,P3. The leaf checks give
the base cases. For a production, choose the certificate case determined by
its child labels. For every requested parent signature, its row prescribes
admitted colored child signatures. The induction hypotheses realize those
signatures, and the exact interface lemma shows their union is star colored
and has the specified parent state. Global color permutations are harmless
because the entire proper/star predicate and the flags are color symmetric.
Parallel child ordering is handled by assigning the listed witnesses to the
corresponding actual children; binary series order is retained explicitly.

Every integer path length l>=2 is2a+3b with a>=0 and b in{0,1}: take b=0 for
even l, and b=1 for odd l. A path of that length is the series composition
of a path2 leaves and b path3 leaves. The one-leaf cases need no series node.
This decomposition introduces no extra edge or vertex beyond the original
path: segment endpoints are identified at the corresponding path vertices.
Every series arity at least two can then be associated into binary joins.
The output cost and extra expression nodes are linear in the expanded path
length and the supplied series arity; no free recognition is assumed.

The same ordinary star-color direct decoder therefore gives the unchanged
full-action guarantee ||Dhat-D||op<=sqrt(2)||E||F with four coordinate queries
and unit row norm. This follows from the proof in CERTIFICATE_REVIEW.md and
does not depend on observing a favorable noise realization. Root's complete
receiving calculation remains a separate implementation obligation.

## Checked source and measured gate

Actual source: `results/general_star_certificate.json`,115,016 bytes,
SHA256 b0ffc8e13badf6faedff7dd821407549e3f4745f7de8a15e6cd765e5163e8fb4.
Independent executable: `verify_general_certificate.py`.
Receipt: `GENERAL_CERTIFICATE_RESULT.json`.

The first recorded gate passed in0.009272629999031778s wall,
0.009272281s CPU, peak RSS11,403,264bytes. This includes reading and checking
the actual certificate and exact leaf enumeration. Startup, receipt writing,
scientific source reading, authoring, proof review and messages are additional
and unmetered. The larger earlier closure and first two-family gate remain
charged in COSTS.md; they are not erased by the smaller final certificate.

The 17-vertex star-three exclusion remains valid and is independent of this
extension. It establishes a star-color count, not a lower against arbitrary
real three-query recovery. Internal validity is separate from historical
priority, external acceptance, practical performance and the full four-query
partial-two-tree question.

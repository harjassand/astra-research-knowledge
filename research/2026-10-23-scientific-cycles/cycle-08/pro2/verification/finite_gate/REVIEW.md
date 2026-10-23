# Independent literal finite-certificate gate

Cycle8 PRO2, 22 October 2026. Reviewer: `/root/cycle8_finite_gate`.
This is a focused check of the load-bearing finite obligation. It did not
repeat the producer's family discovery, the 220-family intermediate search,
the predecessor suites, or any physical/molecular benchmark.

## Verdict

**PASS, within the exact supplied-expression grammar and the proved boundary
semantics.** The complete literal certificate was accepted on the first run by
`verify_certificate.py`, which imports no producer module. It independently
uses set-valued port data, enumerates the actual two-edge-path leaf, applies
the exact local S/P/U predicates, and checks all color relabelings as single
global four-color permutations across both ports of a child.

The authenticated object is:

* `results/loaded_star_certificate.json`
* 982,625 bytes
* SHA256 `63f4cdfd7ccc3b3159782a28a144a199422a315975aa207e5d144e8659e53525`

It has 73 nonempty family guarantees and 608 canonical target profiles.
Every admitted operation/family case appears exactly once:

| Kind | Cases |
|---|---:|
| Left extension | 69 |
| Right extension | 69 |
| Ordered binary series | 2,521 |
| Unordered binary parallel | 566 |
| **Total** | **3,225** |

The checker accepted all 11,142 explicit transition witnesses. Each target
of the selected parent family occurs exactly once in that case. Two leaf
witnesses realize the selected leaf guarantee, checked against a direct
enumeration of all 36 labeled proper/star colorings of the three-vertex path.

No floating arithmetic, optimization success status, sampled graph depth or
truncated transition set is used as a certificate.

## Independent checks performed

The checker requires a nonempty, degree-homogeneous target list for every
family. It validates active colors, positive actual degrees, color masks,
properness at a port, flag inclusion in neighbor support, and the local
multiplicity feasibility of each target. Degree-four records must be the
exact `SAT4` representation: no visible color, support or flag constraints.

For each child witness, membership is checked in the **whole global color
orbit** of the declared family. The checker does not independently permute
the two terminal records. Actual joined colors then have to agree literally.
The selected parent target also uses those same actual labels; the output
must have its exact visible colors and exact degrees, with neighbor supports
and far-end flags contained in the target bounds.

A merge is rejected if its summed actual degree exceeds four or if a color
belongs simultaneously to both child neighbor supports and to either
far-end flag set. A newly saturated port is projected only **after** this
test. The checker disallows a saturated child port in a joined position.
For a terminal extension it checks degree at most three, a different new
terminal color, and absence of that new color from the old far-end flags.
The new single-neighbor flag is calculated from membership in the old
neighbor support.

The set of required family cases is constructed independently from the
degree pairs. There is no reliance on the producer's case count: every
degree-admissible left/right extension, every ordered series pair, and every
unordered parallel pair is required. Missing, duplicated, inadmissible and
incorrectly ordered cases are rejected. The parent's load pair is checked
against the actual operation independently of its witness.

## Why the finite gate gives an all-depth implication

The mathematical premises are the full exact port lemma, the `SAT4`
congruence, and the support/degree quotient and monotonicity proof in the
adjacent `port_lemma/` directory. I read those arguments. Their relevant
content agrees with the independent set-based transitions above:

1. Already star-valid child realizations can create a new bad incident edge
   only when the same neighbor color appears on both sides of a join and
   some such incident edge has a far-end repeat.
2. Nonadjacent terminals and disjoint child interiors ensure actual degree
   sums, preserve opposite-port records, and prevent changes to internal
   neighbors' colored adjacency lists. Shared interior neighbors of a
   module's two terminals remain harmless under those hypotheses.
3. A degree-four terminal cannot later be merged or extended under the
   positive-load degree-four budget. Its hidden color is existentially
   unspecified; it is never an arbitrary prescribed fifth color.
4. Holding visible terminal colors and actual total degrees fixed, reducing
   neighbor-support and far-end-flag sets preserves every accepted S/P/U
   transition and reduces the resulting upper profile. Concentrated actual
   multiplicities remain safe because child realizations were already
   star-valid; the quotient does not certify arbitrary syntactic records.

A family's guarantee is therefore: for every listed target, some actual
star coloring has the exact visible colors and degrees, and no larger
neighbor-support/flag sets. The direct leaf checks establish that guarantee
at the base. At an internal node, its literal witness requests child targets
whose guarantees hold by induction. The exact transition and monotonicity
lemmas glue those actual child realizations into the requested parent bound.
Each admitted family combination has a case, and each selected parent target
has a witness. This proves the guarantee at every finite expression depth.
Nonemptiness of all selected families then supplies an actual root coloring.

Arbitrary path leaves of length at least two can be generated by a two-edge
path and actual one-edge terminal extensions. Series and parallel arities
greater than two can be processed in binary order; positive loads and the
final degree-four cap imply every intermediate load is admitted. These are
descriptions of the original graph's actual edges and identifications, not
permission to add artificial subdivision vertices or delete exterior stubs.

Thus the finite certificate proves a star-four coloring for the stated
augmented grammar at all finite depths. With the separately retained
triangle-free star-decoder theorem, that coloring gives the claimed original
full-action inverse. This gate does not re-prove that inherited norm bound or
verify an implementation's later action/output data.

## What this gate does not establish

It does not prove coverage of every chordless series-parallel atom or every
treewidth-two, degree-four support. It does not assume arbitrary terminal
colors, adjacent terminals, overlapping children, zero-load ports, later
constraints on saturated-terminal colors, or a free graph recognizer.

It does not prove a universal three-query lower bound, an arbitrary-real
four-query obstruction/optimality theorem, or a runtime advantage over the
five-query full-class comparator. Historical priority, external acceptance,
physical usefulness, source delivery and repository integration are separate
questions. The certificate is a constructive mathematical existence object,
not a comparison of research strategies.

## Reproduction and cost boundary

From the package root:

```
python verification/finite_gate/verify_certificate.py \
  results/loaded_star_certificate.json \
  --output independent_finite_gate_result.json
```

The observed gate body took 0.2002076990029309 seconds wall and
0.19994599100000002 seconds CPU; maximum process RSS was 37,216,256 bytes.
The body includes certificate file read/parse, all literal checks and the
input hash. It excludes process startup and final receipt serialization.
These are the gate's costs only. Proof reading, inference, checker authoring,
review writing and integration were not individually metered and remain
unknown. The producer's successful and unsuccessful search costs must remain
additional; this short gate does not replace discovery cost.

The machine receipt is `RESULT.json`.

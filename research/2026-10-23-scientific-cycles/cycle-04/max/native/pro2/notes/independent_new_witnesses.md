# Independent exact verification of the new frozen witnesses

Checker author: `/root/fan_port_lemma`, 22 October 2026 Australia/Brisbane.
Checker: `checks/verify_new_witnesses.py`.
Receipt: `results/independent_new_witnesses.json`.

The checker imports only Python standard-library modules and no producer
source. It was authored after inspecting the fixture schema and mathematical
obligations, and then run once on the five frozen files. All five passed.
No producer regeneration, original benchmark, historical science replay,
floating eigensolver or precision sweep was performed.

## Exact common acceptance conditions

For each file the checker independently parses canonical rational strings,
validates every graph edge and supported matrix coefficient, checks every
query row's squared norm against one, and evaluates every actual action entry
using Fraction arithmetic. It recomputes the exact action norm, verifies that
the claimed operator lower bound is bounded by an actual matrix-entry square,
and checks the inverse-ratio identity against the actual action.

Input binding is SHA256 of canonical JSON `{n,q,edges,X}` with sorted keys and
compact separators. The receipt also pins the complete witness file bytes
and SHA256, including D and metadata. This binding identifies these supplied
exact fixtures; it makes no claim about an external NIST or physical input.

## Core-cancellation fixtures

The checker reconstructs the full root and attached-child support from the
declared graph parameters, validates the vertex partition and port incidence,
and checks the exact principal core matrix. Every root action row is zero.
It verifies each declared port frame is orthonormal, computes its Gram from
all actual child query rows, and checks `A_v=gram_scale P_U` exactly. Grouping
identical rows is an exact counting optimization, not sampling.

It verifies each core action lies in its declared port, and every added spoke
coefficient equals `-<query_row,core_action>/gram_scale`. It independently
reconstructs all permitted coefficients and compares them with the saved D.
The variable count and constraint count match the claimed dimension formulas.

Constraint ranks are independently computed by integer row elimination after
clearing rational denominators. The checker uses standard coordinate rows of
the orthogonal-complement projection, rather than importing the producer's
complementary frame or RREF routine. Redundant projection rows preserve rank.
Identical small core systems in two fixtures share one exact rank computation.

Results:

| Fixture | n | q | Constraint rank | Actual action squared | Operator lower squared |
|---|---:|---:|---:|---|---|
| core_t2_narrow | 295 | 5 | 17 | 1/96 | 1 |
| core_t2_large | 9223 | 5 | 17 | 1/3072 | 1 |
| core_t3 | 1651 | 9 | 69 | 3577339311297738207621692227014426527 / 19868704608183803595524398386636398592 | 1 |

The largest fixture therefore certifies inverse quotient at least
`sqrt(3072)=32 sqrt(3)`. This is an exact fixed-design witness, not an
all-design empirical conclusion or a performance comparison to the old dense
spectral calculation.

## Cone lift

For `cone_three_copies.json`, n=37 and q=3, the checker reconstructs each
local B, Z and R from the actual query rows. It computes the local constraints,
checks the maximum-normalized mixing coefficients and their exact cancellation,
and independently forms every block, apex-border and apex-diagonal entry of
the lift. The mixing constraint rank is two. The full apex action and every
last-coordinate action are exactly zero.

The fixture uses raw rational local matrices; the checker does not silently
pretend that each has operator norm one. Its final bound uses an actual
principal matrix-entry square. It verifies action squared62500/81 and inverse
ratio squared55225/5184. The normalized universal coning theorem is a separate
analytic statement in the proof and coning review.

## Low-rank projection and the actual-input bridge

For `low_projection_actual_input.json`, n=1159 and q=5, the checker binds the
selected child to the actual full graph and verifies that D has no support
outside that child. It checks that the apex query row is unchanged, the
projected path has rank two, the full projected block has rank three, and all
projected query rows satisfy the cap. Orthogonality to the span of projected
path rows verifies the stated path projection directly.

The exact input perturbation norm squared is

    384000000/1000002000001.

Both the projected action and the nonzero perturbation action are recomputed.
Their sum is checked entry by entry against D acting on the ORIGINAL saved
query matrix. The exact cross inner product in this fixture is zero. The
checker also verifies the squared Frobenius matrix-norm perturbation allowance.
Thus it does not certify only a separately projected query block and omit
the connection to the actual data.

## Deliberate tampering

Four modified in-memory copies were rejected:

1. A changed supported coefficient: rejected by the actual action norm.
2. A new forbidden-support coefficient: rejected by support validation.
3. A row cap violation with the canonical input hash updated: rejected by the
   actual row cap, independently of hash mismatch.
4. A projection-error norm understated as zero: rejected by the recomputed
   exact input error.

The original frozen files were not edited by these tests.

## Observed costs and limits

The one checking body, including file reading/parsing, exact ranks and all four
tamper rejections, took **0.884272505 seconds wall**, **0.883769656 seconds CPU**,
with **36,524,032 bytes peak RSS**. Per-file wall scopes in the receipt are
subsets of this body and must not be added again. There was no failed checker
run or repeated numerical attempt.

The checker source SHA256 at this run is
`bb24d13f6d9b54029c8509785f734bc6464ebae588565231748a8fe84b13fb60`.

Source reading, authoring, proof review, model inference, service latency,
monetary cost and energy are additional and not fully metered. The checker
verifies the saved examples and their exact mathematical identities. The
universal all-design claims depend on the complete proof, not on the finite
fixture results. Historical originality, implementation efficiency and
practical spectral performance are separate questions.

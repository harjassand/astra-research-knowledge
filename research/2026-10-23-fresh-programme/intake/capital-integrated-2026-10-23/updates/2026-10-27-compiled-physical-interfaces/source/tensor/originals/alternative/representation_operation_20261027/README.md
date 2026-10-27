# Exact contraction without a supplied gauge

`compiler.py` accepts a closed loopless planar trivalent binary tensor network,
recognizes the generic heterogeneous parity-gauge class described in
[PROOF.md](PROOF.md), and returns its exact rational contraction. When the
contraction is nonzero it also returns normalized ORIGINAL-edge bit weights.
The input contains no decomposition, gauge or answer. Parallel edges and
multiple connected components are supported.

This is an exact research implementation using only Python's standard library.
The completed independent mathematical and implementation acceptance is frozen
in [review/REVIEW.md](review/REVIEW.md); its code hashes are in
[review/INTEGRATION_CHECK.json](review/INTEGRATION_CHECK.json).

## Run

From this directory, with Python 3.11 or later:

```sh
PYTHONINTMAXSTRDIGITS=0 python3 compiler.py INPUT_SIGNED6_EVEN.json -o result.json
PYTHONINTMAXSTRDIGITS=0 python3 compiler.py your_input.json --unbounded-prime-search -o result.json
```

The environment setting removes Python's configurable decimal-integer
conversion limit. It is required for the all-explicit-exact-input completion
contract when integers exceed that interpreter limit; it does not remove time
or memory limits. Without it, sufficiently large valid inputs or output
receipts can fail during decimal parsing/serialization. In an already running
Python process, call `sys.set_int_max_str_digits(0)` where that API is available
before parsing the input or calling this module. Use this configuration only
for the authorized exact input whose resource use you intend to allow.

The default `--prime-budget 200` caps the number of candidate primes and can
return `UNKNOWN`. `--unbounded-prime-search` enables the proved terminating
algorithm on admitted inputs. `--partition-only` omits the original-edge
weights. The budget counts rejected as well as accepted primes.

API, after making this directory importable:

```python
from compiler import compile_network
result = compile_network(data, prime_budget=None, marginals=True)
```

`None` selects the mathematically complete prime search; an integer selects a
work cap. This is a research API with the valid-input contract below, not a
hardened parser for arbitrary hostile JSON or Python objects.

## Input contract

Use a JSON object with `tensors` and `edges`; `name` is optional metadata.
There are exactly eight entries per vertex, indexed in lexicographic order
`000,001,010,011,100,101,110,111`. Entries are explicit JSON integers or exact
rational strings such as `"-17/31"`. Supply expanded integer numerators and
denominators, with nonzero denominators. No binary floating input, abbreviated
scientific-notation encoding, implicit tensor oracle or approximate data is
part of the exact input/resource theorem. The bit length in the theorem is
that of these expanded rational integers and the explicit graph.

An edge `[v, i, w, j]` connects port `i` of vertex `v` to port `j` of vertex
`w`. Vertex indices start at zero. Ports `0,1,2` are the supplied cyclic planar
rotation at every vertex. Each port occurs in exactly one edge; loops are
excluded. Parallel edges are distinguished by their port IDs. The expanded
embedding is checked; an arbitrary ordering is not automatically a planar
embedding. Contraction is bilinear, with no complex conjugation. The included
input JSON files show the complete format.

The admitted generic class requires nonzero local 2x2x2 hyperdeterminants,
nonzero four CP pairings on each edge, and the local exact balance predicate
`beta_v=1`. Within that nondegenerate class the predicate is necessary and
sufficient for compatible independent-edge parity bases. It does not recognize
all tractable networks. Outside the scope, `UNKNOWN` makes no hardness claim.

## Output and boundaries

`EXACT` includes a rational-string `partition`, exact local-recognition
receipts, checked modular residues, original-input height and CRT moduli.
`normalized_edge_weights` follows input edge order and has columns for bits
zero and one. It is null when the exact partition is zero. Zero partition does
not mean all unnormalized pin weights vanish. Signed inputs can give weights
outside [0,1]; these are probabilities only when the original tensors are
nonnegative. The output flag records this distinction.

`UNKNOWN` includes the reason and any partial receipts; it never exposes an
incomplete CRT value as an exact answer. Some malformed/unsupported inputs
receive `INVALID_OR_UNSUPPORTED_INPUT`; general parser-hardening is outside
this implementation's contract. A failed balance test does not rule out
another tractable representation. No noise robustness, sampling, self-loop,
higher-arity or physical-model acquisition guarantee is supplied.

`CHECKPOINT.md` is retained derivation history, including an earlier proposed
Fp4 route. The final evaluator uses Fp2; `PROOF.md` and this README govern the
completed version. No historical-priority or practical-speed advantage is
claimed. See [REPORT.md](REPORT.md) and [SOURCES.md](SOURCES.md).

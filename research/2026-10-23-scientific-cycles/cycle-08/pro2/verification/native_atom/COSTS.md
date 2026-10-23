# Cost of the independent native atom gate

One first-pass execution of `check_native_atom.py` passed. The independent
gate measured:

| Resource | Observed value |
|---|---:|
| Body wall time | 0.011307761000352912 seconds |
| Body CPU time | 0.011303685 seconds |
| Peak process RSS | 14,811,136 bytes |

The timed body includes pinned source reads/hashes, importing the separate
independent arithmetic helper, complete loaded-normalization validation,
actual finite graph-class diagnostics, the single nine-vertex exact
full-action receiver, exact rational LDL checking, the distinct cycle/C3
structural branches, and enumeration of the 243 C5 color assignments.
Process startup and final result JSON serialization are excluded.

No earlier receiving record, finite closure gate, producer search, old
benchmark or old scientific suite was rerun. The helper import defines
functions but invokes neither its main routine nor its old record checks.

These are verification-body costs only. Reading, reasoning, independent
checker design, authoring, mathematical review and integration costs were
not instrumented and remain unknown. The producer's new native receiving
and branch costs are separately recorded in
`results/NATIVE_ATOM_COSTS.json`; this gate does not overwrite or absorb
them. A short check time is not the cost of discovery.

The producer implementation sorts canonical edges and therefore charges
`O(n+m log m)` preparation, rather than claiming that its potential linear
structural algorithm was already implemented. The independent checker
uses exhaustive cycle enumeration and bounded-size elimination search for
this actual graph; that diagnostic is not advertised as an efficient
general graph recognizer or production normalization algorithm.

No floating-point numerical decision is used for the graph, source,
action, inverse, norm or PSD conclusions. Timer values are observational
measurements only. Exact arithmetic bit growth, original action acquisition
and practical downstream performance are separate obligations.

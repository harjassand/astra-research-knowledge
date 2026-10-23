# Receiving and replay instructions

Read RESULT.md, PROOF.md and CONTINUATION.txt first. Python 3.12 and its standard
library suffice for all NEW scientific sources. No solver, paid service,
NumPy/SciPy, graph package or predecessor benchmark run is required. The full
scientific certificate and saved rational inputs are part of this package.

## Verify the exact payload

From this archive's top directory, before adding files to it:

```
python src/verify_payload.py
```

This checks source transport hashes only. It does not prove the mathematics.
The immutable manifest excludes itself and Python bytecode caches. Write replay
outputs OUTSIDE this directory so they do not change the received payload.

## Small independent mathematical and receiving gates

```
python verification/finite_gate/verify_certificate.py results/loaded_star_certificate.json --output ../cycle8_finite_gate_replay.json
python verification/receiving/verify_receiving.py --output ../cycle8_receiving_replay.json
python verification/native_atom/check_native_atom.py --output ../cycle8_native_atom_replay.json
```

The first checker validates every literal finite case with independent set
algebra. The second binds and checks the A5 and mixed16 original-action
records using analytic star least squares and exact PSD reconstruction. The
third binds the native edge-list input and every actual normal-form node,
then checks its original-action inverse. It imports only the earlier
hash-pinned independent arithmetic helper, not producer code, and does not
rerun those earlier receiving records. All gates already passed; a receiver
may run them to establish its own check rather than treating delivery as one.

Read verification/port_lemma/ for exact transition, saturation, occupancy and
dominance proofs; research/structural_scope/ALL_CHORDLESS_ATOMS.md and
verification/atom_scope/ for the all-size graph theorem and focused challenge.
Finite graph tests do not replace those universal arguments.

## Apply the operation to a genuinely new input

For a supplied loaded expression, put src on Python's import path and call
loaded_recovery.build(spec). Child references are topological; repeated child
IDs mean DISJOINT copies in the expanded graph. Expression size and expansion
cost are both charged. The original support must actually be that expression.

For a native atom in the theorem, call:

```
from atom_normal_form import prepare_atom, color_native_atom
normal_form = prepare_atom(n, original_edges)
graph_and_colors = color_native_atom(normal_form)
```

The normal form preserves original vertex IDs and support. This operation
may reject graphs outside the promised class; it is not an arbitrary support
recognizer. C3 returns its separate three-color identity design. On a supplied
nontriangle atom, acquire ALL FOUR original matrix actions for the returned
coordinate colors, prepare coordinate_decoder.prepare, and call decode on
the full observed action. On C3 use symmetrization of the three-column action.

Do not apply the decoder to reduced observations, assume a bound on D deltaX
from row normalization, or call unmeasured floating residual zero. PROOF.md
Section7 gives the complete numerical boundary. Acquisition cost belongs to
the receiving action source. These explicit sparse synthetic operations do
not provide an application-specific action oracle.

## Reproduce discovery only for a changed scientific obligation

The search scripts and all actual failed/resource-limited records are retained.
Their status is not required for checking the literal proof object. Do not
rerun the 300.8656 second sequence as an automatic acceptance ritual. In
particular, do not replay unbounded transient caches that reached 2.185GB merely
because the source is present. Current bounded-cache/resume behavior and the
exact occupancy representation are documented in FAILED_APPROACHES.md.

The first positive 220-family closure and the later 73-family result are both
preserved. The final source and literal witness generator are executable;
no historic cost is erased by the smaller final proof.

## Source continuity and integration

sources/ contains the exact native Cycle7 ZIP, unchanged selected predecessor
files and exact retrievable Cycle5 route. No inaccessible bundle is needed to
check this checkpoint's self-contained new proofs, certificate or operations.
The full predecessor remains available through the stated private identity.
Max retains integration authority. Upload/readback, recipient reading,
scientific acceptance and repository integration are distinct events.

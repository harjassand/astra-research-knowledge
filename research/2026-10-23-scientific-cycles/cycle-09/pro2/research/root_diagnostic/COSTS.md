# Root diagnostic costs and attempts

The parent supplied the three-K2,4 candidate. The child independently
constructed its original labeled support, proved the marked-root
obstruction, and wrote a complete color enumerator and graph checker.
This is independent validation, not a claim to have discovered the
candidate.

One execution of `check_k24_path.py` passed:

| Resource | Observed value |
|---|---:|
| Body wall time | 0.016963791999842215 seconds |
| Body CPU time | 0.016960407999999996 seconds |
| Peak process RSS | 11,665,408 bytes |

The body includes construction and exact support checks on three graphs;
all-cycle chordlessness checks; verification of actual width-two bag trees;
complete canonical star-four enumeration on the one-, two-, and three-block
graphs; a distinct raw enumeration of all 4096 one-block assignments; the
complete degree-two root compatibility table; and input serialization.
Process startup and final result serialization are excluded.

The candidate search tree needed only 142 nodes and 559 proposed color
assignments, but that is not discovery cost. Reading, mathematical reasoning,
code design, proof authoring, review and integration costs were not measured
and remain unknown.

## Attempts that affected direction

Before receiving the specific graph, the child classified the four possible
degree-two rooted hazard types and their compatibility. A wider small-atom
library (cycles, theta graphs, A_L and the earlier native atom) was planned
but **not executed**. The concrete candidate made that search unnecessary;
no cost or evidence from an unperformed search is claimed.

One K2,4 and a two-block join do not obstruct star-four coloring. They were
checked as positive controls and have 192 and 144 labeled star-four
colorings, respectively. Their exact profile information explains the
failure at three blocks: each isolated middle can individually be made
B0, while the two-block join forces every unshared middle to B2. Separate
root feasibility does not give simultaneous feasibility.

No old scientific suite, atom closure, owner numerical benchmark, native
receiver, or finite certificate gate was rerun. No global closure search
was launched. No numerical approximation or solver success status is
used in any coloring, graph-class, or incompatibility decision.

## Replay

From the owner archive root:

```
python research/root_diagnostic/check_k24_path.py \
  --output-dir research/root_diagnostic/replay
```

This writes its own exact inputs and result receipt. Compare the stable
input bytes/hash and the structural/color counts; wall/CPU/RSS observations
are expected to change. The source uses Python's standard library only.

The diagnostic uses exhaustive finite methods and does not advertise an
efficient recognizer or a general coloring procedure. It makes no
historical originality, external acceptance, practical runtime or
application-performance claim.

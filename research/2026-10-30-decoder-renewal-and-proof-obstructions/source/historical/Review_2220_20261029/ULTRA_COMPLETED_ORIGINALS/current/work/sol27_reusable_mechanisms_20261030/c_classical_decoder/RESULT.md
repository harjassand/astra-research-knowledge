# A stored five-gate decoder from opaque calibration records

30 October2026. Completed restricted operation, with mathematical and
computational source scope separated.

For a128-output, one-input mixed Clifford encoding with a warranted
five-site logical light cone, the actual record receiver constructed

    H64; CX(64,63); SDG63; H62; CX(63,62).

Retain wire63 and discard the rest. All later decoding uses this stored
classical circuit, with no source queries and no quantum program. The
net circuit uses three neighboring physical wires and two CNOTs.

The source has two nearest-neighbor entangling layers plus local H/S
layers,127 full-rank mixed magic junk qubits globally entangled by a
Clifford, and coherent Z rotation plus depolarization at every output.
Its unknown gates/junk/noise model are not read by the receiver. The
producer computed exact rational local Born laws and then generated
seeded63-bit-ticket measurement records. There was no quantum device.

The995328 discovery and131072 fresh validation records gave

    Fe >=272566541459/274877906944=.9915913013501267,
    general all-input halfdiamond <=.18339791329162836.

These are conditional on the explicit fixed memoryless-source, fresh
independent ideal-measurement contract. Their joint ideal-law error
probability is below.001; the fair-ticket rounding law adds its explicit
tiny TV budget. A seeded PRNG is not that statistical or hardware
qualification. The hidden model's exact Fe=.9963060262371023 is a
separate withheld audit, not a fitted input or confidence certificate.

The general theorem allows q logical qubits and arbitrary mixed junk;
the executed record CLI is q=1. Exact Pauli algebra and a public signed
Clifford compiler convert fresh actual-channel correlations into a
whole-channel decoder guarantee. Local calibration visibility need not
sum errors over every output. A stronger all-input transfer using an
independently warranted relevant-channel error is proved separately and
does not tighten the saved generic.1834 result.

Product-Pauli/shadow estimation and symplectic synthesis are strong
ordinary methods supplying this restricted route. Clean Bell learning
is already absorbed by StateHSP. General noisy hidden-Clifford recovery
has root's distinct quantum-LPN reduction; no general robust algorithm
or proven hardness follows here. No world-priority, matched speedup,
physical recovery or noisy-control threshold is claimed.

Governing details: [PROOF.md](PROOF.md),
[PRIOR_AND_DECISION.md](PRIOR_AND_DECISION.md),
[QUALIFIED_DECODER.json](QUALIFIED_DECODER.json), and
[COST_SCOPE.json](COST_SCOPE.json). No more source case or shot tuning
was needed to reach this boundary.

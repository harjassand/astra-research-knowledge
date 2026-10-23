# Reproducible checks and their scope

Run commands from this extracted archive's top directory. They use Python3.
The two new exact replays need only the standard library. The historical
exploratory probe additionally uses NumPy and is not required to check the
all-length theorem.

## Package integrity

Run `python3 verify_package.py`. It checks all manifest hashes and the
unchanged predecessor's required identity. The predecessor archive is
3,763,692 bytes with SHA256
`7cc0ba564d5e9d483527b9c4f55928d17bcba0b27db9604875286faa27128654`.

## Focused exact replays

```bash
python3 contributions/temporal_constructive_structure_guard_replay.py --output /tmp/pro1-cycle6-guard.json
python3 contributions/temporal_dual_certificate.py --output /tmp/pro1-cycle6-dual.json
```

The first checks symbolic input/bath token wiring, actual root exchange,
the precise selected transposition and two omitted-premise counterexamples.
Its default bounded range is3<=k<=8. This does not establish all k by
enumeration; the main proof supplies the all-length induction/decomposition.

The second reads the actual preserved Cycle5 polynomial from its ZIP,
verifies its SHA256 and checks an exact rational k4 dual certificate.
It also verifies that uniform-prefix averaging is not optimal. This is
finite evidence, not a premise for the all-length lower or nonlinear theorem.

The exploratory `temporal_constructive_structure_probe.py` is portable via
the unchanged `representation/four_call_representation.py` copy. Its
historical receipts include the only k6 diagnostic. It is deliberately
not in the default verification sequence; no large numerical sweep is
needed to replay the proof.

## Proof build

With a standard pdfLaTeX installation, `python3 build_pdf.py` builds the
complete proof in `output/pdf/`. It records build cost only. Scientific
correctness requires reading the theorem arguments and reviews; a successful
PDF build or ZIP check is not scientific acceptance.

`COMPLETE_PROOF.tex.txt` has both included files expanded and can be read
through the private UTF-8 Page API without binary materialization. Ordered
base64 transport parts, when delivered, reconstruct the identical ZIP;
the external transport manifest supplies their hashes and concatenation rule.

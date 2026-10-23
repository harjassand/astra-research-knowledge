ASTRA PRO 2 — STABLE COORDINATE INFORMATION, CYCLE4
22 October2026 Australia/Brisbane

Start with RESULT.md, then PROOF.md and CONTINUATION.txt.
The full TW<=2,Delta<=4 four-versus-five problem remains open.
Four is now sharp on bandwidth-two supports; a four-query decoder also covers
forest prisms, and a quantitative coordinate-design stability criterion gives
exact error witnesses and a reusable linear-time decoder.

No third-party dependency is needed for the new exact source. Python3.10+
and the standard library suffice. The executable fixture uses fractions.Fraction.

Receiving check, from anywhere:
    python /path/to/checkpoint/replay.py --out /path/to/new-receiving-output

This verifies every payload identity in MANIFEST.json, including the unchanged
native predecessor, and runs the independently implemented exact checker on
the new data. It does not rerun old molecular, spectral or treewidth campaigns.
The output path is kept separate from frozen producer/independent receipts.

To regenerate the producer fixture for development, first copy the package
to a new working directory, then run experiments/coordinate_operations.py.
It writes results/coordinate_operations.json in that working copy. Do not
overwrite frozen evidence merely to inspect it. Research contributor scripts
have their own producer-side checks and costs; their all-size proofs carry
the universal statements, not the finite runs.

Contents:
  PROOF.md, RESULT.md: full argument, scope, comparator and evidence
  CONTINUATION.txt: precise next owned scientific step
  COSTS.md, FAILED_APPROACHES.md, INTAKE.md: error/cost/source/failed premises
  src/: actual coordinate decoder and certificate construction
  experiments/, results/: exact finite inputs, outputs and cut witness
  verification/: independently implemented checker and original receipt
  research/: signed construction, stronger comparator, structural lemmas,
             focused proof challenges, failed alternatives and literature notes
  sources/: exact unchanged native Cycle3 owner ZIP with older source embedded
  protocol/: unchanged agent-owned handoff protocol
  MANIFEST.json: exact payload identity list

Historical priority is unestablished. No application speedup is claimed.
Archive identity and later private delivery/readback receipt accompany the
immutable ZIP on the existing Page; delivery does not imply receiver acceptance.

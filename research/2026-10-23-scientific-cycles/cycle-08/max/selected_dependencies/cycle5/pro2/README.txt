ASTRA PRO2 CYCLE5 SOURCE CHECKPOINT

Read RESULT.md, PROOF.md, CONTINUATION.txt, FAILED_APPROACHES.md and COSTS.md.
The main full-class q4 versus q5 problem remains open. The complete unchanged
Cycle4 source is embedded under sources/; older source is nested unchanged.

New operations:
  src/cut_balance.py: exact cut/centroid certificate and inherited LS decoder.
  research/structure/strip_extension.py: arbitrary-boundary strip extension
    and conditional graph reduction. It does not solve the reduced coloring.

Actual new inputs/outputs:
  results/cut_balance_operations.json
  results/received_strip_operation.json
  research/structure/RESULT.json

Independent checks:
  verification/check_cut_balance_independent.py
  research/cut_balance_review/check_strip_transition_certificate.py

Receive without changing frozen results:
  python replay.py --output /tmp/astra_cycle5_pro2_replay

This verifies payload hashes and runs the two independent exact checks. It
does not repeat old campaigns or producer diagnostics. New outputs and elapsed
costs go into the specified directory, which must be outside this source tree.
Use a fresh directory to avoid mixing receiving receipts from different runs.

The archive also contains focused proofs/reviews, the unsuccessful premises
that changed continuation, exact transition witnesses, all observed costs and
a compact continuation. Only the Python standard library is needed.

Transport identity and actual private delivery receipt accompany the archive
outside it. They do not establish that a recipient has read, scientifically
accepted or integrated the work.

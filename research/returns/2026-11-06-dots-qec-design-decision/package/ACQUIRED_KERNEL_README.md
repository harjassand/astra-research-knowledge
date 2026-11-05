# Internal ordered-fault-tuple research packet

Start with qec_fault_tuple_20261105/RESULT.md. This is a scoped computational result and internal research record, not a hardware reliability certification or a claim of transformative completion.

The fixed d21 modeled target was rejected at individual 99.9% confidence under ideal independent bits. The exact algorithm and finite-table construction passed independent audit and complete replay. The strongest executed published-method challenger stopped at its fixed 20-minute cap after 13 of 31 rungs without a complete estimate. No superiority claim follows. The repetition-line counterexample proves exponential inefficiency remains.

## Reproduce from this directory

Python 3.12 with the versions in requirements.txt is the tested environment; g++ is needed for integer certificate checks. No installed binaries are bundled. Creating a suitable environment/installing dependencies is a separate setup action.

- python qec_fault_tuple_20261105/exact_sampler.py --directory qec_fault_tuple_20261105/d21 --shots 100 --seed 7 --no-confidence --output /tmp/tuple_smoke.json
- python qec_fault_tuple_audit_20261105/check_certificate.py --distance 21
- python qec_fault_tuple_audit_20261105/verify_production.py
- python qec_fault_tuple_audit_20261105/verify_resources_portable.py
- python qec_fault_tuple_20261105/check_repetition_limit.py

The frozen production runs are already preserved; do not interpret smoke tests as new prespecified statistical evidence.

To rebuild tables, run qec_overlap_gate_20261105/fault_tuple_screen.py --distance 21 --cut-distance 64 --modulus 64, then qec_fault_tuple_20261105/build.py --distance 21. Use a working copy because those builders overwrite their derived tables/receipts. Input acquisition is in canonical_qec_circuit_gate_20261105/acquire_graph.py. Full graph/decoder/model scope and audit references are in the technical report.

All sources, original artifacts and mathematical results remain unchanged in this packet, except an explicitly labeled path-only resource-checker sibling described by PORTABILITY.json. Historical resource launchers include original workspace paths; their receipts are preserved, but they are not portable launcher promises. Temporary producer/checker binary blobs and compiled executables are omitted because the source checkers regenerate them. Prior path-cover audit notes may reference older artifacts outside this focused packet; the included input-projection checks and new tuple checks are its reproducibility scope.

The archive contains no environment/venv. Verify PACKET_SHA256SUMS before execution. Sampling uses a reproducible Python PRNG; exact IID coverage assumes ideal independent bits, as stated throughout.

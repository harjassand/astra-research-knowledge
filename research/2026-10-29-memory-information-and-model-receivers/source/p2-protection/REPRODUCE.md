# Reproduce the protection tranche

Run from `producer-workspace/33bc43af9179`. Python 3 and NumPy are sufficient; no network, credentials, hardware access or third-party services are used by these checks. Most checks use integers or `fractions.Fraction`; the coherent-transmutation and selected independent capacity/control checks also use NumPy. Their individual evidence files distinguish exact arithmetic from numerical matrix checks.

## Integrity first

```bash
python p2_protection/verify_integrity.py
```

This checks the current inventory, all six current review receipts and their file pins, and the unchanged manifested bytes of `p2_operation`, `p2_measurement` and `p2_mediator`. It is byte-integrity checking, not scientific revalidation of those accepted predecessors. `--build` is an authoring operation that rewrites only this tranche's inventory; it is not needed to verify a received snapshot and cannot bless a mismatch in a review pin or predecessor manifest.

## Author implementations

```bash
python p2_protection/protected_algebra/coherent_protection_checks.py
python p2_protection/classical_capacity/capacity_checks.py
python p2_protection/exposure_code/exposure_codes.py
python p2_protection/architecture_challenge/architecture_checks.py
python p2_protection/fault_tail_checks.py
python p2_protection/channel_order_checks.py
```

Each writes its own evidence JSON beside the script, except the exposure-code script which defaults to `EXPOSURE_CODE_RESULTS.json` in its directory. Replays may rewrite identical evidence bytes. Preserve any changed result separately for diagnosis; do not regenerate a review receipt to conceal a mismatch. The exposure-code script also accepts `--output PATH` for a separate replay file.

The exposure-code implementation emits the GF(4) checks, binary stabilizers, source encoder, syndrome lookup, two-location failures and exact family inequalities. The tail programs distinguish literal identity-plus-F degree from Pauli weight. Their output bounds are sufficient complete-channel comparisons, not measured physical error rates or optimized actual diamond distances.

## Independent implementations

```bash
python p2_protection/reviews/coherent_transmutation/independent_two_gap_audit.py
python p2_protection/reviews/classical_capacity/independent_capacity_audit.py
python p2_protection/reviews/exposure_code/independent_code_audit.py
python p2_protection/reviews/closed_loop/independent_loop_audit.py
python p2_protection/reviews/fault_tail/independent_tail_audit.py
python p2_protection/reviews/channel_order/independent_channel_audit.py
```

The corresponding `INDEPENDENT_REVIEW.md` and `REVIEW_RECEIPT.json` files state what was reconstructed, read, run, accepted, corrected and excluded. `AUTHOR_REPLAY.json` is replay evidence; it is not the independent implementation. Some replay JSON files contain an execution summary rather than a byte copy of author output, as their receipts specify.

The final channel-order audit imports no author code. It uses a different three-qubit phase code and a two-qubit noncommuting persistent bath, checks every low-degree logical/bath matrix-unit block with the actual syndrome retained, and verifies equality of the complete comparison difference with the high-degree sum. It also preserves the coherent-syndrome failure and a dense overlapping-exposure example. The closed-loop audit includes simultaneous finite control and noncommuting noise, and a leakage negative control.

## Scope of success

Passing these programs verifies their finite identities, specified circuit realizations, inequalities and evidence reproducibility. The documents provide the general proofs. No program acquires a coupling, calibrates an interaction norm, validates a detector, certifies loss recovery, establishes a physical fault law or proves efficient extensive-error decoding. The prior bath certificate is not rerun or transferred to a changed bath or device. The proofs' noise, record, support, initial-correlation and completed-call assumptions remain necessary inputs.

# Reproduce and continue

Use Python 3 and NumPy. The executed environment used NumPy 2.3.5. No external network, quantum hardware or proprietary solver is needed for the saved checks. Run commands from the workspace root. The programs write their corresponding JSON evidence next to themselves; preserve a copy when comparing a later runtime. Actual review receipts already record isolated author replays and independent checks.

## Use the receiver compiler

```bash
python p2_operation/compile_receiver.py --epsilon 1/100 --output p2_operation/COMPILED_EXAMPLE.json
```

To supply a schedule, create JSON with `C_batches`, a list of equally sized symmetric binary matrices with zero diagonal. Their sum modulo two must be zero for this compiler. Optional `source_labels` is a nonempty list of admitted binary source labels; omitted means every label is admitted. Pass `--input path/to/schedule.json`. `--epsilon` accepts an exact rational string. Output is a symbolic controlled-query recipe with actual phase/radical records and a conservative certificate, not a laboratory pulse program.

The emitted canonical query includes q*pi/2 minus its phase-normalization terms. The old retained Pauli frame's scalar power of i must also be implemented when that frame is controlled. The output distinguishes operator order from execution order. Only the final zero-qubit frame constant is added to final source feedback; intermediate frame constants remain part of the next controlled Pauli operation.

## Author constructions

```bash
python p2_operation/reusable_service_checks.py
python p2_operation/operation_metric/exact_schur_checks.py
python p2_operation/operation_metric/raw_record_checks.py
python p2_operation/recovery_challenge/record_gram_checks.py
python p2_operation/causal_algebra/algebra_exact_checks.py
python p2_operation/causal_algebra/operation_separation_exact.py
python p2_operation/extractor_circuit/extractor_checks.py
python p2_operation/robust_extractor/robust_extractor_checks.py
python p2_operation/projective_compiler_checks.py
python p2_operation/memory_fault_checks.py
```

The compiler check imports only the exact rational complex scalar class from `robust_extractor_checks.py`. The command-line compiler imports the finite binary normal-form routines from `projective_compiler_checks.py`; imports do not execute the check suites. Exact Q(i), finite-field, Laurent and cyclotomic calculations are separated from floating diagnostic computations. The latter are not interval enclosures and do not replace the unrestricted operator proofs.

## Independent reviews

Each `reviews/<module>/INDEPENDENT_REVIEW.md` describes the review scope, executed evidence, dependency exclusions and accepted corrections. The nearby `independent_*_audit.py` scripts implement independent checks. Review receipts pin the actual author versions. The general compiler theorem review and the emitted recipe review are separate, because a correct theorem can still have an incomplete executable interface.

## Preserved failures and exclusions

`history/schedule_compiler_initial` preserves the first emitted recipe, which omitted explicit record-normalization control-phase metadata. Do not use it as the current circuit. The earlier private-record leakage and stale-detector counterexamples are executed in `reusable_service_checks.py`. The robust review includes a negative control for omitting disturbance of the earlier phase estimate. The unreviewed general-p note is outside the accepted claims.

No earlier bath-representation, gate-comparison, parity or visibility result is revalidated by these commands. Their original proofs, corrections and actual reviews remain in the predecessor packages. `MANIFEST.json` is an integrity inventory, not additional scientific validation.

```bash
python p2_operation/verify_integrity.py
```

This checks the current inventory, the versions pinned by actual reviews, and predecessor bytes. `--build` is an author maintenance option to refresh the inventory after deliberate changes; it should not be used to conceal failed verification. The preserved initial recipe is not attributed current accepted status.

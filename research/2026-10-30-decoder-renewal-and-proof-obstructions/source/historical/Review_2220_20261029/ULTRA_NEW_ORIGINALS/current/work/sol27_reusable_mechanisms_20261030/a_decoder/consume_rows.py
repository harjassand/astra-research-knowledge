"""Execute only exact classical reference-row/Clifford postprocessing.

The public algebraic input is generated from a declared Clifford for the sole
purpose of a noncanonical phase control.  It is not a Bell-difference source,
noisy-channel simulator, source acquisition run, or physical gate execution.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import time

import row_receiver as rr

pc = rr.pc


def transpose(a):
    x, z, p = a
    return x, z, (p + 2 * (x & z).bit_count()) % 4


def public_dense_clifford(n):
    gates = []
    for j in range(n):
        gates.append(("H", j))
        if j % 3:
            gates.append(("S", j))
    for round_index in range(3):
        for j in range(n - 1):
            gates.append(("CX", j, j + 1))
        for j in range(n - 1, 0, -1):
            gates.append(("CX", j, j - 1))
        for j in range(n):
            if (j + round_index) % 2:
                gates.append(("H", j))
            else:
                gates.append(("S", j))
    return gates


def main():
    started = time.perf_counter()
    q, n = 2, 32
    encoding = public_dense_clifford(n)
    # Independent NONcanonical reference basis.  It contains two Y strings,
    # two-site support, and raw reference products with phases +/-i.
    labels = [(3, 1), (2, 3), (1, 0), (0, 1)]
    records = []
    for rx, rz in labels:
        physical = pc.apply(transpose(pc.canonical(rx, rz)), encoding)
        records.append({"rx": rx, "rz": rz, "px": physical[0],
                        "pz": physical[1], "negative": pc.sign(physical) < 0})
    # Only these signed records enter the row converter.  Encoding is kept
    # outside that API and used later solely as independent algebraic truth.
    compiled = rr.compile_records(records, q, n)
    gates = compiled["gates"]
    original_checks = []
    for record in records:
        reference, physical = rr.record_paulis(record)
        obtained = pc.apply(physical, gates)
        wanted = transpose(reference)
        assert obtained == wanted
        original_checks.append({"obtained": list(obtained), "wanted": list(wanted)})
    product_checks = 0
    for mask in range(1 << (2 * q)):
        reference, physical = (0, 0, 0), (0, 0, 0)
        for j, record in enumerate(records):
            if (mask >> j) & 1:
                r, b = rr.record_paulis(record)
                reference = pc.mul(reference, r)
                physical = pc.mul(physical, b)
        # Transpose reverses multiplication order; comparing the product of
        # individual transposes retains the true row ordering and phases.
        expected = (0, 0, 0)
        for j, record in enumerate(records):
            if (mask >> j) & 1:
                expected = pc.mul(expected, transpose(rr.record_paulis(record)[0]))
        assert pc.apply(physical, gates) == expected
        product_checks += 1
    # Complete generator check: D U0 preserves the logical algebra exactly,
    # and every arbitrary junk Pauli has no support on the logical outputs.
    combined = encoding + gates
    tableau = pc.make_tableau(n, combined)
    generator_checks = 0
    logical_mask = (1 << q) - 1
    for j in range(n):
        for kind, images in (("X", tableau[0]), ("Z", tableau[1])):
            image = images[j]
            if j < q:
                assert image == ((1 << j, 0, 0) if kind == "X" else (0, 1 << j, 0))
            else:
                assert not ((image[0] | image[1]) & logical_mask)
            generator_checks += 1
    # Ignoring raw reference phase is detected, including non-Hermitian
    # physical candidates in the +/-i case.  No source is used for this check.
    wrong_phase_detections = []
    for item in compiled["conversion"]:
        raw = tuple(item["raw_physical"])
        try:
            pc.sign(raw)
            bad = pc.apply(raw, gates)
            target = ((1 << item["logical"], 0, 0) if item["kind"] == "X"
                      else (0, 1 << item["logical"], 0))
            detected = bad != target
            reason = "wrong signed generator" if detected else "not detected"
        except ValueError:
            detected, reason = True, "non-Hermitian raw physical factor"
        if item["raw_reference"][2]:
            assert detected
            wrong_phase_detections.append({"logical": item["logical"],
                                           "kind": item["kind"], "reason": reason})
    assert any(item["raw_reference"][2] in (1, 3) for item in compiled["conversion"])
    assert wrong_phase_detections
    elapsed = time.perf_counter() - started
    result = {
        "status": "PASS_EXACT_CLASSICAL_POSTPROCESSING_ONLY",
        "q": q, "n": n, "signed_input_records": records,
        "input_provenance": "public deterministic Clifford algebra; no source samples",
        "encoding_gate_count": len(encoding),
        "decoder_gate_count": len(gates),
        "decoder_cx_count": sum(g[0] == "CX" for g in gates),
        "maximum_input_row_weight": max((r["px"] | r["pz"]).bit_count() for r in records),
        "conversion": compiled["conversion"], "decoder_gates": gates,
        "original_row_checks": original_checks,
        "all_selected_row_products_checked": product_checks,
        "complete_logical_and_junk_generator_checks": generator_checks,
        "wrong_phase_negative_controls": wrong_phase_detections,
        "compiler_path": str(rr.COMPILER_PATH), "compiler_sha256": rr.COMPILER_SHA256,
        "source_calls": 0, "Bell_difference_shots": 0, "Pauli_validation_shots": 0,
        "quantum_circuit_or_hardware_executions": 0,
        "elapsed_seconds_after_imports": elapsed,
        "not_acquired": ["Bell/source acquisition", "noisy source realization",
                         "physical controls", "native calibration", "practical advantage"]
    }
    for name in ("row_receiver.py", "consume_rows.py"):
        result.setdefault("consumer_input_hashes", {})[name] = hashlib.sha256(
            Path(__file__).with_name(name).read_bytes()).hexdigest()
    path = Path(__file__).with_name("ROW_EXECUTION.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "decoder_gate_count", "decoder_cx_count", "maximum_input_row_weight",
        "all_selected_row_products_checked", "complete_logical_and_junk_generator_checks",
        "wrong_phase_negative_controls", "elapsed_seconds_after_imports")}))


if __name__ == "__main__":
    main()

"""Transfer frozen matrix certificates to exact decimal model endpoints.

This composition uses the exact rational norm in EXACT_BRIDGE.json. It does
not treat a displayed floating-point estimate as an exact decimal endpoint.
"""
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUTS = BASE / "inputs"


def up(x):
    value = float(x)
    if Fraction.from_float(value) < x:
        value = math.nextafter(value, math.inf)
    return value


def down(x):
    value = float(x)
    if Fraction.from_float(value) > x:
        value = math.nextafter(value, -math.inf)
    return value


def interval(row, delta):
    lower = down(Fraction.from_float(row["lower"])-delta)
    upper = up(Fraction.from_float(row["upper"])+delta)
    width = up(Fraction.from_float(upper)-Fraction.from_float(lower))
    assert width <= 0.00159360143764
    return dict(lower=lower, upper=upper, guaranteed_width=width,
                matrix_lower=row["lower"], matrix_upper=row["upper"],
                guarantee_scope="declared Ag compression of exact printed FCIDUMP; standard explicit arithmetic model for upstream matrix certificate")


def main():
    bridge = json.loads((BASE/"EXACT_BRIDGE.json").read_text())
    pair = json.loads((BASE/"COMPACT_PAIR.json").read_text())
    audit = json.loads((INPUTS/"STRONG_AUDIT.json").read_text())
    matched = json.loads((INPUTS/"MATCHED_TARGET_FAST_VECTOR.json").read_text())
    fast_vector = json.loads((INPUTS/"FAST_VECTOR_REPLAY.json").read_text())
    benchmark = json.loads((INPUTS/"BENCHMARK.json").read_text())
    delta = Fraction(int(bridge["bridge"]["exact_infinity_norm_numerator"]),
                     int(bridge["bridge"]["exact_infinity_norm_denominator"]))
    rows = []
    for row in matched["rows"]:
        if row["status"] == "CHECKED":
            result = interval(row,delta)
            result.update(method=row["method"], selected_size=row["size"],
                          method_wall_seconds=row["wall_seconds"])
            rows.append(result)
    full = interval(matched["full_factor"],delta)
    tight = interval(audit["verified_full_factor_comparator"],delta)
    bridge_cost = sum(bridge[x] for x in ["parse_seconds","exact_assembly_seconds","exact_bridge_seconds"])
    file_hashes = {}
    for path in [BASE/"EXACT_BRIDGE.json",BASE/"COMPACT_PAIR.json",INPUTS/"STRONG_AUDIT.json",
                 INPUTS/"MATCHED_TARGET.json",INPUTS/"MATCHED_TARGET_FAST_VECTOR.json",
                 INPUTS/"FAST_VECTOR_REPLAY.json",INPUTS/"CORRECTION_004.txt",
                 INPUTS/"BENCHMARK.json",INPUTS/"N2.STO3G.FCIDUMP"]:
        file_hashes[str(path.relative_to(BASE))] = hashlib.sha256(path.read_bytes()).hexdigest()
    ledger = dict(
        decision="NO_NEW_ENABLING_OPERATION_ESTABLISHED",
        useful_capital="exact decimal FCIDUMP assembly and spectral norm bridge closes the input-to-matrix error contract for the declared Ag compression",
        input_model_sha256=bridge["input_sha256"],
        exact_error_bridge=dict(numerator=str(delta.numerator),denominator=str(delta.denominator),upper=up(delta)),
        transferred_matched_intervals=rows,
        transferred_full_factor_matched=full,
        transferred_full_factor_tight=tight,
        compact_competitor=dict(best_lower=pair["best_lower"],upper=pair["certified_Ag_upper"],
                width=pair["certified_Ag_interval_width"],target=pair["target_width"],
                verdict="FAILS_TARGET",pauli_split_lower=pair["pauli_diagonal_hole_split"]["energy_lower"]),
        costs=dict(
            cost_provenance_status="CORRECTED: initial saved-vector/fastest-timing mismatch preserved in CORRECTION_004; fresh pspace0 vector acquired, hashed and used in literal matched-target replay. Vector is bit-identical to initial vector; intervals unchanged.",
            exact_decimal_bridge_components_seconds=bridge_cost,
            exact_bridge_whole_process_seconds=bridge["elapsed_seconds"],
            full_float_matrix_assembly_seconds=benchmark["full_matrix_acquisition"]["wall_seconds"],
            full_float_matrix_bytes=benchmark["full_matrix_acquisition"]["matrix_bytes"],
            saved_FCI_vector_original_producer_seconds=benchmark["incumbent_fci"][0]["wall_seconds"],
            fastest_measured_FCI_solve_seconds=benchmark["incumbent_fci"][1]["wall_seconds"],
            actual_fresh_fast_vector_solver_seconds=fast_vector["solver_seconds"],
            actual_fresh_fast_vector_save_seconds=fast_vector["vector_save_seconds"],
            actual_fast_vector_parse_seconds=fast_vector["parse_seconds"],
            actual_fast_vector_diagnostic_validation_seconds=fast_vector["validation_seconds"],
            actual_fast_vector_import_seconds=fast_vector["import_seconds"],
            shared_retaining_Rayleigh_seconds=matched["shared_rayleigh_upper_seconds"],
            matched_full_factor_seconds=matched["full_factor"]["wall_seconds"],
            required_retaining_work_post_matrix_seconds=matched["actual_retaining_total_post_matrix_seconds"],
            native_work_post_matrix_seconds=matched["actual_native_total_post_matrix_seconds"],
            retaining_plus_recorded_diagnostic_validation_seconds=matched["actual_retaining_total_post_matrix_seconds"]+fast_vector["validation_seconds"],
            cost_scope="individual single-run measured components; retained audit diagnostic, parse, imports, loading, setup/download and exploratory trial expenses remain separately charged. No statistical or end-to-end speed claim.",
            inference_tokens="UNKNOWN",inference_price="UNKNOWN",electrical_energy="UNKNOWN"),
        arithmetic_assumptions=audit["arithmetic_assumptions"],
        fast_vector_sha256=fast_vector["vector_sha256"],
        exact_input_caveat=bridge["symmetry_note"],
        source_status="primary source and code pinned; internal proof and local execution only",
        full_SOS_v2RDM_target_result="NOT_RUN_AND_NOT_REFUTED_BY_CHEAP_FRAGMENT_FAILURE",
        claims=[
            {"id":"s05-C01","status":"INTERNALLY_PROVED_AND_EXECUTED","claim":"exact printed Ag matrix differs from saved real binary64 matrix by spectral norm at most the exact rational bridge"},
            {"id":"s05-C02","status":"CONDITIONAL_ON_STATED_ARITHMETIC_MODEL","claim":"transferred intervals certify declared Ag finite-model ground energy at the same required width"},
            {"id":"s05-C03","status":"INTERNALLY_PROVED_AND_EXECUTED_NEGATIVE_BENCHMARK","claim":"cheap electron/hole pair certificate and untuned Pauli split fail the chemical-accuracy interval target"},
            {"id":"s05-C04","status":"INTERNALLY_PROVED_SCOPED_INFORMATION_OBSTRUCTION","claim":"visible selected blocks and moments cannot rule out an unrestricted orthogonal dark negative-energy extension"},
            {"id":"s05-C05","status":"NOT_ESTABLISHED","claim":"new omitted-space-free energy operation with novelty and full-cost matched advantage"},
            {"id":"s05-C06","status":"OUTSIDE_SCOPE","claim":"physical N2 ground-state energy or global full Ms=0 energy including all nominal symmetry sectors"}
        ],
        frozen_input_hashes=file_hashes)
    (BASE/"CERTIFICATE_RECEIPT.json").write_text(json.dumps(ledger,indent=2))
    print(json.dumps(ledger,indent=2))


if __name__ == "__main__":
    main()

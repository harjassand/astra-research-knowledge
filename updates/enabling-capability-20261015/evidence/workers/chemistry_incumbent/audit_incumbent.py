"""Read-only audit of the acquired source and acquisition interface.

Does not execute downloaded source/notebooks/pickles, generate assay data, or
present producer-fitted yields as independent truth.
"""

import ast
import hashlib
import json
from pathlib import Path


def digest(path):
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def main():
    out = Path(__file__).resolve().parent
    source_worker = out.parent / "chemistry_search"
    source = source_worker / "source_code/spectral_deconvolution/spectral_deconvolution.py"
    notebook = source_worker / "source_code/spectral_deconvolution/spectral_deconvolution_globus.ipynb"
    tree = ast.parse(source.read_text())
    division_fields = []
    least_squares_bounds = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.BinOp):
            value = node.value
            if (isinstance(value.op, ast.Div) and isinstance(value.right, ast.Name)
                    and value.right.id == "max_yield"):
                for target in node.targets:
                    if isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant):
                        division_fields.append({"field": target.slice.value, "line": node.lineno})
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "least_squares":
                least_squares_bounds.append({"line": node.lineno,
                                            "has_bounds": any(k.arg == "bounds" for k in node.keywords)})
    si = out / "ja6c05959_si_001.pdf"
    ord_file = source_worker / "ord_dataset-805ad863feef48579d95d86a728035f4.parquet"
    report = {
        "status": "NOT_EXECUTED_MISSING_MEASURED_INPUTS",
        "comparison_has_chemical_measurements": False,
        "comparison_has_independent_mixture_truth": False,
        "new_operation_demonstrated": False,
        "source_commit": "449db5a012aca0cb24181ddcbb51d3fad6c2f98e",
        "source": digest(source),
        "notebook": digest(notebook),
        "si": digest(si),
        "si_md5": hashlib.md5(si.read_bytes()).hexdigest(),
        "ord": digest(ord_file),
        "source_least_squares_calls": least_squares_bounds,
        "fields_divided_by_max_yield": sorted(division_fields, key=lambda x: x["line"]),
        "error_fields_not_divided": ["error_DP", "error_SP"],
        "unit_finding_scope": "source CSV contract; downstream files not acquired",
        "default_max_yield_numeric": 0.2 / 4 / 30 * 1000,
        "default_max_yield_unit_in_code_comment": "mM",
        "exact_channel_count": "UNKNOWN_WITHOUT_MZML",
        "source_wavelength_range_nm": [255, 305],
        "raw_data_replay": "NOT_EXECUTED",
        "known_sigma_and_calibration_conditional_ci_only": True,
        "software_checks_are_not_assay_validation": True,
        "lc_arithmetic_costs": {
            "basis": "SI3 method durations/flow; actual 2/8 minute mix and overhead unknown",
            "per_injection_two_minute_solvent_mL": 2 * 0.8,
            "per_injection_eight_minute_solvent_mL": 8 * 0.8,
            "all_50688_two_minute_instrument_hours": 50688 * 2 / 60,
            "all_50688_two_minute_solvent_L": 50688 * 2 * 0.8 / 1000,
            "all_50688_eight_minute_instrument_hours": 50688 * 8 / 60,
            "all_50688_eight_minute_solvent_L": 50688 * 8 * 0.8 / 1000,
            "four_compounds_five_levels_two_instruments_injections_if_one_each": 4 * 5 * 2,
            "same_calibration_at_two_minutes_instrument_minutes": 4 * 5 * 2 * 2,
            "same_calibration_at_two_minutes_solvent_mL": 4 * 5 * 2 * 2 * 0.8,
            "raw_transfer_bytes": "UNKNOWN",
            "calibration_preparation_labor": "UNKNOWN",
            "independent_truth_acquisition": "NOT_ACQUIRED",
            "money_energy_memory_end_to_end": "UNKNOWN",
        },
    }
    manifest = {
        "collection_in_notebook": "bfd43535-052a-46bb-911a-b1cdfb1e92d7",
        "collection_in_jacs_article": "1e0ff2e8-9139-4f7e-97a7-4954714bd34d",
        "unauthenticated_access_result": "ClientError.AuthenticationFailed: No credentials supplied",
        "root_browser_result": "Current article link redirects to Globus login; no data listing acquired",
        "required_files": [
            {"declared_remote_path": "/spectral_deconvolution/matrix_completion/spectral_deconvolution_data.csv",
             "acquired": False, "role": "reaction identifiers, instrument linkage and exact mzml_path"},
            {"declared_remote_path": "/spectral_deconvolution/matrix_completion/calibration_data/CF3_DP_<INSTRUMENT>.pkl",
             "acquired": False, "role": "authentic target response columns nm/ext_coef on actual instrument"},
            {"declared_remote_path": "/spectral_deconvolution/matrix_completion/calibration_data/CF3_SP_<INSTRUMENT>.pkl",
             "acquired": False, "role": "authentic side response columns nm/ext_coef on actual instrument"},
            {"declared_remote_path": "mzml_path values in the missing manifest; exact filenames UNKNOWN",
             "acquired": False, "role": "raw measured wavelength/time arrays and caffeine traces"},
            {"declared_remote_path": "calibration RAW/MZML plus stock, dilution and replicate provenance; exact filenames UNKNOWN",
             "acquired": False, "role": "calibration uncertainty, unit reconciliation, drift and covariance"},
            {"declared_remote_path": "independently quantified blind mixtures; existence/location NOT_ESTABLISHED",
             "acquired": False, "role": "quantitation accuracy and empirical interval coverage"},
        ],
        "available_documentary_evidence": [
            "SI34 pure-compound calibration graph formulas, not full wavelength arrays",
            "SI40 authentic-standard multiwavelength procedure",
            "SI41-42 producer-fitted mixture plots, not independent mixture truth",
            "ORD calibrated target/side assay labels with producer authentic/internal-standard flags",
        ],
        "pickle_policy": "No downloaded pickle executed; inspect serialized contents/provenance before loading",
        "full_comparison_gate": "MISSING_MEASURED_RESPONSE_AND_TRUTH_INTERFACE",
    }
    (out / "INCUMBENT_AUDIT.json").write_text(json.dumps(report, indent=2))
    (out / "REQUIRED_INPUT_MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps({"status": report["status"],
                      "normalized_fields": report["fields_divided_by_max_yield"],
                      "si_bytes": report["si"]["bytes"],
                      "si_publisher_md5_match": report["si_md5"] == "653b2bd22993e1a98f9332847884081e"}, indent=2))


if __name__ == "__main__":
    main()

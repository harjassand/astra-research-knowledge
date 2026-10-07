"""Fast final audit, compact-codec test and finite-input precision budget.

Run after run_experiment.py. This intentionally does not repeat its six-minute
high-precision experiment. It validates stored tables and tests the compact
streaming API against every message in the 5,250-message demonstration.
"""

from fractions import Fraction as F
from itertools import product
import csv
import hashlib
import json
from pathlib import Path
import time

from archive import make_archive
from certified import IV, SCALE, normal_constant, interval_json

BASE = Path(__file__).resolve().parent


def main():
    started = time.monotonic()
    results = json.loads((BASE / "results.json").read_text())
    old_manifest = json.loads((BASE / "MANIFEST.json").read_text())
    # Runtime measurements are from the saved bounded run; these three data
    # files are checked against that run's manifest before metadata cleanup.
    for name in ("results.json", "memory_comparison.csv", "sampler_tables.json"):
        assert hashlib.sha256((BASE / name).read_bytes()).hexdigest() == old_manifest[name]
    archive = make_archive(1, 1, F(1, 4), 8)
    checked = 0
    for labels in product(*(range(axis.labels) for axis in archive.axes)):
        message = archive.pack(labels)
        assert archive.unpack(message) == labels
        representatives = []
        for axis, label in zip(archive.axes, labels):
            left, right = axis.bounds(label)
            representatives.append(right - 1 if left is None else left + 1 if right is None else (left + right) / 2)
        assert archive.encode_packed(iter(representatives)) == message
        checked += 1
    assert checked == archive.alphabet_size
    tables = json.loads((BASE / "sampler_tables.json").read_text())
    denom = 1 << tables["random_bits_per_coordinate"]
    rows = [tables["reference"]] + [row for axisrows in tables["axes"].values() for row in axisrows]
    for row in rows:
        assert len(row) == 97 and all(isinstance(x, int) and 0 <= x <= denom for x in row)
        assert all(a <= b for a, b in zip(row, row[1:]))
    assert len(rows) * 97 == results["finite_grid_sampler"]["table_entries"]
    spacing = F(1, 2**24)
    H = F(8)
    assert all(axis.T < H for axis in archive.axes)
    boundaries = sum(axis.M + 1 for axis in archive.axes)
    enc_error = spacing * boundaries * normal_constant()
    dec_error = F(results["finite_grid_sampler"]["worst_case_kernel_TV_error"])
    combined = IV.exact(F(1, 8)) + enc_error + dec_error
    input_cells = int(2 * H / spacing) + 1
    input_bits = (input_cells - 1).bit_length()
    # Rename a descriptive column that previously suggested an unproved lower
    # bound; this does not alter any numeric result or any experimental scheme.
    for row in results["memory_comparisons"]:
        if "dimension_lower_target" in row:
            row["effective_cutoff_scale"] = row.pop("dimension_lower_target")
    csvrows = list(csv.DictReader((BASE / "memory_comparison.csv").open()))
    for row in csvrows:
        if "dimension_lower_target" in row:
            row["effective_cutoff_scale"] = row.pop("dimension_lower_target")
    with (BASE / "memory_comparison.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csvrows[0])
        writer.writeheader()
        writer.writerows(csvrows)
    (BASE / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    checks = {"status": "passed", "codec_messages_checked": checked,
              "cdf_rows_checked": len(rows), "cdf_entries_checked": len(rows) * 97,
              "source_observation_grid": {"spacing": "1/16777216", "clipping_range": ["-8", "8"],
                                          "symbols": input_cells, "bits_per_streamed_observation": input_bits},
              "active_encoder_boundaries": boundaries,
              "encoder_grid_error_bound": interval_json(enc_error),
              "uniform_rounded_output_TV_bound_with_input_and_decoder_compiler": interval_json(combined),
              "elapsed_seconds": time.monotonic() - started,
              "post_run_changes": "Added and exhaustively tested compact streaming API; renamed cutoff scale metadata; no experimental numeric changes."}
    (BASE / "delivery_checks.json").write_text(json.dumps(checks, indent=2) + "\n")
    files = ["certified.py", "archive.py", "run_experiment.py", "audit_delivery.py", "report.md",
             "results.json", "memory_comparison.csv", "sampler_tables.json", "delivery_checks.json",
             "primary_variance_1106.5985.pdf"]
    manifest = {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest() for name in files}
    (BASE / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Passed compact codec {checked} messages; {len(rows)} CDF rows; input bits={input_bits}; active boundaries={boundaries}")
    print("Encoder input-grid TV bound:", enc_error.decimal_bounds(30))
    print("Uniform rounded-output bound with both errors:", combined.decimal_bounds(30))


if __name__ == "__main__":
    main()

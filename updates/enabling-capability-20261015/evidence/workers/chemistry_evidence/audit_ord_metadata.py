#!/usr/bin/env python3
"""Audit measurement provenance in acquired ORD bytes; no inferred measurements."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parent
SEARCH = ROOT.parent / "chemistry_search"
sys.path.insert(0, str(SEARCH / ".python_packages"))
import pyarrow.parquet as pq
from google.protobuf.json_format import MessageToDict
from ord_schema.proto import reaction_pb2


def paths(value, path=""):
    if isinstance(value, dict):
        for key, val in value.items():
            next_path = path + "." + key if path else key
            yield next_path
            yield from paths(val, next_path)
    elif isinstance(value, list):
        for val in value:
            yield from paths(val, path + "[]")


def main():
    started = time.monotonic()
    source = SEARCH / "ord_dataset-805ad863feef48579d95d86a728035f4.parquet"
    pf = pq.ParquetFile(source)
    present = Counter()
    analyses = Counter()
    custom_fields = Counter()
    yields = Counter()
    samples = []
    examples = {}
    for batch in pf.iter_batches(batch_size=2048):
        for raw in batch.to_pylist():
            rxn = reaction_pb2.Reaction()
            rxn.ParseFromString(raw["reaction"])
            r = MessageToDict(rxn, preserving_proto_field_name=True)
            present.update(set(paths(r)))
            for identifier in r.get("identifiers", []):
                if identifier.get("type") == "CUSTOM":
                    custom_fields[identifier.get("details", "")] += 1
                    if identifier.get("details") == "Sample Name_x" and len(samples) < 30:
                        samples.append(identifier["value"])
            for outcome in r.get("outcomes", []):
                for name, analysis in outcome.get("analyses", {}).items():
                    analyses[(name, json.dumps(analysis, sort_keys=True))] += 1
                for product in outcome.get("products", []):
                    for measurement in product.get("measurements", []):
                        if measurement.get("type") == "YIELD":
                            key = (product.get("reaction_role"), json.dumps({k: v for k, v in measurement.items() if k != "percentage"}, sort_keys=True))
                            yields[key] += 1
            if len(examples) < 1:
                examples[r["reaction_id"]] = {"identifiers": r.get("identifiers"), "analysis": r.get("outcomes", [{}])[0].get("analyses"), "provenance": r.get("provenance")}
    measurement_paths = {p: n for p, n in sorted(present.items()) if re.search(r"analy|measur|provenance|identifier", p, re.I)}
    relevant_absences = ["raw spectral arrays", "raw file path/hash", "instrument serial/name (Nile/Ganges)", "injection timestamp/order", "instrument last calibration date", "independent mixture truth", "stock lot/purity uncertainty", "calibration coefficient/covariance", "technical vs independent replicate identifier", "baseline/noise model and wavelength covariance"]
    result = {
        "source_file": str(source), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "rows": pf.metadata.num_rows, "parquet_schema": str(pf.schema_arrow),
        "analysis_records": [{"key": a, "fields": json.loads(b), "count": n} for (a, b), n in analyses.items()],
        "yield_metadata_variants": [{"role": a, "measurement": json.loads(b), "count": n} for (a, b), n in yields.items()],
        "custom_identifier_details": dict(custom_fields), "first_30_sample_names": samples,
        "present_measurement_provenance_paths": measurement_paths, "example": examples,
        "not_encoded_in_inspected_records": relevant_absences,
        "scope": "Metadata absence is restricted to these acquired ORD bytes. Raw/metadata may exist in the publisher Globus deposit; deposit not acquired here. Publication-record creation times are not acquisition timestamps. Sample strings encode some campaign/temperature/plate/well information but do not establish independent-batch replication.",
        "wall_seconds": time.monotonic() - started,
    }
    (ROOT / "ORD_MEASUREMENT_METADATA.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("present_measurement_provenance_paths", "example")}, indent=2))


if __name__ == "__main__":
    main()

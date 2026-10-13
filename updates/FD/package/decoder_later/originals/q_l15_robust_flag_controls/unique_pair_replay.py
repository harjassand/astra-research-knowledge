"""Replay matched n=16 controls while logging external ordered-pair IDs.

The source-call stream is written as decimal 32-bit pair keys to a temporary
file and externally sorted/deduplicated. This yields exact distinct external
pairs even after the learner memo reaches its 250,000-entry cap. Pair logging
is audit instrumentation; its bytes and sorting are reported separately from
the acquisition runtime.
"""
from __future__ import annotations

import json
import sys
import tempfile
import time
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
WAVE = HERE.parent
S09_DIR = WAVE / "q_s09_robust_flag_implementation"
if str(S09_DIR) not in sys.path:
    sys.path.insert(0, str(S09_DIR))

import run_experiment as s09
import rm_controls as rm


def run_logged(case: str) -> dict:
    with tempfile.TemporaryDirectory(prefix=f"pair-audit-{case}-", dir=HERE) as td:
        td = Path(td)
        raw = td / "external-pairs.txt"
        sorted_unique = td / "external-pairs-unique.txt"

        class LoggedSource(s09.PersistentSource):
            last_instance = None

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._pair_log = raw.open("w", encoding="ascii", buffering=1 << 20)
                type(self).last_instance = self

            def query(self, x, y):
                self._pair_log.write(f"{x | (y << self.n)}\n")
                return super().query(x, y)

            def close_pair_log(self):
                self._pair_log.close()

        start = time.perf_counter()
        if case == "s09":
            original = s09.PersistentSource
            s09.PersistentSource = LoggedSource
            try:
                receipt = s09.run_case(n=16, r=2, seed=960162, epsilon=1/32,
                                       beta=.05, mode="asymmetric_hash",
                                       bad_count=2048, sequential=True,
                                       pair_cache_cap=250000,
                                       canonicalize=False)
            finally:
                s09.PersistentSource = original
        else:
            original = rm.PersistentSource
            rm.PersistentSource = LoggedSource
            try:
                factory = (rm.decoder_factory_full if case == "full-cube"
                           else rm.decoder_factory_local)
                receipt = rm.run_full_case(n=16, r=2, seed=960162,
                                           epsilon=1/32, beta=.05,
                                           mode="asymmetric_hash",
                                           bad_count=2048,
                                           pair_cache_cap=250000,
                                           decoder_factory=factory)
            finally:
                rm.PersistentSource = original
        # All source calls are made synchronously by the learner. Locate and
        # close the fixture logger without retaining source or labels.
        # run_case/run_full_case do not return the source object, so the class
        # keeps the most recent instance only for lifecycle cleanup.
        # (This attribute is installed below by the constructor wrapper.)
        source = LoggedSource.last_instance
        source.close_pair_log()

        sort_start = time.perf_counter()
        subprocess.run(["sort", "-u", str(raw), "-o", str(sorted_unique)],
                       check=True)
        with sorted_unique.open("rb") as f:
            unique_count = sum(1 for _ in f)
        sort_seconds = time.perf_counter() - sort_start
        call_count = (receipt.get("oracle", {}).get("source_calls")
                      if case == "s09" else
                      receipt.get("oracle", {}).get("external_source_calls"))
        receipt["external_pair_identity_audit"] = dict(
            exact_unique_ordered_pairs=unique_count,
            external_source_calls=call_count,
            repeated_external_pair_calls=call_count - unique_count,
            pair_key_encoding="x | (y << 16), preserving source direction",
            pair_log_bytes_written=raw.stat().st_size,
            audit_sort_seconds=sort_seconds,
            audit_runtime_excluded_from_acquisition_seconds=True,
            pair_logging_overhead_included_in_receipt_seconds=True,
            exactness="external sort -u over every source.query call")
        receipt["pair_audit_total_wall_seconds"] = time.perf_counter() - start
        return receipt


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("case", choices=["s09", "full-cube", "local-full"])
    args = parser.parse_args()
    receipt = run_logged(args.case)
    names = {"s09": "unique_pairs_s09_n16.json",
             "full-cube": "unique_pairs_full_cube_n16.json",
             "local-full": "unique_pairs_local_rm_n16.json"}
    out = HERE / names[args.case]
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(dict(output=str(out), case=args.case,
                          finite_result=receipt.get("finite_result"),
                          acquisition_seconds=receipt.get("seconds"),
                          pair_audit_total_wall_seconds=receipt.get(
                              "pair_audit_total_wall_seconds"),
                          source_calls=receipt.get("external_pair_identity_audit", {}).get(
                              "external_source_calls"),
                          exact_unique_pairs=receipt.get(
                              "external_pair_identity_audit", {}).get(
                                  "exact_unique_ordered_pairs"),
                          repeat_external_calls=receipt.get(
                              "external_pair_identity_audit", {}).get(
                                  "repeated_external_pair_calls")), indent=2))


if __name__ == "__main__":
    main()

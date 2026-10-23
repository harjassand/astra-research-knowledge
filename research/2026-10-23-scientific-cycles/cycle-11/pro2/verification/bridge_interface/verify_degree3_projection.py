"""Independent literal check of the NEW degree-three projection only.

No imports from the producer, no grammar closure search or old suite replay.
The inherited 73-family semantic theorem is an explicit proof dependency.
"""
from pathlib import Path
import argparse
import hashlib
import json
import resource
import time

SOURCE_SHA = "63f4cdfd7ccc3b3159782a28a144a199422a315975aa207e5d144e8659e53525"
SOURCE_BYTES = 982625
EXPECTED_IDS = {2, 4, 12, 14, 19, 24, 26, 30, 31, 33, 40, 44, 45, 52, 53, 54, 62, 63}


def channels(mask):
    assert isinstance(mask, int) and 0 <= mask < 16
    return {color for color in range(4) if mask & (1 << color)}


def check(source_path, projection_path):
    before, cpu = time.perf_counter(), time.process_time()
    raw = source_path.read_bytes()
    assert len(raw) == SOURCE_BYTES
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    source = json.loads(raw)
    projected_raw = projection_path.read_bytes()
    projection = json.loads(projected_raw)
    assert projection["source_sha256"] == SOURCE_SHA
    families = {family["id"]: family for family in source["families"]}
    relevant = {fid for fid, family in families.items()
                if family["degree"][0] == 2 and family["degree"][1] in (1, 2, 3)}
    assert relevant == EXPECTED_IDS
    rows = projection["rows"]
    assert len(rows) == len(relevant)
    assert len({row["family"] for row in rows}) == len(rows)
    assert {row["family"] for row in rows} == relevant
    checked = []
    for row in rows:
        family = families[row["family"]]
        target = family["targets"][row["target_index"]]
        assert target == row["inherited_target"]
        a, b, d_left, n_left, f_left, d_right, n_right, f_right = target
        assert [d_left, d_right] == family["degree"] == row["degree"]
        assert d_left == 2 and d_right in (1, 2, 3)
        assert a in range(4) and b in range(4) and a != b
        left_neighbors, left_flags = channels(n_left), channels(f_left)
        right_neighbors, right_flags = channels(n_right), channels(f_right)
        # The three possible positions of the new edge inside a P4.
        assert b not in left_flags
        assert a not in right_flags
        assert not (b in left_neighbors and a in right_neighbors)
        restored_neighbors = left_neighbors | {b}
        restored_flags = left_flags | ({b} if a in right_neighbors else set())
        assert len(restored_neighbors) <= 2
        assert channels(row["root_neighbor_upper_mask"]) == restored_neighbors
        assert channels(row["root_far_flag_upper_mask"]) == restored_flags
        missing = row["missing_color"]
        assert missing in range(4) and missing != a and missing not in restored_neighbors
        assert row["restored_root_degree"] == 3
        checked.append({"family": row["family"], "target_index": row["target_index"],
                        "root_color": a, "protected_neighbor_color": b,
                        "restored_neighbor_colors": sorted(restored_neighbors),
                        "missing_color": missing})
    result = {
        "schema": "astra-independent-degree3-projection-check/v1",
        "status": "PASS",
        "source_sha256": SOURCE_SHA,
        "source_bytes": len(raw),
        "projection_sha256": hashlib.sha256(projected_raw).hexdigest(),
        "projection_bytes": len(projected_raw),
        "literal_witnesses_checked": checked,
        "case_count": len(checked),
        "new_local_predicates_only": True,
        "producer_imports": False,
        "old_grammar_closure_rerun": False,
        "dependency": "Accepted native marked normalizer and 73-family semantic closure theorem, not reproved by this finite check.",
        "wall_seconds": time.perf_counter() - before,
        "cpu_seconds": time.process_time() - cpu,
        "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        "cost_scope": "Read/hash/parse two exact files and inspect 18 literal target witnesses; excludes startup, receipt serialization, source reading, authoring, inference and integration.",
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("projection", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = check(args.source, args.projection)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items()
                      if key != "literal_witnesses_checked"}, indent=2))

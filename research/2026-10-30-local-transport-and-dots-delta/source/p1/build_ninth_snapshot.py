#!/usr/bin/env python3
"""Build continuation nine after checking every predecessor byte and review pin."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import zipfile


PREDECESSOR_NAME = "Astra_P1_Designed_Transport_and_Event_Memory_20261030.zip"
PREDECESSOR_SHA = "2dc6f0020a3f6746ca5c37a0d6c2a054ae1c1a45ecc5b2f6dbf6323ceaca50bc"
OUTPUT_NAME = "Astra_P1_Local_Transport_Law_Realization_20261030.zip"
MANIFEST_NAME = "NINTH_CONTINUATION_MANIFEST.json"
PREFIX = "new_science/continuation9_20261030/"
PINS = {
    "SELECTIVE_TRANSPORT_COUPLING_AND_ACTION.md":
        "42b5d5537a2f357a05a8b1ff55d292414e23c84d50d99bf50d3527073afc3ce2",
    "LOCAL_PASSIVE_LAW_REALIZATION.md":
        "946ecd0eb2463bfa88bb1b27f0062bc1feca1eb679c49430af8fbf5cfae59148",
    "LOCAL_PASSIVE_LAW_REALIZATION_CORRECTION.md":
        "db9576980955f626d66fb8430cd85ed9e4ed3ec37c1bb66c4ee48a9b5d34f2cc",
    "PREPARED_CORRELATIONS_AND_CAUSAL_RESPONSE.md":
        "4d7a596bcbecb717ff7b33c5b1fd35449aa166584603d9b0cf4c9017f24a5974",
    "CAUSAL_RESPONSE_INTERFACE_CLARIFICATION.md":
        "1d43dfd576af8a898b5405f4401ce2789f6ed5a6203a96de9c3634a16c040052",
    "NONLINEAR_PARTICLE_FIELD_ATTACK.md":
        "6c3495f6f410cd5dc5fbd0e3a059dbc5ce4a7c095b824f440c3120be80239606",
    "NONLINEAR_PARTICLE_FIELD_CORRECTION.md":
        "ce0af85387965d85973dad267687a17c5b980870e40d755c71b524d7e78a8408",
    "MOBILITY_GEOMETRY_AND_OPERATION_CHOICE.md":
        "50410d4b89838cb520b1d27f07f1f7b658da038ed17fa74f3f1612c383147b60",
    "physical_mechanism/RECIPROCAL_WAVE_COUNTER.md":
        "893e1cd72c2acc64397021a86613a936bde8e345f9e0d03d2f433052cae2c97c",
    "physical_mechanism/CONSERVATIVE_LOSS_EXTENSION.md":
        "27d41f43fa1f033f39014b2294863213d76c24a4f5d76014cd201ccde00f2541",
    "physical_mechanism/TWO_SIDED_FLOW_TRANSFORMER_AND_FIXED_PORT_BOUNDARY.md":
        "3c4041365b04827a1814b7854413fbb6caa1dee14f0fe87200bb5da903efff7b",
    "record_geometry/FINITE_DURATION_LC_PROGRAM.md":
        "49acbebb439b5eaa2305ee273239101316261d4875be45015f188f8a744b8cf2",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def describe(path: Path, root: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.relative_to(root).as_posix(),
            "bytes": len(data), "sha256": digest(data)}


def main() -> None:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predecessor", type=Path,
                        default=root.parent / PREDECESSOR_NAME)
    parser.add_argument("--output", type=Path,
                        default=root.parent / OUTPUT_NAME)
    args = parser.parse_args()
    predecessor = args.predecessor.resolve()
    output = args.output.resolve()
    if output == predecessor or root == output or root in output.parents:
        raise ValueError("Output must be a new archive outside the research tree.")
    if digest(predecessor.read_bytes()) != PREDECESSOR_SHA:
        raise ValueError("Predecessor archive hash does not match the preserved source.")

    previous = []
    with zipfile.ZipFile(predecessor) as archive:
        infos = [i for i in archive.infolist() if not i.is_dir()]
        if len(infos) != 541:
            raise ValueError("Expected exactly 541 predecessor files.")
        names = set()
        for info in infos:
            name = PurePosixPath(info.filename)
            if name.is_absolute() or ".." in name.parts or info.filename in names:
                raise ValueError(f"Unsafe or duplicate archive path: {info.filename}")
            names.add(info.filename)
            path = root.joinpath(*name.parts)
            if not path.is_file() or path.is_symlink():
                raise ValueError(f"Missing or nonregular predecessor file: {info.filename}")
            original = archive.read(info)
            if path.read_bytes() != original:
                raise ValueError(f"Predecessor bytes changed: {info.filename}")
            previous.append({"path": info.filename, "bytes": len(original),
                             "sha256": digest(original)})

    for relative, expected in PINS.items():
        path = root / PREFIX / relative
        actual = digest(path.read_bytes())
        if actual != expected:
            raise ValueError(f"Reviewed input changed: {relative}: {actual}")

    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative == MANIFEST_NAME:
            continue
        if "__pycache__" in path.parts and relative not in names:
            continue
        if path.is_symlink():
            raise ValueError(f"Unexpected symlink: {relative}")
        files.append(path)
    files.sort(key=lambda p: p.relative_to(root).as_posix())
    additions = [describe(p, root) for p in files
                 if p.relative_to(root).as_posix() not in names]

    manifest = {
        "schema": "astra_p1.full_snapshot.v9",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "research_directory": PREFIX.rstrip("/"),
        "role": "Astra P1; same model and existing complementary allocation",
        "predecessor": {"filename": predecessor.name,
                        "sha256": PREDECESSOR_SHA,
                        "archive_bytes": predecessor.stat().st_size,
                        "files_verified_byte_for_byte": len(previous)},
        "unchanged_predecessor_files": sorted(previous, key=lambda x: x["path"]),
        "new_files": additions,
        "reviewed_input_pins": {PREFIX + k: v for k, v in PINS.items()},
        "file_count_including_this_manifest": len(files) + 1,
        "manifest_scope": "All files except this manifest are hashed; archive hash is emitted by the builder.",
        "scientific_status": {
            "completed": ["local selective Gaussian transport law and full action",
                          "uniform passive finite-band response/noise receiver with correction",
                          "fresh-force locality comparison with physical-geometry clarification",
                          "nonlinear exact invariance and whole-horizon protected-current bound",
                          "mobility diagnostic and strong ordinary flow-transformer alternative"],
            "not_established": ["nonlinear particle density/action receiver",
                                "local finite-bandwidth universal flow transformer",
                                "manufactured apparatus or acquired end-to-end budget",
                                "practical speedup or historical priority"],
        },
    }
    manifest_path = root / MANIFEST_NAME
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for path in files + [manifest_path]:
            archive.write(path, path.relative_to(root).as_posix())
    with zipfile.ZipFile(output) as archive:
        bad = archive.testzip()
        if bad is not None or len(archive.namelist()) != len(files) + 1:
            raise ValueError(f"Archive integrity check failed: {bad}")
    result = {"archive": str(output), "bytes": output.stat().st_size,
              "sha256": digest(output.read_bytes()),
              "predecessor_files_verified": len(previous),
              "new_files_excluding_manifest": len(additions),
              "total_files": len(files) + 1,
              "reviewed_inputs_verified": len(PINS),
              "archive_crc_check": "passed"}
    (root.parent / "NINTH_SNAPSHOT_BUILD_RESULT.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

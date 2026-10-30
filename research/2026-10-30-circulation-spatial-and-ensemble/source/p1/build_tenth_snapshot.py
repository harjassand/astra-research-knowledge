#!/usr/bin/env python3
"""Build continuation ten after checking every predecessor byte and review pin."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import zipfile


PREDECESSOR_NAME = "Astra_P1_Local_Transport_Law_Realization_20261030.zip"
PREDECESSOR_SHA = "fa6d446d0bdbfa633cb1976348c9c70dc00dfdbe4416cad07ec91e4e8e2c1cbe"
OUTPUT_NAME = "Astra_P1_Circulation_Law_and_Rare_Response_20261030.zip"
MANIFEST_NAME = "TENTH_CONTINUATION_MANIFEST.json"
PREFIX = "new_science/continuation10_20261030/"
PINS = {
    "NONLINEAR_CIRCULATION_OPERATION_AND_PATH_LAW.md": "53db4609d6b9a127c2898988a2f50684f4de7643d05c2156af516c19802a0c20",
    "MAIN_THEOREM_CLARIFICATIONS.md": "024205501076efa03c39121f6f5448e661a6b9c1bb62b161d664635ce9460309",
    "RARE_LAW_TYPICAL_LAW_AND_FORCE_LIMITS.md": "1a36eeda2df4523e25778f11ce71404ab2ee58a6e6d4b11c7c1125d4d8d50f13",
    "UNTUNED_PARTIAL_THERMAL_CARRIER.md": "b37e49509e6fc5e3eb0436f330c24159770be73ebb405f6705670d790ee3eb00",
    "UNTUNED_CARRIER_ARMING_SCOPE_CORRECTION.md": "97c9d2d0e6d4627677c55c2bf51d47521b1897ea4a1d6515ab185379549ad6cd",
    "record_geometry/DELAYED_CARRIER_QUEUE_BOUND.md": "b5683cc16a0775846de1bc825f25eb20e4450bfe8f7ae483b9c9376f2936204d",
    "record_geometry/FINITE_DURATION_INTERACTING_CARRIER_PORT.md": "362497578e0a88cd0b85948804ee2526de06fc0198fc60ccc1aeb58db19d6ed6",
    "record_geometry/LOCAL_COUNTER_COMMUNICATION_AND_SOURCE_SCOPE.md": "ad5a68fb11dca0cc81cbde5e6274834295c3412b772254b1455925f8b9d0527c",
    "record_geometry/PARTIAL_REFRESH_CELL_CONSTRUCTIVE_CHECK.md": "3d918f42ce3db48c24376b7905930de583bb2378cc577a15929e2dc3c830ba80",
    "physical_mechanism/PARTIAL_REFRESH_FORCE_WORK.md": "b9e869b0daa990896a0ed316d7040a40438d93868da6701e7ac3a67913215bbb",
    "verify_circulation_operation.py": "3ad87861d4ae9270bf51f6670474e88abb4e3cd1966f2b84067dc7cbaa9cd849",
    "verify_partial_thermal_carrier.py": "3671a052ba20501e1bcb1467a4b888b7aea9c01c7f34c3eea198ad2dead56a32"
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
        if len(infos) != 606:
            raise ValueError("Expected exactly 606 predecessor files.")
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
        "schema": "astra_p1.full_snapshot.v10",
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
            "completed": [
                        "physical nonlinear circulation-history map with unchanged interacting density paths",
                        "rare arming preserving ordinary records while changing macroscopic rare laws",
                        "explicit noncommuting weak-force and large-system limits",
                        "finite-response untuned partial-thermal carrier with actual work comparison",
                        "actual local count protocol, ordinary alternatives and internal reviews"
            ],
            "not_established": [
                        "arbitrary spatial flow law or two-dimensional volume-speed receiver",
                        "manufactured apparatus or acquired end-to-end confidence budget",
                        "arbitrary pulse jitter or carrier-dependent coupling robustness",
                        "total-resource advantage, practical speedup or historical priority"
            ]
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
    (root.parent / "TENTH_SNAPSHOT_BUILD_RESULT.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

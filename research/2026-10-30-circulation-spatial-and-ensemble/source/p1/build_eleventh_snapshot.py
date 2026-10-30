#!/usr/bin/env python3
"""Build continuation eleven after verifying predecessor bytes and actual review pins."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import zipfile


PREDECESSOR_NAME = "Astra_P1_Circulation_Law_and_Rare_Response_20261030.zip"
PREDECESSOR_SHA = "a4268f97669b0bccf48dd16424c9c81a8b38387147c28f23be6617ea25addd37"
OUTPUT_NAME = "Astra_P1_Spatial_Law_and_Passive_Record_20261030.zip"
MANIFEST_NAME = "ELEVENTH_CONTINUATION_MANIFEST.json"
PREFIX = "new_science/continuation11_20261030/"
PINS = {
    "CONSTRUCTION_SELECTION.md": "b3b6f2c3ca19a91cbd3f2f25e4843e5c59a27be2806815dc040ff429c9d15b22",
    "ELASTIC_CARRIER_LAYER_AND_DENSITY_LAW.md": "7f3ecd1fcc7ac70b451fe10a206fd0df17d0bc679dbd90e7f85bc307ea31606a",
    "ELASTIC_LAYER_CORRECTIONS.md": "35a6d351f969e43d64ca002958bb50a5ce2c6fdfd29cd6a374168766181a62b1",
    "JOINT_SPATIAL_TRACKING_AND_NONLINEAR_PROGRAM.md": "dd815be2bc16a734d377f8a141dc117383ff6c6357650a690e55f3d43a2d84ae",
    "SPATIAL_TRACKING_AND_WORK_CLARIFICATIONS.md": "220c8232cb3f97fb352d8e76b60fa9b855d219fb5e9c930925941c71db050241",
    "SPATIAL_ACTION_WORK_AND_APPARATUS_SCOPE.md": "e2c45f5ff21e15e69cca4a815a7ecf322e5b7ababe95ce9c951301a4ead7e904",
    "READOUT_ATTACK_FINITE_RESPONSE_AND_WORK.md": "b89e4fd78aa92a2d035669f9c589ed0ced663af052d952dd39389c7fec2a4038",
    "METERED_FINITE_CELL_AND_SPATIAL_ERROR.md": "dc141155fe9933e9a7c2cd475ec01aa7d2f02ac251ebcd6188fd61a0d391a655",
    "CONTINUOUS_ROW_RECEIVER_AND_LOADED_SCOPE.md": "06b57066f45b59966388534eab9853dc409c8a22f9368b6ea28693dea9d690fb",
    "METERED_RECEIVER_BINDING_CORRECTIONS.md": "1e37f5ae7b7b0059c6d098ae836fbfc31e51000646a900ee9291c3b93fb8f2f1",
    "PRIMARY_PREDECESSORS_AND_SELECTION.md": "763a64bbea1008d2731aa216def16a59f871776540e4661abfd5c44aada91465",
    "RESULT.md": "45ed33a7a4ceb5f6fa72c9e00069f099cfa4166f76158f1378d1d65ceb79e416",
    "EXECUTION_NOTES.md": "ac0cd23a5a7aae5ab531293d63900ca2145259810abc6258b0d1293510b914e0",
    "verify_elastic_spatial_program.py": "3039762ff835c6f55ac332ff1ee8a393c7d9059cde2d328289975e18d82c4f9c",
    "verify_metered_carrier_and_recorder.py": "cf8e17ba4521619ea406b94adac89cb0f9b88cf77945902c47f21be5871b87a0",
    "physical_mechanism/FINITE_RATE_SINGLE_FILE_GEAR.md": "a2135db7a80f7874d7d142ca700391515ab1e85799e7958c9cddcb121e61e071",
    "physical_mechanism/PASSIVE_NATIVE_GEAR_AND_LOAD.md": "7ac360ab3628d35bc20c8dbf4bd896de940f3c0a775fe79458290ff18fb95576",
    "physical_mechanism/UNCALIBRATED_TRAIN_GOVERNOR_AND_WORK.md": "cd4ef3ecdebe068470d03fe08e93d52e34fcfb22352103696fcec565729e4d97",
    "physical_mechanism/PASSIVE_FINITE_RESPONSE_DISPLACEMENT_RECORDER.md": "83b0a3aff1d2ae35b4960eef68718b754575e76e86c3c1e2610048fe9eedef04",
    "physical_mechanism/check_native_gears.py": "965a3d88bafe5589a8c157f82ffdd2e240533d655b00a4b5c4d0e7b697479bbb",
    "physical_mechanism/receiving_review/JOINT_SPATIAL_TRACKING_RECEIVING_REVIEW.md": "c09a156aec06b74d98bb3fb41adb045975ed9aab03fe43da143cf61ae72466a0",
    "physical_mechanism/receiving_review/SPATIAL_ACTION_WORK_RECEIVING_REVIEW.md": "bb64371460b61ab808fc9346b27c32371d6ab4e0b5282b2c2d60dcf757d47441",
    "physical_mechanism/receiving_review/CONTINUOUS_ROW_RECEIVING_REVIEW_AND_PASSIVE_CORRECTION.md": "eff524f0aaa29f4291d9e648bf9e65da3048b9a2095c280d33e7d73720ac29c2",
    "record_geometry/SINGLE_FILE_CONTACT_CONTROLS_NATIVE_DENSITY.md": "b0101449c47336f52ca40d040fdc0a0541dc8ea01867110196f79af49186dd94",
    "record_geometry/TRACER_FREE_ENERGY_FORMULA_CORRECTION.md": "c74a529b5e15e77efe0584182a8f3a301e8bd04501747e57e1e79946ffae1137",
    "record_geometry/DOWNSTREAM_EVENT_READOUT_AND_VOLUME_PRECISION.md": "e5d509f5c5e924e1022e18915447dfce22eeef815d5caa762a05641f83f56fee",
    "record_geometry/TAGGED_POSITION_MARKS_REMOVE_FIXED_LOSS_FLOOR.md": "2a1ebc5a8b0c910ba5e94d3bd3af707e667ddfea31d6512d759d7429cde664f7",
    "record_geometry/check_driven_tracer.py": "2fa86f488b963d6527b988fbb2764c98a15b004af86998ee783502b17bf2c6b3",
    "record_geometry/receiving_review/ELASTIC_CARRIER_LAYER_RECEIVING_REVIEW.md": "13ef67e0cebeaa2db94c7c9155ac2d7a9a587318602c62eba308ea5d6212fe17",
    "record_geometry/receiving_review/ELASTIC_PRODUCT_SOURCE_SCOPE_RECEIPT.md": "40dc5925bdec940441e57a1352d43729d9b1a32b80e6fd86023c3b8f87a66785",
    "record_geometry/receiving_review/METERED_FINITE_CELL_RECEIVING_REVIEW.md": "e15a801d0fdbbbd8914d7945a8db1375d1732e9825408ec6b0ef016e9183828d",
}
ROLE_MANIFESTS = [
    "physical_mechanism/MANIFEST.json",
    "record_geometry/RECEIVING_MANIFEST.json",
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_relative(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError(f"Unsafe relative path: {name}")
    return path


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
        raise ValueError("Predecessor hash does not match the preserved source.")

    previous = []
    names = set()
    with zipfile.ZipFile(predecessor) as archive:
        infos = [i for i in archive.infolist() if not i.is_dir()]
        if len(infos) != 652:
            raise ValueError("Expected exactly 652 predecessor files.")
        for info in infos:
            relative = safe_relative(info.filename)
            if info.filename in names:
                raise ValueError(f"Duplicate archive path: {info.filename}")
            names.add(info.filename)
            path = root.joinpath(*relative.parts)
            if not path.is_file() or path.is_symlink():
                raise ValueError(f"Missing or nonregular predecessor: {info.filename}")
            original = archive.read(info)
            if path.read_bytes() != original:
                raise ValueError(f"Predecessor bytes changed: {info.filename}")
            previous.append({"path": info.filename, "bytes": len(original),
                             "sha256": digest(original)})

    for relative, expected in PINS.items():
        actual = digest((root / PREFIX / relative).read_bytes())
        if actual != expected:
            raise ValueError(f"Pinned input changed: {relative}: {actual}")

    role_receipts = []
    for relative in ROLE_MANIFESTS:
        manifest_path = root / PREFIX / relative
        role_manifest = json.loads(manifest_path.read_text())
        for entry in role_manifest["files"]:
            path = manifest_path.parent.joinpath(*safe_relative(entry["file"]).parts)
            data = path.read_bytes()
            if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
                raise ValueError(f"Role manifest mismatch: {relative}: {entry['file']}")
        role_receipts.append({**describe(manifest_path, root),
                              "entries_verified": len(role_manifest["files"])})

    files = []
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Unexpected symlink: {path.relative_to(root)}")
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative == MANIFEST_NAME:
            continue
        if "__pycache__" in path.parts and relative not in names:
            continue
        files.append(path)
    files.sort(key=lambda p: p.relative_to(root).as_posix())
    additions = [describe(p, root) for p in files
                 if p.relative_to(root).as_posix() not in names]

    manifest = {
        "schema": "astra_p1.full_snapshot.v11",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "research_directory": PREFIX.rstrip("/"),
        "role": "Astra P1; same model and existing complementary allocation",
        "predecessor": {"filename": predecessor.name,
                        "sha256": PREDECESSOR_SHA,
                        "archive_bytes": predecessor.stat().st_size,
                        "files_verified_byte_for_byte": len(previous)},
        "unchanged_predecessor_files": sorted(previous, key=lambda x: x["path"]),
        "new_files": additions,
        "pinned_inputs_reviews_and_checks": {PREFIX + k: v for k, v in PINS.items()},
        "verified_role_manifests": role_receipts,
        "file_count_including_this_manifest": len(files) + 1,
        "manifest_scope": "All files except this manifest are hashed; archive hash is emitted by the builder.",
        "scientific_status": {
            "completed_at_stated_interfaces": [
                "locally prepared elastic auxiliary charge layer with joint volume-scale density control",
                "delayed nonlinear spatial shear-current program and physical path-law contraction",
                "true carrier-force work comparison with sustained-load lower bound",
                "passive displacement memory and native-marginal rare-law comparison",
                "actual metered finite thermal cell and attainable joint spatial-error receiver",
                "continuous nonlinear fixed-row receiver with direct loaded source and work moments",
                "constructive gears, tracers, emitted-count and tagged-position alternatives",
                "executed population-model checks and actual pinned internal reviews"
            ],
            "not_established": [
                "final external pointer reader with acquired full conditional noise and force budget",
                "complete apparatus-record equality or total-variation noninvasiveness of passive probing",
                "arbitrary two-dimensional current or vorticity control",
                "native good path LDP for every unknown nonlinear potential",
                "order-volume total apparatus work or practical efficiency advantage",
                "manufactured device, historical priority or civilisation-scale impact"
            ],
            "binding_corrections": [
                "ELASTIC_LAYER_CORRECTIONS.md",
                "SPATIAL_TRACKING_AND_WORK_CLARIFICATIONS.md",
                "METERED_RECEIVER_BINDING_CORRECTIONS.md",
                "physical_mechanism/receiving_review/CONTINUOUS_ROW_RECEIVING_REVIEW_AND_PASSIVE_CORRECTION.md",
                "record_geometry/TRACER_FREE_ENERGY_FORMULA_CORRECTION.md"
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
    result = {
        "archive": str(output),
        "bytes": output.stat().st_size,
        "sha256": digest(output.read_bytes()),
        "predecessor_files_verified": len(previous),
        "new_files_excluding_manifest": len(additions),
        "total_files": len(files) + 1,
        "pinned_inputs_reviews_and_checks_verified": len(PINS),
        "role_manifest_entries_verified": sum(x["entries_verified"] for x in role_receipts),
        "archive_crc_check": "passed",
    }
    (root.parent / "ELEVENTH_SNAPSHOT_BUILD_RESULT.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the research archive from an explicit whitelist; preserve the prior ZIP."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
DEST = WORKSPACE / "deliverables"
STAGE = DEST / "noisy_thermal_interface_research_package"
PACKAGE_NAME = "Astra_Noisy_Thermal_Interface"
PRIOR_NAME = "Astra_Thermal_Register_Research_Package.zip"
PRIOR_HASH = "fcc57d7e78d9561e87a8bb557347bc9d8bb106dd318d51971d16ef393bf39394"
PRIOR_BYTES = 9131625
FILES = [
    "operation_theorem.md", "inverse_noise_theorem.md",
    "endpoint_route/same_code_controller_bridge.md",
    "endpoint_route/endpoint_and_refresh.md",
    "passive_route/static_tree_regenerator.md",
    "passive_route/history_erasing_bell_export.md",
    "passive_route/soft_polymer_sampling_lemma.md",
    "passive_route/noisy_acquisition_and_control.md",
    "verify_precompensation.py", "precompensation_verification.json",
    "precompensation_verification.md", "precompensation_verification.png",
    "precompensation_verification.pdf",
    "classical_tree_regenerator.py", "classical_tree_regenerator.json",
    "classical_tree_regenerator.png", "classical_tree_regenerator.pdf",
    "passive_route/check_static_tree.py", "passive_route/static_tree_checks.json",
    "endpoint_route/check_interface_identities.py",
    "endpoint_route/interface_identity_checks.json",
    "verify_blackout_boundary.py", "blackout_boundary_checks.json",
    "build_report.py", "run_all_checks.py", "finite_check_receipt.json", "build_package.py",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    prior = DEST / PRIOR_NAME
    assert prior.stat().st_size == PRIOR_BYTES
    assert digest(prior) == PRIOR_HASH, "Predecessor changed; do not replace it silently."
    required = [ROOT / name for name in FILES]
    required += [ROOT / "README_PACKAGE.txt", DEST / "Astra_Noisy_Thermal_Interface.pdf",
                 DEST / "Astra_Noisy_Thermal_Interface_text.txt"]
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)
    STAGE.mkdir(parents=True, exist_ok=True)
    package = STAGE / PACKAGE_NAME
    if package.exists():
        shutil.rmtree(package)
    package.mkdir()
    shutil.copy2(ROOT / "README_PACKAGE.txt", package / "README.txt")
    for name in FILES:
        target = package / "noisy_interface_work" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    for name in ("Astra_Noisy_Thermal_Interface.pdf", "Astra_Noisy_Thermal_Interface_text.txt"):
        shutil.copy2(DEST / name, package / name)
    (package / "predecessors").mkdir()
    shutil.copy2(prior, package / "predecessors" / PRIOR_NAME)
    (package / "PRESERVATION_RECEIPT.json").write_text(json.dumps({
        "predecessor": "predecessors/" + PRIOR_NAME,
        "bytes": PRIOR_BYTES,
        "sha256": PRIOR_HASH,
        "action": "Unchanged byte-for-byte copy; no predecessor theorem or manifest re-audit.",
        "scope": "Preserves earlier independent physical contracts and named sampler-route obstructions.",
    }, indent=2) + "\n")
    manifest = []
    for path in sorted(package.rglob("*")):
        if path.is_file():
            manifest.append({"path": path.relative_to(package).as_posix(),
                             "bytes": path.stat().st_size, "sha256": digest(path)})
    (package / "SHA256_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    archive = DEST / "Astra_Noisy_Thermal_Interface_Research_Package.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as handle:
        for path in sorted(package.rglob("*")):
            if path.is_file():
                handle.write(path, path.relative_to(STAGE))
    with zipfile.ZipFile(archive) as handle:
        assert handle.testzip() is None
    print(json.dumps({"pdf": str(DEST / "Astra_Noisy_Thermal_Interface.pdf"),
                      "archive": str(archive), "archive_bytes": archive.stat().st_size,
                      "archive_sha256": digest(archive), "files": len(manifest) + 1,
                      "predecessor_preserved": True}, indent=2))


if __name__ == "__main__":
    main()

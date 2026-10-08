#!/usr/bin/env python3
"""Package retained research artifacts without redistributing acquired papers.

Packaging integrity is not mathematical verification. Run stage only after the
scientific files have been frozen, and seal only after final report edits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "outputs" / "research"
ALLOWED = {".md", ".txt", ".json", ".jsonl", ".py", ".log", ".tex"}
ACQUIRED_OUTSIDE_SOURCES = {
    "independent/phase2/backman_et_al2606.13960.txt",
    "independent/phase2/larson2607.02208.txt",
    "independent/phase2/lason_michalek1302.5236.txt",
    "independent/phase2/oh21720652.txt",
    "independent/phase2/hodge-02-tensors.tex",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def classification(path: Path, rel: Path) -> tuple[bool, str]:
    if any(p in {"__pycache__", "tmp", ".DS_Store"} for p in rel.parts):
        return False, "transient file"
    if rel.as_posix() in ACQUIRED_OUTSIDE_SOURCES:
        return False, "acquired source text; retain citation and hash, not full text"
    if "sources" in rel.parts and path.suffix != ".json":
        return False, "acquired source; retain citation and hash, not full text"
    if path.suffix not in ALLOWED:
        return False, "acquired binary source or unsupported/transient format"
    if "sources" in rel.parts:
        return True, "source acquisition metadata"
    return True, "retained research proof, audit, diagnostic, provenance or history"


def stage() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    source = ROOT / "work" / "agents"
    rows = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(source)
        keep, reason = classification(path, rel)
        row = {"source": "work/agents/" + rel.as_posix(),
               "included": keep, "classification": reason,
               "bytes": path.stat().st_size, "sha256": sha(path)}
        if keep:
            target = DEST / "proofs" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            assert sha(target) == row["sha256"]
            row["package_path"] = target.relative_to(DEST).as_posix()
        rows.append(row)
    programme = ROOT / "work" / "programme"
    for name in ("run.json", "dispatch.jsonl", "resource_usage.json",
                 "resource_usage.md", "resource_usage.py", "CHARTER.txt",
                 "intake_session.json", "COORDINATOR_STATE.txt",
                 "package_research.py", "replay_diagnostics.py", "plot_rate_phase.py",
                 "plot_critical_window.py", "validate_package.py", "frozen_proofs.json"):
        path = programme / name
        if path.is_file():
            target = DEST / "process" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    payload = {"created_utc": utc(),
               "scope": "Included artifacts are byte-preserving copies. Exclusions remain in the local work directory. This inventory certifies packaging only.",
               "records": rows}
    (DEST / "ARTIFACT_INVENTORY.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"included": sum(r["included"] for r in rows),
                      "excluded": sum(not r["included"] for r in rows),
                      "destination": str(DEST)}))


def seal() -> None:
    rows = []
    for path in sorted(DEST.rglob("*")):
        if path.is_file() and path.name not in {"SHA256SUMS", "PACKAGE_MANIFEST.json"}:
            rows.append({"path": path.relative_to(DEST).as_posix(),
                         "bytes": path.stat().st_size, "sha256": sha(path)})
    manifest = {"sealed_utc": utc(), "status": "packaging integrity only, not theorem certification", "files": rows}
    (DEST / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    checksum_paths = [DEST / row["path"] for row in rows] + [DEST / "PACKAGE_MANIFEST.json"]
    (DEST / "SHA256SUMS").write_text("".join(f"{sha(p)}  {p.relative_to(DEST).as_posix()}\n" for p in checksum_paths))
    archive = DEST.parent / "research-checkpoint.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as out:
        for path in sorted(DEST.rglob("*")):
            if path.is_file():
                out.write(path, "research/" + path.relative_to(DEST).as_posix())
    with zipfile.ZipFile(archive) as inp:
        assert inp.testzip() is None
        for name in inp.namelist():
            p = DEST / Path(name).relative_to("research")
            assert hashlib.sha256(inp.read(name)).hexdigest() == sha(p)
    (DEST.parent / "research-checkpoint.zip.sha256").write_text(f"{sha(archive)}  {archive.name}\n")
    print(json.dumps({"archive": str(archive), "bytes": archive.stat().st_size,
                      "sha256": sha(archive), "verified_files": len(rows)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("stage", "seal"))
    args = parser.parse_args()
    {"stage": stage, "seal": seal}[args.action]()

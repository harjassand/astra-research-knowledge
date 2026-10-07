"""Package derived research capital; byte validation is not theorem validation."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
def digest(data):
    return hashlib.sha256(data).hexdigest()

def selected(p):
    rel = p.relative_to(ROOT)
    parts = set(rel.parts)
    # Full downloaded manuscripts are retained locally, with hashes below.
    if p.suffix.lower() in {".pdf", ".html", ".htm", ".tex", ".png", ".jpg", ".gz"}:
        return False
    if p.suffix.lower() == ".md":
        return True
    if p.suffix.lower() in {".json", ".csv"}:
        return p.stat().st_size < 2_000_000
    if p.suffix.lower() in {".py", ".cpp", ".lean"}:
        return True
    if "root_replay" in parts and p.suffix == ".log":
        return True
    if p.suffix.lower() == ".txt":
        if re.search(r"report|audit|proof|check|diagnostic|candidate|obstruction|regularization|barrier|source_sha|source_commit|source_snapshot|result|outcome|verification|incompatibility", p.name, re.I):
            return p.stat().st_size < 100_000
    return False

payload = {}
omitted = []
for base in (ROOT / "work/agents", ROOT / "work/root_replay"):
    for p in sorted(base.rglob("*")):
        if not p.is_file() or p.is_symlink() or "__pycache__" in p.parts:
            continue
        data = p.read_bytes()
        path = str(p.relative_to(ROOT))
        if selected(p):
            payload[path] = data
        else:
            omitted.append({"local_path": path, "bytes": len(data), "sha256": digest(data),
                            "note": "Omitted source, binary, or intermediate; primary retrieval handles are in branch reports and provenance files."})

for name in ["work/RESEARCH_PROTOCOL.txt", "work/ACTIVE_CONTEXT.txt", "work/build_deliverables.py", "work/package_evidence.py",
             "work/repository/astra_commit.txt", "work/repository/openai_commit.txt", "work/repository/OPENAI_MATH_LICENSE.txt",
             "outputs/frontier_research.tex", "outputs/RESULT_CARDS.json", "outputs/START_HERE.txt"]:
    p = ROOT / name
    payload[name] = p.read_bytes()

for p in sorted((ROOT / "work/repository").iterdir()):
    if p.is_file() and str(p.relative_to(ROOT)) not in payload:
        data = p.read_bytes()
        omitted.append({"local_path": str(p.relative_to(ROOT)), "bytes": len(data), "sha256": digest(data),
                        "note": "Pinned repository intake; exact upstream handles are in the repository metadata and primary source notes."})

source_manifest = {
    "policy": "Downloaded full manuscripts remain local rather than being redistributed. These hashes establish file identity only. Source URLs and repository paths appear in the preserved branch reports and provenance manifests.",
    "repositories": {"astra": {"url": "https://github.com/harjassand/astra-research-knowledge", "commit": "778b78af5d4bbde608ce3fc775049ceaeb55a2d3"},
                     "openai_math": {"url": "https://github.com/openai/math", "commit": "adc7f1241b42e322a6451854ab7e4b4c146bf78a"}},
    "omitted_local_files": omitted
}
payload["SOURCE_FILES.json"] = (json.dumps(source_manifest, indent=2) + "\n").encode()
notice = """THIRD-PARTY SOURCE CODE NOTICE
Code copied from openai/math retains the Apache License 2.0 in
work/repository/OPENAI_MATH_LICENSE.txt, at commit
adc7f1241b42e322a6451854ab7e4b4c146bf78a.
The Potts certificate_portable.cpp differs from the source certificate.cpp
only in its portable standard-library header; the branch provenance records
the exact source and change. Copied Lean files are source artifacts, not
new formal verification performed by this run.
All reports distinguish imported source claims from derived results.
"""
payload["THIRD_PARTY_NOTICE.txt"] = notice.encode()

cards = json.loads((OUT / "RESULT_CARDS.json").read_text())
for card in cards:
    assert card["proof"] in payload, f"Missing authoritative proof: {card['proof']}"
manifest = {"scope": "SHA256 file integrity only; no theorem, source correctness, or novelty certification.",
            "files": [{"path": name, "bytes": len(data), "sha256": digest(data)} for name, data in sorted(payload.items())]}
manifest_data = (json.dumps(manifest, indent=2) + "\n").encode()
payload["MANIFEST.json"] = manifest_data
(OUT / "MANIFEST.json").write_bytes(manifest_data)
(OUT / "SOURCE_FILES.json").write_bytes(payload["SOURCE_FILES.json"])
archive = OUT / "frontier_evidence.zip"
with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name, data in sorted(payload.items()):
        z.writestr(name, data)

# Reopen the final archive, check CRC, every file digest, and all card targets.
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for item in manifest["files"]:
        assert digest(z.read(item["path"])) == item["sha256"]
    assert len(z.namelist()) == len(payload)
validation = {"archive": archive.name, "bytes": archive.stat().st_size,
              "sha256": digest(archive.read_bytes()), "members": len(payload),
              "all_member_sha256_match": True, "crc_pass": True,
              "all_result_card_proofs_present": True,
              "root_replays": json.loads((ROOT / "work/root_replay/results.json").read_text()),
              "scope": "Archive integrity and recorded scoped executions; not mathematical or priority certification."}
latex_log = ROOT / "work/root_replay/latex_compile.json"
if latex_log.exists():
    compile_record = json.loads(latex_log.read_text())
    assert compile_record["source_sha256"] == digest((OUT / "frontier_research.tex").read_bytes())
    validation["native_latex_compile"] = compile_record
(OUT / "VALIDATION.json").write_text(json.dumps(validation, indent=2) + "\n")
print(json.dumps({k:v for k,v in validation.items() if k != "root_replays"}, indent=2))

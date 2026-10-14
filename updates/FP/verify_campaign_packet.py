#!/usr/bin/env python3
"""Verify frozen public authored packet bytes, without claiming scientific validity."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "updates/FP/package/campaign_v0001"
ZIP_SHA256 = "234955eacb1b10a1947eae609654a2a828487beacfc49185f88e9cbdec64e64a"
FULL_LOCAL_SHA256 = "3e12e5efd7bb688b8ac748eb239e1637ed37ce8fc431ff5cfc816832a10f3a73"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    archive = PACKET / "AUTHORED_EVIDENCE.zip"
    assert digest(archive.read_bytes()) == ZIP_SHA256
    manifest_bytes = (PACKET / "AUTHORED_MANIFEST.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    assert manifest["mission_status"] == "NOT_ACHIEVED"
    assert manifest["complete_local_archive_sha256"] == FULL_LOCAL_SHA256
    assert len(manifest["files"]) == 161
    expected = {row["path"]: row for row in manifest["files"]}
    assert len(expected) == len(manifest["files"])
    with zipfile.ZipFile(archive) as packet:
        names = packet.namelist()
        assert len(names) == len(set(names))
        assert set(names) == set(expected) | {"AUTHORED_MANIFEST.json"}
        assert packet.read("AUTHORED_MANIFEST.json") == manifest_bytes
        for name, row in expected.items():
            path = Path(name)
            assert not path.is_absolute() and ".." not in path.parts
            data = packet.read(name)
            assert len(data) == row["size_bytes"] and digest(data) == row["sha256"], name
        for name in ("REPORT.md", "CLAIM_LEDGER.json", "INDEX.json", "REPLAY_NOTES.md"):
            assert packet.read(name) == (PACKET / name).read_bytes()
        assert packet.read("root/REPLAY_RECEIPTS_v0004.json") == (PACKET / "REPLAY_RECEIPTS_v0004.json").read_bytes()
    ledger = json.loads((PACKET / "CLAIM_LEDGER.json").read_text())
    report = (PACKET / "REPORT.md").read_text()
    receipt = json.loads((PACKET / "REPLAY_RECEIPTS_v0004.json").read_text())
    assert ledger["mission_status"] == "NOT_ACHIEVED" and "MISSION STATUS: NOT_ACHIEVED" in report
    assert receipt["unique_scripts_successful"] == 27 and receipt["attempted"] == 29
    print(json.dumps({"status": "PASS_BYTE_INTEGRITY_ONLY", "manifest_entries": len(expected),
                      "archive_sha256": ZIP_SHA256, "mission_status": "NOT_ACHIEVED",
                      "unique_calculations_successful": 27, "attempts": 29,
                      "external_correctness_checked": False, "physical_validation": False}, sort_keys=True))


if __name__ == "__main__":
    main()

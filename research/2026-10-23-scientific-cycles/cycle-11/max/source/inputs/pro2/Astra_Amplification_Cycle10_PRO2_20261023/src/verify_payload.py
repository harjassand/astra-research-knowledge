"""Verify source payload bytes without executing any scientific program.

Usage: python verify_payload.py DIRECTORY_OR_ZIP
The expected MANIFEST.json is inside the supplied directory or ZIP.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    p = PurePosixPath(name)
    return not p.is_absolute() and ".." not in p.parts and "\\" not in name


def check(target):
    if target.is_dir():
        manifest = json.loads((target / "MANIFEST.json").read_text())
        actual = {
            f.relative_to(target).as_posix(): f.read_bytes()
            for f in target.rglob("*")
            if f.is_file() and "__pycache__" not in f.parts
            and f.name != "MANIFEST.json" and not f.name.endswith(".pyc")
        }
        crc = "not applicable: directory"
    else:
        with zipfile.ZipFile(target) as z:
            names = z.namelist()
            assert len(names) == len(set(names)), "duplicate archive member"
            assert all(safe_name(n) for n in names), "unsafe archive member"
            assert z.testzip() is None, "ZIP CRC mismatch"
            manifests = [n for n in names if n.endswith("/MANIFEST.json")]
            assert len(manifests) == 1, "one top-level payload manifest required"
            name = manifests[0]
            prefix = name[:-len("MANIFEST.json")]
            assert all(n.startswith(prefix) for n in names), "mixed archive roots"
            manifest = json.loads(z.read(name))
            actual = {n[len(prefix):]: z.read(n) for n in names
                      if not n.endswith("/") and n != name}
        crc = "PASS"
    assert manifest["schema"] == "astra-source-payload-manifest/v1"
    records = manifest["files"]
    expected = {r["path"]: r for r in records}
    assert len(expected) == len(records), "duplicate manifest path"
    assert set(actual) == set(expected), "payload inventory mismatch"
    for name, data in actual.items():
        r = expected[name]
        assert safe_name(name), "unsafe manifest path"
        assert len(data) == r["bytes"], name
        assert digest(data) == r["sha256"], name
    return dict(status="PASS", members=len(records),
                payload_bytes=sum(len(b) for b in actual.values()),
                zip_crc=crc,
                scope="Exact source bytes; no scientific program executed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    print(json.dumps(check(parser.parse_args().target), indent=2))

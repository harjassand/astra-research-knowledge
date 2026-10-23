"""Verify payload identity and source bindings; performs no scientific rerun."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

OLD = "sources/Astra_Intelligence_Cycle_PRO3_20261021.zip"
PINNED = {
    OLD: (363537, "5f49846ea3b1d74f72833e61d17896a8609b8909be07764a070c737a2cd80f0d"),
    "SAFE_LOCAL_THEOREM.md": (17966, "ad80cb6a4ec919585182ff0fc5210da6643bd9a3378264dace262b6715e9d3da"),
    "TEMPERED_SCREEN.md": (14197, "fa0d12398f3b2bbcaa417a591ab70b8ea33e76c4a940b6976c76018fe833f06c"),
}


def relevant(name):
    return name != "MANIFEST.json" and "__pycache__" not in Path(name).parts and not name.endswith(".pyc")


def check(read, names):
    manifest = json.loads(read("MANIFEST.json"))
    entries = manifest["payloads"]
    expected = {row["path"] for row in entries}
    actual = {name for name in names if relevant(name)}
    assert actual == expected, {"missing": sorted(expected-actual), "extra": sorted(actual-expected)}
    for row in entries:
        blob = read(row["path"])
        assert len(blob) == row["bytes"], row["path"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"], row["path"]
    for name, (size, digest) in PINNED.items():
        blob = read(name)
        assert len(blob) == size and hashlib.sha256(blob).hexdigest() == digest, name
    with zipfile.ZipFile(io.BytesIO(read(OLD))) as old:
        assert old.testzip() is None
    return {"status": "PASS", "payloads_verified": len(entries),
            "pinned_old_owner_source_and_two_proof_bindings": "PASS",
            "old_owner_zip_crc": "PASS", "scientific_rerun": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", type=Path)
    args = parser.parse_args()
    if args.zip:
        with zipfile.ZipFile(args.zip) as archive:
            assert archive.testzip() is None
            all_names = [i.filename for i in archive.infolist() if not i.is_dir()]
            manifests = [n for n in all_names if n.endswith("/MANIFEST.json")]
            assert len(manifests) == 1, manifests
            prefix = manifests[0][:-len("MANIFEST.json")]
            assert all(n.startswith(prefix) for n in all_names)
            names = [n[len(prefix):] for n in all_names]
            assert len(names) == len(set(names))
            assert all(not Path(n).is_absolute() and ".." not in Path(n).parts for n in names)
            result = check(lambda name: archive.read(prefix+name), names)
        result["archive_crc"] = "PASS"
        result["archive_bytes"] = args.zip.stat().st_size
        result["archive_sha256"] = hashlib.sha256(args.zip.read_bytes()).hexdigest()
    else:
        root = Path(__file__).resolve().parent
        names = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
        result = check(lambda name: (root/name).read_bytes(), names)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

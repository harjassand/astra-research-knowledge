"""Build and verify deterministic, byte-preserving N629 evidence archives."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile


FORMAT = "n629-raw-evidence-v1"


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect(source, prefix=""):
    source = Path(source).resolve()
    if not source.is_dir():
        raise ValueError(f"source is not a directory: {source}")
    prefix = PurePosixPath(prefix) if prefix else PurePosixPath()
    if prefix.parts and (prefix.is_absolute() or any(part in ("", ".", "..") for part in prefix.parts)):
        raise ValueError("prefix must be a safe relative path")
    members = []
    for path in sorted(source.rglob("*"), key=lambda p: p.relative_to(source).as_posix()):
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError(f"symbolic links are not supported: {path}")
        if stat.S_ISDIR(info.st_mode):
            continue
        if not stat.S_ISREG(info.st_mode):
            raise ValueError(f"not a regular file: {path}")
        relative = path.relative_to(source).as_posix()
        members.append({
            "path": (prefix / relative).as_posix(),
            "source_path": relative,
            "bytes": info.st_size,
            "mode": stat.S_IMODE(info.st_mode),
            "sha256": sha256_file(path),
        })
    if not members:
        raise ValueError("source directory contains no files")
    return members


def write_archive(source, archive, members):
    source, archive = Path(source).resolve(), Path(archive).resolve()
    if archive == source or source in archive.parents:
        raise ValueError("archive must be outside the source directory")
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", allowZip64=True) as bundle:
        bundle.comment = b""
        for member in members:
            info = zipfile.ZipInfo(member["path"], date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | member["mode"]) << 16
            info.extra = b""
            info.comment = b""
            bundle.writestr(info, (source / member["source_path"]).read_bytes(),
                            compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def pack(source, archive, manifest, prefix=""):
    source, archive, manifest = map(lambda p: Path(p).resolve(), (source, archive, manifest))
    if manifest == source or source in manifest.parents:
        raise ValueError("manifest must be outside the source directory")
    if archive.exists() or manifest.exists():
        raise FileExistsError("refusing to overwrite an archive or manifest")
    members = collect(source, prefix)
    write_archive(source, archive, members)
    manifest_members = [{key: value for key, value in member.items() if key != "source_path"}
                        for member in members]
    record = {
        "format": FORMAT,
        "archive": archive.name,
        "source_prefix": prefix,
        "archive_bytes": archive.stat().st_size,
        "archive_sha256": sha256_file(archive),
        "member_count": len(members),
        "uncompressed_bytes": sum(member["bytes"] for member in members),
        "hash_scope": "SHA-256 of each member's exact uncompressed file bytes",
        "zip_metadata": "Sorted paths; fixed 1980-01-01 timestamps; normalized Unix file modes; DEFLATE level 9",
        "members": manifest_members,
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    return record


def safe_member(name):
    path = PurePosixPath(name)
    return (name == path.as_posix() and not path.is_absolute()
            and bool(path.parts) and all(part not in ("", ".", "..") for part in path.parts)
            and "\\" not in name and "\x00" not in name)


def verify(archive, manifest):
    archive, manifest = Path(archive).resolve(), Path(manifest).resolve()
    record = json.loads(manifest.read_text())
    if record.get("format") != FORMAT or record.get("archive") != archive.name:
        raise ValueError("archive/manifest identity mismatch")
    if archive.stat().st_size != record.get("archive_bytes"):
        raise ValueError("archive byte count mismatch")
    if sha256_file(archive) != record.get("archive_sha256"):
        raise ValueError("archive SHA-256 mismatch")

    expected = {row["path"]: row for row in record.get("members", [])}
    if len(expected) != record.get("member_count") or not expected:
        raise ValueError("manifest member count mismatch")
    if any(not safe_member(name) for name in expected):
        raise ValueError("unsafe archive member path in manifest")
    with zipfile.ZipFile(archive, "r") as bundle:
        infos = bundle.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)) or set(names) != set(expected):
            raise ValueError("archive member paths differ from manifest")
        for info in infos:
            if not safe_member(info.filename) or info.is_dir():
                raise ValueError(f"unsafe or unexpected archive entry: {info.filename}")
            row = expected[info.filename]
            if info.file_size != row["bytes"]:
                raise ValueError(f"member byte count mismatch: {info.filename}")
            mode = stat.S_IMODE(info.external_attr >> 16)
            if mode != row["mode"]:
                raise ValueError(f"member mode mismatch: {info.filename}")
            digest = hashlib.sha256()
            size = 0
            with bundle.open(info, "r") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    size += len(chunk)
                    digest.update(chunk)
            if size != row["bytes"] or digest.hexdigest() != row["sha256"]:
                raise ValueError(f"member SHA-256 mismatch: {info.filename}")
    total = sum(row["bytes"] for row in expected.values())
    if total != record.get("uncompressed_bytes"):
        raise ValueError("manifest uncompressed byte count mismatch")
    return {
        "status": "passed",
        "archive": archive.name,
        "archive_sha256": record["archive_sha256"],
        "member_count": len(expected),
        "uncompressed_bytes": total,
        "archive_bytes": record["archive_bytes"],
        "member_hashes_checked": len(expected),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("pack", help="create a deterministic ZIP and SHA-256 manifest")
    create.add_argument("source", type=Path, help="directory whose files will be archived")
    create.add_argument("--archive", required=True, type=Path)
    create.add_argument("--manifest", required=True, type=Path)
    create.add_argument("--prefix", default="", help="safe path prefix stored before each member name")
    check = commands.add_parser("verify", help="check archive hash, member hashes, paths, and modes")
    check.add_argument("archive", type=Path)
    check.add_argument("manifest", type=Path)
    args = parser.parse_args()
    result = (pack(args.source, args.archive, args.manifest, args.prefix) if args.command == "pack"
              else verify(args.archive, args.manifest))
    print(json.dumps({key: value for key, value in result.items() if key != "members"},
                     sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"evidence archive operation failed: {error}", file=sys.stderr)
        raise SystemExit(1)

#!/usr/bin/env python3
"""Read selected public ZIP members with bounded HTTP ranges; never fetch full ZIP.

The ZIP index was parsed from a separately retrieved central-directory range.
This script fetches only small official metadata entries. No downloaded source
is executed. Every member's decompression length and ZIP CRC are checked.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib
import json
import struct
import urllib.request
import zlib

ROOT = Path(__file__).resolve().parent
URL = "https://drive.usercontent.google.com/download?id=1QzSJkIpYYOtv_kNrC-fEvpW-M3rMm8tk&export=download&confirm=t"
SIZE = 1010489591
SELECTED = json.loads((ROOT / "SELECTED_METADATA_INDEX.json").read_text())


def fetch_range(start, end):
    request = urllib.request.Request(URL, headers={
        "User-Agent": "Astra-source-audit/1.0",
        "Range": f"bytes={start}-{end}",
    })
    with urllib.request.urlopen(request, timeout=45) as response:
        expected = f"bytes {start}-{end}/{SIZE}"
        if response.status != 206 or response.headers.get("Content-Range") != expected:
            raise RuntimeError("Server did not honor exact bounded range")
        blob = response.read(end-start+2)
    if len(blob) != end-start+1:
        raise RuntimeError("Unexpected bounded range length")
    return blob


def retrieve(member):
    relative = Path(member["name"])
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Unsafe member path")
    if member["bytes"] > 1000000 or member["compressed_bytes"] > 1000000:
        raise ValueError("Selection exceeds per-member cap")
    start = member["local_header_offset"]
    # Public archive's observed local extra fields are short. If one is longer,
    # the exact second range below retrieves only its required additional bytes.
    end = start + 30 + len(member["name"].encode("utf-8")) + 128 + member["compressed_bytes"] - 1
    blob = fetch_range(start, end)
    h = struct.unpack_from("<4s5H3I2H", blob)
    signature, version, flags, method, mtime, mdate, crc, csize, usize, nlen, elen = h
    if signature != b"PK\x03\x04" or method != member["method"] or flags & 1:
        raise ValueError("Unsupported/incorrect ZIP local header")
    header_length = 30 + nlen + elen
    expected_name = blob[30:30+nlen].decode("utf-8" if flags & 0x800 else "cp437")
    if expected_name != member["name"]:
        raise ValueError("ZIP header name mismatch")
    required = header_length + member["compressed_bytes"]
    if required > len(blob):
        blob += fetch_range(start+len(blob), start+required-1)
        end = start+required-1
    compressed = blob[header_length:required]
    if method == 8:
        data = zlib.decompress(compressed, -15)
    elif method == 0:
        data = compressed
    else:
        raise ValueError("Unsupported compression method")
    if len(data) != member["bytes"] or zlib.crc32(data) & 0xffffffff != member["crc32"]:
        raise ValueError("ZIP payload length or CRC mismatch")
    out = ROOT / "released_metadata" / relative
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return {
        "member": member["name"], "source_url": URL,
        "range": [start, end], "retrieved_bytes": len(blob),
        "payload_bytes": len(data), "crc32_verified": member["crc32"],
        "payload_sha256": hashlib.sha256(data).hexdigest(),
    }


if __name__ == "__main__":
    receipts, errors = [], []
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = {pool.submit(retrieve, m): m for m in SELECTED}
        for n, future in enumerate(as_completed(jobs), 1):
            try:
                receipts.append(future.result())
            except Exception as exc:
                errors.append({"member": jobs[future]["name"], "error": str(exc)})
            if n % 25 == 0:
                print(f"Completed {n}/{len(SELECTED)}; errors={len(errors)}", flush=True)
    report = {
        "archive_downloaded": False,
        "archive_bytes": SIZE,
        "selected_members": len(SELECTED),
        "completed_members": len(receipts),
        "member_range_bytes": sum(r["retrieved_bytes"] for r in receipts),
        "payload_bytes": sum(r["payload_bytes"] for r in receipts),
        "receipts": sorted(receipts, key=lambda r: r["member"]),
        "errors": errors,
        "limitation": "CRC and member hashes verified; whole-archive checksum not available or calculated.",
    }
    (ROOT / "SELECTED_METADATA_FETCH_RECEIPT.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k != "receipts"}, indent=2))
    if errors:
        raise SystemExit(1)

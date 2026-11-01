"""Read selected public ZIP entries via HTTP ranges; stdlib only.

Acquisition tooling, not a scientific acceleration claim. Every transfer is
recorded. Refuses responses that do not honor the requested range.
"""
import argparse
import binascii
import io
from contextlib import nullcontext
import json
from pathlib import Path
import struct
import time
import urllib.request
import zipfile
import zlib


class RemoteFile(io.RawIOBase):
    def __init__(self, url, size, tail=None):
        self.url, self.size, self.pos = url, size, 0
        self.cache = []
        self.transfers = []
        if tail is not None:
            self.cache.append((size - len(tail), tail))

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else self.pos + offset if whence == 1 else self.size + offset
        if not 0 <= self.pos <= self.size:
            raise ValueError("invalid remote seek")
        return self.pos

    def range(self, start, length):
        if length == 0:
            return b""
        for offset, data in self.cache:
            if offset <= start and start + length <= offset + len(data):
                return data[start-offset:start-offset+length]
        end = start + length - 1
        request = urllib.request.Request(self.url, headers={"Range": f"bytes={start}-{end}"})
        begin = time.perf_counter()
        with urllib.request.urlopen(request, timeout=90) as response:
            actual = response.headers.get("Content-Range", "")
            expected = f"bytes {start}-{end}/{self.size}"
            if response.status != 206 or actual != expected:
                raise RuntimeError(f"range rejected: {response.status} {actual}; expected {expected}")
            data = response.read(length + 1)
        if len(data) != length:
            raise RuntimeError(f"short/long range: {len(data)} != {length}")
        elapsed = time.perf_counter() - begin
        self.transfers.append({"url": self.url, "start": start, "bytes": length, "seconds": elapsed})
        self.cache.append((start, data))
        return data

    def read(self, n=-1):
        if n < 0:
            n = self.size - self.pos
        if n > 128*1024*1024:
            raise RuntimeError("unbounded or oversized read refused")
        n = min(n, self.size-self.pos)
        data = self.range(self.pos, n)
        self.pos += len(data)
        return data


def acquire(source_dir, record, names, output_dir):
    source_dir, output_dir = Path(source_dir), Path(output_dir)
    metadata = json.loads((source_dir / f"{record}_metadata.json").read_text())
    entry = next(f for f in metadata["files"] if f["key"] == "data.zip")
    tail_file = source_dir / f"{record}_zip_tail.bin"
    remote = RemoteFile(entry["links"]["self"], entry["size"], tail_file.read_bytes() if tail_file.exists() else None)
    index_file = source_dir / f"{record}_zip_index.json"
    with nullcontext() if index_file.exists() else zipfile.ZipFile(remote) as archive:
        if index_file.exists():
            index = json.loads(index_file.read_text())
            infos = {}
            for entry_data in index:
                info = zipfile.ZipInfo(entry_data["name"])
                info.file_size, info.compress_size = entry_data["size"], entry_data["compressed"]
                info.header_offset, info.compress_type = entry_data["offset"], entry_data["method"]
                info.CRC = entry_data["crc"]
                infos[info.filename] = info
        else:
            index = [{"name": i.filename, "size": i.file_size, "compressed": i.compress_size,
                      "offset": i.header_offset, "method": i.compress_type, "crc": i.CRC}
                     for i in archive.infolist()]
            index_file.write_text(json.dumps(index, indent=2))
            infos = {i.filename: i for i in archive.infolist()}
        for name in names:
            info = infos[name]
            header = remote.range(info.header_offset, 30)
            values = struct.unpack("<IHHHHHIIIHH", header)
            if values[0] != 0x04034b50:
                raise RuntimeError("bad local ZIP signature")
            start = info.header_offset + 30 + values[-2] + values[-1]
            destination = output_dir / name
            if not destination.resolve().is_relative_to(output_dir.resolve()):
                raise RuntimeError("ZIP path escapes destination")
            destination.parent.mkdir(parents=True, exist_ok=True)
            if info.compress_size < 16*1024*1024:
                compressed = remote.range(start, info.compress_size)
                data = zlib.decompress(compressed, -15) if info.compress_type == 8 else compressed
                if len(data) != info.file_size or binascii.crc32(data) != info.CRC:
                    raise RuntimeError("ZIP integrity failure")
                destination.write_bytes(data)
            else:
                begin = time.perf_counter()
                request = urllib.request.Request(remote.url, headers={"Range": f"bytes={start}-{start+info.compress_size-1}"})
                compressed_count, raw_count, crc = 0, 0, 0
                decompressor = zlib.decompressobj(-15) if info.compress_type == 8 else None
                temporary = destination.with_suffix(destination.suffix + ".partial")
                with urllib.request.urlopen(request, timeout=90) as response, temporary.open("wb") as output:
                    expected = f"bytes {start}-{start+info.compress_size-1}/{remote.size}"
                    if response.status != 206 or response.headers.get("Content-Range") != expected:
                        raise RuntimeError("streamed range rejected")
                    while chunk := response.read(min(4*1024*1024, info.compress_size-compressed_count)):
                        compressed_count += len(chunk)
                        raw = decompressor.decompress(chunk) if decompressor else chunk
                        output.write(raw)
                        raw_count += len(raw)
                        crc = binascii.crc32(raw, crc)
                        if compressed_count % (64*1024*1024) == 0:
                            print(json.dumps({"entry": name, "downloaded": compressed_count,
                                              "total_compressed": info.compress_size}), flush=True)
                    if decompressor:
                        raw = decompressor.flush()
                        output.write(raw)
                        raw_count += len(raw)
                        crc = binascii.crc32(raw, crc)
                if compressed_count != info.compress_size or raw_count != info.file_size or crc != info.CRC:
                    raise RuntimeError("streamed ZIP integrity failure")
                temporary.rename(destination)
                remote.transfers.append({"url": remote.url, "start": start, "bytes": compressed_count,
                                         "seconds": time.perf_counter()-begin})
            print(json.dumps({"acquired": name, "bytes": info.file_size,
                              "compressed": info.compress_size}), flush=True)
    receipt = {"record": record, "archive_size": entry["size"], "requested_entries": names,
               "transfers": remote.transfers,
               "new_transfer_bytes": sum(t["bytes"] for t in remote.transfers),
               "new_transfer_seconds": sum(t["seconds"] for t in remote.transfers),
               "scope": "Byte integrity only; not molecular or comparative validation."}
    receipt_file = source_dir / f"{record}_range_receipt_{time.time_ns()}.json"
    receipt_file.write_text(json.dumps(receipt, indent=2))
    return index, receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("record")
    parser.add_argument("names", nargs="*")
    parser.add_argument("--source-dir", default=str(Path(__file__).parent / "sources"))
    parser.add_argument("--output-dir", default=str(Path(__file__).parent / "acquired"))
    arguments = parser.parse_args()
    index, receipt = acquire(arguments.source_dir, arguments.record, arguments.names, arguments.output_dir)
    print(json.dumps({"entries": len(index), "receipt": receipt}, indent=2))

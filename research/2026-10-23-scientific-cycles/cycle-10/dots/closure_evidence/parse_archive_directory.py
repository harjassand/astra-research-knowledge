"""Read the recovered ZIP64 directory only. Does not run scientific calculations."""
from pathlib import Path
import json, struct

p = Path(__file__).resolve().parent
b = (p / 'monroe_zip_tail.bin').read_bytes()
eocd = b.rfind(b'PK\x06\x06')
signature, record_size, made, needed, disk, cd_disk, disk_count, total_count, cd_size, cd_offset = struct.unpack_from('<4sQ2H2L4Q', b, eocd)
assert signature == b'PK\x06\x06'
out = []
i = b.find(b'PK\x01\x02')
directory_start = i
while i >= 0 and b[i:i+4] == b'PK\x01\x02':
    v = struct.unpack_from('<4s6H3L5H2L', b, i)
    n, ex, cm = v[10:13]
    name = b[i+46:i+46+n].decode('utf-8')
    extra = b[i+46+n:i+46+n+ex]
    cs, us, offset = v[8], v[9], v[16]
    j = 0
    while j+4 <= len(extra):
        tag, size = struct.unpack_from('<HH', extra, j)
        data = extra[j+4:j+4+size]
        if tag == 1:
            k = 0
            if us == 0xffffffff:
                us = struct.unpack_from('<Q', data, k)[0]; k += 8
            if cs == 0xffffffff:
                cs = struct.unpack_from('<Q', data, k)[0]; k += 8
            if offset == 0xffffffff:
                offset = struct.unpack_from('<Q', data, k)[0]; k += 8
        j += 4+size
    out.append(dict(name=name, size=us, compressed_size=cs, header_offset=offset, compression=v[4], crc=v[7]))
    i += 46+n+ex+cm
assert len(out) == total_count == disk_count
assert i-directory_start == cd_size
metadata = json.loads((p / 'monroe_zenodo_metadata.txt').read_text())
assert metadata['files'][0]['size']-len(b)+directory_start == cd_offset
(p / 'monroe_zip_member_list.json').write_text(json.dumps(out, indent=2))
(p / 'monroe_directory_validation.json').write_text(json.dumps(dict(member_count=len(out), zip64_member_count=total_count, central_directory_bytes=cd_size, central_directory_offset=cd_offset, recovered_tail_bytes=len(b), full_archive_bytes=metadata['files'][0]['size'], all_directory_entries_recovered=True, full_archive_md5_verified=False), indent=2))
print('Recovered and verified directory entries:', len(out))

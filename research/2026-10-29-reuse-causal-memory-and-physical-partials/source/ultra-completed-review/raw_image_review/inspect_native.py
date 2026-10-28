"""Read-only native container and declared-record check; no pixel/query rerun.

Independent standard-library implementation. TIFF IFDs are inspected for
four existing source members; pixels are not decoded. Saved sufficient
statistics are checked only for their declared pairing and normalizer.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import struct
import time
import zipfile

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'independent_opening'


def ifds(blob):
    endian = {'II': '<', 'MM': '>'}[blob[:2].decode('ascii')]
    assert struct.unpack_from(endian + 'H', blob, 2)[0] == 42
    off = struct.unpack_from(endian + 'I', blob, 4)[0]
    pages = []
    seen = set()
    sizes = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 1,
             8: 2, 9: 4, 10: 8, 11: 4, 12: 8}
    names = {256: 'width', 257: 'height', 258: 'bits_per_sample',
             259: 'compression', 262: 'photometric',
             270: 'description', 277: 'samples_per_pixel',
             305: 'software', 306: 'datetime', 339: 'sample_format'}
    while off:
        assert off not in seen
        seen.add(off)
        n = struct.unpack_from(endian + 'H', blob, off)[0]
        page = {}
        for i in range(n):
            pos = off + 2 + 12 * i
            tag, typ, count = struct.unpack_from(endian + 'HHI', blob, pos)
            if tag not in names:
                continue
            size = sizes[typ] * count
            dataoff = pos + 8 if size <= 4 else struct.unpack_from(endian + 'I', blob, pos + 8)[0]
            raw = blob[dataoff:dataoff + size]
            assert len(raw) == size
            if typ == 2:
                value = raw.rstrip(b'\0').decode('utf8', errors='replace')
            elif typ in (1, 3, 4):
                value = list(struct.unpack(endian + {1: 'B', 3: 'H', 4: 'I'}[typ] * count, raw))
                if count == 1:
                    value = value[0]
            else:
                value = raw.hex()
            page[names[tag]] = value
        pages.append(page)
        off = struct.unpack_from(endian + 'I', blob, off + 2 + 12 * n)[0]
    return pages


def covariance(left, right):
    n = len(left)
    return Fraction(n * sum(a * b for a, b in zip(left, right)) - sum(left) * sum(right), n * (n - 1))


def main():
    started = time.perf_counter()
    inspected = []
    with zipfile.ZipFile(SOURCE / 'data' / 'MS_Images_H015.zip') as z:
        names = z.namelist()
        assert names == [f'B{i:05}.tif' for i in range(1, 501)]
        for name in ['B00001.tif', 'B00002.tif', 'B00003.tif', 'B00500.tif']:
            blob = z.read(name)
            pages = ifds(blob)
            assert len(pages) == 1
            assert (pages[0]['width'], pages[0]['height'], pages[0]['bits_per_sample']) == (512, 512, 16)
            inspected.append({'name': name, 'source_bytes': len(blob),
                              'sha256': hashlib.sha256(blob).hexdigest(),
                              'IFDs': pages})
    records = json.loads((SOURCE / 'DATA_MOMENTS.json').read_text())['records']
    assert [r['members'] for r in records] == [names[k:k + 2] for k in range(0, 500, 2)]
    totals0 = [r['left'][8] for r in records]
    totals1 = [r['right'][8] for r in records]
    empirical = covariance(totals0, totals1)
    assert empirical == Fraction(-28011124984208, 6225)
    blocks = [covariance(totals0[k:k + 25], totals1[k:k + 25]) for k in range(0, 250, 25)]
    receipt = json.loads((SOURCE / 'DATA_RECEIPT.json').read_text())
    for value, declared in zip(blocks, receipt['ten_contiguous_block_diagnostics_no_iid_confidence']):
        assert value == Fraction(declared['normalizer_empirical']['lower_fraction'])
        assert value == Fraction(declared['normalizer_empirical']['upper_fraction'])
        assert value < 0
    assert not any(k.endswith('_normalized_empirical') for k in receipt)
    out = {'scope': 'Native central directory, four existing TIFF IFDs, all saved pair labels and empirical total-covariance definitions. No pixel decode or weighted-moment rerun.',
           'central_directory_members': len(names), 'IFD_members_inspected': inspected,
           'record_pairs': len(records),
           'declared_pairing': '(B00001,B00002),(B00003,B00004),...,(B00499,B00500)',
           'normalizer_empirical_exact': str(empirical),
           'ten_block_normalizers_exact': list(map(str, blocks)),
           'all_ten_negative': True, 'normalized_output_keys_absent': True,
           'physical_lag_or_gain_qualification': 'NOT_ACQUIRED; sequence labels and TIFF geometry do not supply timestamps, PSF/calibration, an IID model or an annular experiment.',
           'seconds_after_imports': time.perf_counter() - started}
    (HERE / 'NATIVE_CHECK.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'IFD_members_inspected'}, indent=2))


if __name__ == '__main__':
    main()

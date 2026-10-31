#!/usr/bin/env python3
"""Verify this extracted checkpoint or a supplied ZIP. Standard library only."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile


def safe(name):
    p = PurePosixPath(name)
    return (not p.is_absolute() and '..' not in p.parts and '\\' not in name
            and str(p) == name and not name.endswith('/'))


def verify(read, names):
    assert len(names) == len(set(names)), 'duplicate paths'
    assert all(safe(n) for n in names), 'unsafe member path'
    manifest = json.loads(read('MANIFEST.json'))
    rows = manifest['files']
    assert len(rows) == len({r['path'] for r in rows}), 'duplicate manifest entry'
    expected = {r['path'] for r in rows} | {'MANIFEST.json', 'SHA256SUMS.txt'}
    assert set(names) == expected, ('membership mismatch', set(names)^expected)
    for row in rows:
        data = read(row['path'])
        assert len(data) == row['bytes'], ('byte count', row['path'])
        assert hashlib.sha256(data).hexdigest() == row['sha256'], ('hash', row['path'])
    sums = {}
    for line in read('SHA256SUMS.txt').decode().splitlines():
        digest, name = line.split('  ', 1)
        assert name not in sums, 'duplicate checksum entry'
        sums[name] = digest
    assert set(sums) == set(names)-{'SHA256SUMS.txt'}, 'checksum membership'
    for name, digest in sums.items():
        assert hashlib.sha256(read(name)).hexdigest() == digest, ('checksum', name)
    assert read('FILE_LIST.txt').decode().splitlines() == sorted(names), 'file list'
    print(json.dumps({'verified': True, 'files': len(names),
                      'payload_bytes': sum(len(read(n)) for n in names),
                      'scope': 'Integrity/membership only, not mathematical review.'}, indent=2))


def main():
    if len(sys.argv) == 2:
        with zipfile.ZipFile(sys.argv[1]) as z:
            assert z.testzip() is None, 'CRC error'
            for item in z.infolist():
                assert not stat.S_ISLNK(item.external_attr >> 16), 'symlink member'
            verify(z.read, z.namelist())
    elif len(sys.argv) == 1:
        root = Path(__file__).resolve().parent
        paths = [p for p in root.rglob('*') if p.is_file()]
        assert not any(p.is_symlink() for p in root.rglob('*')), 'symlink'
        verify(lambda n: (root/n).read_bytes(), [p.relative_to(root).as_posix() for p in paths])
    else:
        raise SystemExit('Usage: python3 -B verify_checkpoint.py [checkpoint.zip]')


if __name__ == '__main__':
    main()

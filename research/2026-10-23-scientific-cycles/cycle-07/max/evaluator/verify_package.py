#!/usr/bin/env python3
"""Verify the supplied archive payload; this is not a proof certificate."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    failures = []
    for entry in manifest['files']:
        relative = Path(entry['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe manifest path')
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            failures.append({'path': entry['path'], 'reason': 'missing or unsafe'})
        elif path.stat().st_size != entry['bytes'] or digest(path) != entry['sha256']:
            failures.append({'path': entry['path'], 'reason': 'bytes/hash mismatch'})
    result = {'status': 'FAIL' if failures else 'PASS',
              'checked_payload_files': len(manifest['files']),
              'failures': failures,
              'scope': 'Payload identity only, not mathematical truth, originality, scientific acceptance or amplification.'}
    print(json.dumps(result, indent=2))
    if failures:
        raise SystemExit(1)

if __name__ == '__main__':
    main()

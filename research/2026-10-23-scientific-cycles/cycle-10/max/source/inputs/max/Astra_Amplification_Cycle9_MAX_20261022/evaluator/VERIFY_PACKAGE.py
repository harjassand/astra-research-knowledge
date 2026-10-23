"""Portable payload identity check only. Executes no scientific calculation."""
from pathlib import Path, PurePosixPath
import hashlib
import json

ROOT = Path(__file__).resolve().parent

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    total = 0
    for record in manifest['files']:
        rel = PurePosixPath(record['path'])
        assert not rel.is_absolute() and '..' not in rel.parts, record['path']
        path = ROOT.joinpath(*rel.parts)
        assert path.is_file(), record['path']
        assert path.stat().st_size == record['bytes'], record['path']
        assert digest(path) == record['sha256'], record['path']
        total += record['bytes']
    print(json.dumps({'status':'PASS','checked_files':len(manifest['files']),
                      'checked_bytes':total,
                      'scope':'Payload identity only; no scientific execution or acceptance.'},indent=2))

if __name__ == '__main__':
    main()

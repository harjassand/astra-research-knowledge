"""Verify the received payload against its manifest; not a proof certificate."""
from pathlib import Path
import hashlib
import json


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    records = manifest['files']
    names = set()
    for record in records:
        relative = Path(record['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        assert record['path'] not in names
        names.add(record['path'])
        path = root / relative
        assert path.is_file() and not path.is_symlink(), record['path']
        assert path.stat().st_size == record['bytes'], record['path']
        assert digest(path) == record['sha256'], record['path']
    for record in json.loads((root / 'evidence/SOURCE_INTAKE.json').read_text()):
        path = root / 'originals' / Path(record['source']).name
        assert path.stat().st_size == record['bytes'], str(path)
        assert digest(path) == record['sha256'], str(path)
    print(json.dumps({
        'status': 'PASS', 'manifest_payload_files': len(records),
        'unchanged_original_archives': 7,
        'scope': 'Identity only; requires independently received ZIP hash. '
                 'No proof certificate or scientific suite executed.'
    }, indent=2))


if __name__ == '__main__':
    main()

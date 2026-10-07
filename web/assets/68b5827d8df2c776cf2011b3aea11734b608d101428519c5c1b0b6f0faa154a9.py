"""Verify archive CRCs and every file against its embedded SHA-256 manifest."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile

archive = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('research_evidence.zip')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None, 'CRC failure'
    manifest = json.loads(z.read('MANIFEST.json'))
    expected = {r['path'] for r in manifest['files']} | {'MANIFEST.json'}
    assert len(z.namelist()) == len(expected), 'Duplicate or unexpected members'
    assert set(z.namelist()) == expected, 'Missing or unexpected members'
    for row in manifest['files']:
        data = z.read(row['path'])
        assert len(data) == row['bytes'], row['path']
        assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
print(json.dumps({'archive': str(archive), 'verified_files': len(manifest['files']),
                  'crc': 'pass', 'sha256': 'pass',
                  'scope': 'Byte integrity only; not scientific validation.'}))

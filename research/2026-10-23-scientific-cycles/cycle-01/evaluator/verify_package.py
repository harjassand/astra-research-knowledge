"""Verify transport/source identity, not scientific correctness."""
from pathlib import Path, PurePosixPath
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST.json').read_text())
checked = 0
for rel, expected in manifest['files'].items():
    p = PurePosixPath(rel)
    assert not p.is_absolute() and '..' not in p.parts
    f = root / rel
    assert f.is_file(), rel
    assert f.stat().st_size == expected['bytes'], rel
    assert hashlib.sha256(f.read_bytes()).hexdigest() == expected['sha256'], rel
    checked += 1
identities = json.loads((root / 'SOURCE_IDENTITIES.json').read_text())
for owner, item in identities['owners'].items():
    p = root / 'sources' / item['archive']
    assert p.stat().st_size == item['bytes'], owner
    assert hashlib.sha256(p.read_bytes()).hexdigest() == item['sha256'], owner
r1 = root / 'sources/Astra_B2_R1_OWNER_SOURCE_20261021.zip'
assert r1.stat().st_size == 3663087
assert hashlib.sha256(r1.read_bytes()).hexdigest() == '8b813c9f267e3079225219fb2e857cd3e4c18451f82471e3c5ee72be73136676'
print(json.dumps({'PASS': True, 'files_checked': checked, 'unchanged_owner_archives': 6,
 'original_R1_export': True, 'scope': 'Byte identity and source transport only; not a proof certificate or novelty assessment.'}, indent=2))

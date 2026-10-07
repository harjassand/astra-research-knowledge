from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile

out = Path.cwd() / 'outputs'
now = datetime.now(timezone.utc).isoformat()
compiled = []
for name in ('hard_energy_detection.tex', 'projected_slater_preparation.tex'):
    p = out / name
    compiled.append({'path': name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                     'compiler': 'Codex desktop built-in standalone LaTeX compiler',
                     'status': 'success', 'verified_date_utc': '2026-10-07'})
(out / 'COMPILATION_STATUS.json').write_text(json.dumps({
    'scope': 'Source compiled; this is not a proof certificate or external review.',
    'manuscripts': compiled}, indent=2) + '\n')
files = []
for p in sorted(out.rglob('*')):
    if not p.is_file() or p in (out/'MANIFEST.json', out/'research_checkpoint.zip'):
        continue
    files.append({'path': str(p.relative_to(out)), 'bytes': p.stat().st_size,
                  'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
(out/'MANIFEST.json').write_text(json.dumps({
    'saved_at_utc': now,
    'status': 'Internal research checkpoint; no external correctness or novelty certification.',
    'files': files}, indent=2)+'\n')
archive = out/'research_checkpoint.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(out.rglob('*')):
        if p.is_file() and p != archive:
            z.write(p, p.relative_to(out))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for entry in files:
        data = z.read(entry['path'])
        assert len(data) == entry['bytes']
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
print(json.dumps({'archive': str(archive), 'bytes': archive.stat().st_size,
                  'manifest_files': len(files), 'saved_at_utc': now,
                  'zip_and_all_manifest_hashes_verified': True}, indent=2))

"""Package the completed scientific snapshot without modifying predecessors."""
from pathlib import Path
import hashlib
import json
import zipfile

BRANCH = Path(__file__).resolve().parent
PROJECT = BRANCH.parent.parent
WORKSPACE = PROJECT.parent
PREDECESSOR = WORKSPACE / 'Astra_P1_Equilibrium_Information_and_Entropy_20261029.zip'
PREDECESSOR_SHA = 'f6a4f884b9a78735004424499e09de5a154c17c2056719559b6371635f10c6fa'
OUTPUT = WORKSPACE / 'Astra_P1_Physical_Information_and_Hidden_Memory_20261029.zip'
MANIFEST = BRANCH / 'SNAPSHOT_MANIFEST.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    assert digest(PREDECESSOR) == PREDECESSOR_SHA, 'Predecessor identity changed'
    files = []
    for path in sorted(BRANCH.rglob('*')):
        if not path.is_file() or path == MANIFEST:
            continue
        if '__pycache__' in path.parts or path.suffix == '.pyc':
            continue
        files.append((path, 'research/' + path.relative_to(BRANCH).as_posix()))
    files += [
        (BRANCH / 'HANDOFF.md', 'HANDOFF.md'),
        (BRANCH / 'README.md', 'README.md'),
        (PROJECT / 'README.md', 'project_entrypoints/README.md'),
        (PROJECT / 'CURRENT_SCIENCE_STATE.md', 'project_entrypoints/CURRENT_SCIENCE_STATE.md'),
        (PREDECESSOR, 'predecessor/' + PREDECESSOR.name),
    ]
    manifest = {
        'date': '2026-10-29',
        'title': 'Astra P1: Physical information and hidden memory',
        'scope': 'Mathematical constructions, exact executable controls, sources and scoped internal reviews; no new native acquisition',
        'predecessor_library_file_id': 'libfile_627b517495c88191a4b6d005d8b6ed17',
        'predecessor_sha256': PREDECESSOR_SHA,
        'manifest_self_hash_excluded': True,
        'files': [{'path': name, 'bytes': p.stat().st_size, 'sha256': digest(p)} for p, name in files],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n')
    files.append((MANIFEST, 'SNAPSHOT_MANIFEST.json'))
    with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path, name in files:
            z.write(path, name)
    with zipfile.ZipFile(OUTPUT) as z:
        assert z.testzip() is None
        for entry in manifest['files']:
            assert hashlib.sha256(z.read(entry['path'])).hexdigest() == entry['sha256']
    receipt = {
        'file': str(OUTPUT),
        'bytes': OUTPUT.stat().st_size,
        'entries': len(files),
        'sha256': digest(OUTPUT),
        'predecessor_unchanged': True,
        'all_archived_hashes_verified': True,
    }
    (WORKSPACE / 'astra_physical_information_package_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()

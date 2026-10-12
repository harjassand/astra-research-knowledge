"""Verify this package's bytes and links, not its scientific conclusions."""
from pathlib import Path
import hashlib
import json


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    entries = manifest['files']
    assert len(entries) == len({e['path'] for e in entries}), 'duplicate manifest entry'
    for entry in entries:
        path = (root / entry['path']).resolve()
        assert path.is_relative_to(root) and path.is_file(), entry['path']
        data = path.read_bytes()
        assert len(data) == entry['bytes'], f"size: {entry['path']}"
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], f"hash: {entry['path']}"
        if path.suffix == '.json':
            json.loads(data)
    expected = {e['path'] for e in entries} | {'MANIFEST.json'}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()
              and '__pycache__' not in p.parts}
    assert actual == expected, f"unlisted={actual-expected}; absent={expected-actual}"
    draft = json.loads((root / 'CHECKPOINT_DRAFT.json').read_text())
    prefix = 'research/2026-10-12-foundational-discovery-wave/'
    for ref in draft['evidence_refs']:
        assert ref['path'].startswith(prefix), ref['path']
        path = root / ref['path'][len(prefix):]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == ref['sha256'], ref['id']
    receipts = json.loads((root / 'SPAWN_RECEIPTS.json').read_text())['agents']
    assert sum(a['model'] == 'gpt-6-luna' for a in receipts) == 15
    assert sum(a['model'] == 'gpt-6.1-sol' for a in receipts) == 5
    assert all(a['reasoning_effort'] == 'max' and a['fork_turns'] == 'none' for a in receipts)
    assert all(a.get('acceptance', {}).get('task_name') for a in receipts)
    print(json.dumps({'status': 'PASS', 'files_hashed': len(entries),
                      'accepted_luna_max_launches': 15, 'accepted_sol_max_launches': 5,
                      'scientific_correctness_certified': False,
                      'novelty_certified': False}, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Read-only public-edition integrity check. Never runs scientific code."""
import hashlib
import json
from pathlib import Path
import resource
import sys
import time


def main():
    started = time.perf_counter()
    root = Path(__file__).resolve().parent
    archives = json.loads((root / 'SOURCE_ARCHIVES.json').read_text())
    ids = {item['public_id'] for item in archives}
    assert len(ids) == len(archives), 'duplicate source id'
    owners = {'pro1', 'pro2', 'pro3', 'ultra', 'dots', 'max'}
    for cycle in range(12):
        assert owners <= {x['owner'] for x in archives if x['cycle'] == cycle}, cycle
    expected = set()
    counts = {}
    total_bytes = 0
    for archive in archives:
        binding = root / archive['public_id'] / 'PUBLIC_EXPORT_BINDINGS.json'
        assert hashlib.sha256(binding.read_bytes()).hexdigest() == archive['public_bindings_sha256'], binding
        payload = json.loads(binding.read_text())
        assert payload['source'] == {k: v for k, v in archive.items() if k != 'public_bindings_sha256'}, archive['public_id']
        assert len(payload['members']) == archive['native_member_count']
        seen_members = set()
        for entry in payload['members']:
            assert entry['member'] not in seen_members, entry['member']
            seen_members.add(entry['member'])
            state = entry['disposition']
            counts[state] = counts.get(state, 0) + 1
            if state == 'unpacked_or_linked_source':
                assert entry['source_id'] in ids, entry
                original = next(x for x in archives if x['public_id'] == entry['source_id'])
                assert (entry['sha256'], entry['bytes']) == (original['sha256'], original['bytes'])
            elif state in ('exact_copy', 'public_edition'):
                path = root / entry['public_path']
                assert path.resolve().is_relative_to(root), path
                assert entry['public_path'] not in expected, entry['public_path']
                expected.add(entry['public_path'])
                blob = path.read_bytes()
                assert len(blob) == entry['public_bytes'], path
                assert hashlib.sha256(blob).hexdigest() == entry['public_sha256'], path
                if state == 'exact_copy':
                    assert (entry['bytes'], entry['sha256']) == (entry['public_bytes'], entry['public_sha256'])
                else:
                    assert entry['delivery_only_redactions'], path
                total_bytes += len(blob)
            else:
                assert state == 'omitted' and entry['reason'], entry
    # No unaccounted source payload is silently published alongside the bindings.
    observed = set()
    for archive in archives:
        directory = root / archive['public_id']
        observed.update(p.relative_to(root).as_posix() for p in directory.rglob('*')
                        if p.is_file() and p.name != 'PUBLIC_EXPORT_BINDINGS.json')
    assert observed == expected, sorted(observed ^ expected)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    print(json.dumps({
        'status': 'PASS', 'scope': 'selected publication payload identities and predecessor routing only',
        'source_archives': len(archives), 'dispositions': counts,
        'selected_payload_bytes': total_bytes, 'scientific_calculations_executed': 0,
        'wall_seconds': time.perf_counter() - started,
        'cpu_seconds': usage.ru_utime + usage.ru_stime,
        'peak_rss': usage.ru_maxrss,
        'peak_rss_unit': 'bytes' if sys.platform == 'darwin' else 'KiB',
    }, indent=2))


if __name__ == '__main__':
    main()

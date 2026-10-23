#!/usr/bin/env python3
"""Exact new finite admission check; does not import old atom table/producer."""
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import resource
import time


def main():
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    colors = (1, 2, 3)  # Root color is fixed to 0.
    witnesses = []
    for size in (1, 2):
        for parent in combinations(colors, size):
            P = set(parent)
            for forbidden in (None, *parent):
                for original_flag in (None, 1):
                    admitted = []
                    for perm in permutations(colors):
                        mp = dict(zip(colors, perm))
                        N = {mp[1], mp[2]}
                        F = set() if original_flag is None else {mp[original_flag]}
                        common = P & N
                        if forbidden is not None and forbidden in N:
                            continue
                        if len(common) > 1 or common & F:
                            continue
                        if len(P) == 1 and common:
                            continue
                        admitted.append(dict(permutation=[0, *perm],
                                             child_neighbor_support=sorted(N),
                                             child_far_flags=sorted(F),
                                             common=sorted(common)))
                    assert admitted, (parent, forbidden, original_flag)
                    witnesses.append(dict(parent_neighbor_support=list(parent),
                                          forbidden=forbidden,
                                          original_flag=original_flag,
                                          witness=admitted[0],
                                          admissible_permutations=len(admitted)))
    assert len(witnesses) == 30
    end_wall, end_cpu = time.perf_counter(), time.process_time()
    record = dict(status='PASS', cases=len(witnesses), witnesses=witnesses,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  costs=dict(wall_seconds=end_wall-start_wall,
                             cpu_seconds=end_cpu-start_cpu,
                             peak_process_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
                             scope='Local exact case construction/assertions; excludes JSON serialization and all reasoning, reading, authoring and integration.'),
                  mathematical_scope='Every one-root profile with distinct neighbors and <=1 flag, up to root-fixing permutations; parent support size1/2; zero or one forbidden parent channel. All-depth composition proved separately.')
    out=Path(__file__).with_name('CHANNEL_TRANSITION_RESULT.json')
    out.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ('status','cases','costs','source_sha256')}))


if __name__ == '__main__':
    main()

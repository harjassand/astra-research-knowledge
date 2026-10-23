"""Prespecified common search for a bounded representation meta experiment.

No previous closure state or family table is read. Original scientific
backends are preserved and imported from source/src in this package.
"""
import argparse
from collections import defaultdict, Counter
from functools import lru_cache
import hashlib
import heapq
import importlib
import json
import os
from pathlib import Path
import resource
import signal
import sys
import time

PROCESS_START_WALL = time.perf_counter()
PROCESS_START_CPU = time.process_time()


class BudgetStop(Exception):
    pass


def cpu_signal(signum, frame):
    raise BudgetStop('os_cpu_soft_limit')


def configure(arm, source):
    sys.path.insert(0, str(source))
    if arm == 'A_counts_flags':
        backend = importlib.import_module('monotone_ports')
        aliases = [importlib.import_module('active_ports'), backend]
        def base(s):
            return s[0], s[1], s[2], s[4]
        def bits(s):
            return s[3] | (s[5] << 4)
    else:
        backend = importlib.import_module('hazard_ports')
        aliases = [backend]
        if arm == 'B_occupancy_flags':
            def base(s):
                return s[0], s[1], s[2], s[3], s[5], s[6]
            def bits(s):
                return s[4] | (s[7] << 4)
        else:
            def base(s):
                return s[0], s[1], s[2], s[5]
            def bits(s):
                return s[3] | (s[4] << 4) | (s[6] << 8) | (s[7] << 12)

    # Point-profile cache policy is identical; original wrappers start cold.
    backend.canonical.cache_clear()
    backend.orbit.cache_clear()

    @lru_cache(512)
    def expanded(states):
        return tuple(sorted({v for s in states for v in backend.orbit(s)}))

    @lru_cache(128)
    def groups(states):
        result = defaultdict(list)
        for s in expanded(states):
            result[base(s)].append(s)
        return dict(result)

    def below(s, t):
        return base(s) == base(t) and bits(s) & bits(t) == bits(s)

    @lru_cache(512)
    def covers(realizers, targets):
        grouped = groups(realizers)
        return all(any(below(t, s) for t in grouped.get(base(s), ()))
                   for s in targets)

    def reduce(states):
        grouped = defaultdict(set)
        for s in sorted(states):
            for t in backend.orbit(s):
                grouped[base(t)].add(t)
        out = set()
        for ss in grouped.values():
            masks = []
            for s in sorted(ss, key=lambda x: (bits(x).bit_count(), bits(x), x)):
                mask = bits(s)
                if not any(previous & mask == previous for previous in masks):
                    masks.append(mask)
                    out.add(backend.canonical(s))
        return frozenset(out)

    # Changing only the imported alias would leave active_ports.apply using
    # its own unbounded cache. Update both defining and importing namespaces.
    for module in aliases:
        module.expanded = expanded
        module.groups = groups
        module.covers = covers
        module.reduce = reduce
        module.base = base
        module.below = below
    return backend, {'expanded': expanded, 'groups': groups, 'covers': covers,
                     'canonical': backend.canonical, 'orbit': backend.orbit}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--arm', choices=('A_counts_flags', 'B_occupancy_flags',
                                         'C_occupancy_support_flags'), required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2))
    resource.setrlimit(resource.RLIMIT_CPU, (238, 240))
    signal.signal(signal.SIGXCPU, cpu_signal)
    reserve = bytearray(8 * 1024**2)
    backend, caches = configure(args.arm, root / 'source/src')
    setup_wall = time.perf_counter() - PROCESS_START_WALL
    setup_cpu = time.process_time() - PROCESS_START_CPU
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    records, history, heap, tested = [], [], [], []
    active, queued = set(), set()
    checks = 0
    kinds = Counter()
    last_progress = start_wall

    def queue(key):
        if key in queued:
            return
        queued.add(key)
        kind = key[0]
        left = records[key[1]]
        right = records[key[2]] if len(key) == 3 else None
        if not backend.admissible(kind, left['degree'], None if right is None
                                  else right['degree']):
            return
        cost = len(left['states']) * (1 if right is None else len(right['states']))
        heapq.heappush(heap, (cost, len(key), key))

    def add(states, degree, expression):
        old = [i for i in sorted(active) if records[i]['degree'] == degree]
        if any(backend.covers(states, records[i]['states']) for i in old):
            return
        removed = [i for i in old if backend.covers(records[i]['states'], states)]
        active.difference_update(removed)
        idx = len(records)
        records.append({'states': states, 'degree': degree, 'expression': expression})
        active.add(idx)
        history.append({'id': idx, 'degree': degree, 'states': len(states),
                        'removed': removed, 'cpu_seconds': time.process_time()-start_cpu,
                        'wall_seconds': time.perf_counter()-start_wall})
        for kind in ('L', 'R'):
            queue((kind, idx))
        for j in sorted(active):
            queue(('S', idx, j))
            queue(('S', j, idx))
            queue(('P', min(idx, j), max(idx, j)))

    reason, failure = 'closed', None
    try:
        add(backend.reduce(backend.path2()), (1, 1), {'kind': 'path', 'length': 2})
        while heap:
            total_cpu = time.process_time()
            total_wall = time.perf_counter() - PROCESS_START_WALL
            if len(records) >= 2500:
                reason = 'family_record_limit'
                break
            if total_cpu >= 230:
                reason = 'cpu_save_threshold'
                break
            if total_wall >= 290:
                reason = 'wall_save_threshold'
                break
            _, _, key = heapq.heappop(heap)
            if any(i not in active for i in key[1:]):
                continue
            kind = key[0]
            left = records[key[1]]
            right = records[key[2]] if len(key) == 3 else None
            states = backend.reduce(backend.apply(
                kind, left['states'], None if right is None else right['states']))
            tested.append(key)
            checks += 1
            kinds[kind] += 1
            degree = backend.output_degree(kind, left['degree'], None if right is None
                                           else right['degree'])
            if not states:
                reason = 'empty_simulation_family'
                failure = {'kind': kind, 'children': list(key[1:]), 'degree': degree}
                break
            add(states, degree, {'kind': kind, 'children': list(key[1:])})
            if time.perf_counter() - last_progress >= 10:
                print(json.dumps({'arm': args.arm, 'active': len(active),
                                  'discovered': len(records), 'checks': checks,
                                  'cpu_seconds': time.process_time()-start_cpu}), flush=True)
                last_progress = time.perf_counter()
    except (MemoryError, BudgetStop) as exc:
        reserve = None
        reason = type(exc).__name__
        failure = str(exc)
    reserve = None
    body_wall = time.perf_counter() - start_wall
    body_cpu = time.process_time() - start_cpu

    tested_set = set(tested)
    required, missing = 0, []
    for i in sorted(active):
        keys = [('L', i), ('R', i)]
        for j in sorted(active):
            keys.append(('S', i, j))
            if i <= j:
                keys.append(('P', i, j))
        for key in keys:
            right = records[key[2]] if len(key) == 3 else None
            if backend.admissible(key[0], records[i]['degree'], None if right is None
                                  else right['degree']):
                required += 1
                if key not in tested_set:
                    missing.append(key)
    if reason == 'closed':
        assert not missing, 'Closed worklist omitted a final-basis obligation.'
    result = {
        'schema': 'astra-cycle9-representation-experiment/v1',
        'arm': args.arm, 'reason': reason, 'failure': failure,
        'initial_condition': 'cold path2; no checkpoint/final basis loaded',
        'python_hash_seed': os.environ.get('PYTHONHASHSEED'),
        'active_families': len(active), 'discovered_families': len(records),
        'checked_transitions': checks, 'transition_kinds': dict(kinds),
        'remaining_heap': len(heap), 'queued_keys': len(queued),
        'final_basis_required_keys': required, 'final_basis_missing_keys': missing,
        'basis_ids': sorted(active), 'records': [
            {'id': i, 'degree': r['degree'],
             'states': [backend.serialize(s) for s in sorted(r['states'])],
             'expression': r['expression']} for i, r in enumerate(records)],
        'history': history, 'tested_transitions': tested,
        'cache_info': {name: fn.cache_info()._asdict() for name, fn in caches.items()},
        'limits': {'address_space_bytes': 512*1024**2, 'total_cpu_hard_seconds': 240,
                   'loop_cpu_save_threshold_seconds': 230, 'wall_hard_seconds': 300,
                   'loop_wall_save_threshold_seconds': 290, 'family_records': 2500},
        'cost': {'setup_wall_seconds': setup_wall, 'setup_cpu_seconds': setup_cpu,
                 'body_wall_seconds': body_wall, 'body_cpu_seconds': body_cpu},
        'common_driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Closure-search computational experiment, not a new scientific '
                 'theorem, independent certificate, total discovery cost or amplification.'
    }
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    # Stream one serialization. Whole-process wait4 records its CPU and RSS;
    # do not retain a redundant full JSON string or serialize twice.
    with output.open('w') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: result[key] for key in ('arm', 'reason', 'active_families',
          'discovered_families', 'checked_transitions', 'cost')}, indent=2), flush=True)


if __name__ == '__main__':
    main()

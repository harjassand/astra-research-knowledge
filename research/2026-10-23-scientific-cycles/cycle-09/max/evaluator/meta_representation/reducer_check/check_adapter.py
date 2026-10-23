"""Independent focused validation of the NEW representation adapter.

No closure worklist, saved family table, certificate, or old suite is used.
Each condition is run in its own process. Fixed two-layer grammar fixtures
exercise real profiles; this is not universal exhaustive correctness.
"""
from pathlib import Path
from itertools import permutations
import argparse
import hashlib
import importlib.util
import json
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source/src'
sys.path.insert(0, str(ROOT))
from common_search import configure


def load_reference(arm):
    name = 'monotone_ports' if arm == 'A_counts_flags' else 'hazard_ports'
    # A distinct module owns the original function globals. Its imported
    # pointwise active-port functions are unchanged by the common adapter.
    spec = importlib.util.spec_from_file_location('independent_' + name,
                                                 SOURCE / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def explicit_key_and_bits(arm, state):
    if arm == 'A_counts_flags':
        a, b, nl, fl, nr, fr = state
        return (a, b, nl, nr), fl | (fr << 4)
    a, b, dl, nl, fl, dr, nr, fr = state
    if arm == 'B_occupancy_flags':
        return (a, b, dl, nl, dr, nr), fl | (fr << 4)
    return (a, b, dl, dr), nl | (fl << 4) | (nr << 8) | (fr << 12)


def brute_relation(arm, first, second):
    key1, bits1 = explicit_key_and_bits(arm, first)
    key2, bits2 = explicit_key_and_bits(arm, second)
    return key1 == key2 and (bits1 & bits2) == bits1


def brute_expansion(reference, states):
    return set(reference.transform(s, p) for s in states
               for p in permutations(range(4)))


def brute_reduce(arm, reference, states):
    expanded = brute_expansion(reference, states)
    return frozenset(reference.canonical(s) for s in expanded
                     if not any(t != s and brute_relation(arm, t, s)
                                for t in expanded))


def brute_covers(arm, reference, realizers, targets):
    expanded = brute_expansion(reference, realizers)
    return all(any(brute_relation(arm, t, s) for t in expanded)
               for s in targets)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--arm', required=True)
    args = parser.parse_args()
    start, cpu = time.perf_counter(), time.process_time()
    backend, caches = configure(args.arm, SOURCE)
    reference = load_reference(args.arm)
    cases = []
    assertions = 0

    def validate(name, raw, degree):
        nonlocal assertions
        raw = frozenset(raw)
        actual = backend.reduce(raw)
        expected = brute_reduce(args.arm, reference, raw)
        assert actual == expected, ('brute_reduce', name)
        assertions += 1
        if args.arm != 'B_occupancy_flags':
            assert actual == reference.reduce(raw), ('original_reduce', name)
            assertions += 1
        assert actual == backend.reduce(reversed(sorted(raw))), ('input_order', name)
        assert backend.reduce(actual) == actual, ('idempotence', name)
        assertions += 2
        for p in permutations(range(4)):
            recolored = frozenset(reference.transform(s, p) for s in raw)
            assert backend.reduce(recolored) == actual, ('global_recoloring', name, p)
            assertions += 1
        assert all(backend.degrees(s) == degree for s in actual), ('degree', name)
        assertions += 1
        cases.append({'name': name, 'raw_profiles': len(raw),
                      'reduced_profiles': len(actual), 'degree': degree,
                      'states': actual})
        return actual

    leaf = validate('P2', backend.path2(), (1, 1))
    seeds = [('P2', leaf, (1, 1))]
    for kind in ('L', 'R', 'S', 'P'):
        raw = backend.apply(kind, leaf, None if kind in ('L', 'R') else leaf)
        degree = backend.output_degree(kind, (1, 1), None if kind in ('L', 'R') else (1, 1))
        states = validate(kind + '(P2)', raw, degree)
        seeds.append((kind + '(P2)', states, degree))

    # Exactly two fixture layers, independent of any result or subsumption.
    for name, states, degree in seeds:
        for kind in ('L', 'R'):
            if backend.admissible(kind, degree):
                validate(kind + '(' + name + ')', backend.apply(kind, states),
                         backend.output_degree(kind, degree))
    for ln, ls, ld in seeds:
        for rn, rs, rd in seeds:
            for kind in ('S', 'P'):
                if backend.admissible(kind, ld, rd):
                    validate(kind + '(' + ln + ',' + rn + ')', backend.apply(kind, ls, rs),
                             backend.output_degree(kind, ld, rd))

    cover_checks = 0
    # All pairs of this fixed small corpus, restricted to matching actual
    # degrees as used by the search. Distinct fixtures may share a family.
    for left in cases:
        for right in cases:
            if left['degree'] != right['degree']:
                continue
            actual = backend.covers(left['states'], right['states'])
            expected = brute_covers(args.arm, reference, left['states'], right['states'])
            assert actual == expected, ('coverage', left['name'], right['name'])
            if args.arm != 'B_occupancy_flags':
                assert actual == reference.covers(left['states'], right['states'])
                assertions += 1
            cover_checks += 1
            assertions += 1

    saturated = sum(any(-1 in s[:2] for s in c['states']) for c in cases)
    assert saturated > 0
    assertions += 1
    report = {
        'status': 'PASS', 'arm': args.arm, 'fixture_families': len(cases),
        'coverage_pairs': cover_checks, 'assertions': assertions,
        'saturated_port_families': saturated,
        'fixtures': [{k: v for k, v in c.items() if k != 'states'} for c in cases],
        'driver_sha256_at_check': hashlib.sha256((ROOT / 'common_search.py').read_bytes()).hexdigest(),
        'check_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'wall_seconds': time.perf_counter() - start,
        'cpu_seconds': time.process_time() - cpu,
        'peak_rss_bytes_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        'scope': 'Bounded adapter validation on real cold grammar states. '
                 'No closure search or old suite. Not a complete proof or certificate.',
    }
    output = Path(__file__).with_name(args.arm + '.json')
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['status', 'arm', 'fixture_families',
          'coverage_pairs', 'assertions', 'saturated_port_families', 'wall_seconds',
          'cpu_seconds', 'peak_rss_bytes_linux']}))


if __name__ == '__main__':
    main()

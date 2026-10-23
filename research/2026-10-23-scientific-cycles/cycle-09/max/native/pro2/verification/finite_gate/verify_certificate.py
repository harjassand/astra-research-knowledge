"""Independent literal gate for the Cycle8 loaded-port star-four certificate.

No producer imports. Port records use Python sets, and transitions implement
the independently proved occupancy rules directly. This checks a closed
sufficient-family proof, not a search history or solver success flag.
"""
from pathlib import Path
from itertools import permutations
from collections import Counter
import argparse
import hashlib
import json
import resource
import time

PALETTE = frozenset(range(4))
COLOR_PERMUTATIONS = tuple(permutations(range(4)))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def decode_mask(value):
    need(type(value) is int and 0 <= value < 16, 'bad color mask')
    return frozenset(color for color in PALETTE if value & (1 << color))


def port(color, degree, neighbors, flags):
    need(type(degree) is int and 1 <= degree <= 4, 'bad actual degree')
    if degree == 4:
        need(color == -1 and not neighbors and not flags,
             'saturated marker retains unsupported constraints')
        return (-1, 4, frozenset(), frozenset())
    need(type(color) is int and color in PALETTE, 'bad visible color')
    need(color not in neighbors, 'improper port support')
    need(1 <= len(neighbors) <= degree, 'support incompatible with degree')
    need(flags <= neighbors, 'flag without corresponding neighbor')
    need(degree == len(neighbors) or flags != neighbors,
         'no unflagged color can carry excess multiplicity')
    return (color, degree, neighbors, flags)


def parse_state(flat):
    need(isinstance(flat, list) and len(flat) == 8, 'state must have eight entries')
    a, b, d, n, f, e, m, g = flat
    return (port(a, d, decode_mask(n), decode_mask(f)),
            port(b, e, decode_mask(m), decode_mask(g)))


def relabel(state, permutation):
    result = []
    for color, degree, neighbors, flags in state:
        if degree == 4:
            result.append((-1, 4, frozenset(), frozenset()))
        else:
            result.append((permutation[color], degree,
                           frozenset(permutation[c] for c in neighbors),
                           frozenset(permutation[c] for c in flags)))
    return tuple(result)


def orbit(states):
    return frozenset(relabel(state, permutation)
                     for state in states for permutation in COLOR_PERMUTATIONS)


def project(p):
    return (-1, 4, frozenset(), frozenset()) if p[1] == 4 else p


def merge(left, right):
    a, d, n, f = left
    b, e, m, g = right
    need(d < 4 and e < 4, 'cannot use saturated port in a join')
    need(a == b, 'joined terminal colors differ')
    need(d + e <= 4, 'joined actual degree exceeds four')
    need(not (n & m & (f | g)), 'new repeated-color bad edge')
    # Check first, project only afterwards.
    return project((a, d + e, n | m, f | g))


def operation(kind, children, new_color=None):
    if kind == 'S':
        need(len(children) == 2, 'series arity')
        left, right = children
        merge(left[1], right[0])
        return (left[0], right[1])
    if kind == 'P':
        need(len(children) == 2, 'parallel arity')
        left, right = children
        return (merge(left[0], right[0]), merge(left[1], right[1]))
    need(kind in ('L', 'R') and len(children) == 1, 'unknown operation or arity')
    need(type(new_color) is int and new_color in PALETTE, 'extension color')
    child = children[0]
    index = 0 if kind == 'L' else 1
    old = child[index]
    color, degree, neighbors, flags = old
    need(degree <= 3, 'extension of saturated terminal')
    need(new_color != color, 'improper new leaf edge')
    need(new_color not in flags, 'extension creates bad edge')
    new = (new_color, 1, frozenset((color,)),
           frozenset((color,)) if new_color in neighbors else frozenset())
    return (new, child[1]) if index == 0 else (child[0], new)


def smaller(actual, target):
    for p, q in zip(actual, target):
        if p[:2] != q[:2] or not p[2] <= q[2] or not p[3] <= q[3]:
            return False
    return True


def path_two_state(colors):
    need(isinstance(colors, list) and len(colors) == 3, 'path-two colors')
    need(all(type(c) is int and c in PALETTE for c in colors), 'leaf palette')
    adjacency = ((1,), (0, 2), (1,))
    need(colors[0] != colors[1] and colors[1] != colors[2], 'improper leaf')
    output = []
    for v in (0, 2):
        counts = Counter(colors[u] for u in adjacency[v])
        flagged = set()
        for u in adjacency[v]:
            if any(w != v and colors[w] == colors[v] for w in adjacency[u]):
                flagged.add(colors[u])
        output.append((colors[v], len(adjacency[v]), frozenset(counts),
                       frozenset(flagged)))
    return tuple(output)


def allowed(kind, degrees):
    if kind == 'L':
        return len(degrees) == 1 and degrees[0][0] <= 3
    if kind == 'R':
        return len(degrees) == 1 and degrees[0][1] <= 3
    if kind == 'S':
        return len(degrees) == 2 and degrees[0][1] + degrees[1][0] <= 4
    if kind == 'P':
        return (len(degrees) == 2
                and degrees[0][0] + degrees[1][0] <= 4
                and degrees[0][1] + degrees[1][1] <= 4)
    return False


def parent_degree(kind, degrees):
    if kind == 'L':
        return (1, degrees[0][1])
    if kind == 'R':
        return (degrees[0][0], 1)
    if kind == 'S':
        return (degrees[0][0], degrees[1][1])
    return tuple(degrees[0][i] + degrees[1][i] for i in range(2))


def check(path):
    start, cpu = time.perf_counter(), time.process_time()
    raw = Path(path).read_bytes()
    certificate = json.loads(raw)
    need(certificate['schema'] == 'astra-loaded-star-four/v1', 'certificate schema')
    families, degrees, all_orbits = {}, {}, {}
    for family in certificate['families']:
        name = family['id']
        need(type(name) is int and name not in families, 'duplicate/noninteger family')
        degree = tuple(family['degree'])
        need(len(degree) == 2 and all(type(d) is int and 1 <= d <= 4 for d in degree),
             'family load pair')
        states = tuple(parse_state(target) for target in family['targets'])
        need(bool(states), 'empty existence family')
        need(len(set(states)) == len(states), 'duplicate family target')
        need(all(tuple(p[1] for p in state) == degree for state in states),
             'inhomogeneous family degree')
        families[name], degrees[name], all_orbits[name] = states, degree, orbit(states)
    need(bool(families), 'no families')

    # Independently enumerate all actual colorings of the three-vertex path.
    leaf_states = frozenset(path_two_state([a, c, b])
                            for a in PALETTE for c in PALETTE for b in PALETTE
                            if a != c and c != b)
    need(len(leaf_states) == 36, 'unexpected direct leaf enumeration')
    leaf = certificate['leaf']
    leaf_name = leaf['family']
    need(leaf_name in families and degrees[leaf_name] == (1, 1), 'leaf family')
    seen = set()
    for witness in leaf['witnesses']:
        target = witness['target']
        need(type(target) is int and 0 <= target < len(families[leaf_name]), 'leaf target index')
        need(target not in seen, 'duplicate leaf target')
        seen.add(target)
        actual = path_two_state(witness['colors'])
        need(actual in leaf_states, 'leaf witness not actually enumerated')
        need(smaller(actual, families[leaf_name][target]), 'leaf does not realize upper profile')
    need(seen == set(range(len(families[leaf_name]))), 'missing leaf target witness')

    names = sorted(families)
    expected = set()
    for i in names:
        for kind in ('L', 'R'):
            if allowed(kind, (degrees[i],)):
                expected.add((kind, i))
        for j in names:
            if allowed('S', (degrees[i], degrees[j])):
                expected.add(('S', i, j))
            if i <= j and allowed('P', (degrees[i], degrees[j])):
                expected.add(('P', i, j))

    seen_cases = set()
    witness_count = 0
    kind_counts = Counter()
    for row in certificate['transitions']:
        kind, children = row['kind'], tuple(row['children'])
        key = (kind,) + children
        need(key in expected, 'inadmissible or noncanonical family case: ' + str(key))
        need(key not in seen_cases, 'duplicate family case: ' + str(key))
        seen_cases.add(key)
        kind_counts[kind] += 1
        child_degrees = tuple(degrees[i] for i in children)
        parent = row['parent']
        need(parent in families, 'unknown parent family')
        need(degrees[parent] == parent_degree(kind, child_degrees), 'wrong parent load')
        targets_seen = set()
        for witness in row['witnesses']:
            target_index = witness['target']
            need(type(target_index) is int and 0 <= target_index < len(families[parent]),
                 'parent target index')
            need(target_index not in targets_seen, 'duplicate parent target')
            targets_seen.add(target_index)
            child_states = tuple(parse_state(v) for v in witness['child_signatures'])
            need(len(child_states) == len(children), 'child witness arity')
            for name, child_state in zip(children, child_states):
                need(child_state in all_orbits[name], 'child witness outside family global orbit')
            if kind in ('L', 'R'):
                need('new_color' in witness, 'missing new terminal color')
            else:
                need('new_color' not in witness, 'spurious new terminal color')
            output = operation(kind, child_states, witness.get('new_color'))
            need(smaller(output, families[parent][target_index]),
                 'output not below parent target under literal shared labels: ' + str(key))
            witness_count += 1
        need(targets_seen == set(range(len(families[parent]))),
             'missing parent target in case: ' + str(key))
    need(seen_cases == expected, 'missing admitted cases: ' + str(expected - seen_cases))
    return {
        'schema': 'astra-cycle8-independent-finite-gate/v1',
        'status': 'PASS',
        'input': {'filename': Path(path).name, 'bytes': len(raw),
                  'sha256': hashlib.sha256(raw).hexdigest()},
        'families': len(families),
        'canonical_family_targets': sum(map(len, families.values())),
        'actual_labeled_path2_states': len(leaf_states),
        'leaf_witnesses': len(seen),
        'admitted_transition_cases': len(expected),
        'case_counts_by_kind': dict(sorted(kind_counts.items())),
        'transition_witnesses': witness_count,
        'producer_imports': False,
        'semantics': 'Exact visible colors and actual degrees; realized support/flag subsets; SAT4 existential color.',
        'cost': {'body_wall_seconds': time.perf_counter() - start,
                 'body_cpu_seconds': time.process_time() - cpu,
                 'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
                 'scope': 'Includes certificate bytes read/parse, all literal checks, and input hash; excludes process startup and final receipt serialization.'}
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = check(args.certificate)
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

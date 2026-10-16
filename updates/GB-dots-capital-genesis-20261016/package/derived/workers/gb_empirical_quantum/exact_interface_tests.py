#!/usr/bin/env python3
"""Exact source-interface tests. No r50 shots, labels, predictions or fitting.

Reads only ideal circuit annotations, their supplied maps, and r13 preparation
sweep bytes. Writes results in this worker directory. Python standard library.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter, defaultdict, deque
import hashlib, json, re

OUT = Path(__file__).resolve().parent
W = Path('/Users/harjas/Downloads/Dots/willow_empirical_evaluator_2026-10-15')
READS = {}

def read(p):
    b = p.read_bytes()
    READS[str(p)] = {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
    return b

def mask(indices):
    a = 0
    for i in indices:
        a ^= 1 << i
    return a

def indices(a):
    return [i for i in range(a.bit_length()) if (a >> i) & 1]

def basis(rows):
    out = {}
    for a in rows:
        while a:
            k = a.bit_length() - 1
            if k not in out:
                out[k] = a
                break
            a ^= out[k]
    return out

def remainder(a, b):
    for k in sorted(b, reverse=True):
        if (a >> k) & 1:
            a ^= b[k]
    return a

def rank(rows):
    return len(basis(rows))

def span(rows):
    out = [0]
    for a in basis(rows).values():
        out += [v ^ a for v in out]
    return out

def nullspace(rows, n):
    b = basis(rows)
    out = []
    for f in range(n):
        if f in b:
            continue
        a = 1 << f
        for k in sorted(b):
            if (b[k] & a).bit_count() % 2:
                a ^= 1 << k
        assert all((r & a).bit_count() % 2 == 0 for r in rows)
        out.append(a)
    assert len(out) == n - len(b)
    return out

def parse_annotations(p):
    qubits, ds, obs = [], [], []
    for line in read(p).decode().splitlines():
        op = line.split()[0]
        if op == 'M':
            qubits += list(map(int, line.split()[1:]))
        elif op.startswith('DETECTOR') or op.startswith('OBSERVABLE_INCLUDE'):
            js = [len(qubits) + int(i) for i in re.findall(r'rec\[(-?\d+)\]', line)]
            assert min(js) >= 0 and max(js) < len(qubits)
            (ds if op.startswith('DETECTOR') else obs).append(mask(js))
    return qubits, ds, obs

features = {}
for rounds in (13, 50):
    raw = W / 'measured_syndrome_acquisition/data/google_105Q_surface_code_d3_d5_d7/d5_at_q8_7/X' / f'r{rounds}'
    qubits, ds, obs = parse_annotations(raw / 'circuit_ideal.stim')
    supplied = json.loads(read(W / f'measured_syndrome_audit/r{rounds}_independent_map.json'))
    assert qubits == supplied['measurement_qubits']
    assert ds == [mask(r['measurement_indices']) for r in supplied['detectors']]
    assert obs == [mask(r['measurement_indices']) for r in supplied['observables']]
    assert len(obs) == 1
    n, start, target = len(qubits), 24 * rounds, obs[0]
    assert n == start + 25 and len(set(qubits[start:])) == 25
    terminal_mask = ((1 << 25) - 1) << start
    terminal_rows = [(r & terminal_mask) >> start for r in ds if r & terminal_mask]
    assert len(terminal_rows) == 12 and rank(terminal_rows) == 12
    terminal_target = target >> start
    assert target == terminal_target << start
    safe = [1 << i for i in range(start)] + [r << start for r in terminal_rows]
    initial_and_detectors = ds + [1 << i for i in range(24)]
    assert rank(safe) == rank(initial_and_detectors) == rank(safe + initial_and_detectors)
    assert rank(safe + [target]) == rank(safe) + 1
    # A linear label lies in span(H, acquired raw terminal bits) exactly when
    # some member of label + rowspan(H) is supported on those acquired bits.
    representatives = [terminal_target ^ v for v in span(terminal_rows)]
    minimal = min(r.bit_count() for r in representatives)
    leaking = sorted((r for r in representatives if r.bit_count() == minimal), key=indices)
    assert len(representatives) == 4096 and minimal == 5
    # Enumerate every syndrome-invisible terminal translation, then demand an
    # observable flip. This proves failure of EVERY deterministic estimator of
    # the safe features on the unrestricted binary-record domain, not only XORs.
    invisible = span(nullspace(terminal_rows, 25))
    opposite = [z for z in invisible if (terminal_target & z).bit_count() % 2]
    assert len(invisible) == 8192 and len(opposite) == 4096
    wt = min(z.bit_count() for z in opposite)
    witnesses = sorted((z for z in opposite if z.bit_count() == wt), key=indices)
    z = witnesses[0] << start
    assert wt == 5 and all((r & z).bit_count() % 2 == 0 for r in safe + ds)
    assert (target & z).bit_count() % 2 == 1
    # The five target bits alone give the label (with known sweep/offset).
    leaking_set = [1 << (start + i) for i in indices(leaking[0])]
    assert remainder(target, basis(safe + leaking_set)) == 0
    for j in range(5):
        assert remainder(target, basis(safe + leaking_set[:j] + leaking_set[j+1:])) != 0
    features[str(rounds)] = {
        'measurements': n, 'ancilla_measurements': start, 'detectors': len(ds),
        'detector_rank': rank(ds), 'terminal_stabilizer_rank': rank(terminal_rows),
        'safe_feature_rank': rank(safe), 'safe_raw_nullity': n-rank(safe),
        'target_outside_safe_span': True,
        'same_span_as_detectors_plus_complete_initial_frame': True,
        'terminal_target_indices': indices(terminal_target),
        'minimum_extra_terminal_raw_bits_for_exact_target_leakage': minimal,
        'minimum_leaking_subsets_count': len(leaking),
        'minimum_leaking_subsets_terminal_indices': [indices(r) for r in leaking],
        'minimum_translation_witness_weight': wt,
        'minimum_translation_witness_terminal_indices': indices(witnesses[0]),
        'minimum_translation_witness_measurement_indices': indices(z),
        'minimum_translation_witness_qubits': [qubits[i] for i in indices(z)],
        'all_syndrome_invisible_target_flipping_translations_count': len(opposite),
        'minimal_leaking_set_and_its_single_deletions_checked': True,
        'scope': 'Exact affine interface on arbitrary binary records at fixed sweep. No probability, empirical mutual information, physical trajectory support, or decoding advantage inferred.'
    }

# Prepare an exact acquisition design, using calibration sweep input only.
p = W / 'measured_syndrome_acquisition/data/google_105Q_surface_code_d3_d5_d7/d5_at_q8_7/X/r13/sweep_bits.b8'
b = read(p)
assert len(b) == 50000 * 4
rows = [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]
assert all(s >> 25 == 0 for s in rows)
counts = Counter(rows)
configs = list(counts)
assert len(configs) == 10 and set(counts.values()) == {5000}
supplied = json.loads(read(W / 'calibration_state_response/control_design_audit.json'))
assert configs == [mask(r['one_indices']) for r in supplied['configurations']]
assert rank(configs) == rank([(s << 1) | 1 for s in configs]) == 6
original = mask([22, 23])
sig = lambda a: tuple((a & s).bit_count() % 2 for s in configs)
aliases = [mask(p) for k in range(3) for p in combinations(range(25), k) if sig(mask(p)) == sig(original)]
assert len(aliases) == 11 and all(a.bit_count() == 2 for a in aliases)
assert set(aliases) == {original} | {mask(a['indices']) for a in supplied['distinct_minimum_weight_aliases']}

# Encode the 11 edges of a forest with distinct four-bit edge signatures.
# Vertex codes give explicit four additional prepared sweep strings.
graph = defaultdict(list)
for edgecode, a in enumerate(aliases, 1):
    u, v = indices(a)
    graph[u].append((v, edgecode))
    graph[v].append((u, edgecode))
codes = {}
for root in sorted(graph):
    if root in codes:
        continue
    codes[root] = 0
    q = deque([root])
    while q:
        u = q.popleft()
        for v, c in graph[u]:
            if v in codes:
                assert codes[v] == codes[u] ^ c
            else:
                codes[v] = codes[u] ^ c
                q.append(v)
new_masks = [mask(v for v, c in codes.items() if (c >> j) & 1) for j in range(4)]
new_patterns = [configs[0] ^ r for r in new_masks]
assert len(set(new_patterns)) == 4 and not set(new_patterns) & set(configs)
signatures = [tuple((a & s).bit_count() % 2 for s in new_patterns) for a in aliases]
assert len(set(signatures)) == 11
assert 2**3 < len(aliases) <= 2**4
assert rank(configs + new_patterns) == 10

def complete_design(affine=False):
    def lift(a):
        return (a << 1) | 1 if affine else a
    accepted, current = [], [lift(s) for s in configs]
    for a in [0] + [1 << i for i in range(25)]:
        if rank(current + [lift(a)]) > rank(current):
            current.append(lift(a))
            accepted.append(a)
    assert rank(current) == (26 if affine else 25)
    assert len(accepted) == (20 if affine else 19)
    return {'new_pattern_count': len(accepted), 'new_patterns_one_indices': [indices(s) for s in accepted], 'resulting_rank': rank(current)}

design = {
    'read_only_r13_sweep_records': 50000, 'distinct_preparations': 10,
    'linear_rank': 6, 'affine_rank': 6,
    'all_linear_masks_per_current_equivalence_class': 2**19,
    'all_affine_masks_per_current_equivalence_class': 2**20,
    'minimum_weight_original_and_aliases': [indices(a) for a in aliases],
    'minimal_patterns_to_distinguish_these_11_weight_two_candidates': 4,
    'four_preparation_contrasts': [indices(a) for a in new_masks],
    'four_explicit_new_sweep_patterns_one_indices': [indices(a) for a in new_patterns],
    'candidate_signatures_on_four_new_patterns': signatures,
    'rank_after_four_new_patterns': 10,
    'linear_aliases_remaining_after_four_patterns': 2**15,
    'rank_complete_linear_design': complete_design(False),
    'rank_complete_affine_design': complete_design(True),
    'minimal_complement_pairs_for_full_linear_rank_if_pairing_retained': 19,
    'minimal_complement_pairs_for_full_affine_rank_if_pairing_retained': 20,
    'scope': 'Covariate algebra and proposed unexecuted preparations only. Four-pattern optimality holds only for the listed eleven weight-two candidates. No response model, intervention, significance, stationarity or causal effect inferred.'
}
result = {'status': 'PASS', 'new_reserved_shot_analyses': 0, 'new_outcome_tests': 0,
          'experimental_record_reads': ['r13/sweep_bits.b8 only'],
          'features': features, 'control_design': design, 'read_manifest': READS}
(OUT / 'exact_interface_results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'feature_ranks': {r: a['safe_feature_rank'] for r,a in features.items()},
                  'minimum_leak_bits': {r: a['minimum_extra_terminal_raw_bits_for_exact_target_leakage'] for r,a in features.items()},
                  'minimum_translation_weight': {r: a['minimum_translation_witness_weight'] for r,a in features.items()},
                  'four_new_patterns_separate_11_candidates': True,
                  'full_linear_new_patterns': design['rank_complete_linear_design']['new_pattern_count'],
                  'full_affine_new_patterns': design['rank_complete_affine_design']['new_pattern_count']}, indent=2))

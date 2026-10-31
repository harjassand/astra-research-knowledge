"""Exact rational controls for the predictive-flow realization theorem.

The infinite-dimensional and variational theorems are analytic arguments in
PROOF.txt. This receiver checks an actual stationary chain, its all-word
reversal mechanism, exact predictive coordinates and unbiased grid flows.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import math
import time

HERE = Path(__file__).resolve().parent


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def word_probability(P, pi, labels, word):
    row = [p * (a == word[0]) for p, a in zip(pi, labels)]
    for a in word[1:]:
        row = [sum((row[i] * P[i][j] for i in range(len(row))), Q(0)) * (labels[j] == a) for j in range(len(row))]
    return sum(row, Q(0))


def source(b):
    states = list(product((1, -1), repeat=2))
    labels = [(1 - s) // 2 for s, t in states]
    P = [[Q(0)] * 4 for _ in states]
    for i, (s, t) in enumerate(states):
        P[i][states.index((s, -t))] = (1 + b * s * t) / 2
        P[i][states.index((-s, t))] = (1 - b * s * t) / 2
    pi = [Q(1, 4)] * 4
    assert all(sum(row) == 1 for row in P)
    assert all(sum(P[i][j] for i in range(4)) == 1 for j in range(4))
    theta = [states.index((s, -t)) for s, t in states]
    assert all(labels[theta[i]] == labels[i] for i in range(4))
    assert all(P[theta[i]][theta[j]] == P[j][i] for i, j in product(range(4), repeat=2))
    f = [Q(s) for s, t in states]
    g = [Q(t) for s, t in states]
    Pf = [dot(row, f) for row in P]
    Ptf = [sum(P[j][i] * f[j] for j in range(4)) for i in range(4)]
    assert Pf == [b * x for x in g]
    assert Ptf == [-b * x for x in g]
    assert dot([pi[i] * f[i] for i in range(4)], Pf) == 0
    assert dot([pi[i] * Ptf[i] for i in range(4)], Pf) == -b * b
    for length in range(1, 9):
        for word in product(range(2), repeat=length):
            assert word_probability(P, pi, labels, word) == word_probability(P, pi, labels, word[::-1])
    return states, labels, P, pi


def rounding(x, k):
    y = x * k
    lo = y.numerator // y.denominator
    t = y - lo
    return [(lo, Q(1))] if not t else [(lo, 1 - t), (lo + 1, t)]


def quantized_flow(states, labels, P, pi, b, k):
    # The two predictive groups are rounded independently, conditional on
    # each original hidden state. Their cross products are then unbiased.
    coordinates = [((1 - b * t) / 2, (1 + b * t) / 2) for s, t in states]
    R = []
    for a, (plus, minus) in zip(labels, coordinates):
        R.append({(a, u, v): pu * pv for (u, pu), (v, pv) in product(rounding(plus, k), rounding(minus, k))})
    for a, (plus, minus), row in zip(labels, coordinates, R):
        assert sum(row.values()) == 1
        assert sum(p * Q(x[1], k) for x, p in row.items()) == plus
        assert sum(p * Q(x[2], k) for x, p in row.items()) == minus
        assert sum(p * Q(x[1], k) * Q(x[2], k) for x, p in row.items()) == plus * minus
    J = defaultdict(Q)
    for i, j in product(range(4), repeat=2):
        for x, y in product(R[i], R[j]):
            J[x, y] += pi[i] * P[i][j] * R[i][x] * R[j][y]
    J = {key: value for key, value in J.items() if value}
    nodes = sorted({x for x, y in J} | {y for x, y in J})
    mu = {x: sum(J.get((x, y), Q(0)) for y in nodes) for x in nodes}
    assert sum(mu.values()) == 1
    assert all(mu[x] == sum(J.get((y, x), Q(0)) for y in nodes) for x in nodes)
    h = Q(1, k)
    maximum = Q(0)
    for x in nodes:
        forward = sum(J.get((x, y), Q(0)) for y in nodes if y[0] == 1)
        backward = sum(J.get((y, x), Q(0)) for y in nodes if y[0] == 1)
        ferror = abs(forward - mu[x] * Q(x[1], k))
        berror = abs(backward - mu[x] * Q(x[2], k))
        assert ferror <= h * mu[x] and berror <= h * mu[x]
        maximum = max(maximum, ferror / mu[x], berror / mu[x])
    target = {}
    for u, a, v in product(range(2), repeat=3):
        total = sum(mass * (Q(x[2], k) if u else 1 - Q(x[2], k)) * (Q(x[1], k) if v else 1 - Q(x[1], k)) for x, mass in mu.items() if x[0] == a)
        actual = word_probability(P, pi, labels, (u, a, v))
        assert total == actual
        target[''.join(map(str, (u, a, v)))] = str(actual)
    # J itself is an actual finite chain. Its approximate predictive
    # equations do not make its word law identical to the input moments.
    Pg = [[J.get((x, y), Q(0)) / mu[x] for y in nodes] for x in nodes]
    pg = [mu[x] for x in nodes]
    labg = [x[0] for x in nodes]
    errors = [abs(word_probability(Pg, pg, labg, word) - word_probability(P, pi, labels, word)) for word in product(range(2), repeat=3)]
    assert max(errors) <= 2 * h
    entropy = sum(float(value) * math.log(float(value / J[y, x])) for (x, y), value in J.items())
    exact = float(b) * math.log(float((1 + b) / (1 - b)))
    assert entropy <= exact + 1e-12  # DPI is proved analytically, not by this display check.
    return {'mesh_denominator': k, 'full_grid_states': 2 * (k + 1) ** 2, 'positive_quantized_states': len(nodes), 'exact_data_cross_moments_preserved': True, 'maximum_exact_conditional_row_residual': str(maximum), 'maximum_actual_three_word_error': str(max(errors)), 'exact_total_three_word_L1_error': str(sum(errors)), 'quantized_flow_entropy_numeric': entropy, 'target_three_word_law': target}


def verify_lp_certificate():
    cert = json.loads((HERE / 'lp_certificate.json').read_text())
    k = cert['mesh']
    nodes = list(product(range(2), range(k + 1), range(k + 1)))
    words = list(product(range(2), repeat=3))
    n = len(nodes)
    y = list(map(Q, cert['row_duals']))
    data = list(map(Q, cert['data_duals']))
    z = Q(cert['normalization_dual'])
    assert len(y) == 4 * n and len(data) == 16
    assert all(a <= 0 for a in y + data)
    assert -sum(data) <= 1
    yd = [data[2 * j] - data[2 * j + 1] for j in range(8)]

    def feature(node, word):
        a, plus, minus = node
        u, center, v = word
        return Q(a == center) * (Q(minus, k) if u else 1 - Q(minus, k)) * (Q(plus, k) if v else 1 - Q(plus, k))

    rdata = [sum((coef * feature(node, word) for coef, word in zip(yd, words)), Q(0)) for node in nodes]

    def endpoint(i, j):
        out = rdata[i]
        for group, num in enumerate(nodes[i][1:]):
            q = Q(num, k)
            out += y[4 * i + 2 * group] * (nodes[j][0] - q - Q(1, k))
            out += y[4 * i + 2 * group + 1] * (q - nodes[j][0] - Q(1, k))
        return out

    columns = 0
    for i in range(n):
        for j in range(i, n):
            lhs = endpoint(i, j) + z if i == j else endpoint(i, j) + endpoint(j, i) + 2 * z
            assert lhs <= 0
            columns += 1
    assert columns == cert['symmetric_flow_columns']
    target = [Q(1, 8) - Q(1, 32) * (1 - 2 * u) * (1 - 2 * v) for u, a, v in words]
    gap = z + dot(yd, target)
    witness = [-z - a for a in yd]
    assert gap == Q(cert['exact_positive_source_dual_gap']) > 0
    assert witness == list(map(Q, cert['word_statistic']))
    assert dot(witness, target) == -gap
    width = max(witness) - min(witness)
    required = 8 * width ** 2 / gap ** 2
    windows = (required.numerator + required.denominator - 1) // required.denominator
    assert windows == cert['iid_validation_windows_sufficient_for_each_error_below_0_025']
    # The equally informed elementary reflection statistic is a stronger
    # comparator on THIS easier control. Its cost is charged explicitly.
    baseline_gap, baseline_width = Q(1, 4), Q(2)
    baseline = 8 * baseline_width ** 2 / baseline_gap ** 2
    assert baseline.denominator == 1
    return {'exact_rational_flow_columns_checked': columns, 'exact_compiled_word_statistic': list(map(str, witness)), 'exact_compiled_source_gap': str(gap), 'compiled_iid_windows': windows, 'ordinary_reflection_iid_windows': int(baseline), 'sampling_advantage_over_reflection_on_this_control': windows < baseline, 'hidden_state_count_bound_used': False}


def negative_controls():
    # A reversible, genuinely hidden-memory chain must remain an accepted
    # null. Its observed process is not first-order Markov.
    P = [[Q(1, 2), Q(1, 4), Q(1, 4)], [Q(1, 4), Q(3, 4), Q(0)], [Q(1, 4), Q(0), Q(3, 4)]]
    pi, labels = [Q(1, 3)] * 3, [0, 0, 1]
    p = {w: word_probability(P, pi, labels, w) for w in product(range(2), repeat=3)}
    assert p[0, 0, 1] / (p[0, 0, 0] + p[0, 0, 1]) != p[1, 0, 1] / (p[1, 0, 0] + p[1, 0, 1])
    cert = json.loads((HERE / 'lp_certificate.json').read_text())
    values = list(map(Q, cert['word_statistic']))
    assert dot(values, [p[w] for w in product(range(2), repeat=3)]) >= 0
    # Unconditional means alone admit a false zero-entropy explanation:
    # diagonal flow on the four proposed predictive points preserves all
    # data cross-moments, but those points are not its actual predictions.
    states = list(product((1, -1), repeat=2))
    rplus = [(1 - Q(1, 2) * t) / 2 for s, t in states]
    rminus = [(1 + Q(1, 2) * t) / 2 for s, t in states]
    assert sum(rplus) / 4 == sum(rminus) / 4 == Q(1, 2)
    for u, a, v in product(range(2), repeat=3):
        feature = sum((Q(1, 4) * (rminus[i] if u else 1 - rminus[i]) * (rplus[i] if v else 1 - rplus[i]) for i, (s, t) in enumerate(states) if (1 - s) // 2 == a), Q(0))
        assert feature == (1 - Q(1, 4) * (1 - 2 * u) * (1 - 2 * v)) / 8
    assert any(Q((1 - s) // 2) != rplus[i] for i, (s, t) in enumerate(states))
    # Shared rounding of the two groups biases a cross moment even in
    # equilibrium. Independent rounding is a load-bearing requirement.
    q = Q(1, 4)
    shared_product = sum(prob * Q(value) ** 2 for value, prob in rounding(q, 1))
    assert shared_product == q and shared_product != q * q
    return {'reversible_hidden_memory_null_accepted': True, 'unconditional_only_zero_entropy_false_explanation_received': True, 'shared_rounding_cross_moment_bias_received': True}


def systematic_rounding(probabilities, k):
    cumulative = [Q(0)]
    for p in probabilities:
        cumulative.append(cumulative[-1] + k * p)
    assert cumulative[-1] == k
    breaks = {Q(0), Q(1)}
    for x in cumulative:
        frac = x - x.numerator // x.denominator
        if frac:
            breaks.add(1 - frac)
    out = defaultdict(Q)
    cuts = sorted(breaks)
    for lo, hi in zip(cuts, cuts[1:]):
        u = (lo + hi) / 2
        rounded = [(x + u).numerator // (x + u).denominator for x in cumulative]
        counts = tuple(b - a for a, b in zip(rounded, rounded[1:]))
        assert min(counts) >= 0 and sum(counts) == k
        out[counts] += hi - lo
    for j, prob in enumerate(probabilities):
        assert sum(mass * Q(counts[j], k) for counts, mass in out.items()) == prob
    return dict(out)


def deep_quantization(P, pi, labels, k):
    depth = 2
    leaves = list(product(range(2), repeat=depth))
    Pback = [[pi[j] * P[j][i] / pi[i] for j in range(len(P))] for i in range(len(P))]

    def conditional(matrix, word):
        vector = [Q(1)] * len(P)
        for a in word[::-1]:
            vector = [sum((matrix[i][j] * vector[j] for j in range(len(P)) if labels[j] == a), Q(0)) for i in range(len(P))]
        return vector

    plus = [conditional(P, w) for w in leaves]
    minus = [conditional(Pback, w) for w in leaves]
    R = []
    for i in range(len(P)):
        pr = systematic_rounding([p[i] for p in plus], k)
        mr = systematic_rounding([p[i] for p in minus], k)
        R.append({(labels[i], a, b): pa * pb for (a, pa), (b, pb) in product(pr.items(), mr.items())})

    def prefix(node, side, word):
        return sum((Q(count, k) for leaf, count in zip(leaves, node[side + 1]) if leaf[:len(word)] == word), Q(0))

    # Each prefix, not just each individual leaf, has uniformly small error.
    for i, row in enumerate(R):
        for node, mass in row.items():
            for side, matrix in ((0, P), (1, Pback)):
                for length in range(depth + 1):
                    for word in product(range(2), repeat=length):
                        assert abs(prefix(node, side, word) - conditional(matrix, word)[i]) <= Q(1, k)
    J = defaultdict(Q)
    for i, j in product(range(len(P)), repeat=2):
        for x, y in product(R[i], R[j]):
            J[x, y] += pi[i] * P[i][j] * R[i][x] * R[j][y]
    J = {key: value for key, value in J.items() if value}
    nodes = sorted({x for x, y in J} | {y for x, y in J})
    mu = {x: sum(J.get((x, y), Q(0)) for y in nodes) for x in nodes}
    assert all(mu[x] == sum(J.get((y, x), Q(0)) for y in nodes) for x in nodes)
    for x in nodes:
        for label in range(2):
            for length in range(depth):
                for word in product(range(2), repeat=length):
                    fw = sum((J.get((x, y), Q(0)) * prefix(y, 0, word) for y in nodes if y[0] == label), Q(0))
                    bw = sum((J.get((y, x), Q(0)) * prefix(y, 1, word) for y in nodes if y[0] == label), Q(0))
                    assert abs(fw - mu[x] * prefix(x, 0, (label,) + word)) <= mu[x] / k
                    assert abs(bw - mu[x] * prefix(x, 1, (label,) + word)) <= mu[x] / k
    for word in product(range(2), repeat=5):
        observed = sum((mass * prefix(node, 1, word[:2][::-1]) * prefix(node, 0, word[3:]) for node, mass in mu.items() if node[0] == word[2]), Q(0))
        assert observed == word_probability(P, pi, labels, word)
    if all(pi[i] * P[i][j] == pi[j] * P[j][i] for i, j in product(range(len(P)), repeat=2)):
        assert all(value == J.get((y, x), Q(0)) for (x, y), value in J.items())
    return {'future_depth': 2, 'mesh': k, 'all_32_five_word_data_moments_exact': True, 'all_prefix_errors_and_conditioned_flow_rows_exact': True, 'positive_quantized_states': len(nodes)}


def generic_certificate_check(filename):
    path = HERE / filename
    if not path.is_file():
        return {'status': 'NOT_RUN'}
    cert = json.loads(path.read_text())
    if cert['certificate_status'] != 'RATIONAL_DUAL_PROPOSED':
        return {'status': cert['certificate_status'], 'global_equilibrium_conclusion': 'NONE'}
    from flow_grid import geometry, prefix
    s, depth, k = cert['alphabet_size'], cert['depth'], cert['mesh']
    leaves, nodes, descriptors, words = geometry(s, depth, k)
    n, d = len(nodes), len(descriptors)
    y, data, z = list(map(Q, cert['row_duals'])), list(map(Q, cert['data_duals'])), Q(cert['normalization_dual'])
    assert len(y) == n * d and len(data) == 2 * len(words)
    assert all(a <= 0 for a in y + data) and -sum(data) <= 1
    yd = [data[2 * w] - data[2 * w + 1] for w in range(len(words))]

    def F(node, word):
        return Q(node[0] == word[depth]) * prefix(node, 1, word[:depth][::-1], leaves, k) * prefix(node, 0, word[depth + 1:], leaves, k)

    rdata = [sum((a * F(node, word) for a, word in zip(yd, words)), Q(0)) for node in nodes]

    def endpoint(i, j):
        value = rdata[i]
        for r, (side, label, word, sign) in enumerate(descriptors):
            a = y[d * i + r]
            if a:
                following = prefix(nodes[j], side, word, leaves, k) if nodes[j][0] == label else Q(0)
                current = prefix(nodes[i], side, (label,) + word, leaves, k)
                value += a * (sign * (following - current) - Q(1, k))
        return value

    checked = 0
    for i in range(n):
        for j in range(i, n):
            assert endpoint(i, j) + z <= 0 if i == j else endpoint(i, j) + endpoint(j, i) + 2 * z <= 0
            checked += 1
    assert checked == cert['symmetric_flow_columns']
    p = list(map(Q, cert['probabilities']))
    gap = z + dot(yd, p)
    assert gap == Q(cert['exact_source_gap']) > 0
    assert dot(list(map(Q, cert['word_statistic'])), p) == -gap
    return {'status': 'EXACT_RATIONAL_DUAL_RECEIVED', 'flow_columns': checked, 'source_gap': str(gap), 'alphabet_size': s, 'depth': depth}


def finite_count_check():
    path = HERE / 'finite_counts.json'
    if not path.is_file():
        return {'status': 'NOT_RUN'}
    run = json.loads(path.read_text())
    results = {}
    for name, row in run['cases'].items():
        data = json.loads((HERE / f'{name}_counts.json').read_text())
        cert = json.loads((HERE / f'{name}_certificate.json').read_text())
        n = data['window_count']
        assert n == sum(data['word_counts']) == row['independent_windows']
        assert row['stationary_preparations'] == n and row['observed_letters'] == 3 * n and row['simulated_transitions'] == 2 * n
        p = [Q(c, n) for c in data['word_counts']]
        assert list(map(Q, cert['probabilities'])) == p
        assert not row['compiler_received_hidden_transition_matrix']
        alpha = Q(row['pointwise_error_alpha_each_method'])
        C = (int(2 * len(p) / alpha) - 1).bit_length()
        # e>2 and 2**C>=2*M/alpha justify the confidence radius without
        # a rounded logarithm. All rejection comparisons are rational.
        assert 2 ** C >= 2 * len(p) / alpha
        radius_squared = Q(C, 2 * n)
        assert radius_squared == Q(row['selection_safe_uniform_radius_squared'])
        delta = norm = Q(0)
        if cert['certificate_status'] == 'RATIONAL_DUAL_PROPOSED':
            received = generic_certificate_check(f'{name}_certificate.json')
            assert received['status'] == 'EXACT_RATIONAL_DUAL_RECEIVED'
            delta = Q(cert['exact_source_gap'])
            y = list(map(Q, cert['data_duals']))
            norm = sum(abs(y[2 * i] - y[2 * i + 1]) for i in range(len(p)))
        reject = delta > 0 and delta ** 2 > norm ** 2 * radius_squared
        assert delta == Q(row['certified_dual_gap_on_empirical_data'])
        assert norm == Q(row['data_dual_L1_norm']) <= 1
        assert reject == row['selection_safe_LP_rejects']
        results[name] = {'selection_safe_rejects': reject, 'exact_empirical_dual_gap': str(delta), 'iid_windows_charged': n, 'word_counts_and_rational_confidence_comparison_received': True}
    return results


def main():
    start = time.perf_counter()
    b = Q(1, 2)
    states, labels, P, pi = source(b)
    plus = [(1 - b * t) / 2 for s, t in states]
    minus = [(1 + b * t) / 2 for s, t in states]
    assert all(sum(P[i][j] for j in range(4) if labels[j] == 1) == plus[i] for i in range(4))
    assert all(sum(P[j][i] for j in range(4) if labels[j] == 1) == minus[i] for i in range(4))
    for i, a, j in product(range(2), repeat=3):
        assert word_probability(P, pi, labels, (i, a, j)) == (1 - b * b * (1 - 2 * i) * (1 - 2 * j)) / 8
    # An exact exclusion of every symmetric relaxed grid flow at k=8:
    # data force E[(q+ - q-)^2]>=b^2, whereas J=J^T plus the two
    # row tolerances forces |q+ - q-|<=2/k at every positive-mass row.
    assert b * b > 4 * Q(1, 8) ** 2
    controls = [quantized_flow(states, labels, P, pi, b, k) for k in (1, 2, 3, 4, 7, 8)]
    nullP = [[Q(1, 2), Q(1, 4), Q(1, 4)], [Q(1, 4), Q(3, 4), Q(0)], [Q(1, 4), Q(0), Q(3, 4)]]
    nullpi, nulllabels = [Q(1, 3)] * 3, [0, 0, 1]
    for name, dep, model, masses, labs in [('three_word_input', 1, P, pi, labels), ('five_word_input', 2, P, pi, labels), ('five_word_null', 2, nullP, nullpi, nulllabels)]:
        data = {'alphabet_size': 2, 'depth': dep, 'probabilities': [str(word_probability(model, masses, labs, word)) for word in product(range(2), repeat=2 * dep + 1)]}
        (HERE / (name + '.json')).write_text(json.dumps(data, indent=2) + '\n')
    deep = [deep_quantization(P, pi, labels, 3), deep_quantization(nullP, nullpi, nulllabels, 3)]
    generic = {name: generic_certificate_check(name) for name in ['generic_triple_certificate.json', 'generic_five_word_probe.json', 'generic_null_probe.json']}
    result = {'scope': __doc__, 'b': str(b), 'stationary_transition_matrix': [[str(x) for x in row] for row in P], 'stationary_mass': list(map(str, pi)), 'all_word_reversal_mechanism_exact': 'theta(s,t)=(s,-t), same label, theta P theta=P^T', 'observed_path_reversal_KL_all_lengths': '0', 'C1': '0', 'C2': str(-b * b), 'exact_least_hidden_cost': '(log 3)/2 nats per discrete step', 'least_cost_numeric': math.log(3) / 2, 'global_lower_bound': '2*b*artanh(b), proved for arbitrary standard-Borel hidden state space', 'minimum_attained_by_actual_four_state_chain': True, 'same_cost_is_minimum_for_complete_observed_law': True, 'symmetric_relaxed_grid_flow_k8_exactly_excluded': True, 'all_reflection_CP_blindspot': False, 'continuous_time_attainment': 'NOT_ASSERTED', 'quantization_controls': controls, 'simplex_five_word_controls': deep, 'generic_compiler': generic, 'compiled_LP_certificate': verify_lp_certificate(), 'negative_controls': negative_controls(), 'finite_count_inference': finite_count_check(), 'seconds': time.perf_counter() - start}
    (HERE / 'replay.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ['scope', 'stationary_transition_matrix', 'quantization_controls']}, indent=2))


if __name__ == '__main__':
    main()

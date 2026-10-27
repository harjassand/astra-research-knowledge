"""Independent exact checks for bounded-degree ANF gate acquisition."""
import itertools
import json
import random
from pathlib import Path


def mul(a, b):
    out = set()
    for x in a:
        for y in b:
            z = x | y
            if z in out:
                out.remove(z)
            else:
                out.add(z)
    return out


def trunc(a, cap):
    return {x for x in a if x.bit_count() <= cap}


def propagate(n, gates, cap=None, reject=False):
    values = [{1 << i} for i in range(n)]
    peak = 1
    for j, gate in enumerate(gates):
        op, a, *rest = gate
        if op == 'not':
            value = values[a] ^ {0}
        elif op == 'xor':
            value = values[a] ^ values[rest[0]]
        elif op == 'and':
            value = mul(values[a], values[rest[0]])
        else:
            raise ValueError(op)
        peak = max(peak, len(value))
        if cap is not None:
            low = trunc(value, cap)
            if reject and value != low:
                return None, j, peak
            value = low
        values.append(value)
    return values[-1], None, peak


def eval_anf(poly, x):
    return sum((m & x) == m for m in poly) & 1


def eval_gates(n, gates, x):
    values = [(x >> i) & 1 for i in range(n)]
    for op, a, *rest in gates:
        if op == 'not':
            v = 1 ^ values[a]
        elif op == 'xor':
            v = values[a] ^ values[rest[0]]
        else:
            v = values[a] & values[rest[0]]
        values.append(v)
    return values[-1]


def parity_sorted(items):
    """Deterministic coefficient cancellation using sorted equal runs."""
    items.sort()
    return tuple(key for key, run in itertools.groupby(items)
                 if sum(1 for _ in run) & 1)


def compile_terms(n, gates, term_cap, output_degree=3):
    """Acquire complete ANFs of any degree, capping only surviving terms."""
    values = [(1 << i,) for i in range(n)]
    maximum_degree = 1
    maximum_terms = 1
    for j, (op, a, *rest) in enumerate(gates):
        if op == 'not':
            value = parity_sorted(list(values[a]) + [0])
        elif op == 'xor':
            value = parity_sorted(list(values[a]) + list(values[rest[0]]))
        else:
            value = parity_sorted([x | y for x in values[a] for y in values[rest[0]]])
        if len(value) > term_cap:
            return None, 'term_cap', j, maximum_degree
        maximum_terms = max(maximum_terms, len(value))
        maximum_degree = max(maximum_degree, max((m.bit_count() for m in value), default=0))
        values.append(value)
    if any(m.bit_count() > output_degree for m in values[-1]):
        return None, 'output_degree', None, maximum_degree
    return set(values[-1]), 'accepted', None, maximum_degree


def main():
    rng = random.Random(1077)
    quartic = [('and', 0, 1), ('and', 4, 2), ('and', 5, 3)]
    false_constants = []
    for name, gates, expected in [
        ('quartic', quartic, (1, 0)),
        ('complement_quartic', quartic + [('not', 6)], (15, 16)),
        ('quartic_after_multiplication', quartic + [('and', 6, 0)], (1, 0)),
    ]:
        exact, _, _ = propagate(4, gates)
        quotient, _, _ = propagate(4, gates, cap=3)
        acquired, rejection, _ = propagate(4, gates, cap=3, reject=True)
        counts = (sum(eval_anf(exact, x) for x in range(16)),
                  sum(eval_anf(quotient, x) for x in range(16)))
        assert counts == expected
        assert acquired is None and rejection == 2
        false_constants.append({'case': name, 'exact_ones': counts[0],
                                'truncated_ones': counts[1], 'rejected_gate': rejection})

    final_constant = quartic + [('xor', 6, 6), ('not', 7)]
    exact, _, _ = propagate(4, final_constant)
    quotient, _, _ = propagate(4, final_constant, cap=3)
    acquired, rejection, _ = propagate(4, final_constant, cap=3, reject=True)
    assert exact == quotient == {0}
    assert acquired is None and rejection == 2

    # Sparse high-degree intermediates are accepted by the stronger compiler.
    sparse_positive = []
    for n in [4, 8, 20]:
        gates = [('and', 0, 1)]
        previous = n
        for i in range(2, n):
            gates.append(('and', previous, i))
            previous = n + len(gates) - 1
        high = previous
        gates.append(('and', high, 0))
        absorbed = n + len(gates) - 1
        gates.append(('xor', high, absorbed))
        zero = n + len(gates) - 1
        gates.append(('not', zero))
        value, status, _, highest = compile_terms(n, gates, 1)
        assert status == 'accepted' and value == {0} and highest == n
        sparse_positive.append({'inputs': n, 'term_cap': 1,
                                'maximum_intermediate_degree': highest, 'final_constant': 1})
    value, status, _, _ = compile_terms(4, quartic, 1)
    assert value is None and status == 'output_degree'

    # Apparent degree-six cross terms cancel before the cap is tested.
    a = {sum(1 << i for i in s) for s in itertools.combinations(range(8), 3)}
    assert mul(a, a) == a
    assert mul(a, a ^ {0}) == set()

    quotient_checks = 0
    for n in range(1, 9):
        for cap in range(0, min(3, n) + 1):
            for _ in range(20):
                a = {m for m in range(1 << n) if rng.randrange(5) == 0}
                b = {m for m in range(1 << n) if rng.randrange(5) == 0}
                assert trunc(mul(a, b), cap) == trunc(mul(trunc(a, cap), trunc(b, cap)), cap)
                assert trunc(a ^ b, cap) == trunc(a, cap) ^ trunc(b, cap)
                quotient_checks += 1

    accepted = rejected = assignments = 0
    term_accepted = term_rejected = term_assignments = 0
    for _ in range(160):
        n = 6
        gates = []
        for j in range(32):
            op = rng.choice(['xor', 'xor', 'and', 'not'])
            a = rng.randrange(n+j)
            gates.append((op, a) if op == 'not' else (op, a, rng.randrange(n+j)))
        exact, _, _ = propagate(n, gates)
        quotient, _, _ = propagate(n, gates, cap=3)
        acquired, rejection, _ = propagate(n, gates, cap=3, reject=True)
        assert quotient == trunc(exact, 3)
        term_value, term_status, _, _ = compile_terms(n, gates, 42)
        if term_value is None:
            term_rejected += 1
        else:
            term_accepted += 1
            assert term_value == exact
            for x in range(1 << n):
                assert eval_anf(term_value, x) == eval_gates(n, gates, x)
                term_assignments += 1
        if acquired is None:
            rejected += 1
        else:
            accepted += 1
            assert acquired == exact
            for x in range(1 << n):
                assert eval_anf(acquired, x) == eval_gates(n, gates, x)
                assignments += 1

    result = {
        'status': 'all exact assertions passed',
        'false_constant_examples': false_constants,
        'high_intermediate_final_constant': {
            'exact_final': 1, 'truncated_final': 1, 'rejected_gate': 2},
        'cubic_idempotence_and_complement_checks': 2,
        'quotient_ring_identity_checks': quotient_checks,
        'random_circuits': 160,
        'accepted_circuits': accepted,
        'rejected_circuits': rejected,
        'accepted_circuit_truth_checks': assignments,
        'term_budget_sparse_high_degree_positive_cases': sparse_positive,
        'term_budget_accepted_random_circuits': term_accepted,
        'term_budget_rejected_random_circuits': term_rejected,
        'term_budget_truth_checks': term_assignments,
        'term_budget_sparse_quartic_final_degree_rejection': True,
        'new_counting_claim': False,
    }
    Path(__file__).with_name('gate_compiler_audit_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

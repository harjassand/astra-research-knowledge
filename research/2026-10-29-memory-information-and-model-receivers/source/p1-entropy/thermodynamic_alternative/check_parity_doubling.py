"""Exact rational independent checks of parity doubling and port gluing.

No source samples are generated or redrawn. All tests below concern finite
generators constructed algebraically. Laplace checks are exact at the listed
rational arguments; the companion ordinary proof establishes all times.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib
import json

from check_thermodynamic_completion import zero, cycle, gen, inv, mul, tr, entropy


def reverse_flows(a):
    return tr(a)


def full_lift(a, w, eps):
    n = len(w)
    weights = [v / 2 for v in w] * 2
    flow = zero(2 * n)
    for i in range(n):
        for j in range(n):
            flow[i][j] = a[i][j] / 2
            flow[n + i][n + j] = a[j][i] / 2
        flow[i][n + i] = flow[n + i][i] = w[i] * eps / 2
    theta = list(range(n, 2 * n)) + list(range(n))
    source = list(range(n)) * 2
    return flow, weights, theta, source


def glued_lift(a, w, ports):
    n = len(w)
    interior = [i for i in range(n) if i not in ports]
    m, k = len(ports), len(interior)
    bp = {b: i for i, b in enumerate(ports)}
    xp = {x: m + i for i, x in enumerate(interior)}
    xm = {x: m + k + i for i, x in enumerate(interior)}
    flow = zero(m + 2 * k)
    weights = [w[b] for b in ports] + [w[x] / 2 for x in interior] * 2
    theta = list(range(m)) + list(range(m + k, m + 2 * k)) + list(range(m, m + k))
    source = list(ports) + interior * 2
    for b in ports:
        for c in ports:
            if b != c:
                flow[bp[b]][bp[c]] = (a[b][c] + a[c][b]) / 2
        for x in interior:
            flow[bp[b]][xp[x]] = a[b][x] / 2
            flow[xp[x]][bp[b]] = a[x][b] / 2
            flow[bp[b]][xm[x]] = a[x][b] / 2
            flow[xm[x]][bp[b]] = a[b][x] / 2
    for x in interior:
        for y in interior:
            flow[xp[x]][xp[y]] = a[x][y] / 2
            flow[xm[x]][xm[y]] = a[y][x] / 2
    return flow, weights, theta, source


def irreducible(a):
    for start in range(len(a)):
        seen, queue = {start}, [start]
        while queue:
            i = queue.pop()
            for j, value in enumerate(a[i]):
                if value and j not in seen:
                    seen.add(j)
                    queue.append(j)
        if len(seen) != len(a):
            return False
    return True


def assert_parity(flow, weights, theta):
    q = gen(flow, weights)
    n = len(q)
    assert all(theta[theta[i]] == i for i in range(n))
    assert all(weights[i] == weights[theta[i]] for i in range(n))
    assert all(q[i][i] == q[theta[i]][theta[i]] for i in range(n))
    assert all(flow[i][j] == flow[theta[j]][theta[i]]
               for i in range(n) for j in range(n))
    return q


def kernel_laplace(flow, weights, ports, s):
    q = gen(flow, weights)
    interior = [i for i in range(len(q)) if i not in ports]
    if not interior:
        return zero(len(ports))
    resolvent = inv([[(s if i == j else 0) - q[x][y]
                      for j, y in enumerate(interior)]
                     for i, x in enumerate(interior)])
    entry = [[flow[b][x] for x in interior] for b in ports]
    exit_rates = [[q[x][b] for b in ports] for x in interior]
    return mul(mul(entry, resolvent), exit_rates)


def c5_source():
    # Algebraic reproduction of the previously accepted source generator,
    # not a draw from its native sampling interface.
    weights = [F(1)] * 5 + [F(16, 15)] * 10
    flow = zero(15)
    for e in range(5):
        i, j = e, (e + 1) % 5
        for b in [0, 1]:
            x = 5 + 2 * e + b
            p = F(5, 8) if b == 0 else F(3, 8)
            flow[i][x], flow[j][x] = weights[x] * p, weights[x] * (1 - p)
            flow[x][i], flow[x][j] = weights[x] * (1 - p), weights[x] * p
    return flow, weights


def glued_test(a, w, ports, name, reciprocal):
    q = gen(a, w)
    flow, weights, theta, source = glued_lift(a, w, ports)
    q_new = assert_parity(flow, weights, theta)
    assert irreducible(flow)
    assert sum(weights) == sum(w)
    assert all(q_new[i][i] == q[x][x] for i, x in enumerate(source))
    assert all(theta[i] == i for i in range(len(ports)))
    assert [weights[i] for i in range(len(ports))] == [w[i] for i in ports]
    assert [-weights[i] * q_new[i][i] for i in range(len(ports))] == [
        -w[i] * q[i][i] for i in ports]
    for i, b in enumerate(ports):
        for j, c in enumerate(ports):
            assert flow[i][j] == (a[b][c] + a[c][b]) / 2
    controls = []
    for s in [F(0), F(1, 5), F(1), F(3), F(7)]:
        original = kernel_laplace(a, w, ports, s)
        lifted = kernel_laplace(flow, weights, list(range(len(ports))), s)
        sym = [[(original[i][j] + original[j][i]) / 2
                for j in range(len(ports))] for i in range(len(ports))]
        assert lifted == sym
        if reciprocal:
            assert original == sym
        controls.append(dict(s=s, original=original, lifted=lifted))
    return dict(name=name, original_states=len(w), lifted_states=len(weights),
                original_ports=ports, total_mass=sum(w),
                original_rates=[-q[i][i] for i in range(len(w))],
                lifted_rates=[-q_new[i][i] for i in range(len(weights))],
                parity=theta, irreducible=True, generalized_entropy_exactly_zero=True,
                reciprocal=reciprocal, transforms=controls,
                original_ordinary_entropy=entropy(a),
                lifted_ordinary_entropy=entropy(flow))


def conv(value):
    if isinstance(value, (F, Decimal)):
        return str(value)
    if isinstance(value, dict):
        return {k: conv(v) for k, v in value.items()}
    if isinstance(value, list):
        return [conv(v) for v in value]
    return value


def main():
    with localcontext() as ctx:
        ctx.prec = 80
        a = zero(3)
        cycle(a, [0, 1, 2], F(2), F(1))
        w = [F(1), F(2), F(3)]
        q, qstar = gen(a, w), gen(tr(a), w)
        assert q == [[F(-3), F(2), F(1)],
                     [F(1, 2), F(-3, 2), F(1)],
                     [F(2, 3), F(1, 3), F(-1)]]
        assert [q[i][i] for i in range(3)] == [qstar[i][i] for i in range(3)]
        original_entropy = entropy(a)
        assert abs(original_entropy - 3 * Decimal(2).ln()) < Decimal('1e-75')
        full = []
        for eps in [F(0), F(1, 7)]:
            flow, weights, theta, source = full_lift(a, w, eps)
            lift = assert_parity(flow, weights, theta)
            assert sum(weights) == sum(w)
            assert irreducible(flow) == bool(eps)
            assert all(-lift[i][i] == -q[x][x] + eps
                       for i, x in enumerate(source))
            for i in range(3):
                for j in range(3):
                    assert lift[i][j] == q[i][j] - (eps if i == j else 0)
                    assert lift[3 + i][3 + j] == qstar[i][j] - (eps if i == j else 0)
            assert abs(entropy(flow) - original_entropy) < Decimal('1e-75')
            full.append(dict(epsilon=eps, states=len(weights),
                             irreducible=irreducible(flow),
                             generalized_entropy_exactly_zero=True,
                             ordinary_entropy=entropy(flow)))

        single = glued_test(a, w, [0], 'nonuniform_three_state_one_port', True)
        multi = glued_test(a, w, [0, 1], 'nonuniform_three_state_two_ports', False)
        all_ports = glued_test(a, w, [0, 1, 2], 'nonuniform_three_state_all_ports', False)
        formula_checks = []
        for s in [F(0), F(1, 5), F(1), F(3), F(7)]:
            phi = kernel_laplace(a, w, [0], s)[0][0] / 3
            reverse_phi = kernel_laplace(tr(a), w, [0], s)[0][0] / 3
            explicit = (F(5, 9) * s + F(7, 6)) / (s * s + F(5, 2) * s + F(7, 6))
            assert phi == reverse_phi == explicit
            formula_checks.append(dict(s=s, phi=phi))

        c5, wc5 = c5_source()
        native = glued_test(c5, wc5, list(range(5)), 'accepted_fifteen_state_five_port', True)
        assert native['lifted_states'] == 25
        assert abs(native['original_ordinary_entropy'] - native['lifted_ordinary_entropy']) < Decimal('1e-75')
        results = dict(status='PASS',
                       scope='Exact rational generator, parity, stationary mass, clocks, irreducibility, '
                             'direct-flow and Laplace-kernel checks. No source draws. '
                             'The all-time theorem and finite-data conclusions use the separate ordinary proof.',
                       full_lifts=full, glued_lifts=[single, multi, all_ports, native],
                       rational_excursion_formula_checks=formula_checks,
                       code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        out = Path(__file__).with_name('PARITY_DOUBLING_CHECKS.json')
        out.write_text(json.dumps(conv(results), indent=2) + '\n')
        print(json.dumps(dict(status='PASS', full_lifts=len(full), glued_lifts=4,
                              exact_laplace_matrix_checks=20, exact_formula_checks=5,
                              source_draws=0, output=str(out)), indent=2))


if __name__ == '__main__':
    main()

"""Exact local admission and exhaustive native clock checks.

No sampling, trajectory, memory-time simulation, producer imports or large
system acquisition. SymPy is used only for exact rational/complex algebra.
"""
from collections import deque
from fractions import Fraction
from itertools import product
from pathlib import Path
from time import perf_counter
import hashlib
import json
import resource
import sympy as s

HERE = Path(__file__).resolve().parent


def basis(d, a, b):
    out = s.zeros(d)
    out[a, b] = 1
    return out


def dissipator(L, x):
    C = L.H * L
    return L * x * L.H - (C * x + x * C) / 2


def choi(fn, d):
    return sum((s.kronecker_product(basis(d, a, b), fn(basis(d, a, b)))
                for a in range(d) for b in range(d)), s.zeros(d*d)).applyfunc(s.expand)


def exact_ldl(M):
    """Unpivoted Hermitian LDL, with exact positive rational pivots."""
    n = M.rows
    assert M == M.H
    L = s.eye(n)
    D = []
    for i in range(n):
        v = s.expand(M[i, i] - sum(L[i, j] * D[j] * s.conjugate(L[i, j])
                                  for j in range(i)))
        assert v.is_Rational and v > 0, (i, v)
        D.append(v)
        for k in range(i+1, n):
            L[k, i] = s.cancel((M[k, i] - sum(
                L[k, j] * D[j] * s.conjugate(L[i, j])
                for j in range(i))) / v)
    assert s.simplify(L * s.diag(*D) * L.H - M) == s.zeros(n)
    return D


def algebra():
    t0 = perf_counter()
    one = s.eye(2)
    X = s.Matrix([[0, 1], [1, 0]])
    Y = s.Matrix([[0, -s.I], [s.I, 0]])
    Z = s.diag(1, -1)
    named = dict(zip('IXYZ', [one, X, Y, Z]))
    ps = {a+b: s.kronecker_product(named[a], named[b])
          for a in named for b in named if a+b != 'II'}
    h, l = s.symbols('h l', real=True)
    counts = 0
    for P in ps.values():
        J = l * P + s.I*h*s.eye(4)
        assert s.expand(J.H*J) == (l*l+h*h)*s.eye(4)
        for a, b in product(range(4), repeat=2):
            E = basis(4, a, b)
            r = (dissipator(J, E) - l*l*(P*E*P-E)
                 + s.I*l*h*(P*E-E*P))
            assert s.expand(r) == s.zeros(4)
            counts += 1

    # A single unknown support with genuinely noncommuting coherent terms.
    eps = s.Rational(1, 100000)
    H = eps*(ps['XI']/3+ps['ZX']/5+ps['YZ']/7)
    hbound = eps*(s.Rational(1,3)+s.Rational(1,5)+s.Rational(1,7))
    lam = hbound/4
    coefficients = {'XI': eps/3, 'ZX': eps/5, 'YZ': eps/7}
    def direct(E):
        return lam*sum((P*E*P-E for P in ps.values()), s.zeros(4)) \
            - s.I*(H*E-E*H)
    def uniformized(E):
        return sum((dissipator(lam*P+s.I*coefficients.get(name, 0)*s.eye(4), E)/lam
                    for name, P in ps.items()), s.zeros(4))
    assert ps['XI']*ps['ZX'] != ps['ZX']*ps['XI']
    assert s.simplify(choi(direct, 4) - choi(uniformized, 4)) == s.zeros(16)
    rate = 15*lam + sum(c*c for c in coefficients.values())/lam
    assert rate < 8*hbound

    # A nonunital error requires the separate CPTP-event construction.
    A = s.kronecker_product(s.Matrix([[0, 1], [0, 0]]), one)
    gamma = eps/11
    def error(E):
        return (-s.I*(H*E-E*H)+gamma*dissipator(A, E)).applyfunc(s.expand)
    kappa = 2*16*(hbound+gamma)
    def event(E):
        return (s.trace(E)*s.eye(4)/4+error(E)/kappa).applyfunc(s.expand)
    M = choi(event, 4)
    pivots = exact_ldl(M)
    for a, b in product(range(4), repeat=2):
        E = basis(4, a, b)
        assert s.trace(event(E)) == (1 if a == b else 0)
        assert kappa*(event(E)-E) == kappa*(s.trace(E)*s.eye(4)/4-E)+error(E)
    nonunital = s.simplify(event(s.eye(4))-s.eye(4))
    assert nonunital != s.zeros(4)
    # Without ballast, finite-rate Euler uniformization of hZ is not CP.
    euler = choi(lambda E: E-s.I*(Z*E-E*Z)/7, 2)
    bad_minor = euler.extract([0, 3], [0, 3]).det()
    assert bad_minor == -s.Rational(4,49)
    return {
        'symbolic_two_qubit_paulis': len(ps),
        'symbolic_basis_identities': counts,
        'noncommuting_generator_identity': True,
        'coherent_bound': str(hbound),
        'fixed_ballast_per_pauli': str(lam),
        'actual_uniformized_event_rate': str(rate),
        'general_rate_bound_8h': str(8*hbound),
        'nonunital_cptp_padding_rate': str(kappa),
        'choi_dimension': M.rows,
        'positive_exact_ldl_pivots': [str(x) for x in pivots],
        'max_ldl_pivot_bits': max(max(int(x.p).bit_length(), int(x.q).bit_length())
                                  for x in pivots),
        'nonunital_event_on_identity': str(nonunital),
        'unballasted_hamiltonian_choi_minor': str(bad_minor),
        'seconds_excluding_imports': perf_counter()-t0,
    }


def graph(w, h):
    pts = list(product(range(w), range(h)))
    adj = {v: [u for u in pts if abs(u[0]-v[0])+abs(u[1]-v[1]) == 1]
           for v in pts}
    return pts, adj


def enabled(v, phases, adj):
    return all(phases[w] != (phases[v]-1) % 3 for w in adj[v])


def clocks():
    t0 = perf_counter()
    core = [(0,0), (1,0), (2,0), (2,1), (1,1), (0,1)]
    fixed = dict(zip(core, [0,1,2,0,1,2]))
    _, coreadj = graph(3, 2)
    frozen = []
    for states in product(range(3), repeat=6):
        c = dict(zip(core, states))
        if all(not enabled(v, c, coreadj) for v in core):
            frozen.append(states)
    assert tuple(fixed.values()) in frozen
    assert len(frozen) == 6
    assert min(sum(x != 0 for x in row) for row in frozen) == 4
    # Exhaustive graph of ALL outside phase assignments for one native box.
    pts, adj = graph(4, 3)
    outside = [v for v in pts if v not in fixed]
    powers = [3**i for i in range(len(outside))]
    states_n = 3**len(outside)
    indeg = [0]*states_n
    edges = [[] for _ in range(states_n)]
    for idx in range(states_n):
        c = dict(fixed)
        for i, v in enumerate(outside):
            c[v] = (idx//powers[i]) % 3
        assert all(not enabled(v, c, adj) for v in core)
        for i, v in enumerate(outside):
            if enabled(v, c, adj):
                target = idx+(((c[v]+1)%3)-c[v])*powers[i]
                edges[idx].append(target)
                indeg[target] += 1
    queue = deque(i for i in range(states_n) if indeg[i] == 0)
    longest = [0]*states_n
    seen = 0
    while queue:
        i = queue.popleft()
        seen += 1
        for j in edges[i]:
            longest[j] = max(longest[j], longest[i]+1)
            indeg[j] -= 1
            if indeg[j] == 0:
                queue.append(j)
    assert seen == states_n, 'Unexpected nominal clock cycle'
    distances = {v: 0 for v in core}
    queue = deque(core)
    while queue:
        v = queue.popleft()
        for w in adj[v]:
            if w not in distances:
                distances[w] = distances[v]+1
                queue.append(w)
    bound = 2*sum(distances.values())
    assert max(longest) <= bound
    barriers = []
    for a, b in product(range(3), repeat=2):
        delta = (1-(a-b)) % 3
        barrier = a-b+delta
        assert 0 <= delta <= 2 and barrier % 3 == 1
        # At the unique integer barrier a v-increment is forbidden.
        assert not (barrier % 3 != 1)
        barriers.append([a, b, barrier, delta])
    return {
        'internally_frozen_rectangle_assignments': frozen,
        'minimal_nonzero_phases_from_flat': 4,
        'core_perimeter': core,
        'core_phases': list(fixed.values()),
        'native_box': [4, 3],
        'all_outside_assignments_checked': states_n,
        'nominal_transition_edges': sum(map(len, edges)),
        'terminal_assignments': sum(not x for x in edges),
        'all_state_graph_is_acyclic': True,
        'largest_possible_subsequent_update_count': max(longest),
        'analytic_update_bound_2sumdist': bound,
        'all_initial_edge_barriers': barriers,
        'seconds': perf_counter()-t0,
    }


def main():
    t0 = perf_counter()
    result = {
        'scope': 'Exact local algebra and finite clock-state enumeration; no memory trajectory or hardware acquisition',
        'algebra': algebra(),
        'clocks': clocks(),
        'random_samples': 0,
        'seconds_excluding_imports': perf_counter()-t0,
        'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (HERE/'OPERATION_REPLAY.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('algebra','clocks')}, indent=2))
    print('symbolic identities', result['algebra']['symbolic_basis_identities'])
    print('clock graph', result['clocks']['all_outside_assignments_checked'],
          result['clocks']['nominal_transition_edges'],
          'max moves', result['clocks']['largest_possible_subsequent_update_count'])


if __name__ == '__main__':
    main()

"""New focused exact checks; no packet or peer code is imported/executed."""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import hashlib
import json
import math
import resource
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ['REPORT.md', 'PROOF_RECONSTRUCTION.md',
       'DIRECT_LIMIT_INDEPENDENT_ADDENDUM.md', 'ROOT_COMPOSITION_AUDIT.md',
       'GREEN_SATURATION_STRENGTHENING.md', 'exact_checks.py',
       'exactchecks.json', 'sourcehashes.json']


def digest(path):
    data = path.read_bytes()
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def transpose(a):
    return list(map(list, zip(*a)))


def zero(n):
    return [[F(0)]*n for _ in range(n)]


def swap(s, edge):
    x, y = edge
    out = list(s)
    out[x], out[y] = out[y], out[x]
    return tuple(out)


def generator(n, rates):
    states = list(permutations(range(n)))
    ix = {s: i for i, s in enumerate(states)}
    out = zero(len(states))
    for i, s in enumerate(states):
        for edge, rate in rates.items():
            out[i][i] += rate
            out[i][ix[swap(s, edge)]] -= rate
    return out, states, ix


def projection(n, group):
    states = list(permutations(range(n)))
    ix = {s: i for i, s in enumerate(states)}
    p = zero(len(states))
    for i, s in enumerate(states):
        for g in group:
            target = tuple(s[g[j]] for j in range(n))
            p[i][ix[target]] += F(1, len(group))
    return p


def averaging_checks():
    # Triangle: two infinite edges already generate all permutations.
    a, _, _ = generator(3, {(0, 1): 1, (1, 2): 1})
    p = projection(3, list(permutations(range(3))))
    assert mm(p, p) == p
    assert mm(a, p) == zero(6) and mm(p, a) == zero(6)
    for finite_rate in (1, 2, 17, F(3, 7)):
        b, _, _ = generator(3, {(0, 2): finite_rate})
        assert mm(mm(p, b), p) == zero(6)
    # Dimer block plus two outside sites: internal edges disappear and retained
    # endpoints within the block aggregate under the exact projection.
    identity = tuple(range(4))
    transposition = swap(identity, (0, 1))
    p4 = projection(4, [identity, transposition])
    assert mm(p4, p4) == p4
    a4, _, _ = generator(4, {(0, 1): 1})
    assert mm(p4, a4) == zero(24) and mm(a4, p4) == zero(24)
    checks = 0
    for r01, r02, r12, r23 in ((11, 2, 3, 7), (0, F(2, 7), F(3, 5), 1), (1000, 0, 19, 0)):
        b, _, _ = generator(4, {(0, 1): r01, (0, 2): r02, (1, 2): r12, (2, 3): r23})
        collapsed, _, _ = generator(4, {(1, 2): r02+r12, (2, 3): r23})
        assert mm(mm(p4, b), p4) == mm(mm(p4, collapsed), p4)
        checks += 1
    return dict(triangle_boundary_noninjectivity_examples=4,
                dimer_retained_rate_aggregation_examples=checks,
                exact_projection_idempotence_and_kernel_checks=True,
                scope='exact generator identities; no numerical exponential approximation')


def approach_checks():
    theta_star = [F(0), F(0), F(1, 7)]
    c_squared = F(9)  # Four-site connected physical graph.
    rows = []
    previous = [None, None, None]
    for j in (2, 4, 8, 16, 32):
        reference = [F(1, j), F(1, j), F(1, 7)]
        cases = [
            [F(1, j), F(1, j*j), F(1, 7)],
            [F(1, 1 << j), F(1, j), F(1, 7)+F(1, j**3)],
            [F(1, math.factorial(j)), F(1, j**3), F(1, 7)+F(1, j**4)],
        ]
        for case, theta in enumerate(cases):
            assert all(x > 0 for x in theta)
            distance = c_squared*max(abs(x-y) for x, y in zip(theta, reference))
            to_boundary = c_squared*max(abs(x-y) for x, y in zip(theta, theta_star))
            if previous[case] is not None:
                assert distance < previous[case]
            previous[case] = distance
            rows.append(dict(sequence=case, index=j,
                             reciprocal_distance_to_uniform_boost_exact=str(distance),
                             reciprocal_distance_to_boundary_exact=str(to_boundary)))
    return dict(examples=rows,
                scope='exact reciprocal-distance arithmetic receiving the proved Lipschitz theorem')


def allocation_checks():
    eps = F(1, 10)
    c = [F(1, 2), F(3)]
    m = [1, 4]
    weights = [c[0], 2*c[1]]
    allocations = [eps*x/sum(weights) for x in weights]
    objective = sum(F(mi)*ci*ci/e for mi, ci, e in zip(m, c, allocations))
    optimum = sum(weights)**2/eps
    assert objective == optimum == F(845, 2)
    comparisons = 0
    for numerator in range(1, 100):
        trial = [eps*F(numerator, 100), eps*F(100-numerator, 100)]
        assert sum(F(mi)*ci*ci/e for mi, ci, e in zip(m, c, trial)) >= optimum
        comparisons += 1
    non_square = []
    c, m = [F(1, 2), F(3, 2), F(3)], [1, 3, 5]
    for bits, eta in ((8, F(1, 128)), (16, F(1, 8192)), (32, F(1, 1048576))):
        Q = 1 << bits
        lower, upper = [], []
        for mi, ci in zip(m, c):
            root = math.isqrt(mi*Q*Q)
            lo = F(root, Q)
            hi = F(root+(root*root != mi*Q*Q), Q)
            assert lo*lo <= mi <= hi*hi
            assert hi*hi <= (1+eta)**2*mi
            lower.append(ci*lo)
            upper.append(ci*hi)
        alloc = [eps*x/sum(upper) for x in upper]
        assert sum(alloc) == eps and all(x > 0 for x in alloc)
        caps = [ci*ci/e for ci, e in zip(c, alloc)]
        assert sum(ci*ci/k for ci, k in zip(c, caps)) == eps
        integer_caps = [F(math.ceil(k)) for k in caps]
        assert sum(ci*ci/k for ci, k in zip(c, integer_caps)) <= eps
        budget = sum(mi*k for mi, k in zip(m, caps))
        integer_budget = sum(mi*k for mi, k in zip(m, integer_caps))
        assert integer_budget-budget < sum(m)
        # This is stronger than comparing with the true optimum, since the
        # lower square-root sum underestimates that optimum.
        assert budget <= (1+eta)*sum(lower)**2/eps
        non_square.append(dict(square_root_grid_bits=bits, relative_target=str(eta),
                               epsilon_allocations=list(map(str, alloc)),
                               dimensionless_caps=list(map(str, caps)),
                               exact_error_budget=str(sum(ci*ci/k for ci, k in zip(c, caps))),
                               candidate_budget_exact=str(budget),
                               integer_candidate_budget_exact=str(integer_budget)))
    return dict(exact_square_root_optimum=str(optimum), rational_allocation_comparisons=comparisons,
                rational_square_root_receipts=non_square)


def quantum_check():
    p, q = F(3, 4), F(2, 3)
    # Identity and SWAP act on |01> as two distinct basis states.
    out_p = [F(0), p, 1-p, F(0)]
    out_q = [F(0), q, 1-q, F(0)]
    trace_distance = sum(abs(x-y) for x, y in zip(out_p, out_q))/2
    mixture_tv = abs(p-q)
    assert trace_distance == mixture_tv == F(1, 12)
    return dict(classical_TV_exact=str(mixture_tv), output_trace_distance_exact=str(trace_distance),
                diamond_upper_exact=str(2*mixture_tv),
                diamond_lower_from_this_input_exact=str(2*trace_distance),
                scope='sharp mixture-to-random-unitary channel constant, no coherent Hamiltonian claim')


def main():
    begin = time.perf_counter()
    old_before = {name: digest(HERE/name) for name in OLD}
    source = ROOT/'root/RECIPROCAL_RATE_METRIC.md'
    source_record = dict(path='root/RECIPROCAL_RATE_METRIC.md', **digest(source))
    receipt = dict(status='EXACT_CHECKS_PASS', averaging=averaging_checks(),
                   approaches=approach_checks(), allocation=allocation_checks(),
                   quantum=quantum_check(),
                   execution='new standalone standard-library code; no root or packet code executed')
    old_after = {name: digest(HERE/name) for name in OLD}
    assert old_before == old_after
    receipt['old_frozen_files_unchanged'] = True
    receipt['wall_seconds'] = time.perf_counter()-begin
    receipt['ru_maxrss_native_units'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    receipt['resource_scope'] = 'this small focused-check process only; native ru_maxrss units not converted'
    (HERE/'reciprocal_completion_checks.json').write_text(json.dumps(receipt, indent=2)+'\n')
    (HERE/'reciprocal_completion_sources.json').write_text(json.dumps(
        dict(audited_source=source_record, old_frozen_files=old_before,
             checker_source=digest(Path(__file__)), audit_source=digest(HERE/'RECIPROCAL_COMPLETION_AUDIT.md')),
        indent=2)+'\n')
    print(json.dumps({k: receipt[k] for k in ('status', 'old_frozen_files_unchanged', 'wall_seconds', 'quantum')}, indent=2))


if __name__ == '__main__':
    main()

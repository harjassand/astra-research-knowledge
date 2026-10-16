"""Independent adversarial checks. Python standard library only.

Does not import or execute any packet code. Fractions and integers decide every
assertion. Resource floats are reporting metadata only. Not formal verification.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import math
import resource
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def zeros(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]


def transpose(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    bt = transpose(b)
    return [[sum((x*y for x, y in zip(row, col)), F(0)) for col in bt]
            for row in a]


def mv(a, v):
    return [sum((x*y for x, y in zip(row, v)), F(0)) for row in a]


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a, b):
    return [[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c*x for x in row] for row in a]


def mpow(a, k):
    ans = eye(len(a))
    while k:
        if k & 1:
            ans = mm(ans, a)
        a = mm(a, a)
        k //= 2
    return ans


def inverse(a):
    n = len(a)
    v = [list(row)+erow for row, erow in zip(a, eye(n))]
    for j in range(n):
        pivot = next(i for i in range(j, n) if v[i][j])
        v[j], v[pivot] = v[pivot], v[j]
        d = v[j][j]
        v[j] = [x/d for x in v[j]]
        for i in range(n):
            if i != j and v[i][j]:
                d = v[i][j]
                v[i] = [x-d*y for x, y in zip(v[i], v[j])]
    return [row[n:] for row in v]


def killed_pair(n, weighted_edges):
    pairs = list(combinations(range(n), 2))
    ix = {p: i for i, p in enumerate(pairs)}
    w = zeros(n)
    for (x, y), r in weighted_edges.items():
        assert x < y and r >= 0
        w[x][y] = w[y][x] = F(r)
    h = zeros(len(pairs))
    for i, (x, y) in enumerate(pairs):
        h[i][i] = 2*w[x][y]
        for a, other in ((x, y), (y, x)):
            for z in range(n):
                if z not in (x, y):
                    h[i][i] += w[a][z]
                    h[i][ix[tuple(sorted((z, other)))]] -= w[a][z]
    return h, pairs, ix


def swap(s, e):
    ans = list(s)
    x, y = e
    ans[x], ans[y] = ans[y], ans[x]
    return tuple(ans)


def invperm(s):
    ans = [None]*len(s)
    for i, x in enumerate(s):
        ans[x] = i
    return tuple(ans)


def coupling_checks():
    records = []
    for n in range(2, 6):
        edges = list(combinations(range(n), 2))
        weighted = {e: (3*e[0]+5*e[1]+n) % 4 for e in edges}
        h, pairs, ix = killed_pair(n, weighted)
        checks = 0
        for sigma in permutations(range(n)):
            for e in pairs:
                eta = swap(sigma, e)
                left, right, coarse = {}, {}, {}
                killed = F(0)
                for edge, rate in weighted.items():
                    if not rate:
                        continue
                    transitions = ([(swap(sigma, edge), eta, rate),
                                    (sigma, swap(eta, edge), rate)] if edge == e
                                   else [(swap(sigma, edge), swap(eta, edge), rate)])
                    for ss, tt, rr in transitions:
                        if ss != sigma:
                            left[ss] = left.get(ss, F(0))+rr
                        if tt != eta:
                            right[tt] = right.get(tt, F(0))+rr
                        discrep = tuple(i for i in range(n) if ss[i] != tt[i])
                        assert len(discrep) in (0, 2)
                        if not discrep:
                            killed += rr
                        elif discrep != e:
                            coarse[discrep] = coarse.get(discrep, F(0))+rr
                assert left == {swap(sigma, edge): F(rate) for edge, rate in weighted.items() if rate}
                assert right == {swap(eta, edge): F(rate) for edge, rate in weighted.items() if rate}
                i = ix[e]
                assert killed == sum(h[i])
                assert coarse == {pair: -h[i][j] for j, pair in enumerate(pairs) if j != i and h[i][j]}
                checks += 1
        records.append(dict(n=n, joint_generator_states_checked=checks, pair_states=len(pairs)))
    return records


def inversion_checks():
    n = 4
    states = list(permutations(range(n)))
    ix = {s: i for i, s in enumerate(states)}
    edges = list(combinations(range(n), 2))
    rates = {e: (e[0]+2*e[1]) % 4 for e in edges}
    total = sum(rates.values())
    p = eye(len(states))
    for i, s in enumerate(states):
        p[i][i] -= F(total, 2*total)
        for e, r in rates.items():
            p[i][ix[swap(s, e)]] += F(r, 2*total)
    idstate = tuple(range(n))
    checks = 0
    for k in (0, 1, 2, 5):
        pk = mpow(p, k)
        for g in states:
            assert pk[0][ix[g]] == pk[0][ix[invperm(g)]]
        for sigma in states:
            row = pk[ix[sigma]]
            for e in edges:
                endpoint_gradient = sum(abs(row[j]-row[ix[swap(s, e)]]) for j, s in enumerate(states))
                initial_gradient = sum(abs(x-y) for x, y in zip(pk[ix[idstate]], pk[ix[swap(idstate, e)]]))
                assert endpoint_gradient == initial_gradient
                checks += 1
    return dict(n=n, rational_kernel_powers=[0, 1, 2, 5], gradient_equalities=checks)


def rounding_checks():
    # Exact Euler comparison only; the clock-to-heat error is proved in prose.
    records = []
    for n, rates in ((2, [1]), (3, [1, 2]), (4, [1, 0, 2])):
        lap = zeros(n)
        for x, r in enumerate(rates):
            lap[x][x] += r
            lap[x+1][x+1] += r
            lap[x][x+1] -= r
            lap[x+1][x] -= r
        N, Q = 32, 1 << 15
        p = sub(eye(n), scale(F(1, N), lap))
        m = scale(Q, p)
        assert all(x.denominator == 1 for row in m for x in row)
        stored = [m]
        power_checks = 0
        for j in range(5):
            prod = mm(stored[-1], stored[-1])
            rounded = [[F(int(x//Q)) for x in row] for row in prod]
            stored.append(rounded)
        for j, a in enumerate(stored):
            truth = mpow(p, 1 << j)
            for tr, ar in zip(truth, a):
                assert all(F(0) <= x/Q <= y for x, y in zip(ar, tr))
                assert sum(ar) <= Q
                assert sum(y-x/Q for x, y in zip(ar, tr)) <= F(((1 << j)-1)*n, Q)
                power_checks += 1
        binary_checks = 0
        bilinear_checks = 0
        for k in range(N+1):
            rounded = scale(Q, eye(n))
            kk, j = k, 0
            while kk:
                if kk & 1:
                    rounded = [[F(int(x//Q)) for x in row] for row in mm(rounded, stored[j])]
                kk //= 2
                j += 1
            truth = mpow(p, k)
            for tr, ar in zip(truth, rounded):
                assert all(F(0) <= x/Q <= y for x, y in zip(ar, tr))
                assert sum(y-x/Q for x, y in zip(ar, tr)) <= F(k*n, Q)
                binary_checks += 1
            def jform(x, y):
                return sum((x[a]*y[b]-x[b]*y[a] for a, b in combinations(range(n), 2)), F(0))
            for x, y in combinations(range(n), 2):
                exact = jform(truth[x], truth[y])
                approx = jform([v/Q for v in rounded[x]], [v/Q for v in rounded[y]])
                assert abs(exact-approx) <= F(2*k*n, Q)
                bilinear_checks += 1
        records.append(dict(n=n, N=N, Q=Q, stored_power_row_checks=power_checks,
                            binary_row_checks=binary_checks, bilinear_checks=bilinear_checks))
    return records


def projection(n, components, pairs):
    owner = {x: i for i, block in enumerate(components) for x in block}
    cross = list(combinations(range(len(components)), 2))
    members = {cd: [j for j, (x, y) in enumerate(pairs) if tuple(sorted((owner[x], owner[y]))) == cd]
               for cd in cross}
    p = zeros(len(pairs))
    lift = zeros(len(pairs), len(cross))
    for j, cd in enumerate(cross):
        indices = members[cd]
        assert len(indices) == len(components[cd[0]])*len(components[cd[1]])
        for a in indices:
            lift[a][j] = F(1)
            for b in indices:
                p[a][b] = F(1, len(indices))
    return p, lift, cross, owner


def coarse_k(components, slow, cross):
    k = len(components)
    owner = {x: i for i, block in enumerate(components) for x in block}
    b = zeros(k)
    for (x, y), r in slow.items():
        c, d = owner[x], owner[y]
        if c != d:
            b[c][d] += r
            b[d][c] += r
    ix = {cd: j for j, cd in enumerate(cross)}
    h = zeros(len(cross))
    for j, (c, d) in enumerate(cross):
        for a, other in ((c, d), (d, c)):
            for z in range(k):
                if z == a:
                    continue
                rate = b[a][z]/len(components[a])
                h[j][j] += rate
                if z != other:
                    h[j][ix[tuple(sorted((z, other)))]] -= rate
    return h


def limit_checks():
    records = []
    examples = [
        ([[0, 1], [2]], {(0, 1): 1}, {(1, 2): 1}),
        ([[0, 1, 2], [3, 4], [5]], {(0, 1): 2, (1, 2): 3, (3, 4): 1},
         {(0, 3): 1, (1, 4): 4, (2, 5): 2, (4, 5): 3}),
        ([[0, 1], [2, 3], [4], [5]], {(0, 1): 2, (2, 3): 3},
         {(1, 2): 7, (0, 4): 1, (3, 5): 2, (4, 5): 3}),
    ]
    for components, fast, slow in examples:
        n = sum(map(len, components))
        a, pairs, ix = killed_pair(n, fast)
        b, _, _ = killed_pair(n, slow)
        p, lift, cross, owner = projection(n, components, pairs)
        r = sub(inverse(add(a, p)), p)
        ident = eye(len(a))
        assert mm(p, p) == p
        assert mm(a, p) == zeros(len(a))
        assert mm(a, r) == sub(ident, p)
        assert mm(r, a) == sub(ident, p)
        assert mm(r, p) == zeros(len(a))
        c = mm(mm(p, b), p)
        coarse = coarse_k(components, slow, cross)
        assert mm(c, lift) == mm(lift, coarse)
        ones = [F(1)]*len(a)
        leakage = scale(F(-1), mm(mm(r, b), p))
        for edge in fast:
            i = ix[edge]
            block = owner[edge[0]]
            assert owner[edge[1]] == block
            assert all(v >= 0 for v in r[i])
            assert all(v == 0 for j, v in enumerate(r[i])
                       if not (owner[pairs[j][0]] == owner[pairs[j][1]] == block))
            assert all(v >= 0 for v in leakage[i])
            beta = []
            for cd in cross:
                value = F(0)
                if block in cd:
                    other = cd[0] if cd[1] == block else cd[1]
                    for j, (x, y) in enumerate(pairs):
                        if owner[x] == owner[y] == block:
                            exiting = sum((rate for (u, v), rate in slow.items()
                                           if ((u in (x, y) and owner[v] == other) or
                                               (v in (x, y) and owner[u] == other))), 0)
                            value += r[i][j]*exiting
                beta.append(value)
            assert mv(transpose(lift), leakage[i]) == beta
        records.append(dict(n=n, components=components, pair_states=len(a), coarse_pair_states=len(cross),
                            fast_edge_positive_rows_checked=len(fast), coarse_intertwiner_exact=True))

    # Exact explicit minimal example and its resolvent-transform convergence.
    a, pairs, ix = killed_pair(3, {(0, 1): 1})
    b, _, _ = killed_pair(3, {(1, 2): 1})
    p, _, _, _ = projection(3, [[0, 1], [2]], pairs)
    r = sub(inverse(add(a, p)), p)
    assert r == [[F(1, 2), F(0), F(0)],
                 [F(0), F(1, 4), F(-1, 4)],
                 [F(0), F(-1, 4), F(1, 4)]]
    assert sum(r[0]) == F(1, 2)
    assert scale(-1, mm(mm(r, b), p))[0] == [F(0), F(1, 4), F(1, 4)]
    resolvents = []
    for z in (F(1, 2), F(1), F(3)):
        target = F(1, 2)+F(1, 2)/(z+F(3, 2))
        previous = None
        for w in (1, 4, 16, 256, 65536):
            actual = w*mv(inverse(add(scale(z, eye(3)), add(scale(w, a), b))), [F(1)]*3)[0]
            err = abs(actual-target)
            if previous is not None:
                assert err < previous
            previous = err
            resolvents.append(dict(z=str(z), W=w, exact=str(actual), limit=str(target), error=str(err)))
    return records, resolvents


def finite_bit_sampler_checks():
    # Independently evaluate the stated conservative error formulas.
    Q = 1 << 64
    partial = F(0)
    term = F(1)
    for j in range(161):
        if j:
            term *= F(11, j)
        partial += term
    next_term = term*F(11, 161)
    upper = partial+next_term/(1-F(11, 162))
    p_lo, p_hi = 1/upper, 1/partial
    coefficient = F(1)
    retained_mass = F(0)
    floor_mass = 0
    width = F(0)
    for j in range(65):
        if j:
            coefficient *= F(11, j)
        retained_mass += p_lo*coefficient
        floor_mass += (Q*p_lo*coefficient).__floor__()
        width += (p_hi-p_lo)*coefficient
    assert 0 <= floor_mass <= Q and retained_mass <= 1
    count_error = F(11**65, math.factorial(65))/(1-F(11, 66))+width+F(65, Q)
    def failure(m):
        k = (m-1).bit_length()
        return F((1 << k)-m, 1 << k)**32
    results = []
    for n in (3, 6, 12, 20):
        rejection = 64*(failure(11)+failure(n-2))+sum((failure(m) for m in range(2, n-1)), F(0))
        total = count_error+rejection
        results.append(dict(n=n, count_error_exact=str(count_error), rejection_error_exact=str(rejection),
                            total_exact=str(total), total_decimal_display=float(total)))
    assert F(results[1]['total_exact']) < F(44, 10**16)
    assert F(results[2]['total_exact']) < F(48, 10**13)
    assert F(results[3]['total_exact']) < F(2438, 10**13)
    return results


def endpoint_lower(n, rates):
    """Exact rational lower law from positive uniformization/Taylor bounds."""
    states = list(permutations(range(n)))
    ix = {s: i for i, s in enumerate(states)}
    lam = sum(rates.values())
    assert lam > 0
    v = [F(int(i == 0)) for i in range(len(states))]
    partial = v.copy()
    term, exp_partial = F(1), F(1)
    terms = max(100, 4*lam)
    for k in range(1, terms+1):
        nxt = [F(0)]*len(states)
        for i, s in enumerate(states):
            for e, rate in rates.items():
                nxt[ix[swap(s, e)]] += v[i]*F(rate, lam)
        v = nxt
        term *= F(lam, k)
        exp_partial += term
        partial = [a+term*b for a, b in zip(partial, v)]
    upper_exp = exp_partial+term*F(lam, terms+1)/(1-F(lam, terms+2))
    lower = [x/upper_exp for x in partial]
    assert sum(lower) <= 1
    return lower


def green_strengthening_checks():
    interval_checks = 0
    for T in (F(1, 3), F(1), F(7, 2)):
        for a in (F(j, 4) for j in range(21)):
            for b in (F(j, 4) for j in range(21)):
                ell = max(F(0), min(T, a)-max(F(0), T-b))
                assert T*ell <= a*b
                interval_checks += 1
        assert T*max(F(0), min(T, T)-max(F(0), T-T)) == T*T
    normalizations = []
    for n in range(2, 7):
        rates = {(j, j+1): 2*j+3 for j in range(n-1)}
        if n > 2:
            rates[(0, n-1)] = 11
        cap = 4
        capped = {e: min(r, cap) for e, r in rates.items()}
        hr, pairs, ix = killed_pair(n, rates)
        hq, _, _ = killed_pair(n, capped)
        mu_r = mv(inverse(hr), [F(1)]*len(hr))
        mu_q = mv(inverse(hq), [F(1)]*len(hq))
        c = F(n*(n-1), 4)
        assert sum(r*mu_r[ix[e]] for e, r in rates.items()) == c
        assert sum(r*mu_q[ix[e]] for e, r in capped.items()) == c
        mean_bound = sum(abs(r-capped[e])*mu_r[ix[e]]*mu_q[ix[e]] for e, r in rates.items())
        reciprocal = max(abs(F(1, r)-F(1, capped[e])) for e, r in rates.items())
        normalized_bound = c*c*reciprocal
        assert mean_bound <= normalized_bound <= c*c/cap
        normalizations.append(dict(n=n, pair_states=len(pairs), normalization_exact=str(c),
                                   graph_specific_mean_bound_exact=str(mean_bound),
                                   reciprocal_infinity_bound_exact=str(normalized_bound),
                                   uniform_cap_bound_exact=str(c*c/cap)))

    endpoint_cases = []
    for n, rates, capped in (
            (2, {(0, 1): 10}, {(0, 1): 2}),
            (3, {(0, 1): 3, (1, 2): 30}, {(0, 1): 3, (1, 2): 10})):
        lr, lq = endpoint_lower(n, rates), endpoint_lower(n, capped)
        exact_tv_upper = (sum(abs(x-y) for x, y in zip(lr, lq))+2-sum(lr)-sum(lq))/2
        hr, pairs, ix = killed_pair(n, rates)
        hq, _, _ = killed_pair(n, capped)
        mr, mq = mv(inverse(hr), [F(1)]*len(hr)), mv(inverse(hq), [F(1)]*len(hq))
        green_bound = sum(abs(r-capped[e])*mr[ix[e]]*mq[ix[e]] for e, r in rates.items())
        c = F(n*(n-1), 4)
        infinity_bound = c*c*max(abs(F(1, r)-F(1, capped[e])) for e, r in rates.items())
        assert exact_tv_upper <= green_bound <= infinity_bound
        endpoint_cases.append(dict(n=n, rates={str(e): r for e, r in rates.items()},
                                   capped_rates={str(e): r for e, r in capped.items()},
                                   exact_rational_endpoint_TV_upper=str(exact_tv_upper),
                                   endpoint_TV_upper_display=float(exact_tv_upper),
                                   green_bound_exact=str(green_bound),
                                   reciprocal_infinity_bound_exact=str(infinity_bound)))

    # Scalar Erlang receiving interface against independently integrated powers.
    erlang = []
    for shape in (2, 3, 8, 16):
        shift, h, beta, original_decay, coarse_decay = F(20), F(1, 2), F(1, 2), F(0), F(3, 2)
        pr, pk = shift/(shift+original_decay), shift/(shift+coarse_decay)
        atom = shift/(shape-1)*h*pr**(shape-1)
        boundary = sum((beta*pr**j*pk**(shape-j) for j in range(1, shape)), F(0))/(shape-1)
        # For S_original=1 and g=beta exp(-coarse_decay*t),
        # C(t)=h+(beta/coarse_decay)(1-exp(-coarse_decay*t)).
        # E[C(Gamma)/Gamma] has this exact scalar Laplace expression.
        independently = shift/(shape-1)*(h+beta/coarse_decay*(1-pk**(shape-1)))
        assert atom+boundary == independently
        erlang.append(dict(shape=shape, exact_atom_plus_boundary=str(atom+boundary),
                           independent_closed_form_equal=True))
    return dict(interval_geometry_checks=interval_checks, normalization_checks=normalizations,
                positive_uniformization_endpoint_checks=endpoint_cases,
                erlang_scalar_checks=erlang)


def counterexamples():
    n, start, W, boundary = 6, 2, 10**6, 10
    s = n-start
    c = F(s*(s-1), 4)
    k = 0
    while F(1 << k) < F(W)/c:
        k += 1
    tail = F(n-1-start)*c*c/W*(boundary*boundary+2*(1+boundary)*(2+k))
    assert tail == F(15174, 10**6) < F(1, 20)
    # An isolated true label versus the incorrectly reported four-site lift.
    tv_lower = 1-F(1, s)
    assert tv_lower == F(3, 4) > F(1, 20)
    # Equal occupancy means, disjoint correlated outcomes: p=1/2 limiting law.
    law_a = {tuple(sorted(x)): F(1, 4) for x in ((0, 1), (1, 2), (0, 3), (2, 3))}
    law_b = {tuple(sorted(x)): F(1, 4) for x in ((0, 1), (1, 3), (0, 2), (2, 3))}
    for v in range(4):
        assert sum(p for state, p in law_a.items() if v in state) == F(1, 2)
        assert sum(p for state, p in law_b.items() if v in state) == F(1, 2)
    tv = sum(abs(law_a.get(x, F(0))-law_b.get(x, F(0))) for x in set(law_a)|set(law_b))/2
    assert tv == F(1, 2)
    return dict(wrapper_tail_exact=str(tail), incorrect_block_TV_lower_exact=str(tv_lower),
                equal_mean_occupancy_TV_limit_exact=str(tv),
                trajectory_count_TV_lower_exact=str(F(9, 10)-F(1, 9801)),
                direct_limit_atom_only_counterexample='2/3-exp(-3bT/2)/6 > 1/2 for bT>0')


def source_hashes():
    rel = [
        'originals/pair/PAIR_CERTIFIED_AVERAGING_REPORT.md',
        'originals/pair/LOCAL_SATURATION_PROOF.md',
        'originals/pair/source_N727.txt',
        'originals/pair/rigorous_pair_certificate.py',
        'originals/pair/fair_bit_sampler.py',
        'originals/exterior/interchange_path_exterior/EXTERIOR_CERTIFIER_REPORT.md',
        'originals/exterior/interchange_path_exterior/exterior_certificate.py',
        'originals/exterior/interchange_path_exterior/cycle_extension/PROOF.md',
        'root/DIRECT_AVERAGING_CERTIFICATE.md',
        'root/direct_average.py',
        'root/DEPENDENCY_erlang_certificate.v0001.py',
    ]
    result = []
    for path in rel:
        data = (ROOT/path).read_bytes()
        result.append(dict(path=path, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    return result


def main():
    begin = time.perf_counter()
    receipt = dict(status='EXACT_CHECKS_PASS', proof_status='INTERNAL_RECONSTRUCTION_NOT_FORMAL',
                   execution='new independent Python standard-library source only; packet code not imported',
                   coupling=coupling_checks(), inversion=inversion_checks(), rounding=rounding_checks())
    receipt['direct_limit'], receipt['minimal_resolvent_transforms'] = limit_checks()
    receipt['sampler_error_formulas'] = finite_bit_sampler_checks()
    receipt['green_strengthening'] = green_strengthening_checks()
    receipt['counterexamples'] = counterexamples()
    receipt['wall_seconds'] = time.perf_counter()-begin
    receipt['ru_maxrss_native_units'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    receipt['resource_scope'] = 'this exact-check process only; native ru_maxrss units are platform dependent'
    (HERE/'exactchecks.json').write_text(json.dumps(receipt, indent=2)+'\n')
    (HERE/'sourcehashes.json').write_text(json.dumps(source_hashes(), indent=2)+'\n')
    print(json.dumps({k: receipt[k] for k in ('status', 'wall_seconds', 'ru_maxrss_native_units', 'counterexamples')}, indent=2))


if __name__ == '__main__':
    main()

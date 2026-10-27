"""Discriminating arithmetic check, not a novelty benchmark or complete compiler.

Reconstruct dense integer tensor inputs and symmetrize in F_(p^2),
then use ordinary Fisher/Kasteleyn/Pfaffian on exactly those reconstructed
inputs. Compare with independent integer cycle-space enumeration. Distinct
prime local discriminants force characteristic-zero compositum degree 2^V.
No simultaneous-splitting prime is selected. Exact characteristic-zero class
recognition and full CRT are proved separately, not implemented here.
"""
from itertools import product
from pathlib import Path
import json
import random
import time

BITS = tuple(product(range(2), repeat=3))
RADICANDS = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
             31, 37, 41, 43, 47, 53, 59, 61, 67, 71]


class Q:
    """Quadratic extension over either F_p or another Q field."""
    __slots__ = ('a', 'b', 'f')

    def __init__(self, a, b, f):
        self.f = f
        self.a, self.b = f.cast(a), f.cast(b)

    def coerce(self, x):
        if isinstance(x, Q) and x.f is self.f:
            return x
        return Q(x, 0, self.f)

    def __add__(self, x):
        x = self.coerce(x)
        return Q(self.a + x.a, self.b + x.b, self.f)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b, self.f)

    def __sub__(self, x):
        return self + (-self.coerce(x))

    def __rsub__(self, x):
        return self.coerce(x) - self

    def __mul__(self, x):
        x = self.coerce(x)
        return Q(self.a*x.a + self.f.d*self.b*x.b,
                 self.a*x.b + self.b*x.a, self.f)

    __rmul__ = __mul__

    def inv(self):
        n = self.a*self.a - self.f.d*self.b*self.b
        if self.f.base is None:
            ni = pow(n % self.f.p, -1, self.f.p)
        else:
            ni = n.inv()
        return Q(self.a*ni, -self.b*ni, self.f)

    def __truediv__(self, x):
        return self * self.coerce(x).inv()

    def __rtruediv__(self, x):
        return self.coerce(x) / self

    def __pow__(self, n):
        if n < 0:
            return self.inv() ** (-n)
        out, x = self.coerce(1), self
        while n:
            if n & 1:
                out *= x
            x *= x
            n >>= 1
        return out

    def __eq__(self, x):
        try:
            x = self.coerce(x)
        except (TypeError, AttributeError):
            return False
        if self.f.base is None:
            return ((self.a-x.a) % self.f.p == 0 and
                    (self.b-x.b) % self.f.p == 0)
        return self.a == x.a and self.b == x.b

    def __bool__(self):
        return not self == 0

    def key(self):
        if self.f.base is None:
            return (self.a % self.f.p, self.b % self.f.p)
        return self.a.key() + self.b.key()


class Field:
    def __init__(self, p, d, base=None):
        self.p, self.base = p, base
        self.cast = (lambda x: x % p) if base is None else base.element
        self.d = self.cast(d)

    def element(self, x=0, b=0):
        if isinstance(x, Q) and x.f is self and b == 0:
            return x
        return Q(x, b, self)


def quadratic_field(p):
    d = next(a for a in range(2, p) if pow(a, (p-1)//2, p) == p-1)
    f2 = Field(p, d)
    squares = {}
    elements = [f2.element(a, b) for a in range(p) for b in range(p)]
    for x in elements:
        squares.setdefault((x*x).key(), x)
    def sqrt2(x):
        return squares[f2.element(x).key()]
    return f2, sqrt2


def mm(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def det(a):
    return a[0][0]*a[1][1] - a[0][1]*a[1][0]


def inv(a):
    d = det(a)
    return [[a[1][1]/d, -a[0][1]/d], [-a[1][0]/d, a[0][0]/d]]


def cp(t, f2, sqrt2):
    m = [[[f2.element(t[x, i, j]) for j in range(2)] for i in range(2)] for x in range(2)]
    shift = next(k for k in (0, 1, 2) if det([[m[0][i][j]+k*m[1][i][j] for j in range(2)] for i in range(2)]))
    a = [[m[0][i][j]+shift*m[1][i][j] for j in range(2)] for i in range(2)]
    c = mm(m[1], inv(a))
    if c[0][1] or c[1][0]:
        tr = c[0][0]+c[1][1]
        disc = tr*tr-4*det(c)
        if not disc:
            raise ValueError('bad prime: zero local discriminant')
        z = sqrt2(disc)
        eigen = [(tr+z)/2, (tr-z)/2]
        if c[0][1]:
            columns = [[c[0][1], lam-c[0][0]] for lam in eigen]
        else:
            columns = [[lam-c[1][1], c[1][0]] for lam in eigen]
        u = [[columns[j][i] for j in range(2)] for i in range(2)]
    else:
        eigen = [c[0][0], c[1][1]]
        if eigen[0] == eigen[1]:
            raise ValueError('bad prime: repeated diagonal eigenvalues')
        u = [[f2.element(i == j) for j in range(2)] for i in range(2)]
    v = mm(inv(u), a)
    factors = [[[1-shift*lam, lam] for lam in eigen],
               [[u[i][s] for i in range(2)] for s in range(2)],
               [[v[s][j] for j in range(2)] for s in range(2)]]
    for bits in BITS:
        value = sum(factors[0][s][bits[0]]*factors[1][s][bits[1]]*factors[2][s][bits[2]] for s in range(2))
        assert value == t[bits]
    assert all(x**(f2.p*f2.p) == x for leg in factors for column in leg for x in column)
    return factors


def prism(k):
    rotation = {}
    for i in range(k):
        rotation[i] = [(i+1) % k, k+i, (i-1) % k]
        rotation[k+i] = [k+(i-1) % k, i, k+(i+1) % k]
    edges = sorted({tuple(sorted((v, w))) for v, ws in rotation.items() for w in ws})
    return rotation, edges


def transform(t, axis, g):
    return {bits: sum(g[bits[axis]][j] * t[tuple(j if a == axis else bits[a] for a in range(3))] for j in range(2)) for bits in BITS}


def tensors(rotation, edges, odd=False, perturb=False):
    base, dense = {}, {}
    for v in rotation:
        values = iter([1, 1, 1, RADICANDS[v]])
        parity = 1 if odd and v == 0 else 0
        base[v] = {b: next(values) if sum(b) % 2 == parity else 0 for b in BITS}
    if perturb:
        base[0][0, 0, 1] = 1
    dense = {v: dict(t) for v, t in base.items()}
    for k, (v, w) in enumerate(edges):
        a, b = 1+k % 3, 1+(k//3) % 3
        g = [[1, a], [b, 1+a*b]]
        dual = [[1+a*b, -b], [-a, 1]]
        dense[v] = transform(dense[v], rotation[v].index(w), g)
        dense[w] = transform(dense[w], rotation[w].index(v), dual)
    assert all(isinstance(x, int) for t in dense.values() for x in t.values())
    return base, dense


def even_truth(rotation, edges, base):
    # Independent enumeration of the binary cycle space; no Pfaffian or CP.
    index = {e: i for i, e in enumerate(edges)}
    parent, tree, stack = {0: None}, set(), [0]
    while stack:
        v = stack.pop()
        for w in rotation[v]:
            if w not in parent:
                parent[w] = v
                tree.add(tuple(sorted((v, w))))
                stack.append(w)
    cycles = []
    for v, w in edges:
        if (v, w) in tree:
            continue
        path_v, path_w = [], []
        x = v
        while x is not None:
            path_v.append(x)
            x = parent[x]
        x = w
        while x not in path_v:
            path_w.append(x)
            x = parent[x]
        path = path_v[:path_v.index(x)+1] + list(reversed(path_w))
        mask = 1 << index[v, w]
        for a, b in zip(path, path[1:]):
            mask ^= 1 << index[tuple(sorted((a, b)))]
        cycles.append(mask)
    total = 0
    for choices in range(1 << len(cycles)):
        mask = 0
        for k, cyc in enumerate(cycles):
            if choices >> k & 1:
                mask ^= cyc
        term = 1
        for v, ws in rotation.items():
            bits = tuple((mask >> index[tuple(sorted((v, w)))]) & 1 for w in ws)
            term *= base[v][bits]
        total += term
    return total, len(cycles)


def faces(rotation):
    seen, result = set(), []
    for v, ws in rotation.items():
        for w in ws:
            if (v, w) in seen:
                continue
            face, dart = [], (v, w)
            while dart not in seen:
                seen.add(dart)
                face.append(dart)
                a, b = dart
                dart = (b, rotation[b][(rotation[b].index(a)-1) % len(rotation[b])])
            assert dart == (v, w)
            result.append(face)
    return result


def pfaffian(a, one):
    a = [row[:] for row in a]
    out, n = one, len(a)
    for i in range(0, n, 2):
        j = next((j for j in range(i+1, n) if a[i][j]), None)
        if j is None:
            return 0*one
        if j != i+1:
            a[i+1], a[j] = a[j], a[i+1]
            for row in a:
                row[i+1], row[j] = row[j], row[i+1]
            out = -out
        pivot = a[i][i+1]
        out *= pivot
        for j in range(i+2, n):
            for k in range(j+1, n):
                a[j][k] += (a[i+1][j]*a[i][k]-a[i][j]*a[i+1][k])/pivot
                a[k][j] = -a[j][k]
    return out


def fisher_fkt(rotation, edges, weights, field):
    # Established triangle Fisher reduction, constructed from the embedding.
    ports = {(v, w): 3*v+k for v, ws in rotation.items() for k, w in enumerate(ws)}
    fr, ew, external = {}, {}, []
    pref = field.element(pow(pow(2, len(rotation)//2, field.p), -1, field.p))
    for v, ws in rotation.items():
        for k, w in enumerate(ws):
            p = ports[v, w]
            after, before = 3*v+(k+1) % 3, 3*v+(k-1) % 3
            fr[p] = [ports[w, v], after, before]
            ew[tuple(sorted((p, after)))] = field.element(1)
    for edge in edges:
        v, w = edge
        a, b = weights[edge]
        w0, w1 = a+b, a-b
        assert w0 and w1
        e = tuple(sorted((ports[v, w], ports[w, v])))
        ew[e] = w0/w1
        pref *= w1
        external.append(e)
    edge_list = sorted(ew)
    index = {e: i for i, e in enumerate(edge_list)}
    fs = faces(fr)
    assert len(fr)-len(edge_list)+len(fs) == 2
    # Clockwise-odd constraints on all but one face, solved over F_2.
    rows = []
    for face in fs[1:]:
        mask, rhs = 0, 1
        for a, b in face:
            mask ^= 1 << index[tuple(sorted((a, b)))]
            rhs ^= a > b
        rows.append([mask, rhs])
    pivots = {}
    for mask, rhs in rows:
        while mask:
            col = (mask & -mask).bit_length()-1
            if col not in pivots:
                pivots[col] = (mask, rhs)
                break
            old_mask, old_rhs = pivots[col]
            mask ^= old_mask
            rhs ^= old_rhs
        else:
            assert rhs == 0
    solution = 0
    for col in sorted(pivots, reverse=True):
        mask, rhs = pivots[col]
        if ((mask & solution).bit_count() & 1) != rhs:
            solution ^= 1 << col
    for mask, rhs in rows:
        assert ((mask & solution).bit_count() & 1) == rhs
    n, zero = len(fr), field.element(0)
    a = [[zero for _ in range(n)] for _ in range(n)]
    arrow = {}
    for i, e in enumerate(edge_list):
        u, v = e
        arrow[e] = 1 if solution >> i & 1 else -1
        a[u][v] = arrow[e]*ew[e]
        a[v][u] = -a[u][v]
    matching_sign = 1
    for e in external:
        matching_sign *= arrow[e]
    for i, (a0, a1) in enumerate(external):
        for b0, b1 in external[i+1:]:
            if a0 < b0 < a1 < b1 or b0 < a0 < b1 < a1:
                matching_sign = -matching_sign
    return pref*matching_sign*pfaffian(a, field.element(1)), n


def modular_stage(rotation, edges, dense, p, branch_flip=False):
    f2, sqrt2 = quadratic_field(p)
    field = f2  # Every stage uses this same quadratic field.
    factors = {v: cp(t, f2, sqrt2) for v, t in dense.items()}
    if branch_flip:
        for v in rotation:
            if v % 3 != 1:
                factors[v] = [list(reversed(leg)) for leg in factors[v]]
    balance = {v: f2.element(1) for v in rotation}
    g = {v: field.element(1) for v in rotation}
    weights = {}
    for v, w in edges:
        left = factors[v][rotation[v].index(w)]
        right = factors[w][rotation[w].index(v)]
        m = [[sum(left[s][k]*right[t][k] for k in range(2)) for t in range(2)] for s in range(2)]
        if not all(m[s][t] for s in range(2) for t in range(2)):
            raise ValueError('bad prime: zero CP edge pairing')
        r2 = m[1][0]*m[1][1]/(m[0][0]*m[0][1])
        s2 = m[0][1]*m[1][1]/(m[0][0]*m[1][0])
        balance[v] *= r2
        balance[w] *= s2
        r = sqrt2(r2)
        s = field.element(m[1][1]/m[0][0])/r
        assert r*r == r2 and s*s == s2
        assert field.element(m[0][1])/s == field.element(m[1][0])/r
        g[v] *= r
        g[w] *= s
        weights[v, w] = [field.element(m[0][0]), field.element(m[0][1])/s]
    if any(x != 1 for x in balance.values()):
        return {'status': 'UNKNOWN', 'reason': 'local balance fails modulo this prime'}
    assert all(x == 1 or x == -1 for x in g.values())
    sign = field.element(1)
    for x in g.values():
        sign *= x
    if sign == -1:
        return {'status': 'ZERO_PARITY', 'residue': 0, 'global_sign': -1}
    # Incidence sign solve on a spanning tree, keeping one root.
    parent, order = {0: None}, [0]
    for v in order:
        for w in rotation[v]:
            if w not in parent:
                parent[w] = v
                order.append(w)
    for v in reversed(order[1:]):
        w = parent[v]
        if g[v] == -1:
            g[v], g[w] = -g[v], -g[w]
            e = tuple(sorted((v, w)))
            weights[e][1] = -weights[e][1]
    assert all(x == 1 for x in g.values())
    result, fisher_n = fisher_fkt(rotation, edges, weights, field)
    key = result.key()
    assert key[1:] == (0,), ('not a rational-field residue', key)
    return {'status': 'FKT_RESIDUE', 'residue': key[0], 'global_sign': 1,
            'fisher_vertices': fisher_n, 'cp_field_degree': 2,
            'contraction_field_degree': 2,
            'nonsquare_local_discriminants': sum(pow(d % p, (p-1)//2, p) == p-1 for d in RADICANDS[:len(rotation)])}


def arbitrary_pair_root_audit(p=79, target=200):
    # No parity promise or hidden-gauge generator: arbitrary dense integer pairs.
    f2, sqrt2 = quadratic_field(p)
    rng = random.Random(20261027)
    passed = nonbase_roots = attempts = 0
    while passed < target:
        attempts += 1
        pair = [{bits: rng.randrange(-7, 8) for bits in BITS} for _ in range(2)]
        try:
            a, b = [cp(t, f2, sqrt2)[0] for t in pair]
        except (ValueError, KeyError, StopIteration):
            continue
        m = [[sum(a[s][k]*b[t][k] for k in range(2)) for t in range(2)] for s in range(2)]
        if not all(m[s][t] for s in range(2) for t in range(2)):
            continue
        r2 = m[1][0]*m[1][1]/(m[0][0]*m[0][1])
        r = sqrt2(r2)
        assert r*r == r2
        norm = r2**(p+1)
        assert norm.key()[1] == 0
        assert pow(norm.key()[0], (p-1)//2, p) == 1
        nonbase_roots += r.key()[1] != 0
        passed += 1
    return {'arbitrary_dense_pair_count': passed, 'attempts': attempts,
            'prime': p, 'all_edge_square_roots_in_same_quadratic_field': True,
            'roots_outside_base_prime_field': nonbase_roots,
            'parity_balance_promise_used': False}


def main():
    started = time.perf_counter()
    reports = []
    for k in (6, 10):
        rotation, edges = prism(k)
        base, dense = tensors(rotation, edges)
        truth, cycle_dim = even_truth(rotation, edges, base)
        good = 0
        for p in (79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137):
            try:
                result = modular_stage(rotation, edges, dense, p)
            except (ValueError, KeyError, StopIteration) as e:
                reports.append({'vertices': 2*k, 'prime': p, 'skipped': str(e)})
                continue
            assert result['status'] == 'FKT_RESIDUE', result
            assert result['residue'] == truth % p, (p, result, truth % p)
            flipped = modular_stage(rotation, edges, dense, p, True)
            assert flipped['residue'] == result['residue']
            _, odd = tensors(rotation, edges, odd=True)
            odd_result = modular_stage(rotation, edges, odd, p)
            assert odd_result['status'] == 'ZERO_PARITY'
            reports.append({'vertices': 2*k, 'edges': len(edges), 'prime': p,
                            'characteristic_zero_cp_compositum_degree': 1 << (2*k),
                            'independent_cycle_dimension': cycle_dim,
                            'exact_integer_partition': str(truth),
                            'dense_input_all_entries_nonzero': all(x != 0 for t in dense.values() for x in t.values()),
                            'cp_branch_flip_check': 'PASS', 'odd_parity_zero_check': 'PASS',
                            **result})
            print(json.dumps(reports[-1]), flush=True)
            good += 1
            if good == 2:
                break
        assert good == 2
    arbitrary = arbitrary_pair_root_audit()
    output = {'scope': 'finite-field stage and ordinary Fisher/FKT only; no exact class recognizer or full CRT implementation',
              'novel_recognition_or_advantage_claim': False,
              'seconds': time.perf_counter()-started, 'checks': reports,
              'arbitrary_pair_square_root_audit': arbitrary}
    Path(__file__).with_name('FINITE_FIELD_CHECK.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({'seconds': output['seconds'], 'checks': len(reports)}))


if __name__ == '__main__':
    main()

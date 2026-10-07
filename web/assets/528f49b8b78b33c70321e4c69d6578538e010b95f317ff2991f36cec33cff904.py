"""Independent exact transcription checks for the permutation rank certificate.

These are falsification fixtures, not a proof of the infinite quantifiers or
incidence/geometry construction. No source check script is imported.
"""
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
import html
import hashlib
import json
import random

ROOT = Path(__file__).resolve().parents[2]
rng = random.Random(706521)
counts = {}


def rank(a, p=None):
    a = [[Fraction(x) if p is None else x % p for x in row] for row in a]
    if not a:
        return 0
    n = len(a)
    k = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(k, n) if a[i][j]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        if p is None:
            inv = 1 / a[k][j]
        else:
            inv = pow(a[k][j], -1, p)
        a[k] = [x * inv if p is None else x * inv % p for x in a[k]]
        for i in range(k + 1, n):
            c = a[i][j]
            if c:
                a[i] = [x - c * y if p is None else (x - c * y) % p
                        for x, y in zip(a[i], a[k])]
        k += 1
        if k == n:
            break
    return k


def pm(p):
    return [[int(p[j] == i) for j in range(len(p))] for i in range(len(p))]


def compose(a, b):
    return tuple(a[b[j]] for j in range(len(a)))


def inverse(a):
    b = [0] * len(a)
    for j, x in enumerate(a):
        b[x] = j
    return tuple(b)


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def blocks(x):
    r = len(x)
    d = len(x[0][0])
    return [[int(x[u][v][j] == i) for v in range(r) for j in range(d)]
            for u in range(r) for i in range(d)]


def test_array(x, ps):
    r, d = len(x), len(x[0][0])
    y = blocks(x)
    yt = [list(row) for row in zip(*y)]
    t = mm(y, yt)
    m1 = sum(t[i][i] for i in range(r*d))
    m2 = sum(t[i][j] * t[j][i] for i in range(r*d) for j in range(r*d))
    degenerate = 2*r**3-r**2
    nondegenerate_fixed = []
    all_fixed = 0
    for u, up, v, vp in product(range(r), repeat=4):
        w = compose(compose(compose(x[u][v], inverse(x[up][v])), x[up][vp]), inverse(x[u][vp]))
        fixed = sum(j == w[j] for j in range(d))
        all_fixed += fixed
        if u != up and v != vp:
            nondegenerate_fixed.append(fixed)
        else:
            assert fixed == d
    lam = Fraction(max(nondegenerate_fixed), d)
    assert m1 == r*r*d and m2 == all_fixed
    assert m2 <= (degenerate + r*r*(r-1)**2*lam)*d
    dr = rank(y)
    assert dr*m2 >= m1*m1
    assert dr >= Fraction(r*r*d, 1) / (2*r-1+(r-1)**2*lam)
    for p in ps:
        assert p > r
        dp = rank(y, p)
        assert 2*dp >= dr
        assert dp >= Fraction(r*r*d, 2) / (2*r-1+(r-1)**2*lam)
    counts['trace_rank_arrays'] = counts.get('trace_rank_arrays', 0) + 1
    counts['field_rank_checks'] = counts.get('field_rank_checks', 0) + len(ps)


def source_match():
    out = {}
    for sid in ['d-5f4f3b352980d250', 'd-62bae00c7f29762c']:
        hp = ROOT / 'work/astra-research-knowledge/web/pages' / (sid + '.html')
        mp = ROOT / 'work/scouts/groups_sources' / (sid + '.md')
        raw = hp.read_text()
        extracted = html.unescape(raw.split('<pre>', 1)[1].split('</pre>', 1)[0])
        md = mp.read_text()
        assert extracted == md
        out[sid] = hashlib.sha256(md.encode()).hexdigest()
    return out


def check_local_block(r, d, s, t, p, perturb):
    assert s >= r and t >= r and p > r
    pp = list(permutations(range(d)))
    ls = [[rng.choice(pp) for j in range(s)] for u in range(r)]
    rs = [[rng.choice(pp) for k in range(t)] for v in range(r)]
    # Intentionally noncommuting permutations, with shifts independently applied.
    xs = []
    errors = 0
    for alpha, beta in product(range(s), range(t)):
        x = [[compose(inverse(ls[u][(alpha+v) % s]), rs[v][(beta+u) % t])
              for v in range(r)] for u in range(r)]
        for u, v in product(range(r), repeat=2):
            exact = x[u][v]
            if rng.random() < perturb:
                x[u][v] = rng.choice(pp)
            errors += sum(a != b for a, b in zip(x[u][v], exact))
        xs.append(x)
    z = [[0] * (r*d) for i in range(r*d)]
    for x in xs:
        z = add(z, blocks(x))
    left = []
    for u in range(r):
        a = [[0]*d for i in range(d)]
        for j in range(s):
            a = add(a, pm(inverse(ls[u][j])))
        left.extend(a)
    right = []
    rb = []
    for v in range(r):
        a = [[0]*d for i in range(d)]
        for k in range(t):
            a = add(a, pm(rs[v][k]))
        rb.append(a)
    right = [[a[i][j] for a in rb for j in range(d)] for i in range(d)]
    model = mm(left, right)
    diff = [[x-y for x, y in zip(a, b)] for a, b in zip(z, model)]
    assert rank(model, p) <= d
    assert rank(diff, p) <= errors
    assert rank(z, p) <= d+errors
    if not errors:
        assert z == model
    counts['cartesian_blocks'] = counts.get('cartesian_blocks', 0) + 1


def lagrange(x, a, s, p):
    y = 1
    for b in s:
        if b != a:
            y = y * (x-b) * pow((a-b) % p, -1, p) % p
    return y


def check_interpolation(p, h, s):
    assert 2*h*(len(s)-1) < p-1
    marks = list(product(s, repeat=h))
    marks = [a for a in marks if rng.random() < .8]
    if not marks:
        marks = [tuple([s[0]]*h)]
    n = len(marks)
    pts = list(product(range(p), repeat=h))
    hv = {}
    for z in pts:
        f = []
        for a in marks:
            v = 1
            for zt, at in zip(z, a):
                v = v*lagrange(zt, at, s, p) % p
            f.append(v)
        hv[z] = [[a*b % p for b in f] for a in f]
        assert rank(hv[z], p) <= 1
    lines = []
    for i, a in enumerate(marks):
        direction = tuple(rng.randrange(p) for t in range(h))
        while not any(direction):
            direction = tuple(rng.randrange(p) for t in range(h))
        line = [tuple((at+t*dt) % p for at, dt in zip(a, direction)) for t in range(1, p)]
        sums = [[sum(hv[z][j][k] for z in line) % p for k in range(n)] for j in range(n)]
        expected = [[(-int(j == i and k == i)) % p for k in range(n)] for j in range(n)]
        assert sums == expected
        lines.append(line)
    # Check the tensor identity on arbitrary matrices, including no permutation
    # or representation assumptions at all, before invoking rank estimates.
    b = 3
    ys = [[[rng.randrange(p) for j in range(b)] for k in range(b)] for i in range(n)]
    rhs = [[0] * (n*b) for j in range(n*b)]
    for z in pts:
        iz = [i for i, line in enumerate(lines) if z in line]
        zz = [[sum(ys[i][j][k] for i in iz) % p for k in range(b)] for j in range(b)]
        for i, ip, j, k in product(range(n), range(n), range(b), range(b)):
            rhs[i*b+j][ip*b+k] = (rhs[i*b+j][ip*b+k]+hv[z][i][ip]*zz[j][k]) % p
    lhs = [[(-ys[i//b][i%b][j%b] if i//b == j//b else 0) % p
            for j in range(n*b)] for i in range(n*b)]
    assert lhs == rhs
    counts['interpolation_lines'] = counts.get('interpolation_lines', 0) + n
    counts['tensor_identities'] = counts.get('tensor_identities', 0) + 1


hashes = source_match()
for r, d, ps in [(2, 2, [3]), (2, 3, [3, 5]), (3, 2, [5])]:
    pp = list(permutations(range(d)))
    for flat in product(pp, repeat=r*r):
        test_array([list(flat[u*r:(u+1)*r]) for u in range(r)], ps)
for r, d, ps, trials in [(3, 3, [5], 100), (3, 5, [5], 80), (4, 5, [5, 7], 80)]:
    pp = list(permutations(range(d)))
    for _ in range(trials):
        test_array([[rng.choice(pp) for v in range(r)] for u in range(r)], ps)
for r, d, s, t, p in [(2, 3, 2, 3, 3), (3, 5, 3, 4, 5), (4, 5, 5, 4, 5)]:
    for perturb in [0, .02, .2, 1]:
        for _ in range(12):
            check_local_block(r, d, s, t, p, perturb)
for _ in range(12):
    check_interpolation(7, 2, [0, 2])
    check_interpolation(11, 2, [0, 2, 3])

# The linear lower estimate with independently varied rectangle defect.
for r in [2, 3, 5, 100, 10**42]:
    for lam in [Fraction(0), Fraction(1, 10**12), Fraction(1, 100), Fraction(1, 2), Fraction(1)]:
        alpha = Fraction(r*r, 2) / (2*r-1+(r-1)**2*lam)
        assert alpha >= Fraction(r, 4)-Fraction(r*r, 8)*lam
counts['alpha_inequalities'] = 25

# Necessary boundaries: interpolation at degree q-1, and lost row sparsity.
assert sum(pow(t, 2, 3) for t in range(3)) % 3 != 0
assert rank([[3, 0], [0, 3]]) == 2 and rank([[3, 0], [0, 3]], 3) == 0
counts['negative_controls'] = 2
out = {'status': 'PASS', 'counts': counts, 'source_markdown_sha256': hashes,
       'scope': 'Exact finite transcription checks only; incidence and geometry not audited.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))

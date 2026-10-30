"""Independent formula and completeness audit of s10's rank-two certificate.

Does not import the producer implementation.  Uses an analytic inverse for A
and a direct row formula for L.  The producer JSON supplies the proposed
representative blocks and polynomial certificates, all reconstructed here.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import time
import sympy as sp

t = sp.Symbol('t', real=True, nonnegative=True)
z = sp.Symbol('z')
N = 1+t*t
D = t**4+4*t*t+1
DEN = 4*N*D*(t*t+2)*(2*t*t+1)


def schmidt(a):
    return sp.Integer(1) if a == 0 else t if a == 1 else sp.Integer(0)


@lru_cache(None)
def lrow(a, b, c, d):
    """Nonzero coefficients of <cd|L_ab, independently expanded by hand."""
    out = defaultdict(lambda: sp.Integer(0))
    if a == b:
        out[c, d] += schmidt(a)
    if c == a:
        out[b, d] -= schmidt(b)/2
    if d == b:
        out[c, a] -= schmidt(a)/2
    if (c, d) == (a, b):
        out[0, 0] += sp.Rational(1, 4)
        out[1, 1] += t/4
    return {k: sp.expand(v) for k, v in out.items() if v != 0}


def ai(i, j):
    """Exact entries of the analytic inverse A^{-1}; no matrix inversion."""
    if i in ((0, 0), (1, 1)) and j in ((0, 0), (1, 1)):
        if i != j:
            return -t/D
        return (t*t+4)/D if i == (0, 0) else (4*t*t+1)/D
    if i != j:
        return sp.Integer(0)
    a, b = i
    return 1/(N-(schmidt(a)**2+schmidt(b)**2)/2)


def c_entry(row, col):
    a, b, c, d = row
    e, f, g, h = col
    # C = I - F_A/2 - F_B/2 + F_A F_B/4.
    return (sp.Integer(row == col)
            -sp.Rational(int((c, b, a, d) == col), 2)
            -sp.Rational(int((a, d, c, b) == col), 2)
            +sp.Rational(int((c, d, a, b) == col), 4))


@lru_cache(None)
def s_entry(row, col):
    a, b, c, d = row
    e, f, g, h = col
    x = lrow(e, f, c, d)
    y = lrow(a, b, g, h)
    return sp.cancel(sum(v*ai(i, j)*w for i, v in x.items() for j, w in y.items()))


def phase(row, p=4, q=4):
    # Characters of U_A x U_B fixing |00>+t|11>.
    a, b, c, d = row
    v = [0]*(p+q-2)
    for k in (a, c):
        v[k] += 1
    for k in (b, d):
        v[k if k < 2 else p+k-2] += -1 if k < 2 else 1
    return tuple(v)


def matrix_pair(labels):
    return (sp.Matrix([[c_entry(r, c) for c in labels] for r in labels]),
            sp.Matrix([[s_entry(r, c) for c in labels] for r in labels]))


def certify_polynomial_nonnegative(f):
    f = sp.Poly(f, t)
    if all(c >= 0 for c in f.all_coeffs()):
        return 'expanded_nonnegative_coefficients'
    # A real polynomial raised to an even power is nonnegative on the line.
    c, factors = sp.factor_list(f.as_expr(), t)
    if c >= 0 and all(k % 2 == 0 or all(v >= 0 for v in sp.Poly(p, t).all_coeffs())
                      for p, k in factors):
        return 'even_powers_and_nonnegative_coefficients'
    raise AssertionError('No elementary positivity certificate for '+str(f))


def main():
    start = time.perf_counter()
    source = Path(__file__).parents[1]/'s10_foundation_compute'/'rank2_p4_q4.json'
    raw = source.read_bytes()
    data = json.loads(raw)
    groups = defaultdict(list)
    for row in product(range(4), repeat=4):
        groups[phase(row)].append(row)
    assert len(groups) == 84 and sum(map(len, groups.values())) == 256
    assert max(map(len, groups.values())) == 8

    templates = {}
    certificate_rows = []
    coefficient_count = 0
    for record in data['blocks']:
        labels = [tuple(a+b) for a, b in record['representative_labels']]
        C, S = matrix_pair(labels)
        assert C == C.T and S == S.T
        templates[tuple(C)+tuple(S)] = record['index']
        results = {}
        for name, H in [('C_minus_S', DEN*(C-S)),
                        ('S_plus_11C_over9', DEN*(9*S+11*C))]:
            H = H.applyfunc(sp.cancel)
            assert all(not sp.denom(v).has(t) for v in H)
            # Substitute -z into det(zI-H) to obtain det(zI+H).
            cp = sp.Poly(H.charpoly(z).as_expr().subs(z, -z)*(-1)**H.rows, z)
            coefficients = cp.all_coeffs()
            claims = record[name]['det_zI_plus_H_coefficients']
            assert len(coefficients) == len(claims)
            modes = []
            for actual, claim in zip(coefficients, claims):
                alleged = sp.sympify(claim['factor'], locals={'t': t})
                assert sp.expand(actual-alleged) == 0
                modes.append(certify_polynomial_nonnegative(actual))
                coefficient_count += 1
            results[name] = modes
        certificate_rows.append({'producer_index': record['index'],
                                 'dimension': len(labels), 'coefficient_audit': results})

    covered = []
    for weight, labels in groups.items():
        C, S = matrix_pair(labels)
        signature = tuple(C)+tuple(S)
        assert signature in templates
        covered.append(templates[signature])
    assert len(templates) == 23

    # Check absent-phase couplings identically in t, independently of the
    # covariance proof in AUDIT.txt. This is a formula sanity check only.
    mismatches = []
    basis = list(product(range(4), repeat=4))
    for row in basis:
        for col in basis:
            if phase(row) != phase(col):
                if c_entry(row, col) != 0 or s_entry(row, col) != 0:
                    mismatches.append((row, col))
    assert not mismatches

    out = {
        'status': 'INDEPENDENT_EXACT_FORMULA_AND_CERTIFICATE_AUDIT_PASSED',
        'scope': 'All p,q>=2 and nonzero references of bipartite Schmidt rank<=2',
        'conclusion': '-11*C/9 <= S <= C',
        'producer_json': str(source),
        'producer_sha256': hashlib.sha256(raw).hexdigest(),
        'analytic_A_inverse_used': True,
        'producer_python_imported': False,
        'total_phase_blocks': len(groups),
        'distinct_matrix_pairs': len(templates),
        'maximum_block_dimension': max(map(len, groups.values())),
        'coefficients_reconstructed_and_certified': coefficient_count,
        'symbolic_offblock_entries_nonzero': len(mismatches),
        'ambient_completeness': 'Analytic proof in AUDIT.txt; 4x4 is a template bound, not a dimension sample',
        'certificate_rows': certificate_rows,
        'elapsed_code_seconds': time.perf_counter()-start,
        'inference_tokens': 'UNKNOWN', 'cost': 'UNKNOWN', 'energy': 'UNKNOWN',
    }
    path = Path(__file__).with_name('rank2_independent_audit.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'certificate_rows'}, indent=2))


if __name__ == '__main__':
    main()

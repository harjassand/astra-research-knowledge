"""Root's independent exact common-cone review, using SymPy QQ polynomials.

No acquisition model, author verifier, saved interface matrix, or numerical
nullspace is imported. All energy, jet, exterior-derivative and moment maps
are assembled here from literal definitions.
"""
from itertools import combinations, combinations_with_replacement as cw
from pathlib import Path
import hashlib
import json
import time
import sympy as s

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'quartic_alternative/combined_full_cone'
QQ = s.QQ
a = s.symbols('a b c d', real=True)
x = s.symbols('x0:4', real=True)
y = s.symbols('y0:6', real=True)
pcvars = a + x
hvars = a + y
pairs4 = list(cw(range(4), 2))
pairs6 = list(cw(range(6), 2))


def inv(z):
    aa, b, c, d = z
    return aa**2 + c**2, b**2 + d**2, aa*b + c*d, aa*d - b*c


def basis(z):
    u, v, w, q = inv(z)
    return [u**2, v**2, u*v, w**2, u*w, v*w, q*u, q*v, q*w]


def poly(expr, variables):
    return s.Poly(expr, *variables, domain=QQ)


def field(value):
    return QQ.from_sympy(s.Rational(value))


def exact_ldl(matrix, supplied=None):
    """Fresh LDL followed by a full entrywise reconstruction, exact in QQ."""
    n = len(matrix)
    assert all(matrix[i][j] == matrix[j][i]
               for i in range(n) for j in range(n))
    lower = [[QQ.one if i == j else QQ.zero for j in range(n)]
             for i in range(n)]
    pivots = []
    for j in range(n):
        d = matrix[j][j] - sum((lower[j][k]**2*pivots[k]
                               for k in range(j)), QQ.zero)
        assert d > 0, (j, d)
        pivots.append(d)
        for i in range(j+1, n):
            lower[i][j] = (matrix[i][j] - sum(
                (lower[i][k]*lower[j][k]*pivots[k] for k in range(j)),
                QQ.zero)) / d
    assert all(matrix[i][j] == sum(
        (lower[i][k]*pivots[k]*lower[j][k] for k in range(n)), QQ.zero)
        for i in range(n) for j in range(n))
    if supplied is not None:
        assert pivots == [field(d) for d in supplied]
    return pivots


def main():
    start = time.monotonic()
    common_raw = (SOURCE / 'EXACT_COMMON_SEPARATOR.json').read_bytes()
    roc_raw = (SOURCE / 'heat_normal_extreme_ROC.json').read_bytes()
    data, roc = json.loads(common_raw), json.loads(roc_raw)
    pcvalues = dict(zip(map(tuple, data['PC_monomial_order']),
                        map(field, data['PC_lambda'])))
    assert len(pcvalues) == 658

    def pc(expr):
        pp = expr if isinstance(expr, s.Poly) else poly(expr, pcvars)
        assert set(pp.monoms()) <= set(pcvalues)
        return sum((field(c)*pcvalues[e] for e, c in pp.terms()), QQ.zero)

    zp = [poly(ai*x[j]*x[k], pcvars) for ai in a for j, k in pairs4]
    zp += [poly(x[i]*x[j]*x[k], pcvars) for i, j, k in cw(range(4), 3)]
    assert len(zp) == 60
    span = {e for p in zp for q in zp for e in (p*q).monoms()}
    assert span == set(pcvalues)
    dp = exact_ldl([[pc(p*q) for q in zp] for p in zp],
                   data['PC_positive_LDL_pivots'])
    nx, dx = sum(t*t for t in x), inv(x)[3]
    selectors = [pc(nx*a[i]*a[j]*dx) for i, j in pairs4]
    assert selectors == [QQ.zero]*10

    hmonomials = [poly(a[i]*a[j]*y[k]*y[l], hvars)
                  for i, j in pairs4 for k, l in pairs6]
    hvalues = {p.monoms()[0]: field(v)
               for p, v in zip(hmonomials, data['heat_lambda'])}
    assert len(hvalues) == 210

    def heat(expr):
        pp = expr if isinstance(expr, s.Poly) else poly(expr, hvars)
        assert set(pp.monoms()) <= set(hvalues)
        return sum((field(c)*hvalues[e] for e, c in pp.terms()), QQ.zero)

    zh = [poly(ai*bj, hvars) for ai in a for bj in y]
    dh = exact_ldl([[heat(p*q) for q in zh] for p in zh],
                   data['heat_positive_LDL_pivots'])
    j1 = (y[0], y[1], y[3], y[4])
    j2 = (y[1], y[2], y[4], y[5])
    eta = [field(v) for v in data['closedness_dual_eta']]
    triples = list(combinations(range(4), 3))
    assert len(eta) == 16
    # A basis of ALL quadratic two-forms, not merely a supplied closed basis.
    closure_rows = []
    for i, j in combinations(range(4), 2):
        for k, l in pairs4:
            coeff = a[k]*a[l]

            def omega(u, v):
                return coeff if (u, v) == (i, j) else (
                    -coeff if (v, u) == (i, j) else s.S.Zero)

            dform = [poly(s.diff(omega(v, w), a[u])
                          - s.diff(omega(u, w), a[v])
                          + s.diff(omega(u, v), a[w]), a)
                     for u, v, w in triples]
            column = [field(p.coeff_monomial(ai))
                      for p in dform for ai in a]
            closure_rows.append(column)
            pullback = coeff*(j1[i]*j2[j] - j1[j]*j2[i])
            assert heat(pullback) == sum(
                (v*w for v, w in zip(eta, column)), QQ.zero)
    assert len(closure_rows) == 60
    closure_rank = s.Matrix(closure_rows).rank()
    assert closure_rank == 15  # Full closed space therefore has dimension 45.

    shifted = dict(zip(a, (ai+xi for ai, xi in zip(a, x))))
    gp, gh, acoustic = [], [], []
    for f in basis(a):
        breg = f.xreplace(shifted) - f - sum(
            s.diff(f, ai)*xi for ai, xi in zip(a, x))
        gp.append(pc(nx*breg))
        hess = s.hessian(f, a)
        diss = (s.Matrix(j1).T*hess*s.Matrix(j1))[0] + (
            s.Matrix(j2).T*hess*s.Matrix(j2))[0]
        gh.append(heat(diss))
        aa = s.hessian(s.diff(f, a[0], 2), a)/2
        ab = s.hessian(s.diff(f, a[0], a[1]), a)/2
        bb = s.hessian(s.diff(f, a[1], 2), a)/2
        acoustic.append(s.BlockMatrix([[aa, ab], [ab, bb]]).as_explicit())
    assert gp == gh == [field(v) for v in data['shared_energy_normal']]
    p = [field(v) for v in data['target_coefficients']]
    pairing = sum((v*w for v, w in zip(gp, p)), QQ.zero)
    assert pairing == field(data['target_pairing']) < 0
    assert gp[2] - gp[3] > 0
    assert p == [field(v) for v in roc['coefficients']]
    canonical = sum((s.Rational(str(p[k]))*acoustic[k]
                     for k in range(9)), s.zeros(8))
    q = s.Matrix([[s.Rational(v) for v in row] for row in roc['matrix']])
    sk = s.zeros(4)
    for (i, j), v in zip(combinations(range(4), 2), roc['skew_parameters']):
        sk[i, j], sk[j, i] = s.Rational(v), -s.Rational(v)
    assert q == canonical + s.BlockMatrix(
        [[s.zeros(4), sk], [-sk, s.zeros(4)]]).as_explicit()
    # The skew block contributes zero to the literal rank-one row test.
    z = s.Matrix([y[0]*ai for ai in a] + [y[1]*ai for ai in a])
    f = sum(s.Rational(str(pk))*fk for pk, fk in zip(p, basis(a)))
    rank_one_curvature = (y[0]**2*s.diff(f, a[0], 2)
                          + 2*y[0]*y[1]*s.diff(f, a[0], a[1])
                          + y[1]**2*s.diff(f, a[1], 2))
    assert poly((z.T*q*z)[0] - rank_one_curvature, hvars).is_zero
    rho = field(roc['positive_shift'])
    assert rho == QQ(1, 200000)
    dr = exact_ldl([[field(q[i, j]) - (rho if i == j else QQ.zero)
                     for j in range(8)] for i in range(8)],
                   roc['shifted_LDL_pivots'])
    acoustic_l1 = sum((abs(field(v)) for m in acoustic for v in m), QQ.zero)
    normal_l1 = sum(map(abs, gp), QQ.zero)
    radius = min(rho/(2*acoustic_l1), -pairing/(2*normal_l1))
    assert acoustic_l1 == 132 and radius == QQ(1, 52800000)

    # A new exact point restores the discrete symmetries: L=-M exactly.
    even = p.copy()
    even[6], even[7] = (p[6]-p[7])/2, (p[7]-p[6])/2
    changes = [even[i]-p[i] for i in range(9)]
    assert max(map(abs, changes)) == QQ(1, 20000000000) < radius
    even_pairing = sum((v*w for v, w in zip(gp, even)), QQ.zero)
    assert even_pairing < 0
    even_q = q + sum((s.Rational(str(changes[k]))*acoustic[k]
                      for k in range(9)), s.zeros(8))
    even_rho = QQ(1, 400000)
    de = exact_ldl([[field(even_q[i, j]) - (
        even_rho if i == j else QQ.zero) for j in range(8)] for i in range(8)])
    # Check the two discrete symmetries from literal quartic expressions.
    ef = sum(s.Rational(str(pk))*fk for pk, fk in zip(even, basis(a)))
    column_swap = dict(zip(a, (a[1], a[0], a[3], a[2])))
    paired_reflection = dict(zip(a, (a[0], -a[1], -a[2], a[3])))
    assert poly(ef.xreplace(column_swap)-ef, a).is_zero
    assert poly(ef.xreplace(paired_reflection)-ef, a).is_zero
    projected = {'status': 'EXACT_SYMMETRIC_STRICT_ROC_COMMON_SEPARATOR',
                 'basis': ['u2', 'v2', 'uv', 'w2', 'uw', 'vw', 'qu', 'qv', 'qw'],
                 'coefficients': list(map(str, even)),
                 'pairing': str(even_pairing),
                 'ROC_matrix': [[str(v) for v in row] for row in even_q.tolist()],
                 'ROC_shift': str(even_rho),
                 'shifted_LDL_pivots': list(map(str, de)),
                 'discrete_symmetries': ['COLUMN_SWAP', 'PAIRED_ROW_COLUMN_REFLECTION'],
                 'inherits_common_dual_sha256': hashlib.sha256(common_raw).hexdigest()}
    (ROOT / 'EXACT_SYMMETRIC_TARGET.json').write_text(json.dumps(projected, indent=2)+'\n')
    receipt = {
        'status': 'ROOT_INDEPENDENT_EXACT_COMMON_CONE_REVIEW_PASS',
        'common_sha256': hashlib.sha256(common_raw).hexdigest(),
        'ROC_sha256': hashlib.sha256(roc_raw).hexdigest(),
        'engine': 'SymPy QQ exact polynomial and rational arithmetic; no author imports',
        'PC_moment_positive_pivots': len(dp),
        'heat_moment_positive_pivots': len(dh),
        'ROC_positive_shifted_pivots': len(dr),
        'all_quadratic_selector_annihilators': list(map(str, selectors)),
        'full_exterior_derivative_basis_columns': len(closure_rows),
        'exterior_derivative_rank': closure_rank,
        'shared_energy_pairings': list(map(str, gp)),
        'strict_negative_target_pairing': str(pairing),
        'full9_coefficient_box_radius': str(radius),
        'symmetric_target_pairing': str(even_pairing),
        'symmetric_target_ROC_shift': str(even_rho),
        'seconds': time.monotonic()-start,
        'scope': 'Strict ROC; exclusion from the sum of norm-level1 PC support and identity-diffusion closed quadratic two-form/bilinear SOS heat classes. No non-PC or non-QC claim.'}
    (ROOT / 'INDEPENDENT_COMMON_REPLAY.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()

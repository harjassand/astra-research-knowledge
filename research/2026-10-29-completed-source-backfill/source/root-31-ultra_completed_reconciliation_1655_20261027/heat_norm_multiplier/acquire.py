"""One complementary heat operation: norm-A multiplied pointwise dissipation.

Exact literal maps are generated independently of the earlier heat interface.
Numerical acquisitions below do not establish a positive or negative theorem.
"""
from pathlib import Path
from itertools import combinations, combinations_with_replacement as cw
import json
import time
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
import sympy as s
import numpy as np
import scipy.sparse as sp
import cvxpy as cp

ROOT = Path(__file__).resolve().parent
a = s.symbols('a b c d')
y = s.symbols('y0:6')
variables = a+y
pa = list(cw(range(4), 2))
py = list(cw(range(6), 2))
j1 = s.Matrix([y[0], y[1], y[3], y[4]])
j2 = s.Matrix([y[1], y[2], y[4], y[5]])


def basis():
    aa, b, c, d = a
    u, v, w, q = aa**2+c**2, b**2+d**2, aa*b+c*d, aa*d-b*c
    return [u*u, v*v, u*v, w*w, u*w, v*w, q*u, q*v, q*w]


def exponent(indices):
    out = [0]*10
    for i in indices:
        out[i] += 1
    return tuple(out)


def build():
    start = time.monotonic()
    rows = [exponent(ai+tuple(4+j for j in yi))
            for ai in cw(range(4), 4) for yi in py]
    index = {e: i for i, e in enumerate(rows)}
    assert len(rows) == 735
    norm = sum(ai*ai for ai in a)
    forms, columns = [], []
    triples = list(combinations(range(4), 3))
    for i, j in combinations(range(4), 2):
        for k, l in pa:
            coeff = a[k]*a[l]

            def omega(u, v):
                return coeff if (u, v) == (i, j) else (
                    -coeff if (v, u) == (i, j) else s.S.Zero)

            closure = [s.Poly(s.diff(omega(v, w), a[u])
                              - s.diff(omega(u, w), a[v])
                              + s.diff(omega(u, v), a[w]), *a)
                       for u, v, w in triples]
            columns.append([p.coeff_monomial(ai) for p in closure for ai in a])
            forms.append(coeff*(j1[i]*j2[j]-j1[j]*j2[i]))
    closure = s.Matrix(columns).T
    nullbasis = closure.nullspace()
    assert closure.rank() == 15 and len(nullbasis) == 45
    ns = s.Matrix.hstack(*nullbasis)
    assert closure*ns == s.zeros(16, 45)

    def vector(expr):
        out = np.zeros(735)
        for e, c in s.Poly(expr, *variables, domain=s.QQ).terms():
            if c:
                out[index[e]] = float(c)
        return out

    pullback = np.stack([vector(norm*f) for f in forms], axis=1)
    o = pullback @ np.array(ns, dtype=float)
    energy = []
    for f in basis():
        h = s.hessian(f, a)
        energy.append(vector(norm*((j1.T*h*j1)[0]+(j2.T*h*j2)[0])))
    e = np.stack(energy, axis=1)
    features = [exponent((i, j, 4+k)) for i, j in pa for k in range(6)]
    rr, cc, vv = [], [], []
    sr, sc, sv = [], [], []
    for col, (i, j) in enumerate(cw(range(60), 2)):
        power = tuple(v+w for v, w in zip(features[i], features[j]))
        rr.append(index[power]); cc.append(col); vv.append(1 if i == j else 2)
        sr.append(i*60+j); sc.append(col); sv.append(1)
        if i != j:
            sr.append(j*60+i); sc.append(col); sv.append(1)
    gram = sp.coo_matrix((vv, (rr, cc)), shape=(735, 1830)).tocsr()
    sym = sp.coo_matrix((sv, (sr, sc)), shape=(3600, 1830)).tocsr()
    assert set(rr) == set(range(735))
    # These coefficients and nullspace are exact integers or halves.
    assert np.array_equal(2*o, np.rint(2*o))
    assert np.array_equal(e, np.rint(e))
    np.savez(ROOT/'LITERAL_MAPS.npz', E=e, O=o, N=np.array(ns, dtype=float),
             C=np.array(closure, dtype=np.int64), exponents=np.array(rows),
             features=np.array(features), gram_rows=rr, gram_cols=cc, gram_values=vv)
    (ROOT/'INTERFACE.json').write_text(json.dumps({
        'construction': 'NORM_A_SQUARED_TIMES_IDENTITY_HEAT_DISSIPATION_PLUS_CLOSED_FORM',
        'features': 60, 'coefficient_equations': 735,
        'closed_form_variables': 45, 'full_closure_rank': 15,
        'map_engine': 'SymPy exact literal derivatives and rational nullspace',
        'seconds': time.monotonic()-start}, indent=2)+'\n')
    return e, o, gram, sym


def main():
    e, o, gram, sym = build()
    q = cp.Variable(1830)
    omega = cp.Variable(45)
    rho = cp.Variable()
    p = cp.Parameter(9)
    matrix = cp.reshape(sym@q, (60, 60), order='C')
    equality = gram@q - o@omega == e@p
    problem = cp.Problem(cp.Maximize(rho), [equality, matrix-rho*np.eye(60) >> 0, rho <= 1])
    control = [1, 1, 2, 0, 0, 0, -2.2, -2.2, 0]
    target_raw = (ROOT.parent/'common_cone_review/EXACT_SYMMETRIC_TARGET.json').read_bytes()
    target = json.loads(target_raw)
    targets = [('DM_control', control), ('symmetric_target', [float(s.Rational(v)) for v in target['coefficients']])]
    results = []
    for name, value in targets:
        start = time.monotonic()
        p.value = value
        problem.solve(solver='CLARABEL', max_iter=180, tol_gap_abs=1e-9,
                      tol_gap_rel=1e-9, tol_feas=1e-9)
        out = {'name': name, 'status': 'NUMERICAL_ACQUISITION_ONLY',
               'solver_status': problem.status,
               'margin': None if rho.value is None else float(rho.value),
               'seconds': time.monotonic()-start,
               'max_affine_residual': None if q.value is None else float(np.max(np.abs(equality.violation()))),
               'scope': 'No positive theorem or class infeasibility without exact reconstruction.'}
        if q.value is not None:
            np.savez(ROOT/(name+'.npz'), q=q.value, omega=omega.value,
                     equality_dual=equality.dual_value, rho=rho.value)
        (ROOT/(name+'.json')).write_text(json.dumps(out, indent=2)+'\n')
        results.append(out)
        print(json.dumps(out), flush=True)
    (ROOT/'ACQUISITIONS.json').write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()

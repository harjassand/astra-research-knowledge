"""Ordinary bounds and noncommuting multistart search; no claim of novelty.

Run with /usr/local/bin/python3. Output is written only when main is called.
Upper bounds are rationally checked. Optimizer values are numerical diagnostics,
not certified global maxima. Physical state preparation is outside this task.
"""
from pathlib import Path
import json
import math
import sys
import numpy as np
import sympy as sp
from scipy.linalg import eigh
from scipy.optimize import minimize


def mm(a, b):
    return np.einsum('ij,jk->ik', a, b, optimize=False)


def channel(raw):
    return np.array([[float(sp.Rational(x)) for x in row] for row in raw])


def exact(raw):
    return sp.Matrix([[sp.Rational(x) for x in row] for row in raw])


def form(k, qs):
    n, d = len(qs), len(qs[0])
    b = np.vstack([np.eye(n-1), -np.ones((1, n-1))])
    out = np.zeros(((n-1)*d, (n-1)*d), complex)
    for row in k:
        w = sum(row[i]*qs[i] for i in range(n))
        a = row @ b
        out += np.kron(np.outer(a, a), np.linalg.inv(w))
    return (out + out.conj().T)/2


def quotient(k, l, qs):
    fk, fl = form(k, qs), form(l, qs)
    vals, vecs = eigh(fk, fl, check_finite=True)
    return float(vals[-1]), vecs[:, -1]


def hermitian(v, d):
    h = np.diag(v[:d]).astype(complex)
    pos = d
    for i in range(d):
        for j in range(i):
            h[i, j] = v[pos] + 1j*v[pos+1]
            h[j, i] = h[i, j].conjugate()
            pos += 2
    return h


def effects(v, n, d):
    es = []
    for i in range(n):
        h = hermitian(v[i*d*d:(i+1)*d*d], d)
        ev, uu = np.linalg.eigh(h)
        es.append(mm(uu*np.exp(ev), uu.conj().T))
    ev, uu = np.linalg.eigh(sum(es))
    if min(ev) <= 0:
        raise ValueError('nonpositive normalization')
    inv = mm(uu*(ev**-.5), uu.conj().T)
    return [mm(mm(inv, e), inv) for e in es]


def ordinary_search(k, l, d=3, starts=5, maxiter=90, seed=41026):
    n = k.shape[1]
    rng = np.random.default_rng(seed)
    best = None
    for s in range(starts):
        x0 = np.zeros(n*d*d) if s == 0 else rng.normal(0, 1.5, n*d*d)
        def loss(v):
            try:
                val, _ = quotient(k, l, effects(v, n, d))
                return -val if math.isfinite(val) else 1e8
            except (ValueError, np.linalg.LinAlgError):
                return 1e8
        fit = minimize(loss, x0, method='L-BFGS-B', bounds=[(-7, 7)]*len(x0),
                       options={'maxiter': maxiter, 'ftol': 1e-11, 'maxls': 35})
        qs = effects(fit.x, n, d)
        value, vec = quotient(k, l, qs)
        row = {'value': value, 'optimizer_success': bool(fit.success),
               'message': str(fit.message), 'evaluations': int(fit.nfev),
               'effects_real': [x.real.tolist() for x in qs],
               'effects_imag': [x.imag.tolist() for x in qs],
               'u_free_real': vec.real.tolist(), 'u_free_imag': vec.imag.tolist()}
        if best is None or value > best['value']:
            best = row
    return best


def psd2(a):
    return a[0, 0] >= 0 and a[1, 1] >= 0 and a.det() >= 0


def ordinary_upper(kraw, lraw):
    k, l = exact(kraw), exact(lraw)
    b = sp.Matrix([[1, 0], [0, 1], [-1, -1]])
    if k == l:
        return {'upper': '1', 'reason': 'identical channels'}
    if all(k[:, i] == k[:, 0] for i in range(1, 3)):
        return {'upper': '0', 'reason': 'constant channel'}
    # min_i row_i <= W_row <= max_i row_i, with sum(Q_i)=I.
    # These scalar bounds imply FK <= U tensor I and FL >= V tensor I.
    u = b.T*k.T*sp.diag(*[1/min(k.row(y)) for y in range(k.rows)])*k*b
    v = b.T*l.T*sp.diag(*[1/max(l.row(y)) for y in range(l.rows)])*l*b
    assert v[0, 0] > 0 and v.det() > 0
    cfloat = float(eigh(np.array(u).astype(float), np.array(v).astype(float),
                       eigvals_only=True)[-1])
    c = sp.Rational(math.ceil(cfloat*1000000)+1, 1000000)
    assert psd2(c*v-u)
    choices = [(c, 'rational matrix bound', {'U': str(u), 'V': str(v),
                                           'PSD_minor_certificate': [str(x) for x in [(c*v-u)[0,0], (c*v-u)[1,1], (c*v-u).det()]]})]
    if l.det() != 0:
        t = k*l.inv()
        if all(x >= 0 for x in t):
            delta = sum(min(t.row(y)) for y in range(t.rows))
            # T=delta replacer+(1-delta)T'; positivity of the output
            # inverse forms and data processing give FK <= (1-delta)FL.
            choices.append((1-delta, 'exact stochastic degradation/Doeblin bound', {'T': str(t), 'delta': str(delta)}))
            off = t[0, 1]
            lam = t[0, 0]-off
            if 0 <= lam <= 1 and all(t[i,j] == (lam if i == j else 0)+off for i in range(3) for j in range(3)):
                # Q_i <= I implies lam^2(lam Q_i+b I)^-1
                # <= [lam^2/(lam+b)] Q_i^-1, term by term.
                if lam+off > 0:
                    choices.append((lam**2/(lam+off), 'uniform reset operator bound', {'lambda': str(lam), 'b': str(off)}))
    c, reason, cert = min(choices, key=lambda x: x[0])
    return {'upper': str(c), 'reason': reason, 'certificate': cert}


def run_case(case, starts=5, maxiter=90):
    k, l = channel(case['K']), channel(case['L'])
    numeric = ordinary_search(k, l, starts=starts, maxiter=maxiter)
    scalar = ordinary_search(k, l, d=1, starts=starts, maxiter=maxiter)
    upper = ordinary_upper(case['K'], case['L'])
    assert numeric['value'] <= float(sp.Rational(upper['upper'])) + 1e-7
    return {'id': case['id'], 'ordinary_upper': upper,
            'noncommuting_search': numeric, 'scalar_search': scalar,
            'warning': 'Search values are numerical lower candidates, not certified global bounds or exact state witnesses.'}


if __name__ == '__main__':
    p = Path(sys.argv[1])
    cases = json.loads(p.read_text())['cases']
    starts = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    maxiter = int(sys.argv[3]) if len(sys.argv) > 3 else 90
    results = []
    for c in cases:
        r = run_case(c, starts=starts, maxiter=maxiter)
        results.append(r)
        print(json.dumps({'id': r['id'], 'search': r['noncommuting_search']['value'],
                          'scalar': r['scalar_search']['value'],
                          'upper': r['ordinary_upper']['upper']}), flush=True)
    Path('BASELINE_RESULTS.json').write_text(json.dumps({'results': results,
        'scope': 'Ordinary bounds plus numerical searches. No global optimizer or new discovery claimed.'}, indent=2)+'\n')

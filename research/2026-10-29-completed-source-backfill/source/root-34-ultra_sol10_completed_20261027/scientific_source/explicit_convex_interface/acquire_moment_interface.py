"""Literal order-two moment evaluator, with exact rational value brackets.

Established moment/SOS machinery, applied to the accepted rational-selector
quartic. No numerical PSD/solver status is a proof premise. The consumer below
rounds both sides, corrects affine equations, mixes with exact interior points,
and checks all PSD matrices by Fraction LDL. Sources are read-only.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations_with_replacement
from pathlib import Path
from functools import lru_cache
import json
import math
import time

import cvxpy as cp
import numpy as np
import sympy as sp

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
OLD = ROOT / 'work/sol8_opportunity_selection_20261027/rational_selector'
DEN = 1 << 40
ZERO = (0, 0, 0, 0)


def exponent(indices):
    ans = [0] * 4
    for i in indices:
        ans[i] += 1
    return tuple(ans)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


MOMS = [exponent(ii) for n in range(5)
        for ii in combinations_with_replacement(range(4), n)]
FEAT = [e for e in MOMS if sum(e) <= 2]
INDEX = {e: i for i, e in enumerate(MOMS)}
MIDX = np.array([[INDEX[add(e, f)] for f in FEAT] for e in FEAT])
assert len(MOMS) == 70 and len(FEAT) == 15
PICK = {}
for e in MOMS:
    choices = [(i, j) for i in range(15) for j in range(i, 15)
               if add(FEAT[i], FEAT[j]) == e]
    PICK[e] = max(choices, key=lambda ij: min(sum(FEAT[ij[0]]), sum(FEAT[ij[1]])))

a, b, c, d = sp.symbols('a b c d')
VARS = (a, b, c, d)
T = a*a + b*b + c*c + d*d
DET = a*d - b*c
u, v, w = a*a+c*c, b*b+d*d, a*b+c*d
p0, p2, p3, ell = (sp.Rational(55220381, 10**10),
                  sp.Rational(114430029, 625000000),
                  -sp.Rational(801761987, 5000000000),
                  sp.Rational(118849817, 4000000000))
F = p0*(u*u+v*v)+p2*u*v+p3*w*w+ell*DET*(u-v)


def literal_coeff(poly):
    return {e: Q(int(v.p), int(v.q))
            for e, v in sp.Poly(poly, *VARS, domain=sp.QQ).terms()}


FCOEFF = literal_coeff(F)
NCOEFF = literal_coeff(T*T)
TCOEFF = literal_coeff(T)
QCOEFF = literal_coeff(DET)


def qfloat(x):
    assert math.isfinite(float(x))
    return Q(round(float(x)*DEN), DEN)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), Q(0))


def matrix_coeff(mat):
    ans = {e: Q(0) for e in MOMS}
    for i in range(15):
        for j in range(i, 15):
            ans[add(FEAT[i], FEAT[j])] += mat[i][j]*(1 if i == j else 2)
    return ans


def ldl_positive(mat):
    """Strict positivity; exact Fraction pivots, no eigenvalue premise."""
    n = len(mat)
    low = [[Q(0) for j in range(n)] for i in range(n)]
    pivots = []
    for i in range(n):
        pivot = mat[i][i] - sum((low[i][k]**2*pivots[k] for k in range(i)), Q(0))
        if pivot <= 0:
            return None
        pivots.append(pivot)
        low[i][i] = 1
        for j in range(i+1, n):
            low[j][i] = (mat[j][i] - sum(
                (low[j][k]*low[i][k]*pivots[k] for k in range(i)), Q(0)))/pivot
    return pivots


def exact_gram():
    raw = json.loads((OLD/'EXACT_RATIONAL_SUPPORT.json').read_text())
    denom = int(raw['gram_denominator'])
    # First of the ten A-pairs is (0,0). Its ten X-pairs occupy 80:90.
    g = [[Q(raw['gram_integer_matrix'][80+i][80+j], denom)
          for j in range(10)] for i in range(10)]
    full = [[Q(0) for j in range(15)] for i in range(15)]
    for i in range(10):
        for j in range(10):
            full[5+i][5+j] = g[i][j]
    assert {e: v for e, v in matrix_coeff(full).items() if v} == FCOEFF
    shifted = [[g[i][j] - (Q(1, 400000) if i == j else 0)
                for j in range(10)] for i in range(10)]
    assert ldl_positive(shifted) is not None
    return g


GRAMF = exact_gram()


def interior_gram(eps, model):
    mat = [[Q(0) for j in range(15)] for i in range(15)]
    mat[0][0] = 1
    for i in range(1, 5):
        mat[i][i] = eps
    if model == 'old_F':
        g = GRAMF
    else:
        # Sum squares of the ten quadratic monomials: norm^4 has weights 1,2.
        g = [[Q(0) for j in range(10)] for i in range(10)]
        for i, e in enumerate(FEAT[5:]):
            g[i][i] = 1 if 2 in e else 2
    for i in range(10):
        for j in range(10):
            mat[5+i][5+j] = g[i][j]
    assert ldl_positive(mat) is not None
    return mat


def gaussian_moments(mean, target_det):
    """Full-support rational Gaussian, matched to all six affine constraints."""
    detmean = mean[0]*mean[3] - mean[1]*mean[2]
    gap = target_det-detmean
    radius = abs(gap)+1
    cov = [[radius if i == j else Q(0) for j in range(4)] for i in range(4)]
    cov[0][3] = cov[3][0] = gap/2
    cov[1][2] = cov[2][1] = -gap/2
    assert ldl_positive(cov) is not None

    @lru_cache(None)
    def centered(ii):
        if not ii:
            return Q(1)
        if len(ii) % 2:
            return Q(0)
        return sum((cov[ii[0]][ii[k]]*centered(ii[1:k]+ii[k+1:])
                    for k in range(1, len(ii))), Q(0))

    def raw(e):
        ii = tuple(i for i, n in enumerate(e) for _ in range(n))
        ans = Q(0)
        for mask in range(1 << len(ii)):
            ci = tuple(ii[j] for j in range(len(ii)) if mask & (1 << j))
            prod = math.prod(mean[ii[j]] for j in range(len(ii))
                             if not mask & (1 << j))
            ans += prod*centered(ci)
        return ans

    yy = [raw(e) for e in MOMS]
    assert yy[0] == 1
    assert [yy[INDEX[exponent((i,))]] for i in range(4)] == mean
    assert dot([QCOEFF.get(e, Q(0)) for e in MOMS], yy) == target_det
    assert ldl_positive([[yy[k] for k in row] for row in MIDX]) is not None
    return yy


def moment_matrix(yy):
    return [[yy[int(k)] for k in row] for row in MIDX]


def mixing_weights():
    # First successful weight is accepted only after exact positive LDL.
    yield Q(0)
    for n in range(14, -1, -1):
        yield Q(1, 10**n)


def repair_primal(y_numeric, mean, target_det):
    yy = [qfloat(t) for t in y_numeric]
    yy[0] = Q(1)
    for i in range(4):
        yy[INDEX[exponent((i,))]] = mean[i]
    ad, bc = INDEX[(1,0,0,1)], INDEX[(0,1,1,0)]
    yy[ad] = target_det+yy[bc]
    safe = gaussian_moments(mean, target_det)
    for theta in mixing_weights():
        mix = [(1-theta)*x+theta*z for x, z in zip(yy, safe)]
        pivots = ldl_positive(moment_matrix(mix))
        if pivots is not None:
            return mix, theta, pivots
    raise AssertionError('interior primal unexpectedly failed')


def repair_dual(q_numeric, multipliers, coeff, eps, model):
    # lambda = minus CVXPY equality multiplier, by its Lagrangian convention.
    lam = [-qfloat(t) for t in multipliers]
    mat = [[qfloat((q_numeric[i,j]+q_numeric[j,i])/2) for j in range(15)]
           for i in range(15)]
    target = [coeff.get(e, Q(0)) for e in MOMS]
    target[0] -= lam[0]
    for i in range(4):
        target[INDEX[exponent((i,))]] -= lam[1+i]
    for e, val in QCOEFF.items():
        target[INDEX[e]] -= lam[5]*val
    actual = matrix_coeff(mat)
    corrections = []
    for e, value in zip(MOMS, target):
        residual = value-actual[e]
        corrections.append(abs(residual))
        i, j = PICK[e]
        if i == j:
            mat[i][i] += residual
        else:
            mat[i][j] += residual/2
            mat[j][i] += residual/2
    assert list(matrix_coeff(mat).values()) == target
    safe = interior_gram(eps, model)
    safe_lam = [Q(-1)] + [Q(0)]*5
    for theta in mixing_weights():
        mix = [[(1-theta)*mat[i][j]+theta*safe[i][j] for j in range(15)]
               for i in range(15)]
        pivots = ldl_positive(mix)
        if pivots is not None:
            ll = [(1-theta)*x+theta*z for x, z in zip(lam, safe_lam)]
            check = [coeff.get(e, Q(0)) for e in MOMS]
            check[0] -= ll[0]
            for i in range(4):
                check[INDEX[exponent((i,))]] -= ll[1+i]
            for e, value in QCOEFF.items():
                check[INDEX[e]] -= ll[5]*value
            assert list(matrix_coeff(mix).values()) == check
            return ll, mix, theta, pivots, max(corrections)
    raise AssertionError('interior dual unexpectedly failed')


def query_scale(mean, target_det, eps):
    magnitude = max(max(map(abs, map(float, mean))), math.sqrt(abs(float(target_det))),
                    math.sqrt(float(eps)))
    k = math.floor(math.log2(magnitude)) if magnitude else 0
    return Q(2**k) if k >= 0 else Q(1, 2**(-k))


class Program:
    def __init__(self, model):
        self.model = model
        self.y = cp.Variable(70)
        self.bb = cp.Parameter(4)
        self.ss = cp.Parameter()
        self.eps = cp.Parameter(nonneg=True)
        self.mm = cp.bmat([[self.y[int(k)] for k in row] for row in MIDX])
        base = FCOEFF if model == 'old_F' else NCOEFF
        self.base = np.array([float(base.get(e, Q(0))) for e in MOMS])
        self.tc = np.array([float(TCOEFF.get(e, Q(0))) for e in MOMS])
        self.qc = np.array([float(QCOEFF.get(e, Q(0))) for e in MOMS])
        self.constraints = [self.mm >> 0, self.y[0] == 1]
        self.constraints += [self.y[INDEX[exponent((i,))]] == self.bb[i] for i in range(4)]
        self.constraints += [self.qc @ self.y == self.ss]
        self.problem = cp.Problem(cp.Minimize((self.base+self.eps*self.tc) @ self.y),
                                  self.constraints)

    def solve(self, label, mean, target_det, eps):
        started = time.monotonic()
        scale = query_scale(mean, target_det, eps)
        bb = [x/scale for x in mean]
        ss, ee = target_det/scale**2, eps/scale**2
        self.bb.value, self.ss.value, self.eps.value = list(map(float, bb)), float(ss), float(ee)
        solver_start = time.monotonic()
        val = self.problem.solve(solver='CLARABEL', tol_gap_abs=1e-10,
                                 tol_gap_rel=1e-10, tol_feas=1e-10,
                                 max_iter=250, warm_start=False, verbose=False)
        solver_wall = time.monotonic()-solver_start
        assert self.y.value is not None
        ynum = np.asarray(self.y.value)
        qnum = self.constraints[0].dual_value
        multipliers = [float(cc.dual_value) for cc in self.constraints[1:]]
        base = FCOEFF if self.model == 'old_F' else NCOEFF
        coeff = {e: base.get(e, Q(0))+ee*TCOEFF.get(e, Q(0)) for e in MOMS}
        exact_start = time.monotonic()
        yy, ptheta, pp = repair_primal(ynum, bb, ss)
        lam, gram, dtheta, dp, affine_error = repair_dual(qnum, multipliers, coeff, ee, self.model)
        upper = dot([coeff[e] for e in MOMS], yy)*scale**4
        lower = dot(lam, [Q(1)]+bb+[ss])*scale**4
        assert lower <= upper
        exact_wall = time.monotonic()-exact_start
        eigs = np.linalg.eigvalsh(np.asarray(moment_matrix(yy), dtype=float))
        gram_eigs = np.linalg.eigvalsh(np.asarray(gram, dtype=float))
        # Save sufficient exact data for a consumer which never runs a solver.
        cert = {'scale':str(scale), 'mean_scaled':list(map(str, bb)),
                'det_scaled':str(ss), 'eps_scaled':str(ee),
                'primal_moments':list(map(str, yy)),
                'dual_lambda':list(map(str, lam)),
                'dual_gram':[[str(x) for x in row] for row in gram]}
        path = OUT/'certificates'/f'{self.model}_{label}.json'
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(cert, indent=2)+'\n')
        out = {'label':label, 'model':self.model, 'B':list(map(str, mean)), 's':str(target_det),
               'epsilon':str(eps), 'scale':str(scale), 'lower':str(lower), 'upper':str(upper),
               'display_lower':float(lower), 'display_upper':float(upper),
               'display_width':float(upper-lower), 'primal_mix':str(ptheta),
               'dual_mix':str(dtheta), 'max_affine_Gram_correction':str(affine_error),
               'solver_status_diagnostic':self.problem.status, 'solver_value_diagnostic':val*float(scale**4),
               'solver_iterations':self.problem.solver_stats.num_iters,
               'solver_wall_seconds':solver_wall, 'exact_repair_seconds':exact_wall,
               'total_seconds':time.monotonic()-started,
               'primal_min_pivot':str(min(pp)), 'dual_min_pivot':str(min(dp)),
               'numeric_primal_eigen_range_diagnostic':[float(eigs[0]),float(eigs[-1])],
               'numeric_dual_eigen_range_diagnostic':[float(gram_eigs[0]),float(gram_eigs[-1])],
               'certificate_path':str(path.relative_to(OUT))}
        return out


def main():
    started = time.monotonic()
    eps = Q(1,100)
    queries = [
        ('origin', [Q(0)]*4, Q(0)),
        ('graph_diag', [Q(1),Q(0),Q(0),Q(3,4)], Q(3,4)),
        ('graph_generic', [Q(3,5),Q(-1,5),Q(3,10),Q(9,10)], Q(3,5)),
        ('slice_001', [Q(0)]*4, Q(1,100)),
        ('slice_01', [Q(0)]*4, Q(1,10)),
        ('slice_1', [Q(0)]*4, Q(1)),
        ('slice_neg1', [Q(0)]*4, Q(-1)),
        ('off_diag_up', [Q(1),Q(0),Q(0),Q(3,4)], Q(5,4)),
        ('off_diag_down', [Q(1),Q(0),Q(0),Q(3,4)], Q(1,4)),
        ('off_generic_up', [Q(3,5),Q(-1,5),Q(3,10),Q(9,10)], Q(11,10)),
        ('off_generic_negative', [Q(3,5),Q(-1,5),Q(3,10),Q(9,10)], Q(-2,5)),
    ]
    rows = []
    for model in ['old_F', 'norm4_control']:
        prog = Program(model)
        for label, mean, det in queries:
            row = prog.solve(label, mean, det, eps)
            rows.append(row)
            (OUT/'MOMENT_EVALUATIONS.json').write_text(json.dumps(
                {'status':'PARTIAL_EXACT_BRACKETS', 'rows':rows}, indent=2)+'\n')
            print(json.dumps({k:row[k] for k in ['label','model','display_lower',
                             'display_upper','display_width','solver_status_diagnostic',
                             'solver_iterations','total_seconds']}), flush=True)
    result = {'status':'EXACT_FINITE_SDP_VALUE_BRACKETS', 'variables':70,
              'PSD_size':15, 'equalities':6, 'rounding_denominator':DEN,
              'rows':rows, 'full_acquisition_seconds':time.monotonic()-started,
              'scope':'Exact rational feasible primal/dual brackets, including solver and repair costs. '
              'Finite convex lift; not globally smooth and not a certificate for the newer non-PC quartic.'}
    (OUT/'MOMENT_EVALUATIONS.json').write_text(json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    main()

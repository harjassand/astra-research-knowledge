"""A base-point denominator rather than an increment norm hierarchy.

Search |A|² B_F(A,X) - K4(A) detX = Z80.T Q Z80, Q PSD.
For A!=0 this gives a rational homogeneous minor-support selector.
All 35 quartic K4 coefficients are allowed. Numerical results only.
"""
from itertools import combinations_with_replacement as cw
from pathlib import Path
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
a = s.symbols('a0:4')
x = s.symbols('x0:4')
variables = a+x


def exp_indices(ai, xi):
    e = [0]*8
    for i in ai:
        e[i] += 1
    for i in xi:
        e[4+i] += 1
    return tuple(e)


def basis(z):
    aa, b, c, d = z
    u, v, w, q = aa*aa+c*c, b*b+d*d, aa*b+c*d, aa*d-b*c
    return [u*u, v*v, u*v, w*w, u*w, v*w, q*u, q*v, q*w]


def build():
    start = time.monotonic()
    rows = [exp_indices(ai,xi) for da in (4,3,2)
            for ai in cw(range(4),da) for xi in cw(range(4),6-da)]
    lookup = {e:i for i,e in enumerate(rows)}
    assert len(rows) == len(lookup) == 1100
    z = [exp_indices(ai,(k,)) for ai in cw(range(4),2) for k in range(4)]
    z += [exp_indices((i,),xi) for i in range(4) for xi in cw(range(4),2)]
    assert len(z) == len(set(z)) == 80
    gr, gc, gv, sr, sc, sv = [], [], [], [], [], []
    for col,(i,j) in enumerate(cw(range(80),2)):
        power = tuple(v+w for v,w in zip(z[i],z[j]))
        gr.append(lookup[power]);gc.append(col);gv.append(1 if i==j else 2)
        sr.append(i*80+j);sc.append(col);sv.append(1)
        if i!=j:
            sr.append(j*80+i);sc.append(col);sv.append(1)
    assert set(gr) == set(range(1100))
    gram = sp.coo_matrix((gv,(gr,gc)),shape=(1100,3240)).tocsr()
    sym = sp.coo_matrix((sv,(sr,sc)),shape=(6400,3240)).tocsr()

    def vector(expr):
        out = np.zeros(1100)
        for e,c in s.Poly(expr,*variables,domain=s.QQ).terms():
            if c:
                out[lookup[e]] = float(c)
        return out

    norm = sum(ai*ai for ai in a)
    shifted = dict(zip(a,(ai+xi for ai,xi in zip(a,x))))
    e = np.stack([vector(norm*(f.xreplace(shifted)-f-sum(
        s.diff(f,ai)*xi for ai,xi in zip(a,x)))) for f in basis(a)],axis=1)
    dx = x[0]*x[3]-x[1]*x[2]
    selectors = list(cw(range(4),4))
    c = np.stack([vector(s.prod(a[i] for i in indices)*dx)
                  for indices in selectors],axis=1)
    assert np.array_equal(e,np.rint(e)) and np.array_equal(c,np.rint(c))
    np.savez(ROOT/'LITERAL_MAPS.npz', E=e,C=c,exponents=np.array(rows),features=np.array(z),
             gram_rows=gr,gram_cols=gc,gram_values=gv,
             selector_indices=np.array(selectors))
    (ROOT/'INTERFACE.json').write_text(json.dumps({
        'operation':'RATIONAL_BASE_POINT_SELECTOR_K4_OVER_NORM_A_SQUARED',
        'features':80,'equations':1100,'selector_coefficients':35,
        'literal_map_engine':'SymPy exact rational polynomials; integer coefficients',
        'seconds':time.monotonic()-start},indent=2)+'\n')
    return e,c,gram,sym


def main():
    e,c,gram,sym = build()
    q = cp.Variable(3240)
    selector = cp.Variable(35)
    rho = cp.Variable()
    p = cp.Parameter(9)
    matrix = cp.reshape(sym@q,(80,80),order='C')
    equality = gram@q+c@selector == e@p
    problem = cp.Problem(cp.Maximize(rho),[equality,matrix-rho*np.eye(80)>>0,rho<=1])
    raw = (ROOT.parent/'common_cone_review/EXACT_SYMMETRIC_TARGET.json').read_bytes()
    target = json.loads(raw)
    tests = [('norm_control',[1,1,2,0,0,0,0,0,0]),
             ('symmetric_target',[float(s.Rational(v)) for v in target['coefficients']])]
    out = []
    for name,value in tests:
        start = time.monotonic();p.value=value
        problem.solve(solver='CLARABEL',max_iter=180,tol_gap_abs=1e-9,
                      tol_gap_rel=1e-9,tol_feas=1e-9)
        record={'name':name,'status':'NUMERICAL_ACQUISITION_ONLY',
                'solver_status':problem.status,
                'margin':None if rho.value is None else float(rho.value),
                'max_affine_residual':None if q.value is None else float(np.max(np.abs(equality.violation()))),
                'seconds':time.monotonic()-start,
                'scope':'No PC or infeasibility assertion without exact reconstruction.'}
        if q.value is not None:
            np.savez(ROOT/(name+'.npz'),q=q.value,selector=selector.value,
                     equality_dual=equality.dual_value,rho=rho.value)
        (ROOT/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
        out.append(record);print(json.dumps(record),flush=True)
    (ROOT/'ACQUISITIONS.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__ == '__main__':
    main()

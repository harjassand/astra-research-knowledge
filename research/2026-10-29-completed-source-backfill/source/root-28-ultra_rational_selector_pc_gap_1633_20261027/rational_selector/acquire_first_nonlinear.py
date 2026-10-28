"""First symmetry-allowed nonlinear rational selector on the symmetric target.

k(A)=p6(A)/|A|^4; p6 spans x³,x²z,xz²,z³,xy²,y²z in Hopf variables.
Search |A|^4 B_F-p6 detX SOS in all 180 A³X / A²X² monomials.
"""
from pathlib import Path
from itertools import combinations_with_replacement as cw
import json
import time
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import sympy as s
import numpy as np
import scipy.sparse as sp
import cvxpy as cp
from acquire import a,x,variables,exp_indices,basis

ROOT=Path(__file__).resolve().parent


def main():
    begin=time.monotonic()
    rows=[exp_indices(ai,xi) for da in (6,5,4)
          for ai in cw(range(4),da) for xi in cw(range(4),8-da)]
    lookup={e:i for i,e in enumerate(rows)}
    assert len(rows)==len(lookup)==3185
    features=[exp_indices(ai,(k,)) for ai in cw(range(4),3) for k in range(4)]
    features += [exp_indices(ai,xi) for ai in cw(range(4),2) for xi in cw(range(4),2)]
    assert len(features)==len(set(features))==180
    rr,cc,vv,sr,sc,sv=[],[],[],[],[],[]
    for col,(i,j) in enumerate(cw(range(180),2)):
        power=tuple(v+w for v,w in zip(features[i],features[j]))
        rr.append(lookup[power]);cc.append(col);vv.append(1 if i==j else 2)
        sr.append(i*180+j);sc.append(col);sv.append(1)
        if i!=j:
            sr.append(j*180+i);sc.append(col);sv.append(1)
    assert set(rr)==set(range(3185))
    gram=sp.coo_matrix((vv,(rr,cc)),shape=(3185,16290)).tocsr()
    sym=sp.coo_matrix((sv,(sr,sc)),shape=(32400,16290)).tocsr()
    def vec(expr):
        out=np.zeros(3185)
        for e,c in s.Poly(expr,*variables,domain=s.QQ).terms():
            if c:out[lookup[e]]=float(c)
        return out
    norm=sum(ai*ai for ai in a)
    replace=dict(zip(a,(ai+xi for ai,xi in zip(a,x))))
    e=np.stack([vec(norm**2*(f.xreplace(replace)-f-sum(
        s.diff(f,ai)*xi for ai,xi in zip(a,x)))) for f in basis(a)],axis=1)
    aa,b,c,d=a
    hx,hy,hz=aa*aa+c*c-b*b-d*d,2*(aa*b+c*d),2*(aa*d-b*c)
    selectors=[hx**3,hx**2*hz,hx*hz**2,hz**3,hx*hy**2,hy**2*hz]
    detx=x[0]*x[3]-x[1]*x[2]
    cmat=np.stack([vec(v*detx) for v in selectors],axis=1)
    assert np.array_equal(e,np.rint(e)) and np.array_equal(cmat,np.rint(cmat))
    np.savez(ROOT/'NONLINEAR_LITERAL_MAPS.npz',E=e,C=cmat,features=np.array(features),exponents=np.array(rows),gram_rows=rr,gram_cols=cc,gram_values=vv)
    (ROOT/'NONLINEAR_INTERFACE.json').write_text(json.dumps({
        'operation':'HOPF_CUBIC_NUMERATOR_OVER_NORM_A_FOURTH',
        'features':180,'equations':3185,'symmetry_complete_selector_coefficients':6,
        'selector_basis':['x3','x2z','xz2','z3','xy2','y2z'],
        'map_seconds':time.monotonic()-begin,
        'scope':'First genuinely nonlinear denominator degree allowed by the exact target symmetries; no completeness of this finite degree.'},indent=2)+'\n')
    qv=cp.Variable(16290);selector=cp.Variable(6);rho=cp.Variable();p=cp.Parameter(9)
    matrix=cp.reshape(sym@qv,(180,180),order='C')
    eq=gram@qv+cmat@selector==e@p
    problem=cp.Problem(cp.Maximize(rho),[eq,matrix-rho*np.eye(180)>>0,rho<=1])
    point=json.loads((ROOT.parent/'common_cone_review/EXACT_SYMMETRIC_TARGET.json').read_text())
    tests=[('nonlinear_norm_control',[1,1,2,0,0,0,0,0,0]),
           ('nonlinear_symmetric_target',[float(s.Rational(v)) for v in point['coefficients']])]
    results=[]
    for name,coeff in tests:
        start=time.monotonic();p.value=coeff
        problem.solve(solver='CLARABEL',max_iter=120,tol_gap_abs=1e-8,
                      tol_gap_rel=1e-8,tol_feas=1e-8)
        out={'name':name,'status':'NUMERICAL_ACQUISITION_ONLY',
             'solver_status':problem.status,'margin':None if rho.value is None else float(rho.value),
             'max_affine_residual':None if qv.value is None else float(np.max(abs(eq.violation()))),
             'seconds':time.monotonic()-start,
             'scope':'No PC or class infeasibility assertion without exact reconstruction.'}
        if qv.value is not None:
            np.savez(ROOT/(name+'.npz'),q=qv.value,selector=selector.value,
                     equality_dual=eq.dual_value,rho=rho.value)
        (ROOT/(name+'.json')).write_text(json.dumps(out,indent=2)+'\n')
        results.append(out);print(json.dumps(out),flush=True)
    (ROOT/'NONLINEAR_ACQUISITIONS.json').write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__':main()

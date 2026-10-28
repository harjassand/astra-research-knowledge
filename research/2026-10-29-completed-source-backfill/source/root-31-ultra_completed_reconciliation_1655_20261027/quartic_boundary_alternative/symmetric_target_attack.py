#!/usr/bin/env python3
"""Literal rational Hopf ROC check and direct global-support search.

The ROC test is exact. The opposite-determinant search is numerical acquisition
only; a negative must subsequently be rationalized and checked independently.
No SDP or certificate-cone test is used.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json, time, hashlib
import sympy as S
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'sol6_openings_20261027/independent_opening/vendor'))
from scipy.optimize import minimize, differential_evolution

H = np.array([
    [[2,0,0,0],[0,-2,0,0],[0,0,2,0],[0,0,0,-2]],
    [[0,2,0,0],[2,0,0,0],[0,0,0,2],[0,0,2,0]],
    [[0,0,0,2],[0,0,-2,0],[0,-2,0,0],[2,0,0,0]],
], dtype=float)

def main():
    started = time.perf_counter()
    source = HERE.parent / 'common_cone_review/EXACT_SYMMETRIC_TARGET.json'
    source_bytes = source.read_bytes()
    data = json.loads(source_bytes)
    p = list(map(S.Rational, data['coefficients']))
    assert p[0] == p[1] and p[4] == p[5] == p[8] == 0 and p[6] == -p[7]
    k1 = p[0]
    k2 = (p[0]+p[1]+p[2]+p[3])/4
    d = (p[6]-p[7])/8
    r = (p[0]+p[1]+p[2])/4
    s = S.Symbol('s', real=True)
    k = k2+(k1-k2)*s
    n11 = 2*k1*k2-k2*k2-(k1*k1-k2*k2+d*d)*s
    n22 = 2*k*r-k2*k2-(k1*k1-k2*k2+3*d*d)*s
    determinant = S.Poly(S.expand(n11*n22-4*d*d*k2*k2*(1-s)), s)
    assert k1 > 0 and k2 > 0 and n11.subs(s,0)>0 and n11.subs(s,1)>0
    a,b,c = determinant.all_coeffs()
    assert a > 0
    stationary = -b/(2*a)
    exact_minimum = min(determinant.eval(0),determinant.eval(1),
                        determinant.eval(stationary) if 0<stationary<1
                        else determinant.eval(0))
    assert exact_minimum > 0
    roc = {
        'status':'EXACT_STRICT_ROC_BY_EQUATORIAL_SCHUR_COMPLEMENT',
        'K_parameters':list(map(str,(k1,k2,d,r))),
        'K_parameters_float':list(map(float,(k1,k2,d,r))),
        'N11_endpoints':list(map(str,(n11.subs(s,0),n11.subs(s,1)))),
        'determinant_coefficients':list(map(str,determinant.all_coeffs())),
        'stationary_s':str(stationary),
        'determinant_minimum':str(exact_minimum),
        'determinant_minimum_float':float(exact_minimum),
    }
    K = np.array([[float(k1),0,float(d)],[0,float(k2),0],
                  [float(d),0,float(r)]]) / float(k1)

    def T(matrix):
        v = matrix.reshape(4)
        h = np.einsum('i,kij,j->k',v,H,v)/2
        J = np.einsum('kij,j->ki',H,v)
        kh = K@h
        f = h@kh
        return J.T@(K-np.outer(kh,kh)/f)@J+np.einsum('k,kij->ij',kh,H)

    def rotation(phi):
        c = np.cos(phi); s = np.sin(phi)
        return np.array([[c,-s],[s,c]])

    def matrices(x):
        s,t,phi,psi,theta=x
        rp=np.diag([np.exp(s),np.exp(-s)])@rotation(phi)
        rm=rotation(theta)@np.diag([np.exp(t),-np.exp(-t)])@rotation(psi)
        return rp,rm

    def objective(x):
        rp,rm=matrices(x)
        return np.linalg.eigvalsh(T(rp)+T(rm))[0]/(np.sum(rp*rp)+np.sum(rm*rm))

    rng=np.random.default_rng(281061)
    trials=[]
    for _ in range(5000):
        x=np.r_[rng.uniform(-3,3,2),rng.uniform(-np.pi,np.pi,3)]
        trials.append((float(objective(x)),x))
    trials.sort(key=lambda z:z[0])
    best=trials[0]
    refinements=[]
    bounds=[(-6,6),(-6,6)]+[(-np.pi,np.pi)]*3
    for _,x in trials[:24]:
        res=minimize(objective,x,method='L-BFGS-B',bounds=bounds,
                     options={'maxiter':180,'ftol':1e-14,'gtol':1e-10})
        refinements.append({'value':float(res.fun),'x':res.x.tolist(),
                            'success':bool(res.success)})
        if res.fun<best[0]: best=(float(res.fun),res.x.copy())
    de=differential_evolution(objective,bounds,seed=781,maxiter=120,
                              popsize=10,polish=True,tol=1e-9,workers=1)
    if de.fun<best[0]: best=(float(de.fun),de.x.copy())
    rp,rm=matrices(best[1])
    eig,vec=np.linalg.eigh(T(rp)+T(rm))
    out={'source_sha256':hashlib.sha256(source_bytes).hexdigest(),
         'source':str(source),'coefficients':list(map(str,p)),
         'ROC':roc,
         'support_search_status':'NUMERICAL_ACQUISITION_ONLY',
         'samples':5000,'local_refinements':24,
         'DE_evaluations':int(de.nfev),
         'best_normalized_eigenvalue':float(best[0]),
         'best_raw_eigenvalue':float(eig[0]),
         'best_parameters':best[1].tolist(),'Rp':rp.tolist(),'Rm':rm.tolist(),
         'candidate_A':vec[:,0].tolist(),'refinements':refinements,
         'elapsed_seconds':time.perf_counter()-started}
    (HERE/'SYMMETRIC_TARGET_ATTACK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='refinements'},indent=2))

if __name__=='__main__': main()

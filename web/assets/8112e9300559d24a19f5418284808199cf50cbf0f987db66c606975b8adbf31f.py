"""Exact new U2 thermal-character/gap and rank-two kernel distinction checks."""
from fractions import Fraction
import json
from pathlib import Path

import numpy as np

from check_cold_carrier import nodes


def det3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-
            a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+
            a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def schur(k,m,p):
    degree = k+m+2
    hh = {n:sum((p[0]**a*p[1]**b*p[2]**(n-a-b)
                 for a in range(n+1) for b in range(n-a+1)),Fraction(0))
          for n in range(degree+1)}
    lam = [k+m,m,0]
    return det3([[hh.get(lam[i]-i+j,Fraction(0)) for j in range(3)]
                 for i in range(3)])


def scalar_cases():
    rows = []
    count = 0
    for k,m in ((0,1),(1,0),(1,1),(2,2),(4,3),(8,4),(16,8)):
        for p in ((Fraction(1,2),Fraction(1,3),Fraction(1,6)),
                  (Fraction(2,5),Fraction(2,5),Fraction(1,5)),
                  (Fraction(9,10),Fraction(9,100),Fraction(1,100))):
            q,q1,q2 = p[1]/p[0],p[2]/p[0],p[2]/p[1]
            def f(l):
                return sum((q**i for i in range(l+1)),Fraction(0))/(l+1)
            zz = schur(k,m,p)
            w = p[0]**(k+m)*p[1]**m/zz
            c0 = w*f(k)
            mass = Fraction(0)
            layer = {}
            dims = 0
            for s in range(k+1):
                for t in range(m+1):
                    n,ell = s+t,k+t-s
                    c = c0*q1**s*q2**t*f(ell)/f(k)
                    assert c <= c0*q2**n
                    assert c <= w
                    mass += (ell+1)*c
                    dims += ell+1
                    layer[n] = layer.get(n,0)+ell+1
                    count += 1
            assert mass == 1
            assert dims == (k+1)*(m+1)*(k+m+2)//2
            assert all(g <= (k+1)*(n+1) for n,g in layer.items())
            w0 = (k+1)*c0
            assert w0 >= (1-q2)**2
            coefficient = (k+1)*c0**2/w*(1-q2)**2
            assert coefficient == (1-q2)**2*w0*f(k)
            assert coefficient >= (1-q2)**4*f(k)
            assert f(k) >= 1/(1+(k+1)*(1-q))
            rows.append({'k':k,'m':m,'p':[str(x) for x in p],
                         'vacuum_weight':float(w0),'score_coefficient':float(coefficient),
                         'coefficient_lower':float((1-q2)**4*f(k))})
    return count,rows


def kernel_case():
    d,r = 3,2
    ss = np.zeros((9,9),complex)
    tt = np.zeros((9,9),complex)
    for v,w in nodes(1):
        line = np.outer(v,v.conj())
        pp = np.eye(3)-line
        vec = pp.ravel(order='F')
        ss += d/r*w*np.kron(pp.T,pp)
        tt += d/r**2*w*np.outer(vec,vec.conj())
    ident = np.eye(3).ravel(order='F')
    pred_s = 5/8*np.eye(9)+1/8*np.outer(ident,ident)
    pred_t = 1/16*np.eye(9)+5/16*np.outer(ident,ident)
    s_error = float(np.linalg.norm(ss-pred_s))
    t_error = float(np.linalg.norm(tt-pred_t))
    assert s_error < 1e-12 and t_error < 1e-12
    def energy(a):
        av = a.ravel(order='F')
        return float(np.vdot(av,(np.eye(9)-ss)@av).real)
    rng = np.random.default_rng(1072)
    for rank in (1,2,3):
        f = np.diag([1/np.sqrt(rank)]*rank+[0]*(3-rank))
        assert abs(energy(f)-(3-rank)/8) < 1e-12
        for _ in range(5):
            a = ((rng.normal(size=(3,rank))+1j*rng.normal(size=(3,rank)))@
                 (rng.normal(size=(rank,3))+1j*rng.normal(size=(rank,3))))
            a /= np.linalg.norm(a,'fro')
            u,s,vh = np.linalg.svd(a)
            right = (vh.conj().T*s)@vh
            left = (u*s)@u.conj().T
            assert energy(a) >= (energy(right)+energy(left))/2-1e-12
            assert energy(a) >= (3-rank)/8-1e-12
    return {'d':d,'r':r,'sandwich_traceless':5/8,'frame_traceless':1/16,
            'sandwich_formula_error':s_error,'frame_formula_error':t_error,
            'positive_modulus_fixtures':15,'toy_capacity':{'Q1':1/4,'Q2':1/8,'Q3':0}}


def main():
    count,rows = scalar_cases()
    result = {'status':'FINITE-EVIDENCE',
              'scope':'Exact Jacobi-Trudi versus U2 component characters/gaps, normalized score coefficients, and one rank-two sandwich/frame counterexample only',
              'component_cases':count,'scalar_cases':rows,'kernel_case':kernel_case(),
              'old_suites_rerun':False,'uniform_iid_external_or_novelty_validation':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v if k!='scalar_cases' else len(v) for k,v in result.items()},indent=2))


if __name__ == '__main__':
    main()

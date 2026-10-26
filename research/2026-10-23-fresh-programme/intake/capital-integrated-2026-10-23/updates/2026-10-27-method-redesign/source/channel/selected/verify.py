"""Independent exact rational verifier for evaluator certificates.

No numerical eigensolver or optimizer is used here. See PROOF.md for the universal
operator identities proved by the three small PSD tests.
"""
import json
import sys
from pathlib import Path
import sympy as s


def mat(raw): return s.Matrix([[s.Rational(x) for x in row] for row in raw])
def serial(m): return [[str(m[i,j]) for j in range(m.cols)] for i in range(m.rows)]
def psd(m):
    assert m==m.T
    if m.rows==1:return m[0,0]>=0
    if m.rows==2:return m[0,0]>=0 and m[1,1]>=0 and m.det()>=0
    raise ValueError('verifier supports witness dimensions one and two')
def pd(m):
    return psd(m) and m.det()>0

def data(case):
    k,l=mat(case['K']),mat(case['L'])
    assert k.shape==l.shape==(3,3)
    assert all(a>0 for a in list(k)+list(l))
    assert all(sum(k[:,i])==sum(l[:,i])==1 for i in range(3))
    assert l.det()!=0
    b=s.Matrix([[1,0],[0,1],[-1,-1]])
    p=s.Matrix([[1,0,0],[0,1,0]])
    r=p*l.inv(); e=[s.Matrix([1,0]),s.Matrix([0,1]),s.zeros(2,1)]
    ml=[r*s.diag(*list(l[:,i]))*r.T for i in range(3)]
    d=p*k*b; x=[p*k[:,i] for i in range(3)]
    ti=[s.diag(*list(a))-a*a.T for a in x]
    si=[d*(ml[i]-e[i]*e[i].T)*d.T for i in range(3)]
    return k,l,x,ti,si

def upper_check(case, cert):
    k,l,x,ti,si=data(case);c=s.Rational(cert['c'])
    assert c>=0
    if cert['regime']=='vertex':
        assert c>=1
        bs=[c*ti[i]-si[i] for i in range(3)]
    elif cert['regime']=='subunit':
        assert c<1
        z=s.Matrix([s.Rational(v) for v in cert['z']])
        bs=[c*ti[i]-si[i]-(1-c)*(z-x[i])*(z-x[i]).T for i in range(3)]
    elif cert['regime']=='constant':
        assert c==0 and all(k[:,i]==k[:,0] for i in range(1,3))
        return c,[]
    else: raise ValueError('unknown certificate regime')
    assert all(psd(a) for a in bs),'rational upper PSD check failed'
    return c,bs

def lower_check(case,witness):
    k,l,*_=data(case)
    es=[mat(a) for a in witness['effects_unnormalized']]
    h=[s.Matrix([s.Rational(a) for a in row]) for row in witness['vectors_unnormalized']]
    assert len(es)==len(h)==3 and len({a.shape for a in es})==1
    d=es[0].rows
    assert d in (1,2) and es[0].cols==d
    assert all(a.shape==(d,1) for a in h)
    assert all(psd(a) for a in es)
    g=sum(es,s.zeros(d)); assert pd(g)
    assert sum(h,s.zeros(d,1))==s.zeros(d,1)
    def form(a):
        out=s.Rational(0)
        for y in range(3):
            ey=sum((a[y,i]*es[i] for i in range(3)),s.zeros(d))
            hy=sum((a[y,i]*h[i] for i in range(3)),s.zeros(d,1))
            assert pd(ey)
            out+=(hy.T*ey.inv()*hy)[0]
        return out
    fk,fl=form(k),form(l)
    assert fl>0 and fk>=0
    return fk/fl,fk,fl

def verify(case,result):
    up,bs=upper_check(case,result['upper_certificate'])
    low,fk,fl=lower_check(case,result['lower_witness'])
    assert low==s.Rational(result['lower'])
    assert up==s.Rational(result['upper'])
    assert low<=up
    return {'verified':True,'lower':str(low),'upper':str(up),
            'lower_float':float(low),'upper_float':float(up),
            'width':float(up-low),
            'endpoint_pass':bool(up-low <= s.Rational(1,50)*max(s.Rational(1),low)),
            'upper_principal_minors':[[str(a[0,0]),str(a[1,1]),str(a.det())] for a in bs],
            'F_K_witness':str(fk),'F_L_witness':str(fl)}

if __name__=='__main__':
    inp=json.loads(Path(sys.argv[1]).read_text())
    if 'cases' in inp:
        out=json.loads(Path(sys.argv[2]).read_text())
        results=out['results']
        print(json.dumps([{'id':c.get('id'),**verify(c,r)} for c,r in zip(inp['cases'],results)],indent=2))
    else:
        print(json.dumps(verify(inp,json.loads(Path(sys.argv[2]).read_text())),indent=2))

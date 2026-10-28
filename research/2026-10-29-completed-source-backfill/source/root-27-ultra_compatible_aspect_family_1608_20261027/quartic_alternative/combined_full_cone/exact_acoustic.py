"""Exact acoustic acquisition plus separate literal stdlib-only verification."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,time,argparse
N=6
def clean(p):return {e:c for e,c in p.items() if c}
def add(*ps):
    z={}
    for p in ps:
        for e,c in p.items():z[e]=z.get(e,F(0))+c
    return clean(z)
def scale(p,c):return clean({e:v*c for e,v in p.items()})
def mul(p,q):
    z={}
    for e,c in p.items():
        for f,d in q.items():
            g=tuple(i+j for i,j in zip(e,f));z[g]=z.get(g,F(0))+c*d
    return clean(z)
def var(i):
    e=[0]*N;e[i]=1;return {tuple(e):F(1)}
def diff(p,i):
    z={}
    for e,c in p.items():
        if e[i]:
            g=list(e);g[i]-=1;z[tuple(g)]=c*e[i]
    return z
def ldl(A):
    n=len(A);L=[[F(i==j) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        d=A[j][j]-sum(L[j][k]**2*D[k] for k in range(j));assert d>0,(j,d);D.append(d)
        for i in range(j+1,n):L[i][j]=(A[i][j]-sum(L[i][k]*D[k]*L[j][k] for k in range(j)))/d
    assert all(A[i][j]==sum(L[i][k]*D[k]*L[j][k] for k in range(n)) for i in range(n) for j in range(n))
    return D
def verify(path):
    start=time.monotonic();raw=Path(path).read_bytes();r=json.loads(raw)
    a,b,c,d=[var(i) for i in range(4)];s,t=var(4),var(5)
    u=add(mul(a,a),mul(c,c));v=add(mul(b,b),mul(d,d));w=add(mul(a,b),mul(c,d));q=add(mul(a,d),scale(mul(b,c),-1))
    bases=[mul(u,u),mul(v,v),mul(u,v),mul(w,w),mul(u,w),mul(v,w),mul(q,u),mul(q,v),mul(q,w)]
    f=add(*(scale(p,F(x)) for p,x in zip(bases,r['coefficients'])))
    target=add(mul(mul(s,s),diff(diff(f,0),0)),scale(mul(mul(s,t),diff(diff(f,0),1)),2),mul(mul(t,t),diff(diff(f,1),1)))
    features=[mul(s,x) for x in [a,b,c,d]]+[mul(t,x) for x in [a,b,c,d]]
    Q=[[F(x) for x in row] for row in r['matrix']]
    assert len(Q)==8 and all(len(row)==8 for row in Q) and all(Q[i][j]==Q[j][i] for i in range(8) for j in range(8))
    rebuilt=add(*(scale(mul(features[i],features[j]),Q[i][j]*(1 if i==j else 2)) for i in range(8) for j in range(i,8)))
    assert target==rebuilt
    rho=F(r['positive_shift']);assert rho>0
    D=ldl([[Q[i][j]-(rho if i==j else 0) for j in range(8)] for i in range(8)])
    assert D==list(map(F,r['shifted_LDL_pivots']))
    return {'status':'EXACT_STRICT_ROC_LITERAL_ACOUSTIC_CERTIFICATE_PASS','certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'positive_shift':str(rho),
            'exact_pivots':8,'coefficient_order':'u2,v2,uv,w2,uw,vw,qu,qv,qw','seconds':time.monotonic()-start,
            'scope':'All backgrounds and rankone increments by leftSO2 reduction; no PC or QC assertion.'}
def acquire(v,source_Q,path,rho=F(1,2000),denominator=100_000_000):
    values=[F(round(float(x)*denominator),denominator) for x in v]
    Q=[[sum(values[k]*int(source_Q[k,i,j]) for k in range(15)) for j in range(8)] for i in range(8)]
    rho=F(rho);D=ldl([[Q[i][j]-(rho if i==j else 0) for j in range(8)] for i in range(8)])
    out={'status':'EXACT_ACOUSTIC_MATRIX_ACQUIRED_PENDING_LITERAL_REPLAY','coefficients':list(map(str,values[:9])),
         'skew_parameters':list(map(str,values[9:])),'matrix':[[str(x) for x in row] for row in Q],
         'positive_shift':str(rho),'shifted_LDL_pivots':list(map(str,D))}
    path=Path(path);path.write_text(json.dumps(out,indent=2)+'\n');receipt=verify(path)
    path.with_name(path.stem+'_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return values[:9],receipt
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('certificate')
    print(json.dumps(verify(parser.parse_args().certificate),indent=2))

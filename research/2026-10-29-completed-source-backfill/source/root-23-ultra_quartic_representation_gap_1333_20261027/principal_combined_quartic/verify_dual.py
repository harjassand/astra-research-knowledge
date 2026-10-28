"""Independent stdlib-only literal-polynomial replay of the SOS separator.
No acquisition imports, SymPy, NumPy, solver or saved affine maps.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations_with_replacement
import json,time,hashlib
ROOT=Path(__file__).resolve().parent
def plus(*ps):
    p={}
    for a in ps:
        for e,c in a.items():p[e]=p.get(e,Q(0))+c
    return {e:c for e,c in p.items() if c}
def times(p,q):
    d={}
    for a,b in p.items():
        for c,f in q.items():
            e=tuple(x+y for x,y in zip(a,c));d[e]=d.get(e,Q(0))+b*f
    return {e:c for e,c in d.items() if c}
def scale(p,c):return {e:c*v for e,v in p.items() if c*v}
def dx(p,i):
    d={}
    for e,c in p.items():
        if e[i]:
            f=list(e);f[i]-=1;d[tuple(f)]=c*e[i]
    return d
def var(i):return {tuple(int(j==i) for j in range(8)):Q(1)}
def invariants(A):
    a,b,c,d=A
    return plus(times(a,a),times(c,c)),plus(times(b,b),times(d,d)),plus(times(a,b),times(c,d)),plus(times(a,d),scale(times(b,c),-1))
def energy(A):
    u,v,w,q=invariants(A)
    return plus(times(u,u),times(v,v),scale(times(w,w),3),scale(times(q,q),Q(113,10)),scale(times(q,plus(u,scale(v,-1))),4))
def ldl(A):
    n=len(A);L=[[Q(int(i==j)) for j in range(n)] for i in range(n)];D=[]
    for j in range(n):
        d=A[j][j]-sum((L[j][k]*L[j][k]*D[k] for k in range(j)),Q(0))
        assert d>0;D.append(d)
        for i in range(j+1,n):L[i][j]=(A[i][j]-sum((L[i][k]*L[j][k]*D[k] for k in range(j)),Q(0)))/d
    assert all(A[i][j]==sum((L[i][k]*L[j][k]*D[k] for k in range(n)),Q(0)) for i in range(n) for j in range(n))
    return D
def main():
    started=time.monotonic();raw=(ROOT/'EXACT_SUPPORT_SEPARATOR.json').read_bytes();data=json.loads(raw)
    assert data['input_nine_coefficients']==['1','1','113/10','-83/10','0','0','4','-4','0']
    monoms=list(map(tuple,data['monomial_order']));values=list(map(Q,data['lambda']))
    assert len(monoms)==len(values)==215 and len(set(monoms))==215
    functional=dict(zip(monoms,values))
    def apply(p):return sum((c*functional[e] for e,c in p.items()),Q(0))
    a=[var(i) for i in range(4)];x=[var(i+4) for i in range(4)]
    f=energy(a)
    residual=plus(energy([plus(a[i],x[i]) for i in range(4)]),scale(f,-1),*(scale(times(dx(f,i),x[i]),-1) for i in range(4)))
    u,v,w,q=invariants(a);qx=invariants(x)[3]
    assert apply(times(plus(u,scale(v,-1)),qx))==0
    assert apply(times(q,qx))==0
    # Stronger than the acquisition constraints: ALL quadratic selectors,
    # with no rotational/special-symmetry averaging required.
    all_quadratic_selector_pairings=[apply(times(times(a[i],a[j]),qx))
       for i,j in combinations_with_replacement(range(4),2)]
    assert all(v==0 for v in all_quadratic_selector_pairings)
    pairing=apply(residual);assert pairing==Q(-39,125000)==Q(data['energy_pairing'])
    z=[times(ai,xj) for ai in a for xj in x]+[times(x[i],x[j]) for i,j in combinations_with_replacement(range(4),2)]
    moment=[[apply(times(zi,zj)) for zj in z] for zi in z]
    assert moment==[list(map(Q,row)) for row in data['moment26']]
    pivots=ldl(moment);assert pivots==list(map(Q,data['positive_ldl_pivots']))
    receipt={'status':'INDEPENDENT_LITERAL_F_STDLIB_DUAL_PASS',
      'certificate_sha256':hashlib.sha256(raw).hexdigest(),
      'equations_scope':'All215 literal Bregman/feature monomials rebuilt; ALL TEN homogeneous quadratic selector terms annihilated',
      'all_quadratic_selector_pairings':list(map(str,all_quadratic_selector_pairings)),
      'energy_pairing':str(pairing),'strict_positive_moment_pivots':len(pivots),
      'seconds':time.monotonic()-started,
      'analytic_scope':'Together with all-degree homogeneity, excludes every polynomial SOS minor-support selector for this quartic WITHOUT a symmetry restriction. Does not exclude non-SOS positive support.'}
    (ROOT/'INDEPENDENT_DUAL_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()

"""Independent exact fixtures for Schur-Radau, spectral moments and exp intervals.
No peer code imported. No numerical eigenvalue sign used as a certificate.
"""
from fractions import Fraction as Q
from math import comb, factorial, ceil
from pathlib import Path
import json,datetime

def solve(A,b):
    n=len(A);Z=[list(A[i])+[b[i]] for i in range(n)]
    for j in range(n):
        p=next(i for i in range(j,n) if Z[i][j])
        Z[j],Z[p]=Z[p],Z[j]
        t=Z[j][j];Z[j]=[x/t for x in Z[j]]
        for i in range(n):
            if i!=j:
                t=Z[i][j]
                if t:Z[i]=[a-t*b for a,b in zip(Z[i],Z[j])]
    return [z[-1] for z in Z]

def ldlt(A,allow_last_zero=False):
    n=len(A);L=[[Q(0)]*n for _ in range(n)];d=[]
    for i in range(n):
        for j in range(i):
            L[i][j]=(A[i][j]-sum((L[i][k]*L[j][k]*d[k] for k in range(j)),Q(0)))/d[j]
        p=A[i][i]-sum((L[i][k]**2*d[k] for k in range(i)),Q(0))
        assert p>0 or (allow_last_zero and i==n-1 and p==0)
        d.append(p);L[i][i]=1
    return d

def mv(A,v):return [sum((a*b for a,b in zip(row,v)),Q(0)) for row in A]
def transpose(A):return list(map(list,zip(*A)))
def exp_negative_interval(x,P):
    assert x>=0
    if x==0:return Q(1),Q(1),0
    T=ceil(6*x)+P+4
    term=S=Q(1)
    for j in range(1,T+1):term*=x/j;S+=term
    nxt=term*x/(T+1)
    lo,hi=1/(S+2*nxt),1/S
    assert hi-lo<=Q(1,2**P)
    return lo,hi,T

moment_sets={
 'uniform':lambda l:Q(1,l+1),
 'beta22':lambda l:Q(6,(l+2)*(l+3)),
 'linear_density':lambda l:(Q(1,l+1)+Q(2,l+2))/2,
 'uniform_plus_atom':lambda l:Q(1,4*(l+1))+Q(3,4)*Q(3,10)**l,
 'positive_quadratic_density':lambda l:Q(1,2*(l+1))+Q(3,(l+2)*(l+3))
}
rows=[];moment_checks=0;block_checks=0
for name,fun in moment_sets.items():
    for n in range(1,13):
        m=n//2;d=m+1;u=[fun(l) for l in range(n+2)]
        assert u[0]==1
        H=[[u[i+j] for j in range(d)] for i in range(d)]
        K=[[u[i+j+1] for j in range(d)] for i in range(d)]
        if n%2==0:
            A=[row[:m] for row in K[:m]];v=[K[i][m] for i in range(m)]
            z=solve(A,v);K[m][m]=sum((a*b for a,b in zip(v,z)),Q(0))
        hd=ldlt(H);kd=ldlt(K,allow_last_zero=n%2==0)
        cd=ldlt([[H[i][j]-K[i][j] for j in range(d)] for i in range(d)])
        assert n%2 or kd[-1]==0
        block_checks+=3
        columns=[solve(H,[K[i][j] for i in range(d)]) for j in range(d)]
        T=transpose(columns);v=[Q(1)]+[Q(0)]*(d-1)
        recovered=[]
        for ell in range(n+2):
            y=mv(H,v);rec=y[0];recovered.append(rec)
            if ell<=n:assert rec==u[ell];moment_checks+=1
            v=mv(T,v)
        if name=='uniform' and n==2:assert recovered[3]!=u[3]
        rows.append({'measure':name,'n':n,'d':d,'rule':'Gaussian' if n%2 else 'Radau0','exact_through':n,'minimum_H_pivot':str(min(hd)),'minimum_support_pivot':str(min(cd)),'next_moment_preserved':recovered[n+1]==u[n+1]})
intervals=[]
for x in map(Q,['0','1/10','3/2','10','37/3']):
    a,b,T=exp_negative_interval(x,32);c,e,U=exp_negative_interval(x,128)
    assert a<=c<=e<=b
    intervals.append({'x':str(x),'terms32':T,'terms128':U,'nested':True,'width32_le_2^-32':True,'width128_le_2^-128':True})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_passed':True,
 'scope':'finite exact matrix construction and rational interval checks; all-N bit theorem remains the analytic proof',
 'fixtures':rows,'exact_moment_checks':moment_checks,'exact_PSD_block_checks':block_checks,
 'exp_intervals':intervals,'peer_code_imported':False,
 'negative_scope_check':'uniform n2 Radau next moment differs, so exactness is only through the assigned even degree'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='fixtures'},indent=2))

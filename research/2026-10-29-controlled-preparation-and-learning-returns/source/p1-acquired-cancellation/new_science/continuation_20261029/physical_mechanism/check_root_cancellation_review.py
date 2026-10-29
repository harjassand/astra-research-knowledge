"""Independent exact checks of root's weighted loop and cancellation identities."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import hashlib
import json

mu=[F(1,10),F(2,10),F(3,10),F(4,10)]
labels=[0,0,1,1]
weights=[[1,1,2,2],[3,3,1,1]]
Ts=[]
for j,w in enumerate(weights):
    nu=[mu[i]*w[i] for i in range(4)]
    total=sum(nu)
    nu=[x/total for x in nu]
    t=[[F(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for h in range(4):
            if i==h: continue
            conductance=F(i+h+1,1000) if j==0 else F(i*h+1,1200)
            t[i][h]=conductance/nu[i]
        t[i][i]=1-sum(t[i][h] for h in range(4) if h!=i)
    assert all(t[i][h]>=0 for i in range(4) for h in range(4))
    assert all(nu[i]*t[i][h]==nu[h]*t[h][i] for i in range(4) for h in range(4))
    Ts.append(t)
fs=[[[sum(t[x][v] for v in range(4) if labels[v]==b) for x in range(4)]
      for b in range(2)] for t in Ts]
loops=[]
for a in range(2):
    mass=sum(mu[x] for x in range(4) if labels[x]==a)
    means=[[sum(mu[x]*fs[j][b][x] for x in range(4) if labels[x]==a)/mass
            for b in range(2)] for j in range(2)]
    for i in range(2):
        for j in range(2):
            direct=sum(mu[x]*sum(fs[i][b][x]*fs[j][b][x] for b in range(2))
                       for x in range(4) if labels[x]==a)/mass
            weighted=F(0)
            ordinary=F(0)
            for x in range(4):
                for middle in range(4):
                    if labels[middle]!=a: continue
                    for end in range(4):
                        if labels[x]!=labels[end]: continue
                        event=mu[x]*Ts[i][x][middle]*Ts[j][middle][end]/mass
                        ordinary+=event
                        weighted+=F(weights[i][x],weights[i][middle])*event
            assert direct==weighted
            H=direct-sum(means[i][b]*means[j][b] for b in range(2))
            residual=sum(mu[x]*sum((fs[i][b][x]-means[i][b])*
                                   (fs[j][b][x]-means[j][b]) for b in range(2))
                         for x in range(4) if labels[x]==a)/mass
            assert H==residual
            loops.append({'a':a,'i':i,'j':j,'weighted_loop_equals_conditional_Gram':True,
                          'unweighted_loop_error':str(ordinary-direct)})
assert any(F(x['unweighted_loop_error'])!=0 for x in loops)

u=[F(1,10),F(3,10),F(1,4),F(7,20)]
v=[F(1,20),-F(3,20),F(1,10),-F(1,10)]
pa=[F(3,4),F(1,4),F(0),F(0)]
pb=[F(0),F(0),F(1,2),F(1,2)]
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
assert dot(pa,v)==0 and dot(pb,v)==0
assert dot(pa,u)==F(3,20) and dot(pb,u)==F(3,10)
vp=[abs(x) for x in v]
c=min(F(2,3)*x*vp[0] for x in vp)
v2=F(2,3)*vp[0]**2
assert c*c/v2==F(1,600)
return_a=1-u[0]-u[1]+2*u[0]*u[1]+F(2,3)*v[0]*v[1]
return_b=1-u[0]-u[1]+2*u[0]*u[1]+F(2,3)*vp[0]*vp[1]
assert return_b-return_a==F(1,100)
assert sum(pa[i]*2*abs(v[i]) for i in range(4))==F(3,20)

def det(mat):
    a=[row[:] for row in mat]
    d=F(1)
    n=len(a)
    for i in range(n):
        k=next((k for k in range(i,n) if a[k][i]),None)
        if k is None:return F(0)
        if k!=i:
            a[k],a[i]=a[i],a[k]
            d=-d
        pivot=a[i][i]
        d*=pivot
        for j in range(i+1,n):
            factor=a[j][i]/pivot
            for k in range(i+1,n):a[j][k]-=factor*a[i][k]
    return d

# Integral of (4/5-h/10)^n over uniform h in [-1,1].
mom=[sum(F(comb(n,r))*F(4,5)**(n-r)*(-F(1,10))**r/F(r+1)
         for r in range(0,n+1,2)) for n in range(11)]
dets=[det([[mom[i+j] for j in range(n)] for i in range(n)]) for n in range(1,6)]
assert all(d>0 for d in dets)

inp=Path(__file__).parent/'reviewed_versions'/'ACQUIRED_HIDDEN_RESPONSE_CANCELLATION_17507118b24d.md'
result={'reviewed_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),
        'weighted_loop_checks':loops,'mixture_A_flip':str(dot(pa,u)),
        'mixture_B_flip':str(dot(pb,u)),'source_B_min_squared_residual':str(c*c/v2),
        'cross_return_probability_source_A':str(return_a),
        'cross_return_probability_source_B':str(return_b),
        'cross_separation':str(return_b-return_a),'retained_key_two_hidden_points_TV':'3/20',
        'autocorrelation_Hankel_determinants_sizes_1_to_5':[str(x) for x in dets],
        'scope':'Exact independent algebra checks; ordinary proof supplies all sizes and all horizons.'}
out=Path(__file__).with_name('ROOT_CANCELLATION_REVIEW_CHECKS.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

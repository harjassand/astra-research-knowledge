"""Standard-library exact replay; no floating arithmetic or assert statements."""
from fractions import Fraction as F
from pathlib import Path
import json

d=json.loads((Path(__file__).parent/'exact_certificate_v1.json').read_text())
def matrix(key):return [[F(a) for a in row] for row in d[key]]
def require(test,label):
    if not test:raise RuntimeError(label)
def transpose(a):return [list(row) for row in zip(*a)]
def mul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def sub(a,b):return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def zero(a):return all(x==0 for row in a for x in row)
def det(a):
    a=[row[:] for row in a];out=F(1);n=len(a)
    for i in range(n):
        pivot=next((j for j in range(i,n) if a[j][i]),None)
        if pivot is None:return F(0)
        if pivot!=i:a[i],a[pivot]=a[pivot],a[i];out=-out
        p=a[i][i];out*=p
        for j in range(i+1,n):
            ratio=a[j][i]/p
            for k in range(i,n):a[j][k]-=ratio*a[i][k]
    return out

v=matrix('points');z=matrix('farkas_z');D=matrix('internal_D');C=matrix('covariance');B=matrix('B')
Q=matrix('Q');H=matrix('H');M=matrix('M');L=matrix('L')
mean=[sum(row[k] for row in v)/5 for k in range(2)]
u=[[row[k]-mean[k] for k in range(2)] for row in v]
require(all(sum(a*a for a in row)==1 for row in v),'all circle points')
require(len(set(tuple(row) for row in v))==5,'distinct points')
require(all(Q[i][j]>=0 for i in range(10) for j in range(10) if i!=j),'CTMC positivity')
require(all(sum(row)==0 for row in Q),'generator row sums')
require(all(sum(row[j] for row in Q)==0 for j in range(10)),'uniform stationarity')
require(all(Q[i][j]>0 for i in range(5) for j in range(5) if i!=j),'internal irreducibility')
require(all((Q[i][j]>0)==(Q[j][i]>0) for i in range(10) for j in range(i+1,10)),'finite EPR support')
require(zero(sub(mul(Q,H),mul(H,L))),'observable subspace invariant')
require(zero(sub(mul(M,L),mul(transpose(L),M))),'restricted generator selfadjoint')
require(M==[[sum(H[k][i]*H[k][j] for k in range(10))/10 for j in range(8)] for i in range(8)],'observable Gram')
require(det(M)>0,'observable rank eight')
require(zero(sub(mul(C,transpose(D)),mul(D,C))),'internal selfadjoint drift')
require(B[0][0]>0 and det(B)>0,'positive internal drift')
facets=matrix('facets')
require(all(f[0]+f[1]*p[0]+f[2]*p[1]>=0 for f in facets for p in v),'polygon facets')
require(sum(f[1] for f in facets)==sum(f[2] for f in facets)==0,'constant total marker rate')
require(any(det([facets[i],facets[j],facets[k]])!=0 for i in range(5) for j in range(i+1,5) for k in range(j+1,5)),'marker reachability of hidden affine coordinates')
moment=[[1,p[0],p[1],p[0]*p[0],p[0]*p[1]] for p in v]
require(det(transpose(moment))==F(d['five_point_moment_determinant'])!=0,'unique five-point moments')
pairings=[]
for i in range(5):
    for j in range(i+1,5):
        pairing=sum((z[i][k]-z[j][k])*(v[i][k]-v[j][k]) for k in range(2))
        require(pairing>0,'strict Farkas monotonicity')
        pairings.append(pairing)
drift_pairing=sum(sum(z[i][k]*sum(D[k][h]*u[i][h] for h in range(2)) for k in range(2))/5 for i in range(5))
require(drift_pairing==F(d['farkas_drift_pairing'])<0,'negative Farkas drift pairing')
# Full eight-coordinate monotone field, with marker terms cancelling exactly.
Z=[[F(0),*z[i],*[sum(z[i][k]*v[i][k] for k in range(2))]*5] for i in range(5)]+[[F(0)]*8 for _ in range(5)]
for i in range(10):
    for j in range(i+1,10):
        require(sum((Z[i][k]-Z[j][k])*(H[i][k]-H[j][k]) for k in range(8))>=0,'full monotone field')
negative_QH=mul([[-a for a in row] for row in Q],H)
full_pairing=sum(sum(Z[i][k]*negative_QH[i][k] for k in range(8))/10 for i in range(10))
require(full_pairing==drift_pairing/2<0,'full marker cancellation and Farkas obstruction')
# Remove the known symmetric marker links and check the internal drift directly.
for i in range(5):
    for k in range(2):
        lhs=sum(Q[i][j]*(v[j][k]-v[i][k]) for j in range(5))
        rhs=-sum(D[k][h]*u[i][h] for h in range(2))
        require(lhs==rhs,'exact internal drift')
print(json.dumps(dict(status='PASS',arithmetic='fractions.Fraction',states=10,outputs=6,observable_rank=8,strict_monotonicity_min=str(min(pairings)),negative_farkas_pairing=str(drift_pairing),full_farkas_pairing=str(full_pairing)),indent=2))

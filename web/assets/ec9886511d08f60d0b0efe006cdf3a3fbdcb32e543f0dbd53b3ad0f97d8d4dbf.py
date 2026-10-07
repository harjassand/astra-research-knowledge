#!/usr/bin/env python3
"""Small exact Fraction diagnostic; no optimizer, no theorem inference."""
from fractions import Fraction as F
from itertools import combinations
import json,time,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
start=time.monotonic()
def zeros(n,m=None): return [[F(0) for _ in range(m or n)] for _ in range(n)]
def eye(n):
 a=zeros(n)
 for i in range(n):a[i][i]=F(1)
 return a
def trans(a): return list(map(list,zip(*a)))
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def sub(a,b): return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,c): return [[c*x for x in ar] for ar in a]
def mul(a,b):
 bt=trans(b)
 return [[sum((x*y for x,y in zip(ar,bc)),F(0)) for bc in bt] for ar in a]
def vec(a,x):return [sum((v*w for v,w in zip(ar,x)),F(0)) for ar in a]
def det(a):
 a=[r[:] for r in a];v=F(1);n=len(a)
 for k in range(n):
  j=next((j for j in range(k,n) if a[j][k]),None)
  if j is None:return F(0)
  if j!=k:a[k],a[j]=a[j],a[k];v=-v
  p=a[k][k];v*=p
  for j in range(k+1,n):
   q=a[j][k]/p
   for l in range(k+1,n):a[j][l]-=q*a[k][l]
 return v
def psd_principal(a):
 assert a==trans(a)
 vals=[]
 for k in range(1,len(a)+1):
  for ids in combinations(range(len(a)),k):
   z=det([[a[i][j] for j in ids] for i in ids]); assert z>=0,(ids,z)
   vals.append(z)
 return {'count':len(vals),'zero':sum(z==0 for z in vals),'min':str(min(vals))}
def encode(a):return [[str(x) for x in r] for r in a]
w=[F(1,3),F(2,3)]
P=[[F(1,2),F(1,4)],[F(1,2),F(3,4)]] # P[output][input]
assert all(sum(P[b][a] for b in range(2))==1 for a in range(2))
assert [sum(P[b][a]*w[a] for a in range(2)) for b in range(2)]==w
R=[[w[a]*P[b][a]/w[b] for a in range(2)] for b in range(2)]
t=F(7,25);ell=[F(1),F(24,25),F(24,25),F(1)];q=[F(1),F(0),F(0),t]
n=8;L=zeros(n);Q=zeros(n);Psi=zeros(n);G=zeros(n);Ginv=zeros(n)
for b in range(2):
 for k in range(4):
  i=4*b+k;G[i][i]=w[b];Ginv[i][i]=1/w[b]
  Psi[i][i]=[F(1),F(0),F(0),t*t][k]
  for a in range(2):
   L[i][4*a+k]=R[b][a]*ell[k];Q[i][4*a+k]=R[b][a]*q[k]
C=scale(add(L,Q),F(1,2));Cdag=mul(mul(Ginv,trans(C)),G);Phi=mul(Cdag,C)
I=eye(n)
assert mul(G,Phi)==trans(mul(G,Phi))
certs={
 'I_minus_Ldag_L':psd_principal(sub(G,mul(mul(trans(L),G),L))),
 'Psi_minus_Qdag_Q':psd_principal(sub(mul(G,Psi),mul(mul(trans(Q),G),Q))),
 'factor_two':psd_principal(mul(G,sub(add(I,Psi),scale(Phi,F(2)))))
}
# Exact identity using the noncanonical EB branch Q.
left=mul(G,sub(add(I,Psi),scale(Phi,F(2))))
right=add(add(sub(G,mul(mul(trans(L),G),L)),sub(mul(G,Psi),mul(mul(trans(Q),G),Q))),scale(mul(mul(trans(sub(L,Q)),G),sub(L,Q)),F(1,2)))
assert left==right
# Actual effects: P[b][a] times diag(16/25,9/25) or its reverse in input block a.
# Preparation is pure |y> in output block b; these are not canonical preparations.
effects=[]
for a in range(2):
 for b in range(2):
  for y in range(2):
   diag=[F(0)]*4
   diag[2*a:2*a+2]=[P[b][a]*F(16 if y==0 else 9,25),P[b][a]*F(9 if y==0 else 16,25)]
   p=w[a]*P[b][a]/2
   prep=[F(0)]*4;prep[2*b+y]=F(1)
   effects.append({'input_block':a,'output_block':b,'outcome':y,'effect_diagonal':list(map(str,diag)),'p_tau':str(p),'preparation_diagonal':list(map(str,prep))})
assert all(sum(F(e['effect_diagonal'][i]) for e in effects)==1 for i in range(4))
assert [sum(F(e['p_tau'])*F(e['preparation_diagonal'][i]) for e in effects) for i in range(4)]==[F(1,6),F(1,6),F(1,3),F(1,3)]
# Full trace norm is exact on the diagonal likelihood fixtures below.
def norm1_diag(x):return sum(w[a]*(abs(x[4*a]+x[4*a+3])+abs(x[4*a]-x[4*a+3]))/2 for a in range(2))
fixtures=0;theta=F(1,2)
for u in range(-2,3):
 for v in range(-2,3):
  for z in range(-2,3):
   h=[F(0)]*n;h[0]=F(u,12);h[4]=-F(u,24);h[3]=F(v,12);h[7]=F(z,12)
   assert w[0]*h[0]+w[1]*h[4]==0
   assert max(abs(h[4*a])+abs(h[4*a+3]) for a in range(2))<=theta
   ph=vec(Phi,h);ps=vec(Psi,h)
   r=norm1_diag([x-y for x,y in zip(h,ph)])
   err=norm1_diag([x-y for x,y in zip(h,ps)])
   assert err*err<=2*theta*r
   fixtures+=1
out={'status':'DIAGNOSTIC_ONLY','theorem_basis':'Exact factorization and contraction proof in INITIAL.txt; these fixtures do not prove universality','algebra':'M2 direct sum M2','weights':list(map(str,w)),'transition_P':encode(P),'likelihood_R':encode(R),'noncanonical_preparation':True,'block_changing':True,'kraus_spin':['diag(4/5,3/5)','diag(3/5,4/5)'],'L':encode(L),'Q':encode(Q),'Psi':encode(Psi),'Phi':encode(Phi),'Gram':encode(G),'principal_minor_certificates':certs,'exact_SOS_identity':True,'effects_and_preparations':effects,'exact_diagonal_likelihood_fixtures':fixtures,'wall_seconds':time.monotonic()-start}
(ROOT/'weighted_instrument_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','principal_minor_certificates','exact_SOS_identity','exact_diagonal_likelihood_fixtures','wall_seconds']},indent=2))

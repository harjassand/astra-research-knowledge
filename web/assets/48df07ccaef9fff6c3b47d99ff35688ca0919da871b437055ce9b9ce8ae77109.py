#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import combinations
import pathlib,json,time
ROOT=pathlib.Path(__file__).resolve().parent;t0=time.monotonic()
def trans(a):return list(map(list,zip(*a)))
def add(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,c):return [[c*x for x in r] for r in a]
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):return [[sum((x*y for x,y in zip(ar,bc)),F(0)) for bc in trans(b)] for ar in a]
def diag(v):return [[x if i==j else F(0) for j in range(len(v))] for i,x in enumerate(v)]
def det(a):
 a=[r[:] for r in a];out=F(1)
 for k in range(len(a)):
  j=next((j for j in range(k,len(a)) if a[j][k]),None)
  if j is None:return F(0)
  if j!=k:a[k],a[j]=a[j],a[k];out=-out
  p=a[k][k];out*=p
  for j in range(k+1,len(a)):
   z=a[j][k]/p
   for l in range(k+1,len(a)):a[j][l]-=z*a[k][l]
 return out

def psd(a):
 assert a==trans(a);vs=[]
 for k in range(1,len(a)+1):
  for inds in combinations(range(len(a)),k):
   v=det([[a[i][j] for j in inds] for i in inds]);assert v>=0,(inds,v);vs.append(v)
 return {'principal_minors':len(vs),'zero':sum(v==0 for v in vs)}
s=[F(9,25),F(16,25)];sab=F(12,25);g=s+[2*sab,2*sab]
G=diag(g);Gi=diag([1/x for x in g]);I=diag([F(1)]*4)
L=[[s[0],s[1],F(0),F(0)],[s[0],s[1],F(0),F(0)],[F(0)]*4,[F(0)]*4]
Q=[r[:] for r in L];Q[2][2]=F(72,125)
Psi=[r[:] for r in L];Psi[2][2]=F(216,625)
C=scale(add(L,Q),F(1,2));Cd=mul(mul(Gi,trans(C)),G);Phi=mul(Cd,C)
A=sub(G,mul(mul(trans(L),G),L));B=sub(mul(G,Psi),mul(mul(trans(Q),G),Q));D=scale(mul(mul(trans(sub(L,Q)),G),sub(L,Q)),F(1,2))
slack=mul(G,sub(add(I,Psi),scale(Phi,F(2))));assert slack==add(add(A,B),D)
certs={'I-LdagL':psd(A),'Psi-QdagQ':psd(B),'factor_two':psd(slack)}
assert mul(G,Phi)==trans(mul(G,Phi))
# Effects commute neither with sigma nor with the prepared states in general.
t=F(3,5);commutator_upper_right=(s[0]-s[1])*t/2;assert commutator_upper_right!=0
p=[F(1,2),F(1,2)];rho_plus=[[s[0],sab],[sab,s[1]]];rho_minus=[[s[0],-sab],[-sab,s[1]]]
assert det(rho_plus)==det(rho_minus)==0
assert add(scale(rho_plus,F(1,2)),scale(rho_minus,F(1,2)))==diag(s)
def mv(a,x):return [sum(v*z for v,z in zip(r,x)) for r in a]
def physical_norm1_square(v):
 z0,z1,x,y=v;trace=s[0]*z0+s[1]*z1;de=s[0]*s[1]*z0*z1-sab*sab*(x*x+y*y)
 return trace*trace-4*de if de<=0 else trace*trace
fixtures=0;theta=F(1,2)
for u in range(-2,3):
 for v in range(-2,3):
  for z in range(-2,3):
   h=[F(16*u,400),F(-9*u,400),F(v,20),F(z,20)]
   assert sum(s[i]*h[i] for i in range(2))==0
   assert max(abs(h[0]),abs(h[1]))+abs(h[2])+abs(h[3])<=theta
   hp=mv(Psi,h);hf=mv(Phi,h)
   en=physical_norm1_square([a-b for a,b in zip(h,hp)])
   rn=physical_norm1_square([a-b for a,b in zip(h,hf)])
   assert en>=0 and rn>=0 and en*en<=4*theta*theta*rn
   fixtures+=1
enc=lambda a:[[str(x) for x in r] for r in a]
out={'status':'EXACT_SMALL_DIAGNOSTIC; GENERAL_PROOF_IN_NONCENTRAL_EB_BRANCH.txt','sigma':enc(diag(s)),'sqrt_sigma':enc(diag([F(3,5),F(4,5)])),'effect_sigma_commutator_upper_right':str(commutator_upper_right),'noncanonical_preparation':True,'Gram':enc(G),'L':enc(L),'Q':enc(Q),'Psi':enc(Psi),'Phi':enc(Phi),'exact_SOS':True,'PSD_certificates':certs,'exact_Hermitian_likelihood_fixtures':fixtures,'wall_seconds':time.monotonic()-t0}
(ROOT/'noncentral_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','effect_sigma_commutator_upper_right','exact_SOS','PSD_certificates','exact_Hermitian_likelihood_fixtures','wall_seconds']},indent=2))

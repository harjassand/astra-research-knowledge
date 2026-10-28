"""Exact operator/cap checks only. No Bernoulli draws, RNG, or source calls."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def eye(m):return [[F(i==j) for j in range(m)] for i in range(m)]
def zeros(m):return [[F(0) for _ in range(m)] for _ in range(m)]
def mul(A,B):
 m=len(A);return [[sum((A[i][k]*B[k][j] for k in range(m)),F(0)) for j in range(m)] for i in range(m)]
def trprod(A,B):return sum((A[i][j]*B[j][i] for i in range(len(A)) for j in range(len(A))),F(0))
def psd(A):
 A=[row[:] for row in A];n=len(A)
 for k in range(n):
  if A[k][k]<0:return False
  if A[k][k]==0:
   if any(A[k][j]!=0 for j in range(k+1,n)):return False
   continue
  for i in range(k+1,n):
   for j in range(i,n):
    A[i][j]-=A[i][k]*A[k][j]/A[k][k];A[j][i]=A[i][j]
 return True
def ceilf(x):return (x.numerator+x.denominator-1)//x.denominator
def clog(x):
 k=0;v=F(1)
 while v<x:k+=1;v*=2
 return k

operator_cases=[]
for m in range(1,5):
 I=eye(m);Rot=eye(m)
 if m>1:
  Rot[0][0]=Rot[1][1]=F(3,5);Rot[0][1]=F(-4,5);Rot[1][0]=F(4,5)
 Rt=[list(r) for r in zip(*Rot)]
 eig=[F(1,2)+F(j,2*m) for j in range(m)]
 B=mul(mul(Rot,[[eig[i] if i==j else F(0) for j in range(m)] for i in range(m)]),Rt)
 A=[[B[i][j]/4+F(1,8*m) for j in range(m)] for i in range(m)]
 tau=F(1,2);Q=[[I[i][j]-B[i][j]/4 for j in range(m)] for i in range(m)]
 C=zeros(m);Qpow=eye(m);coef=F(1)
 for k in range(48):
  for i in range(m):
   for j in range(m):C[i][j]+=coef*Qpow[i][j]/2
  Qpow=mul(Qpow,Q);coef*=F(2*k+1,2*k+2)
 C2=mul(C,C);target=mul(mul(C,A),C);target2=mul(target,target)
 design=[]
 for a in range(m):
  P=zeros(m);P[a][a]=F(1);design.append((F(2,m*(m+2)),P))
 for signs in product((-1,1),repeat=m):design.append((F(m,(m+2)*2**m),[[F(signs[i]*signs[j],m) for j in range(m)] for i in range(m)]))
 EY2=zeros(m);mean=zeros(m);S=F(m*m*(m+3),4);R=F(m*(m+1))
 for prob,P in design:
  weight=trprod(C2,P);effect=trprod(target,P)
  T=[[F(m*(m+2),2)*P[i][j]-F(m,2)*I[i][j] for j in range(m)] for i in range(m)]
  T2=mul(T,T)
  for i in range(m):
   for j in range(m):
    EY2[i][j]+=prob*weight*effect*T2[i][j]
    mean[i][j]+=prob*effect*T[i][j]
  for y in [0,1]:
   X=[[y*weight*T[i][j]-target[i][j] for j in range(m)] for i in range(m)]
   for sign in [-1,1]:assert psd([[R/tau*I[i][j]+sign*X[i][j] for j in range(m)] for i in range(m)])
 assert mean==target
 variance=[[EY2[i][j]-target2[i][j] for j in range(m)] for i in range(m)]
 assert psd(variance)
 assert psd([[S/tau*I[i][j]-variance[i][j] for j in range(m)] for i in range(m)])
 assert psd([[S/tau*I[i][j]-EY2[i][j] for j in range(m)] for i in range(m)])
 operator_cases.append({'m':m,'canonical_C':'rational binomial polynomial','noncommuting_A_B':mul(A,B)!=mul(B,A),'exact_mean_CAC':'PASS','operator_variance_S_over_tau':'PASS','both_sign_centered_norm_R_over_tau':'PASS','finite_design_atoms':len(design)})

cases=[]
for m,eps,gamma,beta in product([1,2,5,17],[F(1,2),F(1,4),F(1,8),F(3,16),F(1,64)],[F(1,2),F(1,4),F(3,4),F(1,16)],[F(1,20),F(1,1000)]):
 S=F(m*m*(m+3),4);R=F(m*(m+1));P=2*S+R
 if eps<gamma:
  J=clog(gamma/eps);H=J+1;tau=F(1,2**J);L=clog(F(4*m*H)/beta)
  assert eps/(2*gamma)<tau<=eps/gamma
  samples=0
  for j in range(1,J+1):
   tj=F(1,2**(j-1));delta=F(1,64);N=ceilf(P*L/(tj*delta*delta));samples+=N
   assert N*tj*delta*delta>=P*L
   assert 2*S+F(2,3)*R*delta<=P
  delta=gamma/64;N=ceilf(P*L/(tau*delta*delta));samples+=N
  assert N*tau*delta*delta>=P*L
  cap=H+16384*P*L/(gamma*eps);assert samples<=cap
  u=gamma/28;v=gamma*tau/16
  assert (1+u)/(1-u)<=1+2*gamma/27
  assert (2*v+eps/16)/(1-u)<=7*eps/36<=eps/4
  regime='relative_terminal'
 else:
  H=1;J=0;L=clog(F(4*m*H)/beta);delta=eps/16
  samples=ceilf(P*L/(delta*delta));cap=1+256*P*L/(gamma*eps);assert samples<=cap
  assert 3*eps/16<=eps/4
  regime='additive'
 assert 0<delta<=1
 assert F(2*m,2**L)<=beta/(2*H)
 cases.append({'m':m,'epsilon':str(eps),'gamma':str(gamma),'beta':str(beta),'regime':regime,'H':H,'L':L,'computed_but_NOT_sampled_count':samples})
result={'status':'PASS','source_calls':0,'Bernoulli_samples':0,'RNG_draws':0,'kind':'Exact prescribed-matrix operator moments/norm certificates and rational cap/terminal arithmetic; not source simulation and not a proof of the imported matrix Bernstein theorem.','operator_cases':operator_cases,'parameter_case_count':len(cases),'relative_branch_cases':sum(r['regime']=='relative_terminal' for r in cases),'additive_branch_cases':sum(r['regime']=='additive' for r in cases),'parameter_cases':cases,'primary_theorem_checked_separately':'Tropp arXiv1004.4389v6 Theorem6.1(ii), printed pages21-22; two signs needed.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print('PASS: four canonical operator cases and',len(cases),'exact regime/cap cases; zero source calls/RNG.')

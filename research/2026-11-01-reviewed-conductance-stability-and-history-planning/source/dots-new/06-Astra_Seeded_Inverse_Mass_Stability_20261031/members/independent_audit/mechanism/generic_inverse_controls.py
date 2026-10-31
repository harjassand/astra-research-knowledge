#!/usr/bin/env python3
from fractions import Fraction as F
from math import prod,ceil
from exact_seeded_checks import hard_raw,ff,comps,ceil_sqrt
import json

def profile(raw,w,t):
 n=len(w)+1;internal=raw[2:];lam,mu=raw[0][2],raw[1][2];v=[F(1)]+list(w)
 assert all(u[0]>=1 and z[0]>=1 and sum(u)==sum(z) and 1<=sum(u)-1<=2 for u,z,k in internal)
 jumps=[sum(a*(b-c) for a,b,c in zip(v,z,u)) for u,z,k in internal];ell=1+max(map(abs,jumps));co={}
 for (u,z,k),delta in zip(internal,jumps):
  stripped=(u[0]-1,)+u[1:];rho=delta/ell if delta>=0 else ell*delta;co[stripped]=co.get(stripped,F(0))+k*rho
 pure=[co.get(tuple(2*int(i==j) for i in range(n)),F(0)) for j in range(1,n)]
 if not all(a>0 for a in pure):return None
 for i in range(1,n):
  for j in range(i+1,n):
   assert co.get(tuple(int(k==i)+int(k==j) for k in range(n)),F(0))>=0
 K1=max([F(0)]+[-c for u,c in co.items() if sum(u)==1]);K2=max([F(0)]+[-c for u,c in co.items() if sum(u)==2 and u[0]])
 K0=K1+K2;K=K0+sum((u+K0)**2/(2*u) for u in pure);D=mu*(1-1/t);c=min(F(1),D/(4*K));C=lam*(t-1)+3*mu+D;zeta=min(lam/4,D/4,F(1));S=sum(a*a/u for a,u in zip(w,pure));compatible=(S==0 or c/(4*(1+c)*S)>=C+zeta)
 if not compatible:return {'compatible':False}
 Ac=ceil(4*(C+zeta)/(3*D));threshold=9*Ac**2/S if S else 2*(1+c)*(C+zeta)*Ac**2/c;cuts=[ceil_sqrt(threshold/u) for u in pure]
 return {'compatible':True,'weights':w,'ell':ell,'coefficients':co,'u':pure,'K1':K1,'K2':K2,'Ktilde':K,'D':D,'c':c,'C':C,'zeta':zeta,'S':S,'Acut':Ac,'cuts':cuts}

def check(label,raw,w,t=F(2),limit=14):
 z=profile(raw,w,t);assert z and z['compatible'];n=len(w)+1;c=z['c']
 def hh(x):return 2*t*(1+c) if not x[0] else 1+c/(x[0]+sum(a*b for a,b in zip(w,x[1:])))
 def state(x):
  A=x[0];out=lint=F(0);Psi=F(0)
  for u,v,k in raw:
   rate=k*ff(x,u)
   if not rate:continue
   y=tuple(a-b+d for a,b,d in zip(x,u,v));out+=rate*(t**(sum(v)-sum(u))*hh(y)/hh(x)-1)
   if sum(u)==sum(v):lint+=rate*(hh(y)-hh(x))
  if not A:assert out<=-raw[0][2]/2 and lint==0;return
  r=(A-1,)+x[1:];Psi=sum(c0*ff(r,u) for u,c0 in z['coefficients'].items());Q=sum(u*b*b for u,b in zip(z['u'],x[1:]));R=A+sum(a*b for a,b in zip(w,x[1:]))
  assert lint<=-c*A*Psi/R**2
  assert Psi>=Q/2-z['Ktilde']*A*A
  neg=c*A*Q/(2*(1+c)*R*R)
  assert lint/hh(x)<=c*z['Ktilde']*A-neg
  assert out<=z['C']-3*z['D']*A/4-neg
  if A>=z['Acut'] or any(b>=cut for b,cut in zip(x[1:],z['cuts'])):assert out<=-z['zeta']
 count=0
 for N in range(limit+1):
  for x in comps(N,n):state(x);count+=1
 points=[]
 for A in [0,1,2,z['Acut']-1,z['Acut']]:
  for j in range(n-1):
   for B in [z['cuts'][j]-1,z['cuts'][j],z['cuts'][j]+1,10**50]:
    x=[A]+[0]*(n-1);x[j+1]=B;points.append(tuple(x))
 for x in points:state(x)
 return {'label':label,'weights':list(map(str,w)),'ell':str(z['ell']),'u':list(map(str,z['u'])),'K1':str(z['K1']),'K2':str(z['K2']),'S':str(z['S']),'Acut':z['Acut'],'cuts':z['cuts'],'ordinary_checks':count,'targeted_checks':len(points)}
raw=hard_raw([1,1,1,1,1,1,2,1]);eta=F(1,8)
while not profile(raw,[eta,F(0)],F(2))['compatible']:eta/=2
rows=[check('generic_hard_profile',raw,[eta,F(0)])]
# Nonzero stripped unary correction.
unary=raw+[((2,0,0),(1,1,0),F(3,5)),((1,1,0),(2,0,0),F(7,4))];eta=F(1,8)
while not profile(unary,[eta,F(0)],F(2))['compatible']:eta/=2
rows.append(check('negative_stripped_unary_K1',unary,[eta,F(0)]));assert F(rows[-1]['K1'])>0
# Zero-weight branch with a size-two service jump: ell is three, not two.
raw2=[((0,0),(1,0),F(1)),((1,0),(0,0),F(1)),((3,0),(1,2),F(2)),((1,2),(3,0),F(3))]
rows.append(check('S_zero_ell_three',raw2,[F(0)],limit=25));assert rows[-1]['ell']=='3' and rows[-1]['S']=='0'
print(json.dumps({'generic_effective_coefficient_and_square_bounds_checked':True,'cases':rows,
 'scope':'A generic positive-S fixed-base receipt gives that base moment only; all-base acquisition is separate.'},indent=2))

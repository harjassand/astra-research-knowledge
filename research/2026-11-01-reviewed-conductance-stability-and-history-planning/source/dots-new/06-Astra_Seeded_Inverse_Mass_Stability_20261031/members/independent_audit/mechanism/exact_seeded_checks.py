#!/usr/bin/env python3
from fractions import Fraction as F
from math import prod,ceil,isqrt
import json

def ff(x,u):
 if any(a<b for a,b in zip(x,u)):return 0
 return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,u))
def comps(N,n):
 if n==1:yield(N,)
 else:
  for a in range(N+1):
   for z in comps(N-a,n-1):yield(a,)+z

def baseline(label,lam,mu,alphas,betas,t=F(2),limit=18):
 lam,mu,t=map(F,[lam,mu,t]);alphas=list(map(F,alphas));betas=list(map(F,betas));m=len(alphas);n=m+1;z=(0,)*n;unit=(1,)+(0,)*m
 raw=[(z,unit,lam),(unit,z,mu)]
 for j,(a,b) in enumerate(zip(alphas,betas),1):
  u=tuple(2 if i==0 else int(i==j) for i in range(n));v=tuple(1 if i==0 else 2*int(i==j) for i in range(n));raw.extend([(u,v,a),(v,u,b)])
 if m>=2:
  u=(1,2,0)+(0,)*(m-2);v=(1,0,2)+(0,)*(m-2);raw.extend([(u,v,F(1)),(v,u,F(1))])
  # Higher-order neutral channels are completely invisible to the comparator.
  u=(1,3,0)+(0,)*(m-2);v=(1,1,2)+(0,)*(m-2);raw.extend([(u,v,F(1,3)),(v,u,F(7,4))])
 D=mu*(1-1/t);beta=min(betas);alpha=max(alphas);L=alpha+beta/2;c=min(F(1),D*beta/(2*m*L**2));k=c*beta/(2*m*(1+c));C0=lam*(t-1)+mu+5*D/4;kap=min(3*D/8,k/8);zeta=min(lam/2,kap);R=max(1,ceil((C0+zeta)/kap))
 def h(x):return 2*t*(1+c) if x[0]==0 else 1+c/F(x[0])
 def state(x):
  a=x[0];b=sum(x[1:]);N=sum(x);out=lint=F(0)
  for u,v,k0 in raw:
   rate=k0*ff(x,u)
   if not rate:continue
   y=tuple(a0-b0+c0 for a0,b0,c0 in zip(x,u,v));out+=rate*(t**(sum(v)-sum(u))*h(y)/h(x)-1)
   if sum(u)==sum(v):lint+=rate*(h(y)-h(x))
  if a==0:assert out==-lam/2 and lint==0
  else:
   exact=-c*sum(beta0*xj*(xj-1) for beta0,xj in zip(betas,x[1:]))/(a+1)
   if a>=2:exact+=c*sum(alpha0*xj for alpha0,xj in zip(alphas,x[1:]))
   assert lint==exact
   assert lint/h(x)<=-k*b*b/(a+1)+c*m*L**2*(a+1)/(2*beta)
   assert out<=C0-3*D*a/4-k*b*b/(a+1)<=C0-kap*N
   if N>=R:assert out<=-zeta
  return out
 count=0
 for N in range(limit+1):
  for x in comps(N,n):state(x);count+=1
 huge=0
 for N in [R-1,R,R+1,10**6,10**50]:
  for a in [0,1,2,N]:
   if a>N:continue
   x=(a,N-a)+(0,)*(m-1);state(x);huge+=1
 return {'case':label,'m':m,'t':str(t),'c':str(c),'C0':str(C0),'kappa':str(kap),'R':R,'ordinary_checks':count,'huge_checks':huge}

def hard_raw(rates):
 lam,mu,a1,b1,a2,b2,a3,b3=map(F,rates)
 return [((0,0,0),(1,0,0),lam),((1,0,0),(0,0,0),mu),
 ((2,1,0),(1,1,1),a1),((1,1,1),(2,1,0),b1),((2,0,1),(1,2,0),a2),((1,2,0),(2,0,1),b2),
 ((1,1,1),(1,0,2),a3),((1,0,2),(1,1,1),b3)]
def ceil_sqrt(r):
 k=isqrt(r.numerator//r.denominator)
 return k if k*k*r.denominator>=r.numerator else k+1

def inverse(label,rates,t=F(2),limit=18):
 rates=list(map(F,rates));lam,mu,a1,b1,a2,b2,a3,b3=rates;raw=hard_raw(rates);D=mu*(1-1/t);alpha=max(a1,a2);u=b2/4;k=b3/2;C0=lam*(t-1)+3*mu+D;zeta=min(lam/4,D/4,F(1));eta=min(F(1,4),b1/(4*a3));trials=[]
 Kbar=(2*alpha+u)**2/(2*u)+2*alpha**2/k+2*alpha+k/2;c0=min(F(1),D/(4*Kbar));guaranteed_eta=c0*u/(8*(C0+zeta))
 while True:
  v=k*eta;K=(2*alpha+u)**2/(2*u)+(2*alpha+v)**2/(2*v);c=min(F(1),D/(4*K));strength=c*u/(4*(1+c)*eta**2)
  assert K<=Kbar/eta and c>=c0*eta and strength>=c0*u/(8*eta)
  trials.append({'eta':str(eta),'c':str(c),'passes':strength>=C0+zeta})
  if strength>=C0+zeta:break
  assert eta>guaranteed_eta;eta/=2
 Ac=ceil(4*(C0+zeta)/(3*D));Bc=ceil(3*Ac/eta);Rbar=Ac+eta*Bc;Cc=ceil_sqrt(u*Rbar**2/(2*v*eta**2));assert Cc*Cc>=u*Rbar**2/(2*v*eta**2)
 def h(x):return 2*t*(1+c) if x[0]==0 else 1+c/(x[0]+eta*x[1])
 def state(x):
  A,B,C=x;N=sum(x);out=lint=F(0)
  for source,target,rate0 in raw:
   rate=rate0*ff(x,source)
   if not rate:continue
   xp=tuple(a-b+d for a,b,d in zip(x,source,target));out+=rate*(t**(sum(target)-sum(source))*h(xp)/h(x)-1)
   if sum(source)==sum(target):lint+=rate*(h(xp)-h(x))
  if not A:assert lint==0 and out<=-lam/2
  else:
   R=A+eta*B;neg=c*A*(u*B*B+v*C*C)/(2*(1+c)*R*R)
   assert lint/h(x)<=c*K*A-neg
   assert out<=C0-3*D*A/4-neg
   if A>=Ac or B>=Bc or C>=Cc:assert out<=-zeta
  return out
 count=0
 for N in range(limit+1):
  for x in comps(N,3):state(x);count+=1
 points=[]
 for A in [0,1,2,Ac-1,Ac,Ac+1]:
  for B in [0,Bc-1,Bc,Bc+1]:
   for C in [0,Cc-1,Cc,Cc+1]:points.append((A,B,C))
 for M in [10**6,10**50]:points += [(0,0,M),(0,M,0),(1,0,M),(1,M,0),(2,0,M),(M,M,M)]
 for x in points:state(x)
 return {'case':label,'rates':list(map(str,rates)),'t':str(t),'eta':str(eta),'c':str(c),'K':str(K),'C0':str(C0),'zeta':str(zeta),'eta_trials':trials,'guaranteed_eta':str(guaranteed_eta),'A_cut':Ac,'B_cut':Bc,'C_cut':Cc,'ordinary_checks':count,'boundary_huge_checks':len(points),'finite_box_not_enumerated':True}

def aggregate_no_go_checks():
 rates=[F(2,3),F(7,5),F(1,2),F(3,4),F(5,7),F(2,9),F(11,3),F(13,5)];lam,mu,a1,b1,a2,b2,a3,b3=rates;raw=hard_raw(rates)
 def agg(x):
  initial=(x[0],sum(x));out={}
  for u,v,k in raw:
   rate=k*ff(x,u)
   if not rate:continue
   y=tuple(a-b+c for a,b,c in zip(x,u,v));dest=(y[0],sum(y))
   if dest==initial:continue
   out[dest]=out.get(dest,F(0))+rate;out[initial]=out.get(initial,F(0))-rate
  return {a:c for a,c in out.items() if c}
 count=0
 for n in [3,4,10,10**6,10**50]:
  assert agg((0,0,n-1))=={(1,n):lam,(0,n-1):-lam}
  assert agg((1,0,n-1))=={(2,n+1):lam,(0,n-1):mu,(1,n):-lam-mu}
  loss=2*a2*(n-2);assert agg((2,0,n-2))=={(3,n+1):lam,(1,n-1):2*mu,(1,n):loss,(2,n):-lam-2*mu-loss};count+=3
 eps=min(F(1,100),lam**2/(4*(lam+mu)));r=1-eps/lam;s=(lam+mu-eps-mu/r)/lam;q=(lam+2*mu-eps)/(2*a2);rho=(1+s)/2
 assert 0<s<r<1 and s>F(5,12);n0=max(3,2+ceil(2*s*q/(1-s)))
 assert s*(1+q/F(n0-2))<=rho<1
 paths=[[(1,0,1),(2,0,1),(1,2,0),(2,2,0),(1,2,1),(1,1,2),(1,0,3)],[(1,0,2),(2,0,2),(2,1,1),(1,1,2),(1,0,3)]]
 for k in [2,3,10,10**6]:paths.append([(1,0,k),(2,0,k),(2,1,k-1),(1,1,k),(1,0,k+1)])
 for k in [1,2,10,10**6]:paths.append([(0,0,k),(1,0,k),(2,0,k),(3,0,k)])
 edges=0
 for path in paths:
  for x,y in zip(path,path[1:]):
   assert any(ff(x,u)>0 and tuple(a-b+c for a,b,c in zip(x,u,v))==y for u,v,k in raw)
   assert any(ff(y,u)>0 and tuple(a-b+c for a,b,c in zip(y,u,v))==x for u,v,k in raw);edges+=1
 return {'aggregate_generator_row_identities':count,'closed_class_edges_with_enabled_reverses':edges,'epsilon':str(eps),'r':str(r),'s':str(s),'rho':str(rho),'acquired_contraction_index':n0}

def main():
 base=[baseline('generic_nonCB_with_neutral_high_order',1,1,[1,2],[1,1]),baseline('near_one',1,1,[1,2],[1,1],F(65,64)),baseline('c_cap_one',1,100,[1],[1],limit=24),baseline('three_satellites',F(2,3),F(7,5),[1,2,F(1,7)],[F(3,4),2,F(1,11)],limit=12)]
 hard=[inverse('mediated_lift_nonCB',[1,1,1,1,1,1,2,1]),inverse('near_one',[1,1,1,1,1,1,2,1],F(65,64)),inverse('heterogeneous_rates',[F(2,3),F(7,5),F(1,2),F(3,4),F(5,7),F(2,9),F(11,3),F(13,5)],limit=12),inverse('large_requested_base',[1,1,1,1,1,1,2,1],F(100),limit=10)]
 print(json.dumps({'direct_star_baselines':base,'inverse_mass_mechanism_cases':hard,'aggregate_no_go_exact_controls':aggregate_no_go_checks(),'finite_tests_supplement_ordinary_proofs':True},indent=2))
if __name__=='__main__':main()

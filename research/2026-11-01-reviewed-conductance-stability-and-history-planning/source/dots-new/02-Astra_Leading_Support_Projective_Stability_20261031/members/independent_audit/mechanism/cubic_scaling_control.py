#!/usr/bin/env python3
"""Exact top-degree lift: validates the essential p-dependent normalization."""
from fractions import Fraction as F
from exact_mechanism_checks import raw,mul,add,scale,generator_poly,ev,ff,comps
import json
rates=[1,1,1,1,2,1,1,1];base=raw(rates)
internal=[]
for u,w,k in base[2:]:
 for j in range(3):
  e=tuple(int(i==j) for i in range(3))
  internal.append((tuple(a+b for a,b in zip(u,e)),tuple(a+b for a,b in zip(w,e)),k))
rs=base[:2]+internal
H={(1,1,0):F(2),(1,0,1):F(2),(0,1,1):F(1)}
Np={(1,0,0):F(1),(0,1,0):F(1),(0,0,1):F(1)}
L2=generator_poly(base[2:],H);L3=generator_poly(internal,H)
assert L3==mul(add(Np,{(0,0,0):-F(2)}),L2)
G3={a:c for a,c in L2.items() if sum(a)==3};G4={a:c for a,c in L3.items() if sum(a)==4}
assert G4==mul(Np,G3)
assert ev(G3,(4,3,3))==-3 and ev(G4,(4,3,3))==-30
assert all(c>=0 for a,c in G4.items() if a[0]==0)
beta=min(G4[(0,4,0)],G4[(0,0,4)]);assert beta==1
K=sum(-c for a,c in G4.items() if a[0] and c<0)
rem={a:c for a,c in L3.items() if sum(a)<=3};CR=sum(abs(c) for c in rem.values())
t=F(2);D=F(1,2);eps=min(F(1,2),D/(4*K));C=t/(1-eps)-1+2*eps/(t*(1-eps))+eps*CR/(1-eps)
kap=min(D/4,eps*beta/(2**7*2**3))
def quotient(x,power):
 N=sum(x);h=1-eps*ev(H,x)/F((N+1)**power);out=F(0)
 for u,w,k in rs:
  rate=k*ff(x,u)
  if not rate:continue
  xp=tuple(a-b+c for a,b,c in zip(x,u,w));hp=1-eps*ev(H,xp)/F((sum(xp)+1)**power)
  out+=rate*(t**(sum(w)-sum(u))*hp/h-1)
 return out
count=0
for N in range(17):
 for x in comps(N):
  assert ev(L3,x)==(N-2)*ev(L2,x)
  assert quotient(x,3)<=C-kap*N
  count+=1
rows=[]
for n in [10**3,10**6,10**50]:
 x=(4*n,3*n,3*n);bad=quotient(x,2);good=quotient(x,3)
 assert ev(L2,x)==-3*n**3-87*n**2+6*n
 assert ev(L3,x)==-30*n**4-864*n**3+234*n**2-12*n
 assert bad>0 and good<0 and good<=C-kap*sum(x)
 if n>=10**6:assert C-kap*sum(x)<0
 rows.append({'n':n,'unattenuated_power2_quotient':str(bad),'corrected_power3_quotient':str(good),'corrected_linear_upper_bound':str(C-kap*sum(x))})
print(json.dumps({'exact_generator_multiplier':'L3=(N-2)L2','top_order_leading_relation':'G4=N G3',
 'ray_G3_at_4n3n3n':'-3 n^3','ray_G4':'-30 n^4','beta':str(beta),'K':str(K),'C_R':str(CR),
 'epsilon':str(eps),'C0':str(C),'kappa':str(kap),'ordinary_exact_corrected_checks':count,
 'scaling_negative_controls':rows},indent=2))

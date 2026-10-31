#!/usr/bin/env python3
"""Independent finite support certificates and coefficient-elevation identities."""
from fractions import Fraction as F
from math import prod,factorial
from exact_mechanism_checks import raw,ff,mul,power,add,scale,ev
import json

def support_closures(rs,n,A,p):
 out=[]
 for seed in range(n):
  S={seed};history=[]
  while True:
   change=False
   for row,(u,v,k) in enumerate(rs):
    if sum(u)==p and all(u[i]==0 or i in S for i in range(n)):
     nxt={i for i in range(n) if v[i]};new=nxt-S
     if new:
      history.append({'row':row,'before':sorted(S),'added':sorted(new)});S|=new;change=True
   if not change:break
  assert all(not(sum(u)==p and all(not u[i] or i in S for i in range(n))) or all(not v[i] or i in S for i in range(n)) for u,v,k in rs)
  out.append({'seed':seed,'terminal':sorted(S),'reaches_A':A in S,'history':history})
 return out

base=raw([1,1,1,1,2,1,1,1]);closed=support_closures(base[2:],3,0,2);assert all(x['reaches_A'] for x in closed)
cubic=[]
for u,v,k in base[2:]:
 for j in range(3):
  e=tuple(int(i==j) for i in range(3));cubic.append((tuple(a+b for a,b in zip(u,e)),tuple(a+b for a,b in zip(v,e)),k))
closed3=support_closures(cubic,3,0,3);assert all(x['reaches_A'] for x in closed3)
A=(1,0,0);B=(0,1,0);C=(0,0,1);z=(0,0,0);BB=(0,2,0);CC=(0,0,2)
stable=[(z,A,F(1)),(A,z,F(1)),(A,B,F(1)),(B,A,F(1)),(A,C,F(1)),(C,A,F(1)),(BB,CC,F(1)),(CC,BB,F(1))]
failed=support_closures(stable[2:],3,0,2);assert failed[1]['terminal']==failed[2]['terminal']==[1,2]
checks=0
for a in range(9):
 for b in range(9):
  for c in range(9):
   x=(a,b,c);quot=F(0)
   for u,v,k in stable:
    quot+=k*ff(x,u)*(F(4)**(v[0]-u[0])*F(5)**(v[1]+v[2]-u[1]-u[2])-1)
   assert quot==3-F(a,4)-F(b+c,5);checks+=1
# A boundary polynomial positive everywhere but with negative initial coefficients.
Nb={(0,1,0):F(1),(0,0,1):F(1)}
g={(0,2,0):F(1),(0,1,1):-F(1),(0,0,2):F(1)}
identity_checks=0;coupling_checks=0;elevations=[]
for q in [2,3,5]:
 poly=mul(g,power(Nb,q-2));S=sum(abs(c) for c in poly.values())
 for r in range(q,13):
  exact=mul(poly,power(Nb,r-q));mn=None
  for b in range(r+1):
   gamma=(0,b,r-b);den=prod(range(r-q+1,r+1))
   coeff=sum(c*ff(gamma,alpha)/F(den) for alpha,c in poly.items())
   mult=F(factorial(r),factorial(b)*factorial(r-b));assert coeff==exact.get(gamma,F(0))/mult
   value=ev(poly,tuple(F(x,r) for x in gamma));assert abs(coeff-value)<=S*F(q*(q-1),2*r)
   mn=coeff if mn is None else min(mn,coeff);identity_checks+=1;coupling_checks+=1
  elevations.append({'q':q,'r':r,'minimum_normalized_coefficient':str(mn)})
assert next(x for x in elevations if x['q']==2 and x['r']==4)['minimum_normalized_coefficient']=='0'
assert F(next(x for x in elevations if x['q']==2 and x['r']==5)['minimum_normalized_coefficient'])>0
print(json.dumps({'quadratic_success_closures':closed,'cubic_success_closures':closed3,
 'stable_all_degree_obstruction_closures':failed,'stable_direct_Foster':'V=4^A5^(B+C), LV/V=3-A/4-(B+C)/5',
 'stable_exact_checks':checks,'normalized_coefficient_identities_checked':identity_checks,
 'coupling_error_bounds_checked':coupling_checks,'elevation_examples':elevations},indent=2))

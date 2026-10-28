#!/usr/bin/env python3
"""Exact rational guards and fixed-cap constants for the acquired-excitation source."""
from fractions import Fraction as F
from pathlib import Path
import json

def ceil_log2(x):
 k=0
 while F(2)**k<x:k+=1
 return k
cases=[];guard_cases=0
for n,q,w in [(3,1,3),(4,2,2),(6,3,2),(8,4,3),(2,2,1)]:
 W=min(n,3*w-2);d=2**W;C=min(q,2*W-1);K=min(q,W+2*(C-1)*(W-1));A=min(q,K*K)
 for eps in [F(1),F(1,10),F(7,1000)]:
  b=F(1)
  while b*b>eps/F(18*A*q):b/=2
  assert b<=F(1,4) and b*b>eps/F(72*A*q)
  for kap in [F(1),F(1,17),F(1,1000)]:
   for mu in [F(1),F(1,10)]:
    r=mu/d;s=0
    while F(1,16*d*2**s)>b*kap*r/5:s+=1
    funded=s+2;beta=eps/8;beta1=beta/2;L=ceil_log2(F(6*d*q*(funded+1),1)/beta1)
    Ns=[]
    for k in range(funded+1):
     a=F(1,16*d*2**k);N=8*3**W*L/a**2;assert N.denominator==1;N=int(N);Ns.append(N)
     denom=2*(2*3**W+F(4*d,3)*a)
     assert denom<=5*3**W
     exponent=N*a*a/denom;assert exponent>=L
    assert F(6*d*q*(funded+1),2**L)<=beta1
    base=Ns[0];assert sum(Ns)==base*(4**(funded+1)-1)//3
    assert sum(Ns[:s+1])<F(4,3)*Ns[s]
    a=F(1,16*d*2**s);l=r-F(5,2)*a;e=F(5,4)*a
    assert l>=r/2 and 5*a<=2*b*kap*l and e<kap*l
    sign_bound=2*e/(2*kap*l-e);assert sign_bound<=b
    cap=F(57600*A*q*3**W*L,1)/(kap*kap*r*r*eps)+1;assert Ns[s]<=cap
    # Direct gap sufficiency with gamma=kap*r and a<=b gamma/5.
    gamma=kap*r;h=gamma-e
    assert h>e and 10*a<=b*(8*h-5*a)
    assert 2*e/(2*h-e)<=b/(4-F(3,2)*b)<b
    assert F(9,2)*A*q*b*b<=eps/4
    assert eps/4+beta+eps/4<eps
    guard_cases+=2
    cases.append({'n':n,'q':q,'w':w,'W':W,'epsilon':str(eps),'kappa':str(kap),'mu':str(mu),'b':str(b),'success_stage':s,'funded_last_stage':funded,'N_success':Ns[s],'all_fine_cap':sum(Ns),'signed_op_bound':str(sign_bound)})
r={'status':'PASS exact guard and budget constants','source_draws':0,'rng_draws':0,'budget_cases':len(cases),'acceptance_guard_cases':guard_cases,'cases':cases}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='cases'},indent=2))

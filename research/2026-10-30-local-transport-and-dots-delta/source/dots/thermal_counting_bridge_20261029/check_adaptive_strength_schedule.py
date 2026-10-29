from fractions import Fraction as F
from math import isqrt
import random,json
from pathlib import Path
rng=random.Random(20261029)
def ceil(x):return (x.numerator+x.denominator-1)//x.denominator
def ceil_log2(x):
 j=max(0,x.numerator.bit_length()-x.denominator.bit_length())
 while F(2)**j<x:j+=1
 while j and F(2)**(j-1)>=x:j-=1
 return j
def ceil_sqrt(x):
 j=isqrt(x.numerator//x.denominator)
 if j*j*x.denominator<x.numerator:j+=1
 return j
maxdj=F(0);maxerr=F(0);examples=[];checks=0
for _ in range(2500):
 n=rng.choice([1,2,7,100,100000]);k=rng.randint(1,4)
 tau=F(1,rng.choice([1,2,3,10,100,10000]));g=F(rng.randint(1,30),rng.randint(1,7))
 if g<=tau/4:continue
 a=tau*n/4;L=a+(g*n-a)*F(rng.randint(1,1000),1000)
 q=ceil(512*L*L/(tau*tau*n));J=L/q;lam=q*g/L
 D=ceil(9*lam)+ceil_log2(200*g/tau)
 assert tau*tau/(528*g)<=J<tau/128
 assert D*J<10*g
 K=20*k*k*g;beta=4/tau
 r=max(1,ceil(2*K*beta),ceil_sqrt(F(64,9)*K*K*beta*beta*g/tau))
 delta=beta/r;theta=tau/(4*g);eta=delta*theta*J/16
 B=ceil_log2(2*(2**k)/eta)
 assert F(1,2**B)<=eta/(2*(2**k))
 assert K*delta<=F(1,2) and delta*J<1 and eta<F(1,4)
 error=4*g*K*K*beta*beta/(3*r*r*(1-(K*delta)**2))
 assert error<=tau/4
 checks+=1;maxdj=max(maxdj,D*J/g);maxerr=max(maxerr,error/tau)
 if len(examples)<8:examples.append({'n':n,'k':k,'tau':str(tau),'g':str(g),'q':q,'D':D,'r':r,'B':B,'DJ_over_g':float(D*J/g),'error_over_tau':float(error/tau)})
out={'seed':20261029,'exact_rational_schedules_checked':checks,'maximum_DJ_over_g':float(maxdj),'maximum_Trotter_error_over_tau':float(maxerr),'examples':examples,'scope':'Exact rational resource inequalities and least-integer schedules; no full #SAT solver or rare-probability validation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

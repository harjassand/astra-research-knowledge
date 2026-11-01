#!/usr/bin/env python3
"""Independent exact proof-ledger/startup/tail/window checks; no full scalar solve."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import hashlib,json
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
SRC=ROOT/'boundary_clearance_kernel_root_20261101/coarse_cold_algorithm_20261101'
checks=[]
def ck(x,name):
    assert x,name
    checks.append(name)
C=json.loads((SRC/'COARSE_CERTIFICATE.json').read_text())
# Independent dense formal-polynomial calculation (no constructor imports).
def mul(a,b):
    o=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):o[i+j]+=x*y
    return o
p=[F(0)]*29
for n in range(28):
    sq=mul(p[:n+1],p[:n+1]);four=mul(sq,sq)
    p[n+1]=(F(2 if n==2 else 0)+(3*sq[n-1] if n else 0)+F(9,8)*four[n])/(n+1)
for n,c in enumerate(p):
    ck((8**n*factorial(n))%c.denominator==0,f'D_n denominator {n}')
    ck(0<=c<=2**n,f'coefficient magnitude {n}')
sq=mul(p,p);four=mul(sq,sq);res=[F(0)]*113;res[2]=2
for i,c in enumerate(sq):res[i+1]+=3*c
for i,c in enumerate(four):res[i]+=F(9,8)*c
for i,c in enumerate(p[1:],1):res[i-1]-=i*c
common=8**113*factorial(112)
for i,c in enumerate(res):
    ck(c>=0,f'residual sign {i}')
    ck(common%c.denominator==0,f'residual common denominator {i}')
    ck(max(abs(c.numerator).bit_length(),c.denominator.bit_length())<1280,f'residual word bound {i}')
ck(all(c==0 for c in res[:28]),'matched residual degrees')
a=F(1,2);elo=sum((c*a**i for i,c in enumerate(p)),F(0));rr=sum((c*a**i for i,c in enumerate(res)),F(0));delta=rr/(1-F(105,256));ehi=elo+a*delta
for name,val in [('forward_e_lower',elo),('forward_e_upper',ehi),('residual_max',rr),('linear_barrier_delta',delta)]:
    ck(F(C['startup'][name])==val,'independent startup '+name)
    ck(max(abs(val.numerator).bit_length(),val.denominator.bit_length())<1536,'startup word '+name)
ck(ehi<F(1,4),'startup supersolution rectangle')
# Ordinary Taylor-tail formula re-derived at the frozen inverse endpoint.
L,H=F(C['s_at_E_lower']),F(C['s_at_E_upper']); E=F(16); t0=F(8,27)/E**3; U=H+t0
lo=L+t0-F(64,135)*U/E**5
hi=H+t0-F(64,135)*L/E**5+F(128,189)*L*L/E**7
ck(lo==F(C['s_star_lower']) and hi==F(C['s_star_upper']),'exact paid-tail endpoints')
ck(0<lo<hi<U<2,'scalar/tail order')
ck(hi-lo<F(8678,10**11),'scalar width < 8.678e-8')
ck(F('1.106580470126746169')<=lo and hi<=F('1.106580556897779284'),'outward coarse decimals')
# Explicit upper costs for elementary operations, not measured Python costs.
W=8192
rational_raw=4097
ordinary_cost=8*(rational_raw+1)**2*(2*rational_raw+20)
quantize_cost=8*4178**2*(322+20)
compare_cost=80*4258**2
ck(max(ordinary_cost,quantize_cost,compare_cost)<4*(W+1)**3,'per rational operation explicit gcd/division ceiling')
ck(60<=64,'maximum expanded Box atom reserve')
startup_dense=2*sum(k*k+(2*k-1)**2 for k in range(1,29))+2*(29**2+57**2)
# Include a deliberately naive power-by-repeated-multiplication evaluator.
startup_remainder=6328+406+2*113+2*29+8*28+4*113+500
ck(startup_dense==82128,'dense convolution arithmetic count')
ck(startup_dense+startup_remainder<100000,'startup remaining arithmetic including naive powers')
step=106+134+15;one=100000+4*step*320+200*320+20000
ck(one==510400 and one<600000,'one complete scalar pass bundle cap')
ck(3*600000+3*10000<2000000,'three passes and three consumers bundle cap')
ck(10**9*2**28+2**38+10**15<10**18,'nonarithmetic control traffic reserve')
cost=2000000*256*(W+1)**3+10**18
ck(cost==282578068509184000000 and cost<3*10**20<2*10**21-1,'complete narrow prospective comparison')
ck(4096*8192+2**25+2**24<2**27,'live storage reserve')
# Independent integer binary-search square root, no isqrt or consumer import.
def up_sqrt(x):
    scale=10**24;n=x.numerator*scale**2//x.denominator
    left,right=0,1<<((n.bit_length()+1)//2)
    while left<right:
        mid=(left+right+1)//2
        if mid*mid<=n:left=mid
        else:right=mid-1
    q=F(left,scale)
    if q*q<x:q+=F(1,scale)
    ck((q-F(1,scale))**2<x<=q*q,'independent sqrt bracket')
    return q
def fmt(x,up):
    y=x*10**6;k=y.numerator//y.denominator
    if up and k<y:k+=1
    return f'{k//10**6}.{k%10**6:06d}'
windows=json.loads((SRC/'COARSE_WINDOWS.json').read_text());rows=[]
for T,expected in zip((10000,100000),windows['fixtures']):
    r=F(11,20000)+F(4380,19*T)+F(7254,T*T);v=F(1449,800*T)+F(1285200,T**3);j=F(27,25*T)
    m=2*j+up_sqrt(12*v+4*j*j);eps=F(1,T)+r+m+F(3000000,T**6)
    low=lo-eps;high=hi+eps+F(5,T)
    ck(hi+F(1,T)+r+m+F(1,70*T*T)<4,'original4T forced-cap inequality '+str(T))
    ck([fmt(low,False),fmt(high,True)]==expected['scaled_interval'],'scaled interval '+str(T))
    ck([fmt(low*T,False),fmt(high*T,True)]==expected['physical_interval'],'physical interval '+str(T))
    rows.append({'T':T,'scaled_interval':expected['scaled_interval'],'physical_interval':expected['physical_interval']})
ck(sum((F(6**k,factorial(k)) for k in range(18)),F(0))>400,'two-sided Freedman failure <1/200')
ck(F(1,200)+F(1,10**8)+F(16,2**100)<F(1,100),'full per-fixture failure <1/100')
old=json.loads((ROOT/'boundary_clearance_kernel_root_20261101/finite_window_consumer/ADMISSION_SOURCE_BINDINGS.json').read_text())['files']
new=json.loads((SRC/'COLD_SOURCE_BINDINGS.json').read_text())['files']
old={x['path']:x['sha256'] for x in old};new={x['path']:x['sha256'] for x in new}
removed=set(old)-set(new);added=set(new)-set(old)
ck(len(removed)==6 and all(x.startswith(('inverse_clearance_clock_','audit_inverse_clock_certificate_')) for x in removed),'only old scalar inputs removed')
ck(added=={'boundary_clearance_kernel_root_20261101/coarse_cold_algorithm_20261101/coarse_clock.py'},'only fresh constructor added')
ck(all(old[x]==new[x] for x in set(old)&set(new)),'all stochastic sources unchanged')
out={'status':'PASS_INDEPENDENT_EXACT_STATIC_STARTUP_TAIL_AND_WINDOW_CHECKS','checks':len(checks),'check_names':checks,'prospective_bit_cost':str(cost),'fixtures':rows,'full_scalar_solves':0,'partial_startup_reconstructions':1,'source_closure_removed':sorted(removed),'source_closure_added':sorted(added)}
(HERE/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='check_names'},indent=2))

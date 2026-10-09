#!/usr/bin/env python3
"""Exact target second-moment enclosure, not a universal null variance claim.
Run at portable package root. Requires only stdlib and the exact witness files.
"""
from fractions import Fraction as F
from pathlib import Path
import runpy,sys,json,math,time,hashlib
root=Path(__file__).resolve().parents[2]
start=time.perf_counter();sys.argv=['exact_witness.py','--half']
a=runpy.run_path(str(root/'work/discrete_critic/exact_witness.py'))
P=a['P'];labels=a['labels'];ff=a['ff'];dd=a['dd'];gg=a['gg'];q=a['q'];dot=a['dot']
def ceil(x):return -((-x.numerator)//x.denominator)
B=40;D=1<<B;A=[[ceil(p*D) for p in row] for row in P]
if not all(F(A[i][j],D)>=P[i][j]>=0 for i in range(10) for j in range(10)):raise RuntimeError('dyadic majorization')
front={(y,):[int(labels[i]==y) for i in range(10)] for y in range(6)}
for _ in range(4):
 new={}
 for word,vec in front.items():
  moved=[sum(vec[i]*A[i][j] for i in range(10)) for j in range(10)]
  for y in range(6):new[word+(y,)]=[moved[i] if labels[i]==y else 0 for i in range(10)]
 front=new
num=0
for w,vec in front.items():
 fm=ff[w[2],w[1]];fp=ff[w[2],w[3]];p0=F(w[2]==0)
 s2=dot(fm[1:3],fp[1:3]);rh=dot(dd[w[2],w[1]],dd[w[2],w[3]]);rt=dot(gg[w[2],w[1],w[0]],gg[w[2],w[3],w[4]])
 sq=q[0]*p0+q[1]*(fm[1]+fp[1])/2+q[2]*(fm[2]+fp[2])/2+q[3]*fm[1]*fp[1]+q[4]*(fm[1]*fp[2]+fm[2]*fp[1])/2
 W=sq+a['circle']*(p0-s2)+a['alpha']*(p0+s2)+a['beta']*p0+a['lam']*rh+a['mu']*rt
 num+=sum(vec)*ceil(W*W)
upper=F(num,10*D**4);V=ceil(upper);Delta=a['certgap'];span=a['hi']-a['lo']
# Strict inequality achieved by +1, all comparisons rational.
n=max(ceil(160*V/(Delta*Delta)),ceil(80*span/Delta),2)+1
if not F(n)>160*V/(Delta*Delta) or not F(n)>80*span/Delta:raise RuntimeError('planning count')
report={'status':'PASS','epsilon':str(a['eps']),'source_seed_sha256':hashlib.sha256((root/'work/hidden_equilibrium/certificate.txt').read_bytes()).hexdigest(),'method':'nonnegative entrywise dyadic majorization of transition probabilities; exact integer forward recursion and ceil of exact rational W squared','transition_dyadic_bits':B,'words':len(front),'second_moment_upper_exact':str(upper),'second_moment_upper_integer':V,'certified_gap':str(Delta),'range_width':span,'empirical_bernstein_windows':n,'type_I_at_most':'.025','target_power_at_least':'.975','planning_formula':'n > max(160 V/Delta^2, 80 R/Delta, 2); log80<5','conditional_on':'proved universal mean inequality and exact target mean; iid stationary windows of one fixed law; independent internal analytic review only','elapsed_seconds':time.perf_counter()-start}
out=root/'work/root/DISCRETE_VARIANCE_CERTIFICATE.json';out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','second_moment_upper_integer','empirical_bernstein_windows','elapsed_seconds']},indent=2))

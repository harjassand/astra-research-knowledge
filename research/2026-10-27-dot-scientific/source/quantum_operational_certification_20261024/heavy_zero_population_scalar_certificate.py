"""Exact rational log checks for heavy_zero_population_scalar_theorem.md."""
from fractions import Fraction as F
import json
from pathlib import Path
N=160

def log_iv(q):
 q=F(q);z=(q-1)/(q+1)
 c=2*sum((z**(2*k+1)/F(2*k+1) for k in range(N)),F(0))
 e=2*abs(z)**(2*N+1)/(F(2*N+1)*(1-z*z))
 return c-e,c+e

def linear(terms,const=0):
 lo=hi=F(const)
 for coeff,q in terms:
  a,b=log_iv(q);coeff=F(coeff)
  lo+=coeff*(a if coeff>=0 else b);hi+=coeff*(b if coeff>=0 else a)
 return lo,hi

def B(a):
 t=1-a
 return linear([(t,t),(-(1+a),1+a),(1+a,4),(-1,3)])
def D(a):return linear([(1,4/(1-a*a))],-2)
checks={
 'log4_lt_3_over_2':log_iv(4)[1]<F(3,2),
 'B_two_thirds_gt_minus_571_over_100000':B(F(2,3))[0]>-F(571,100000),
 'abs_D_two_thirds_lt_26_over_1000':D(F(2,3))[0]>-F(26,1000) and D(F(2,3))[1]<F(26,1000),
 'B_11_over_20_gt_1_over_100':B(F(11,20))[0]>F(1,100),
 'B_4_over_5_gt_1_over_100':B(F(4,5))[0]>F(1,100),
 'D_11_over_20_negative':D(F(11,20))[1]<0,
 'D_4_over_5_positive':D(F(4,5))[0]>0,
 'global_B_bound_gt_minus_6_over_1000':-F(571,100000)-F(3,8)*F(26,1000)**2>-F(6,1000),
}
def R(a):return 3*a*a*(2*a-1)*(1-a)/(2*(11*a-4))
checks['R_11_over_20_gt_9_over_1000']=R(F(11,20))>F(9,1000)
checks['R_4_over_5_gt_9_over_1000']=R(F(4,5))>F(9,1000)
assert all(checks.values()),checks
out={'method':'Exact Fraction arithmetic; 160-term atanh log series with geometric rational tails','checks':checks,'diagnostics':{str(a):{'B_interval':[float(x) for x in B(a)],'D_interval':[float(x) for x in D(a)],'R_exact':str(R(a))} for a in [F(11,20),F(2,3),F(4,5)]}}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

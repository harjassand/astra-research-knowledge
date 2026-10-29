"""Exact conservative diagnostic; caller supplies genuine observed counters."""
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path

def sqrt_upper(q):
 q=F(q);assert q>=0
 r=isqrt(q.numerator//q.denominator)
 return r+(r*r*q.denominator<q.numerator)

def certificate(T,m,p,R,M,observed_gap,observed_squared_feedback,b,a,alpha,Gamma=0,ke=20,km=20,kv=20,d=35,L=720):
 T=int(T);m=int(m);p=F(p);R=F(R);a=F(a);alpha=F(alpha);Gamma=F(Gamma)
 E=F(observed_gap);V=F(observed_squared_feedback)
 assert T>=1 and m>=1 and 0<p<=1 and R>0 and M>=1 and E>=0 and V>=0
 assert Gamma>=0 and 0<a<=1 and alpha>0 and b>=0 and all(isinstance(k,int) and k>=1 for k in (ke,km,kv))
 B=F((T-1)*L,p)+d*R
 assert E<=m*T*B and V<=m*T*(F(L,p))**2
 U=2*E+2*m*B*ke
 H=F(m*d,4)*R+V/(4*R)+L*sqrt_upper(F(m*T,R)*U+F(m*m*d*T*T,M))+m*(1+F(L,p))*sqrt_upper(2*T*km)
 validation=sqrt_upper(F(T*kv,2));threshold=a*alpha*(Gamma+H)+validation
 return {'gap_mean_sum_upper':str(U),'true_regret_upper':str(H),'failure_count_upper':str(threshold),'threshold_strictly_passes':threshold<b+1,'declared_joint_failure_budget_excluding_role_shortage':str(F(1,2**ke)+F(1,2**km)+F(1,2**kv)),'qualification':'Numeric pass is only a joint false-readiness bound with valid comparator promise, verified code and no non-source abort; not a conditional success/error probability.'}

def main():
 rows=[]
 for h in [5,20,40,80,120,160]:
  Bfield=2**h;N=16*h*Bfield;T=9*N;p=F(1,3);m=3;d=35;L=720
  R=F(1)
  while R*R<F(L*L*T,d*p):R*=2
  M=1
  while M<140*T*T:M*=2
  t=(Bfield//8)*((h+1)//2);b=t//4
  # SYNTHETIC scaling inputs, NOT acquired data or an implemented oracle run.
  E=F(0);V=m*T*F(L*L,p)
  out=certificate(T,m,p,R,M,E,V,b,F(4,9),8)
  rows.append(dict(h=h,T=str(T),b=str(b),synthetic_counter_scope='zero observed gap and nominal probe-frequency worst-size feedback; not acquired data',**out))
 Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'Exact diagnostic implementation and synthetic scale tests only. Actual records must be supplied separately.','cases':rows},indent=2)+'\n')
 for r in rows:print(r['h'],r['threshold_strictly_passes'])
if __name__=='__main__':main()

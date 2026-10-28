"""Finite off-Bell coherence countercontrol, exact spectra and scalar logs."""
from fractions import Fraction as Q
from pathlib import Path
from math import isqrt
import json,time,sys
sys.set_int_max_str_digits(0)
START=time.perf_counter()
import sympy as s
OUT=Path(__file__).resolve().parent
def add(*vs):return(sum(v[0] for v in vs),sum(v[1] for v in vs))
def scale(c,v):return(min(c*v[0],c*v[1]),max(c*v[0],c*v[1]))
def mul(v,w):
 xs=[a*b for a in v for b in w]
 return min(xs),max(xs)
def logs(y):
 z=(y-1)/(y+1);n=24
 lo=2*sum((z**(2*k+1)/Q(2*k+1) for k in range(n)),Q(0))
 return lo,lo+2*z**(2*n+1)/(Q(2*n+1)*(1-z*z))
ln2=logs(Q(2))
def logq(y):
 k=0
 while y<1:y*=2;k-=1
 while y>2:y/=2;k+=1
 return add(logs(y),scale(k,ln2))
def f(v):
 assert v[0]>0
 return mul(v,(logq(v[0])[0],logq(v[1])[1]))
def exact(x):return x,x
def root(x):
 den=2**50;k=isqrt(x.numerator*den*den//x.denominator)
 return Q(k,den),Q(k+1,den)
def pair(center,rad):
 rr=scale(Q(1,2),root(rad))
 return add(exact(center),scale(-1,rr)),add(exact(center),rr)
a=t=Q(1,100)
xl,xh=pair(a+Q(3,2),9+24*t*t)
dx=add(f(xl),f(xh),scale(-1,f(exact(a+3))),scale(-1,f(exact(a))))
dn=[]
for c in [Q(1),Q(1,2),Q(1,2)]:
 lo,hi=pair(a+Q(1,2),1+4*c*c*t*t)
 dn.append(add(f(lo),f(hi),scale(-1,f(exact(a+1))),scale(-1,f(exact(a)))))
difference=add(dx,scale(-2,add(*dn)))
baseline=add(f(exact(a+3)),scale(9,f(exact(a+Q(1,3)))),scale(-6,f(exact(a+1))),scale(-4,f(exact(a))))
actual=add(baseline,difference)
assert difference[1]<-Q(1,10000) and actual[0]>0
assert 101**3>301**2
aa,tt=s.Rational(a),s.Rational(t);l=s.symbols('l')
om=s.zeros(9,1);vv=s.zeros(9,1)
for i in [0,4,8]:om[i]=1
vv[0]=1;vv[4]=-1
H=s.I*(om*vv.T-vv*om.T);X0=aa*s.eye(9)+om*om.T;X=X0+tt*H
pt=s.Matrix(9,9,lambda i,j:X[(j//3)*3+i%3,(i//3)*3+j%3])
NX=((1+3*aa)*s.eye(9)-pt)/2
assert s.simplify(X.charpoly(l).as_expr()-(l-aa)**7*((l-aa-3)*(l-aa)-6*tt**2))==0
assert s.simplify(NX.charpoly(l).as_expr()-(l-aa)**3*((l-aa-1)*(l-aa)-tt**2)*((l-aa-1)*(l-aa)-tt**2/4)**2)==0
omega=(-1+s.sqrt(3)*s.I)/2;total=s.zeros(9)
for z in range(3):
 for b in range(3):
  v=s.zeros(9,1)
  for j in range(3):v[3*j+(j+z)%3]=omega**(b*j)
  P=(v*s.conjugate(v).T/3).applyfunc(s.simplify)
  assert s.simplify(s.trace(P*H))==0
  total+=P
assert all(s.simplify(v)==0 for v in total-s.eye(9))
assert all(sum(H[3*i+b,3*i+c] for i in range(3))==0 for b in range(3) for c in range(3))
trace=3+9*a
out={'status':'EXACT_FINITE_BELL_TWIRL_INCREASES_DELTA','a':str(a),'t':str(t),'trace':str(trace),'Delta_change_raw_interval':list(map(str,difference)),'Delta_change_raw_display':list(map(float,difference)),'Delta_change_normalized_interval':list(map(str,scale(1/trace,difference))),'Delta_perturbed_positive_interval':list(map(str,actual)),'faithful_input_minimum_lower':str(xl[0]),'same_both_marginals':True,'exact_Bell_twirl_of_X':'X0','exact_spectra_checks':True,'Hessian_sign_integer_check':'101^3>301^2','seconds_including_sympy':time.perf_counter()-START,'scope':'Finite counter to Bell-twirl monotonicity, instantiating the known N983 coherence/half-metric obstruction. Perturbed entropy remains positive; no global WH3 counterexample or novelty claim.'}
(OUT/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','Delta_change_raw_display','seconds_including_sympy']},indent=2))

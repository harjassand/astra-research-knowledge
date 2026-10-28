#!/usr/bin/env python3
"""Exact moments, guards, and Loewner steps; no source calls, count sampling or RNG."""
from pathlib import Path
import itertools,json,math
import sympy as s
R=s.Rational
zero=lambda a:a.applyfunc(s.expand)==s.zeros(*a.shape)
tr=lambda a:s.expand(s.trace(a))
frob2=lambda a:tr(a.T*a)

def psd(a):
 # Exact Schur-complement recursion, including semidefinite singular cases.
 a=s.Matrix(a)
 if a!=a.T:return False
 while a.rows:
  if any(a[i,i]<0 for i in range(a.rows)):return False
  pivot=next((i for i in range(a.rows) if a[i,i]>0),None)
  if pivot is None:return zero(a)
  inds=[pivot]+[i for i in range(a.rows) if i!=pivot]
  a=a.extract(inds,inds)
  a=(a[1:,1:]-a[1:,0]*a[0,1:]/a[0,0]).applyfunc(s.cancel)
 return True

def design(m):
 for i in range(m):
  p=s.zeros(m);p[i,i]=1
  yield R(2,m*(m+2)),p
 for signs in itertools.product([-1,1],repeat=m):
  v=s.Matrix(signs)
  yield R(m,(m+2)*2**m),v*v.T/m

def rational_inverse_root(B,tau):
 m=B.rows;Q=s.eye(m)-B/4
 # Tests use dyadic tau, so ceil(log2(32/tau)) is exact integer arithmetic.
 ratio=R(32)/tau;L=ratio.p.bit_length()-1
 assert ratio==2**L
 N=int((4/tau)*L)-1
 P=s.eye(m);C=s.zeros(m)
 for k in range(N+1):
  C+=(R(math.comb(2*k,k),4**k)/2)*P
  P=P*Q
 return C,N

moment_records=[]
for m in range(1,6):
 I=s.eye(m);tau=s.S(1)
 B=s.diag(*[1+R(3*i,max(1,m-1)) for i in range(m)])
 C,N=rational_inverse_root(B,tau)
 assert psd(C*B*C-R(49,64)*I) and psd(I-C*B*C)
 assert psd(2*B-C.inv()**2)
 u=s.ones(m,1);A=I/R(8)+u*u.T/R(16*m)
 assert psd(A) and psd(I-A) and psd(B-A)
 F=C*A*C;L_m=R(m**3*(m+3),4)
 mean=s.zeros(m);second=s.S(0);moment2=s.zeros(m*m)
 weight=s.S(0);isotropic=s.zeros(m)
 for prob,P in design(m):
  weight+=prob;isotropic+=prob*P
  T=R(m*(m+2),2)*P-R(m,2)*I
  ss=tr(C*C*P);numerator=tr(F*P);p=numerator/ss
  assert 0<=p<=1 and 0<ss<=1/tau and frob2(T)==L_m
  mean+=prob*p*ss*T
  second+=prob*p*ss*ss*L_m
  moment2+=prob*s.kronecker_product(P,P)
 assert weight==1 and zero(isotropic-I/m) and zero(mean-F)
 assert second<=L_m/tau
 # Fourth moment checked entrywise via the real sphere tensor rule.
 for i,j,k,l in itertools.product(range(m),repeat=4):
  wanted=R(int(i==j)*int(k==l)+int(i==k)*int(j==l)+int(i==l)*int(j==k),m*(m+2))
  assert moment2[i*m+k,j*m+l]==wanted
 moment_records.append({'m':m,'design_atoms_enumerated_only_for_this_small_check':m+2**m,'inverse_root_series_degree':N,'T_Frobenius_squared':str(L_m),'second_moment':str(second),'exact_mean_F':True,'A_B_noncommuting':not zero(A*B-B*A)})

# Prescribed adversarial matrix-error histories, NOT synthetic acquired count records.
updates=0;noncommuting=0;rounding_records=[]
for m,gamma in itertools.product([2,3],[s.S(1),R(1,2),R(1,8)]):
 I=s.eye(m);u=s.Matrix([i+1 for i in range(m)])
 A=I/16+u*u.T/(16*tr(u*u.T));assert psd(A) and psd(I-A)
 c=gamma/16;a=1/(1-2*c);B=2*I;tau=s.S(1)
 for j in range(9):
  assert psd(B-A-tau*I) and psd(a*A+2*tau*I-B)
  M=s.zeros(m);M[0,1]=M[1,0]=1 if j%2==0 else -1
  # This deterministic estimation perturbation is inside the permitted relative ball.
  Ahat=A+c*tau*M/8
  raw=Ahat+c*B+tau*I/2
  h=s.S(1)
  while h>c*tau/(2*m):h/=2
  rounded=raw.applyfunc(lambda x:h*s.floor(x/h+R(1,2)))
  assert frob2(rounded-raw)<=(c*tau/4)**2
  tau_next=tau/2
  assert psd(rounded-A-tau_next*I)
  assert psd(a*A+2*tau_next*I-rounded)
  assert psd(rounded-tau_next*I) and psd(4*I-rounded)
  noncommuting+=not zero(rounded*A-A*rounded)
  updates+=1;B=rounded;tau=tau_next
  rounding_records.append({'m':m,'gamma':str(gamma),'stage':j,'tau':str(tau)})
# Exact all-history PSD guards reject indefinite and above-cap examples.
assert not psd(s.Matrix([[0,1],[1,0]]))
assert not psd(s.diag(1,-1))
assert psd(s.Matrix([[1,1],[1,1]]))
# First fixed-radius strict-majority center, using squared rational distances only.
median_cases=0
for b in [1,3,5,7,9]:
 c=R(1,16);r=c/12;center=s.Matrix([[R(1,3),R(1,7)],[R(1,7),R(1,4)]])
 good=(b+1)//2;xs=[]
 for i in range(good):xs.append(center+s.diag((-1)**i*r*R(i+1,good),0))
 for i in range(b-good):xs.append(center+s.diag((i+2)*r*4,(-1)**i*7*r))
 eligible=[i for i,x in enumerate(xs) if sum(int(bool(frob2(x-y)<=4*r*r)) for y in xs)>=good]
 assert eligible
 chosen=eligible[0]
 assert frob2(xs[chosen]-center)<=(3*r)**2
 median_cases+=1
# Dyadic stage/cap arithmetic.
cap_cases=0
for epsilon,gamma in itertools.product([R(1),R(1,3),R(1,1000)],[R(1),R(1,7)]):
 target=8/epsilon;J=0
 while 2**J<target:J+=1
 c=gamma/16
 assert R(1,2**J)<=epsilon/8 and 2**J-1<16/epsilon
 assert 2304/c**2*(2**J-1)<9437184/(gamma**2*epsilon)
 assert 1/(1-2*c)<=1+gamma/7
 assert R(3,2)*R(1,2**J)<=R(3,16)*epsilon
 cap_cases+=1
# Sharp m-anchor domination and actual decoder regret for G(x)=|x><x|.
anchor=[]
for m in [1,2,3,5]:
 bar=s.eye(m)/m;P=s.zeros(m);P[0,0]=1
 assert psd(m*bar-P)
 if m>1:assert not psd((m-1)*bar-P)
 # Gauge-controlled logical-Z gives loss Tr(PG); ideal decoder has zero loss.
 local=tr(P*bar);worst=tr(P*P)
 assert worst==m*local==1
 anchor.append({'m':m,'anchor_average_Bell_loss':str(local),'worst_encoder_regret':'1','sharp_domination_factor':m})
out={'status':'PASS','source_calls':0,'RNG_used':False,'count_acquisition_simulated':False,'kind':'exact design moments, prescribed invariant/rounding histories, rational medoid and sharp anchor examples','moment_records':moment_records,'prescribed_Loewner_updates':updates,'updates_noncommuting_with_A':noncommuting,'median_geometry_cases':median_cases,'dyadic_cap_cases':cap_cases,'source_cap_constant':9437184,'all_history_exact_PSD_guard_examples':'PASS','sharp_anchor_examples':anchor,'not_claimed':'These prescribed perturbations are not a count-acquired learner experiment; concentration and runtime are analytic.'}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(p.read_text(),end='')

#!/usr/bin/env python3
"""Exact operator moments, terminal examples and caps; no source calls or RNG."""
import itertools,json,math
from pathlib import Path
import sympy as s
R=s.Rational
tr=lambda a:s.expand(s.trace(a))
zero=lambda a:a.applyfunc(s.cancel)==s.zeros(*a.shape)
def psd(a):
 a=s.Matrix(a)
 if a!=a.T:return False
 while a.rows:
  if any(a[i,i]<0 for i in range(a.rows)):return False
  k=next((i for i in range(a.rows) if a[i,i]>0),None)
  if k is None:return zero(a)
  ids=[k]+[i for i in range(a.rows) if i!=k];a=a.extract(ids,ids)
  a=(a[1:,1:]-a[1:,0]*a[0,1:]/a[0,0]).applyfunc(s.cancel)
 return True

def design(m):
 for i in range(m):
  P=s.zeros(m);P[i,i]=1;yield R(2,m*(m+2)),P
 for ss in itertools.product([-1,1],repeat=m):
  z=s.Matrix(ss);yield R(m,(m+2)*2**m),z*z.T/m

def ceil_log2(x):
 k=0
 while 2**k<x:k+=1
 return k

def C_poly(B,tau):
 m=B.rows;N=int((4/tau)*ceil_log2(32/tau))-1
 Q=s.eye(m)-B/4;term=s.eye(m);C=s.zeros(m)
 for k in range(N+1):
  C+=R(math.comb(2*k,k),2*4**k)*term;term=term*Q
 return C,N

moments=[]
for m,tau in itertools.product([1,2,3,4],[s.S(1),R(1,2)]):
 I=s.eye(m);B=s.diag(*[1+R(3*i,max(1,m-1)) for i in range(m)])
 C,N=C_poly(B,tau);u=s.ones(m,1);A=I/8+u*u.T/(16*m);F=C*A*C
 S=R(m*m*(m+3),4);RR=m*(m+1)
 first=s.zeros(m);second=s.zeros(m);T2=s.zeros(m);atoms=0
 for weight,P in design(m):
  T=R(m*(m+2),2)*P-R(m,2)*I;ss=tr(C*C*P);p=tr(F*P)/ss;Y=ss*T
  assert 0<=p<=1
  first+=weight*p*Y;second+=weight*p*(Y*Y);T2+=weight*(T*T)
  assert psd((RR/tau)**2*I-(Y-F)**2)
  atoms+=1
 assert zero(first-F) and zero(T2-S*I)
 variance=(second-F*F).applyfunc(s.cancel)
 assert psd(variance) and psd((S/tau)*I-variance)
 assert psd((S/tau)*I-second)
 assert psd((RR/tau)**2*I-F*F)
 moments.append({'m':m,'tau':str(tau),'series_degree':N,'design_atoms':atoms,'operator_variance_bound':str(S/tau),'centered_range_bound':str(RR/tau),'noncommuting_A_B':not zero(A*B-B*A),'exact_operator_PSD_checks':True})

terminal=[];O=s.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]]);Z=s.diag(1,-1)
for gamma,epsilon,ls in itertools.product([R(1,2),R(1,8)],[R(1,100),R(1,1000)],[(s.S(0),R(1,2)),(R(1,10),R(3,4)),(R(1,3),R(1,3))]):
 assert epsilon<gamma
 J=ceil_log2(gamma/epsilon);tau=R(1,2**J);a0=R(8,7)
 A=O*s.diag(*ls)*O.T;B=a0*A+R(3,2)*tau*s.eye(2)
 delta=gamma/64;r=2*delta;E=r*tau*Z;M=A+E
 assert psd(B-A-tau*s.eye(2)) and psd(a0*A+2*tau*s.eye(2)-B)
 assert psd(r*B-E) and psd(r*B+E)
 mu=tr(M)/2;h=s.sqrt(((M[0,0]-M[1,1])/2)**2+M[0,1]**2)
 assert h>0
 P=(s.eye(2)-(M-mu*s.eye(2))/h)/2
 assert zero(P*P-P) and tr(P)==1 and s.simplify(tr(M*P)-(mu-h))==0
 p=s.simplify(tr(A*P));pstar=min(ls);uu=gamma/28;v=gamma*tau/16;zeta=epsilon/16
 detailed=(1+uu)/(1-uu)*pstar+(2*v+zeta)/(1-uu)
 simple=(1+2*gamma/27)*pstar+7*epsilon/36
 assert bool(s.simplify(detailed-p)>=0)
 assert bool(s.simplify(simple-detailed)>=0)
 assert bool(s.simplify((1+gamma)*pstar+epsilon/4-simple)>=0)
 terminal.append({'gamma':str(gamma),'epsilon':str(epsilon),'tau':str(tau),'A_eigenvalues':[str(t) for t in ls],'raw_M_can_be_indefinite':not psd(M),'A_M_noncommuting':not zero(A*M-M*A),'terminal_bounds':True})

caps=[]
for m,epsilon,gamma,beta in itertools.product([1,2,5,20],[R(1,2),R(1,7),R(1,1000)],[R(1,2),R(1,10),R(1,10000)],[R(1,10),R(1,10000)]):
 S=R(m*m*(m+3),4);RR=m*(m+1);P=2*S+RR
 def N(tau,delta,L):return int(s.ceiling(P*L/(tau*delta*delta)))
 if epsilon<gamma:
  J=ceil_log2(gamma/epsilon);H=J+1;L=ceil_log2(4*m*H/beta)
  total=sum(N(R(1,2**j),R(1,64),L) for j in range(J))+N(R(1,2**J),gamma/64,L)
  bound=H+16384*P*L/(gamma*epsilon);branch='relative'
 else:
  H=1;L=ceil_log2(4*m/beta);total=N(1,epsilon/16,L)
  bound=1+256*P*L/(gamma*epsilon);branch='additive'
 assert total<=bound and R(2*m*H,2**L)<=beta/2
 # Denominator domination for every prescribed stage accuracy <=1.
 assert 2*S+R(2,3)*RR<=P
 caps.append({'m':m,'epsilon':str(epsilon),'gamma':str(gamma),'branch':branch,'exact_source_cap':total})
assert R(3,16)/(1-R(1,28))==R(7,36)
out={'status':'PASS','source_calls':0,'RNG_used':False,'count_acquisition_simulated':False,'kind':'exact operator moment sums, prescribed terminal-matrix examples and finite arithmetic; not acquired outcomes','operator_variance_fixtures':moments,'terminal_cases':len(terminal),'terminal_cases_with_indefinite_raw_M':sum(x['raw_M_can_be_indefinite'] for x in terminal),'terminal_cases_noncommuting_A_M':sum(x['A_M_noncommuting'] for x in terminal),'finite_cap_cases':len(caps),'relative_regime_cap_cases':sum(x['branch']=='relative' for x in caps),'additive_regime_cap_cases':sum(x['branch']=='additive' for x in caps),'confidence_union_certificate':'2mH*2^(-L)<=beta/2','terminal_additive_constant':'7/36','relative_cap_constant':16384,'matrix_Bernstein_primary_not_reproved':True}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(p.read_text(),end='')

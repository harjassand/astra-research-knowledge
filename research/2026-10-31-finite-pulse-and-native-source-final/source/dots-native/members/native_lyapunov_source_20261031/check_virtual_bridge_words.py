"""Monte Carlo diagnostic of the positive bridge word identity, not a gate backend.
The production proof pays finite-bit/cap errors separately. This uses floats and
fixed bisection for small matrices, with no endpoint rejection sampling.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(771031)
p=np.array([1.,1.])/np.sqrt(2);q=np.array([1.,-1.])/np.sqrt(2)
P=np.outer(p,p);Q=np.outer(q,q);I=np.eye(2);Z=np.diag([1.,-1.]);X=np.array([[0.,1.],[1.,0.]])
proj=[np.kron(P,I),np.kron(Q,I)];H=np.kron(Q,I)
K=np.kron(Z,X)+.3*np.kron(Q,Z);H0=.7*np.kron(I,Z);b=1.3
T=.004;N=20000;rows=[]
for lam in [1e4,1e6]:
 c=b*np.sqrt(lam);r=lam/2;delta=r-2*c;nu=np.sqrt(delta*delta+8*c*c);down=(nu+delta)/2;up=2*c*c/down
 def trans(i,j,t):
  e=np.exp(-nu*t);o=-np.expm1(-nu*t)
  if i==0:return (down+up*e)/nu if j==0 else up*o/nu
  return down*o/nu if j==0 else (up+down*e)/nu
 def bridge(i,j):
  state=i;remaining=T;now=0.;visits=[];events=[]
  for _ in range(64):
   den=trans(state,j,remaining);rate=up if state==0 else down
   atom=np.exp(-rate*remaining)/den if state==j else 0.
   v=rng.random()
   if v>=1-atom:
    visits.append((state,now,T));break
   lo=0.;hi=remaining
   for _ in range(60):
    mid=(lo+hi)/2
    cdf=1-np.exp(-rate*mid)*trans(state,j,remaining-mid)/den
    if cdf<v:lo=mid
    else:hi=mid
   dt=(lo+hi)/2;visits.append((state,now,now+dt));now+=dt;remaining=T-now
   state=1-state;events.append((now,state))
  else:raise RuntimeError('diagnostic cap exceeded')
  assert state==j
  for state,left,right in visits:
   if state==1:
    for t in left+(right-left)*rng.random(rng.poisson(2*c*(right-left))):events.append((float(t),1))
  events.sort();return events
 def free(state,dt):
  U=np.kron(I,np.diag(np.exp(-1j*.7*dt*np.array([1.,-1.]))))
  return proj[state]@U*(.5*np.exp(-r*dt) if state else 1.)
 def word(i,j):
  state=i;last=0.;A=np.eye(4,dtype=complex)
  for t,new in bridge(i,j):
   A=free(state,t-last)@A
   A=(-1j)*proj[new]@(K/b)@proj[state]@A
   last=t;state=new
  return free(state,T-last)@A
 E=expm(T*np.array([[0,c],[2*c,-delta]]))@np.diag([1.,2.])
 estimate=np.zeros((4,4),complex);se2=0.
 for i in range(2):
  for j in range(2):
   total=np.zeros((4,4),complex);total2=np.zeros((4,4))
   for _ in range(N):
    A=word(i,j);total+=A;total2+=abs(A)**2
   mean=total/N;var=np.maximum(0,total2/N-abs(mean)**2)
   estimate+=E[j,i]*mean;se2+=E[j,i]**2*np.sum(var)/N
 exact=expm(T*(-1j*H0-1j*np.sqrt(lam)*K-lam*H))
 err=float(np.linalg.norm(estimate-exact));se=float(np.sqrt(se2))
 wrong_exact=expm(T*(-1j*H0+np.sqrt(lam)*K-lam*H))
 phase_gap=float(np.linalg.norm(wrong_exact-exact))
 assert err<=10*se+1e-8
 rows.append({'lambda':lam,'time':T,'samples_per_endpoint':N,'frobenius_error':err,'estimated_frobenius_standard_error':se,'error_over_estimated_SE':err/se,'exact_gap_if_minus_i_phase_omitted':phase_gap})
 print(json.dumps(rows[-1]),flush=True)
Path(__file__).with_name('virtual_bridge_word_checks.json').write_text(json.dumps({'scope':'Monte Carlo word-identity diagnostic; not algorithmic precision certification','rows':rows},indent=2)+'\n')

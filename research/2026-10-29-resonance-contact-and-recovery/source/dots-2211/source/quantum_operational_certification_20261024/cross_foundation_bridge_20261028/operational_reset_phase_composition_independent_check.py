#!/usr/bin/env python3
"""Enumerated actual correlated calibration, burn-in and coherent service; no source draws."""
from pathlib import Path
import numpy as np,cmath,json
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);R=(I-2j*(X+Y+Z))/np.sqrt(13)
psi=np.array([np.sqrt(3)/2,.5]);sigma=np.outer(psi,psi);lam=2/3;roots=[(1,0),(0,1),(-1,0),(0,-1)]
CZ=np.diag([1,1,1,-1]);native=np.kron(R,I)@CZ;bell=np.array([1,0,0,1])/np.sqrt(2);Bell=np.outer(bell,bell)
assert np.linalg.norm(R.conj().T@R-I)<1e-14
def reset(rho,t):return lam**t*rho+(1-lam**t)*np.trace(rho)*sigma
def instrument(rho,z,y):
 K=R@np.diag([(1+y*z.conjugate())/2,(1-y*z.conjugate())/2]);return K@rho@K.conj().T/4

def cal(N,t):
 initial=R@np.diag([0.,1.])@R.conj().T;states=[((0,0),initial)]
 for _ in range(N):
  nxt=[]
  for (sx,sy),rho in states:
   rho=reset(rho,t)
   for dx,dy in roots:
    z=complex(dx,dy)
    for y in [-1,1]:nxt.append(((sx+y*dx,sy+y*dy),instrument(rho,z,y)))
  states=nxt
 assert abs(sum(np.trace(r).real for _,r in states)-1)<1e-12
 return states

def ideal_programs(N):
 laws={(0,0):1.}
 for _ in range(N):
  nxt={}
  for (sx,sy),prob in laws.items():
   for dx,dy in roots:
    for y in [-1,1]:
     key=(sx+y*dx,sy+y*dy);nxt[key]=nxt.get(key,0)+prob*np.trace(instrument(sigma,complex(dx,dy),y)).real
  laws=nxt
 return laws

def service(rho,r):
 U=np.kron(native,I);out=U@np.kron(rho,Bell)@U.conj().T
 half=cmath.sqrt(r);D=np.kron(np.kron(I,np.diag([half,half.conjugate()])),I)
 return D@out@D.conj().T

def rotations(key):
 z=complex(*key);return [z/abs(z)] if z else [complex(*r) for r in roots]
def td(A,B):return float(np.abs(np.linalg.eigvalsh(A-B)).sum()/2)
rows=[]
for N in [1,2,3]:
 programs=ideal_programs(N);reflearn=np.zeros((8,8),complex)
 for key,prob in programs.items():
  rs=rotations(key)
  for r in rs:reflearn+=prob*service(sigma,r)/len(rs)
 refexact=service(sigma,1);referr=td(reflearn,refexact)
 for t in [0,1,3,7]:
  states=cal(N,t);actual=np.zeros((8,8),complex);actualexact=np.zeros((8,8),complex)
  for key,rho in states:
   rho=reset(rho,t);actualexact+=service(rho,1);rs=rotations(key)
   for r in rs:actual+=service(rho,r)/len(rs)
  eps=lam**t
  hybrid=td(actual,reflearn);limiterror=td(actual,refexact);sameerror=td(actual,actualexact);targetshift=td(actualexact,refexact)
  assert hybrid<=(N+1)*eps+1e-12
  assert limiterror<=referr+(N+1)*eps+1e-12
  assert targetshift<=eps+1e-12
  assert sameerror<=referr+(N+2)*eps+1e-12
  rows.append({'N':N,'reset_repetitions':t,'enumerated_calibration_records':8**N,'same_program_tie_rule':True,'actual_to_limit_learner':hybrid,'actual_to_limit_exact_inverse':limiterror,'actual_to_same_finite_state_exact_inverse':sameerror,'exact_comparator_start_shift':targetshift,'reference_retired_error':referr,'physical_pointer_reset_allowance':eps})
out={'status':'PASS_ENUMERATED_OPERATIONAL_RESET_PHASE_COMPOSITION_AND_COMPARATOR_DEBITS','source_draws':0,'rng_draws':0,'cases':rows,'scope':'Floating exact-tree enumeration of every ordinary outcome, not Monte Carlo. Complete pointer/payload/reference retained; invisible counter omitted analytically. No initial core acquisition or hardware executed.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cases':len(rows),'source_draws':0},indent=2))

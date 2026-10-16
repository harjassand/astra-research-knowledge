"""Own exact linear-algebra checks; no experimental outcomes or external code."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,time,resource
from pathlib import Path
import numpy as np
from scipy.linalg import expm
resource.setrlimit(resource.RLIMIT_CPU,(120,120))
start=time.process_time(); I=np.eye(2); X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]]); Z=np.diag([1,-1])
paulis=[I,X,Y,Z]
def exact_transfer(h,g,t):
    k=np.sqrt(complex(g*g-4*h*h))
    f=t if abs(k)<1e-14 else np.sinh(k*t)/k
    c=np.cosh(k*t)
    a=np.eye(4,dtype=complex);a[1,1]=np.exp(-2*g*t)
    a[2:,2:]=np.exp(-g*t)*np.array([[c-g*f,-2*h*f],[2*h*f,c+g*f]])
    return np.real_if_close(a)
def generator(H,g,S):
    n=len(H);eye=np.eye(n)
    return -1j*(np.kron(eye,H)-np.kron(H.T,eye))+g*(np.kron(S.T,S)-np.eye(n*n))
def evolve(rho,H,g,S,t):
    return (expm(generator(H,g,S)*t)@rho.reshape(-1,order='F')).reshape(rho.shape,order='F')
def td(A,B):return float(np.linalg.svd(A-B,compute_uv=False).sum()/2)
def pinch(rho,S):return (rho+S@rho@S)/2
def bound(J,g,t):return J*J/g*(t+np.expm1(-2*g*t)/(2*g))
max_channel_error=0.;max_bit_violation=0.;min_twirl_prob=1.
for g in [.3,1.,3.]:
 for h in [0.,.01,.15,.5,1.,3.]:
  for t in [0.,.01,.2,1.,3.]:
   T=exact_transfer(h,g,t)
   direct=np.array([[np.trace(P@evolve(Q,h*X,g,Z,t))/2 for Q in paulis] for P in paulis])
   max_channel_error=max(max_channel_error,float(np.max(abs(T-direct))))
   px=(1+T[1,1]-T[2,2]-T[3,3])/4
   py=(1-T[1,1]+T[2,2]-T[3,3])/4
   pz=(1-T[1,1]-T[2,2]+T[3,3])/4
   pi=(1+T[1,1]+T[2,2]+T[3,3])/4
   min_twirl_prob=min(min_twirl_prob,px,py,pz,pi)
   p=(1-T[3,3])/2
   max_bit_violation=max(max_bit_violation,p-bound(abs(h),g,t))
assert max_channel_error<1e-11 and min_twirl_prob>-1e-12 and max_bit_violation<1e-12
rng=np.random.default_rng(902137)
def randherm(d):
 a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); a=(a+a.conj().T)/2;return a/np.linalg.norm(a,2)
def randstate(d):
 v=rng.normal(size=d)+1j*rng.normal(size=d);v/=np.linalg.norm(v);return np.outer(v,v.conj())
checks=[]
for d in [2,3]:
 for bath_scale in [0.,1.,30.]:
  for J in [.01,.3,1.]:
   B=randherm(d); HB=bath_scale*randherm(d);S=np.kron(Z,np.eye(d));H0=np.kron(I,HB);H=H0+J*np.kron(X,B)
   rho0=np.kron(np.diag([1.,0.]),randstate(d))
   commnorm=float(np.linalg.norm(B@HB-HB@B,2))
   for t in [.03,.5,2.]:
    rho=evolve(rho0,H,1.,S,t); target=expm(-1j*H0*t)@rho0@expm(1j*H0*t)
    wrong=float(np.trace(rho[d:,d:]).real);error=td(pinch(rho,S),target);b=bound(J,1.,t)
    assert wrong<=b+1e-11 and error<=b+1e-11
    checks.append({'bath_dimension':d,'bath_norm':bath_scale,'commutator_norm':commnorm,'J':J,'gamma':1,'t':t,'wrong_sector_probability':wrong,'pinched_trace_distance':error,'bound':b})
# General block-diagonal H0 and general Hermitian off-diagonal V, not just X tensor B.
for d in [2,3]:
 H0=np.zeros((2*d,2*d),complex);H0[:d,:d]=7*randherm(d);H0[d:,d:]=11*randherm(d)
 A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));A=A/np.linalg.norm(A,2)*.2
 V=np.block([[np.zeros((d,d)),A],[A.conj().T,np.zeros((d,d))]])
 S=np.kron(Z,np.eye(d));rho0=np.kron(np.diag([.4,.6]),randstate(d))
 for t in [.1,1.,3.]:
  rho=evolve(rho0,H0+V,1.,S,t);U=expm(-1j*H0*t)
  assert td(pinch(rho,S),U@rho0@U.conj().T)<=bound(.2,1,t)+1e-11
coherence=[]
for h in [1e-1,1e-2,1e-3,1e-4]:
 t=1.;T=exact_transfer(h,1.,t);rho=evolve(np.diag([1.,0.]),h*X,1.,Z,t)
 coherent_distance=td(rho,pinch(rho,Z));b=bound(h,1,t)
 coherence.append({'h':h,'t':t,'coherent_trace_distance':coherent_distance,'coherent_distance_over_h':coherent_distance/h,'population_bound':b,'coherent_distance_over_requested_scaling':coherent_distance/(2*h*h)})
# Conserved B with coherent initial bath: reduced map is mixture over spectral populations.
B=np.diag([-.7,.2,1.]);HB=np.diag([3.,-2.,.1]);bath=randstate(3);h=.2;t=.8;rho=np.array([[.7,.1+.2j],[.1-.2j,.3]])
out=evolve(np.kron(rho,bath),np.kron(I,HB)+h*np.kron(X,B),1.,np.kron(Z,np.eye(3)),t)
reduced=np.trace(out.reshape(2,3,2,3),axis1=1,axis2=3)
mix=sum(bath[k,k].real*evolve(rho,h*B[k,k]*X,1.,Z,t) for k in range(3))
mixture_error=float(np.max(abs(reduced-mix)));assert mixture_error<1e-12
result={'max_exact_transfer_error':max_channel_error,'minimum_pauli_twirl_probability':float(min_twirl_prob),'max_bit_bound_violation':max_bit_violation,'noncommuting_bath_checks':checks,'general_block_H0_checks':6,'conserved_bath_mixture_error':mixture_error,'coherent_channel_counterexample':coherence,'cpu_seconds':time.process_time()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2));print({k:v for k,v in result.items() if k!='noncommuting_bath_checks'})

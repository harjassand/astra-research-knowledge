"""Finite algebra checks for global exponential moment bridges, not a code theorem."""
from functools import reduce
from pathlib import Path
import json,numpy as np
from scipy.linalg import expm,eigvalsh,norm,logm

def ten(*xs):return reduce(np.kron,xs)
I=np.eye(2);Z=np.diag([1.,-1.]);X=np.array([[0.,1.],[1.,0.]])
P0=np.diag([1.,0.]);B=np.diag([0.,1.]);Id=np.eye(32)
# DATA, flag1, flag2, monitor1, monitor2.
U=ten(B,I,I,I,I);B1=ten(I,B,I,I,I);B2=ten(I,I,B,I,I)
s=.7;R=4.;t=.03
Sbad1=.45*I+.12*X;Sbad2=.55*I+.1*Z
S1=Id-B1+ten(I,B,I,Sbad1,I);S2=Id-B2+ten(I,I,B,I,Sbad2)
def sqrtp(M):
 d,v=np.linalg.eigh(M);return (v*np.sqrt(np.maximum(d,0)))@v.conj().T
# Erasure-adjoint O -> I_flag tensor its flag=0 compression.
def erase(O,site):
 out=np.zeros_like(O)
 for a in [0,1]:
  k=np.zeros((2,2));k[0,a]=1
  ks=[I]*5;ks[site]=k;K=ten(*ks)
  out+=K.conj().T@O@K
 return out
A1=sqrtp(S1);C1=sqrtp(Id-S1);A2=sqrtp(S2);C2=sqrtp(Id-S2)
def Tb1(O):return A1@O@A1+C1@erase(O,1)@C1
def Tb2(O):return A2@O@A2+C2@erase(O,2)@C2
def Tb(O):return Tb1(Tb2(O))
def Tt(O):return (1-t)*O+t*erase(O,0)
def T(O):return Tb(Tt(O))
E=U+R*(B1+B2);V=expm(s*E)
# Positive noncommuting monitor activity; commutes E but not bad coefficients.
J=.10*ten(I,I,I,(I+Z)/2,I)+.07*ten(I,I,I,I,(I+X)/2)
G=expm(2*J);VG=V@G;gN=float(np.log(eigvalsh(G)[-1]));F=T(VG)
smin=min(eigvalsh(Sbad1)[0],eigvalsh(Sbad2)[0]);kap=-np.log(smin)
sp=s-kap/R
flag_lower=(1-t)*expm(s*U+(s*R-kap)*(B1+B2))
energy_lower=(1-t)*expm(sp*E)
lo=float(eigvalsh(F-flag_lower)[0]);lo2=float(eigvalsh(F-energy_lower)[0]);up=float(eigvalsh(np.exp(gN)*V-F)[0])
ready=ten(I,P0,P0,I,I)
ready_exact=float(norm(ready@(Tb(V)-V)@ready))
assert lo>-1e-10 and lo2>-1e-10 and up>-1e-10 and ready_exact<1e-10
rng=np.random.default_rng(742)
rows=[]
for mass in [1.,.4,.01]:
 W=rng.normal(size=(32,32))+1j*rng.normal(size=(32,32));rho=W@W.conj().T;rho*=mass/np.trace(rho)
 x=float(np.trace(rho@F).real)
 z=float(np.trace(rho@T(VG@(s*E+2*J))).real)
 y=float(np.trace(rho@T(E@VG)).real)
 jensen=z-x*np.log(x/mass)
 weak=y-(x*np.log(x)-gN*x)/s
 assert jensen>-1e-8 and weak>-1e-8
 rows.append({'trace':mass,'x':x,'spectral_jensen_slack':jensen,'entropy_energy_slack':weak,'state_VG_commutator_norm':float(norm(rho@VG-VG@rho))})
out={'scope':'Only exact finite CP/no-jump/scalar-Jensen algebra. No controller drift, code confinement, or logical lifetime is established numerically.','s':s,'R':R,'s_min':float(smin),'kappa_D':float(kap),'s_prime':float(sp),'flag_lower_min_eigenvalue':lo,'energy_lower_min_eigenvalue':lo2,'upper_min_eigenvalue':up,'all_good_dirty_credit_loss':ready_exact,'unitality_residual':float(norm(T(Id)-Id)),'samples':rows}
Path(__file__).with_name('global_moment_algebra_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

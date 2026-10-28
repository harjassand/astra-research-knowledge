"""Independent rational binomial and real-covariance checks; ideal known-center scope only."""
from pathlib import Path
from fractions import Fraction as F
import math,json,hashlib
import numpy as np
root=Path(__file__).resolve().parent
exact_cases=0; maxima=[F(0),F(0),F(0)]
for l in list(range(2,26))+[32,48,64]:
 for q in [F(3,4),F(4,5),F(7,8),F(9,10),F(15,16),F(99,100),F(1)]:
  s=1-q
  ps=[F(math.comb(l,k))*q**k*s**(l-k) for k in range(l+1)]
  hs=[F(l+1,k+1) for k in range(l+1)]
  ts=[F(k,l) for k in range(l+1)]
  eh=sum(p*h for p,h in zip(ps,hs))
  eh2=sum(p*h*h for p,h in zip(ps,hs))
  mse=sum(p*(h-1/q)**2 for p,h in zip(ps,hs))
  er2=sum(p*(h-1/q+(t-q)/q**2)**2 for p,h,t in zip(ps,hs,ts))
  assert eh==(1-s**(l+1))/q
  assert eh2<=2/q**2 and mse<=F(4,l) and er2<=F(9,l*l)
  for j,v in enumerate([eh2,l*mse,l*l*er2]):maxima[j]=max(maxima[j],v)
  # Direct finite-difference ANOVA order-one coefficient.
  p1=[F(math.comb(l-1,k))*q**k*s**(l-1-k) for k in range(l)]
  derivative=l*sum(p*(hs[k+1]-hs[k]) for k,p in enumerate(p1))
  assert derivative==-1/q**2+s**l*(l*q+1)/q**2
  exact_cases+=1
rng=np.random.default_rng(28100720)
count=0; nullcount=0; maxratio=0.; maxformresid=0.
for D in [2,3,4,6,9]:
 d=D-1
 for q in [.75,.82,.97,1.]:
  b=rng.normal(size=d)+1j*rng.normal(size=d)
  b*=math.sqrt((1-q)/np.vdot(b,b).real)
  z=math.sqrt(q)*b;psi=np.r_[math.sqrt(q),b];P=np.outer(psi,psi.conj())
  Sigma=q*np.eye(d)+d/(d+1)*((1-q)*np.eye(d)+np.outer(b,b.conj()))-np.outer(z,z.conj())
  Pi=-np.outer(z,z)
  # Covariance of (Re xi, Im xi), independently of author complex formula.
  Vr=np.block([[(Sigma.real+Pi.real)/2,(Pi.imag-Sigma.imag)/2],[(Pi.imag+Sigma.imag)/2,(Sigma.real-Pi.real)/2]])
  assert np.linalg.eigvalsh(Vr).min()>-1e-12
  for typ in range(3):
   H=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D));O=(H+H.conj().T)/2
   if typ==1:
    Q=np.eye(D)-P;O=Q@O@Q;nullcount+=1
   if typ==2:O=P.copy()
   alpha=O[0,0].real;c=O[1:,0];B=O[1:,1:];b0=np.vdot(z,B@z).real
   MB=np.block([[B.real,-B.imag],[B.imag,B.real]])
   ro=np.vdot(psi,O@O@psi).real;fro=np.trace(O@O).real
   for m in [2,3,7,20]:
    for l in [m,2*m]:
     p=np.array([math.comb(l,k)*q**k*(1-q)**(l-k) for k in range(l+1)])
     h=(l+1)/(np.arange(l+1)+1);t=np.arange(l+1)/l
     mu=alpha*t+b0*h
     varq=float(np.dot(p,(mu-np.dot(p,mu))**2))
     lin=[]
     for hh in h:
      v=c+hh*(B@z);a=2*np.r_[v.real,v.imag]
      lin.append(float(a@Vr@a)/m)
     pair=float(np.trace(MB@Vr@MB@Vr))/math.comb(m,2)
     alt=(np.trace(B@Sigma@B@Sigma).real+b0*b0)/(m*(m-1))
     maxformresid=max(maxformresid,abs(pair-alt))
     var=varq+np.dot(p,lin)+np.dot(p,h*h)*pair
     bound=24*max(0.,ro)/m+80*fro/m**2
     assert var>=-1e-11 and var<=bound+1e-9
     maxratio=max(maxratio,var/max(bound,1e-100));count+=1
source=root/'ordinary_adaptive_pure_known_center_independent_audit_20261028.md'
result={'status':'PASS_KNOWN_CENTER_ONLY','audit_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'exact_rational_binomial_cases':exact_cases,'max_Eh2_lMSE_l2ER2':[float(x) for x in maxima],'real_covariance_cases':count,'null_observables':nullcount,'maximum_bound_ratio':maxratio,'maximum_real_complex_formula_residual':maxformresid,'scope':'Does not receive coarse-center acquisition, finite Gaussian QR compilation, random purification, mixed consequence, or encoder sharing.'}
(root/'ordinary_adaptive_pure_known_center_independent_audit_20261028_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

"""Actual two-output coherent counting checks; finite enumeration is diagnostic."""
from pathlib import Path
from fractions import Fraction as Q
import json,math,cmath
import numpy as np
import mpmath as mp
from scipy.optimize import minimize
from scipy.stats import poisson
from accepted_certify_bus import certify
ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,ok,**extra):
 assert bool(ok),(name,extra);checks.append(dict(name=name,**extra))
def close(name,x,y,tol=2e-11):
 er=float(np.linalg.norm(np.array(x)-np.array(y)));check(name,er<tol,error=er,tolerance=tol)
bvals=np.array([-2.,0.,2.]);base=certify(8)
S=float(Q(base['captured_displacement_energy']['interval'][1]));ell=float(Q(base['inaccessible_displacement_energy']['interval'][1]))
def amplitudes(z,M):
 out=np.zeros((len(z),M+1),complex);out[:,0]=np.exp(-abs(z)**2/2)
 for m in range(M):out[:,m+1]=out[:,m]*z/np.sqrt(m+1)
 return out

def actual(nlo,etap=1.,etam=1.,Mmax=70,cap=None):
 # Input nlo and S are pre-attenuation for this direct instrument function.
 A=np.sqrt(S);L=np.sqrt(nlo);theta=.5*np.arctan(2*A/L)
 zp=(bvals*A+1j*L)/np.sqrt(2);zm=(bvals*A-1j*L)/np.sqrt(2)
 cp=amplitudes(np.sqrt(etap)*zp,Mmax);cm=amplitudes(np.sqrt(etam)*zm,Mmax)
 lp=np.sqrt(1-etap)*zp;lm=np.sqrt(1-etam)*zm
 lost=np.empty((3,3),complex)
 for i in range(3):
  for j in range(3):lost[i,j]=np.exp(-.5*(abs(lp[i])**2+abs(lp[j])**2+abs(lm[i])**2+abs(lm[j])**2)+lp[j].conjugate()*lp[i]+lm[j].conjugate()*lm[i])
 chi=A*L*(etap-etam)/2
 kernel=np.zeros((3,3),complex);pbad=np.zeros(3)
 for m in range(Mmax+1):
  for n in range(Mmax+1):
   v=cp[:,m]*cm[:,n]
   overflow=cap is not None and m+n>cap
   if overflow:pbad+=abs(v)**2
   else:v=v*np.exp(1j*(m-n)*theta*bvals)
   v=v*np.exp(-1j*chi*bvals)
   kernel+=np.outer(v,v.conj())
 kernel*=lost
 return kernel,pbad

def theoretical(nlo,etap=1.,etam=1.):
 eta=(etap+etam)/2
 lam=nlo+bvals*bvals*S
 k=np.exp(-eta*(np.sqrt(lam)[:,None]-np.sqrt(lam)[None,:])**2/2)
 k*=np.exp(-(1-eta)*S*(bvals[:,None]-bvals[None,:])**2/2)
 return k
for nlo in [1,3,4,13]:
 for ep,em in [(1.,1.),(.8,.8),(.8,.93),(.274,.354)]:
  K,_=actual(nlo,ep,em)
  close('actual_balanced_BS_number_instrument',K,theoretical(nlo,ep,em),2e-11)
  close('trace_preservation',np.diag(K),np.ones(3),2e-11)
# Overflow uniform probability and CP difference checked on random pure input distributions.
rng=np.random.default_rng(994)
for nlo in [3,4,8,13,16]:
 K,pbad=actual(nlo,cap=20);ideal=theoretical(nlo)
 close('actual_total_count_overflow',pbad,poisson.sf(20,nlo+bvals*bvals*S),3e-12)
 for j in range(4):
  prob=rng.dirichlet(np.ones(3));D=np.sqrt(prob);change=(K-ideal)*D[:,None]*D[None,:]
  norm=sum(abs(np.linalg.eigvalsh(change)))
  check('overflow_channel_receiving',norm<=2*max(pbad)+2e-12,norm=float(norm),bound=float(2*max(pbad)))
# Special phase identity cannot silently be transferred to a generic many-level B.
theta=.5*np.arctan(2*np.sqrt(S/4))
check('three_level_phase_identity',max(abs(np.arctan(bvals*np.sqrt(S/4))-bvals*theta))<2e-15)
check('generic_B_counterexample',abs(np.arctan(3*np.sqrt(S/4))-3*theta)>1e-3)
# Exact kernel diamond formula checked by direct complete-channel input optimization.
for nlo in [1,3,4,13]:
 K=theoretical(nlo)*np.exp(-ell*(bvals[:,None]-bvals[None,:])**2/2)
 w=1-K[0,1];q=1-K[0,2];exact=q if q>=2*w else 4*w*w/(4*w-q)
 def objective(p):
  p=np.maximum(p,0);v=np.sqrt(p);return -sum(abs(np.linalg.eigvalsh((K-1)*v[:,None]*v[None,:])))
 ans=minimize(objective,[.33,.34,.33],method='SLSQP',bounds=[(0,1)]*3,constraints=[dict(type='eq',fun=lambda p:sum(p)-1)],options={'ftol':1e-14,'maxiter':500})
 close('diamond_vs_direct_optimization',-ans.fun,exact,4e-9)
# Independent high precision recomputation, including actual Poisson tail versus certified upper.
mp.mp.dps=110;cert=json.loads((ROOT/'finite_lo_certificates.json').read_text())
def mpq(x):
 x=Q(x);return mp.mpf(x.numerator)/x.denominator
def inside(name,x,r):
 lo,hi=map(mpq,r['interval']);check(name,lo<=x<=hi,width=str(hi-lo))
T=2*mp.pi;B=mp.mpf(8);D=B*B+1;r=mp.exp(-B*T)
Fw=(T*(1+B*B/(2*D))-(1-r)/(B*D*D))/24-(1-r)**2*mp.exp(-2)/(48*B*D*D)
s=mp.mpf('.999')*mp.mpf('.2')*Fw;e=mp.pi/40-s
for row in cert['rows']:
 n=mpq(row['parameters']['observed_LO_mean']);a=mp.exp(-2*e);d=mp.exp(-8*e);v=mp.exp(-(mp.sqrt(n+4*s)-mp.sqrt(n))**2/2);t=a*v;w=1-t;q=1-d
 dm=q if q>=2*w else 4*w*w/(4*w-q);lam=n+4*s
 tail=mp.exp(-lam)*lam**21/mp.factorial(21)/(1-lam/22)
 total=dm+2*tail+mp.mpf('.0004')*(T+mp.mpf('.125')+mp.mpf('.01')+1)+mp.mpf('.000004')+mp.mpf('.001')
 inside('finite_LO_factor_interval',v,row['LO_adjacent_factor']);inside('diamond_interval',dm,row['exact_bus_receiver_diamond']);inside('complete_error_interval',total,row['total_complete_error_upper'])
 actualtail=mp.exp(-lam)*mp.fsum([lam**j/mp.factorial(j) for j in range(21,250)])
 check('Poisson_tail_upper',actualtail<=mpq(row['uniform_overflow_probability_upper']['interval'][1]),tail=str(actualtail))
 th=mp.atan(2*mp.sqrt(s/n))/2;inside('correction_angle_interval',th,row['theta_interval'])
 for tab in row['finite_correction_table']:
  raw=tab['count_difference']*th;wrapped=raw-mp.nint(raw/mp.pi)*mp.pi;command=mpq(tab['local_Z_coefficient_angle']);err=mpq(tab['computation_error_upper'])
  check('finite_table_angle_enclosure',abs(command-wrapped)<=err)
# Actual ideal on/off-per-bin comparison: not a number-resolving instrument.
bucket=[];nlo=4;theta=.5*np.arctan(2*np.sqrt(S/nlo))
for N in [1,4,16,64,128,256,512,1024,4096]:
 def kval(b,c):
  lb=nlo+b*b*S;lc=nlo+c*c*S
  c0=np.exp(-(lb+lc)/(4*N));h=(b*c*S+nlo+1j*(c-b)*np.sqrt(S*nlo))/(2*N)
  x=c0*(1+np.exp(1j*theta*(b-c))*np.expm1(h))
  return abs(x)**(2*N)*np.exp(-ell*(b-c)**2/2)
 adjacent=kval(2,0);extreme=kval(2,-2);w=1-adjacent;q=1-extreme;dm=q if q>=2*w else 4*w*w/(4*w-q)
 K=np.array([[kval(b,c) for c in bvals] for b in bvals]);check('bucket_kernel_CP',np.linalg.eigvalsh(K).min()>-1e-12)
 bucket.append(dict(equal_energy_bins=N,adjacent=float(adjacent),extreme=float(extreme),bus_diamond=float(dm)))
check('bucket_not_number_instrument',bucket[-1]['bus_diamond']>0.00516 and bucket[-2]['bus_diamond']>bucket[-1]['bus_diamond'])
result={'scope':'Author numerical/high-precision checks; exact certificate and analytic receiving remain controlling','checks':checks,'check_count':len(checks),'bucket_detector_diagnostic':bucket}
(ROOT/'test_finite_lo_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'status':'PASS','bucket_points':len(bucket)},indent=2))

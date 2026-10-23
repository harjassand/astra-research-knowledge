"""Synthetic algebra only: no fitted physical coefficients, time integration or PDE."""
import json, math
from pathlib import Path
import numpy as np
R = np.array([1., 1.3, .8])
cp = np.array([4., 4.5, 3.])
hf = np.array([2., -3., 1.])
theta = np.array([2., 3., 1.5])

def ev(t): return R*theta/np.expm1(theta/t)
def sv(t):
    x=theta/t
    return R*(x/np.expm1(x)-np.log(-np.expm1(-x)))
def hb(t): return cp*t+hf
def zb(t,x): return hb(t)/t-cp*np.log(t)+R*np.log(x)
def psi(t): return ev(t)/t-sv(t)
TL,TR=2.,1.2
vL=np.array([3.,1.4,2.2]); vR=np.array([1.6,2.7,1.1])
xL=np.array([.6,.3,.1]); xR=np.array([.2,.35,.45])
bL,bR=1/TL,1/TR; bvL,bvR=1/vL,1/vR
hbar=(zb(TR,xL)-zb(TL,xL))/(bR-bL)
ebar=(psi(vR)-psi(vL))/(bvR-bvL)
zL=zb(TL,xL)+psi(vL); zR=zb(TR,xR)+psi(vR)
a=R*np.log(xR/xL)
P=np.eye(3)-np.ones((3,3))/3
j=-P@a
q0=2*(bR-bL); qv=np.array([1.,2.,3.])*(bvR-bvL)
Fv=ebar*j+qv
FE=q0+hbar@j+Fv.sum()
alphaL=bvL-bL; alphaR=bvR-bR
sigma_direct=FE*(bR-bL)-j@(zR-zL)+Fv@(alphaR-alphaL)
sigma_square=2*(bR-bL)**2+np.dot(np.array([1.,2.,3.]),(bvR-bvL)**2)+a@P@a
assert abs(j.sum())<1e-14
assert abs(sigma_direct-sigma_square)<1e-13
assert sigma_direct>0
# A mode transfer absent from total energy creates a spurious global energy ledger.
# Local source partition: total energy contains no internal-exchange source.
Svt=ev(TL)-ev(vL)
sigma_vt=(bvL-bL)@Svt
assert sigma_vt>=0
assert abs((-Svt.sum())+Svt.sum())<1e-14
# Equal-temperature manifold: alpha=0 makes all eta choices have identical kinetics.
# k=1, Ru=1, entropy affinity a0=1, all in arbitrary consistent units.
def channel(alpha,eta):
    A=1.+alpha*eta
    rate=2*math.sinh(A/2)
    return dict(affinity=A,rate=rate,mode_source=eta*rate,entropy=A*rate)
eq0,eq1=channel(0.,0.),channel(0.,1.)
assert eq0['rate']==eq1['rate']
assert eq0['mode_source']!=eq1['mode_source']
neq0,neq1=channel(-.5,0.),channel(-.5,1.)
assert neq0['entropy']>0 and neq1['entropy']>0
assert neq0['rate']!=neq1['rate']
inherited_rate_entropy=(1.-.5*3.)*eq0['rate']
assert inherited_rate_entropy<0
# Mismatched quanta, naive forward VV at hot-donor/cooler-acceptor temperatures.
beta,beta_a,beta_b=1/1000.,1/2000.,1/1500.
ea,eb=1.,4.
vvA=ea*(beta-beta_a)+eb*(beta_b-beta)
assert vvA<0 # donor is hotter, yet chosen forward quantum event lowers entropy
out={'scope':'Synthetic dimensionless algebra, not nitrogen coefficients or a trajectory',
 'face_entropy_direct':float(sigma_direct),'face_entropy_nonnegative_form':float(sigma_square),
 'mass_flux_sum':float(j.sum()),'VT_entropy':float(sigma_vt),
 'chemical_same_equal_temperature_manifold':{'eta0':eq0,'eta1':eq1},
 'chemical_unequal_temperatures':{'eta0':neq0,'eta1':neq1},
 'naive_mismatched_VV_entropy_per_forward_event':vvA,
 'unchanged_single_temperature_chemistry_entropy_counterexample':inherited_rate_entropy,
 'all_assertions_passed':True}
Path(__file__).with_name('algebra_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

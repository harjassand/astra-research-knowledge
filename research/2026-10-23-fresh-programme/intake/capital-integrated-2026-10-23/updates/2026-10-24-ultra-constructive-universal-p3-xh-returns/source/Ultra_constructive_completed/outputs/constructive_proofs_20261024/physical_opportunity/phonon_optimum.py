"""Global finite-T phonon design using a scalar spectral dual.
All frequencies are dimensionless; theta=k_B T/hbar=1/2.
Only numpy + Python standard library are required.
"""
from decimal import Decimal, getcontext
import json, math
from pathlib import Path
import numpy as np
getcontext().prec=70
D=Decimal
def sinhD(x): return (x.exp()-(-x).exp())/2
h1=D(1)/sinhD(D(1))**2
h2=D(8)/sinhD(D(2))**2
muD=(h1-h2)/6
lamD=-(4*h1-h2)/3
def FD(x):
    return x**3/sinhD(x)**2+lamD+2*muD*x*x
# Exact roots 1 and 2 arise by construction; the third is isolated at (4,5).
assert lamD<0<muD
assert FD(D(4))<0<FD(D(5))
lo,hi=D(4),D(5)
for _ in range(250):
    mid=(lo+hi)/2
    if FD(mid)<0: lo=mid
    else: hi=mid
cD=(lo+hi)/2
c=float(cD); mu=float(muD); lam=float(lamD)
m=1.
S=c*c-3.
K=S/4
MT=4-12/(c*c)
MS=MT-m
k=4*MS/MT
Omega_r=c/2

def g(w):
    w=np.asarray(w,dtype=float)
    out=np.ones_like(w)
    mask=w!=0
    out[mask]=(w[mask]/np.sinh(w[mask]))**2
    return out
def quad(f,a,b,n=192):
    xs,ws=np.polynomial.legendre.leggauss(n)
    return float((b-a)/2*np.dot(ws,f((a+b)/2+(b-a)/2*xs)))
Jstar=quad(g,0,1)+quad(g,2,c)
Jrigid=quad(g,0,Omega_r)
adv=Jrigid-Jstar
# Conservative Riemann certificate for strict advantage.
# Cancellation reduces difference to int_[1,2] g - int_[c/2,c] g.
# g is strictly decreasing, so right endpoints lower-bound first integral
# and left endpoints upper-bound second. c endpoints use outward floats
# only for this numeric display; the proof gives the exact implicit root.
n=100000
x1=np.linspace(1.,2.,n+1)
x2=np.linspace(c/2,c,n+1)
lower=(1/n)*float(np.sum(g(x1[1:]))) - (c/2/n)*float(np.sum(g(x2[:-1])))
assert lower>0
# Physical two-mass dynamic matrices with all side mass counted.
D0=k*np.array([[1/m,-1/math.sqrt(m*MS)],[-1/math.sqrt(m*MS),1/MS]])
vp=np.array([1/math.sqrt(m),0])
Dpi=D0+4*K*np.outer(vp,vp)
alpha=np.linalg.eigvalsh(D0)
beta=np.linalg.eigvalsh(Dpi)
assert np.allclose(alpha,[0,4],atol=1e-12)
assert np.allclose(beta,[1,c*c],atol=1e-12)
assert abs(np.trace(Dpi)-np.trace(D0)-4*K/m)<1e-12
assert abs(np.prod(beta)/alpha[1]-4*K/MT)<1e-12

# Scalar dual sign samples are diagnostics. The analytic proof of at most
# three roots in PHONON_OPTIMUM.md supplies the all-frequency statement.
ws=np.linspace(.00001,12,24001)
f=ws*g(ws)+lam+2*mu*ws*ws
target=(ws<1)|((ws>2)&(ws<c))
assert np.all(f[target]<1e-10)
assert np.all(f[~target]>-1e-10)
# Expansion coefficient signs: constant -, linear +, even terms - then +.
coef=[2*mu+4*lam/((2*n+2)*(2*n+1)) for n in range(1,101)]
transitions=sum((coef[i]<0)!=(coef[i+1]<0) for i in range(len(coef)-1))
assert transitions<=1
assert coef[0]<0<coef[-1]
result=dict(theta=.5,dual_lambda=str(lamD),dual_mu=str(muD),
            third_root=str(cD),root_bracket=[str(lo),str(hi)],
            normalized_resources=dict(backbone_min_mass=m,total_mass=MT,
                                      side_mass=MS,intercell_spring=K,internal_spring=k),
            bands=dict(optimal=[[0.,1.],[2.,c]],rigid=[[0.,Omega_r]]),
            bose_integrals=dict(optimal=Jstar,rigid=Jrigid,improvement=adv,
                                ratio=Jstar/Jrigid,reduction_fraction=adv/Jrigid,
                                monotone_riemann_lower_bound_improvement=lower),
            total_classical_bandwidth=dict(optimal=1+c-2,rigid=Omega_r),
            alpha=alpha.tolist(),beta=beta.tolist(),
            interpretation="G=(k_B/2pi) J; full harmonic ideal-contact ballistic model",
            scope="Global spectral-dual optimum within all finite passive connected internal cells with one intercell backbone spring, same K,total mass,and backbone mass >=1. Not general 3D conductivity or material/electronic advantage.")
HERE=Path(__file__).resolve().parent
(HERE/"phonon_optimum.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))


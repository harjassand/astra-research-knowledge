#!/usr/bin/env python3
"""Exact-rational analytic certificate for a reciprocal, bidirectional 2-emitter gate.

Data: photon band [0,2], v_R(w)=w/sqrt(2)*(1,exp(+i*tau*w)),
                              v_L(w)=w/sqrt(2)*(1,exp(-i*tau*w))
with gamma=1, tau=11/10, energy E0=3/2, half-bandwidth w=6/125=0.048.
Two positive passive parity resonators calibrated by EXACT PV derivatives.

B_p(E) = PV int_0^2 z^2(1+p*cos(tau*z))/(z-E) dz,
p in {+1,-1}. Rational Taylor expansion of cos and artanh for ln(1/3)
certifies B_p(E0), first two derivatives. The remaining continuous-band
bound is analytical by a third-derivative inequality (not frequency sampling).
"""
from fractions import Fraction as Q
from math import factorial
import json

def f(n,d=1): return Q(n,d)
class Interval:
    def __init__(self,lo,hi=None):
        self.lo=Q(lo);self.hi=Q(lo if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(self,o):
        o=as_iv(o);return Interval(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return Interval(-self.hi,-self.lo)
    def __sub__(self,o):return self+-as_iv(o)
    def __rsub__(self,o):return as_iv(o)+-self
    def __mul__(self,o):
        o=as_iv(o);p=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi]
        return Interval(min(p),max(p))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=as_iv(o);assert o.lo*o.hi>0
        return self*Interval(1/o.hi,1/o.lo)
    def __rtruediv__(self,o):return as_iv(o)/self
    def __pow__(self,n):
        assert n>=0 and isinstance(n,int)
        if n==0:return Interval(1)
        if n%2==0 and self.lo<0<self.hi:
            return Interval(0,max(self.lo**n,self.hi**n))
        return Interval(min(self.lo**n,self.hi**n),max(self.lo**n,self.hi**n))
    def widen(self,h):
        h=Q(h);return Interval(self.lo-h,self.hi+h)
    def out(self,digits=15):return [float(self.lo),float(self.hi)]
def as_iv(x):return x if isinstance(x,Interval) else Interval(x)

E=Q(3,2);tau=Q(11,10);gam=Q(1);W=Q(6,125);lo=E-W;hi=E+W;CHI=Q(1800)
# L0=ln((2-E)/E)=ln(1/3)=-2*atanh(1/2)
J=65; y=Q(1,2)
Lpartial=-2*sum((y**(2*j+1))/Q(2*j+1) for j in range(J))
Ltail=2*y**(2*J+1)/(Q(2*J+1)*(1-y*y))
L=Interval(Lpartial-Ltail,Lpartial)
Lp=-1/(2-E)-1/E
Lpp=-1/(2-E)**2+1/E**2
assert Q(-2)<L.lo and L.hi<Q(-1)

def Im(n,dr):
    """PV integral of x^n/(x-E), derivative dr in E for E=3/2."""
    assert dr in (0,1,2)
    pp=sum(Q(2)**(n-j) * (Q(factorial(j),factorial(j-dr)) if j>=dr else 0) * E**(j-dr) / Q(n-j)
           for j in range(dr,n))
    if dr==0: return Interval(pp)+E**n*L
    if dr==1: return Interval(pp)+n*E**(n-1)*L+E**n*Lp
    return Interval(pp)+n*(n-1)*E**(n-2)*L+2*n*E**(n-1)*Lp+E**n*Lpp

N=20
Tn=Q(100)*(2*N+2)**3 * 2**(2*N+2) * tau**(2*N)/Q(factorial(2*N))
ratio=((Q(2*N+4,2*N+2))**3 * (2*tau)**2 /Q((2*N+2)*(2*N+1)))
assert ratio<Q(1,100)
TAIL=Tn/(1-ratio)
assert TAIL<Q(1,10**25)

def B(p,dr):
    I2=Im(2,dr)
    csum=Interval(0)
    for n in range(N):
        csum=csum + Q((-1)**n)*tau**(2*n)/Q(factorial(2*n))*Im(2*n+2,dr)
    return (I2+p*csum).widen(TAIL)

par={}
for p in (+1,-1):
    b,bp,bpp=(B(p,j) for j in (0,1,2))
    t=-1-gam*bp
    d=-2*t/(gam*bpp)
    r=t*d*d
    Om=E+d
    bare=E+gam*b+r/d
    # W_p = integral_0^2 x (1+p cos(tau x)) dx, bounded 0<=W_p<=4.
    # Strong positivity even against the crude upper bound 4:
    c_lower=bare-4*gam-r/Om
    assert t.lo>0 and d.lo>W and r.lo>0 and Om.lo>hi and c_lower.lo>0
    par[str(p)]={'B0':b.out(),'Bp':bp.out(),'Bpp':bpp.out(),
                  't':t.out(),'d':d.out(),'r':r.out(),
                  'Omega':Om.out(),'bare_emitter_energy':bare.out(),
                  'positive_schur_lower_bound_using_W_le_4':c_lower.out()}
    par[p]={'t':t,'d':d,'r':r,'bare':bare,'Omega':Om}

# Analytical third derivative bound.  f(x)=x^2(1+p cos(tau x)).
# B_p(E) = f(E)*L(E) + integral_0^2 integral_0^1 f'(E+v(x-E)) dv dx.
# |B'''| <= |f'''| |L| + 3|f''||L'| + 3|f'||L''| + |f||L'''|
#             + (1/2)*sup_{x in [0,2]}|f''''(x)|.
# All bounds use |cos|,|sin|<=1; x in [lo,hi] for first four, [0,2] for last.
f0=2*hi*hi
f1=4*hi+tau*hi*hi
f2=4+4*hi*tau+hi*hi*tau*tau
f3=6*tau+6*hi*tau*tau+hi*hi*tau**3
f4global=12*tau*tau+16*tau**3+4*tau**4
# |L| <= 124/100 on this interval, certified by e^(124/100)>hi/(2-hi).
# Lower bound e^u >sum_{k=0}^8 u^k/k! for u>0.
U=Q(124,100)
assert sum(U**k/Q(factorial(k)) for k in range(9))>hi/(2-hi)
L0bound=U
L1bound=1/(2-hi)+1/lo
L2bound=1/(2-hi)**2+1/lo**2
L3bound=2/(2-hi)**3+2/lo**3
M=f3*L0bound+3*f2*L1bound+3*f1*L2bound+f0*L3bound+f4global/2
assert M<Q(420)
# |cos(tau E)|=|sin(tau E-pi/2)| <= |tau E-pi/2|.
# Use pi in (314159/100000, 314160/100000) by classical Archimedean bounds.
pilo=Q(314159,100000); pihi=Q(314160,100000)
assert tau*lo>pihi/2 # angles throughout interval above pi/2
cosbound=tau*hi-pilo/2
assert cosbound<Q(133,1000)
a_min=pilo*lo*lo*(1-cosbound)
a_max=pihi*hi*hi*(1+cosbound)
assert a_min>Q(57,10)

# Resource no-gos under the same fixed bare waveguide response:
# both entries of I+gamma*Bprime are negative, so two independent rank-one
# positive-residue resonators are necessary to null the full derivative.
assert (-1-gam*B(+1,1)).lo>0 and (-1-gam*B(-1,1)).lo>0
# Any parity-odd side pole at or below E0 contributes r/d^3 <=0; any pole
# at/above the bath's upper edge 2 has r/d^3 <= 2*r/d^2. Thus a solution
# with the desired odd derivative moments must contain an in-band pole E0<Omega<2.
odd_required_second=-gam*B(-1,2)/2
odd_required_first=-1-gam*B(-1,1)
assert (odd_required_second-2*odd_required_first).lo>0

errors={}
for p in (+1,-1):
    d=par[p]['d'];r=par[p]['r']
    # The exactly cancelled 0,1,2 jets leave the bath Taylor remainder
    # and an exact passive-pole remainder r*w^3/(d^3*(d-w)).
    qbound=gam*M*W**3/6+r*W**3/(d**3*(d-W))
    selected=2*qbound/a_min
    notfull=2*a_max/(CHI-qbound)
    assert selected.hi<Q(1,100)
    assert notfull.hi<Q(1,100)
    errors[str(p)]={'qbound':qbound.out(),'selected_error_bound':selected.out(),
                    'notfull_error_bound':notfull.out()}

out={'model':'reciprocal two-emitter bidirectional finite-band waveguide with two parity-coupled passive side modes',
     'gamma':1,'tau':1.1,'center':1.5,'halfbandwidth':float(W),'memory_shift_per_missing_occupancy':int(CHI),
     'positive_emitter_Schur_margins':{str(p):par[str(p)]['positive_schur_lower_bound_using_W_le_4'] for p in (+1,-1)},
     'parity_parameters':{str(p):par[str(p)] for p in (+1,-1)},
     'error_bounds':errors,'required_resonator_rank_at_least':2,'odd_channel_in_band_pole_necessary':True,'odd_second_moment_minus_twice_first_lower_bound':float((odd_required_second-2*odd_required_first).lo),'B_second_derivative_rational_series_tail':float(TAIL),
     'B_third_derivative_bound':float(M),'a_min':float(a_min),'a_max':float(a_max),
     'certified_full_selected_error':max(x['selected_error_bound'][1] for x in errors.values()),
     'certified_full_unselected_error':max(x['notfull_error_bound'][1] for x in errors.values()),
     'proof':'Exact rational interval arithmetic for center derivatives, elementary analytic Taylor remainder and a positivity-of-Schur-form all-N energy inequality. All errors are continuous-band norm bounds and include both propagation directions.',
     'scope':'All statements refer to a lossless reciprocal 1D two-direction finite-band model plus parity-coupled side modes. No unmodeled independent radiation channels, waveguide dispersion uncertainty, pulse injection/extraction or finite-time bound.'}
path='/mnt/data/astra_reciprocal_parity_interval_certificate_20261026.json'
with open(path,'w') as fjson: json.dump(out,fjson,indent=2)
print(json.dumps(out,indent=2))

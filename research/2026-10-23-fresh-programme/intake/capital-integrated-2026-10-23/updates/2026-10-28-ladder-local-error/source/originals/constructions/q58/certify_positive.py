#!/usr/bin/env python3
"""Rigorous interval certificate using only radicals and spectral-support bounds.
No continuum quadrature accuracy assumption enters this lower bound.
mpmath.iv uses outward-rounded interval arithmetic. g is exactly 1/5.
"""
from pathlib import Path
import json
import mpmath as mp
iv=mp.iv
iv.dps=50
one=iv.mpf(1)
g=one/5
kp=2*g*g;km=g*g
Eplus=3-2*kp/(2+iv.sqrt(3+4*kp))
Eminus=3+2*km/(2+iv.sqrt(3+4*km))
def atomweight(e,c,k):
    d=abs(e-c)
    qp=2*(-1+d/iv.sqrt(d*d-1))
    return 1/(1+k*qp)
Zplus=atomweight(Eplus,5,kp);Zminus=atomweight(Eminus,1,km)

def flo_upper(z):
    atom=Zplus**2/(2*Eplus-z)+Zminus**2/(2*Eminus-z)
    cp=2*Zplus*(1-Zplus)/(Eplus+4-z)+(1-Zplus)**2/(8-z)
    return atom+cp

def fhi_lower(z):
    atom=Zplus**2/(2*Eplus-z)+Zminus**2/(2*Eminus-z)
    cm=2*Zminus*(1-Zminus)/(z-Eminus-2)+(1-Zminus)**2/(z-4)
    return atom-cm

elo=iv.mpf('5.9785');ehi=iv.mpf('5.9787')
Ep=iv.mpf(['5.9785','5.9787'])
flo=flo_upper(elo);fhi=fhi_lower(ehi)
assert flo.b<0 and fhi.a>0
# Thus the exact strictly increasing even-root function has its unique root
# inside (elo,ehi), independently of the numerical continuum solver.

def qbelow(z,c):
    d=c-z
    return 2/(d+iv.sqrt(d*d-1))
def qabove(z,c):
    d=z-c
    return -2/(d+iv.sqrt(d*d-1))
def rp(z):return 1/(3-z-kp*qbelow(z,5))
def rm(z):return 1/(3-z-km*qabove(z,1))
def density(x,c,k):
    u=x-c;v2=1-u*u
    return 2*k*iv.sqrt(v2)/(iv.pi*((3-x+2*k*u)**2+4*k*k*v2))
J1=iv.mpf(['4.1995','4.2005']);J2=iv.mpf(['5.7995','5.8005'])
W1=rp(Ep-J1)+rm(J1);W2=rp(Ep-J2)+rm(J2)
gap=W2.a-W1.b
assert gap.a>0
mass1=iv.mpf('.001')*density(J1,5,kp)*density(Ep-J1,1,km)
mass2=iv.mpf('.001')*density(J2,5,kp)*density(Ep-J2,1,km)
assert mass1.a>0 and mass2.a>0
Lp_upper=Zplus**2/(2*Eplus-Ep)**2+2*Zplus*(1-Zplus)/(Eplus+4-Ep)**2+(1-Zplus)**2/(8-Ep)**2
Lm_upper=Zminus**2/(2*Eminus-Ep)**2+2*Zminus*(1-Zminus)/(Ep-Eminus-2)**2+(1-Zminus)**2/(Ep-4)**2
N2_lower=2/(Lp_upper+Lm_upper).b
m1=mass1.a;m2=mass2.a
lower=N2_lower*(m1*m2/(m1+m2))*gap.a**2
assert lower.a>0
# A simple readable rational bound is checked by the interval result.
assert lower.a>iv.mpf('4e-16')
result={
 'runtime':{'mpmath':mp.__version__},
 'g':'1/5 exactly',
 'E_plus':str(Eplus),'E_minus':str(Eminus),
 'Z_plus':str(Zplus),'Z_minus':str(Zminus),
 'exact_pair_enclosure':str(Ep),
 'F_at_left_upper_bound':str(flo),'F_at_right_lower_bound':str(fhi),
 'J1':str(J1),'J2':str(J2),'shell_W_on_J1':str(W1),'shell_W_on_J2':str(W2),
 'separation_lower_bound':str(gap),'mass_J1_lower_bound':str(mass1.a),'mass_J2_lower_bound':str(mass2.a),
 'normalizer_squared_lower_bound':str(N2_lower),
 'rho_lower_bound':str(lower),
 'certified_statement':'rho(Ep) > 4e-16. Finiteness is established analytically in PROOF.md.',
 'method':'Outward-rounded interval arithmetic, exact radical atoms, spectral-support bounds, and two disjoint continuum intervals; no finite chain or quadrature-error estimate.'
}
(Path(__file__).resolve().parent/'positive_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

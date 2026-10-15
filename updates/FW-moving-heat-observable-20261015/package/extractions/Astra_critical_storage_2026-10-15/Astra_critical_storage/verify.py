#!/usr/bin/env python3
"""Exact checks for the finite-family calibration and primitive obstruction."""
import sympy as s, json, pathlib
p,q,t,k,z,delta=s.symbols('p q t k z delta', real=True)
a=s.Rational(107,24); b=s.Rational(29,2)
u=p*p+t*t; v=q*q; j=p*q
G=3*(u+v-2*j)**2+s.Rational(35,24)*u*u+j*j-s.Rational(5,2)*j*u
L=a*p**4-b*p**3*q+19*p*p*q*q-12*p*q**3+3*q**4
phase=s.Rational(107,12)*p*p-b*p*q+6*q*q
assert s.expand(G-L-phase*t*t-a*t**4)==0
assert s.discriminant(phase,p)==-s.Rational(15,4)*q*q
h=L.subs(q,1); stationary=107*k**4-232*k**3+152*k*k-24
c=h.subs(p,k)/k
factor=(p-k)**2*(a*p*p+(2*a*k-b)*p+3/k**2)
num=s.together(h-c*p-factor).as_numer_denom()[0]
# Every coefficient vanishes modulo the stationary polynomial.
for coeff in s.Poly(num,p).all_coeffs(): assert s.rem(coeff,stationary,k)==0
Iplus=(s.Rational(890923272145,10**12),s.Rational(890923272146,10**12))
Iminus=(s.Rational(-318411269741,10**12),s.Rational(-318411269740,10**12))
assert s.Poly(stationary,k).count_roots(*Iplus)==1
assert s.Poly(stationary,k).count_roots(*Iminus)==1
# Quadratic cofactor discriminant is strictly negative throughout both isolating intervals.
# Conservative rational boxes suffice; exact endpoints and rational arithmetic only.
def maxsq(lo,hi): return max(lo*lo,hi*hi)
for lo,hi in [Iplus,Iminus]:
 midlo=2*a*lo-b; midhi=2*a*hi-b
 lower_const=3/maxsq(lo,hi)
 assert maxsq(midlo,midhi)-4*a*lower_const<0
roots=s.polys.polytools.intervals(stationary,eps=s.Rational(1,10**14))
assert sum(m for iv,m in roots)==2
psi=z*(1-z)**2
collar=s.integrate(s.expand(L.subs({p:s.diff(psi,z),q:delta*psi})),(z,0,1))
assert collar==s.Rational(107,420)-s.Rational(29,840)*delta+s.Rational(19,1386)*delta**2+delta**4/2145
assert s.integrate(L.subs(p,1),(q,0,1))==s.Rational(137,120)
assert s.integrate(L.subs(p,-1),(q,0,1))==s.Rational(2597,120)
# Check actual certificate's normal-plane coefficients.
cert=json.loads(pathlib.Path(__file__).with_name('G_EXACT_HEAT_CERTIFICATE.json').read_text())
assert s.Rational(cert['omega_coefficients'][1][0])==s.Rational(788811,20000)
assert s.Rational(cert['omega_coefficients'][1][7])==s.Rational(98601,2500)
assert (s.Rational(788811,20000)+s.Rational(98601,2500))/8==s.Rational(1577619,160000)
rp=float(s.nroots(stationary)[1]); rm=float(s.nroots(stationary)[0])
report={'status':'EXACT_CHECKS_PASS','scope':'B=0; circular Fourier state family, arbitrary W1,4 coefficient paths', 'incoming_k':rp,'incoming_storage_coefficient':float(c.subs(k,rp)/4),'return_k':-rm,'available_storage_coefficient':float(c.subs(k,rm)/4),'collar_action_coefficient':str(collar),'primitive_circulation_coefficient':'1577619/160000','full_space_identification':False,'strict_coercivity_used':False}
pathlib.Path(__file__).with_name('receipt.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
# Symmetry-breaking certificate: exact reduction and rational interval signs.
def ia(x,y):return (x[0]+y[0],x[1]+y[1])
def im(x,y):
 v=[a*b for a in x for b in y];return(min(v),max(v))
def ip(poly,interval):
 out=(s.Rational(0),s.Rational(0))
 for v in s.Poly(poly,k).all_coeffs():out=ia(im(out,interval),(v,v))
 return out
alpha=s.Rational(2033,4)*k*k-s.Rational(1653,2)*k+358
beta=s.Rational(2033,4)*k**4-2088*k**3+3541*k*k-2916*k+936
I2=alpha*s.Rational(1000,3)+beta*s.Rational(100000,30)
assert ip(I2,Iplus)[1]<-16000
A=s.symbols('a b c d');aa,bb,cc,dd=A
uu=aa*aa+cc*cc;vv=bb*bb+dd*dd;jj=aa*dd-bb*cc
fullG=3*(uu+vv-2*jj)**2+s.Rational(35,24)*uu*uu+jj*jj-s.Rational(5,2)*jj*uu
H=s.hessian(fullG,A).subs({aa:k,bb:0,cc:0,dd:1})
e,f=s.symbols('eta deta');vc=s.Matrix([4*(f-k*e),0,0,-5*e]);vs=s.Matrix([0,-9*e,-3*(f-k*e),0])
Q=s.expand(((vc.T*H*vc)[0]+(vs.T*H*vs)[0])/2)
assert s.expand(Q.coeff(f,2)-alpha)==0
assert s.expand(Q.coeff(e,2)-beta)==0
DG=[s.diff(fullG,x).subs({aa:k,bb:0,cc:0,dd:1}) for x in A]
assert s.expand(3*k*DG[0]-DG[3]-stationary/2)==0
assert 3*k*DG[2]+DG[1]==0
assert 150*s.Rational(11,4)**36*260**4<10**28
lam=s.Rational(1,10**16); seed=s.Rational(1,10**9)
assert -8000*lam**2+10**28*lam**4+2*seed**4 < -s.Rational(7,10**29)
report['symmetry_breaking']={'status':'EXACT_NEGATIVE_SECOND_VARIATION','physical_Fourier_modes':[1,2,4],'second_variation_upper_bound':'-16000','amplitude':'1/10^16','seed_amplitude':'1/10^9','full_action_gain_lower_bound':'7/10^29','comparison':'strictly below the circular-family required supply; not a negative closed-loop action'}
pathlib.Path(__file__).with_name('receipt.json').write_text(json.dumps(report,indent=2)+'\n')
print('SYMMETRY-BREAKING EXACT CHECKS PASS')

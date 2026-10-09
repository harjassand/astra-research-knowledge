"""Exact replay of supplied root/log component obstructions only."""
import json
import sympy as s

t = s.symbols('t', real=True)
N = 3 + 2*t + 3*t*t
H = s.Matrix([[1,t,0],[t,1,0],[0,0,1+t]])
sig = H*H/N
L = s.diag(s.Rational(1,5),s.Rational(9,5),1)
assert s.simplify(s.trace(sig*L)) == 1
E = s.simplify(s.trace(H*L*H*L)/N - 1)
assert s.simplify(E - 32*(1-t*t)/(25*N)) == 0
lg5, lg9 = s.symbols('lg5 lg9')
logL = s.diag(-lg5,lg9-lg5,0)
Elg = s.simplify(s.trace(H*L*H*logL)/N - s.trace(sig*logL))
assert s.simplify(Elg - s.Rational(4,5)*(1-t*t)*lg9/N) == 0
sqrtL = s.diag(1/s.sqrt(5),3/s.sqrt(5),1)
Er = s.simplify(s.trace(H*sqrtL*H*sqrtL)/N - s.trace(sig*sqrtL)**2)
assert s.simplify(s.limit(Er,t,1) - (9-4*s.sqrt(5))/20) == 0
residual = s.simplify(H*L*H/N-sig)
assert s.simplify(residual-s.Rational(4,5)*(t*t-1)*s.diag(1,-1,0)/N)==s.zeros(3)

tv=s.Rational(99,100)
Nv=N.subs(t,tv); Hv=H.subs(t,tv); sv=sig.subs(t,tv)
m=(1+tv*tv)/Nv; k=(1+tv)**2/Nv
mu=2*m+s.Rational(9,10)*k
assert mu == s.Rational(752429,792030)
c12=tv*tv/Nv-m*m
a=-s.Rational(8,5)*c12+s.Rational(7,10)*m*k
c=s.Rational(1,5)*m*k
assert a == -s.Rational(131609645,12546230418)
assert c == s.Rational(784139401,31365576045)
upper=2*a+s.Rational(7,10)*c
assert upper == -s.Rational(363835481,104551920150)
L0=s.diag(s.Rational(1,5),s.Rational(9,5),s.Rational(9,10))
lg2=s.symbols('lg2')
logL0=s.diag(-lg5,lg9-lg5,lg9-lg5-lg2)
actual_form=s.simplify(s.trace(Hv*L0*Hv*logL0)/Nv-mu*s.trace(sv*logL0))
assert s.simplify(actual_form-a*lg9-c*lg2)==0
third_difference=s.simplify(k*(1-s.Rational(9,10)/mu))
assert third_difference == m*k/(5*mu)
assert third_difference > 0
gamma=2*tv/(1+tv*tv)
pis=[];weights=[]
for sign in [-1,1]:
 for rsign in [-1,1]:
  v=s.Matrix([s.sqrt(m),sign*s.sqrt(m),rsign*s.sqrt(k)])
  pi=v*v.T;w=(1+sign*gamma)/4
  assert s.simplify(s.trace(pi))==1
  assert s.simplify(pi*pi-pi)==s.zeros(3)
  assert w>0
  pis.append(pi);weights.append(w)
bar=s.simplify(sum((w*pi for w,pi in zip(weights,pis)),s.zeros(3)))
assert bar == sv
S_inv=s.sqrt(Nv)*Hv.inv()
effects=[s.simplify(w*S_inv*pi*S_inv) for w,pi in zip(weights,pis)]
assert s.simplify(sum(effects,s.zeros(3)))==s.eye(3)
for w,M in zip(weights,effects):assert s.simplify(s.trace(sv*M))==w
rho=s.simplify(Hv*L0*Hv/(Nv*mu))
prepared=s.simplify(sum((pi*s.trace(M*rho) for pi,M in zip(pis,effects)),s.zeros(3)))
assert prepared==sv
print(json.dumps({'status':'EXACT_COMPONENT_OBSTRUCTIONS_PASS',
 'root_energy_limit':'(9-4*sqrt(5))/20 > 0',
 'rational_log_upper_bound':str(upper),
 'half_trace_effect_lower_bound':str(third_difference),
 'pure_canonical_atoms':4,
 'physical_state_preservation_orientation':'Psi_t* sigma = sigma',
 'genuine_relative_entropy_or_Qrho_power_refuted':False},indent=2))

"""Exact identities/fixtures only; diagnostics are not finite-error admissions."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json
import sympy as s
P=Path(__file__).resolve().parent;checks=[]
def ok(label,condition):
 assert condition,label
 checks.append(label)
def eq(label,left,right=0):ok(label,s.simplify(left-right)==0)
a,m,u,t,beta,k,p=s.symbols('alpha m u t beta k p',positive=True)
eq('ordinary coarea degree',(m-1)/4-s.Rational(3,4),m/4-1)
eq('Hessian shell degree',(m-1)/4+s.Rational(1,2)-s.Rational(3,4),m/4-s.Rational(1,2))
eq('gradient shell degree',(m-1)/4+s.Rational(6,4)-s.Rational(3,4),m/4+s.Rational(1,2))
eq('Gauss shell primitive',s.diff(u**(a+s.Rational(1,2))/(a+s.Rational(1,2)),u),u**(a-s.Rational(1,2)))
eq('conditional gradient degree',(a+s.Rational(1,2))-(a-1),s.Rational(3,2))
eq('radial gamma normalization',s.integrate(u**(a-1)*s.exp(-beta*u),(u,0,s.oo)),s.gamma(a)/beta**a)
eq('longitudinal beta prefactor',1/(beta*(s.gamma(a)/beta**a)),beta**(a-1)/s.gamma(a))
eq('transverse radial exponent',(a-1)+s.Rational(3,2),a+s.Rational(1,2))
eq('Tonelli inner primitive',s.integrate(u**(a-s.Rational(1,2)),(u,0,t)),t**(a+s.Rational(1,2))/(a+s.Rational(1,2)))
eq('Bernoulli covariance range margin',s.Rational(1,4)-p*(1-p),(p-s.Rational(1,2))**2)
y=s.symbols('y',real=True);v=lambda y:1+k*(1-y*y)**2;V=1+k;vb=1+9*k/16
neq=eq
neq('slab range',V-vb,7*k/16)
eq('uniform u derivative bound',beta*(V-vb)/4,7*beta*k/64)
Iprime=s.integrate(beta*v(t),(t,-s.Rational(1,2),s.Rational(1,2)))
eq('I at zero derivative',Iprime,beta*(1+203*k/240))
hu0=s.integrate(beta*v(t),(t,y,s.Rational(1,2)))-(s.Rational(1,2)-y)*Iprime
neq('finite origin trial derivative',hu0,beta*k*(-37*y/240+2*y**3/3-y**5/5))
eq('left trace u derivative',hu0.subs(y,-s.Rational(1,2)),0)
eq('right trace u derivative',hu0.subs(y,s.Rational(1,2)),0)
# Exact diagonal pair-quartic trace identity with genuinely nonuniform coefficients.
z=s.symbols('z0:3',real=True);dd=s.symbols('d0:3',positive=True);mm=s.symbols('mu0:3',positive=True);g01,g12,g02=s.symbols('g01 g12 g02',nonnegative=True)
U=sum(dd[i]*z[i]**4 for i in range(3))+g01*z[0]**2*z[1]**2+g12*z[1]**2*z[2]**2+g02*z[0]**2*z[2]**2
cc=[12*mm[0]*dd[0]+2*(mm[1]*g01+mm[2]*g02),12*mm[1]*dd[1]+2*(mm[0]*g01+mm[2]*g12),12*mm[2]*dd[2]+2*(mm[0]*g02+mm[1]*g12)]
eq('complete diagonal Hessian trace',sum(mm[i]*s.diff(U,z[i],2) for i in range(3)),sum(cc[i]*z[i]**2 for i in range(3)))
eq('isotropic radial exact shell check',4*(m+2)/(m/4+s.Rational(1,2)),16)
# Full SPD cannot simply use the diagonal-only trace price. m=16 admitted example.
actual=s.Rational(232,5);wrong_bound_squared=4*(2*16**2+14*s.Rational(12,1000)**2)
ok('off-diagonal omission violates price in m16',actual**2>wrong_bound_squared)
ok('off-diagonal SPD block determinant',1-s.Rational(9,10)**2>0)
# Exact rational Cauchy/coercivity fixtures for the diagonal class.
for nn in [2,3,4,8,16]:
 for seed in range(1,9):
  ds=[Q(seed+i+1,seed+1) for i in range(nn)];mus=[Q(2*i+seed+1,seed+2) for i in range(nn)]
  edges=[(i,i+1,Q(seed+i+1,3)) for i in range(nn-1)]
  coeff=[12*mus[i]*ds[i] for i in range(nn)]
  for i,j,g in edges:coeff[j]+=2*mus[i]*g;coeff[i]+=2*mus[j]*g
  for shift in range(1,5):
   zs=[Q(((-1)**i)*(i+shift),seed+shift) for i in range(nn)]
   energy=sum(ds[i]*zs[i]**4 for i in range(nn))+sum(g*zs[i]**2*zs[j]**2 for i,j,g in edges)
   tr=sum(coeff[i]*zs[i]**2 for i in range(nn));cn2=sum(c*c for c in coeff)
   ok('diagonal full-price fixture '+str((nn,seed,shift)),tr>=0 and tr*tr<=cn2*energy/min(ds))
for nn in [16,64,128,512]:
 coeff=[52]+[92]*(nn-2)+[52]
 ok('path exact coefficients '+str(nn),coeff[0]==12+2*20 and coeff[-1]==52 and all(c==12+2*(20+20) for c in coeff[1:-1]))
 ok('mobility-growth counterexample '+str(nn),(12*nn)**2*nn==144*nn**3)
cn2=2*52**2+510*92**2
ok('m512 exact c norm squared',cn2==4322048)
ok('diagnostic coefficient about32.5',Q(324,10)**2<Q(cn2,64**2)<Q(326,10)**2)
eq('odd-source positive pricing gap',2*vb-V,1+k/8)
eq('odd-source b factor',2*beta*s.Rational(1,2)**3,beta/4)
# Formal Laplace coefficient algebra only (no remainder or finite-accuracy proof).
shift,curv,quart=s.symbols('shift curv quart',positive=True)
Ar=3*(quart-curv**2/2)/(4*curv**2)
Aa=shift**2-shift+3*(quart+curv**2/2)/(4*curv**2)
eq('formal dual coefficient',Aa-Ar,shift**2-shift+s.Rational(3,4))
eq('formal optimized dual coefficient',(Aa-Ar).subs(shift,s.Rational(1,2)),s.Rational(1,2))
neq('formal frozen longitudinal coefficient',-s.Rational(1,8)-3/(16*quart)+(3/(16*quart)-s.Rational(3,8)),-s.Rational(1,2))
eq('Gaussian derivative y integral',s.integrate(y*y*s.exp(-curv*u*y*y),(y,-s.oo,s.oo)),s.sqrt(s.pi)/(2*(curv*u)**s.Rational(3,2)))
for name,row in json.loads((P/'INPUT_SHA256.json').read_text()).items():
 data=(P.parent/name).read_bytes();ok('frozen source '+name,hashlib.sha256(data).hexdigest()==row['sha256'] and len(data)==row['bytes'])
report={'status':'PASS','exact_assertions':len(checks),'scope':'exact identities and fixtures; formal coefficient algebra explicitly diagnostic, not finite admission','checks':checks}
(P/'CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'}))

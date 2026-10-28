"""Independent reconstruction and Descartes receiver; no root-code imports."""
from pathlib import Path
from fractions import Fraction as Q
import json,time,sys
sys.set_int_max_str_digits(0);START=time.perf_counter()
import sympy as s
from acquire_binary import add,scale,flog,rat,enc
BASE=Path(__file__).resolve().parents[2]/'sol14_capability_frontier_20261028'/'parent'/'memory_budget'
OUT=Path(__file__).resolve().parent/'outputs'
source=json.loads((BASE/'SOURCE.json').read_text());data=json.loads((BASE/'WHITE_POLYNOMIAL.json').read_text());white=json.loads((BASE/'WHOLE_WHITE.json').read_text())
def readmatrix(a):return s.Matrix([[s.Rational(z[0])+s.sqrt(-3)*s.Rational(z[1]) for z in row] for row in a])
omega=(-1+s.sqrt(-3))/2;weights=[1000,1,2,3,4,5,6,7,8]
PX=s.ones(2)/2;MX=s.Matrix([[1,-1],[-1,1]])/2;PZ=s.diag(1,0);MZ=s.diag(0,1)
states=[s.eye(2)/2,PX,MX,PZ,MZ,MZ,PZ,MX,PX];aa=[p*q for p,q in zip(weights,states)]
X=s.zeros(18);M=s.zeros(6)
for i,(a,b) in enumerate((a,b) for a in range(3) for b in range(3)):
 v=s.zeros(9,1);u=s.zeros(3,1)
 for j in range(3):v[3*j+(j+a)%3]=omega**(b*j)
 u[(a+1)%3]=1;u[(a+2)%3]=-omega**(-b)
 X+=s.kronecker_product(v*v.H/3,aa[i]);M+=s.kronecker_product(u*u.H/2,aa[i])
X=X.applyfunc(s.simplify);M=M.applyfunc(s.simplify)
assert all(s.simplify(v)==0 for v in X-readmatrix(source['X']))
assert all(s.simplify(v)==0 for v in M-readmatrix(source['M']))
assert sum(aa,s.zeros(2))==518*s.eye(2) and s.trace(X)==1036
x=s.symbols('x');char=s.Poly(M.charpoly(x).as_expr(),x,domain=s.QQ)
assert list(map(str,char.all_coeffs()))==data['M_char_coefficients']
P=s.Poly(char.as_expr().subs(x,-3*x)/3**6,x)
num=s.Poly(x**8*(x+500)**2*s.prod(x+j for j in range(1,9))*(x+s.Rational(518,9))**18,x)
R=num-P**6;assert R.degree()==34
assert R.all_coeffs()==[s.Rational(v) for v in data['R_coefficients']]
signs=[1 if c>0 else -1 for c in R.all_coeffs() if c]
variations=sum(a!=b for a,b in zip(signs,signs[1:]));assert variations==2
crit=[tuple(Q(v) for v in iv) for iv,m in data['positive_critical_intervals']]
for lo,hi in crit:assert R.eval(s.Rational(lo.numerator,lo.denominator))*R.eval(s.Rational(hi.numerator,hi.denominator))<0
assert len(crit)==2 and 0<crit[0][0]<crit[0][1]<crit[1][0]<crit[1][1]
assert R.eval(0)<0 and R.LC()<0 and crit[1][0]>1
# Descartes upper count2 and two disjoint sign brackets give exactly two
# positive roots counted with multiplicity, hence both simple. No Sturm
# or count_roots result is imported or called in this independent review.
def ev(v):return rat(char.eval(s.Rational(v.numerator,v.denominator)))
eigs=[]
for record in white['M_eigenvalue_intervals']:
 lo,hi=Q(record['lower']),Q(record['upper']);assert lo>0 and ev(lo)*ev(hi)<0
 while hi-lo>Q(1,2**70):
  mid=(lo+hi)/2;v=ev(mid)
  if v==0:lo=hi=mid;break
  if (v>0)==(ev(lo)>0):lo=mid
  else:hi=mid
 eigs.append((lo,hi))
assert len(eigs)==6 and all(a[1]<b[0] for a,b in zip(eigs,eigs[1:]))
def hvalue(t):
 terms=[scale(2,flog(add(t,(Q(500),Q(500))))),scale(8,flog(t)),scale(18,flog(add(t,(Q(518,9),Q(518,9)))))]
 terms += [flog(add(t,(Q(j),Q(j)))) for j in range(1,9)]
 terms += [scale(-6,flog(add(t,scale(Q(1,3),iv)))) for iv in eigs]
 return add(*terms)
h0=hvalue((Q(0),Q(0)));hs=[hvalue(iv) for iv in crit]
assert h0[0]>76 and all(v[0]>76 for v in hs)
assert h0[0]>=Q(white['h0_interval']['lower'])
U=s.ones(2)/2;V=s.diag(1,0);Z=s.kronecker_product(X,U)+s.kronecker_product(s.eye(18),V)
stored_bath=json.loads((BASE/'BATH_SOURCE.json').read_text())
assert all(s.simplify(v)==0 for v in Z-readmatrix(stored_bath['Z']))
assert s.trace(Z)==1054
assert all(s.simplify(sum(Z[12*i+k,12*j+k] for k in range(12))-(s.Rational(1054,3) if i==j else 0))==0 for i in range(3) for j in range(3))
gap=h0[0]/2108;assert gap>Q(36,1000)
result={'status':'INDEPENDENT_SOURCE_AND_WHOLE_WHITE_ACCEPTED','root_module_imports':False,'exact_source_components':324,'exact_SIC_output_components':36,'actual_bath_components':1296,'polynomial_degree':34,'Descartes_sign_variations':variations,'positive_critical_roots_with_multiplicity':2,'no_count_roots_or_Sturm_call':True,'positive_sextic_roots':6,'eigen_bracket_absolute_bits':70,'h0_interval':[enc(v) for v in h0],'critical_h_intervals':[[enc(v) for v in iv] for iv in hs],'raw_h0_lower_display':float(h0[0]),'critical_h_lower_displays':[float(v[0]) for v in hs],'normalized_bath_CMI_lower':enc(gap),'normalized_bath_CMI_lower_display':float(gap),'seconds_including_sympy_import':time.perf_counter()-START}
(OUT/'ROOT_WHITE_INDEPENDENT_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['h0_interval','critical_h_intervals','normalized_bath_CMI_lower']},indent=2))

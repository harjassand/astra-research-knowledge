"""Exact critical-point admission of a strong Bell source's ENTIRE white curve."""
from pathlib import Path
from fractions import Fraction as Q
import json,time,sys
sys.set_int_max_str_digits(0)
START=time.perf_counter()
import sympy as s
OUT=Path(__file__).resolve().parent
a=s.symbols('a');x=s.symbols('x');omega=(-1+s.sqrt(3)*s.I)/2
weights=[s.Rational(t,79) for t in [64,8,4,2,1]]
labels=[(0,0),(0,1),(0,2),(1,0),(1,1)]
rho=s.zeros(9);M=s.zeros(3)
for (aa,b),p in zip(labels,weights):
 for j in range(3):
  for k in range(3):rho[3*j+(j+aa)%3,3*k+(k+aa)%3]+=p*omega**(b*(j-k))/3
 i,j=(aa+1)%3,(aa+2)%3
 M[i,i]+=p/2;M[j,j]+=p/2;M[i,j]-=p*omega**b/2;M[j,i]-=p*omega**(-b)/2
rho=rho.applyfunc(s.simplify);M=M.applyfunc(s.simplify)
tau=s.eye(9)/9
pt=s.Matrix(9,9,lambda i,j:rho[(j//3)*3+i%3,(i//3)*3+j%3])
nrho=(s.eye(9)/3-pt)/2
perm=s.zeros(9)
for u in range(3):
 for d in range(3):perm[3*((u+d)%3)+(u+2*d)%3,3*u+d]=1
assert all(s.simplify(v)==0 for v in perm.T*nrho*perm-s.kronecker_product(s.eye(3)/3,M))
P=s.Poly(s.simplify((a*s.eye(3)+M/3).det()),a,domain=s.QQ)
assert P.as_expr()==a**3+a**2/3+s.Rational(515,37446)*a+s.Rational(319,4437351)
char=s.Poly(s.simplify((x*s.eye(3)-M).det()),x,domain=s.QQ)
numerator=s.Poly(a**4*s.prod(a+p for p in weights)*(a+s.Rational(1,9))**9,a)
R=numerator-P**6
assert R.degree()==16 and R.eval(0)<0 and R.LC()<0
def variations(signs):
 vals=[v for v in signs if v]
 return sum(int(bool(vals[i]*vals[i-1]<0)) for i in range(1,len(vals)))
sturm=[s.Poly(t,a,domain=s.QQ) for t in s.sturm(R.as_expr(),a)]
v0=variations([s.sign(t.eval(0)) for t in sturm]);vinf=variations([s.sign(t.LC()) for t in sturm])
assert v0-vinf==2
crit=[(ii,m) for ii,m in R.intervals(eps=s.Rational(1,2**40)) if ii[0]>0]
eigs=char.intervals(eps=s.Rational(1,2**40))
assert len(crit)==2 and all(m==1 for ii,m in crit)
assert len(eigs)==3 and all(m==1 and ii[0]>0 for ii,m in eigs)
assert R.eval(crit[0][0][0])<0<R.eval(crit[0][0][1])
assert R.eval(crit[1][0][0])>0>R.eval(crit[1][0][1])
def rat(v):return Q(int(v.p),int(v.q))
def plus(*ivs):return(sum(v[0] for v in ivs),sum(v[1] for v in ivs))
def scale(c,v):return(min(c*v[0],c*v[1]),max(c*v[0],c*v[1]))
def times(v,w):
 t=[p*q for p in v for q in w]
 return min(t),max(t)
def alog(y):
 z=(y-1)/(y+1);n=24
 lo=2*sum((z**(2*j+1)/Q(2*j+1) for j in range(n)),Q(0))
 tail=2*z**(2*n+1)/(Q(2*n+1)*(1-z*z))
 return lo,lo+tail
ln2=alog(Q(2))
def logq(v):
 k=0;y=v
 assert y>0
 while y<1:y*=2;k-=1
 while y>2:y/=2;k+=1
 return plus(alog(y),scale(k,ln2))
def flog(iv):
 lo,hi=iv
 if hi==0:return Q(0),Q(0)
 assert lo>0
 return times(iv,(logq(lo)[0],logq(hi)[1]))
lambdaivs=[tuple(map(rat,ii)) for ii,m in eigs]
def hvalue(iv):
 terms=[flog(plus(iv,(rat(p),rat(p)))) for p in weights]
 terms += [scale(4,flog(iv)),scale(9,flog(plus(iv,(Q(1,9),Q(1,9)))))]
 terms += [scale(-6,flog(plus(iv,scale(Q(1,3),ll)))) for ll in lambdaivs]
 return plus(*terms)
h0=hvalue((Q(0),Q(0)));bounds=[hvalue(tuple(map(rat,ii))) for ii,m in crit]
assert h0[0]>Q(1,5) and all(v[0]>Q(1,5) for v in bounds)
assert rat(crit[1][0][0])>Q(1,16)
def strings(iv):return [str(v) for v in iv]
out={'status':'EXACT_STRONG_BELL_ENTIRE_WHITE_CURVE_ADMITTED','labels':labels,'weights':list(map(str,weights)),'channel_identity':'INDEPENDENT_EXACT9x9_REPLAY','M_characteristic_polynomial_coefficients':list(map(str,char.all_coeffs())),'P_coefficients':list(map(str,P.all_coeffs())),'R_coefficients':list(map(str,R.all_coeffs())),'Sturm_coefficients':[list(map(str,t.all_coeffs())) for t in sturm],'Sturm_variations_at_0_and_infinity':[v0,vinf],'positive_critical_roots':[strings(tuple(map(rat,ii))) for ii,m in crit],'SIC_eigenvalue_intervals':[strings(v) for v in lambdaivs],'h0_interval':strings(h0),'critical_h_intervals':[strings(v) for v in bounds],'proved_compact_lower':'1/5 on[0,1/16]','whole_curve':'STRICTLY_POSITIVE_AT_EVERY_FINITE_a>=0; tends0_at_infinity','noncommuting_bath_CMI_lower':'1/100','bath_normalizing_trace':'10','reference_dimension':6,'extension_dimension':54,'seconds_including_sympy_import':time.perf_counter()-START,'scope':'One exact strong coherent5-Bell source, all scalar white noise and all positive common baths via inherited identity. Root uses exact linear algebra/Sturm/rational log intervals, no numeric entropy premise. Not all5-weight white curves, arbitrary Choi states, physical implementation or priority.'}
# Finalize after constructing/checking the actual bath source.
Ub=s.ones(2)/2;Vb=s.diag(1,0);Z=s.kronecker_product(rho,Ub)+s.kronecker_product(s.eye(9),Vb)
assert Ub*Ub==Ub and Vb*Vb==Vb and Ub*Vb!=Vb*Ub
assert s.trace(Z)==10
assert all(s.simplify(sum(Z[6*i+j,6*k+j] for j in range(6))-(s.Rational(10,3) if i==k else 0))==0 for i in range(3) for k in range(3))
off=Z[:6,6:12];assert any(s.simplify(v)!=0 for v in off*off)
(OUT/'MATRIX_INPUT.json').write_text(json.dumps({'rho':[[str(v) for v in row] for row in rho.tolist()],'M':[[str(v) for v in row] for row in M.tolist()],'Z':[[str(v) for v in row] for row in Z.tolist()]},indent=2)+'\n')
out['seconds_including_sympy_import']=time.perf_counter()-START
out['max_entropy_endpoint_bits']=max(max(v.numerator.bit_length(),v.denominator.bit_length()) for iv in [h0]+bounds for v in iv)
(OUT/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'critical_points':[list(map(float,ii)) for ii,m in crit],'h0_lower_display':float(h0[0]),'critical_lower_displays':[float(v[0]) for v in bounds],'seconds':out['seconds_including_sympy_import']},indent=2))

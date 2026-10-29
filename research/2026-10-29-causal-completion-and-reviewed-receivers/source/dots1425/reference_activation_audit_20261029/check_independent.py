import sympy as s,mpmath as m,json,hashlib
from pathlib import Path
p=Path(__file__).parent;src=p.parent/'nonstationary_coverage_obstruction_20261029'
for mn in ['STRONGER_SHA256SUMS.txt','REFERENCE_ACTIVATION_SHA256SUMS.txt','ACTIVATION_SCOPE_SHA256SUMS.txt']:
 for ln in (src/mn).read_text().splitlines():
  if ln.strip():
   h,f=ln.split(maxsplit=1);assert hashlib.sha256((src/f.lstrip('*')).read_bytes()).hexdigest()==h
x=s.symbols('e',positive=True);v=s.Matrix([s.sqrt(x),0,0,s.sqrt(1-x)]);r=s.Rational(2,3)*v*v.T;r[1,1]+=s.Rational(1,3)
K=[s.Matrix([[0,1/s.sqrt(2)],[1,0]]),s.diag(0,1/s.sqrt(2))];ks=[s.kronecker_product(k,s.eye(2)) for k in K]
F=lambda z:s.simplify(sum((k*z*k.T for k in ks),s.zeros(4)))
y=F(r);z=F(y)
def ref(A):return s.Matrix([[A[i,j]+A[i+2,j+2] for j in range(2)] for i in range(2)])
def pop0(A):return A[0,0]+A[1,1]
assert s.simplify(ref(y)-ref(r))==s.zeros(2) and s.simplify(ref(z)-ref(r))==s.zeros(2)
assert s.simplify(pop0(y)-pop0(r))==-x and s.simplify(pop0(z)-pop0(r))==-x/2
u=s.symbols('u');assert s.factor(r.charpoly(u).as_expr())==u**2*(3*u-2)*(3*u-1)/9
assert s.simplify((u*s.eye(4)-y).det(method="berkowitz")-u*u*(u-(1+x)/3)*(u-(2-x)/3))==0
block=z.extract([0,3],[0,3]);tr=s.trace(block);det=s.factor(block.det());assert s.simplify(tr-s.Rational(2,3)+x/6)==0 and s.simplify(det-x/9+x*x/18)==0
small=(tr-s.sqrt(tr**2-4*det))/2;assert s.limit(small/x,x,0,dir='+')==s.Rational(1,6)
assert z[2,2]==x/3 and z[1,1]==s.Rational(1,3)-x/6
h=lambda t:-t*s.log(t)-(1-t)*s.log(1-t)
l1=h((1+x)/3)-h(s.Rational(1,3))+x*s.log(2)
assert s.limit(l1/x,x,0,dir='+')==s.Rational(4,3)*s.log(2)
# Fully independent arbitrary-precision diagonalization rather than reusing block eigenvalue formulas.
m.mp.dps=90;rows=[]
for power in [4,12,30]:
 e=m.mpf(10)**(-power);rr=m.matrix([[2*e/3,0,0,2*m.sqrt(e*(1-e))/3],[0,m.mpf(1)/3,0,0],[0,0,0,0],[2*m.sqrt(e*(1-e))/3,0,0,2*(1-e)/3]])
 mats=[m.matrix([[0,1/m.sqrt(2)],[1,0]]),m.matrix([[0,0],[0,1/m.sqrt(2)]])]
 def kron(a,b):return m.matrix([[a[i//b.rows,j//b.cols]*b[i%b.rows,j%b.cols] for j in range(a.cols*b.cols)] for i in range(a.rows*b.rows)])
 lifts=[kron(k,m.eye(2)) for k in mats]
 def apply(a):return sum((k*a*k.T for k in lifts),m.zeros(4))
 def entropy(a):return -sum(v*m.log(v) for v in m.eigsy(a,eigvals_only=True) if v>m.mpf('1e-80'))
 yy=apply(rr);zz=apply(yy);L1=entropy(yy)-entropy(rr)+e*m.log(2);L2=entropy(zz)-entropy(rr)+e*m.log(2)/2
 coh=m.mpf(2)/3*(-e*m.log(e)-(1-e)*m.log(1-e));dist=m.mpf(2)/3*m.sqrt(e*(1-e))
 rows.append({'epsilon':str(e),'L1_over_e':str(L1/e),'coherence_over_L1_log':str(coh/L1/m.log(1/e)),'L2_over_L1_log':str(L2/L1/m.log(1/e)),'trace_over_sqrt_L1':str(dist/m.sqrt(L1))})
out={'manifests_verified':True,'exact_input_and_one_step_characteristic_polynomials':'pass','exact_reference_marginal_preservation':'pass','exact_population_changes':['-e','-e/2'],'exact_small_two_step_eigenvalue_slope':'1/6','exact_L1_slope':'4*log(2)/3','independent_dense_eigensolver_precision':90,'rows':rows,'scope':'Exact symbolic identities and independent high-precision spectral diagnostics; no unrestricted N371 or all-noisy-product no-go.'}
(p/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

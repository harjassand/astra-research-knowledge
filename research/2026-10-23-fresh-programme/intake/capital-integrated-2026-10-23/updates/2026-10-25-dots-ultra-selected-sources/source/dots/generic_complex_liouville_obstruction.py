"""Exact obstruction to the particular output-arithmetic-mean lift, not to coefficient equality."""
import sympy as S,json,time,resource
from pathlib import Path
start=time.perf_counter();I=S.eye(2)
s=S.Matrix([[1,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,1]])/2
s=S.Rational(9,10)*s+S.eye(4)/40
pt=S.zeros(4)
for a in range(2):
 for b in range(2):
  for i in range(2):
   for j in range(2):pt[a*2+i,b*2+j]=s[a*2+j,b*2+i]
x=S.kronecker_product(s,I);y0=S.kronecker_product(pt,I);y=S.zeros(8)
for a in range(2):
 for b in range(2):
  for i in range(2):
   for j in range(2):
    for k in range(2):
     for l in range(2):y[4*a+2*i+j,4*b+2*k+l]=y0[4*a+2*j+i,4*b+2*l+k]
g=(x+y)/4
paulis=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-S.I],[S.I,0]]),S.diag(1,-1)]
effects=[(I+sign*S.Rational(1,2)*p)/6 for p in paulis for sign in [1,-1]]
for e in effects:
 si=S.zeros(2);gi=S.zeros(4)
 for a in range(2):
  for b in range(2):
   si+=e[b,a]*s[a*2:(a+1)*2,b*2:(b+1)*2]
   gi+=e[b,a]*g[a*4:(a+1)*4,b*4:(b+1)*4]
 assert gi==(S.kronecker_product(si,I)+S.kronecker_product(I,si.T))/4
assert S.Matrix.hstack(*[S.Matrix(e).reshape(4,1) for e in effects]).rank()==4
vals=g.eigenvals();mn=(1-S.Rational(9,10)*S.sqrt(3))/8
assert mn in vals and mn<0
out={'input_sigma':[[str(z) for z in s.row(i)] for i in range(4)],'input_eigenvalues':{str(k):v for k,v in s.eigenvals().items()},'forced_lift_eigenvalues':{str(k):v for k,v in vals.items()},'negative_eigenvalue':str(mn),'effects':'(I +/- sigma_j/2)/6 for j=X,Y,Z','effect_floor':'1/12','effect_span_rank':4,'all_output_arithmetic_mean_identities_exact':True,'scope':'The unique r^2-dimensional top block matching these IC measurement outputs is not positive. This refutes this literal lift, NOT equality of complete and conditional coefficients.','elapsed_seconds':time.perf_counter()-start,'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

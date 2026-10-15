from pathlib import Path
from fractions import Fraction as F
import json,hashlib,itertools,time
import sympy as s
R=Path(__file__).resolve().parents[1];path=R/'workers/nonlinear_qc/G_EXACT_HEAT_CERTIFICATE.json';raw=path.read_bytes();v=json.loads(raw);start=time.monotonic()
B=[[F(x) for x in row] for row in v['basis']];T=[[F(x) for x in row] for row in v['reduced_gram']];Q=[[F(x) for x in row] for row in v['gram']]
assert len(B)==24 and all(len(row)==18 for row in B);assert len(T)==18 and all(len(row)==18 for row in T);assert all(T[i][j]==T[j][i] for i in range(18) for j in range(18))
L=[[F(int(i==j)) for j in range(18)] for i in range(18)];piv=[]
for i in range(18):
 d=T[i][i]-sum(L[i][k]*L[i][k]*piv[k] for k in range(i));assert d>0;piv.append(d)
 for j in range(i+1,18):L[j][i]=(T[j][i]-sum(L[j][k]*L[i][k]*piv[k] for k in range(i)))/d
for i in range(24):
 for j in range(24):assert Q[i][j]==sum(B[i][k]*T[k][l]*B[j][l] for k in range(18) for l in range(18))
a,b,c,d=s.symbols('a b c d',real=True);A=[a,b,c,d];h=list(s.symbols('h0:6',real=True));u=a*a+c*c;vv=b*b+d*d;q=a*d-b*c
G=3*(u+vv-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u
Hx=s.Matrix([h[0],h[1],h[3],h[4]]);Hy=s.Matrix([h[1],h[2],h[4],h[5]]);H=s.hessian(G,A);D=s.Matrix([[s.Rational(x) for x in row] for row in v['diffusion']]);assert D==s.diag(s.Rational(4897,5000),s.Rational(5103,5000))
mon=[A[i]*A[j] for i,j in v['quadratic_coefficient_order']];om={}
for pair,co in zip(v['omega_pair_order'],v['omega_coefficients']):om[tuple(pair)]=s.expand(sum(s.Rational(x)*z for x,z in zip(co,mon)))
def omega(i,j):return om[i,j] if i<j else -om[j,i] if i>j else 0
for i,j,k in itertools.combinations(range(4),3):assert s.expand(s.diff(omega(j,k),A[i])-s.diff(omega(i,k),A[j])+s.diff(omega(i,j),A[k]))==0
Z=[x*y for x in A for y in h];sos=sum(s.Rational(Q[i][i].numerator,Q[i][i].denominator)*Z[i]*Z[i] for i in range(24))
sos+=sum(2*s.Rational(Q[i][j].numerator,Q[i][j].denominator)*Z[i]*Z[j] for i in range(24) for j in range(i+1,24))
heat=D[0,0]*(Hx.T*H*Hx)[0]+D[1,1]*(Hy.T*H*Hy)[0]
null=sum(omega(i,j)*(Hx[i]*Hy[j]-Hx[j]*Hy[i]) for i in range(4) for j in range(i+1,4))
diff=s.Poly(s.expand(sos-heat-null),*(A+h));assert diff.is_zero
receipt=dict(status='EXACT_PASS',scope='Independent root reconstruction from only portable certificate JSON: Fraction LDL positivity, everyGram/basis entry, quartic Hessian density, all four closedness equations and coefficient identity. Analytic heat/QC implication reviewed separately; no historical or external certification.',certificate_path=str(path.relative_to(R)),certificate_sha256=hashlib.sha256(raw).hexdigest(),positive_exact_fraction_pivots=len(piv),basis_shape=[24,18],reconstructed_gram_entries=576,identity_nonzero_coefficients=len(diff.terms()) if not diff.is_zero else 0,closedness_triples=4,diffusion=[str(D[0,0]),str(D[1,1])],wall_seconds=time.monotonic()-start,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(R/'root/G_HEAT_INDEPENDENT_CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))

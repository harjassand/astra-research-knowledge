from pathlib import Path
import json,sympy as S,hashlib
base=Path(__file__).parent
cert=json.loads((base/'ALL_R_STRESS_EXACT_CERTIFICATE.json').read_text())
r,a,b,c,d,s=S.symbols('r a b c d s',real=True)
loc={str(x):x for x in [r,a,b,c,d,s]}
parse=lambda x:S.sympify(x,locals=loc)
Q=S.Matrix([[S.Rational(x) for x in row] for row in cert['gram']]);n0=cert['block_split']
z0=S.Matrix([parse(x) for x in cert['z0']]);z1=S.Matrix([parse(x) for x in cert['z1']]);n=Q.rows
sigma1=parse(cert['stress']['sigma1']);sigma2=parse(cert['stress']['sigma2'])
u=(a+s)**2+c*c;v=b*b+(d+s)**2;j=(a+s)*(d+s)-b*c
J=S.Rational(3,8)*r/(r+2)*(u+v-2*j)**2+r*(r-1)*u*u/6+j*j+r*u*j
G=J-parse(cert['subtracted_constant'])-parse(cert['subtracted_first_row_tangent'])-sigma1*c-sigma2*d
rhs=(z0.T*Q[:n0,:n0]*z0)[0]+r*(z1.T*Q[n0:,n0:]*z1)[0]
identity=S.Poly(S.cancel((r+2)*G-rhs),r,a,b,c,d,s)
if identity.as_expr()!=0:raise RuntimeError('pointwise identity fails')
blocks=cert['positive_definite_blocks']
if sorted(i for inds in blocks for i in inds)!=list(range(n)):raise RuntimeError('partition fail')
for i in range(n):
 for k in range(n):
  if not any(i in inds and k in inds for inds in blocks) and Q[i,k]!=0:raise RuntimeError('cross-block coefficient nonzero')
def ldl_positive(B):
 L=S.eye(B.rows);p=[]
 for k in range(B.rows):
  d0=S.factor(B[k,k]-sum(L[k,j]**2*p[j] for j in range(k)))
  if not d0>0:raise RuntimeError('nonpositive exact pivot')
  p.append(d0)
  for i in range(k+1,B.rows):L[i,k]=S.factor((B[i,k]-sum(L[i,j]*L[k,j]*p[j] for j in range(k)))/d0)
 if L*S.diag(*p)*L.T!=B:raise RuntimeError('LDL product fails')
 return p
piv=[ldl_positive(Q.extract(inds,inds)) for inds in blocks]
if [[str(x) for x in pp] for pp in piv]!=cert['ldl_pivots']:raise RuntimeError('saved pivots differ')
eta=S.Rational(1,512)
coercivity_pivots=[ldl_positive(Q.extract(inds,inds)-eta*S.eye(len(inds))) for inds in blocks if inds[0]>=n0]
rowvars=[a,b,c,d]
B4=sum(x**4 for x in rowvars)+sum(rowvars[i]**2*rowvars[j]**2 for i in range(4) for j in range(i+1,4))
N2=sum(x*x for x in rowvars)
margin=sum((rowvars[i]**2-rowvars[j]**2)**2 for i in range(4) for j in range(i+1,4))
if S.expand(8*B4-5*N2*N2-margin)!=0:raise RuntimeError('five-eighths quartic margin')
K=r/(4*(r+2))*(6*(r+2)*s*s+14*(r+2)*s*a+(4*r+3)*a*a+14*b*b)
if S.cancel(S.diff(sigma1,b)+S.diff(sigma2,a)-K)!=0:raise RuntimeError('stress divergence identity')
h=a*d-b*c+s*(a+d)
if S.cancel(G.subs(r,0)-h*h)!=0:raise RuntimeError('determinant anchor')
G_s=S.Poly(S.cancel(G),s)
G2=(r+1)**2*a*a+(r/2+2)*a*d+r*(r+2)*c*c/3+d*d
G1=r*(2*r+1)/3*a*(a*a+c*c)+(5*r/4+2)*a*a*d-2*(r+1)*a*b*c+2*a*d*d-2*b*c*d+r*c*c*d
if S.cancel(G_s.coeff_monomial(s*s)-G2)!=0:raise RuntimeError('all-r quadratic derivation')
if S.cancel(G_s.coeff_monomial(s)-G1)!=0:raise RuntimeError('all-r cubic derivation')
if S.factor((r+1)**2-(r/4+1)**2)!=3*r*(5*r+8)/16:raise RuntimeError('all-r quadratic determinant')
P_r=S.Poly(S.cancel((r+2)*G),r)
P3=(a*a+c*c+2*a*s)**2/6+s*s*(a*a+c*c)/3
if S.expand(P_r.coeff_monomial(r**3)-P3)!=0:raise RuntimeError('leading parametric Gram support')
alpha=S.Rational(3,8)*r/(r+2)
Sn1=-(r+2)*s*s*b+4*alpha*b**3
Sn2=(r+2)*s**3+(3*r+4)*s*s*a+(3*r+2)*s*a*a+(r-4*alpha)*a**3
Gn=S.cancel(J-parse(cert['subtracted_constant'])-parse(cert['subtracted_first_row_tangent'])-Sn1*c-Sn2*d)
Gn_s=S.Poly(Gn,s)
Gn2=(r+1)**2*a*a+r*(r+2)*c*c/3+d*d
Gn1=r*(2*r+1)/3*a*(a*a+c*c)-2*(r+1)*a*b*c+2*a*d*d-2*b*c*d+r*c*c*d
if S.cancel(Gn_s.coeff_monomial(s*s)-Gn2)!=0:raise RuntimeError('natural stress quadratic derivation')
if S.cancel(Gn_s.coeff_monomial(s)-Gn1)!=0:raise RuntimeError('natural stress cubic derivation')
Gn_fixed=S.cancel(Gn.subs({a:1,b:3,c:1,d:1,s:1}))
if S.cancel(Gn_fixed-(10*r**3-2*r*r+115*r-24)/(3*(r+2)))!=0:raise RuntimeError('natural stress failure polynomial')
if Gn_fixed.subs(r,S.Rational(1,10))!=-S.Rational(139,70):raise RuntimeError('natural stress failure witness')
t=S.symbols('t',real=True)
flux=S.cancel((2*sigma1+sigma2).subs({a:2*s*t,b:s*t}))
A=(8*r+13)/(6*(r+2));F=t*(S.Rational(3,2)+S.Rational(7,2)*t+A*t*t)
if S.cancel(flux-((r+2)*s**3+2*r*s**3*F))!=0:raise RuntimeError('nonseparated flux formula')
quot=S.cancel((F-F.subs(t,S.Rational(1,4)))/(t-S.Rational(1,4)))
expected=A*t*t+(S.Rational(7,2)+A/4)*t+(S.Rational(3,2)+S.Rational(7,8)+A/16)
if S.cancel(quot-expected)!=0:raise RuntimeError('flux quadratic factor')
D=S.factor((S.Rational(7,2)+A/4)**2-4*A*(S.Rational(3,2)+S.Rational(7,8)+A/16))
Dp=(304*r*r+2008*r+2791)/(192*(r+2)**2)
if S.cancel(D-Dp)!=0:raise RuntimeError('positive flux discriminant')
negative_root_check=S.factor((92*r+181)**2-(912*r*r+6024*r+8373))
if any(x<=0 for x in S.Poly(negative_root_check,r).all_coeffs()):raise RuntimeError('negative root sign certificate')
receipt={'status':'PASS','scope':'Exact polynomial identity, four positive-definite rational Gram blocks, Q1 >= I/512, stress-divergence identity, determinant anchor, and nonseparated laminate flux algebra. Analytic integration proof is stated separately. No general quasiconvexity or historical novelty claim.','checks':{'pointwise_polynomial_identity':True,'positive_definite_blocks':list(map(len,blocks)),'exact_ldl_pivot_count':sum(map(len,piv)),'q1_floor':'1/512','q1_shifted_ldl_pivot_count':sum(map(len,coercivity_pivots)),'quartic_monomial_five_eighths_margin_identity':True,'stress_divergence_identity':True,'r_zero_determinant_square_anchor':True,'all_r_taylor_and_parametric_support_derivations':True,'failed_natural_stress_exact_witness':'r=1/10, (a,b,c,d,s)=(1,3,1,1,1), G=-139/70','nonseparated_laminate_flux_factorization':True,'laminate_discriminant_positive_coefficients':[304,2008,2791],'negative_root_sign_polynomial':str(negative_root_check)},'certificate_sha256':hashlib.sha256((base/'ALL_R_STRESS_EXACT_CERTIFICATE.json').read_bytes()).hexdigest(),'coercivity_shifted_ldl_pivots':[[str(x) for x in pp] for pp in coercivity_pivots]}
(base/'VERIFICATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='coercivity_shifted_ldl_pivots'},indent=2))

"""Independent exact verifier for G_EXACT_HEAT_CERTIFICATE.json.

Uses only JSON, pathlib and SymPy. It imports no search/acquisition helper,
reads no NumPy candidate, and performs no sampled positivity calculation.
The global analytic implication is proved in G_QUASICONVEXITY_PROOF.md.
"""
from pathlib import Path
import json,time,hashlib
import sympy as S

ROOT=Path(__file__).resolve().parent
tick=time.monotonic()
path=ROOT/'G_EXACT_HEAT_CERTIFICATE.json'
cert=json.loads(path.read_text())
checks=[]


def record(name,detail):
    checks.append({'name':name,'status':'PASS','detail':detail})
    print('PASS:',name,flush=True)


def matrix(values):
    return S.Matrix([[S.Rational(v) for v in row] for row in values])


assert cert['schema']=='astra-G-closed-anisotropic-heat/1'
assert cert['matrix_entry_order']==['a','b','c','d']
assert cert['jet_order']==['phi1_xx','phi1_xy','phi1_yy','phi2_xx','phi2_xy','phi2_yy']
x=S.symbols('a b c d');z=S.symbols('z0:6')
a,b,c,d=x
u=a*a+c*c;v=b*b+d*d;j=a*d-b*c
G=3*(u+v-2*j)**2+S.Rational(35,24)*u*u+j*j-S.Rational(5,2)*j*u
assert all(sum(exp)==4 for exp,co in S.Poly(G,x).terms())
record('Integrand and variable conventions',str(S.expand(G)))

diffusion=matrix(cert['diffusion'])
assert diffusion==S.diag(S.Rational(4897,5000),S.Rational(5103,5000))
assert diffusion[0,0]>0 and diffusion[1,1]>0
record('Exact positive anisotropic diffusion',[str(diffusion[0,0]),str(diffusion[1,1])])

basis=matrix(cert['basis']);reduced=matrix(cert['reduced_gram']);gram=matrix(cert['gram'])
assert basis.shape==(24,18) and basis.rank()==18
assert reduced.shape==(18,18) and reduced==reduced.T
assert gram.shape==(24,24) and gram==gram.T
assert gram==basis*reduced*basis.T
L,D=reduced.LDLdecomposition(hermitian=False)
pivots=list(D.diagonal())
assert all(v>0 for v in pivots)
assert L*D*L.T==reduced
assert [str(v) for v in pivots]==cert['ldl_diagonal']
record('Exact PSD Gram through positive 18-dimensional factor',{'rank':18,'positive_LDL_pivots':18})

pairs=[(i,k) for i in range(4) for k in range(i+1,4)]
monpairs=[(i,k) for i in range(4) for k in range(i,4)]
assert cert['omega_pair_order']==[list(p) for p in pairs]
assert cert['quadratic_coefficient_order']==[list(p) for p in monpairs]
omega={}
for pair,row in zip(pairs,cert['omega_coefficients']):
    assert len(row)==10
    omega[pair]=sum(S.Rational(co)*x[i]*x[k] for co,(i,k) in zip(row,monpairs))


def form(i,k):
    if i==k:
        return S.Integer(0)
    return omega[(i,k)] if i<k else -omega[(k,i)]


for i in range(4):
    for k in range(i+1,4):
        for ell in range(k+1,4):
            closed=S.diff(form(k,ell),x[i])-S.diff(form(i,ell),x[k])+S.diff(form(i,k),x[ell])
            assert S.expand(closed)==0
record('Exact closedness of the quadratic two-form','All four exterior derivative components vanish identically')

primitive=[sum(x[k]*form(k,i) for k in range(4))/4 for i in range(4)]
for i,k in pairs:
    assert S.expand(S.diff(primitive[k],x[i])-S.diff(primitive[i],x[k])-form(i,k))==0
record('Global polynomial primitive','alpha=(1/4) i_Euler omega; d alpha=omega exactly')

B1=S.Matrix([z[0],z[1],z[3],z[4]])
B2=S.Matrix([z[1],z[2],z[4],z[5]])
Z=S.Matrix([xx*zz for xx in x for zz in z])
H=S.hessian(G,x)
heat=diffusion[0,0]*(B1.T*H*B1)[0]+diffusion[1,1]*(B2.T*H*B2)[0]
correction=sum(form(i,k)*(B1[i]*B2[k]-B1[k]*B2[i]) for i,k in pairs)
identity=S.Poly(S.expand((Z.T*gram*Z)[0]-heat-correction),*(x+z))
assert identity.is_zero
record('Complete compatible-jet polynomial identity','All 210 possible A^2 jet^2 coefficients agree exactly')

identity_point={a:1,b:0,c:0,d:1}
assert G.subs(identity_point)==-S.Rational(1,24)
assert G.subs({a:1,b:0,c:0,d:-1})==S.Rational(1271,24)
law_mean=(36**4*(-S.Rational(1,24))+36**2*S.Rational(1271,24))/(1+36**2)
assert law_mean==-S.Rational(1350,1297)
assert S.expand(G.subs({a:1,b:S.Symbol('t'),c:0,d:1})+S.Rational(1,24)-3*S.Symbol('t')**4)==0
record('Boundary acoustic and nonpolyconvexity witness constants',{
    'G_I':'-1/24','acoustic_zero':'G(I+t e12)=-1/24+3t^4',
    'lifted_barycenter_law_gap':str(law_mean)})

receipt={'status':'EXACT_PASS','groups':len(checks),'checks':checks,
    'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    'seconds':time.monotonic()-tick,
    'scope':'exact finite polynomial identity, exact closedness and PSD; analytic heat and QC proof is separate',
    'external_review':'UNKNOWN','historical_novelty':'UNKNOWN'}
(ROOT/'G_HEAT_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='checks'},indent=2),flush=True)

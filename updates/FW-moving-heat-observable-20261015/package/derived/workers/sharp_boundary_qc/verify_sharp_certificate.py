"""Standalone rational certificate verifier. Reads JSON only, no discovery code.

Usage: python verify_sharp_certificate.py [certificate.json]
Requires Python and SymPy. No optimizer, float eigensolver, repository source,
or pickle files are used. The heat-flow analytic implication is in REPORT.txt.
"""
import sympy as s
import json,sys,hashlib
from pathlib import Path
from itertools import combinations,combinations_with_replacement as cwr
base=Path(__file__).parent
path=Path(sys.argv[1]) if len(sys.argv)>1 else base/'SHARP_ACOUSTIC_HEAT_CERTIFICATE.json'
data=json.loads(path.read_text())
r,t=s.symbols('r t',real=True)
def pol(coeffs):return sum((s.Rational(vv)*r**ii for ii,vv in enumerate(coeffs)),s.S.Zero)
def matrix(rows):return s.Matrix([[pol(vv) for vv in row] for row in rows])
DC=pol(data['C_denominator']);DS=pol(data['S_denominator']);DW=pol(data['W_denominator'])
CN=matrix(data['C_numerator']);SN=matrix(data['S_numerator']);WN=matrix(data['W_numerator'])
d1,d2=[pol(pp) for pp in data['diffusion']]
assert CN.shape==(24,12) and SN.shape==(12,12) and WN.shape==(6,10)
assert SN==SN.T and DS==DW==-(r+2)
assert s.expand(DC-9*(r+1)*(2*r+1))==0
assert CN[12:24,:]==DC*s.eye(12)
lo,hi=map(s.Rational,data['interval']);assert (lo,hi)==(-s.Rational(21,8),-s.Rational(5,2))
assert d1+d2==2
assert all(dd.subs(r,endpoint)>0 for dd in [d1,d2] for endpoint in [lo,hi])
assert all(s.degree(dd,r)<=1 for dd in [d1,d2])
x=s.Matrix(s.symbols('a b c d'));a,b,c,d=x
z=s.Matrix(s.symbols('z0:6'))
B1=s.Matrix([z[0],z[1],z[3],z[4]]);B2=s.Matrix([z[1],z[2],z[4],z[5]])
Z=s.kronecker_product(x,z)
u=a*a+c*c;v=b*b+d*d;j=a*d-b*c
F=3*r/(8*(r+2))*(u+v-2*j)**2+r*(r-1)*u**2/6+j*j+r*u*j
HH=s.hessian(F,x)
heat=d1*(B1.T*HH*B1)[0]+d2*(B2.T*HH*B2)[0]
mons=s.Matrix([x[ii]*x[jj] for ii,jj in cwr(range(4),2)])
OO=s.zeros(4)
for (ii,jj),pp in zip(combinations(range(4),2),WN*mons):OO[ii,jj]=pp;OO[jj,ii]=-pp
print('Checking universal rational heat identity...',flush=True)
lhs=(Z.T*CN*SN*CN.T*Z)[0]
rhs=DC**2*s.expand(DS*heat)+(DC**2*(B1.T*OO*B2)[0])
diff=s.Poly(s.expand(lhs-rhs),*(list(x)+list(z)))
assert all(s.cancel(cc)==0 for cc in diff.coeffs())
closed=[s.expand(s.diff(OO[kk,ll],x[ii])-s.diff(OO[ii,ll],x[kk])+s.diff(OO[ii,kk],x[ll]))
        for ii,kk,ll in combinations(range(4),3)]
assert all(cc==0 for cc in closed)
primitive=OO.T*x/4
assert all(s.expand(s.diff(primitive[jj],x[ii])-s.diff(primitive[ii],x[jj])-OO[ii,jj])==0
           for ii,jj in combinations(range(4),2))
print('Checking six exact Bernstein matrices...',flush=True)
degree=data['bernstein']['degree'];assert degree==5
BB=[s.Matrix([[s.Rational(vv) for vv in row] for row in mm]) for mm in data['bernstein']['matrices']]
assert len(BB)==degree+1
reconstruction=sum((s.binomial(degree,ii)*t**ii*(1-t)**(degree-ii)*BB[ii]
                    for ii in range(degree+1)),s.zeros(12))
assert all(s.expand(vv)==0 for vv in SN.subs(r,lo+t/8)-reconstruction)
pivots=[]
for ii,BBi in enumerate(BB):
    assert BBi==BBi.T
    LL,DD=BBi.LDLdecomposition(hermitian=False)
    assert LL*DD*LL.T==BBi
    pp=list(DD.diagonal());assert len(pp)==12 and all(vv>0 for vv in pp)
    pivots.append([str(vv) for vv in pp])
print('Checking the two fourth-order acoustic contacts...',flush=True)
def acoustic(AA,xi):
    rr=s.Matrix([xi[0],xi[1],0,0])
    return s.factor((rr.T*HH*rr)[0].subs(dict(zip(x,list(AA)))))
oldA=s.Matrix([[1,-(r+1)*t],[(r+1)*t,1]])
newA=s.Matrix([[-3*(r+1)*t/(2*r+1),(2*r+1)/3],[1,(r+1)*t]])
assert acoustic(oldA,(t,1))==s.Rational(2,3)*r*(r+1)**2*(r+2)*t**4
assert acoustic(newA,(1,t))==6*r*(r+1)**2*(r+2)*t**4/(2*r+1)**2
alpha=s.symbols('alpha')
Fa=alpha*(u+v-2*j)**2+r*(r-1)*u**2/6+j*j+r*u*j
AA0=s.Matrix([[0,(2*r+1)/3],[1,0]])
qbelow=s.diff(Fa,a,2).subs(dict(zip(x,list(AA0))))
assert s.factor(qbelow-16*(r+2)**2/9*(alpha-3*r/(8*(r+2))))==0
p,q=s.symbols('p q');rot=s.Matrix([[p,-q],[q,p]])
kernel=[]
for AA,xi in [(oldA,(t,1)),(newA,(1,t))]:
    Arot=rot*AA;nn,mm=xi;target=rot[:,0]
    zz=s.Matrix([target[0]*nn*nn,target[0]*nn*mm,target[0]*mm*mm,
                 target[1]*nn*nn,target[1]*nn*mm,target[1]*mm*mm])
    ZZ=s.kronecker_product(s.Matrix(list(Arot)),zz)
    for order in [0,1]:
        vv=ZZ.diff(t,order).subs(t,0)
        for mon in [p*p,p*q,q*q]:kernel.append(s.Matrix([s.Poly(vv0,p,q).coeff_monomial(mon) for vv0 in vv]))
KK=s.Matrix.hstack(*kernel)
assert all(s.cancel(vv)==0 for vv in KK.T*CN)
assert s.factor(KK[:12,:].det())!=0
receipt={'status':'PASS','certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'sympy_version':s.__version__,'universal_identity':True,'closedness':True,'primitive':True,
         'moving_support_rank':12,'forced_kernel_rank':12,'fourth_order_acoustic_contacts':2,
         'bernstein_degree':degree,'positive_rational_pivots':72,'pivots':pivots,
         'positive_diffusion_whole_interval':True,
         'scope':'quasiconvexity at the exact acoustic floor for every r in [-21/8,-5/2]; analytic argument in REPORT.txt',
         'formal_proof_verification':False,'external_review':False}
(base/'SHARP_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: identity, closedness, primitive, rank-12 moving support, two acoustic contacts, 72 positive exact pivots.',flush=True)

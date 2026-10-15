"""Portable exact universal r<-2 verifier. Reads only the universal JSON.

No imports from discovery code, pickle, optimizer, or floating-point spectrum.
The analytic implication is recorded in UNIVERSAL_REPORT.txt.
"""
import sympy as s
import json,hashlib,sys
from pathlib import Path
from itertools import combinations,combinations_with_replacement as cwr
base=Path(__file__).parent
path=Path(sys.argv[1]) if len(sys.argv)>1 else base/'UNIVERSAL_SHARP_NEGATIVE_CERTIFICATE.json'
data=json.loads(path.read_text());r,uu=s.symbols('r uu',real=True)
def pol(coeffs):return sum((s.Rational(vv)*r**ii for ii,vv in enumerate(coeffs)),s.S.Zero)
def rational(item):return s.cancel(pol(item['numerator'])/pol(item['denominator']))
def matrix(rows):return s.Matrix([[rational(vv) for vv in row] for row in rows])
def polynomial_sign(pp):
    cc=s.Poly(pp,uu).all_coeffs()
    if all(vv>=0 for vv in cc) and any(vv>0 for vv in cc):return 1
    if all(vv<=0 for vv in cc) and any(vv<0 for vv in cc):return -1
    raise AssertionError('Polynomial has no recorded coefficient-sign proof: '+str(pp))
def strictly_positive(vv):
    nn,dd=s.fraction(s.cancel(vv.subs(r,-2-uu)))
    assert polynomial_sign(nn)==polynomial_sign(dd)
def nowhere_zero(vv):
    nn,dd=s.fraction(s.cancel(vv.subs(r,-2-uu)))
    polynomial_sign(nn);polynomial_sign(dd)
assert data['domain']=='r < -2'
C=matrix(data['C']);S=matrix(data['S']);W=matrix(data['W']);V=matrix(data['congruence_basis_V'])
assert C.shape==(24,12) and S.shape==(12,12) and W.shape==(6,10) and V.shape==(12,12)
assert S==S.T and C[12:24,:]==s.eye(12)
for M in [C,S,W,V]:
    for vv in M:
        _,dd=s.fraction(vv);nowhere_zero(dd)
d1,d2=[rational(pp) for pp in data['diffusion']]
assert s.cancel(d1-(2*r+1)/(r-1))==0 and s.cancel(d2+3/(r-1))==0
assert s.cancel(d1+d2-2)==0
strictly_positive(d1);strictly_positive(d2)
print('Checking universal negative-branch identity...',flush=True)
x=s.Matrix(s.symbols('a b c d'));a,b,c,d=x;z=s.Matrix(s.symbols('z0:6'))
B1=s.Matrix([z[0],z[1],z[3],z[4]]);B2=s.Matrix([z[1],z[2],z[4],z[5]])
Z=s.kronecker_product(x,z);u=a*a+c*c;v=b*b+d*d;j=a*d-b*c
H=(u+v-2*j)**2
F=3*r/(8*(r+2))*H+r*(r-1)*u**2/6+j*j+r*u*j
HH=s.hessian(F,x)
heat=d1*(B1.T*HH*B1)[0]+d2*(B2.T*HH*B2)[0]
mons=s.Matrix([x[ii]*x[jj] for ii,jj in cwr(range(4),2)])
OO=s.zeros(4)
for (ii,jj),pp in zip(combinations(range(4),2),W*mons):OO[ii,jj]=pp;OO[jj,ii]=-pp
# Coefficient equality in A and compatible z; all coefficients rational in r.
left=(Z.T*C*S*C.T*Z)[0]
right=heat+(B1.T*OO*B2)[0]
poly=s.Poly(s.expand(left-right),*(list(x)+list(z)))
assert all(s.cancel(cc)==0 for cc in poly.coeffs())
closed=[s.expand(s.diff(OO[kk,ll],x[ii])-s.diff(OO[ii,ll],x[kk])+s.diff(OO[ii,kk],x[ll]))
        for ii,kk,ll in combinations(range(4),3)]
assert all(s.cancel(cc)==0 for pol0 in closed for cc in s.Poly(pol0,*x).coeffs())
primitive=OO.T*x/4
assert all(s.cancel(vv)==0 for ii,jj in combinations(range(4),2)
           for vv in s.Poly(s.expand(s.diff(primitive[jj],x[ii])-s.diff(primitive[ii],x[jj])-OO[ii,jj]),*x).coeffs())
print('Checking rational block congruence and all-branch positivity...',flush=True)
detV=s.factor(V.det());nowhere_zero(detV)
BB=(V.T*S*V).applyfunc(s.cancel)
sizes=data['block_sizes'];assert sizes==[4,4,2,2]
reconstructed=s.zeros(12);offset=0;pivots=[]
for sz,record in zip(sizes,data['block_LDL']):
    LL=matrix(record['L']);pp=[rational(vv) for vv in record['pivots']]
    assert LL.shape==(sz,sz) and len(pp)==sz
    assert all(LL[ii,jj]==0 for ii in range(sz) for jj in range(ii+1,sz))
    assert all(LL[ii,ii]==1 for ii in range(sz))
    for vv in LL:
        _,dd=s.fraction(vv);nowhere_zero(dd)
    for vv in pp:strictly_positive(vv)
    reconstructed[offset:offset+sz,offset:offset+sz]=LL*s.diag(*pp)*LL.T
    offset+=sz;pivots.extend(pp)
assert all(s.cancel(vv)==0 for vv in BB-reconstructed)
assert len(pivots)==12
alpha=s.symbols('alpha')
Fa=alpha*H+r*(r-1)*u**2/6+j*j+r*u*j
AA0=[0,(2*r+1)/3,1,0]
assert s.factor(s.diff(Fa,a,2).subs(dict(zip(x,AA0)))-16*(r+2)**2/9*(alpha-3*r/(8*(r+2))))==0
receipt={'status':'PASS','certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'sympy_version':s.__version__,'domain':'all real r < -2',
         'universal_identity':True,'closedness':True,'primitive':True,'C_rank':12,
         'rational_congruence_invertible_whole_branch':True,'block_sizes':sizes,
         'positive_rational_pivots_whole_branch':12,'pivots':[str(s.factor(vv)) for vv in pivots],
         'positivity_proof':'positive polynomial coefficients after r=-2-uu, uu>0',
         'diffusion_positive_whole_branch':True,'below_floor_acoustic_witness':True,
         'formal_proof_verification':False,'external_review':False}
(base/'UNIVERSAL_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: universal r<-2 identity, closedness, primitive, invertible congruence, 12 exact positive pivot functions.',flush=True)

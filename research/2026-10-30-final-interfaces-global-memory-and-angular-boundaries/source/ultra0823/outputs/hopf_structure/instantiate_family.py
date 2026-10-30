"""Execute the finite rational continuation operation. Requires SymPy.

With no arguments, reproduces the exact certified center. Three rational
arguments instantiate another family member; a quantitative neighborhood
test is not supplied and QC outside the proved neighborhood is not implied.
"""
from pathlib import Path
import sympy as S,json,argparse,time
start=time.perf_counter();here=Path(__file__).parent;cert=json.loads((here/'certificate.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('parameters',nargs='*');parser.add_argument('--out')
args=parser.parse_args()
if args.parameters and len(args.parameters)!=3:parser.error('Supply exactly three rational parameters a b c')
values=list(map(S.Rational,args.parameters or cert['ray']['parameters']));A0=values+[S.Integer(1)]
phi=[]
for rows in cert['normal_form']:
    phi.append(sum(S.Rational(row[3],row[4])*S.prod(x**e for x,e in zip(values,row[:3])) for row in rows))
if phi[0]==0:raise ValueError('The u=1 normalization is singular at this input')
K=[S.factor(x/phi[0]) for x in phi]
A=S.symbols('x0:4');aa,bb,cc,dd=A;T=sum(x*x for x in A);X=aa*aa+cc*cc-bb*bb-dd*dd;Y=2*(aa*bb+cc*dd);Z=2*(aa*dd-bb*cc)
u,l,p,n,q,r=K;F=u*X*X+2*l*X*Y+2*p*X*Z+n*Y*Y+2*q*Y*Z+r*Z*Z
point=dict(zip(A,A0));HF=S.hessian(F,A).subs(point);TT=sum(x*x for x in A0)**2
basis=[]
for j in range(len(cert['profile_variables'])):
    pp=[]
    for rows in cert['primitive_basis']:
        pol=0
        for row in rows:
            co=sum(S.Rational(num,den) for idx,num,den in row['weights'] if idx==j)
            pol+=co*S.prod(x**e for x,e in zip(A,row['powers']))
        pp.append(pol)
    basis.append(pp)
jet=S.zeros(3,len(basis))
for k,pp in enumerate(basis):
    for j in (1,2,3):
        om=T*(S.diff(pp[j],A[0])-S.diff(pp[0],A[j]))-2*(A[0]*pp[j]-A[j]*pp[0])
        jet[j-1,k]=om.subs(point)/2
dep=cert['dependent_indices'];free=[j for j in range(len(basis)) if j not in dep]
coeff=[S.Rational(cert['profile_coefficients'][name]) for name in cert['profile_variables']]
rhs=S.Matrix([0,-TT*HF[0,3],0])-jet[:,free]*S.Matrix([coeff[j] for j in free])
matrix=jet[:,dep]
if matrix.det()==0:raise ValueError('The selected three-jet continuation chart is singular at this input')
sol=matrix.inv()*rhs
for j,x in zip(dep,sol):coeff[j]=S.factor(x)
assert jet*S.Matrix(coeff)+S.Matrix([0,TT*HF[0,3],0])==S.zeros(3,1)
center=not args.parameters or values==list(map(S.Rational,cert['ray']['parameters']))
if center:
    assert list(map(str,K))==cert['ray']['K_coefficients']
    assert all(x==S.Rational(cert['profile_coefficients'][name]) for x,name in zip(coeff,cert['profile_variables']))
result={'parameters':list(map(str,values)),'K_coefficients':list(map(str,K)),
        'profile_coefficients':dict(zip(cert['profile_variables'],map(str,coeff))),
        'primitive_basis':cert['primitive_basis'],
        'scope':'Exact closed angular family member. QC is guaranteed in the qualitative neighborhood proved in PROOF.txt; this script does not decide membership in that neighborhood.'}
if args.out:Path(args.out).write_text(json.dumps(result)+'\n')
print(json.dumps({'center_reproduced':center,'jet_equations_exact':True,'profile_parameters':len(coeff),'seconds':time.perf_counter()-start},indent=2))

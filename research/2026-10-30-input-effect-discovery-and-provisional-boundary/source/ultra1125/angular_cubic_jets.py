"""Acquire a closed angular cubic correction, not a supplied selector."""
from pathlib import Path
import sympy as S,json,time,signal
from sympy.polys.matrices import DomainMatrix
signal.alarm(120)
root=Path(__file__).resolve().parents[1];start=time.perf_counter()
base=json.loads((root/'outputs/hopf_structure/certificate.json').read_text());gd=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text())
A=S.symbols('a b c d');x,y=S.symbols('x y');av=list(map(S.Rational,base['ray']['A0']));a,b,c,d=av
T=sum(z*z for z in A);T2=S.expand(T*T)
def deg(n,k):
    if k==1:yield(n,)
    else:
        for i in range(n+1):
            for pw in deg(n-i,k-1):yield(i,)+pw
def rotate(v):return [x*v[0]-y*v[2],x*v[1]-y*v[3],y*v[0]+x*v[2],y*v[1]+x*v[3]]
pairs=[(rotate(av),S.Matrix([x,0,0,y,0,0])),(rotate([-b,a,d,-c]),S.Matrix([0,0,x,0,0,y]))]
p1=(0,1,3,4);p2=(1,2,4,5)
def jets_heat(C):
    H=S.hessian(C,A);B=S.zeros(6)
    for mapping in (p1,p2):
        for i in range(4):
            for j in range(4):B[mapping[i],mapping[j]]+=H[i,j]*T2
    return jets(B)
def jets(B):
    col=[]
    for K,h in pairs:
        v=B.subs(dict(zip(A,K)),simultaneous=True)*h
        for ent in v:col.extend(S.Poly(S.expand(ent),x,y).coeff_monomial(x**(6-i)*y**i) for i in range(7))
    return S.Matrix(col)
cc=[];pp=[];primitive_powers=[]
for pw in gd['cubic_powers']:cc.append(jets_heat(S.prod(z**e for z,e in zip(A,pw))))
for component in range(4):
    for pw in deg(4,4):
        P=[S.S.Zero]*4;P[component]=S.prod(z**e for z,e in zip(A,pw));B=S.zeros(6)
        for i in range(4):
            for j in range(4):
                ww=(T*(S.diff(P[j],A[i])-S.diff(P[i],A[j]))-2*(A[i]*P[j]-A[j]*P[i]))/2
                B[p1[i],p2[j]]+=ww;B[p2[j],p1[i]]+=ww
        pp.append(jets(B));primitive_powers.append([component,*pw])
    print('primitive component',component,'elapsed',time.perf_counter()-start,flush=True)
CM=S.Matrix.hstack(*cc);PM=S.Matrix.hstack(*pp)
print('matrices built',time.perf_counter()-start,flush=True)
rrdm,pivots=DomainMatrix.from_Matrix(PM.row_join(CM)).rref(method='GJ');rr=rrdm.to_Matrix()
rankp=sum(i<PM.cols for i in pivots);rankall=len(pivots);obrank=rankall-rankp
print('ranks',rankp,rankall,obrank,'elapsed',time.perf_counter()-start,flush=True)
basis=S.Matrix.hstack(*(S.Matrix(list(map(S.Rational,v))) for v in gd['cubic_kernel_basis']))
target=-CM*basis;rhs=-rr[:,PM.cols:]*basis
assert rhs[rankp:,:]==S.zeros(PM.rows-rankp,12)
selection=S.zeros(PM.cols,12)
for row,pivot in enumerate(pivots[:rankp]):
    for j in range(12):selection[pivot,j]=rhs[row,j]
assert PM*selection==target
result={'primitive_jet_rank':rankp,'joint_rank':rankall,'cubic_obstruction_rank':obrank,'compatible_cubic_dimension':20-obrank,
        'primitive_powers':primitive_powers,'selection':[[str(z) for z in row] for row in selection.tolist()],
        'seconds':time.perf_counter()-start,'scope':'Exact linear closed angular correction for the full asymptotic acoustic column; global positivity not acquired.'}
(root/'work/angular_cubic_jets.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('selection','primitive_powers')},indent=2))

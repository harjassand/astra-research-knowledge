"""Test whether a polynomial cubic correction attains the full acoustic jet."""
from pathlib import Path
import sympy as S,json,time
root=Path(__file__).resolve().parents[1];start=time.perf_counter()
base=json.loads((root/'outputs/hopf_structure/certificate.json').read_text());gd=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text())
A=S.symbols('a b c d');x,y=S.symbols('x y');av=list(map(S.Rational,base['ray']['A0']));a,b,c,d=av
def deg(n,k):
    if k==1:yield(n,)
    else:
        for i in range(n+1):
            for pw in deg(n-i,k-1):yield(i,)+pw
def rotate(v):return [x*v[0]-y*v[2],x*v[1]-y*v[3],y*v[0]+x*v[2],y*v[1]+x*v[3]]
pairs=[(rotate(av),S.Matrix([x,0,0,y,0,0])),(rotate([-b,a,d,-c]),S.Matrix([0,0,x,0,0,y]))]
p1=(0,1,3,4);p2=(1,2,4,5)
def density(C,P):
    H=S.hessian(S.sympify(C),A);B=S.zeros(6)
    for mapping in (p1,p2):
        for i in range(4):
            for j in range(4):B[mapping[i],mapping[j]]+=H[i,j]
    for i in range(4):
        for j in range(4):
            ww=(S.diff(P[j],A[i])-S.diff(P[i],A[j]))/2
            B[p1[i],p2[j]]+=ww;B[p2[j],p1[i]]+=ww
    return B
def jets(B):
    col=[]
    for K,h in pairs:
        v=B.subs(dict(zip(A,K)),simultaneous=True)*h
        for ent in v:col.extend(S.Poly(S.expand(ent),x,y).coeff_monomial(x**(2-i)*y**i) for i in range(3))
    return S.Matrix(col)
cc=[];pp=[]
for pw in gd['cubic_powers']:cc.append(jets(density(S.prod(z**e for z,e in zip(A,pw)),[S.S.Zero]*4)))
for component in range(4):
    for pw in deg(2,4):
        P=[S.S.Zero]*4;P[component]=S.prod(z**e for z,e in zip(A,pw));pp.append(jets(density(0,P)))
CM=S.Matrix.hstack(*cc);PM=S.Matrix.hstack(*pp);rankp=PM.rank();rankall=PM.row_join(CM).rank()
left=PM.T.nullspace();obstruction=S.Matrix.vstack(*(v.T*CM for v in left));obrank=obstruction.rank()
result={'primitive_jet_rank':rankp,'joint_rank':rankall,'cubic_obstruction_rank':obrank,'compatible_cubic_dimension':20-obrank,
        'seconds':time.perf_counter()-start,'scope':'Full-column polynomial cubic heat jets only, not a positivity or QC obstruction.'}
(root/'work/cubic_closed_jets.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

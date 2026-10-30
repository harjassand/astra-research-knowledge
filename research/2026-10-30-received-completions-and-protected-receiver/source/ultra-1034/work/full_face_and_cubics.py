"""Exact full-polynomial acoustic constraints at the generic Hopf ray."""
from pathlib import Path
import sympy as S,json,time,signal
signal.alarm(180);start=time.perf_counter();here=Path(__file__).parent
cert=json.loads((here.parent/'outputs/hopf_structure/certificate.json').read_text())
A=S.symbols('a b c d',real=True);x,y=S.symbols('x y',real=True)
def degrees(total,n):
    if n==1:yield(total,)
    else:
        for j in range(total+1):
            for pw in degrees(total-j,n-1):yield(j,)+pw
av=list(map(S.Rational,cert['ray']['A0']));a,b,c,d=av
A2=[-b,a,d,-c]
def rotate(v):return S.Matrix([x*v[0]-y*v[2],x*v[1]-y*v[3],y*v[0]+x*v[2],y*v[1]+x*v[3]])
pairs=[(S.Matrix([x,0,y,0]),S.Matrix([0,x,0,y]),rotate(av)),
       (S.Matrix([0,x,0,y]),S.Matrix([x,0,y,0]),rotate(A2))]
def clean_rows(rows):
    out=[]
    for row in rows:
        den=S.ilcm(*(v.q for v in row));ints=[int(v*den) for v in row];gg=S.igcd(*ints)
        out.append([v//gg if gg else v for v in ints])
    return out
quartic=list(degrees(4,4));cubic=list(degrees(3,4));Qcols=[];Ccols=[]
for pw in quartic:
    G=S.prod(z**e for z,e in zip(A,pw));H=S.hessian(G,A);col=[]
    for R,Rp,K in pairs:
        vec=H.subs(dict(zip(A,R)),simultaneous=True)*K
        for ex in vec:col.extend(S.Poly(S.expand(ex),x,y).coeff_monomial(x**(3-i)*y**i) for i in range(4))
        deriv=2*(R.T*H.subs(dict(zip(A,K)),simultaneous=True)*Rp)[0]
        col.extend(S.Poly(S.expand(deriv),x,y).coeff_monomial(x**(4-i)*y**i) for i in range(5))
    Qcols.append(col)
for pw in cubic:
    G=S.prod(z**e for z,e in zip(A,pw));grad=S.Matrix([S.diff(G,z) for z in A]);col=[]
    for R,_,K in pairs:
        score=(grad.subs(dict(zip(A,R)),simultaneous=True).T*K)[0]
        col.extend(S.Poly(S.expand(score),x,y).coeff_monomial(x**(3-i)*y**i) for i in range(4))
    Ccols.append(col)
QM=S.Matrix.hstack(*map(S.Matrix,Qcols));CM=S.Matrix.hstack(*map(S.Matrix,Ccols))
qr=QM.rank();cr=CM.rank()
print('full quartic face constraint rank',qr,'kernel',35-qr,'cubic rank',cr,'kernel',20-cr,'seconds',time.perf_counter()-start,flush=True)
kernel=CM.nullspace();simple=[]
for v in kernel:
    den=S.ilcm(*(z.q for z in v));iv=[int(z*den) for z in v];gg=S.igcd(*iv);iv=[z//gg for z in iv]
    poly=sum(z*S.prod(q**e for q,e in zip(A,pw)) for z,pw in zip(iv,cubic));simple.append(str(poly))
result={'quartic_powers':quartic,'cubic_powers':cubic,'quartic_matrix':clean_rows(QM.tolist()),'cubic_matrix':clean_rows(CM.tolist()),
        'quartic_rank':qr,'quartic_kernel_dimension':35-qr,'cubic_rank':cr,'cubic_kernel_dimension':20-cr,
        'cubic_kernel_basis':simple,'seconds':time.perf_counter()-start,
        'scope':'Exact necessary acoustic constraints. No stabilization, full-space extremality, or QC conclusion follows from the ranks alone.'}
(here/'full_face_and_cubics.json').write_text(json.dumps(result,indent=2)+'\n')
print('cubic basis acquired',len(simple),flush=True)

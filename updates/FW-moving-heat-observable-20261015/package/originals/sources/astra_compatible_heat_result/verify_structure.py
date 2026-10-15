#!/usr/bin/env python3
"""Exact fixed-face and local-null-form calculations. Requires SymPy.
Independent of discovery pickle files; reads the portable certificate only.
"""
import json
from pathlib import Path
from itertools import combinations, combinations_with_replacement, permutations
import sympy as s
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
root=Path(__file__).parent
q=json.loads((root/'MOVING_ACOUSTIC_CERTIFICATE.json').read_text())
R=s.Rational;r0=-R(5,2)
def base_matrix(name,denom):
    blocks=[s.Matrix([[R(v) for v in row] for row in block]) for block in q[name]]
    return sum((r0**k*B for k,B in enumerate(blocks)),s.zeros(*blocks[0].shape))/denom
C=base_matrix('C_numerator',r0+1)
x=s.Matrix(s.symbols('a b c d'));a,b,c,d=x
z=s.Matrix(s.symbols('z0:6'));Z=s.kronecker_product(x,z)
B1=s.Matrix([z[0],z[1],z[3],z[4]]);B2=s.Matrix([z[1],z[2],z[4],z[5]])
D1,D2=map(R,q['diffusion']);xb=list(combinations_with_replacement(range(4),2));zb=list(combinations_with_replacement(range(6),2));pairs=list(combinations(range(4),2));allvars=list(x)+list(z)
exps=[]
for i,j in xb:
    for k,l in zb:
        e=[0]*10;e[i]+=1;e[j]+=1;e[4+k]+=1;e[4+l]+=1;exps.append(tuple(e))
ix={e:k for k,e in enumerate(exps)}
def pcol(p):
    col=s.zeros(226,1)
    for exp,val in s.Poly(s.expand(p),*allvars).terms():col[ix[exp]]=val
    return col
ell=C.T*Z
GM=s.Matrix.hstack(*[pcol((1 if i==j else 2)*ell[i]*ell[j]) for i,j in combinations_with_replacement(range(18),2)])
wc=[]
for i,j in pairs:
    for k,l in xb:
        O=s.zeros(4);O[i,j]=x[k]*x[l];O[j,i]=-x[k]*x[l]
        co=pcol((B1.T*O*B2)[0]);offset=210
        for aa,bb,cc in combinations(range(4),3):
            eq=s.diff(O[bb,cc],x[aa])-s.diff(O[aa,cc],x[bb])+s.diff(O[aa,bb],x[cc])
            for xx in x:co[offset]=s.diff(eq,xx);offset+=1
        wc.append(co)
WM=s.Matrix.hstack(*wc)
u=a*a+c*c;v=b*b+d*d;j=a*d-b*c;w=a*b+c*d
fb=[u*u,v*v,u*v,w*w,u*w,v*w,u*j,v*j,w*j]
def heat(F):
    H=s.hessian(F,x)
    return D1*(B1.T*H*B1)[0]+D2*(B2.T*H*B2)[0]
FM=s.Matrix.hstack(*[pcol(heat(F)) for F in fb]);M=GM.row_join(-WM)
rr,piv=DomainMatrix.from_Matrix(M.row_join(-FM)).convert_to(QQ).rref();rr=rr.to_Matrix()
assert sum(k<231 for k in piv)==183 and len(piv)==190
constraints=s.Matrix.vstack(*[rr[i,231:] for i in range(rr.rows) if all(vv==0 for vv in rr[i,:231]) and any(vv!=0 for vv in rr[i,231:])])
expected=s.zeros(7,9)
expected[0,0]=1;expected[0,6]=R(7,12);expected[0,7]=-R(1,3)
expected[1,1]=1;expected[1,7]=R(1,4)
expected[2,2]=1;expected[2,6]=R(2,5);expected[2,7]=R(11,10)
expected[3,3]=1;expected[3,6]=-R(2,5);expected[3,7]=-R(3,5)
expected[4,4]=1;expected[5,5]=1;expected[6,8]=1
assert constraints.rref()[0]==expected.rref()[0]
print('PASS: fixed support permits exactly span{G,H}',flush=True)
# Symbol kernel for constant-coefficient Hessian null forms.
p,qq,xi,eta=s.symbols('p q xi eta')
zrank=s.Matrix([p*xi**2,p*xi*eta,p*eta**2,qq*xi**2,qq*xi*eta,qq*eta**2])
symbols=[s.expand(zrank[k]*zrank[l]) for k,l in zb]
mons=sorted(set(e for pol in symbols for e,_ in s.Poly(pol,p,qq,xi,eta).terms()))
SM=s.Matrix([[s.Poly(pol,p,qq,xi,eta).coeff_monomial(e) for pol in symbols] for e in mons])
assert SM.shape==(15,21) and SM.rank()==15
minors=[s.expand(B1[i]*B2[k]-B1[k]*B2[i]) for i,k in pairs]
MC=s.Matrix([[s.Poly(pol,*z).coeff_monomial(z[i]*z[j]) for pol in minors] for i,j in zb])
assert MC.rank()==6 and SM*MC==s.zeros(15,6)
# Closedness forced by arbitrary third jets in the Euler equation.
Ts=s.symbols('T012 T013 T023 T123');TD={}
for tr,tt in zip(combinations(range(4),3),Ts):
    for prm in permutations(tr):TD[prm]=(-1)**sum(prm[i]>prm[j] for i in range(3) for j in range(i+1,3))*tt
Tv=[s.expand(sum(TD.get((i,k,l),0)*B1[k]*B2[l] for k in range(4) for l in range(4))) for i in range(4)]
y=s.symbols('y0:8');zx=[y[0],y[1],y[2],y[4],y[5],y[6]];zy=[y[1],y[2],y[3],y[5],y[6],y[7]]
E=s.expand(sum(s.diff(Tv[0],z[i])*zx[i]+s.diff(Tv[1],z[i])*zy[i] for i in range(6)))
EP=s.Poly(E,*list(z),*y)
assert EP.coeff_monomial(z[0]*y[6])==-Ts[0]
assert EP.coeff_monomial(z[0]*y[7])==-Ts[1]
assert EP.coeff_monomial(z[3]*y[6])==Ts[2]
assert EP.coeff_monomial(z[3]*y[7])==Ts[3]
# Common acoustic-contact face has dimension four.
f=s.symbols('f0:9');F=sum(f[i]*fb[i] for i in range(9));n,m=s.symbols('n m');Rdir=s.Matrix([n,m,0,0]);h=(Rdir.T*s.hessian(F,x)*Rdir)[0]
point={a:1,b:0,c:0,d:1,n:0,m:1}
contacteq=[s.diff(h,xx).subs(point) for xx in list(x)+[n,m]]
EC,_=s.linear_eq_to_matrix(contacteq,f)
assert EC.rank()==5
# Six geometrically forced acoustic null vectors span the full moving kernel.
r,t=s.symbols('r t')
blocks=[s.Matrix([[R(vv) for vv in row] for row in block]) for block in q['C_numerator']]
Cr=sum((r**k*B for k,B in enumerate(blocks)),s.zeros(24,18))/(r+1)
columns=[]
for co,si in [(1,0),(0,1),(1/s.sqrt(2),1/s.sqrt(2))]:
    rot=s.Matrix([[co,-si],[si,co]])
    AA=rot*s.Matrix([[1,-(r+1)*t],[(r+1)*t,1]])
    zz=s.Matrix([co*t*t,co*t,co,si*t*t,si*t,si])
    Zt=s.kronecker_product(s.Matrix(list(AA)),zz)
    for k in [0,1]:
        col=Zt.diff(t,k).subs(t,0).applyfunc(s.expand)
        assert (Cr.T*col).applyfunc(s.simplify)==s.zeros(18,1)
        columns.append(col)
KM=s.Matrix.hstack(*columns)
assert s.simplify(KM[[1,2,4,5,8,11],:].det()+(r+1)/4)==0
pivotrows=[0,3,6,7,9,10,12,13,14,15,16,17,18,19,20,21,22,23]
assert (Cr[pivotrows,:]-s.eye(18)).applyfunc(s.cancel)==s.zeros(18)

# Exact failure of the particular continuation at r=-8/3.
fail=json.loads((root/'FAILED_CONTINUATION_WITNESS.json').read_text());rv=R(fail['parameter'])
blocks=[s.Matrix([[R(vv) for vv in row] for row in block]) for block in q['S_numerator']]
Sr=sum((rv**k*B for k,B in enumerate(blocks)),s.zeros(18))/(-(rv+1))
ww=s.Matrix([R(vv) for vv in fail['witness_vector']]);nv=R(fail['negative_quadratic_value'])
assert (ww.T*Sr*ww)[0]==nv<0
receipt={'status':'EXACT_PASS','fixed_face_identity_matrix_rank':183,'fixed_face_augmented_rank':190,'fixed_face_quartic_dimension':2,'fixed_face_constraints':[[str(vv) for vv in row] for row in expected.tolist()],'symbol_map_dimensions':[15,21],'symbol_map_rank':15,'null_symbol_dimension':6,'closedness_third_jet_test':True,'acoustic_contact_face_dimension':4,'moving_forced_kernel_dimension':6,'moving_kernel_minor':'-(r+1)/4','particular_continuation_failure_verified':True,'scope':'Exact finite identities support, but do not replace, the analytic arguments in RESEARCH_REPORT.md.'}
(root/'STRUCTURAL_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: local null-form dimensions, closedness test, contact face, and scoped failed continuation')

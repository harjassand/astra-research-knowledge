#!/usr/bin/env python3
"""Fresh exact tensor heat acquisition at the lambda=4 C4 boundary.

Reads no source numerical or pickle data. A success requires a universal
polynomial identity and exact positivity over the isolated number field.
"""
from pathlib import Path
import json
import itertools
import numpy as np
import sympy as s
from general_c4 import build

OUT=Path(__file__).parent
z=build();A,C,E,L=z['parameters'];x=z['coordinates'];h=z['jets'];q=z['q']
m=L**4-48*L**2+384;j=s.Symbol('j')
gb=s.groebner([m,j*j+(s.Rational(3,8)*L*L-8)*j+1],j,L,order='lex',domain=s.QQ)
def red(f):return gb.reduce(s.expand(f))[1]
def redL(f):return s.rem(s.Poly(s.expand(f),L,domain=s.QQ),s.Poly(m,L)).as_expr()
v=L*L
AA=s.Matrix([[12+8*j,16*j,-2*j],[16,8+12*j,-1-3*j],[-2*v,-v*(1+3*j),4+8*j]])
nums=AA.adjugate()*s.Matrix([-3-j,-2,0]);rho,si,chi=nums.applyfunc(red);D=red(AA.det())
ap=L*rho;bp=L*si;cp=chi;dp=D
vp=s.Matrix([ap,j*ap,j*bp,-j*cp,-dp,-j*dp]).applyfunc(red)
vm=s.Matrix([j*bp,bp,ap,dp,j*cp,cp]).applyfunc(red)
Up=s.Matrix([ap-j*dp,j*ap-dp,j*(bp-cp)]).applyfunc(red)
Ui=s.Matrix([cp+j*bp,j*cp+bp,dp+ap]).applyfunc(red)
Vp=s.Matrix([ap+j*dp,j*ap+dp,j*(bp+cp)]).applyfunc(red)
Vi=s.Matrix([cp-j*bp,j*cp-bp,dp-ap]).applyfunc(red)

def constant_null(vectors,n):
    cols=[]
    for i in range(n):
        for d in range(4):
            values=[]
            for vv in vectors:
                pp=s.Poly(red(vv[i]*L**d),j,L,domain=s.QQ)
                values.extend(pp.coeff_monomial(j**e*L**f) for e in range(2) for f in range(4))
            cols.append(s.Matrix(values))
    null=s.Matrix.hstack(*cols).nullspace()
    return [s.Matrix([sum(nn[4*i+d]*L**d for d in range(4)) for i in range(n)]) for nn in null]

kn=3.18490086807250
def choose(vectors,n):
    ans=[];ev=np.empty((n,0))
    for vv in vectors:
        numeric=np.array(vv.subs(L,kn),float).ravel()
        if np.linalg.matrix_rank(np.column_stack([ev,numeric]),tol=1e-8)>len(ans):
            # Fixed rational normalization affects only acquisition coordinates.
            scale=max(1,round(float(np.linalg.norm(numeric))))
            vv=vv/scale;numeric=numeric/scale
            ans.append(vv);ev=np.column_stack([ev,numeric])
    return ans

scalar_vectors=choose(constant_null([vp,vm],6),6)
uvec=choose(constant_null([Up,Ui],3),3)
vvec=choose(constant_null([Vp,Vi],3),3)
assert len(scalar_vectors)==4 and len(uvec)==len(vvec)==1
VV=s.Matrix.hstack(*scalar_vectors);uu=uvec[0];vv=vvec[0]
print('field frames acquired',VV.shape,uu.T,vv.T,flush=True)

# Exact full closed homogeneous-quadratic two-form interface.
xpairs=list(itertools.combinations_with_replacement(range(4),2))
hpairs=list(itertools.combinations_with_replacement(range(6),2))
fpairs=list(itertools.combinations(range(4),2))
mon=[x[i]*x[j]*h[k]*h[l] for i,j in xpairs for k,l in hpairs]
exps=[s.Poly(mm,*(tuple(x)+h)).monoms()[0] for mm in mon];lookup={e:i for i,e in enumerate(exps)}
def coeff(poly):
    ans=s.zeros(210,1)
    for exp,c in s.Poly(s.expand(poly),*(tuple(x)+h)).terms():ans[lookup[exp]]=redL(c)
    return ans
omega=s.symbols('w0:60');xmon=[x[i]*x[j] for i,j in xpairs]
forms={ij:sum(omega[10*n+k]*mm for k,mm in enumerate(xmon)) for n,ij in enumerate(fpairs)}
def om(i,j):return forms[(i,j)] if i<j else -forms[(j,i)]
ceq=[]
for i,j,k in itertools.combinations(range(4),3):
    df=s.diff(om(j,k),x[i])-s.diff(om(i,k),x[j])+s.diff(om(i,j),x[k])
    ceq.extend(s.expand(df).coeff(xx) for xx in x)
Cl,_=s.linear_eq_to_matrix(ceq,omega)
NN=s.Matrix.hstack(*Cl.nullspace())
OO=s.Matrix.hstack(*[coeff(mm*(z['B1'][i]*z['B2'][j]-z['B1'][j]*z['B2'][i])) for i,j in fpairs for mm in xmon])
ON=OO*NN
DD=s.Matrix.hstack(*ON.T.nullspace()).T

zp=VV.T*z['zplus'];zm=VV.T*z['zminus']
tij=list(itertools.combinations_with_replacement(range(4),2))
polys=[(zp[i]*zp[j]+zm[i]*zm[j])*(1 if i==j else 2) for i,j in tij]
# Complex spin-two bilinear channels, with explicit real coefficients.
a,b,c,d=x;X=h[0]+s.I*h[3];Y=h[1]+s.I*h[4];Z=h[2]+s.I*h[5]
xx=a+s.I*c;yy=b+s.I*d
bu=s.Matrix([xx*X+s.I*yy*Z,xx*Z+s.I*yy*X,yy*Y+s.I*xx*Y])
bv=s.Matrix([xx*X-s.I*yy*Z,xx*Z-s.I*yy*X,yy*Y-s.I*xx*Y])
fu=s.expand((uu.T*bu)[0]);fv=s.expand((vv.T*bv)[0])
pu=s.re(fu).expand()**2+s.im(fu).expand()**2
pv=s.re(fv).expand()**2+s.im(fv).expand()**2
targetF=sum(pp*ff for pp,ff in zip([1,4,0,L],z['basis']))
HF=s.hessian(targetF,x)
Ef=coeff((z['B1'].T*HF*z['B1']+z['B2'].T*HF*z['B2'])[0])
target=(DD*Ef).applyfunc(redL)
columns=[(DD*coeff(p)).applyfunc(redL) for p in polys+[pu,pv]]
def expandK(vec):
    return s.Matrix([s.Poly(c,L).nth(d) for c in vec for d in range(4)])
rhs=expandK(target)
mat=s.Matrix.hstack(*[expandK((L**d*col).applyfunc(redL)) for col in columns for d in range(4)])
rr,piv=mat.row_join(rhs).rref()
assert all(i<mat.cols for i in piv)
free=[i for i in range(mat.cols) if i not in piv]
print('exact tensor affine shape',mat.shape,'rank',len(piv),'free',free,flush=True)
np.savez(OUT/'tensor_field_linear.npz',matrix=np.array(mat,float),rhs=np.array(rhs,float))

# Choose the two tensor coefficients as rational constants, keeping other
# free field coefficients zero. Values are acquisition choices only.
accepted=None
for alpha in [0,s.Rational(1,4),s.Rational(1,2),1,2,4,8,16]:
    for beta in [0,s.Rational(1,4),s.Rational(1,2),1,2,4,8,16]:
        sol=s.zeros(mat.cols,1)
        for idx,val in [(40,alpha),(44,beta)]:
            if idx in free:sol[idx]=val
        for i,k in enumerate(piv):sol[k]=rr[i,-1]-sum(rr[i,f]*sol[f] for f in free)
        weights=[sum(sol[4*i+d]*L**d for d in range(4)) for i in range(12)]
        TT=s.zeros(4)
        for (i,j),val in zip(tij,weights):TT[i,j]=TT[j,i]=val
        eig=np.linalg.eigvalsh(np.array(TT.subs(L,kn),float))
        if eig[0]>1e-5 and float(weights[10].subs(L,kn))>=0 and float(weights[11].subs(L,kn))>=0:
            accepted=(sol,weights,TT,eig);break
    if accepted:break
assert accepted is not None,'Bounded rational tensor-weight choices did not acquire positivity.'
sol,weights,TT,eig=accepted
assert mat*sol==rhs
lo=s.Rational(318490086807,10**11);hi=s.Rational(318490086808,10**11)
assert s.Poly(m,L).count_roots(lo,hi)==1
def interval(poly):
    l=u=s.Rational(0)
    for c in s.Poly(poly,L).all_coeffs():
        cand=[l*lo,l*hi,u*lo,u*hi];l=min(cand)+c;u=max(cand)+c
    return l,u
minors=[redL(TT[:i,:i].det()) for i in range(1,5)]
bounds=[interval(v) for v in minors]
assert all(l>0 for l,u in bounds)
assert interval(weights[10])[0]>=0 and interval(weights[11])[0]>=0
poly=sum(w*p for w,p in zip(weights,polys+[pu,pv]))
diff=(coeff(poly)-Ef).applyfunc(redL)
omegak=ON.gauss_jordan_solve(diff)[0].applyfunc(redL)
omegaf=(NN*omegak).applyfunc(redL)
assert (OO*omegaf-diff).applyfunc(redL)==s.zeros(210,1)
assert Cl*omegaf==s.zeros(16,1)
print('EXACT_PASS tensor weights',weights[10:], 'T eigen orientation only',eig,'minor intervals',[[float(a),float(b)] for a,b in bounds],flush=True)
out={'status':'EXACT_PASS','scope':'lambda=4 endpoint tensor certificate; no full cone inclusion',
     'root_polynomial':str(m),'root_interval':[str(lo),str(hi)],
     'scalar_frame':[[str(v) for v in row] for row in VV.tolist()],
     'u':list(map(str,uu)),'v':list(map(str,vv)),
     'T':[[str(v) for v in row] for row in TT.tolist()],
     'tensor_weights':list(map(str,weights[10:])),
     'omega':[[str(v) for v in omegaf[10*i:10*i+10,0]] for i in range(6)],
     'T_minor_bounds':[[str(a),str(b)] for a,b in bounds]}
(OUT/'C4_LAMBDA4_TENSOR_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')

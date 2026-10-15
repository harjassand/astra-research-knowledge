"""Full coupled G search using elliptic complex diffusion and closed 2-forms.

Exploration only. Search arithmetic is floating point; a successful search
requires a separate rational certificate and analytic proof. No sampled map
or phase energy is used. Exact acoustic-null facial reduction is imposed.
"""
from pathlib import Path
import json,time,sys
import numpy as np
import sympy as S

ROOT=Path(__file__).resolve().parent
x=S.symbols('a b c d');z=S.symbols('z0:6')
a,b,c,d=x
u=a*a+c*c;v=b*b+d*d;j=a*d-b*c
F=3*(u+v-2*j)**2+S.Rational(35,24)*u*u+j*j-S.Rational(5,2)*j*u
J1=S.Matrix([z[0],z[1],z[3],z[4]])
J2=S.Matrix([z[1],z[2],z[4],z[5]])
target_J=S.Matrix([[0,0,-1,0],[0,0,0,-1],[1,0,0,0],[0,1,0,0]])
H=S.hessian(F,x)
heat=[S.expand((J1.T*H*J1)[0]),S.expand((J1.T*H*J2)[0]),S.expand((J2.T*H*J2)[0])]
complex_xx=S.expand((J1.T*H*target_J*J1)[0])

xpairs=[(i,k) for i in range(4) for k in range(i,4)]
zpairs=[(i,k) for i in range(6) for k in range(i,6)]
formpairs=[(i,k) for i in range(4) for k in range(i+1,4)]
xmon=[x[i]*x[k] for i,k in xpairs]
zmon=[z[i]*z[k] for i,k in zpairs]
mon=[xx*zz for xx in xmon for zz in zmon]
exp=[S.Poly(m,*(x+z)).monoms()[0] for m in mon]
lookup={e:i for i,e in enumerate(exp)}


def coeff(poly):
    out=S.zeros(210,1)
    for powers,value in S.Poly(S.expand(poly),*(x+z)).terms():
        out[lookup[powers]]=value
    return out


# All closed homogeneous-quadratic two-forms, not merely an invariant ansatz.
w=S.symbols('w0:60')
forms={ij:sum(w[10*n+k]*m for k,m in enumerate(xmon)) for n,ij in enumerate(formpairs)}
def form(i,k):
    return forms[(i,k)] if i<k else -forms[(k,i)]
closed=[]
for i in range(4):
    for k in range(i+1,4):
        for ell in range(k+1,4):
            poly=S.diff(form(k,ell),x[i])-S.diff(form(i,ell),x[k])+S.diff(form(i,k),x[ell])
            closed.extend(S.expand(poly).coeff(xx) for xx in x)
C,_=S.linear_eq_to_matrix(closed,w)
assert C.rank()==15
N=S.Matrix.hstack(*C.nullspace())
assert N.shape==(60,45)
O=S.Matrix.hstack(*[coeff(m*(J1[i]*J2[k]-J1[k]*J2[i])) for i,k in formpairs for m in xmon])
ON=np.array(O*N,dtype=float)
U,sig,_=np.linalg.svd(ON,full_matrices=True)
assert np.sum(sig>1e-9)==45
annihilator=U[:,45:].T

# Exact three-dimensional null span of every PSD Gram certificate, from the
# conformal acoustic-zero orbit. Coefficient ordering is x_i*z_j.
null=S.zeros(24,3)
null[2,0]=1;null[20,0]=1
null[11,1]=-1;null[17,1]=1
null[5,2]=1;null[8,2]=-1;null[14,2]=1;null[23,2]=1
face_tag=''
if len(sys.argv)>2:
    face_path=ROOT/sys.argv[2]
    face_data=json.loads(face_path.read_text())
    extra=S.Matrix([[S.Rational(v) for v in row] for row in face_data['extra_null_columns']])
    null=null.row_join(extra)
    face_tag='_'+face_path.stem
Brat=S.Matrix.hstack(*null.T.nullspace())
assert Brat.rows==24 and null.T*Brat==S.zeros(null.cols,Brat.cols)
Borth,_=np.linalg.qr(np.array(Brat,dtype=float))

bmon=S.Matrix([xx*zz for xx in x for zz in z])
Pfull=np.column_stack([np.array(coeff(bmon[i]*bmon[k]),float).ravel()
                     for i in range(24) for k in range(24)])
n=Brat.cols
ij=np.triu_indices(n)
weight=np.where(ij[0]==ij[1],1.,np.sqrt(2.))


def matrix(vec):
    M=np.zeros((n,n));M[ij]=vec/weight;M[(ij[1],ij[0])]=vec/weight
    return M


def vech(M):
    return M[ij]*weight


reduced_columns=[]
for i,k in zip(*ij):
    outer=np.outer(Borth[:,i],Borth[:,k])
    if i!=k:
        outer=(outer+outer.T)/np.sqrt(2.)
    reduced_columns.append(Pfull@outer.ravel())
P=np.column_stack(reduced_columns)
HD=np.column_stack([np.array(coeff(heat[0]),float).ravel(),
                    np.sqrt(2.)*np.array(coeff(heat[1]),float).ravel(),
                    np.array(coeff(heat[2]),float).ravel()])
HE=np.array(coeff(complex_xx),float).ravel()
gramlen=len(ij[0])
T=np.column_stack([annihilator@P,-annihilator@HD,-annihilator@HE])
trace=np.zeros(T.shape[1]);trace[gramlen]=1;trace[gramlen+2]=1
T=np.vstack([T,trace]);rhs=np.r_[np.zeros(165),2.]
inverse=np.linalg.pinv(T,rcond=1e-11)
anchor=inverse@rhs
projector=np.eye(T.shape[1])-inverse@T
assert np.linalg.norm(T@anchor-rhs)<1e-8


def diffusion(vec):
    return np.array([[vec[0],vec[1]/np.sqrt(2.)],[vec[1]/np.sqrt(2.),vec[2]]])


def diffusion_vech(M):
    return np.array([M[0,0],np.sqrt(2.)*M[0,1],M[1,1]])


gram_margin=float(sys.argv[1]) if len(sys.argv)>1 else 0.
suffix=face_tag+('' if gram_margin==0 else '_margin_'+str(gram_margin))


def cone_projection(vec,margin):
    lam,V=np.linalg.eigh(matrix(vec[:gramlen]))
    gram=vech((V*np.maximum(lam,gram_margin))@V.T)
    Dlam,DV=np.linalg.eigh(diffusion(vec[gramlen:gramlen+3]))
    D=diffusion_vech((DV*np.maximum(Dlam,margin))@DV.T)
    return np.r_[gram,D,vec[-1]]


margin=.01
steps=8000
y=anchor.copy();dual=np.zeros_like(y)
tick=time.monotonic()
for step in range(steps+1):
    xx=anchor+projector@(y-dual)
    yy=cone_projection(xx+dual,margin)
    dual+=xx-yy
    residual=np.linalg.norm(xx-yy);change=np.linalg.norm(yy-y);y=yy
    if step%1000==0:
        print('step',step,'residual',residual,'change',change,'E_xx',xx[-1],flush=True)
    if residual<1e-10 and change<1e-10:
        break
R=Borth@matrix(xx[:gramlen])@Borth.T
D=diffusion(xx[gramlen:gramlen+3])
e=xx[-1]
form_rhs=P@xx[:gramlen]-HD@xx[gramlen:gramlen+3]-HE*e
form_parameters=np.linalg.lstsq(ON,form_rhs,rcond=1e-11)[0]
form_coeff=np.array(N,float)@form_parameters
rec={'status':'NUMERICAL_ONLY','iterations':step,'seconds':time.monotonic()-tick,
     'gram_margin_requested':gram_margin,
     'primal_residual':float(residual),'iterate_change':float(change),
     'affine_residual':float(np.linalg.norm(T@xx-rhs)),
     'min_reduced_gram_eigenvalue':float(np.linalg.eigvalsh(matrix(xx[:gramlen]))[0]),
     'diffusion':D.tolist(),'diffusion_eigenvalues':np.linalg.eigvalsh(D).tolist(),
     'complex_xx_coefficient':float(e),'closed_form_reconstruction_residual':float(np.linalg.norm(ON@form_parameters-form_rhs)),
     'scope':'full closed quadratic two-form and bilinear SOS, elliptic complex diffusion; no QC conclusion'}
np.savez(ROOT/('complex_diffusion_candidate'+suffix+'.npz'),gram=R,reduced_gram=matrix(xx[:gramlen]),
        diffusion=D,complex_xx=e,closed_form_coeff=form_coeff,affine_dual=dual,
        T=T,rhs=rhs,annihilator=annihilator,closed_basis=np.array(N,float),
        Pfull=Pfull,heat_coeff=HD,complex_coeff=HE,null_span=np.array(null,float),
        rational_quotient_basis=np.array(Brat,float))
(ROOT/('complex_diffusion_search'+suffix+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2),flush=True)

"""Attempt an exact global polynomial heat SOS at a larger admitted quadratic.
Build bilinear syzygies of the entire leading acoustic null variety first.
"""
import sys
import sympy as S
import numpy as np
from pathlib import Path
x,y,u,v=S.symbols('x y u v',real=True);ZZ=S.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C=x*(u*u-v*v)-2*y*u*v;lam=S.Rational(sys.argv[1]) if len(sys.argv)>1 else S.Rational(1,1);P0=F+C+lam*(r+t)
h=S.Matrix(S.symbols('h0:6',real=True));Jx=S.Matrix([h[0]+h[4],h[3]-h[1],h[0]-h[4],h[3]+h[1]]).jacobian(h);Jy=S.Matrix([h[1]+h[5],h[4]-h[2],h[1]-h[5],h[4]+h[2]]).jacobian(h)
def correction(P):
 W=P.jacobian(ZZ).T-P.jacobian(ZZ);temp=Jx.T*W*Jy;return S.expand((temp+temp.T)/2)
H=S.hessian(P0,ZZ);Bbase=S.expand(Jx.T*H*Jx+Jy.T*H*Jy)
q1,q3,f,g,j,k=S.symbols('q1 q3 f g j k');az=S.Matrix([-y,x,0,0]);aw=S.Matrix([0,0,-v,u]);PF=(q1/8+S.Rational(3,2))*r*az+q1*t*az+(6-q3)*r*aw+q3*t*aw
PC=f*S.Matrix([0,0,x*u-y*v,-x*v-y*u])+g*S.Matrix([0,0,x*v+y*u,x*u-y*v]);PQ=j*az/2+k*aw/2;B=S.expand(Bbase+correction(PF+PC+PQ));params=[q1,q3,f,g,j,k]
Bconst=B.subs({p:0 for p in params});Bcoeff=[S.diff(B,p) for p in params]
# All bilinear syzygies of the actual leading acoustic nulls.
a,b,c,d=S.symbols('a b c d');U=S.Matrix([[a,-b],[b,a]]);V=S.Matrix([[c,-d],[d,c]]);K=U*S.diag(S.Rational(1,3),1)*V.T
Ac=S.Matrix([K[0,0]+K[1,1],K[1,0]-K[0,1],K[0,0]-K[1,1],K[1,0]+K[0,1]])
hc=S.Matrix([a*c*c,a*c*d,a*d*d,b*c*c,b*c*d,b*d*d]);bilinear=[A*hh for A in ZZ for hh in h]
cols=[S.Poly(S.expand(A*hh),a,b,c,d) for A in Ac for hh in hc];keys=sorted(set(pw for co in cols for pw,z in co.terms()))
M=S.Matrix([[co.coeff_monomial(pw) for co in cols] for pw in keys]);ns=M.nullspace();L=[S.expand(sum(zz*bb for zz,bb in zip(vec,bilinear))) for vec in ns];print('leading syzygy dimension',len(L),flush=True)
features=L+list(h);n=len(features);allvars=[*ZZ,*h]
polys=[S.Poly(S.expand(a*b),allvars) for a in features for b in features]
def matpoly(BB):return S.Poly(S.expand((h.T*BB*h)[0]),allvars)
pp=[matpoly(Bconst),*[matpoly(BB) for BB in Bcoeff]]
keys=sorted(set(pw for po in [*polys,*pp] for pw,co in po.terms()))
AG=S.Matrix([[p.coeff_monomial(pw) for p in polys] for pw in keys]);AP=S.Matrix([[p.coeff_monomial(pw) for p in pp[1:]] for pw in keys]);A=AG.row_join(-AP);target=S.Matrix([pp[0].coeff_monomial(pw) for pw in keys]);print('affine coefficient system',A.shape,flush=True)
af=np.array(A,float);bf=np.array(target,float).ravel();pin=np.linalg.pinv(af,rcond=1e-10);nullproj=np.eye(af.shape[1])-pin@af;part=pin@bf
v0=part.copy();best=None
for iteration in range(3000):
 xa=part+nullproj@v0;other=2*xa-v0;GG=other[:n*n].reshape(n,n);GG=(GG+GG.T)/2;ev,U=np.linalg.eigh(GG);psd=(U*np.maximum(ev,0))@U.T;ya=other.copy();ya[:n*n]=psd.ravel();v0+=ya-xa
 if iteration%100==0:
  vv=xa[:n*n].reshape(n,n);eig=np.linalg.eigvalsh((vv+vv.T)/2);err=np.linalg.norm(af@xa-bf);print('iter',iteration,'minEig',eig.min(),'affineErr',err,'params',xa[n*n:],flush=True)
  if eig.min()>1e-5:best=xa.copy();break
if best is None:
 print('No strict Gram acquired; this is not a proof of infeasibility.',flush=True);np.savez(Path(__file__).with_name('sos_search.npz'),variables=xa);raise SystemExit
# Rationalize within the exact coefficient affine space by pivot elimination.
print('rationalizing',flush=True)
aug=A.row_join(target);rr,piv=aug.rref();assert (A.cols not in piv)
free=[i for i in range(A.cols) if i not in piv];vals={i:S.Rational(int(round(best[i]*10**7)),10**7) for i in free}
for row,pivot in enumerate(piv):vals[pivot]=rr[row,-1]-sum(rr[row,col]*vals[col] for col in free)
vec=S.Matrix([vals[i] for i in range(A.cols)]);assert A*vec==target
G=S.Matrix(n,n,list(vec[:n*n]));G=(G+G.T)/2
# Exact positive pivots; no numerical status is promoted.
Gp=G.copy();pivs=[]
for i in range(n):
 pivot=Gp[i,i];pivs.append(pivot)
 if pivot<=0:raise ArithmeticError('Rational Gram not positive definite')
 for j0 in range(i+1,n):
  for k0 in range(j0,n):Gp[j0,k0]=Gp[k0,j0]=Gp[j0,k0]-Gp[j0,i]*Gp[k0,i]/pivot
print('EXACT positive Gram acquired, size',n,'lambda',lam,flush=True)
primitive=(PF+PC+PQ).subs(dict(zip(params,list(vec[n*n:]))))
Path(__file__).with_name('sos_minus_certificate_'+str(lam).replace('/','_')+'.txt').write_text(repr({'lambda':str(lam),'features':[str(f) for f in features],'Gram':[[str(v) for v in row] for row in G.tolist()],'primitive':[str(v) for v in primitive]}))
print('primitive',primitive,flush=True)

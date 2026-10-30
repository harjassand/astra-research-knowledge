"""Search the full invariant numerator-degree<=5 heat primitive P/(1+16|A|c²).
Discovery only; outputs are not a quasiconvexity certificate.
"""
import sympy as S
import numpy as np
from itertools import product
from pathlib import Path
x,y,u,v=S.symbols('x y u v',real=True);ZZ=S.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C=x*(u*u-v*v)+2*y*u*v;P0=F+C+S.Rational(3,16)*(r+t)
D=1+16*(r+t)
h=S.Matrix(S.symbols('h0:6',real=True));Jx=S.Matrix([h[0]+h[4],h[3]-h[1],h[0]-h[4],h[3]+h[1]]).jacobian(h);Jy=S.Matrix([h[1]+h[5],h[4]-h[2],h[1]-h[5],h[4]+h[2]]).jacobian(h)
def symw(W):
 T=Jx.T*W*Jy;return S.expand((T+T.T)/2)
def numerator(P):
 W=D*(P.jacobian(ZZ).T-P.jacobian(ZZ))
 dD=S.Matrix([S.diff(D,a) for a in ZZ]);W-=dD*P.T-P*dD.T
 return symw(W)
H=S.hessian(P0,ZZ);Bbase=S.expand(D*D*(Jx.T*H*Jx+Jy.T*H*Jy))
# All real invariant polynomial one-forms, without silently fixing a gauge.
Pforms=[];labels=[]
for deg in range(1,6):
 for target,form in [(-2,S.Matrix([1,S.I,0,0])),(-1,S.Matrix([0,0,1,S.I]))]:
  for pw in product(range(deg+1),repeat=4):
   if sum(pw)!=deg or 2*pw[0]-2*pw[1]+pw[2]-pw[3]!=target:continue
   mon=(x+S.I*y)**pw[0]*(x-S.I*y)**pw[1]*(u+S.I*v)**pw[2]*(u-S.I*v)**pw[3]
   vv=mon*form
   for part in [S.re,S.im]:
    Pforms.append(vv.applyfunc(lambda q:S.expand(part(S.expand_complex(q)))))
    labels.append((deg,target,pw,str(part)))
print('invariant numerator forms',len(Pforms),flush=True)
Blist=[numerator(P) for P in Pforms]
# Remove density gauges before the null equations.
keys=sorted(set((i,j,pw) for BB in Blist for i in range(6) for j in range(i,6) for pw,co in S.Poly(BB[i,j],*ZZ).terms() if co))
BM=S.Matrix([[S.Poly(BB[i,j],*ZZ).coeff_monomial(pw) for BB in Blist] for i,j,pw in keys])
pivots=BM.rref()[1];Blist=[Blist[i] for i in pivots];Pforms=[Pforms[i] for i in pivots];labels=[labels[i] for i in pivots]
print('independent rational correction densities',len(Blist),flush=True)
# All exact sharp-boundary and asymptotic acoustic null conditions.
tau,q=S.symbols('tau q',real=True);Astar={x:-S.Rational(1,4),y:tau,u:-tau/2,v:-S.Rational(1,4)};hs=S.Matrix([1,-1,1,1,-1,1])
Ac={x:-2*(1-q*q),y:-4*q,u:1+q*q,v:0};hc=S.Matrix([1,-q,q*q,q,-q*q,q*q*q])
def top(BB):
 return BB.applyfunc(lambda pol:S.Add(*(co*S.prod(a**pp for a,pp in zip(ZZ,pw)) for pw,co in S.Poly(pol,*ZZ).terms() if sum(pw)==6)))
cols=[]
for BB in [Bbase,*Blist]:
 vals=[]
 for sub,hh,var,part in [(Astar,hs,tau,BB),(Ac,hc,q,top(BB))]:
  out=part.subs(sub,simultaneous=True)*hh
  for entry in out:
   pp=S.Poly(S.expand(entry),var);vals.extend(pp.nth(i) for i in range(18))
 cols.append(vals)
A=S.Matrix.hstack(*(S.Matrix(c) for c in cols[1:]));rhs=-S.Matrix(cols[0]);print('null linear system',A.shape,'rank',A.rank(),flush=True)
try:solution,parameters=A.gauss_jordan_solve(rhs)
except ValueError:
 print('EXACT FAILURE: no rational primitive in this denominator/numerator class satisfies necessary null columns.');raise SystemExit
print('free density parameters',len(parameters),flush=True)
Bconst=S.expand(Bbase+sum((co.subs({p:0 for p in parameters})*BB for co,BB in zip(solution,Blist)),S.zeros(6)))
Bs=[S.expand(sum((S.diff(co,p)*BB for co,BB in zip(solution,Blist)),S.zeros(6))) for p in parameters]
# Save exact affine family for independent replay and continued computation.
cache=Path(__file__).with_name('rational_family.txt')
cache.write_text(str({'denominator':D,'labels':labels,'solution':solution,'parameters':parameters}))
print('building numerical evaluators',flush=True)
funcs=[S.lambdify((x,y,u,v),BB,'numpy',cse=True) for BB in [Bconst,*Bs]]
pts=[(a,b,c,0) for a in [-3,-1,-.5,-.25,0,.25,.5,1,3] for b in [0,.125,.5,1,3] for c in [0,.125,.25,.5,1,3]]
rng=np.random.default_rng(20261030);pts.extend(tuple([*rng.normal(size=3),0]) for _ in range(500))
mat=np.array([[ff(*pt) for ff in funcs] for pt in pts],float)
# Normalize each sample and avoid giving large gradients excessive weight.
scales=np.maximum(np.linalg.norm(mat[:,0],axis=(1,2)),1)
mat=mat/scales[:,None,None,None]
pn=len(parameters);theta=np.zeros(pn);best=(np.inf,None)
for iteration in range(2500):
 B=mat[:,0]+np.einsum('p,npij->nij',theta,mat[:,1:]);ev,U=np.linalg.eigh(B);worst=ev[:,0];loss=np.mean(np.minimum(worst,0)**2)
 if loss<best[0]:best=loss,theta.copy()
 if iteration%100==0:print('iteration',iteration,'loss',loss,'worst',worst.min(),'parameters',theta,flush=True)
 if worst.min()>-1e-9:break
 # Convex squared hinge loss for all sampled minimum eigenvectors.
 hh=U[:,:,0];grads=np.einsum('ni,npij,nj->np',hh,mat[:,1:],hh);neg=np.minimum(worst,0)
 gradient=2*np.mean(neg[:,None]*grads,axis=0)
 L=2*np.linalg.norm(grads,2)**2/len(pts)
 theta-=gradient/max(L,1e-12)
np.savez(Path(__file__).with_name('search_result.npz'),theta=best[1],loss=best[0])
print('best numerical sampled loss',best[0],'theta',best[1],flush=True)
print('Numerical feasibility or failure is not a global mathematical conclusion.',flush=True)

"""One specified s-dependent rational alternative; finite diagnostics only.

g_sigma = eps*T + [F*H^2 + p6*d + alpha*T^2*d^2
                              + c*d^2*(s^2+H^2)]/(H^2+d^2),
H=T+sigma, d=s-det(B). Graph values and normal derivatives are exact.
The weighted homogeneous sigma=eps=0 limit is a necessary convexity test.
This file tests that limit, rather than claiming a sampled global proof.
"""
from pathlib import Path
import json
import time
import numpy as np
import sympy as sp
import cvxpy as cp

OUT=Path(__file__).resolve().parent
start=time.monotonic()
a,b,c0,d0,s=vv=sp.symbols('a b c d s')
u,v,w,q=a*a+c0*c0,b*b+d0*d0,a*b+c0*d0,a*d0-b*c0
T=u+v
x,y,z=u-v,2*w,2*q
F=(sp.Rational(55220381,10**10)*(u*u+v*v)
   +sp.Rational(114430029,625000000)*u*v
   -sp.Rational(801761987,5000000000)*w*w
   +sp.Rational(118849817,4000000000)*q*(u-v))
p=(sp.Rational(6222019,200000000)*x**3
   +sp.Rational(1686519911,10**10)*x*x*z
   +sp.Rational(81172813,2000000000)*x*z*z
   +sp.Rational(1726116771,10**10)*z**3
   +sp.Rational(128626163,5000000000)*x*y*y
   +sp.Rational(373321239,2000000000)*y*y*z)
dd=s-q
D=T*T+dd*dd
nums=[sp.expand(F*T*T+p*dd),sp.expand(T*T*dd*dd),
      sp.expand(dd*dd*(s*s+T*T))]
data=[]
for n in nums:
    data.append(sp.lambdify(vv,(n,sp.Matrix([sp.diff(n,t) for t in vv]),
                                sp.hessian(n,vv)),modules='numpy',cse=True))
dfun=sp.lambdify(vv,(D,sp.Matrix([sp.diff(D,t) for t in vv]),sp.hessian(D,vv)),
                 modules='numpy',cse=True)
compile_seconds=time.monotonic()-start


def hessians(point):
    den,den_g,den_h=dfun(*point)
    den_g=np.asarray(den_g,dtype=float).reshape(5)
    den_h=np.asarray(den_h,dtype=float)
    ans=[]
    for func in data:
        n,ng,nh=func(*point)
        ng=np.asarray(ng,dtype=float).reshape(5)
        nh=np.asarray(nh,dtype=float)
        ans.append((den*den*nh-den*(np.outer(ng,den_g)+np.outer(den_g,ng)+n*den_h)
                    +2*n*np.outer(den_g,den_g))/den**3)
    return np.asarray(ans)


rng=np.random.default_rng(281028)
points=[]
for k in range(420):
    bvec=rng.normal(size=4)
    bvec/=np.linalg.norm(bvec)
    ns=rng.uniform(-2,2) if k%2 else rng.choice([-1,1])*10**rng.uniform(-2,2)
    points.append([*bvec,ns])
for base in [[1,0,0,0],[1,0,0,1],[1,0,0,-1]]:
    base=np.asarray(base,dtype=float)/np.linalg.norm(base)
    for ns in np.linspace(-3,3,31):
        points.append([*base,ns])
points=np.asarray(points)
hh=np.asarray([hessians(point) for point in points])
alpha=cp.Variable(nonneg=True)
cc=cp.Variable(nonneg=True)
margin=cp.Variable()
constraints=[hh[k,0]+alpha*hh[k,1]+cc*hh[k,2]-margin*np.eye(5)>>0
             for k in range(len(points))]
constraints += [margin<=sp.Rational(1,100)]
prob=cp.Problem(cp.Maximize(margin-1e-10*(alpha+cc)),constraints)
solve_start=time.monotonic()
value=prob.solve(solver='CLARABEL',tol_gap_abs=1e-10,tol_gap_rel=1e-10,
                 tol_feas=1e-10,max_iter=150,verbose=False)
solve_seconds=time.monotonic()-solve_start
out={'status':'FINITE_NECESSARY_HESSIAN_DIAGNOSTIC','solver_status':prob.status,
     'points':len(points),'compile_seconds':compile_seconds,
     'solve_seconds':solve_seconds,'total_seconds':time.monotonic()-start,
     'objective':value,'alpha':None if alpha.value is None else float(alpha.value),
     'c':None if cc.value is None else float(cc.value),
     'margin':None if margin.value is None else float(margin.value),
     'scope':'Fixed two-parameter rational profile, homogeneous necessary limit only; '
             'sampled Hessians never certify global convexity.'}
if alpha.value is not None:
    aa,bb=float(alpha.value),float(cc.value)
    eigen=[]
    for k in range(len(points)):
        ee,ev=np.linalg.eigh(hh[k,0]+aa*hh[k,1]+bb*hh[k,2])
        eigen.append((float(ee[0]),k,ev[:,0]))
    worst=min(eigen,key=lambda t:t[0])
    out['worst']={'value':worst[0],'point':points[worst[1]].tolist(),
                  'direction':worst[2].tolist()}
    duals=np.asarray([con.dual_value for con in constraints[:-1]])
    np.savez_compressed(OUT/'RATIONAL_PROFILE_DATA.npz',points=points,hessians=hh,duals=duals)
(OUT/'RATIONAL_PROFILE_SEARCH.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2),flush=True)

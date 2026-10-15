import sympy as S, numpy as np, json, sys
from scipy.optimize import minimize
from pathlib import Path
out=Path(__file__).parent
X=S.symbols('a b c d');a,b,c,d=X;u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
F=S.expand(u*u+v*v+S.Rational(166,3)*u*v-S.Rational(460,9)*w*w-S.Rational(52,9)*q*(u-v))
grad=[S.diff(F,x) for x in X];hess=S.hessian(F,X)
gf=S.lambdify(X,grad,'numpy');hf=S.lambdify(X,hess,'numpy')
mode_sets=[[(1,0),(0,1),(1,1)],[(1,0),(0,1),(1,1),(1,-1)],[(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2)]]
mi=int(sys.argv[1]) if len(sys.argv)>1 else 0
modes=np.array(mode_sets[mi]);N=16;xx=np.arange(N)*2*np.pi/N;xy=np.array(np.meshgrid(xx,xx,indexing='ij')).reshape(2,-1);cs=np.cos(modes@xy)
dim=4+2*len(modes);D=np.zeros((dim,4,N*N));L=np.zeros_like(D)
for j in range(4): D[j,j,:]=1
for k,n in enumerate(modes):
 for target in range(2):
  D[4+2*k+target,target*2:target*2+2,:]=n[:,None]*cs[k]
  L[4+2*k+target]=np.dot(n,n)*D[4+2*k+target]
# normalize all physical gradient columns to comparable L2 size.
scales=np.sqrt(np.mean(np.sum(D*D,axis=1),axis=1));D/=scales[:,None,None];L/=scales[:,None,None]
def fg(z):
 A=np.einsum('i,ijk->jk',z,D);V=np.einsum('i,ijk->jk',z,L);G=np.array(gf(*A));H=np.array(hf(*A));value=np.mean(np.sum(G*V,axis=0));G1=np.einsum('ijk,jk->ik',H,V);g=np.einsum('jk,ijk->i',G1,D)/(N*N)+np.einsum('jk,ijk->i',G,L)/(N*N);return value,g
rng=np.random.default_rng(100+mi);record=[];best=None
for i in range(150):
 z=rng.normal(size=dim);z/=np.linalg.norm(z)
 sol=minimize(lambda z:fg(z),z,jac=True,method='SLSQP',constraints=[{'type':'eq','fun':lambda z:z@z-1,'jac':lambda z:2*z}],options={'ftol':1e-11,'maxiter':600})
 if best is None or sol.fun<best.fun:
  best=sol;print('mode set',mi,'iteration',i,'best',sol.fun,'status',sol.success,flush=True)
 if best.fun < -1e-7:break
np.savez(out/f'heat_search_modes{mi}.npz',modes=modes,z=best.x,scales=scales,value=best.fun,N=N)
print('modes',modes.tolist(),'B',best.x[:4].tolist(),'raw coefficients',(best.x/scales).tolist(),'value',best.fun,flush=True)

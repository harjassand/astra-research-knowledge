"""Face tangent equations including the spatial acoustic-zero derivative."""
from pathlib import Path
import numpy as np,sympy as S,json
from scipy.optimize import minimize_scalar
here=Path(__file__).parent
a,b,c,d,t=S.symbols('a b c d t',real=True);vv=S.symbols('u l p n q r',real=True)
u,l,p,n,q,r=vv;X=a*a+c*c-b*b-d*d;Y=2*(a*b+c*d);Z=2*(a*d-b*c)
F=u*X*X+2*l*X*Y+2*p*X*Z+n*Y*Y+2*q*Y*Z+r*Z*Z
H=S.hessian(F,(a,b,c,d));pieces=[S.lambdify((a,b,c,d),H.diff(v),'numpy',cse=True) for v in vv]
results=[]
for nn,pp,qq in [(1.5,.4,.3),(1.3,.5,.2),(1.,.8,0.),(1.5,.8,0.)]:
    B=np.diag([1.,nn]);dd=np.array([pp,qq]);HH=2*nn*np.eye(2)-B@B-np.outer(dd,dd);tt=np.array([qq,-nn*pp])
    def threshold(theta):
        e=np.array([np.cos(theta),np.sin(theta)])
        return (e@(B@B+3*np.outer(dd,dd))@e+4*(e@tt)**2/(e@HH@e))/(2*e@B@e)
    grid=np.linspace(0,np.pi,1001,endpoint=False);idx=max(range(len(grid)),key=lambda i:threshold(grid[i]));center=grid[idx]
    fit=minimize_scalar(lambda x:-threshold(x),bounds=(center-.02,center+.02),method='bounded',options={'xatol':1e-15})
    theta=fit.x;rv=-fit.fun;R=np.array([np.cos(theta/2),np.sin(theta/2),0.,0.]);Rprime=np.array([-R[1],R[0],0.,0.])
    co=np.array([1.,0.,pp,nn,qq,rv]);HR=sum(z*f(*R) for z,f in zip(co,pieces));val,vec=np.linalg.eigh(HR);A=vec[:,0]
    face=np.column_stack([f(*R)@A for f in pieces]);extra=np.array([2*Rprime@f(*A)@R for f in pieces])[None,:]
    sv0=np.linalg.svd(face,compute_uv=False);sv=np.linalg.svd(np.vstack((face,extra)),compute_uv=False)
    results.append({'n':nn,'p':pp,'q':qq,'r':rv,'theta':theta,'R':R.tolist(),'A':A.tolist(),
                    'face_singular_values':sv0.tolist(),'with_derivative':sv.tolist(),'residual':float(np.linalg.norm(np.vstack((face,extra))@co))})
    print(json.dumps(results[-1]),flush=True)
(here/'face_rank_diagnostic.json').write_text(json.dumps(results,indent=2)+'\n')

"""Target true PC support at the singular acoustic background; numeric only."""
from pathlib import Path
import sys,json,time
import numpy as np
from scipy.optimize import differential_evolution
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'sector_gap'))
from matrix_pair_search import hessian_batch
from search_support import energy,invariants
from acoustic_boundary import acoustic


def gradient(z,tau):
    a,b,c,d=np.moveaxis(np.asarray(z),-1,0);u,v,w,q=invariants(z)
    du,dv,dw,dq=2*u+4*q,2*v-4*q,6*w,2*tau*q+4*(u-v)
    return np.stack([2*a*du+b*dw+d*dq,2*b*dv+a*dw-c*dq,
                     2*c*du+d*dw-b*dq,2*d*dv+c*dw+a*dq],axis=-1)


def sphere(theta):
    t,p,a=np.asarray(theta)
    return np.stack([np.cos(t),np.sin(t)*np.cos(p),
                     np.sin(t)*np.sin(p)*np.cos(a),
                     np.sin(t)*np.sin(p)*np.sin(a)],axis=-1)


def main():
    start=time.monotonic();tau=89-12*np.sqrt(42);m=-39/58+15*np.sqrt(42)/29
    y=(m+np.sqrt(m*m-4))/2;z=np.sqrt(y)
    Q=np.array(acoustic(tau,z),float);values,vectors=np.linalg.eigh(Q)
    A=vectors[:,0];H=np.array([1,z,0,0]);cof=np.array([0,0,-z,1])
    k=float((hessian_batch(A[None],tau)[0]@H)@cof/(cof@cof))
    residual=hessian_batch(A[None],tau)[0]@H-k*cof
    def objective(theta):
        R=np.atleast_2d(sphere(theta))
        g=np.einsum('i,nij,j->n',A,hessian_batch(R,tau),A)/2
        g-=(gradient(R,tau)@A)**2/(4*energy(R,tau))
        answer=g-k*invariants(R)[3]
        return answer[0] if np.asarray(theta).ndim==1 else answer
    searches=[]
    for seed in [20261027,20261028,20261029]:
        r=differential_evolution(objective,[(0,np.pi),(0,np.pi),(0,2*np.pi)],
            seed=seed,popsize=20,maxiter=200,tol=1e-10,atol=1e-12,
            vectorized=True,updating='deferred',workers=1,polish=True)
        searches.append({'seed':seed,'minimum':float(r.fun),'R':sphere(r.x).tolist(),
                         'iterations':r.nit,'batch_evaluations':r.nfev})
    u,v,w,q=invariants(A)
    out={'status':'NUMERICAL_ONLY_NO_PC_OR_NON_PC_CONCLUSION','tau':tau,
         'critical_z':z,'acoustic_eigenvalues':values.tolist(),'A':A.tolist(),
         'forced_kappa':k,'forced_gradient_residual':float(np.linalg.norm(residual)),
         'critical_cubic_pairing':float(gradient(H,tau)@A),
         'quadratic_selector_constraint':{'u_minus_v':float(u-v),'q':float(q),'rhs':k},
         'targeted_global_searches':searches,'wall_seconds':time.monotonic()-start}
    (Path(__file__).resolve().parent/'BOUNDARY_PROBE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()

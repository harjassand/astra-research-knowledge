"""Periodic P1 gradients; exact cell integration, numerical candidate search."""
import json,time,argparse
import numpy as np
import scipy.sparse as ss
from scipy.optimize import minimize
from compatible_core import TENSOR,SCALE,value,gradient,ROOT

class FEMProblem:
 def __init__(self,n,alternate=False):
    self.n=n;self.alternate=alternate;tri=[];rr=[];cc=[];vv=[]
    for i in range(n):
     for j in range(n):
      v=[i*n+j,((i+1)%n)*n+j,((i+1)%n)*n+(j+1)%n,i*n+(j+1)%n]
      if alternate and(i+j)%2:specs=[([v[0],v[1],v[3]],[[-1,-1],[1,0],[0,1]]),([v[1],v[2],v[3]],[[0,-1],[1,1],[-1,0]])]
      else:specs=[([v[0],v[1],v[2]],[[-1,0],[1,-1],[0,1]]),([v[0],v[2],v[3]],[[0,-1],[1,0],[-1,1]])]
      for vertices,grads in specs:
       t=len(tri);tri.append((vertices,grads))
       for node,g in zip(vertices,grads):
        for o in range(2):
         for axis in range(2):
          if g[axis]:rr.append(4*t+2*o+axis);cc.append(2*node+o);vv.append(n*g[axis])
    self.triangles=tri;self.N=len(tri);self.design=ss.csr_matrix((vv,(rr,cc)),shape=(4*self.N,2*n*n))
 def evaluate(self,p,details=False):
    norm=np.linalg.norm(p);q=p/norm;x=(self.design@q).reshape(-1,4);cov=x.T@x/self.N
    h=12*np.einsum('ijkl,kl->ij',TENSOR,cov);b=np.mean(gradient(x),axis=0);c=float(np.mean(value(x)))
    m2=float(np.trace(cov));he=np.linalg.eigvalsh(h);assert he[0]>=.99*SCALE/200000*m2
    B=-np.linalg.solve(h,b);gap=c+float(b@B)/2;square=np.sum(x*x,axis=1);m4=float(np.mean(square*square));obj=gap/m4
    g=gradient(x)+12*np.einsum('ijkl,j,nk,nl->ni',TENSOR,B,x,x,optimize=True)
    g+=x@(12*np.einsum('ijkl,j,k->il',TENSOR,B,B)).T;g=(g-obj*4*square[:,None]*x)/m4
    gq=self.design.T@g.reshape(-1)/self.N;gp=(gq-q*np.dot(q,gq))/norm
    if not details:return obj,gp
    return dict(objective_scaled=obj,original_gap=gap/SCALE,fourth_moment=m4,second_moment=m2,c_scaled=c,Schur_loss_scaled=-float(b@B)/2,background=B.tolist(),H_eigenvalues_scaled=he.tolist(),covariance_eigenvalues=np.linalg.eigvalsh(cov).tolist(),mean_gradient_max=float(np.max(abs(np.mean(x,axis=0)))),mean_determinant=float(np.mean(x[:,0]*x[:,3]-x[:,1]*x[:,2])),gradient_norm=float(np.linalg.norm(gp)),normalized_nodes=q.reshape(self.n,self.n,2).tolist(),mesh=self.n,alternating_diagonal=self.alternate)

def run(n,starts,iterations,alternate):
 p=FEMProblem(n,alternate);rng=np.random.default_rng(617+n+31*alternate);out={'status':'RESTRICTED_COMPATIBLE_P1_SEARCH_NOT_QC_CERTIFICATE','runs':[]};path=ROOT/f'data/fem_n{n}_alt{int(alternate)}.json'
 for k in range(starts):
    start=time.monotonic();x=rng.normal(size=(n*n,2));x-=x.mean(axis=0)
    opt=minimize(p.evaluate,x.reshape(-1),jac=True,method='L-BFGS-B',options=dict(maxiter=iterations,ftol=1e-14,gtol=2e-10,maxls=50,maxcor=20))
    r=p.evaluate(opt.x,True);r.update(start=k,iterations=int(opt.nit),function_evaluations=int(opt.nfev),success=bool(opt.success),message=str(opt.message),seconds=time.monotonic()-start)
    out['runs'].append(r);out['best_start']=min(range(len(out['runs'])),key=lambda i:out['runs'][i]['objective_scaled']);path.write_text(json.dumps(out,indent=2));print(n,alternate,k,r['objective_scaled'],r['gradient_norm'],r['seconds'],flush=True)
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=8);p.add_argument('--starts',type=int,default=8);p.add_argument('--iterations',type=int,default=1500);p.add_argument('--alternate',action='store_true');a=p.parse_args();run(a.n,a.starts,a.iterations,a.alternate)

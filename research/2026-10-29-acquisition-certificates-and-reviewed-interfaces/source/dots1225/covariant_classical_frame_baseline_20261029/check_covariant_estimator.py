import numpy as np,json,time
from pathlib import Path
rng=np.random.default_rng(1977)
def rot():
 q=rng.normal(size=4);q/=np.linalg.norm(q);w,x,y,z=q
 return np.array([[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)],[2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]])
R=rot();eta=.1;alpha=1/(8+eta);g=(1-eta)/(8+eta);rows=[];start=time.time()
for m in [100,1000,10000]:
 matrices=[];mse=[];covmse=[]
 for trial in range(2000):
  A,B=rot(),rot();S=A@R@B.T;c=S.flatten()/np.sqrt(3);sigma=alpha*np.eye(9)-g*np.outer(c,c)
  hat=np.diag(rng.binomial(m,np.diag(sigma))/m)
  for i in range(9):
   for j in range(i+1,9):
    pm=(sigma[i,i]+sigma[j,j]+2*sigma[i,j])/2;pn=(sigma[i,i]+sigma[j,j]-2*sigma[i,j])/2
    counts=rng.multinomial(m,[pm,pn,1-pm-pn]);hat[i,j]=hat[j,i]=(counts[0]-counts[1])/(2*m)
  covmse.append(np.linalg.norm(hat-sigma,'fro')**2)
  _,vec=np.linalg.eigh(hat);Q=np.sqrt(3)*vec[:,0].reshape(3,3)
  if np.linalg.det(Q)<0:Q=-Q
  u,_,vh=np.linalg.svd(Q);Shat=u@np.diag([1,1,np.linalg.det(u@vh)])@vh
  Rh=A.T@Shat@B;matrices.append(Rh);mse.append(np.linalg.norm(Rh-R,'fro')**2)
 M=np.mean(matrices,axis=0);kappa=np.trace(R.T@M)/3
 rows.append(dict(m_per_setting=m,total_records=45*m,trials=2000,mean_rotation_squared_error=float(np.mean(mse)),averaged_error_scalar_proxy=float(np.mean(mse)/8),covariance_mse=float(np.mean(covmse)),covariance_mse_upper=81/(4*m),finite_mc_covariance_residual=float(np.linalg.norm(M-kappa*R,'fro')),exact_trace_identity_residual=abs(float(np.mean(mse))-6*(1-kappa)),conservative_theorem_bound=min(1,432/(m*g*g))))
out=dict(eta=eta,rows=rows,seconds=time.time()-start,scope='Monte Carlo classical estimator at fixed unknown frame; finite Monte Carlo average is not exactly depolarizing; theorem uses exact quadrature')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

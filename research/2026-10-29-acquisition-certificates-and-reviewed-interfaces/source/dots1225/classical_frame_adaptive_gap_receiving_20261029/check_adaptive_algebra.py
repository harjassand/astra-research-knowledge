"""Independent exact gap inequalities and floating frame-error diagnostics."""
from fractions import Fraction as F
from pathlib import Path
import numpy as np,json
exact=0
for g in [F(1,8),F(1,100),F(1,10**6)]:
 for eratio in [F(0),F(1,1000),F(1,100),F(1,8),F(1,3)]:
  E=g*eratio
  for p0,p1 in [(E,-E),(-E,E),(F(0),F(0))]:
   # Restrict ordered-eigenvalue test to noncrossing diagonal perturbations.
   gap=g+p1-p0
   if gap<0:continue
   lower=max(F(0),gap-2*E);assert lower<=g and lower>=g-4*E;exact+=1
assert sum(F(1,l*(l+1)) for l in range(1,1001))==1-F(1,1001)
rng=np.random.default_rng(20261137);count=0;maxratio=0.
def rot(q):
 w,x,y,z=q
 return np.array([[w*w+x*x-y*y-z*z,2*(x*y-w*z),2*(x*z+w*y)],[2*(x*y+w*z),w*w-x*x+y*y-z*z,2*(y*z-w*x)],[2*(x*z-w*y),2*(y*z+w*x),w*w-x*x-y*y+z*z]])
for g in [.125,.01,1e-6]:
 for ratio in [.001,.005,.01,.02,.03]:
  for _ in range(8):
   q=rng.normal(size=4);q/=np.linalg.norm(q);R=rot(q);c=R.ravel()/np.sqrt(3);sigma=(1+g)*np.eye(9)/9-g*np.outer(c,c)
   V=rng.normal(size=(9,9));V=(V+V.T)/2;V*=g*ratio/np.linalg.norm(V,2);E=np.linalg.norm(V,2);vals,U=np.linalg.eigh(sigma+V);gl=max(0,vals[1]-vals[0]-2*E)
   assert gl<=g+1e-14 and gl>=g-4*E-1e-14
   A=np.sqrt(3)*U[:,0].reshape(3,3)
   if np.linalg.det(A)<0:A=-A
   u,s,vh=np.linalg.svd(A);Rh=u@np.diag([1,1,np.linalg.det(u@vh)])@vh;error=np.linalg.norm(Rh-R,'fro')/(2*np.sqrt(2));radius=2*np.sqrt(3)*E/gl
   assert error<=radius+1e-12 and radius<.2;maxratio=max(maxratio,error/radius);count+=1
out=dict(exact_gap_extremes=exact,exact_delta_schedule_partial_sum=True,independent_frame_perturbations=count,largest_error_to_certificate_ratio=maxratio,scope='Algebraic inequality and finite floating frame projection tests; no interval eigensolver, actual quantum data, finite-cap conditional guarantee or hardware claim.')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

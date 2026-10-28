"""Direct normalized Schur-loss search; same actual compatible fields."""
import json,time,numpy as np,scipy.sparse as ss
from scipy.optimize import minimize
from compatible_core import FourierProblem,half_square,gradient,ROOT
from search_fem import FEMProblem

def objective(problem,p):
 phi,gphi=problem.evaluate(p);r=problem.evaluate(p,True);m4=r['fourth_moment'];c=r['c_scaled'];assert c>0
 norm=np.linalg.norm(p);q=p/norm;sparse=ss.issparse(problem.design)
 x=(problem.design@q).reshape(-1,4)if sparse else np.einsum('npi,p->ni',problem.design,q)
 def derivative(v):
    z=problem.design.T@v.reshape(-1)/problem.N if sparse else np.einsum('npi,ni->p',problem.design,v)/problem.N
    return(z-q*np.dot(q,z))/norm
 gm4=derivative(4*np.sum(x*x,axis=1)[:,None]*x);gc=derivative(gradient(x))
 ratio=phi*m4/c;g=(m4*gphi+phi*gm4-ratio*gc)/c
 return ratio,g

def derivative_check():
 rng=np.random.default_rng(1981);out=[]
 for name,problem,dim in [('Fourier3',FourierProblem(half_square(3)),96),('P1_16',FEMProblem(16,False),512)]:
  z=rng.normal(size=dim);_,g=objective(problem,z);errors=[]
  for k in range(8):
   h=rng.normal(size=dim);h/=np.linalg.norm(h);eps=1e-5
   fd=(objective(problem,z+eps*h)[0]-objective(problem,z-eps*h)[0])/(2*eps)
   errors.append(abs(fd-h@g))
  assert max(errors)<1e-7
  out.append(dict(model=name,directional_derivative_max_error=max(errors),directions=8))
 (ROOT/'data/NUMERICAL_CONTROLS.json').write_text(json.dumps(out,indent=2));return out

def run():
 out={'status':'RESTRICTED_COMPATIBLE_SCHUR_RATIO_SEARCH','runs':[]};rng=np.random.default_rng(961)
 for kind in ['fourier','fem']:
  p=FourierProblem(half_square(3))if kind=='fourier'else FEMProblem(16,False)
  dim=4*p.m if kind=='fourier'else 512
  for k in range(8):
    start=time.monotonic();opt=minimize(lambda z:objective(p,z),rng.normal(size=dim),jac=True,method='L-BFGS-B',options=dict(maxiter=2000,gtol=2e-10,ftol=1e-14,maxcor=20,maxls=50))
    rec=p.evaluate(opt.x,True);rec.update(kind=kind,start=k,Delta_over_c=float(objective(p,opt.x)[0]),seconds=time.monotonic()-start)
    out['runs'].append(rec);(ROOT/'data/schur_ratio_search.json').write_text(json.dumps(out,indent=2));print(kind,k,rec['Delta_over_c'],rec['objective_scaled'],rec['seconds'],flush=True)
 return out
if __name__=='__main__':run()

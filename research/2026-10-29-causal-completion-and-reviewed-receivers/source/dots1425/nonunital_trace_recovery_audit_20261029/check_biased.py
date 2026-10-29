import numpy as np,json
rng=np.random.default_rng(1303);X=np.array([[0,1],[1,0]],complex);e01=np.array([[0,1],[0,0]],complex);mx=0;count=0
for gamma in [.5,.7,.95]:
 eta=1-gamma;K=[X@np.diag([1,np.sqrt(eta)]),X@np.array([[0,np.sqrt(gamma)],[0,0]])];F=lambda y:sum(k@y@k.conj().T for k in K)
 for p in [.001,.1,.333,.7,.99,.9999]:
  sig=np.array([p,1-p]);r=eta*(1-p);nu=np.array([r,1-r]);R=[np.diag(np.sqrt(sig))@k.conj().T@np.diag(1/np.sqrt(nu)) for k in K];a=np.sqrt(eta*p/(gamma+eta*p));theta=(np.log(p/(1-p))+np.log(r/(1-r)))/2
  for t in [-2,-.7,0,.9,3]:
   u=np.diag(np.exp(.5j*t*np.log(sig)));v=np.diag(np.exp(-.5j*t*np.log(nu)));Rt=[u@k@v for k in R];out=sum(k@F(e01)@k.conj().T for k in Rt);res=np.linalg.norm(out-a*np.exp(1j*t*theta)*e01);mx=max(mx,res);assert res<1e-12;count+=1
out={'rotated_map_cases':count,'max_formula_residual':mx,'scope':'floating algebra diagnostic; proof is in addendum'};print(out);open('BIASED_CHECKS.json','w').write(json.dumps(out,indent=2)+'\n')

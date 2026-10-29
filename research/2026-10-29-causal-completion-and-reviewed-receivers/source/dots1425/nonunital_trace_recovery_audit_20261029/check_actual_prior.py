import numpy as np,json
rng=np.random.default_rng(1305);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);S=lambda a:-sum(v*np.log(v) for v in np.linalg.eigvalsh(a) if v>1e-14);T=lambda a,b:.5*sum(abs(np.linalg.eigvalsh(a-b)));rows=[]
for d in [1,2,3]:
 shift=np.roll(np.eye(d),1,axis=0);phase=np.diag(np.exp(2j*np.pi*np.arange(d)/d))
 for gamma in [.5,.7,.95]:
  eta=1-gamma;A=[np.kron(X@np.diag([1,np.sqrt(eta)]),np.eye(d)),np.kron(X@np.array([[0,np.sqrt(gamma)],[0,0]]),np.eye(d))];F=lambda y:sum(k@y@k.conj().T for k in A);zz=np.kron(Z,np.eye(d));maxratio=0
  for _ in range(20):
   g=rng.normal(size=(2*d,2*d))+1j*rng.normal(size=(2*d,2*d));r=g@g.conj().T;r/=np.trace(r);ensemble=[]
   for a in range(2):
    for b in range(d):
     for c in range(d):
      u=np.kron(np.linalg.matrix_power(Z,a),np.linalg.matrix_power(shift,b)@np.linalg.matrix_power(phase,c));ensemble.append(u@r@u.conj().T)
   avg=sum(ensemble)/len(ensemble);out=[F(e) for e in ensemble];avgo=sum(out)/len(out);delta=S(avg)-sum(map(S,ensemble))/len(ensemble)-S(avgo)+sum(map(S,out))/len(out);dist=sum(T(e,(e+zz@e@zz)/2) for e in ensemble)/len(ensemble);p=np.trace(avg[:d,:d]).real;a=np.sqrt(eta*p/(gamma+eta*p));ratio=dist*(1-a)/np.sqrt(delta);assert ratio<=1+1e-10;maxratio=max(maxratio,ratio)
   assert np.linalg.norm(avg-np.kron(np.diag([p,1-p]),np.eye(d)/d))<1e-12
  rows.append({'reference_dimension':d,'gamma':gamma,'ensembles':20,'max_e_over_claimed_bound':float(maxratio)})
print(rows);open('ACTUAL_PRIOR_CHECKS.json','w').write(json.dumps({'scope':'floating actual Holevo calculations on explicit correlated-state ensembles','rows':rows},indent=2)+'\n')

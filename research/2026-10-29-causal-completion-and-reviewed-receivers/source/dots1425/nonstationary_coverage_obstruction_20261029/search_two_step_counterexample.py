import numpy as np,json
from scipy.optimize import minimize
rng=np.random.default_rng(77531);d=2;X=np.array([[0,1],[1,0]],complex)
A=[np.kron(X@np.diag([1,1/np.sqrt(2)]),np.eye(d)),np.kron(X@np.array([[0,1/np.sqrt(2)],[0,0]]),np.eye(d))];ls=np.kron(np.diag(np.log([1/3,2/3])),np.eye(d))
def ent(a):
 e=np.linalg.eigvalsh(a);e=e[e>1e-14];return -np.sum(e*np.log(e))
def evaluate(v):
 g=(v[:16]+1j*v[16:]).reshape(4,4);r=g@g.conj().T;r/=np.trace(r);o=sum(k@r@k.conj().T for k in A);o2=sum(k@o@k.conj().T for k in A)
 l1=ent(o)-ent(r)+np.trace((o-r)@ls).real;l2=ent(o2)-ent(r)+np.trace((o2-r)@ls).real
 return (l2/l1 if l1>1e-9 else 0),r,l1,l2
best=(-1,None);rows=[]
for i in range(10):
 fit=minimize(lambda v:-evaluate(v)[0],rng.normal(size=32),method='L-BFGS-B',options={'maxiter':300,'ftol':1e-11});ratio,r,l1,l2=evaluate(fit.x);rows.append({'start':i,'ratio':ratio,'iterations':fit.nit,'success':bool(fit.success)})
 if ratio>best[0]:best=(ratio,{'rho_real':r.real.tolist(),'rho_imag':r.imag.tolist(),'loss1':l1,'loss2':l2})
print(best[0],flush=True);open('TWO_STEP_OPTIMIZER.json','w').write(json.dumps({'scope':'untrusted floating finder, no bound proved','rows':rows,'best_ratio':best[0],'best':best[1]},indent=2)+'\n')

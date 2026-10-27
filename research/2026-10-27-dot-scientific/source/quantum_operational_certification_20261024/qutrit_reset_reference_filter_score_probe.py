exec(open('mixed_reset_purity_probe.py').read().split('best=-1e9')[0])
from scipy.optimize import differential_evolution
ph=np.eye(3).reshape(-1)/np.sqrt(3)
def flog(X):
 e,V=np.linalg.eigh(X);return (V*np.where(e>1e-15,e*np.log(np.maximum(e,1e-300)),0))@V.conj().T
def score(logs):
 A=np.diag(np.exp(logs));X=3*np.outer(ph,ph)+np.kron(np.eye(3),A);R=ptr(X,3);B=N(X,3)
 Q=ptr(flog(X)-2*flog(B),3)+flog(R)-np.log(3)*R
 return np.linalg.eigvalsh(Q)[0]
if __name__=='__main__':
 ans=differential_evolution(score,[(-5,5)]*3,seed=382,popsize=6,maxiter=70,tol=1e-8)
 print('minimum reference score',ans.fun,np.exp(ans.x),flush=True);np.savez('qutrit_reset_reference_filter_score_candidate.npz',noise=np.exp(ans.x),score=ans.fun)

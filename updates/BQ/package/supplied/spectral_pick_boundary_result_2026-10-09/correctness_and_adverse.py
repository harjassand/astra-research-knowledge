import numpy as np,json
from pick_inverse import inverse,free_stieltjes,matrices
from scipy.special import softmax
out={}
# Verify analytical forward Jacobian independently against central differences.
k=3;a=np.array([-1.,.2,1.]);p=np.array([.25,.5,.25]);t=.5625
z=np.linspace(-1.4,1.4,8)+.6j
x=np.r_[a,np.log(p[:-1]/p[-1]),t]
def f(x):
 aa=x[:k];pp=softmax(np.r_[x[k:2*k-1],0.]);tt=x[-1]
 return free_stieltjes(z,aa,pp,tt)
g=f(x);den=z[:,None]-t*g[:,None]-a;D=np.sum(p/den**2,axis=1);Q=1-t*D
J=np.column_stack([(p/den**2)/Q[:,None],((1/den)/Q[:,None])@(np.diag(p)-np.outer(p,p))[:,:-1],g*D/Q])
Jfd=np.column_stack([(f(x+np.eye(len(x))[i]*1e-5)-f(x-np.eye(len(x))[i]*1e-5))/(2e-5) for i in range(len(x))])
out['forward_jacobian_fd_max_abs']=float(np.max(abs(J-Jfd)))
# Coincident transform values do not invalidate the strictness theorem.
z=np.array([.5j,2j]);g=np.array([-.4j,-.4j]);r=inverse(z,g)
out['coincident_g']={key:val.tolist() if isinstance(val,np.ndarray) else val for key,val in r.items()}
# Local boundary slope, compared directly with finite differences.
z=np.linspace(-1.4,1.4,3)+.6j;g=free_stieltjes(z,a,p,t);_,K,S,_=matrices(z,g,t);ev,U=np.linalg.eigh(S);v=U[:,0]
c=float(np.real(v.conj()@(K*K)@v));d=1e-6
slope=(np.linalg.eigvalsh(matrices(z,g,t+d)[2])[0]-np.linalg.eigvalsh(matrices(z,g,t-d)[2])[0])/(2*d)
w=z-t*g;fp=np.sum(v.conj()[:,None]/(w[:,None]-a)**2,axis=0)
cexact=float(np.sum(p**2*abs(fp)**2))
out['boundary_slope']={'minus_derivative':c,'finite_difference':float(slope),'atomic_formula':cexact,'next_eigenvalue':float(ev[1])}
# Deliberately close atoms: routine double precision has no uniform guarantee.
ad=[]
for sep in [.5,.1,.01,.001]:
 aa=np.array([-sep,0,sep]);pp=np.ones(3)/3;gg=free_stieltjes(z,aa,pp,t)
 try:
  r=inverse(z,gg)
  ad.append({'separation':sep,'variance_error':abs(r['variance']-t),'atoms':r['atoms'].tolist(),'weights':r['weights'].tolist(),'K_condition':float(r['K_eigenvalues'][-1]/r['K_eigenvalues'][0])})
 except Exception as exc:ad.append({'separation':sep,'failure':str(exc)})
out['close_atom_adverse']=ad
# Over-specifying model order generally returns a different interpolant under finite N.
raw=np.load('finite_matrix_raw.npz');cc=raw['N1024_k3_v0.5625_r0_eigenvalues'];mid=(min(cc)+max(cc))/2;half=(max(cc)-min(cc))/2
rr=[]
for m in [2,3,4,5,8]:
 zz=mid+.8*half*np.linspace(-1,1,m)+.3j*half;gg=np.mean(1/(zz[:,None]-cc),axis=1)
 try:
  r=inverse(zz,gg);rr.append({'assumed_atoms':m,'variance':r['variance'],'K_condition':float(r['K_eigenvalues'][-1]/r['K_eigenvalues'][0]),'atoms':r['atoms'].tolist()})
 except Exception as exc:rr.append({'assumed_atoms':m,'failure':str(exc)})
out['model_order_sensitivity']=rr
try:inverse(np.array([-1+1j,1+1j]),np.array([-2j,-2j]));out['invalid_data_rejected']=False
except ValueError as exc:out['invalid_data_rejected']=str(exc)
json.dump(out,open('correctness_and_adverse_results.json','w'),indent=2)
print(json.dumps(out,indent=2))

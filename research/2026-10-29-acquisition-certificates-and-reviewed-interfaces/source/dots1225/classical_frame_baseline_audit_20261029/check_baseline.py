import numpy as np,json,hashlib
from pathlib import Path
rng=np.random.default_rng(20261029)
def rotation():
 q,_=np.linalg.qr(rng.normal(size=(3,3)));q[:,0]*=np.linalg.det(q);return q
def infer(S):
 _,V=np.linalg.eigh(S);v=V[:,0];A=np.sqrt(3)*v.reshape(3,3)
 if np.linalg.det(A)<0:A=-A
 u,s,vh=np.linalg.svd(A);return u@np.diag([1,1,np.linalg.det(u@vh)])@vh
def error(R,H):return np.linalg.norm(R-H,'fro')/(2*np.sqrt(2))
eta=.2;alpha=1/(8+eta);g=(1-eta)/(8+eta);eps=.2;delta=.01
e=g*eps/(18*np.sqrt(3));m=int(np.ceil(np.log(90/delta)/(2*e*e)))
maxerr=maxratio=maxentry=0.;bad=0
for trial in range(300):
 R=rotation();c=R.ravel()/np.sqrt(3);S=alpha*np.eye(9)-g*np.outer(c,c);Sh=np.zeros((9,9))
 for i in range(9):Sh[i,i]=rng.binomial(m,S[i,i])/m
 for i in range(9):
  for j in range(i):
   pplus=(S[i,i]+S[j,j]+2*S[i,j])/2;pminus=(S[i,i]+S[j,j]-2*S[i,j])/2
   cnt=rng.multinomial(m,[pplus,pminus,1-pplus-pminus]);Sh[i,j]=Sh[j,i]=(cnt[0]-cnt[1])/(2*m)
 E=np.linalg.norm(Sh-S,2);err=error(R,infer(Sh));maxerr=max(maxerr,err);maxentry=max(maxentry,np.max(np.abs(Sh-S)))
 maxratio=max(maxratio,err/(2*np.sqrt(3)*E/g));bad+=err>eps
 assert err<=2*np.sqrt(3)*E/g+1e-12
# deliberately non-tomographic, adversarial bounded symmetric matrix perturbations
admax=0.
for trial in range(1000):
 R=rotation();c=R.ravel()/np.sqrt(3);S=alpha*np.eye(9)-g*np.outer(c,c)
 D=rng.normal(size=(9,9));D=(D+D.T)/2;D*=rng.uniform(.001,.14)*g/np.linalg.norm(D,2)
 E=np.linalg.norm(D,2);err=error(R,infer(S+D));admax=max(admax,err/(2*np.sqrt(3)*E/g));assert err<=2*np.sqrt(3)*E/g+1e-12
out=dict(seed=20261029,eta=eta,g=g,epsilon=eps,delta=delta,records_per_setting=m,total_records=45*m,measurement_trials=300,observed_failures=int(bad),max_gate_halfdiamond=maxerr,max_entry_error=maxentry,entry_threshold=e,max_bound_ratio=maxratio,adversarial_trials=1000,adversarial_max_bound_ratio=admax,scope='Floating diagnostics; synthetic IID promised states, no acquisition or hardware execution. Exact proof is separate.')
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

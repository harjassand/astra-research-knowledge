import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(91220261029)
rows=[]
for eta in [0.,.2,.8]:
 g=(1-eta)/(8+eta);S=np.eye(9)/(8+eta)-g*np.outer(np.eye(3).ravel(),np.eye(3).ravel())/3
 for seedtrial in range(10):
  total=0;passed=False
  for l in range(1,41):
   m=2**l;total+=45*m;deltal=.01/(l*(l+1));e=np.sqrt(np.log(90/deltal)/(2*m));E=9*e;Sh=np.zeros((9,9))
   for i in range(9):Sh[i,i]=rng.binomial(m,S[i,i])/m
   for i in range(9):
    for j in range(i):
     pp=(S[i,i]+S[j,j]+2*S[i,j])/2;pm=(S[i,i]+S[j,j]-2*S[i,j])/2
     cnt=rng.multinomial(m,[pp,pm,1-pp-pm]);Sh[i,j]=Sh[j,i]=(cnt[0]-cnt[1])/(2*m)
   vals,V=np.linalg.eigh(Sh);gl=max(0.,vals[1]-vals[0]-2*E)
   if gl>0 and 2*np.sqrt(3)*E/gl<=.2:
    A=np.sqrt(3)*V[:,0].reshape(3,3)
    if np.linalg.det(A)<0:A=-A
    u,s,vh=np.linalg.svd(A);R=u@np.diag([1,1,np.linalg.det(u@vh)])@vh
    err=np.linalg.norm(R-np.eye(3),'fro')/(2*np.sqrt(2));passed=True
    assert err<=.2 and gl<=g and np.linalg.norm(Sh-S,2)<=E
    rows.append(dict(eta=eta,trial=seedtrial,stage=l,total_records=total,g_lower=gl,true_gap=g,gate_error=err));break
  if not passed:rows.append(dict(eta=eta,trial=seedtrial,aborted=True,total_records=total))
Path(__file__).with_name('ADAPTIVE_CHECKS.json').write_text(json.dumps({'scope':'Synthetic floating diagnostic, not certified eigensolver or source experiment. Finite cap 40 stages.','rows':rows},indent=2)+'\n')
print([(eta,max(r['stage'] for r in rows if r['eta']==eta),max(r['gate_error'] for r in rows if r['eta']==eta)) for eta in [0.,.2,.8]])

from pathlib import Path
import numpy as np,json
OUT=Path(__file__).parent
rng=np.random.default_rng(20261027)
def fg(A):
 a,b,c,d=A.T;u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c;F=u*u+v*v+3*w*w+16*q*q+4*q*(u-v);fu=2*u+4*q;fv=2*v-4*q;fw=6*w;fq=32*q+4*(u-v)
 grad=np.stack((2*fu*a+fw*b+fq*d,2*fv*b+fw*a-fq*c,2*fu*c+fw*d-fq*b,2*fv*d+fw*c+fq*a),axis=-1)
 return F,grad
Bs=[np.array([1.,0,0,1]),np.array([1.,0,0,0]),np.array([1.,0,0,-1])]+[rng.normal(size=4) for _ in range(60)]
records=[]
for i,B in enumerate(Bs):
 B=B/np.linalg.norm(B);X=rng.normal(size=(200000,4));X*=rng.choice([.1,.3,.6,1,2,4],size=(len(X),1));A=X+B
 FB,gB=fg(B.reshape(1,4));FA,_=fg(A);detX=X[:,0]*X[:,3]-X[:,1]*X[:,2];ratio=(FA-FB-X@gB[0])/detX
 lo=int(np.where(detX< -1e-8,ratio,-np.inf).argmax());hi=int(np.where(detX>1e-8,ratio,np.inf).argmin())
 rec={'B':B.tolist(),'lower':float(ratio[lo]),'upper':float(ratio[hi]),'Xlower':X[lo].tolist(),'Xupper':X[hi].tolist(),'index':i,'status':'NUMERICAL_ONLY'};records.append(rec)
 if ratio[lo]>ratio[hi]+1e-4:
  print(json.dumps(rec),flush=True);break
else:print('No sampled support contradiction',flush=True)
(OUT/'polyconvex_results.json').write_text(json.dumps(records,indent=2)+'\n')

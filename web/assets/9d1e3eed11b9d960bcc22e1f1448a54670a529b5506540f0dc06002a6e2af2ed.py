import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import numpy as np
import json,time
st=time.monotonic();rng=np.random.default_rng(600402)
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]);I=np.eye(2)
K=lambda a,b,c:np.kron(np.kron(a,b),c)
err=0;expr_slack=1e9;cases=0
for trial in range(60):
 angle=rng.uniform(0,np.pi);g1=X;g2=np.cos(angle)*X+np.sin(angle)*Y
 def inv():
  v=rng.normal(size=3);v/=np.linalg.norm(v);return v[0]*X+v[1]*Y+v[2]*Z
 b1,b2,c1,c2=[inv() for _ in range(4)]
 GG1=K(g1,I,I);GG2=K(g2,I,I);B1=K(I,b1,I);B2=K(I,b2,I);C1=K(I,I,c1);C2=K(I,I,c2)
 p=(GG1@GG2+GG2@GG1)/2;f=1j*(GG1@GG2-GG2@GG1)/2
 R=B1-C1;S=B2-C2;M=R+1j*f@S
 H=GG1@(B1+C1)+GG2@(B2+C2)
 zz=B1@B2+B2@B1+C1@C2+C2@C1+2*B1@C2+2*B2@C1
 rhs=8*np.eye(8)-p@p@S@S+p@zz
 err=max(err,float(np.max(np.abs(H@H+M.conj().T@M-rhs))))
 w=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));w=w@w.conj().T;w/=np.trace(w)
 sig=np.trace(w.reshape(2,4,2,4),axis1=1,axis2=3)
 ant=g1@g2+g2@g1;eps=np.sqrt(np.trace(sig@ant@ant).real)
 score=np.trace(w@H).real;slack=2*np.sqrt(2+eps)-score
 assert slack>-1e-10;expr_slack=min(expr_slack,slack);cases+=1
records=[]
for t in [0,.2,.4,.6,.8]:
 sig=(I+t*Z)/2;root=np.diag(np.sqrt(np.diag(sig)))
 for angle in [np.pi/2,np.pi/2+.1,np.pi/2+.3]:
  gg=[X,np.cos(angle)*X+np.sin(angle)*Y];a=.5
  q=sum(np.trace(root@g@root@g).real for g in gg)/2
  ant=gg[0]@gg[1]+gg[1]@gg[0];eps=np.sqrt(np.trace(sig@ant@ant).real)
  lower=a/4*max(0,2*q-np.sqrt(2+eps))
  z=rng.normal(size=(4,2))+1j*rng.normal(size=(4,2));v,_=np.linalg.qr(z)
  def joint(rho):
   j=v@rho@v.conj().T;swap=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
   return (j+swap@j@swap)/2
  def marginal(j):return np.trace(j.reshape(2,2,2,2),axis1=1,axis2=3)
  b=0
  for g in gg:
   for sign in [-1,1]:
    rho=root@(I+sign*a*g)@root
    out=marginal(joint(rho));b=max(b,np.linalg.svd(out-rho,compute_uv=False).sum()/2)
  assert b+1e-10>=lower
  assert abs(q-np.sqrt(1-t*t))<1e-10
  records.append({'reference_bloch_t':t,'angle':angle,'Q':float(q),'E':float(eps),'proved_lower':float(lower),'actual_random_broadcaster_error':float(b)})
result={'status':'PASS_DIAGNOSTIC_ONLY','random_exact_SOS_fixtures':cases,'SOS_max_entry_residual':err,'minimum_expectation_bound_slack':expr_slack,'actual_channel_fixtures':records,'wall_seconds':time.monotonic()-st,'scope':'Transcription of symbolic identity and weighted transfer, not universal rounding or growing-dimensional separation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='actual_channel_fixtures'},indent=2))

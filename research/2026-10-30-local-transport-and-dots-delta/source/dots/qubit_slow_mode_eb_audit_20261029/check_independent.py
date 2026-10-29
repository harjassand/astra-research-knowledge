import numpy as np,json
from scipy.linalg import expm
from pathlib import Path
rng=np.random.default_rng(39194)
I=np.eye(2);ss=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
S=np.array([[1,0,0],[0,1/np.sqrt(2),0],[0,1/np.sqrt(2),0],[0,0,1]],complex)
def bloch(v):return np.einsum('a,aij->ij',v,ss)
def mapop(X,T,t):return (np.trace(X)*(I+bloch(t))+bloch(np.array([np.trace(s@X) for s in ss])@T.T))/2
def choi(T,t):
 out=np.zeros((4,4),complex)
 for a in range(2):
  for b in range(2):
   E=np.zeros((2,2));E[a,b]=1;out[2*a:2*a+2,2*b:2*b+2]=mapop(E,T,t)/2
 return out
cases=[]
# Exactly self-compatible channels from symmetric broadcast isometries.
for j in range(220):
 if j<140:
  scale=10**rng.uniform(-4,-.7);H=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));H=(H+H.conj().T)/2
  Q=expm(1j*scale*H)[:,[0,2]];V=S@Q
 else:
  Q=np.linalg.qr(rng.normal(size=(3,2))+1j*rng.normal(size=(3,2)))[0];V=S@Q
 ks=[V.reshape(2,2,2)[:,b,:] for b in range(2)]
 ch=lambda X:sum(k@X@k.conj().T for k in ks)
 T=np.array([[np.trace(a@ch(b)).real/2 for b in ss] for a in ss]);t=np.array([np.trace(a@ch(I/2)).real for a in ss]);cases.append(('symmetric_broadcast',T,t,None))
# Classical channels with extremely biased endpoint stationary states.
for j in range(220):
 ap=10**rng.uniform(-7,-1.2);am=10**rng.uniform(-7,-1.2)
 rp=np.array([np.sin(ap),0,np.cos(ap)]);rm=np.array([0,np.sin(am),-np.cos(am)])
 if j%4==0:rp=np.array([0.,0.,1.]);ap=0.
 T=np.zeros((3,3));T[:,2]=(rp-rm)/2;t=(rp+rm)/2;zz=(np.sin(am/2)**2-np.sin(ap/2)**2)/(np.sin(am/2)**2+np.sin(ap/2)**2);fixed=t+T[:,2]*zz;fixed[2]=zz;cases.append(('biased_classical',T,t,fixed))
# Complex spectrum and exact lambda=1 endpoint fixtures.
for angle in [.2,1.,2.3]:
 R=np.array([[np.cos(angle),-np.sin(angle),0],[np.sin(angle),np.cos(angle),0],[0,0,1]])
 cases.append(('complex_depolarizing',.5*R,np.zeros(3),None))
cases.append(('exact_dephasing',np.diag([0.,0.,1.]),np.zeros(3),None))
cases.extend([('defective_far',np.array([[.2,.1,0],[0,.2,0],[0,0,.1]]),np.zeros(3),None),('negative_unit',np.diag([0.,0.,-1.]),np.zeros(3),None),('threshold_near',np.diag([0.,0.,.99]),np.zeros(3),None),('threshold_far',np.diag([0.,0.,.9899]),np.zeros(3),None)])
reference_cases=0;reference_residual=0.
res={'factorization':0.,'all_operator_identity':0.,'stationarity':0.,'endpoint_excess':0.,'compatibility_excess':0.};counts={'near':0,'far':0,'complex':0};largestL=0.;maxs=0.;near_pure=0
for family,T,t,known_s in cases:
 singular=np.linalg.svd(T,compute_uv=False);res['compatibility_excess']=max(res['compatibility_excess'],float(max(0,singular[0]**2+singular[1]**2-1)))
 ev=np.linalg.eigvals(T)
 counts['complex']+=int(np.any(abs(ev.imag)>1e-8))
 if family=='exact_dephasing':s=np.array([0.,0.,.9])
 elif known_s is not None:s=known_s
 else:s=np.linalg.solve(np.eye(3)-T,t)
 assert np.linalg.norm(s)<=1+1e-7, (family,np.linalg.norm(s),np.linalg.eigvals(T),t)
 near_pure+=int(np.linalg.norm(s)>.999)
 slow=[v.real for v in ev if abs(v.imag)<1e-9 and v.real>=.99]
 if slow:
  counts['near']+=1;lam=max(slow);g=max(0,1-lam)
  ew,ewv=np.linalg.eig(T.T);w=ewv[:,np.argmin(abs(ew-lam))].real;w/=np.linalg.norm(w)
  axis=np.eye(3)[np.argmin(abs(w))];u2=axis-w*(w@axis);u2/=np.linalg.norm(u2);u3=np.cross(w,u2);O=np.column_stack([w,u2,u3])
  TT=O.T@T@O;a=TT[1:,0];B=TT[1:,1:];h=np.linalg.solve(lam*np.eye(2)-B,a);n=O@np.r_[1,h];k=1-16*g
  TF=k*np.outer(n,w);tf=s-TF@s
  rp=s+k*(1-w@s)*n;rm=s+k*(-1-w@s)*n
  res['endpoint_excess']=max(res['endpoint_excess'],max(0,np.linalg.norm(rp)-1,np.linalg.norm(rm)-1))
  assert max(np.linalg.norm(rp),np.linalg.norm(rm))<=1+1e-7
  D=np.linalg.inv(np.eye(2)-B);LM=np.zeros((3,3));LM[0,0]=16;LM[1:,0]=(16*np.eye(2)-D)@h;LM[1:,1:]=D;L=O@LM@O.T
  assert np.linalg.norm(L,2)<24+1e-9
 else:
  counts['far']+=1;TF=np.zeros((3,3));tf=s;L=np.linalg.inv(np.eye(3)-T)
  assert np.linalg.norm(L,2)<=6400+1e-6
 largestL=max(largestL,3*np.linalg.norm(L,2));maxs=max(maxs,np.linalg.norm(s))
 if reference_cases<80 or family in ['defective_far','negative_unit','threshold_near','threshold_far']:
  r=2+reference_cases%2;z=rng.normal(size=(2*r,2*r))+1j*rng.normal(size=(2*r,2*r));rho=z@z.conj().T;rho/=np.trace(rho)
  def apply_ref(M,translation,X):
   Y=np.zeros_like(X).reshape(2,r,2,r);XX=X.reshape(2,r,2,r)
   for c in range(r):
    for d in range(r):Y[:,c,:,d]=mapop(XX[:,c,:,d],M,translation)
   return Y.reshape(2*r,2*r)
  defect=rho-apply_ref(T,t,rho);target=rho-apply_ref(TF,tf,rho)
  # mapop includes the identity component; defect has zero partial A trace, so it equals L here.
  composed=apply_ref(L,np.zeros(3),defect)
  reference_residual=max(reference_residual,float(np.linalg.norm(target-composed)))
  assert np.linalg.norm(target,ord='nuc')<=3*np.linalg.norm(L,2)*np.linalg.norm(defect,ord='nuc')+1e-9
  reference_cases+=1
 res['factorization']=max(res['factorization'],float(np.linalg.norm(np.eye(3)-TF-L@(np.eye(3)-T))))
 res['stationarity']=max(res['stationarity'],float(np.linalg.norm(TF@s+tf-s)))
 J=choi(TF,tf);Jpt=J.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
 assert np.linalg.eigvalsh(J).min()>-1e-7 and np.linalg.eigvalsh(Jpt).min()>-1e-7
 # Full-operator identity includes nonunital identity input, not merely traceless Pauli inputs.
 for X in [I,*ss]:
  deficit=X-mapop(X,T,t);LX=bloch(L@np.array([np.trace(a@deficit) for a in ss]))/2
  res['all_operator_identity']=max(res['all_operator_identity'],float(np.linalg.norm(X-mapop(X,TF,tf)-LX)))
assert max(res.values())<1e-6
out={'reference_cases':reference_cases,'reference_factorization_residual':reference_residual,'channel_cases':len(cases),'regimes':counts,'near_pure_fixed_states':near_pure,'max_stationary_bloch_norm':float(maxs),'largest_observed_3_operator_norm_L':float(largestL),'residuals':res,'scope':'Independent physical self-compatible channels and complete linear-map identities, not universal proof or hardware'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

"""Search for a universal completely positive lift of four acoustic 2x2 blocks.
Exploration only; failures are not impossibility proofs."""
import numpy as np,sympy as sp,scipy.linalg as la,pickle,itertools,os,time
BASE=os.path.dirname(__file__)
with open(BASE+'/c4_heat_symbolic.pkl','rb') as f:z=pickle.load(f)
C=z['C'];pr=C.T.rref()[1];C=np.array(C[list(pr),:]).astype(float);P=z['P'];EA=np.array((P*z['EA'])[list(pr),:]).astype(float);EM=np.array((P*z['EM'])[list(pr),:]).astype(float).ravel()
# seven a,c,e,L,k,h,l params.
pars=sp.symbols('a c e L k h l');a,c,e,L,k,h,l=pars
Q=[sp.Matrix([[6*a+c+e+k/2,h/2-2*L],[h/2-2*L,c-e/2+l/2]]),
sp.Matrix([[k/2,-h/2],[-h/2,2*a+e/2+l/2]]),
sp.Matrix([[6*a-c-e-k/2,L+h/2],[L+h/2,c+e/2-l/2]]),
sp.Matrix([[2*c+2*e-k/2,-L-h/2],[-L-h/2,2*a-e/2-l/2]])]
Qc=np.array([[[[float(sp.diff(q[i,j],v)) for j in range(2)] for i in range(2)] for v in pars] for q in Q])
ij6=list(itertools.combinations_with_replacement(range(6),2))
blocks=[12]*4+[2]*4
ij=[list(itertools.combinations_with_replacement(range(n),2)) for n in blocks];offset=np.r_[0,np.cumsum([len(v) for v in ij])]
def unpack(x):
 mats=[]
 for n,inds,l,r in zip(blocks,ij,offset[:-1],offset[1:]):
  G=np.zeros((n,n))
  for val,(i,j) in zip(x[l:r],inds):G[i,j]=G[j,i]=val/(1 if i==j else np.sqrt(2))
  mats.append(G)
 return mats
cols=[]
for b,n in enumerate(blocks):
 for i,j in ij[b]:
  G=np.zeros((n,n));G[i,j]=G[j,i]=1 if i==j else 1/np.sqrt(2)
  out=[]
  for p in range(7):
   if b<4:
    S=np.einsum('kilj,ij->kl',G.reshape(6,2,6,2),Qc[b,p])
    res=C@np.array([S[k,l] for k,l in ij6])
   else:res=EM*np.sum(G*Qc[b-4,p])
   out.extend(res)
  cols.append(out)
A=np.array(cols).T;b=np.column_stack((EA,np.zeros((len(pr),3)))).T.ravel()
U,s,R=la.svd(A,full_matrices=False);rank=(s>1e-9).sum();U=U[:,:rank];s=s[:rank];R=R[:rank];x0=R.T@((U.T@b)/s)
print('sizes',A.shape,'rank',rank,'consistency',la.norm(b-U@(U.T@b)),flush=True)
def proj_aff(g):return g+x0-R.T@(R@g)
def psd(g):
 out=[]
 for mat,inds in zip(unpack(g),ij):
  w,V=la.eigh(mat,check_finite=False);Y=(V*np.maximum(w,0))@V.T
  out.extend([Y[i,j]*(1 if i==j else np.sqrt(2)) for i,j in inds])
 return np.array(out)
x=x0.copy();t=time.time()
for k in range(20000):
 y=psd(x);v=proj_aff(2*y-x);x+=v-y
 if k%500==0 or k==19999:
  zz=proj_aff(y);err=la.norm(zz-y);ev=min(la.eigvalsh(G)[0] for G in unpack(zz));print(k,err,ev,flush=True)
  if err<1e-9:break
np.savez(BASE+'/c4_universal_lift.npz',x=zz,A=A,b=b,blocks=blocks,res=err)
print('time',time.time()-t)

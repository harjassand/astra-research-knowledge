"""Numerical search for a universal positive lift. Not a proof."""
import numpy as np,sympy as sp,scipy.linalg as la,pickle,itertools,os,time
BASE=os.path.dirname(__file__)
with open(BASE+'/c4_spin2.pkl','rb') as f:z=pickle.load(f)
C=z['C'];pr=C.T.rref()[1];C=np.array(C[list(pr),:]).astype(float);P=z['P'];EA=np.array((P*z['EA'])[list(pr),:]).astype(float);EM=np.array((P*z['EM'])[list(pr),:]).astype(float).ravel()
pars=sp.symbols('a c e L k h l');a,c,e,L,k,h,l=pars
Q=[sp.Matrix([[6*a+c+e+k/2,h/2-2*L],[h/2-2*L,c-e/2+l/2]]),sp.Matrix([[k/2,-h/2],[-h/2,2*a+e/2+l/2]]),sp.Matrix([[6*a-c-e-k/2,L+h/2],[L+h/2,c+e/2-l/2]]),sp.Matrix([[2*c+2*e-k/2,-L-h/2],[-L-h/2,2*a-e/2-l/2]])]
Qc=np.array([[[[float(sp.diff(q[i,j],v)) for j in range(2)] for i in range(2)] for v in pars] for q in Q])
target_sizes=[6,3,3,1];target_offsets=[0,21,27,33];Cs=[C[:,:21],C[:,21:27],C[:,27:33],EM[:,None]]
blocks=[2*n for b in range(4) for n in target_sizes];ij=[list(itertools.combinations_with_replacement(range(n),2)) for n in blocks];offset=np.r_[0,np.cumsum([len(v) for v in ij])];inds=[np.array(v).T for v in ij];sfs=[np.where(i==j,1,np.sqrt(2)) for i,j in inds]
def unpack(x):
 mats=[]
 for n,(i,j),sf,l,r in zip(blocks,inds,sfs,offset[:-1],offset[1:]):
  G=np.zeros((n,n));G[i,j]=x[l:r]/sf;G[j,i]=x[l:r]/sf;mats.append(G)
 return mats
cols=[]
for b,n in enumerate(blocks):
 input_index=b//4;target_index=b%4;nt=target_sizes[target_index];ijtar=list(itertools.combinations_with_replacement(range(nt),2))
 for i,j in ij[b]:
  G=np.zeros((n,n));G[i,j]=G[j,i]=1 if i==j else 1/np.sqrt(2)
  out=[]
  for p in range(7):
   S=np.einsum('kilj,ij->kl',G.reshape(nt,2,nt,2),Qc[input_index,p]);res=Cs[target_index]@np.array([S[k,l] for k,l in ijtar]);out.extend(res)
  cols.append(out)
A=np.array(cols).T;b=np.column_stack((EA,np.zeros((len(pr),3)))).T.ravel();U,s,R=la.svd(A,full_matrices=False);rank=(s>1e-9).sum();U=U[:,:rank];s=s[:rank];R=R[:rank];x0=R.T@((U.T@b)/s)
print('sizes',A.shape,'rank',rank,'consistency',la.norm(b-U@(U.T@b)),flush=True)
def aff(g):return g+x0-R.T@(R@g)
def psd(g):
 out=[]
 for mat,(i,j),sf in zip(unpack(g),inds,sfs):
  w,V=la.eigh(mat,check_finite=False);Y=(V*np.maximum(w,0))@V.T;out.extend(Y[i,j]*sf)
 return np.array(out)
x=x0.copy();t=time.time()
for k in range(20000):
 y=psd(x);v=aff(2*y-x);x+=v-y
 if k%1000==0 or k==19999:
  zz=aff(y);err=la.norm(zz-y);ev=min(la.eigvalsh(G)[0] for G in unpack(zz));print(k,err,ev,flush=True)
  if err<1e-9:break
np.savez(BASE+'/c4_spin_universal.npz',x=zz,A=A,b=b,blocks=blocks,res=err)
print('time',time.time()-t)

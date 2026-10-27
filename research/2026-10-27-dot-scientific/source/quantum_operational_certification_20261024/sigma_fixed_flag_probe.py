import numpy as np, json
rng=np.random.default_rng(261026)
def ptr(A,d):return np.einsum('ar as->rs',A.reshape(3,d,3,d)) if False else np.trace(A.reshape(3,d,3,d),axis1=0,axis2=2)
def N(A,d):return (np.kron(np.eye(3),ptr(A,d))-A.reshape(3,d,3,d).transpose(2,1,0,3).reshape(3*d,3*d))/2
def metric(A,H):
 w,u=np.linalg.eigh(A); z=u.conj().T@H@u; mask=w>1e-12;w=w[mask];z=z[np.ix_(mask,mask)]; x=w[:,None];y=w[None,:]; v=np.log(x)-np.log(y); dif=x-y
 L=np.divide(v,dif,out=1/((x+y)/2),where=abs(dif)>1e-12)
 return np.sum(abs(z)**2*L).real
def build(s,f,p):
 k=len(s);d=len(f);K=np.zeros((3*d,k),complex)
 for a in range(3):
  for l in range(k):K[a*d+a*k+l,l]=1/np.sqrt(3)
 return p*K@s@K.conj().T+(1-p)*np.kron(np.eye(3)/3,np.outer(f,f.conj())),K
best=(-1e10,None)
for j in range(500):
 k=2 if j<350 else 3;d=3*k+1
 z=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k));s=z@z.conj().T;s/=np.trace(s)
 f=rng.normal(size=d)+1j*rng.normal(size=d);f/=np.linalg.norm(f);p=rng.uniform(.02,.98)
 z=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k));h=z+z.conj().T;h-=np.trace(h)*np.eye(k)/k;h/=np.linalg.norm(h)
 A,K=build(s,f,p);H=p*K@h@K.conj().T;O=N(A,d);R=ptr(A,d)
 hs=metric(A,H)+metric(R,ptr(H,d))-2*metric(O,N(H,d))
 if hs>best[0]:
  best=(hs,j);np.savez('sigma_fixed_flag_best.npz',sigma=s,flag=f,p=p,h=h,hessian=hs)
 if hs>1e-6:print('POSITIVE',j,hs,flush=True);break
print('best',best)

import numpy as np,json

def basis(d):
 out=[np.eye(d,dtype=complex)]
 for a in range(d):
  for b in range(a+1,d):
   x=np.zeros((d,d),complex);x[a,b]=x[b,a]=np.sqrt(d/2);out.append(x)
   y=np.zeros((d,d),complex);y[a,b]=-1j*np.sqrt(d/2);y[b,a]=1j*np.sqrt(d/2);out.append(y)
 for k in range(1,d):
  z=np.zeros(d);z[:k]=1;z[k]=-k
  out.append(np.diag(z)*np.sqrt(d/(k*(k+1))))
 return out

def weyl(d):
 X=np.roll(np.eye(d),1,axis=0);Z=np.diag(np.exp(2j*np.pi*np.arange(d)/d))
 return [np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b) for a in range(d) for b in range(d)]

def ad(U):return np.kron(U.conj(),U)

reports=[]
for da,db in [(2,2),(2,3),(3,3)]:
 D=da*db;I=np.eye(D);ident=np.eye(D*D)
 vec=I.reshape(-1,order='F');Dep=np.outer(vec,vec)/D
 Fs=[np.kron(A,B) for A in basis(da) for B in basis(db)]
 diss=np.zeros((D*D,D*D),complex)
 for F in Fs[1:]:
  F2=F@F;diss+=ad(F)-.5*(np.kron(I,F2)+np.kron(F2.T,I))
 twirl=sum(ad(np.kron(U,V)) for U in weyl(da) for V in weyl(db))/(D*D)
 reports.append({'dimensions':[da,db],'real_channels':len(Fs)-1,'dissipator_identity_max_error':float(np.max(abs(diss-D*D*(Dep-ident)))),'product_weyl_identity_max_error':float(np.max(abs(twirl-Dep)))})
assert all(r['dissipator_identity_max_error']<1e-10 and r['product_weyl_identity_max_error']<1e-12 for r in reports)
print(json.dumps(reports,indent=2))

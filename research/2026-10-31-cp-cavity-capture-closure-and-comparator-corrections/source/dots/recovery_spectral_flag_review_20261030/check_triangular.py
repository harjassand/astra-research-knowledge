import numpy as np, scipy.linalg as la, json
rng=np.random.default_rng(30102026); n=4; masks=range(4)
a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)); H=(a+a.conj().T)/5
A=(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))/5
I=np.eye(n); ps={d:np.diag([float((x & (3^d))==0) for x in masks]) for d in masks}
def L(x):return -1j*(H@x-x@H)+A@x@A.conj().T-(A.conj().T@A@x+x@A.conj().T@A)/2
def mat(fn):
 out=[]
 for j in range(16):
  x=np.zeros((4,4),complex);x.flat[j]=1;out.append(fn(x).reshape(-1))
 return np.array(out).T
B=np.zeros((64,64),complex)
for d in masks:
 p=ps[d];B[d*16:(d+1)*16,d*16:(d+1)*16]=mat(lambda x,p=p:p@L(p@x@p)@p)
 r=3^d
 for j in masks:
  if not j or j&r!=j:continue
  def gamma(x,j=j,r=r,p=p):
   lx=L(p@x@p);out=np.zeros((4,4),complex)
   for alpha in masks:
    if alpha&r!=alpha:continue
    ea=np.diag([float((v&r)==alpha) for v in masks])
    for beta in masks:
     if beta&r!=beta or alpha|beta!=j:continue
     eb=np.diag([float((v&r)==beta) for v in masks]);out+=ea@lx@eb
   return out
  B[(d|j)*16:((d|j)+1)*16,d*16:(d+1)*16]=mat(gamma)
x=np.zeros(64,complex);x[0]=1
v=(la.expm(.7*B)@x).reshape(4,4,4)
actual=(la.expm(.7*mat(L))@x[:16]).reshape(4,4)
result={'sum_error':float(la.norm(v.sum(axis=0)-actual)), 'corner_error':max(float(la.norm(v[d]-ps[d]@v[d]@ps[d])) for d in masks),'flag_min_eigenvalues':[float(la.eigvalsh((y+y.conj().T)/2).min()) for y in v]}
assert result['sum_error']<1e-12 and result['corner_error']<1e-12

p=np.diag([float((v&1)==0) for v in masks])
k=mat(lambda x:p@L(p@x@p)@p)
g=mat(lambda x:L(p@x@p)-p@L(p@x@p)@p)
coarse=np.block([[k,np.zeros((16,16))],[g,mat(L)]])
xc=np.zeros(32,complex);xc[0]=1
vc=(la.expm(.7*coarse)@xc).reshape(2,4,4)
coarsening_error=max(la.norm(vc[0]-v[0]-v[2]),la.norm(vc[1]-v[1]-v[3]))
assert coarsening_error<1e-12
result['coarsening_error']=float(coarsening_error)
print(json.dumps(result,indent=2))

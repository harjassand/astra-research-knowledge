import numpy as np,json
from itertools import product
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]).astype(complex); Y=1j*X@Z
P={'I':I,'X':X,'Y':Y,'Z':Z}
def kron(*xs):
    a=np.array([[1]],complex)
    for x in xs:a=np.kron(a,x)
    return a
def word(s):return kron(*(P[c] for c in s))
n=5; pp=np.eye(32,dtype=complex)
for s in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']:pp=pp@(np.eye(32)+word(s))/2
z=word('ZZZZZ');p0=pp@(np.eye(32)+z)/2
v=p0[:,0];v/=np.linalg.norm(v);v1=word('XXXXX')@v;enc=np.column_stack([v,v1])
errs=[np.eye(32,dtype=complex)]
for i in range(n):
    for p in [X,Y,Z]:errs.append(kron(*(p if j==i else I for j in range(n))))
frame=np.column_stack([e@enc[:,l] for l in range(2) for e in errs]);dec=frame.conj().T
unitary=float(np.linalg.norm(dec@frame-np.eye(32)))
maxres=0.
for site,a,b in product(range(n),range(2),range(2)):
    m=np.zeros((2,2),complex);m[a,b]=1
    e=kron(*(m if j==site else I for j in range(n)))
    actual=dec@e@enc;w=actual[:16,0]
    expected=np.zeros((32,2),complex);expected[:16,0]=w;expected[16:,1]=w
    maxres=max(maxres,float(np.linalg.norm(actual-expected)))
rng=np.random.default_rng(37428)
c=rng.normal(size=(16,16))+1j*rng.normal(size=(16,16)) # deliberately not CP or Hermitian
rho=np.array([[.4,.2+.1j],[.2-.1j,.6]])
physical=sum((c[a,b]*(errs[a]@enc@rho@enc.conj().T@errs[b].conj().T) for a,b in product(range(16),repeat=2)),np.zeros((32,32),complex))
actual=dec@physical@dec.conj().T
res=float(np.linalg.norm(actual-np.kron(rho,c)))
result={'code':'[[5,1,3]] perfect stabilizer code','decoder_unitarity_residual':unitary,'all_20_single_site_matrix_unit_open_factorization_max_residual':maxres,'arbitrary_signed_non_CP_cross_term_tensor_residual':res,'scope':'Exact ideal recovery-cut identity; not an autonomous EC gadget or threshold.'}
assert unitary<1e-12 and maxres<1e-12 and res<1e-11
print(json.dumps(result,indent=2))

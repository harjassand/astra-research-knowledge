import numpy as np,itertools,math,json
from pathlib import Path
rng=np.random.default_rng(202610291104)
def permutation(d,n,p):
 dim=d**n;U=np.zeros((dim,dim),complex)
 for v in itertools.product(range(d),repeat=n):
  a=sum(v[j]*d**(n-1-j) for j in range(n));w=[v[p[j]] for j in range(n)];b=sum(w[j]*d**(n-1-j) for j in range(n));U[b,a]=1
 return U
def anti(d,n):
 out=np.zeros((d**n,d**n),complex)
 for p in itertools.permutations(range(n)):
  sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n));out+=sign*permutation(d,n,p)/math.factorial(n)
 return out
rows=[]
for d,k in [(3,1),(4,2)]:
 n=k+1;dim=d**n;perms=list(itertools.permutations(range(n)));a=len(perms);u=np.ones(a)/math.sqrt(a);e=np.eye(a)[:,0];v=e-u;Prep=np.eye(a)-2*np.outer(v,v)/np.dot(v,v)
 Select=np.zeros((a*dim,a*dim),complex)
 for j,p in enumerate(perms):
  sg=(-1)**sum(p[i]>p[l] for i in range(n) for l in range(i+1,n));Select[j*dim:(j+1)*dim,j*dim:(j+1)*dim]=sg*permutation(d,n,p)
 U=np.kron(Prep.T,np.eye(dim))@Select@np.kron(Prep,np.eye(dim));P=anti(d,n);Ein=np.kron(e.reshape(-1,1),np.eye(dim));Q0=Ein@Ein.conj().T;K0=U.conj().T@Q0@U@Ein;K1=U.conj().T@(np.eye(a*dim)-Q0)@U@Ein
 err0=np.linalg.norm(K0-Ein@P);err1=np.linalg.norm(K1-Ein@(np.eye(dim)-P));assert max(err0,err1)<1e-12
 old=np.kron(anti(d,k),np.eye(d));assert np.linalg.norm(old@P-P)<1e-12
 W=np.eye(d)[:,:d-1];r=d-1;Pk=anti(d,k);emb=W
 for _ in range(k-1):emb=np.kron(emb,W)
 z=rng.normal(size=(r**k,3))+1j*rng.normal(size=(r**k,3));psi=Pk@emb@z;psi/=np.linalg.norm(psi);omega=psi@psi.conj().T
 gamma=np.zeros((d,d),complex)
 for j in range(k):
  arr=omega.reshape([d]*(2*k));perm=[j]+[i for i in range(k) if i!=j]+[k+j]+[k+i for i in range(k) if i!=j];ar=arr.transpose(perm).reshape(d,d**(k-1),d,d**(k-1));gamma+=np.trace(ar,axis1=1,axis2=3)
 eig=np.linalg.eigvalsh(gamma);assert eig.min()>-1e-12 and eig.max()<1+1e-12 and abs(np.trace(gamma)-k)<1e-12
 vals=np.arange(1,r+1,dtype=float);vals/=vals.sum();sigma=W@np.diag(vals)@W.T;rho=np.kron(omega,sigma);actual=np.trace(P@rho).real;formula=(1-np.trace(gamma@sigma).real)/(k+1);lower=(r-k)*vals.min()/(k+1);assert abs(actual-formula)<1e-12 and actual>=lower-1e-12
 fail=(np.eye(dim)-P)@rho@(np.eye(dim)-P);leak=np.trace((np.eye(dim)-old)@fail).real;assert abs(leak)<1e-12
 rows.append(dict(d=d,k=k,luders_success_residual=float(err0),luders_failure_residual=float(err1),growth_probability=float(actual),one_body_formula=float(formula),uniform_lower=float(lower),failure_old_block_leakage=float(leak)))
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(scope='Dense known-control and one-body growth diagnostics; no unknown source inverse or native hardware run',rows=rows),indent=2)+'\n');print(rows)

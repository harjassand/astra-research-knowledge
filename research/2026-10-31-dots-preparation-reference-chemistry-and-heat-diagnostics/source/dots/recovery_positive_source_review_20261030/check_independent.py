import numpy as np, json, itertools
from scipy.linalg import expm
rng=np.random.default_rng(61030)
# Joint system-bath centered HP maps; no positivity assumed for individual terms.
worst=-1.; trials=0
for r in [1,2,3]:
 d=2**r; db=3
 for theta in [.01,.3,1.,3.]:
  f=np.diag(np.exp(theta*np.array([i.bit_count() for i in range(d)])))
  F=np.kron(f,np.eye(db)); inv=np.diag(1/np.sqrt(np.diag(F)))
  for _ in range(20):
   aa=[rng.normal(size=(d*db,d*db))+1j*rng.normal(size=(d*db,d*db)) for j in range(3)]
   aa=[a/np.linalg.norm(a,2) for a in aa]; cc=rng.normal(size=3)
   h=sum(c*a.conj().T@a for c,a in zip(cc,aa))
   raw=sum(c*a.conj().T@F@a for c,a in zip(cc,aa))
   out=raw-(h@F+F@h)/2
   # Rigorous cb upper bound for centered signed dissipator.
   cb=2*sum(abs(cc)); bound=cb*np.exp(r*theta)
   maxev=np.linalg.eigvalsh(inv@out@inv)[-1]
   worst=max(worst,float(maxev/bound)); trials+=1
   assert maxev<=bound+1e-9
# Reset identity and spectral Jensen for arbitrary joint correlated density matrices.
reset_err=0.; jensen_slack=1e100
for theta in [.01,.3,1.,3.]:
 n=3; ds=2**n; db=2
 F=np.kron(np.diag(np.exp(theta*np.array([i.bit_count() for i in range(ds)]))),np.eye(db))
 counts=np.repeat([i.bit_count() for i in range(ds)],db)
 reset=np.zeros_like(F)
 # Adjoint reset takes diagonal input bit to zero.
 diag=np.diag(F)
 for i in range(n):
  new=np.array([diag[((x//db)&~(1<<i))*db+x%db] for x in range(ds*db)])
  reset+=np.diag(new)-F
 exact=-(1-np.exp(-theta))*np.diag(counts)@F
 reset_err=max(reset_err,float(np.linalg.norm(reset-exact)))
 a=rng.normal(size=(ds*db,ds*db))+1j*rng.normal(size=(ds*db,ds*db))
 rho=a@a.conj().T;rho/=np.trace(rho)
 x=np.trace(F@rho).real
 slack=np.trace(F@np.diag(theta*counts)@rho).real-x*np.log(x)
 jensen_slack=min(jensen_slack,slack);assert slack>=-1e-10
# Independent small ATG: common per-record ray, including invalid raw records and fixed MW syndrome decoder.
edges=[(0,2),(1,3),(2,4),(3,5),(6,0),(6,1),(7,4),(7,5)]
boundary=[0,1,4,5];bulk=[2,3,6,7]
def embed(v,ss):return sum(((v>>j)&1)<<i for j,i in enumerate(ss))
def sign(v):return (-1)**v.bit_count()
psi=np.zeros((16,16))
for b,s in itertools.product(range(16),repeat=2):
 for k in range(16):
  x=embed(b,boundary)|embed(k,bulk)
  psi[b,s]+=(-1)**(sum(((x>>i)&1)*((x>>j)&1) for i,j in edges)+(k&s).bit_count())/64
valid=[s for s in range(16) if np.linalg.norm(psi[:,s])>1e-10]
assert 0 in valid
# Derive parity checks, not hard-coded metasyndrome.
checks=[a for a in range(1,16) if all((a&s).bit_count()%2==0 for s in valid)]
def synd(s):return tuple((a&s).bit_count()%2 for a in checks)
beta={}
for f in sorted(range(16),key=lambda f:(f.bit_count(),f)):
 beta.setdefault(synd(f),f)
def pauli(v,x,z):return np.array([sign((b^x)&z)*v[b^x] for b in range(16)])
target=psi[:,0]/np.linalg.norm(psi[:,0]);frames={}
for m in range(16):
 v=psi[:,m^beta[synd(m)]];v=v/np.linalg.norm(v)
 for x,z in itertools.product(range(16),repeat=2):
  out=pauli(v,x,z)
  if abs(abs(np.vdot(target,out))-1)<1e-10:
   frames[m]=(x,z);break
 else:raise AssertionError('No Pauli frame')
max_res=0.;cases=0
for f in range(16):
 ray=None
 for m in range(16):
  v=psi[:,m^f]
  if np.linalg.norm(v)<1e-10:continue
  x,z=frames[m];out=pauli(v/np.linalg.norm(v),x,z)
  if ray is None:ray=out
  max_res=max(max_res,float(np.sqrt(max(0,1-abs(np.vdot(ray,out))**2))));cases+=1
assert max_res<1e-7
print(json.dumps(dict(result='PASS',relative_HP_trials=trials,max_relative_bound_ratio=worst,reset_identity_error=reset_err,min_Jensen_slack=jensen_slack,ATG_valid_records=len(valid),ATG_metacheck_vectors=checks,ATG_common_ray_cases=cases,ATG_common_ray_max_residual=max_res,scope='finite falsification checks, not an asymptotic certificate'),indent=2))

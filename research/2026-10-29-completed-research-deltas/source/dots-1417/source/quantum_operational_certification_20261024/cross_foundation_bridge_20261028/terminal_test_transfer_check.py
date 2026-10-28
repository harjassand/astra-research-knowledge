"""Direct retained-memory checks of the subnormalized terminal-test identity."""
import numpy as np,json,hashlib
from pathlib import Path
rng=np.random.default_rng(281354)
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);six=[(I+s*P)/2 for P in (X,Y,Z) for s in (1,-1)]
def unitary(d):
 q,r=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)));return q
phi=np.array([1,0,0,1])/np.sqrt(2)
worst=0.;cases=0;minbranch=1.
for mem in (2,3,4):
 for t in range(40):
  G=rng.normal(size=(mem,mem))+1j*rng.normal(size=(mem,mem));xi=G@G.conj().T;xi/=np.trace(xi)
  V=unitary(mem)
  weights=rng.uniform(0,1,mem) if t%2 else np.full(mem,1e-9)
  Ks=[V@np.diag(np.sqrt(weights))@V.conj().T,V@np.diag(np.sqrt(1-weights))@V.conj().T]
  branches=[]
  for K in Ks:
   Uh=unitary(mem);xh=Uh@K@xi@K.conj().T@Uh.conj().T
   minbranch=min(minbranch,float(np.trace(xh).real));W=unitary(2*mem);R=unitary(2)
   def action(a,xh=xh,W=W,R=R):
    out=W@np.kron(a,xh)@W.conj().T
    red=np.trace(out.reshape(2,mem,2,mem),axis1=1,axis2=3)
    return R@red@R.conj().T
   branches.append(action)
  def channel(a):return sum(f(a) for f in branches)
  J=np.zeros((4,4),complex)
  for i in range(2):
   for j in range(2):
    e=np.zeros((2,2));e[i,j]=1
    J+=np.kron(e,channel(e))/2
  f=float((phi@J@phi).real)
  mismatch=1-sum(np.trace(p@channel(p)).real for p in six)/6
  worst=max(worst,abs(mismatch-(2/3)*(1-f)))
  assert np.linalg.eigvalsh(J).min()>-1e-12 and abs(np.trace(J)-1)<1e-12
  cases+=1
assert worst<1e-12
p=Path(__file__).parent
out={'cases':cases,'memory_dimensions':[2,3,4],'min_history_probability':minbranch,'max_identity_residual':worst,'kind':'deterministic channel algebra; zero source samples','source_sha256':hashlib.sha256((p/'TERMINAL_TEST_PREDICTIVE_RECOVERY_TRANSFER.md').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'pass':True}
(p/'terminal_test_transfer_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

"""Dense checks are validation only; compiler production path is binary."""
import itertools,json,numpy as np
from algebra_compiler_v1 import compile_algebra,gate_rows,unitary,pauli,basis

def hermitian_paulis(n):
 for bits in itertools.product([0,1],repeat=2*n):
  v=np.array(bits,dtype=np.uint8)
  yield v, (1j**int(np.dot(v[:n],v[n:]))) * pauli(v,n)
def fe_reduced(kraus,dg,dk,gauge=None):
 # mixed-gauge Kraus blocks, or selected pure computational gauge
 return sum(abs(np.trace(K.reshape(dg,dk,dg,dk)[i,:,j,:]))**2
  for K in kraus for i in range(dg) for j in (range(dg) if gauge is None else [gauge]))/(dk*dk*(dg if gauge is None else 1))
def run():
 rng=np.random.default_rng(202610290016); records=[]
 for n,a,b in [(2,0,1),(3,1,0),(3,0,2),(4,1,1)]:
  rows=[]
  for j in range(a):
   for c in [j,n+j]:
    v=np.zeros(2*n,dtype=np.uint8);v[c]=1;rows.append(v)
  for j in range(a,a+b):
   v=np.zeros(2*n,dtype=np.uint8);v[n+j]=1;rows.append(v)
  A=np.array(rows)
  for _ in range(10*n):
   c,t=rng.choice(n,2,replace=False);gate_rows(A,('CX',int(c),int(t)),n)
   gate_rows(A,('H',int(c)),n);gate_rows(A,('S',int(t)),n)
  out=compile_algebra(A,n);U=np.eye(2**n,dtype=complex)
  for g in out['gates']:U=unitary(g,n)@U
  d=2**n;dg=2**(a+b);dk=d//dg
  # Generic coherent CPTP channel via Haar isometry, NOT a Pauli channel.
  z=rng.normal(size=(3*d,d))+1j*rng.normal(size=(3*d,d));q,_=np.linalg.qr(z)
  Ks=[q[i*d:(i+1)*d] for i in range(3)]
  Kc=[U@K@U.conj().T for K in Ks]
  good=0;total=0
  for v,P in hermitian_paulis(n):
   weight=sum(abs(np.trace(P.conj().T@K)/d)**2 for K in Ks);total+=weight
   w=v[None,:].copy()
   for g in out['gates']:gate_rows(w,g,n)
   if not np.any(w[0,a+b:n]) and not np.any(w[0,n+a+b:]):good+=weight
  fe=fe_reduced(Kc,dg,dk)
  records.append(dict(n=n,a=a,b=b,k=n-a-b,total_process_mass=float(total),good_mass=float(good),actual_mixed_gauge_Fe=float(fe),absolute_error=float(abs(fe-good)),tp_error=float(np.linalg.norm(sum(K.conj().T@K for K in Ks)-np.eye(d)))))
 I=np.eye(2);X=np.array([[0,1],[1,0]]);V=np.kron(np.diag([1,0]),X)+np.kron(np.diag([0,1]),I)
 counter=dict(channel='controlled X on gauge=0',good_mass=.5,pure_zero_Fe=float(fe_reduced([V],2,2,0)),mixed_gauge_Fe=float(fe_reduced([V],2,2)))
 print(json.dumps(dict(seed=202610290016,coherent_checks=records,pure_gauge_counterexample=counter),indent=2))
if __name__=='__main__':run()

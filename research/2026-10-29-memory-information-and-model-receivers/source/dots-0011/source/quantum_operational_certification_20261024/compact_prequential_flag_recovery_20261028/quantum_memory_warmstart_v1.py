"""Floating actual retained-quantum-memory proof diagnostic; NOT certified learner."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np,json
from pathlib import Path
from check_compressed_projection_v1 import project
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
pa=[I,X,Y,Z];d=4;r=2;A=16
Ps=[np.kron(a,b) for a in pa for b in pa]
phi=np.eye(d).reshape(-1)/np.sqrt(d);Phi=np.outer(phi,phi.conj())
bells=np.array([np.kron(np.eye(d),p)@phi for p in Ps])
def k3(a,b,c):return np.kron(np.kron(a,b),c)
def exp_pauli(theta,p):return np.cos(theta)*np.eye(p.shape[0])-1j*np.sin(theta)*p
U=np.eye(16,dtype=complex)
for theta,p in [(.47,k3(np.kron(X,I),X,I)),(.63,k3(np.kron(I,Z),Z,I)),(.38,k3(np.kron(Y,X),Y,I)),(.57,k3(np.eye(4),X,X)),(.29,k3(np.eye(4),Y,I))]:U=exp_pauli(theta,p)@U
Uf=np.kron(np.eye(d),U);flag0=np.diag([1.,0.])
def emit(mem):
 rho=Uf@np.kron(np.kron(Phi,mem),flag0)@Uf.conj().T
 # axes R,D,M,G, R',D',M',G'
 rho8=rho.reshape(d,d,2,2,d,d,2,2)
 rdg=np.trace(rho8,axis1=2,axis2=6).reshape(d*d*2,d*d*2)
 blocks=[]
 for v in bells:
  T=np.kron(v[:,None],np.eye(4))
  blocks.append(T.conj().T@rho@T)
 sig=np.array([np.trace(q.reshape(2,2,2,2),axis1=0,axis2=2) for q in blocks])
 return rho,rdg,np.array(blocks),sig

def memory_after(block,W,b):
 E=(I+b*W)/2 if not np.array_equal(W,I) else I
 # Tr_G[(I_M tensor E) block], using E contraction
 return np.einsum('mgnh,hg->mn',block.reshape(2,2,2,2),E)

def resource(rdg,M):
 j=np.zeros((16,16),complex);t=rdg.reshape(16,2,16,2)
 for x,p in enumerate(Ps):
  z=np.einsum('agbh,hg->ab',t,M[x]);C=np.kron(np.eye(d),p)
  j+=C@z@C.conj().T
 return j

def teleport_choi(omega):
 vals,vec=np.linalg.eigh(omega);out=np.zeros((16,16),complex)
 for val,v in zip(vals,vec.T):
  if val<1e-14:continue
  V=v.reshape(d,d)
  for p in Ps:
   K=np.sqrt(val/d)*p.T@V.T@p.conj()
   z=np.kron(np.eye(d),K)@phi
   out+=np.outer(z,z.conj())
 return out

max_grad=0;max_resource=0;max_tele=0;max_norm=0;max_backaction=0
runs=[];records=[]
N=64
for seed in [7301,7302,7303]:
 rng=np.random.default_rng(seed);mem=np.array([[.5,.5],[.5,.5]],complex)
 M=np.zeros((A,2,2),complex);M[0]=I;sumscore=0;sumI=0
 term=int(rng.integers(1,N+1));term_score=None
 # all-probe path, independently sampled T indexes prefix resource; no post-T samples used by terminal consumer
 for t in range(1,N+1):
  rho,rdg,blocks,sig=emit(mem)
  assert np.min(np.linalg.eigvalsh(mem))>-1e-10
  rebuilt=np.zeros_like(sig)
  for x in range(A):
   for W in pa:
    for b in ([1] if np.array_equal(W,I) else [-1,1]):
     p=float(np.trace(memory_after(blocks[x],W,b)).real)/4
     rebuilt[x]+=p*2*b*W
  max_grad=max(max_grad,float(np.max(abs(rebuilt-sig))))
  score=float(np.einsum('xij,xji->',M,sig).real);sumscore+=score;sumI+=float(np.trace(sig[0]).real)
  if t==term or t in [1,N]:
   omega=resource(rdg,M);res=float(np.vdot(phi,omega@phi).real)
   max_resource=max(max_resource,abs(res-score));q=np.array([np.vdot(v,omega@v).real for v in bells])
   expected=sum(p*np.outer(v,v.conj()) for p,v in zip(q,bells))
   actual=teleport_choi(omega)
   max_tele=max(max_tele,float(np.max(abs(actual-expected))))
   if t==term:term_score=res
  probs=np.trace(sig,axis1=1,axis2=2).real;probs=np.maximum(probs,0);probs/=sum(probs)
  x=int(rng.choice(A,p=probs));wi=int(rng.integers(4));W=pa[wi]
  if wi==0:b=1
  else:
   plus=float(np.trace(memory_after(blocks[x],W,1)).real)/probs[x]
   b=1 if rng.random()<min(1,max(0,plus)) else -1
  new=memory_after(blocks[x],W,b);p=float(np.trace(new).real);memnew=new/p
  max_norm=max(max_norm,abs(np.trace(memnew)-1))
  max_backaction=max(max_backaction,float(np.linalg.norm(memnew@mem-mem@memnew)))
  records.append([seed,t,x,wi,b])
  # Learner sees ONLY x,wi,b. mem/rho/sig not supplied to update.
  center=M.copy();center[x]+=(1/(r*np.sqrt(N)))*r*b*W
  M,it=project(center,np.ones(A));mem=memnew
 runs.append({'seed':seed,'N':N,'private_terminal_T':term,'terminal_conditional_resource_bell_score':term_score,'path_average_conditional_learned_score':sumscore/N,'path_average_fixed_identity_score':sumI/N,'scope':'one-path conditional diagnostic, not expected occupation oracle or confidence statement'})
result={'source':'2 data qubits, 1 retained memory qubit, 1 fresh emitted flag; noncommuting coherent interactions listed in source','training_interface':'2 protected Bell reference halves, 2 Bell readouts, one random flag Pauli parity','source_calls_simulated':3*N,'max_conditional_gradient_entry_error':max_grad,'max_resource_bell_identity_error':max_resource,'max_explicit_teleport_choi_error':max_tele,'max_memory_trace_error':float(max_norm),'max_successive_memory_commutator_Fnorm':max_backaction,'runs':runs,'scope':'same-seed deterministic replay with identity initialization; not new independent source calls; initial-distance constant differs from governing theorem; no confidence or advantage claim'}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(result,indent=2)+'\n');np.save(Path(__file__).with_name('quantum_memory_records_warmstart_v1.npy'),np.array(records,dtype=np.int64));print(json.dumps(result))

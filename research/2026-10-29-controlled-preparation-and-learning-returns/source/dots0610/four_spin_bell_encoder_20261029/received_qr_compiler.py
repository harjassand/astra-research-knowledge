"""Explicit ideal four-spin encoder; numerical validation of analytic gate identities."""
import numpy as np, json
from pathlib import Path
P=Path(__file__).parent
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)
H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
T=np.diag([1,np.exp(1j*np.pi/4)])
def single(t,m): return ('u',t,np.asarray(m,complex))
def cx(c,t): return ('cx',c,t)
def rz(x):return np.diag([np.exp(-1j*x/2),np.exp(1j*x/2)])
def ry(x):return np.array([[np.cos(x/2),-np.sin(x/2)],[np.sin(x/2),np.cos(x/2)]],complex)
def cu(c,t,U):
 alpha=np.angle(np.linalg.det(U))/2; S=U*np.exp(-1j*alpha); a,b=S[0]
 gamma=2*np.arctan2(abs(b),abs(a))
 if abs(b)<1e-13: beta=-2*np.angle(a);delta=0.
 elif abs(a)<1e-13: beta=-2*np.angle(-b);delta=0.
 else:beta=-np.angle(a)-np.angle(-b);delta=-np.angle(a)+np.angle(-b)
 return [single(t,rz((delta-beta)/2)),cx(c,t),single(t,rz(-(delta+beta)/2)),single(t,ry(-gamma/2)),cx(c,t),single(t,ry(gamma/2)),single(t,rz(beta)),single(c,np.diag([1,np.exp(1j*alpha)]))]
def cc(c,d,t,U):
 ev,Q=np.linalg.eig(U);V=Q@np.diag(np.exp(.5j*np.angle(ev)))@np.linalg.inv(Q)
 assert np.linalg.norm(V@V-U)<1e-12
 return cu(d,t,V)+[cx(c,d)]+cu(d,t,V.conj().T)+[cx(c,d)]+cu(c,t,V)
def tof(a,b,t):
 return [single(t,H),cx(b,t),single(t,T.conj().T),cx(a,t),single(t,T),cx(b,t),single(t,T.conj().T),cx(a,t),single(b,T),single(t,T),single(t,H),cx(a,b),single(a,T),single(b,T.conj().T),cx(a,b)]
def apply(W,g):
 if g[0]=='u':
  t,M=g[1:]; aa=np.array([a for a in range(W.shape[0]) if not a&(1<<t)]);bb=aa|(1<<t)
  A=W[aa].copy(); B=W[bb].copy();W[aa]=M[0,0]*A+M[0,1]*B;W[bb]=M[1,0]*A+M[1,1]*B
 else:
  c,t=g[1:];aa=np.array([a for a in range(W.shape[0]) if a&(1<<c) and not a&(1<<t)]);bb=aa|(1<<t);W[aa],W[bb]=W[bb].copy(),W[aa].copy()
def adjacent(a,b,M):
 t=(a^b).bit_length()-1; assert (a^b).bit_count()==1
 if a&(1<<t):M=X@M@X
 controls=[j for j in range(4) if j!=t]; opens=[single(j,X) for j in controls if not a&(1<<j)]
 c,d,e=controls
 return opens+tof(c,d,4)+cc(4,e,t,M)+tof(c,d,4)+opens[::-1]
def twolevel(a,b,M):
 path=[a]
 for bit in range(4):
  if (a^b)&(1<<bit):path.append(path[-1]^(1<<bit))
 swaps=[(path[i],path[i+1],X) for i in range(len(path)-2)]
 primitives=swaps+[(path[-2],path[-1],M)]+swaps[::-1]
 return sum([adjacent(*g) for g in primitives],[]),len(primitives)
def target():
 E=np.zeros((16,2),complex)
 for s,v in [('0101',.5),('0110',-.5),('1001',-.5),('1010',.5)]: E[int(s,2),0]=v
 for s,v in [('0011',1),('1100',1),('0101',-.5),('0110',-.5),('1001',-.5),('1010',-.5)]:E[int(s,2),1]=v/np.sqrt(3)
 return E
def build():
 E=target(); A=E.copy(); reductions=[]
 for col in range(2):
  for row in range(15,col,-1):
   x,y=A[col,col],A[row,col]
   if abs(y)<1e-14:continue
   r=np.sqrt(abs(x)**2+abs(y)**2);G=np.array([[x.conjugate(),y.conjugate()],[-y,x]])/r
   A[[col,row]]=G@A[[col,row]];reductions.append((col,row,G))
 assert np.linalg.norm(A-np.eye(16)[:,:2])<1e-12
 two=[(a,b,G.conj().T) for a,b,G in reductions[::-1]]
 direct=np.eye(16,dtype=complex);gates=[];nprim=0
 for a,b,G in two:
  direct[[a,b]]=G@direct[[a,b]]; gs,n=twolevel(a,b,G);gates+=gs;nprim+=n
 return E,direct,gates,two,nprim

def main():
 E,U,gates,two,nprim=build(); W=np.eye(32,dtype=complex)
 for g in gates:apply(W,g)
 errors={'target_orthonormal':float(np.linalg.norm(E.conj().T@E-np.eye(2))), 'direct_target':float(np.linalg.norm(U[:,:2]-E)), 'full_clean_work_action':float(np.linalg.norm(W[:16,:16]-U)), 'work_restoration':float(np.linalg.norm(W[16:,:16])), 'unitarity':float(np.linalg.norm(W.conj().T@W-np.eye(32)))}
 # Total-spin annihilation establishes the columns are singlets.
 paulis=[X,np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
 spins=[]
 for pauli in paulis:
  S=np.zeros((16,16),complex)
  for j in range(4):
   V=np.eye(16,dtype=complex);apply(V,single(j,pauli));S+=V/2
  spins.append(np.linalg.norm(S@E))
 errors['total_spin_annihilation']=float(max(spins))
 # Complete decoder: U† then trace bits1,2,3. Contrast with reset leakage-to-|0> target decoder.
 D=[U.conj().T[[2*a,2*a+1],:] for a in range(8)]
 errors['decoder_trace_preservation']=float(np.linalg.norm(sum(d.conj().T@d for d in D)-np.eye(16)))
 rng=np.random.default_rng(292026); maxcoh=0.; maxinverse=0.
 for _ in range(30):
  psi=rng.normal(size=(2,3))+1j*rng.normal(size=(2,3));psi/=np.linalg.norm(psi)
  phys=E@psi;recovered=sum(np.outer((d@phys).reshape(-1),(d@phys).reshape(-1).conj()) for d in D)
  maxcoh=max(maxcoh,np.linalg.norm(recovered-np.outer(psi.reshape(-1),psi.reshape(-1).conj())))
  v=rng.normal(size=16)+1j*rng.normal(size=16);v/=np.linalg.norm(v);w=np.r_[v,np.zeros(16)]
  for g in gates:apply(w[:,None],g)
  for g in reversed(gates):apply(w[:,None],single(g[1],g[2].conj().T) if g[0]=='u' else g)
  maxinverse=max(maxinverse,np.linalg.norm(w-np.r_[v,np.zeros(16)]))
 # Canonical CPTP reset completion, with explicit readout/reset branches.
 canonical=[E.conj().T]
 for a in range(1,8):
  for logical in range(2):
   k=np.zeros((2,16),complex);k[0]=U.conj().T[2*a+logical];canonical.append(k)
 reset_err=0.
 for _ in range(20):
  v=rng.normal(size=(16,3))+1j*rng.normal(size=(16,3));v/=np.linalg.norm(v)
  got=sum(np.outer((k@v).reshape(-1),(k@v).reshape(-1).conj()) for k in canonical)
  coded=E.conj().T@v; leak=(np.eye(16)-E@E.conj().T)@v
  bath=leak.T@leak.conj(); expected=np.outer(coded.reshape(-1),coded.reshape(-1).conj());expected[:3,:3]+=bath
  reset_err=max(reset_err,np.linalg.norm(got-expected))
 errors['canonical_reset_on_entangled_physical_inputs']=float(reset_err)
 errors['canonical_reset_trace_preservation']=float(np.linalg.norm(sum(k.conj().T@k for k in canonical)-np.eye(16)))
 errors['coherent_logical_reference_recovery']=float(maxcoh);errors['inverse_full_physical']=float(maxinverse)
 assert max(errors.values())<1e-11,errors
 np.savez_compressed(P/'circuit.npz',kind=np.array([g[0] for g in gates]),arg1=np.array([g[1] for g in gates]),arg2=np.array([g[2] if g[0]=='cx' else -1 for g in gates]),matrices=np.array([g[2] if g[0]=='u' else I for g in gates]),isometry=E,unitary=U)
 result={'status':'PASS_FLOATING_VALIDATION_OF_ANALYTIC_IDEAL_CIRCUIT','physical_bit_order':'ket q3 q2 q1 q0; logical input q0; q1,q2,q3 initialized zero; clean work q4','two_level_gates':len(two),'addressed_three_controlled_primitives':nprim,'cnot_count':sum(g[0]=='cx' for g in gates),'single_qubit_count':sum(g[0]=='u' for g in gates),'peak_qubits_per_block':5,'errors':errors,'decoder_note':'Plain inverse then discard ancillas is CPTP and exactly recovers code, but differs on leakage from canonical reset-to-zero decoder. Add ancilla-zero test and conditional logical reset to match canonical decoder.'}
 (P/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

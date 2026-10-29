"""Independent numerical execution of root's analytic Bell-label encoder."""
import numpy as np,json
from pathlib import Path
from received_qr_compiler import target,apply,single,cx,ry,X,H
P=Path(__file__).parent
Z=np.diag([1,-1])
def negcry(c,t,theta):
 return [single(c,X),single(t,ry(theta/2)),cx(c,t),single(t,ry(-theta/2)),cx(c,t),single(c,X)]
def gates():
 # label A=(a=q0,b=q1), B=(a=q2,b=q3), physical ket q3q2q1q0
 theta=-2*np.arcsin(np.sqrt(2/3))
 return [single(0,X),single(1,X)]+negcry(0,1,theta)+negcry(1,0,np.pi/2)+[single(0,Z),single(1,Z),cx(0,2),cx(1,3),single(0,H),cx(0,1),single(2,H),cx(2,3)]
def main():
 gs=gates();U=np.eye(16,dtype=complex)
 for g in gs:apply(U,g)
 E=target();err={'encoded_columns':float(np.linalg.norm(U[:,:2]-E)),'unitarity':float(np.linalg.norm(U.conj().T@U-np.eye(16)))}
 ks=[U.conj().T[:2]]
 for a in range(1,8):
  for b in range(2):
   k=np.zeros((2,16),complex);k[0]=U.conj().T[2*a+b];ks.append(k)
 err['canonical_TP']=float(np.linalg.norm(sum(k.conj().T@k for k in ks)-np.eye(16)))
 rng=np.random.default_rng(291008);inv=0.;reset=0.;coherent=0.
 for _ in range(100):
  W=U.copy()
  for g in gs[::-1]:apply(W,single(g[1],g[2].conj().T) if g[0]=='u' else g)
  inv=max(inv,np.linalg.norm(W-np.eye(16)))
  v=rng.normal(size=(16,4))+1j*rng.normal(size=(16,4));v/=np.linalg.norm(v)
  got=sum(np.outer((k@v).reshape(-1),(k@v).reshape(-1).conj()) for k in ks)
  c=E.conj().T@v;leak=(np.eye(16)-E@E.conj().T)@v
  want=np.outer(c.reshape(-1),c.reshape(-1).conj());want[:4,:4]+=leak.T@leak.conj()
  reset=max(reset,np.linalg.norm(got-want))
  p=rng.normal(size=(2,4))+1j*rng.normal(size=(2,4));p/=np.linalg.norm(p)
  got=sum(np.outer((k@E@p).reshape(-1),(k@E@p).reshape(-1).conj()) for k in ks)
  coherent=max(coherent,np.linalg.norm(got-np.outer(p.reshape(-1),p.reshape(-1).conj())))
 err.update(full_inverse=float(inv),entangled_reset=float(reset),coherent_recovery=float(coherent));assert max(err.values())<1e-12,err
 result={'status':'PASS_NUMERICAL_IDEAL_CIRCUIT','cnot_count':sum(g[0]=='cx' for g in gs),'single_count':sum(g[0]=='u' for g in gs),'peak_qubits':4,'errors':err,'scope':'Root analytic construction independently executed; no numerical interval/hardware fidelity claim. Full unitary differs from QR completion but same isometry and canonical reset channel.'}
 np.savez_compressed(P/'bell_circuit.npz',kind=np.array([g[0] for g in gs]),arg1=np.array([g[1] for g in gs]),arg2=np.array([g[2] if g[0]=='cx' else -1 for g in gs]),matrices=np.array([g[2] if g[0]=='u' else np.eye(2) for g in gs]),unitary=U,isometry=E)
 (P/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

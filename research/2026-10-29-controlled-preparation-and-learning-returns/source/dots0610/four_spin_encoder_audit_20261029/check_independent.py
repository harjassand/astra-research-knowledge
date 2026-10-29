import numpy as np,sys,json,itertools
from pathlib import Path
p=Path(__file__).parent;s=p.parent/'four_spin_encoder_compiler_20261029';sys.path.insert(0,str(s));import compiler as c
rng=np.random.default_rng(202610290509)
def circuit(gs,n):
 W=np.eye(1<<n,dtype=complex)
 for g in gs:
  if g[0]=='u':
   M=np.array([[1.]],complex)
   for bit in reversed(range(n)):M=np.kron(M,g[2] if bit==g[1] else np.eye(2))
   W=M@W
  else:
   ctrl,target=g[1:];perm=np.arange(1<<n);perm^=np.where((perm>>ctrl)&1,1<<target,0);W=W[perm]
 return W
def controlled(U,n,controls,t):
 M=np.eye(1<<n,dtype=complex)
 for a in range(1<<n):
  if a&(1<<t) or not all(a&(1<<v) for v in controls):continue
  M[np.ix_([a,a|(1<<t)],[a,a|(1<<t)])]=U
 return M
def randU():
 Q,R=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)));return Q@np.diag(np.exp(1j*rng.uniform(-3,3,2)))
errs={};Ulist=[np.eye(2),c.X,np.diag([1j,-1j]),np.exp(.71j)*np.eye(2)]+[randU() for _ in range(20)]
errs['controlled_unitary']=max(np.linalg.norm(circuit(c.cu(0,1,U),2)-controlled(U,2,[0],1)) for U in Ulist)
errs['double_controlled_unitary']=max(np.linalg.norm(circuit(c.cc(0,1,2,U),3)-controlled(U,3,[0,1],2)) for U in Ulist)
errs['Toffoli']=np.linalg.norm(circuit(c.tof(0,1,2),3)-controlled(c.X,3,[0,1],2))
# All addressed cube edges, both order orientations, with arbitrary U.
edge_count=0;edgeerr=0.;grayerr=0.
for a in range(16):
 for bit in range(4):
  b=a^(1<<bit);U=randU();M=np.eye(16,dtype=complex);M[np.ix_([a,b],[a,b])]=U
  W=circuit(c.adjacent(a,b,U),5)
  edgeerr=max(edgeerr,np.linalg.norm(W[:16,:16]-M),np.linalg.norm(W[16:,:16]));edge_count+=1
for a,b in [(0,15),(15,0),(3,12),(12,3),(5,10),(10,5),(2,9),(7,8)]:
 U=randU();M=np.eye(16,dtype=complex);M[np.ix_([a,b],[a,b])]=U;gs,_=c.twolevel(a,b,U);W=circuit(gs,5)
 grayerr=max(grayerr,np.linalg.norm(W[:16,:16]-M),np.linalg.norm(W[16:,:16]))
errs['all_addressed_edges']=edgeerr;errs['Gray_nonadjacent']=grayerr
E,U,gs,tw,np_=c.build();W=circuit(gs,5)
errs['full_clean_action']=np.linalg.norm(W[:16,:16]-U);errs['full_work_restore']=np.linalg.norm(W[16:,:16]);errs['target']=np.linalg.norm(W[:16,:2]-E)
# Choi comparison uses ACTUAL inverse circuit, not ideal completed U metadata.
V=W.conj().T;K=[V[:2,:16]]
for a in range(1,8):
 for l in range(2):
  k=np.zeros((2,16),complex);k[0]=V[2*a+l,:16];K.append(k)
J=sum(np.outer(k.reshape(-1),k.reshape(-1).conj()) for k in K)
# Canonical independent Choi from E and leakage effect Pperp.
P=np.eye(16)-E@E.conj().T;Jtarget=np.outer(E.conj().T.reshape(-1),E.conj().T.reshape(-1).conj());Jtarget[:16,:16]+=P.T
errs['actual_inverse_canonical_reset_Choi']=np.linalg.norm(J-Jtarget)
errs['actual_inverse_reset_TP']=np.linalg.norm(sum(k.conj().T@k for k in K)-np.eye(16))
# Explicit distinction plain inverse/discard versus canonical reset on leakage column3.
leak=U[:,3];plain=np.zeros((2,2),complex)
for a in range(8):
 v=U.conj().T[2*a:2*a+2]@leak;plain+=np.outer(v,v.conj())
assert np.linalg.norm(plain-np.diag([0,1]))<1e-12
reset=sum(np.outer(k@leak,(k@leak).conj()) for k in K);assert np.linalg.norm(reset-np.diag([1,0]))<1e-12
assert max(errs.values())<1e-11
out={'status':'PASS_FLOATING_INDEPENDENT_GATE_AND_CHANNEL_REVIEW','controlled_unitary_examples':len(Ulist),'all_addressed_oriented_cube_edges':edge_count,'nonadjacent_Gray_examples':8,'CNOT':sum(g[0]=='cx' for g in gs),'single_qubit':sum(g[0]=='u' for g in gs),'errors':{k:float(v) for k,v in errs.items()},'plain_inverse_vs_canonical_reset_leakage_trace_distance':1.0,'scope':'Independent matrix-embedding numerical check of ideal identities; not interval arithmetic or hardware calibration.'};(p/'independent_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

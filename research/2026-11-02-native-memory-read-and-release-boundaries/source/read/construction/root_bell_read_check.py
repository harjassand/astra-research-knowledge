"""Full-space Bell decoding check on actual five-qubit seed, arbitrary coherent syndromes/reference."""
import numpy as np,itertools,json
from functools import reduce
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex);Y=1j*X@Z
kron=lambda x:reduce(np.kron,x)
checks=[kron([X if j in a else I for j in range(5)]) for a in [[0,1,4],[2,3,4]]]+[kron([Z if j in a else I for j in range(5)]) for a in [[0,2,4],[1,3,4]]]
P0=np.eye(32,dtype=complex)
for S in checks:P0=P0@(np.eye(32)+S)/2
zlog=kron([Z if j in [0,1] else I for j in range(5)])
vals,vecs=np.linalg.eigh(P0@(np.eye(32)+zlog)/2);v0=vecs[:,np.argmax(vals)]
xlog=kron([X if j in [0,2] else I for j in range(5)]);V=np.stack([v0,xlog@v0],axis=1)
assert np.linalg.norm(V.conj().T@V-np.eye(2))<1e-12
paulis=[];reps={}
for labels in sorted(itertools.product(range(4),repeat=5),key=lambda a:(sum(x!=0 for x in a),a)):
 P=kron([[I,X,Y,Z][x] for x in labels]);s=tuple(int(np.linalg.norm(S@P-P@S)>1e-8) for S in checks)
 paulis.append((s,P));reps.setdefault(s,P)
rng=np.random.default_rng(145);a=rng.normal(size=(64,7))+1j*rng.normal(size=(64,7));rho=a@a.conj().T;rho/=np.trace(rho)
ideal=np.zeros((4,4),complex);actual=np.zeros_like(ideal);counts={s:0 for s in reps};frame_res=0
for s,R in reps.items():
 K=np.kron(V.conj().T@R.conj().T,np.eye(2));ideal+=K@rho@K.conj().T
for s,P in paulis:
 M=V.conj().T@P@reps[s]@V
 frame_res=max(frame_res,float(np.linalg.norm(M.conj().T@M-np.eye(2))))
 K=np.kron(M.conj().T@V.conj().T@P/np.sqrt(64),np.eye(2));actual+=K@rho@K.conj().T;counts[s]+=1
err=float(np.linalg.norm(actual-ideal,ord='nuc'));assert err<1e-12;assert set(counts.values())=={64}
r=dict(scope='Actual five-qubit seed, explicit coset decoder; not full-family noisy access simulation.',input_rank=7,input_system_reference_dimension=64,syndromes=len(reps),bell_outcomes=len(paulis),outcomes_per_syndrome=64,frame_unitarity_residual=frame_res,reference_safe_trace_difference=err,output_trace=float(np.trace(actual).real))
print(json.dumps(r,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(r,indent=2)+'\n')

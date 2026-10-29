import numpy as np,json
from pathlib import Path
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.]);P=[X,Y,Z]
u=np.array([3/5,0,4/5]);T0=np.diag([.8,.8,.64]);T1=.8*np.eye(3)-.16*np.outer(u,u)
r0=np.diag([1.,0]);r1=np.diag([0.,1]);C=[]
for j in range(3):
 C.append(sum(np.kron(sum(T[a,j]*P[a] for a in range(3))/2,r)/2 for T,r in [(T0,r0),(T1,r1)]))
G=np.array([[np.trace(a@b).real for b in C] for a in C]);e,v=np.linalg.eigh(G);W=(v*(1/np.sqrt(e)))@v.T
F=[sum(C[k]*W[k,j] for k in range(3)) for j in range(3)]
def sign(a):
 e,v=np.linalg.eigh(a);return (v*np.sign(e))@v.conj().T
S=list(map(sign,F));B=[np.kron(p,I) for p in P]
r={'status':'PASS_BOUNDARY_NUMERICAL_FIXTURE','T0':T0.tolist(),'T1':T1.tolist(),'gram_eigenvalues':e.tolist(),'whitened_sign_errors':[float(np.linalg.norm(s-b,2)) for s,b in zip(S,B)],'XZ_anticommutator_norm':float(np.linalg.norm(S[0]@S[2]+S[2]@S[0],2)),'min_sign_gap':min(float(np.min(np.abs(np.linalg.eigvalsh(f)))) for f in F),'source':'Equal mixture: own-qubit AD rate9/25 along z or (3/5,0,4/5), spectator reset to orthogonal branch flag. Valid product-channel components; fixed V=I.','limitations':'Floating diagnostic of an explicit analytic counterexample, not sampled acquisition or a universal impossibility.'}
assert min(r['gram_eigenvalues'])>0 and r['min_sign_gap']>0 and max(r['whitened_sign_errors'])>.01 and r['XZ_anticommutator_norm']>.01
out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))

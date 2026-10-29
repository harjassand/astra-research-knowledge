import numpy as np,json
from scipy.linalg import expm,eigh
from functools import reduce
rng=np.random.default_rng(2026102906)
P=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex);kron=lambda xs:reduce(np.kron,xs)
rows=[]
for n in [4,6]:
 d=2**n;ops=[[kron([P[a] if i==j else np.eye(2) for i in range(n)]) for j in range(n)] for a in range(3)]
 J=[sum(x)/2 for x in ops];vals,Z=eigh(sum(A@A for A in J));Es=Z[:,vals<1e-8];ds=Es.shape[1];Proj=Es@Es.conj().T;Q=np.eye(d)-Proj;k=2**int(np.floor(np.log2(ds)));E=Es[:,:k]
 Hbath=sum(np.kron(J[a],P[a]) for a in range(3))+np.kron(np.eye(d),.13*P[0])
 for label,h in [('small_random',.03*rng.normal(size=(n,3))),('moderate_random',.3*rng.normal(size=(n,3))),('common_rotation',np.tile([.3,.2,-.4],(n,1)))]:
  H=sum(h[j,a]*ops[a][j]/2 for a in range(3) for j in range(n));W=expm(-1j*H);S=W@E
  variance=np.trace(Proj@H@H).real/ds;formula=n/(4*(n-1))*sum(np.linalg.norm(x-h.mean(axis=0))**2 for x in h)
  weighted_leak=np.linalg.norm(Q@W@Proj,'fro')**2/ds;code_leak=np.linalg.norm(Q@S,'fro')**2/k;bound=ds/k*n/(n-1)*sum(np.linalg.norm(x-h.mean(axis=0))**2 for x in h)
  assert abs(variance-formula)<1e-11 and weighted_leak<=variance+1e-11
  for t in [1,13,100]:
   U=expm(-1j*t*Hbath).reshape(d,2,d,2);As=[S.conj().T@U[:,b,:,0]@S for b in range(2)];F=sum(abs(np.trace(A))**2 for A in As)/k**2
   assert 1-F<=4*code_leak+1e-10 and 1-F<=bound+1e-10
   rows.append({'n':n,'logical_dim':k,'case':label,'time':t,'exact_variance':float(variance),'covariance_formula':float(formula),'weighted_leakage':float(weighted_leak),'code_average_leakage':float(code_leak),'direct_Bell_loss':float(1-F),'four_leakage_bound':float(4*code_leak),'frame_variance_bound':float(bound)})
print(json.dumps({'seed':2026102906,'checks':rows},indent=2))

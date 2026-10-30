import numpy as np,json
rng=np.random.default_rng(1439)
I=np.eye(2); Ic=np.eye(3)
G=np.zeros((12,12),complex)
idx=lambda q,b,c:(q*2+b)*3+c
for q in range(2):
 for b in range(2):
  for c in range(3):G[idx(*( (q,b,c) if c==0 else (b,q,c))),idx(q,b,c)]=1
P=np.kron(np.eye(4),np.diag([1,1,0]))
R=np.zeros((3,3),complex);R[:2,:2]=[[2.75,-.5j],[.5j,2]]
A=R/np.linalg.eigvalsh(R).max();r=1/np.linalg.eigvalsh(R).max()
Hc=np.zeros((3,3),complex);Hc[0,1]=Hc[1,0]=1
Jc=np.zeros((3,3),complex);Jc[2,1]=1
jsc=[Jc]+[np.diag(np.eye(3)[i]) for i in range(3)]
def adj(W,H,js):
 out=1j*(H@W-W@H)
 for J in js:
  D=J.conj().T@J;out+=J.conj().T@W@J-(D@W+W@D)/2
 return out
rows=[]
for u in [.03,.1,.5]:
 F=np.diag(np.exp([.2,-.2]));V=Ic+u*A;W=np.kron(np.kron(F,I),V)
 eig,U=np.linalg.eigh(W);inv=(U*(eig**-.5))@U.conj().T
 Lr=np.kron(np.kron(F,I),adj(V,Hc,jsc))
 for k in range(12):
  X=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));H=(X+X.conj().T)/2;H/=np.linalg.norm(H,2)
  J=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));J/=np.linalg.norm(J,2)
  Hhot=G@np.kron(np.kron(H,I),Ic)@G.conj().T
  Jhot=G@np.kron(np.kron(J,I),Ic)@G.conj().T
  Lh=adj(W,Hhot,[Jhot]);C=float(np.linalg.norm(inv@Lh@inv,2))
  corner=float(np.linalg.norm(Lh-P@Lh@P))
  scale=(C+1)*(1+u)/(r*u)
  slack=-Lh-scale*Lr
  rows.append({'u':u,'fixture':k,'active_corner_error':corner,'relative_hot_norm':C,'paid_router_scale':scale,'minimum_absorbed_drift':float(np.linalg.eigvalsh(slack)[0])})
assert max(r['active_corner_error'] for r in rows)<1e-12
assert min(r['minimum_absorbed_drift'] for r in rows)>-1e-10
print(json.dumps({'scope':'local operator fixtures only, not many-body memory validation','rows':rows},indent=2))

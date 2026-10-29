import numpy as np,json
I2=np.eye(2);I3=np.eye(3);p=np.diag([1.,0,0]);q=I3-p
def ten(a,b,c):return np.kron(np.kron(a,b),c)
def aux(op,x):return ten(I2,op,I3) if x==0 else ten(I2,I3,op)
P=[aux(p,x) for x in range(2)];Q=[aux(q,x) for x in range(2)];K=[[np.diag([1,np.sqrt(.6)]),np.array([[0,np.sqrt(.4)],[0,0]])],[np.sqrt(.7)*I2,np.sqrt(.3)*np.array([[0,1],[1,0]])]]
V=[];jumps=[]
for x in range(2):
 v=np.zeros((18,18),complex)
 for s in range(2):
  up=np.zeros((3,3));up[s+1,0]=1
  v+=ten(K[x][s],up,I3) if x==0 else ten(K[x][s],I3,up)
  jumps.append((x,aux(up.T,x)))
 V.append(v)
g=.7;k=1.2;H=sum(g*P[1-x]@(V[x]+V[x].conj().T) for x in range(2))
def L(A):
 out=1j*(H@A-A@H)
 for x,b in jumps:
  n=b.conj().T@b
  out+=k*(b.conj().T@A@b-.5*(n@A+A@n))
 return out
out=[]
for x in range(2):
 cur=L(L(Q[x]));G=P[1-x];E=V[x]@V[x].conj().T
 B=cur-2*g*g*G@(P[x]-E)-k*k*Q[x]
 out.append(dict(x=x,isometry_error=float(np.linalg.norm(V[x].conj().T@V[x]-P[x])),ready_curvature_error=float(np.linalg.norm(P[x]@cur@P[x]-2*g*g*G@P[x])),offdiag_error=float(np.linalg.norm(P[x]@B@P[x])+np.linalg.norm(Q[x]@B@Q[x])),B_norm=float(np.linalg.norm(B,2)),B_bound=2*g*g+4*k*g+k*g))
assert all(r['ready_curvature_error']<1e-10 and r['offdiag_error']<1e-10 and r['B_norm']<=r['B_bound'] for r in out)
print(json.dumps(out,indent=2))

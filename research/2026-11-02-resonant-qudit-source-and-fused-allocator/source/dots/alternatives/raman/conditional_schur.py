import numpy as np,json

def make(w,eta,c1=0,c2=0,orderB=None,undo=True):
 # Same w data qubits, Z and X checks; use EVEN w so commute.
 ndata=w;ndata_dim=2**w;I=np.eye(2);Z=np.diag([1.,-1]);X=np.array([[0.,1],[1,0]])
 def psite(p,i):
  out=np.ones((1,1))
  for j in range(w):out=np.kron(out,p if i==j else I)
  return out
 orderB=list(range(w)) if orderB is None else orderB
 P=[[psite(Z,i) for i in range(w)],[psite(X,i) for i in orderB]]
 Q=[]
 for a in range(2):
  q=[np.eye(ndata_dim)]
  for p in P[a]:q.append(p@q[-1])
  if undo:q+=q[:w-1]
  Q.append(q)
 nb=len(Q[0]);states=[(a,b) for a in range(nb) for b in range(nb)];nn=len(states)
 phi=np.zeros(ndata_dim);phi[0]=phi[-1]=2**-.5
 GG=[Q[0][a]@Q[1][b] for a,b in states]
 def scalar(m,B,j):return (phi@GG[m].T@B@GG[j]@phi).real
 D=1/eta;A=np.diag(np.full(w-1,D))+np.diag(np.ones(w-2),1)+np.diag(np.ones(w-2),-1);Ai=np.linalg.inv(A);J=-Ai[-1,0];shift=Ai[0,0];h=np.sqrt(abs(J))/2
 H=np.zeros((nn,nn),complex)
 for a,c in enumerate([c1,c2]):
  for j,r in enumerate(states):
   q=r[a]
   H[j,j]+=shift if q in [0,w] else D
   if q<w:
    rr=list(r);rr[a]+=1;m=states.index(tuple(rr));v=scalar(m,P[a][q],j);H[m,j]+=v;H[j,m]+=v
   if q==0:
    rr=list(r);rr[a]=w;m=states.index(tuple(rr));v=-(-1)**c*J*scalar(m,np.eye(ndata_dim),j);H[m,j]+=v;H[j,m]+=v
   if undo and q in range(1,w):
    rr=list(r);rr[a]=w+q;m=states.index(tuple(rr));v=h*scalar(m,P[a][q-1],j);H[m,j]+=v;H[j,m]+=v
 low=[i for i,r in enumerate(states) if all(x in [0,w] for x in r)];high=[i for i in range(nn) if i not in low]
 def schur(H):return H[np.ix_(low,low)]-H[np.ix_(low,high)]@np.linalg.solve(H[np.ix_(high,high)],H[np.ix_(high,low)])
 eff=schur(H)
 # non-Hermitian no-jump exact Schur; endpoint decay J, dump decay g
 Hnh=H.copy()
 for i,r in enumerate(states):Hnh[i,i]-=.5j*sum(abs(J) if q==w else (1 if q>w else 0) for q in r)
 effnh=schur(Hnh)
 diag=np.diag(eff).real;dnh=np.diag(effnh)
 return dict(w=w,eta=eta,caches=[c1,c2],orderB=orderB,undo=undo,J=float(abs(J)),diag_over_J=(diag/abs(J)).tolist(),conditional_ZZ_over_J=float((diag[0]-diag[1]-diag[2]+diag[3])/(4*abs(J))),transition_detunings_over_J=((diag[[2,3,1,3]]-diag[[0,1,0,2]])/abs(J)).tolist(),eff_over_J=np.round(eff.real/abs(J),8).tolist(),nh_diag_real_over_J=(dnh.real/abs(J)).tolist())
if __name__=='__main__':
 for w in [4,6]:
  for eta in [.03,.05,.1,.2]:
   for c in [(0,0),(1,0),(1,1)]:print(json.dumps(make(w,eta,*c)),flush=True)

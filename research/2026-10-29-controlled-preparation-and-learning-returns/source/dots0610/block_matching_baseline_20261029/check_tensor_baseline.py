import numpy as np,itertools,json
from pathlib import Path
P=Path(__file__).parent
rng=np.random.default_rng(291516)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
def kronall(xs):
 r=np.array([[1.]])
 for x in xs:r=np.kron(r,x)
 return r
def E4():
 E=np.zeros((16,2),complex)
 for i,v in [(5,.5),(6,-.5),(9,-.5),(10,.5)]:E[i,0]=v
 for i,v in [(3,1),(12,1),(5,-.5),(6,-.5),(9,-.5),(10,-.5)]:E[i,1]=v/np.sqrt(3)
 return E
def matching_state(pairs):
 v=np.zeros(16)
 for bits in itertools.product(range(2),repeat=2):
  x=[0]*4;sign=1
  for (a,b),z in zip(pairs,bits):x[a]=z;x[b]=1-z;sign*=(-1)**z
  v[sum(z<<i for i,z in enumerate(x))]=sign/2
 return v
E=E4()
matching=[E.conj().T@matching_state(p) for p in [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]]
six=[]
for A in [X,Y,Z]:
 _,V=np.linalg.eigh(A);six.extend([V[:,0],V[:,1]])
def frame(states):
 vs=[np.outer(v,v.conj()).reshape(-1) for v in states]
 return sum(np.outer(v,v.conj()) for v in vs)/len(vs)
def product_states(states,h):return [kronall([v[:,None] for v in vs]).reshape(-1) for vs in itertools.product(states,repeat=h)]
def local_reps():
 gs=[]
 for perm in itertools.permutations(range(4)):
  T=np.zeros((16,16))
  for a in range(16):b=sum(((a>>j)&1)<<perm[j] for j in range(4));T[b,a]=1
  gs.append(E.conj().T@T@E)
 return gs
def trial(h):
 d=2**h;m=2; out=d+1
 A=rng.normal(size=(out*m,d*m))+1j*rng.normal(size=(out*m,d*m));K=np.linalg.qr(A)[0]
 B=sum(K.reshape(out,m,d,m)[i,:,i,:] for i in range(d))/d
 G=np.zeros_like(K)
 for i in range(d):G[i*m:(i+1)*m,i*m:(i+1)*m]=B
 R=K-G;Hbad=np.eye(m)-B.conj().T@B
 gs=[kronall(x) for x in itertools.product(local_reps(),repeat=h)]
 avgR=np.zeros_like(K);eff=np.zeros((d*m,d*m),complex);CJ=np.zeros((out*d*m*m,out*d*m*m),complex);badCJ=CJ.copy()
 for g in gs:
  gout=np.eye(out,dtype=complex);gout[:d,:d]=g
  kg=np.kron(gout.conj().T,np.eye(m))@K@np.kron(g,np.eye(m));rg=kg-G
  avgR+=rg/len(gs);eff+=rg.conj().T@rg/len(gs)
  kv=kg.reshape(-1);rv=rg.reshape(-1);CJ+=np.outer(kv,kv.conj())/len(gs);badCJ+=np.outer(rv,rv.conj())/len(gs)
 gv=G.reshape(-1);split=np.linalg.norm(CJ-badCJ-np.outer(gv,gv.conj()))
 # Failure effects on memory, actual product state survival tests, no scalar shortcut.
 def test_effect(states):
  F=np.zeros((m,m),complex)
  for v in states:
   prep=np.kron(v[:,None],np.eye(m));vout=np.r_[v,0];a=np.kron(vout.conj()[None,:],np.eye(m))@K@prep
   F+=(np.eye(m)-a.conj().T@a)/len(states)
  return F
 effects={}
 for name,states,C in [('matching',matching,2.),('six_state',six,1.5)]:
  F=test_effect(product_states(states,h));effects[name]={'minimum_eigenvalue_C_failure_minus_Hbad':float(np.linalg.eigvalsh(C*F-Hbad).min()),'maximally_mixed_memory_failure':float(np.trace(F).real/m)}
 assert np.linalg.norm(avgR)<1e-12 and np.linalg.norm(eff-np.kron(np.eye(d),Hbad))<1e-12 and split<1e-12
 assert min(x['minimum_eigenvalue_C_failure_minus_Hbad'] for x in effects.values())>-1e-12
 # Completed canonical reset channel, separately twirled by product logical Paulis.
 D0=np.zeros((d,out),complex);D0[:,:d]=np.eye(d)
 D1=np.zeros((d,out),complex);D1[0,d]=1
 Ls=[np.kron(D,np.eye(m))@K for D in [D0,D1]]
 Bs=[sum(L.reshape(d,m,d,m)[i,:,i,:] for i in range(d))/d for L in Ls]
 Hcomp=np.eye(m)-sum(B.conj().T@B for B in Bs)
 Fc=np.zeros((m,m),complex)
 states=product_states(six,h)
 for v in states:
  prep=np.kron(v[:,None],np.eye(m));read=np.kron(v.conj()[None,:],np.eye(m));passop=sum((read@L@prep).conj().T@(read@L@prep) for L in Ls)
  Fc+=(np.eye(m)-passop)/len(states)
 paulis=[kronall(x) for x in itertools.product([I,X,Y,Z],repeat=h)]
 ceff=np.zeros((d*m,d*m),complex);mean=[np.zeros_like(L) for L in Ls]
 for g in paulis:
  for k,(L,B) in enumerate(zip(Ls,Bs)):
   Rg=np.kron(g.conj().T,np.eye(m))@L@np.kron(g,np.eye(m))-np.kron(np.eye(d),B)
   mean[k]+=Rg/len(paulis);ceff+=Rg.conj().T@Rg/len(paulis)
 compgap=float(np.linalg.eigvalsh(1.5*Fc-Hcomp).min());cerr=float(np.linalg.norm(ceff-np.kron(np.eye(d),Hcomp)))
 assert compgap>-1e-12 and cerr<1e-12 and max(np.linalg.norm(x) for x in mean)<1e-12
 effects['completed_six_state_with_logical_Pauli_twirl']={'minimum_eigenvalue_C_failure_minus_completed_Hbad':compgap,'completed_twirl_bad_effect_residual':cerr,'logical_Pauli_keys':len(paulis)}
 return {'h':h,'logical_dimension':d,'joint_source_isometry_residual':float(np.linalg.norm(K.conj().T@K-np.eye(d*m))),'physical_permutations':len(gs),'mean_residual':float(np.linalg.norm(avgR)),'bad_effect_residual':float(np.linalg.norm(eff-np.kron(np.eye(d),Hbad))),'exact_twirl_CP_split_residual':float(split),'bad_Choi_minimum':float(np.linalg.eigvalsh(badCJ).min()),'effects':effects}
def main():
 frames=[]
 for h in [1,2,3]:
  d=2**h
  for name,states,r in [('matching',matching,.5),('six_state',six,1/3)]:
   F=frame(product_states(states,h));idv=np.eye(d).reshape(-1)/np.sqrt(d);res=F-np.outer(idv,idv.conj())/d
   eig=np.linalg.eigvalsh(res);assert abs(eig[-1]-r/d)<1e-12
   frames.append({'h':h,'ensemble':name,'scalar_eigenvalue':1/d,'largest_nonscalar_eigenvalue':float(eig[-1]),'constant':1/(1-r)})
 out={'status':'PASS_FLOATING_EXACT_FORMULA_CHECKS','frames':frames,'correlated_memory_leakage_fixtures':[trial(1),trial(2)]}
 (P/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()

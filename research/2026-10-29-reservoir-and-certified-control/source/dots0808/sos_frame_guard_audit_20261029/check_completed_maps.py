"""Independent direct complete-decoder Kraus construction for frozen fixed candidates."""
import numpy as np,json,itertools
from pathlib import Path
root=Path('producer-workspace/sos_frame_guard_bridge_20261029');z=np.load(root/'maps_and_fixture.npz');U=z['source_unitary'];I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);ps=[I,X,Y,Z]
def channel(bs):
 T=np.zeros((4,4),complex)
 for i in range(2):
  for j in range(2):
   A=np.zeros((2,2),complex);A[i,j]=1
   T[:,2*i+j]=sum((b@A@b.conj().T for b in bs),np.zeros((2,2),complex)).reshape(-1)
 return T
out=[]
for name,key in [('sos','E_sos'),('ordinary_Nelder_Mead','E_nm')]:
 E=z[key];Q=np.linalg.qr(E,mode='complete')[0];dec=[E.conj().T]+[np.outer([1,0],Q[:,k].conj()) for k in range(2,16)]
 assert np.linalg.norm(sum(D.conj().T@D for D in dec)-np.eye(16))<1e-12
 Ks=[(np.kron(D,I)@U@np.kron(E,I)).reshape(2,2,2,2) for D in dec]
 branches=[]
 for P in ps:
  B=[sum((P[j,i].conjugate()*K[j,:,i,:] for j in range(2) for i in range(2)),np.zeros((2,2),complex))/2 for K in Ks]
  branches.append(channel(B))
 service=channel([K[o,:,i,:]/np.sqrt(2) for K in Ks for o in range(2) for i in range(2)])
 six=np.zeros((4,4),complex)
 for P in ps[1:]:
  _,V=np.linalg.eigh(P)
  for c in V.T:
   B=[sum((c[o].conjugate()*c[i]*K[o,:,i,:] for o in range(2) for i in range(2)),np.zeros((2,2),complex)) for K in Ks]
   six+=channel(B)/6
 matching=np.zeros((4,4),complex)
 for pairs in [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]:
  v=np.zeros(16,complex)
  for bits in itertools.product([0,1],repeat=2):
   b=[0]*4;sg=1
   for (a,c),t in zip(pairs,bits):b[a]=t;b[c]=1-t;sg*=(-1)**t
   v[sum(x*2**(3-i) for i,x in enumerate(b))]=sg/2
  physical=E@(z['E0'].conj().T@v)
  B=np.kron(physical.conj().reshape(1,16),I)@U@np.kron(physical.reshape(16,1),I)
  matching+=channel([B])/3
 residuals={k:float(np.linalg.norm(A-z[name+'_'+k])) for k,A in [('service',service),('completed_good',branches[0]),('six_pass',six),('matching_pass',matching)]}
 residuals['Pauli_sum']=float(np.linalg.norm(sum(branches)-service));assert max(residuals.values())<2e-12
 # Matrix-unit equality is a complete memory map identity, including untouched references.
 out.append({'candidate':name,'residuals':residuals,'decoder_kraus':len(dec)})
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

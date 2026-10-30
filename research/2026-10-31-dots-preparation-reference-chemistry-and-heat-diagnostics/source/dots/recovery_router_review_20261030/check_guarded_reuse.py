import numpy as np,json
rng=np.random.default_rng(9314)
def adj(O,H,L):
 D=L.conj().T@L
 return 1j*(H@O-O@H)+L.conj().T@O@L-(D@O+O@D)/2
S=np.zeros((4,4))
for q in range(2):
 for b in range(2):S[2*b+q,2*q+b]=1
P0=np.diag([1.,0,0]);P1=np.diag([0.,0,1]);Pe=np.diag([0.,1,0]);I2=np.eye(2)
G=np.kron(np.kron(np.eye(4),P0)+np.kron(S,Pe+P1),I2)
P=np.kron(np.kron(np.eye(4),P1),I2)
R=np.zeros((3,3),complex);R[:2,:2]=[[2.35,-.5j],[.5j,2]]
Vr=np.eye(3)+.3*R
F=np.array([[1.7,.2j],[-.2j,1.2]])
W=np.kron(np.kron(np.kron(F,I2),Vr),I2)
def embed(O):
 ans=np.zeros((24,24),complex)
 for q in range(2):
  for b in range(2):
   for c in range(3):
    for e in range(2):
     i=((q*2+b)*3+c)*2+e
     for qq in range(2):
      for ee in range(2):
       j=((qq*2+b)*3+c)*2+ee;ans[i,j]=O[2*q+e,2*qq+ee]
 return ans
rows=[]
for _ in range(12):
 h=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));h=(h+h.conj().T)/2
 l=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
 H=G@P@embed(h)@G;L=G@P@embed(l)@G
 z=adj(W,H,L)
 rows.append(float(np.linalg.norm(z)))
assert max(rows)<1e-10
# Wrong cached ACK would permit a Q bit flip in clock0; full adjoint not zero.
X=np.array([[0.,1],[1,0]])
H=G@embed(np.kron(X,I2))@G
wrong=float(np.linalg.norm(1j*(H@W-W@H)))
assert wrong>.1
print(json.dumps({'guarded_full_adjoint_residuals':rows,'unguarded_or_cached_ack_commutator':wrong,'scope':'Exact full-Hilbert random joint consumer/bath algebra; no state or truthful-history assumption.'},indent=2))

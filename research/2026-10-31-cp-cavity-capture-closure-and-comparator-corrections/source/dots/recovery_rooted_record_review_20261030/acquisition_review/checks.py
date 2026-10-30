import numpy as np,json
from scipy.linalg import expm
I=np.eye(2);X=np.array([[0,1],[1,0]]);P=np.diag([0,1])
kron=lambda a,b,c:np.kron(np.kron(a,b),c)
H=kron(P,np.pi/2*(I-X),I)
R=kron(P,I,X)
V0=np.diag(np.exp(np.arange(8)/8))
t=.37;eps=1e-6;a=.4
V=lambda t:expm(-1j*t*H)@(np.exp(-a*t)*V0)@expm(1j*t*H)
res=(V(t+eps)-V(t-eps))/(2*eps)+1j*(H@V(t)-V(t)@H)+a*V(t)
assert np.linalg.norm(res)<1e-8
assert np.linalg.norm(H@R-R@H)<1e-12
# A small temporary graph: old rooted path 0-1-2, target leaves 3 at 0, 4 at 2.
edges=[(0,1),(1,2),(0,3),(2,4)]
def conn(A):
 seen={0}
 while True:
  more=seen|{v for u,v in edges if u in seen and v in A}|{u for u,v in edges if v in seen and u in A}
  if more==seen:return seen==A
  seen=more
animals=[{i for i in range(5) if m>>i&1} for m in range(1,32,2)]
animals=[A for A in animals if conn(A)]
a=3.;L=7.;r=1.1;ap=a-4*np.log1p(np.exp(-a)*r)
maxratio=0
for mask in range(8):
 occ={i for bit,i in enumerate([1,3,4]) if mask>>bit&1}
 lhs=sum(np.exp(-a*len(A)+L*len(A&occ&{1}))*r**len(A&occ&{3,4}) for A in animals)
 rhs=sum(np.exp(-ap*len(B)+L*len(B&occ&{1})) for B in [{0},{0,1},{0,1,2}])
 maxratio=max(maxratio,lhs/rhs);assert lhs<=rhs
print(json.dumps({'moving_frame_derivative_residual':float(np.linalg.norm(res)),'copy_read_commutator_norm':float(np.linalg.norm(H@R-R@H)),'soft_attachment_max_ratio':maxratio},indent=2))

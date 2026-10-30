"""Finite check of common coherent recovery/inverse-encoder target; not noisy hardware simulation."""
import numpy as np,itertools,json
n=7;N=1<<n;H=[0b1111000,0b1100110,0b1010101]
C=[0]
for h in H:C += [v^h for v in C[:]]
V=np.zeros((N,2),complex)
for b in range(2):
 for c in C:V[c^(127 if b else 0),b]=1/np.sqrt(len(C))
syn=lambda x,z:sum((((h&z).bit_count()&1)<<i)|(((h&x).bit_count()&1)<<(i+3)) for i,h in enumerate(H))
def apply(x,z,A):
 phases=np.array([(-1)**((i&z).bit_count()) for i in range(N)])
 return (phases[:,None]*A)[np.arange(N)^x,:]
representatives={}
for x in range(N):
 for z in range(N):
  s=syn(x,z);key=((x|z).bit_count(),x,z)
  if s not in representatives or key<representatives[s]:representatives[s]=key
# Columns ordered logical-first, then syndrome; dagger is coherent decoder.
W=np.zeros((N,N),complex)
for s,(_,x,z) in representatives.items():
 E=apply(x,z,V)
 for b in range(2):W[:,b*64+s]=E[:,b]
D=W.conj().T
unit=float(np.linalg.norm(W.conj().T@W-np.eye(N),2));res=0.;cnt=0
for x in range(N):
 for z in range(N):
  if (x|z).bit_count()>1:continue
  A=D@apply(x,z,V);s=syn(x,z);c=A[s,0]
  want=np.zeros((N,2),complex);want[s,0]=c;want[64+s,1]=c
  res=max(res,float(np.linalg.norm(A-want,2)));cnt+=1
assert unit<1e-12 and res<1e-12
print(json.dumps(dict(result='PASS',code='Steane7',correctable_Pauli_operators=cnt,common_quantum_factor_residual=res,coherent_decoder_unitarity_residual=unit,scope='exact target recovery/decoding algebra, not numerical FT threshold or actual noisy output simulation'),indent=2))

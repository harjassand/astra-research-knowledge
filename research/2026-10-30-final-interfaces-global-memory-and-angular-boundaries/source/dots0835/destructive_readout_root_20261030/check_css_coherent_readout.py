import numpy as np,json
rng=np.random.default_rng(96317)
# Steane CSS: columns of H are binary 1,...,7; row span is simplex C_X.
H=np.array([[(j>>r)&1 for j in range(1,8)] for r in range(3)],dtype=int)
CX=[]
for u in range(8):CX.append(tuple((np.array([(u>>r)&1 for r in range(3)])@H)%2))
def ind(bits):return sum(int(v)<<j for j,v in enumerate(bits))
Enc=np.zeros((128,2),complex)
for l in range(2):
 for c in CX:Enc[ind([(v+l)%2 for v in c]),l]=1/np.sqrt(8)
labels=[]
for x in range(128):
 bits=np.array([(x>>j)&1 for j in range(7)])
 s=H@bits%2; k=sum(int(s[r])<<r for r in range(3))
 if k:bits[k-1]^=1
 labels.append(int(sum(bits)%2))
def pauli(state,j,p):
 out=np.zeros_like(state)
 for x in range(128):
  bit=(x>>j)&1
  if p=='X':out[x^(1<<j)]+=state[x]
  elif p=='Z':out[x]+=(-1)**bit*state[x]
  elif p=='Y':out[x^(1<<j)]+=1j*(-1)**bit*state[x]
 return out
res=[]
for t in range(100):
 psi=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));psi/=np.linalg.norm(psi)
 state=Enc@psi
 errs=[state]+[pauli(state,j,p) for j in range(7) for p in ['X','Y','Z']]
 c=rng.normal(size=22)+1j*rng.normal(size=22);c/=np.linalg.norm(c)
 noisy=sum(a*e for a,e in zip(c,errs))
 got=[np.zeros((2,2),complex) for _ in range(2)]
 for x in range(128):got[labels[x]]+=np.outer(noisy[x],noisy[x].conj())
 expected=[np.outer(psi[l],psi[l].conj()) for l in range(2)]
 error=max(np.max(np.abs(got[l]-expected[l])) for l in range(2))
 res.append(float(error))
assert max(res)<1e-12
print(json.dumps({'trials':100,'max_instrument_entry_error':max(res),'scope':'Coherent full span of all weight-one Steane Pauli errors with an entangled reference; ideal physical Z readout and classical syndrome/coset decoder only.'},indent=2))

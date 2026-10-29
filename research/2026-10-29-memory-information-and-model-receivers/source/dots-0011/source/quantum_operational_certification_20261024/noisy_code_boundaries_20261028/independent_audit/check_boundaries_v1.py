"""Independent full-operator ideal proof and density-matrix noisy boundary replay."""
from pathlib import Path
import sys,json,hashlib,itertools,importlib.util
import numpy as np
import sympy as s
D=Path(__file__).parent;A=D.parent;Q=A.parent
sys.path.insert(0,str(A));import boundary_channel_v2 as author
P=[s.eye(2),s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
H=(P[1]+P[3])/s.sqrt(2);S=s.diag(1,s.I)
gates={'H':H,'S':S,'SDG':S.H,'X':P[1],'CX':s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])}
def embed(g,qs):
 out=s.zeros(32)
 for col in range(32):
  bits=[(col>>(4-q))&1 for q in range(5)];j=sum(bits[q]<<(len(qs)-1-k) for k,q in enumerate(qs))
  for i in range(2**len(qs)):
   if g[i,j]==0:continue
   b=bits.copy()
   for k,q in enumerate(qs):b[q]=(i>>(len(qs)-1-k))&1
   row=sum(b[q]<<(4-q) for q in range(5));out[row,col]=g[i,j]
 return out
ops,enc,_=author.synthesize();U=s.eye(32)
for name,qs in ops:U=embed(gates[name],qs)*U
V,R=author.m.c.exact_encoder_recovery();table=author.syndrome_table(np.array(U,complex));newR=[]
for a in range(16):newR.append(P[table[a]]*U[[a,16+a],:])
matched=[]
for B in newR:
 choices=[i for i,r in enumerate(R) if any(B==z*r for z in [1,-1,s.I,-s.I])]
 assert len(choices)==1;matched.append(choices[0])
assert sorted(matched)==list(range(16))
assert U*V==s.Matrix(32,2,lambda i,j:1 if i==16*j else 0) or U*V==-s.Matrix(32,2,lambda i,j:1 if i==16*j else 0)
# Independent exact timing recount, all native Clifford gate supports.
from collections import Counter
counts=Counter(n for n,q in ops);gate_time=sum(2 if n=='CX' else 1 for n,q in ops);boundary_time=4*2+2*gate_time+4*4+1+1
assert boundary_time==26+2*gate_time
pn=[np.array(x,complex) for x in P];basis=[]
for word in itertools.product(range(4),repeat=5):
 b=np.ones((1,1),complex)
 for i in word:b=np.kron(b,pn[i])
 basis.append(b)
basis=np.array(basis);bits=np.array([[(i>>(4-q))&1 for q in range(5)] for i in range(32)])
def emb(g,qs):return np.array(embed(s.Matrix(g),qs),complex)
def rotate(p,eta):return np.cos(eta/2)*np.eye(len(p))-1j*np.sin(eta/2)*p
def bg(r,rate,dt,live):
 ham=np.sum(bits[:,None,live]!=bits[None,:,live],axis=2);return r*np.exp(-rate*dt*ham)
def noise_circuit(r,ops,eta,rate):
 for name,qs in ops:
  ideal=np.array(gates[name],complex);err=np.kron(pn[3],pn[3]) if name=='CX' else pn[1]
  g=emb(rotate(err,eta)@ideal,qs);r=g@r@g.conj().T;r=bg(r,rate,2 if name=='CX' else 1,list(range(5)))
 return r
def measured(r,eta,rate):
 live=list(range(5));branches={():r}
 for q in range(1,5):
  new={};rot=emb(rotate(pn[2],eta),[q])
  for hist,x in branches.items():
   x=bg(x,rate,4,live);x=rot@x@rot.conj().T
   for z in [0,1]:
    mask=(bits[:,q]==z).astype(float);new[hist+(z,)]=mask[:,None]*x*mask[None,:]
  branches=new;live.remove(q)
 out=np.zeros((2,2),complex)
 for hist,x in branches.items():
  x=bg(x,rate,1,[0]);a=sum(b<<(3-k) for k,b in enumerate(hist));y=np.array([[sum(x[16*i+t,16*j+t] for t in range(16)) for j in range(2)] for i in range(2)])
  if table[a]:g=rotate(pn[1],eta)@pn[table[a]];y=g@y@g.conj().T
  y[0,1]*=np.exp(-rate);y[1,0]*=np.exp(-rate);out+=y
 return out
rng=np.random.default_rng(20261029);rows=[]
for eta,rate in [(0.,0.),(.001,.03/201),(-.01,.1/201),(.03,.3/201)]:
 # Challenge arbitrary non-Hermitian physical operator, not merely codespace states.
 x=rng.normal(size=(32,32))+1j*rng.normal(size=(32,32));x/=np.linalg.norm(x)
 coeff=np.einsum('aij,ji->a',basis,x)[:,None]
 got=author.measured_decode(author.circuit(coeff.real,ops,eta,rate),np.array(U,complex),eta,rate)+1j*author.measured_decode(author.circuit(coeff.imag,ops,eta,rate),np.array(U,complex),eta,rate)
 # Author returns output Pauli coefficients /2, so reconstruction uses no extra /2.
 gotmat=sum(got[k,0]*pn[k] for k in range(4));want=measured(noise_circuit(x,ops,eta,rate),eta,rate)
 err=float(np.max(abs(gotmat-want)));assert err<1e-12
 # Independently form noisy prepared ancilla product and sequential liveness.
 p0=pn[1];r=p0.copy()
 for _ in range(4):r=np.kron(r,np.diag([1.,0.]))
 for q in range(1,5):g=emb(rotate(pn[2],eta),[q]);r=g@r@g.conj().T;r=bg(r,rate,2,list(range(q+1)))
 r=noise_circuit(r,enc,eta,rate);ac=author.circuit(author.initial(eta,rate),enc,eta,rate)[:,1]
 actual=sum(ac[k]*basis[k] for k in range(1024))/32
 prep_err=float(np.max(abs(actual-r)));assert prep_err<1e-12
 rows.append({'eta':eta,'rate':rate,'arbitrary_operator_decoder_error':err,'prepared_encoder_error':prep_err})
files=[A/'boundary_channel_v2.py',A/'encoder_check_v2.json',Path(__file__)]
out={'status':'PASS_BOUNDARY_REPRESENTATION_AND_EXACT_IDEAL_CHANNEL','exact_syndrome_Kraus_permutation':matched,'gate_counts_each_direction':dict(counts),'gate_time_each_direction':gate_time,'boundary_time':boundary_time,'density_checks':rows,'source_draws':0,'sha256':{str(p.relative_to(Q)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(D/'check_boundaries_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

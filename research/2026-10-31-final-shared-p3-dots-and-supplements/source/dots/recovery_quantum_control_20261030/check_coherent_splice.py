import itertools,json,numpy as np
# Alternating-layer dependency chain, two brickwork layer types.
N=6
edges=[(i,i+1) if i%2==0 else (i+1,i) for i in range(N-1)]
def valid(h):return all(h[a]-h[b] in (0,1) for a,b in edges)
base_cuts=[h for h in itertools.product(range(3),repeat=N) if valid(h)]
counts={}; max_event=0
for s in (1,2,3):
 Q=2*s+5; count=0
 for h in base_cuts:
  for start in range(N-s+1):
   S=tuple(range(start,start+s))
   # Every component has unchanged boundary since s<N.
   # Check every valid lifted local change then uniqueness of its residue image.
   outputs={}
   for delta in itertools.product(range(-s,s+1),repeat=s):
    hh=list(h)
    for i,d in zip(S,delta):hh[i]+=d
    if not valid(hh):continue
    residues=tuple(hh[i]%Q for i in S)
    assert residues not in outputs
    outputs[residues]=hh
    actual={(i,k) for i in S for k in range(min(h[i],hh[i])+1,max(h[i],hh[i])+1)}
    envelope={(i,k) for i in S for k in range(h[i]-s+1,h[i]+s+1)}
    assert actual<=envelope and len(envelope)==2*s*s
    max_event=max(max_event,len(actual));count+=1
   # Exhaust every residue replacement. Every modulo-valid replacement must
   # have exactly the already enumerated anchored lift; this tests wrap cases.
   for res in itertools.product(range(Q),repeat=s):
    rr=[x%Q for x in h]
    for i,x in zip(S,res):rr[i]=x
    if all((rr[a]-rr[b])%Q in (0,1) for a,b in edges):
     assert res in outputs
 counts[str(s)]=count
# Independent numerical coherent retained-clock correction diagnostic.
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex);Y=1j*X@Z
P={'I':I,'X':X,'Y':Y,'Z':Z}
def kron(*xs):
 r=np.ones((1,1),complex)
 for x in xs:r=np.kron(r,x)
 return r
def word(s):return kron(*(P[x] for x in s))
p=np.eye(32,dtype=complex)
for s in ['XZZXI','IXZZX','XIXZZ','ZXIXZ']:p=p@(np.eye(32)+word(s))/2
p0=p@(np.eye(32)+word('ZZZZZ'))/2
v=p0[:,0];v/=np.linalg.norm(v);enc=np.column_stack((v,word('XXXXX')@v))
errors=[np.eye(32,dtype=complex)]
for i in range(5):
 for a in (X,Y,Z):errors.append(kron(*(a if j==i else I for j in range(5))))
frame=np.column_stack([a@enc[:,l] for l in range(2) for a in errors]);decoder=frame.conj().T
# Three coherent output-clock branches carrying X,Y,Z on one physical site.
root=np.vstack([errors[j]@enc/np.sqrt(3) for j in (1,2,3)])
actual=np.kron(np.eye(3),decoder)@root
# Layout clock, logical, syndrome. Check common logical identity while keeping clock.
W=np.zeros((3,16),complex)
for c,j in enumerate((1,2,3)):W[c,j]=1/np.sqrt(3)
expected=np.zeros((3,2,16,2),complex)
for l in range(2):expected[:,l,:,l]=W
res=float(np.linalg.norm(actual-expected.reshape(96,2)))
assert res<1e-12
# The retained auxiliary clock-syndrome state is coherent, not a classical mixture.
w=W.reshape(-1);aux=np.outer(w,w.conj())
off=aux.copy()
for c in range(3):off[c*16:(c+1)*16,c*16:(c+1)*16]=0
result={'valid_base_cuts':len(base_cuts),'checked_valid_local_outputs_by_support_size':counts,'max_symmetric_difference_event_count':max_event,'coherent_clock_retained_decoder_residual':res,'retained_off_diagonal_clock_frobenius_norm':float(np.linalg.norm(off)),'scope':'Finite anchored-cut exhaustive tests and ideal five-qubit common-span diagnostic. No physical clock-compiler, invalid-root repair, or threshold verification.'}
print(json.dumps(result,indent=2))

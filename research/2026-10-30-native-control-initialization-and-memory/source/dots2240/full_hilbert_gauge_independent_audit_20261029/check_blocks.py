"""Independent finite block-matrix regression; not the author's checker."""
import itertools, json, numpy as np
from scipy.linalg import expm
I=np.eye(16,dtype=complex)
X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]); eye=np.eye(2)
def embed(op,q):
    v=np.array([[1]],complex)
    for i in range(4): v=np.kron(v,op if i==q else eye)
    return v
# Qubits W_A,W_B,D_0,D_1. Includes genuinely hub-only ownership-checked gate.
U={h:[expm(-.37j*embed(X,h)),expm(-.29j*embed(Z,h)@embed(X,3)),expm(-.41j*embed(X,h)@embed(Z,2))] for h in range(2)}
target=[0,1,0]
phases=['A0','A1','A2']+[f'C{t}' for t in range(4)]+[f'R{t}' for t in range(4)]+['Q0','Q1','Q2']
locks=list(itertools.product(range(5),repeat=2)) # free, o_A,o_B,z_A,z_B

def V(h,p,m):
    if p[0] not in 'CR': return I
    t=int(p[1:]); v=I
    for e in range(t): v=U[h][e]@v if m[target[e]]==h+1 else I
    return v

def F(ps,m):return V(0,ps[0],m)@V(1,ps[1],m)
res={}; count={}
def check(name,a,b):
    err=float(np.max(np.abs(a-b)));res[name]=max(res.get(name,0),err);count[name]=count.get(name,0)+1
    assert err<1e-12,(name,err)

def edge(h,p,q,m,n,G,want,name):
    for other in phases:
        ps=[other,other];qs=[other,other];ps[h]=p;qs[h]=q
        check(name,F(qs,n).conj().T@G@F(ps,m),want)

for m in locks:
  for ps in itertools.product(phases,repeat=2):
    a,b=V(0,ps[0],m),V(1,ps[1],m)
    check('owner_gauges_commute',a@b,b@a)
    check('frame_unitary',F(ps,m).conj().T@F(ps,m),I)
  for h in range(2):
    for e in range(3):
      if m[target[e]]==h+1:edge(h,f'C{e}',f'C{e+1}',m,m,U[h][e],I,'gates_including_hub_only')
    for t in range(4):
      for j in range(2):
        if m[j]!=h+1:edge(h,f'C{t}',f'R{t}',m,m,I,I,'abort_leaves')
    for j in range(2):
      if m[j]==0:
        n=list(m);n[j]=h+1;n=tuple(n)
        edge(h,f'A{j}',f'A{j+1}',m,n,I,I,'acquisition_mask_changes')
      if m[j]==h+1:
        n=list(m);n[j]=h+3;n=tuple(n)
        for p in phases:
          if p[0]=='Q' or (p[0]=='A' and int(p[1:])<=j):
            edge(h,p,p,m,n,I,I,'cleanup_mask_changes')
      if m[j]==h+3:
        n=list(m);n[j]=0;n=tuple(n)
        for p in phases:edge(h,p,p,m,n,I,I,'unconditional_z_reset')
    edge(h,'A2','C0',m,m,I,I,'commit_frame_identity')
    for p in ['C3']+[f'R{t}' for t in range(4)]+['A0','A1','A2','Q0','Q1','Q2']:
      total=np.zeros_like(I)
      for s in range(2):
        mat=np.zeros((2,2),complex);mat[0,s]=1;K=embed(mat,h)
        v=V(h,p,m)
        edge(h,p,'Q0' if p[0] in 'CR' else p,m,m,K,K@v,'individual_reset_formula')
        total+=(K@v).conj().T@(K@v)
      check('complete_reset_loss',total,I)
report={'max_residuals':res,'checks':count,'total_checks':sum(count.values()),'scope':'all clock/lock basis transition blocks; coherent off-diagonal action follows matrix identities by linearity'}
# Explicit coherent mask cross terms, including an entangled external reference.
from scipy.linalg import block_diag
rng=np.random.default_rng(521)
m,n=(1,1),(1,2); src=('C3','C2');dst=('Q0','C2')
Fs=block_diag(F(src,m),F(src,n));Fd=block_diag(F(dst,m),F(dst,n))
psi=rng.normal(size=64)+1j*rng.normal(size=64);psi/=np.linalg.norm(psi)
rho=np.outer(psi,psi.conj());Fs=np.kron(Fs,eye);Fd=np.kron(Fd,eye)
physical=Fs@rho@Fs.conj().T
out_ph=np.zeros_like(rho);out_formula=np.zeros_like(rho)
for s in range(2):
 mat=np.zeros((2,2),complex);mat[0,s]=1;K=embed(mat,0)
 J=np.kron(block_diag(K,K),eye)
 Jt=np.kron(block_diag(K@V(0,'C3',m),K@V(0,'C3',n)),eye)
 out_ph+=J@physical@J.conj().T
 out_formula+=Jt@rho@Jt.conj().T
out_conjugated=Fd.conj().T@out_ph@Fd
err=float(np.max(np.abs(out_formula-out_conjugated)))
coherence=float(np.linalg.norm(out_formula[:32,32:]))
assert err<1e-12 and coherence>.01
report['coherent_mask_reference_test']={'max_residual':err,'offdiagonal_mask_frobenius_norm':coherence,'output_trace':float(np.trace(out_formula).real),'note':'Mask dephasing would erase a demonstrably nonzero cross block and is NOT equivalent.'}
print(json.dumps(report,indent=2))

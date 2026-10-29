"""Independent finite-dimensional checks; not proof or hardware evidence."""
import json, math, itertools
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
rng=np.random.default_rng(730129)

def partitions(n, cap=None):
    if n==0:
        yield ()
    else:
        for j in range(min(n,cap or n),1-1,-1):
            for tail in partitions(n-j,j): yield (j,)+tail

def swap(n,i,j):
    D=2**n; S=np.zeros((D,D))
    for a in range(D):
        b=a
        if ((a>>i)&1)!=((a>>j)&1): b=a^(1<<i)^(1<<j)
        S[b,a]=1
    return S

def singlets(n):
    D=2**n
    # J^2 = sum_{i<j} SWAP_ij + n(4-n) I/4.
    H=sum(swap(n,i,j) for i in range(n) for j in range(i))+n*(4-n)*np.eye(D)/4
    w,v=eigh(H)
    return v[:,np.abs(w)<1e-8]

def channel(D,r=3):
    A=rng.normal(size=(r,D,D))+1j*rng.normal(size=(r,D,D))
    w,v=eigh(sum(a.conj().T@a for a in A))
    inv=(v/np.sqrt(w))@v.conj().T
    return [a@inv for a in A]

def permutation_unitary(n,p):
    D=2**n; U=np.zeros((D,D))
    for x in range(D): U[sum(((x>>i)&1)<<p[i] for i in range(n)),x]=1
    return U

def average(K,n):
    # Explicit group average only for small independent validation, not implementation.
    return sum(U@K@U.T for U in (permutation_unitary(n,p) for p in itertools.permutations(range(n))))/math.factorial(n)

def evaluate(A,n,E,do_average=False):
    D=2**n; k=E.shape[1]; P=E@E.conj().T
    ds=[]; comms=[]
    for i in range(n):
        for j in range(i):
            S=swap(n,i,j)
            ds.append(float(1-sum(np.trace(S@a.conj().T@S@a).real for a in A)/D))
            comms.append(sum(np.linalg.norm(S@a-a@S,'fro')**2 for a in A)/(2*D))
    # Explicit TP completion: leakage basis mapped to fixed logical |0>.
    w,v=eigh(np.eye(D)-P); B=v[:,w>.5]
    dec=[E.conj().T]+[np.outer(np.eye(k)[:,0],b.conj()) for b in B.T]
    fe=sum(abs(np.trace(d@a@E))**2 for d in dec for a in A)/k**2
    base=sum(abs(np.trace(E.conj().T@a@E))**2 for a in A)/k**2
    bound=D/k*sum(ds)/n
    assert 1-fe <= bound+1e-10
    assert base<=fe+1e-10
    assert np.max(np.abs(np.array(ds)-comms))<1e-10
    out=dict(n=n,K=k,loss=1-fe,bound=bound,commutator_residual=float(np.max(np.abs(np.array(ds)-comms))))
    if do_average:
        avg=[average(a,n) for a in A]
        residual=sum(np.linalg.norm(a-b,'fro')**2 for a,b in zip(A,avg))/D
        assert residual<=sum(ds)/n+1e-10
        out['hs_residual']=residual
    return out

result={}
# Exact integer central-character eigenvalues, all partitions through n=24.
gaps=[]
for n in range(2,25):
    gaps.append(min(n*(n-1)//2-sum(j-i for i,row in enumerate(p) for j in range(row)) for p in partitions(n) if p!=(n,)))
assert gaps==list(range(2,25)); result['exact_partition_gaps_n2_to24']=gaps
result['random_cptp']=[]
for n in [2,4,6]:
    V=singlets(n); k=2**int(math.floor(math.log2(V.shape[1]))); E=V[:,:k]
    for _ in range(3): result['random_cptp'].append(evaluate(channel(2**n),n,E,n<=4))
# Nontrivial near-identity arbitrary CPTP channels (not only vacuous >1 bounds).
for n in [4,6]:
    V=singlets(n); E=V[:,:2**int(math.floor(math.log2(V.shape[1])))]; eta=1e-3
    A=[np.sqrt(1-eta)*np.eye(2**n)]+[np.sqrt(eta)*a for a in channel(2**n)]
    result.setdefault('near_identity',[]).append(evaluate(A,n,E))
# Physical ancilla controlled-SWAP density simulation, including nonunital N.
n=2; D=4; S=swap(n,0,1); A=channel(D)
C=np.block([[np.eye(D),np.zeros((D,D))],[np.zeros((D,D)),S]])
rho=np.kron(np.ones((2,2))/2,np.eye(D)/D)
rho=C@rho@C
rho=sum(np.kron(np.eye(2),a)@rho@np.kron(np.eye(2),a.conj().T) for a in A)
rho=C@rho@C
minus=np.array([[1,-1],[-1,1]])/2
q=np.trace(np.kron(minus,np.eye(D))@rho).real
delta=1-sum(np.trace(S@a.conj().T@S@a).real for a in A)/D
assert abs(q-delta/2)<1e-12
result['physical_test']={'p_minus':q,'delta_over_2':delta/2}
# Subcode trace equality counterexample: U=-1 on one selected singlet, +1 elsewhere.
n=6; D=64; V=singlets(n); E=V[:,:4]; U=np.eye(D)-2*np.outer(V[:,0],V[:,0].conj())
# Singlet scalar of permutation average is sector trace / dim=3/5; subcode trace / dim=1/2.
a=np.trace(V.conj().T@U@V).real/5
b=np.trace(E.conj().T@U@E).real/4
assert abs(a-.6)<1e-12 and abs(b-.5)<1e-12
result['subcode_trace_equality_counterexample']={'twirled_scalar':a,'subcode_scalar':b,**evaluate([U],n,E)}
# Rare-sector controlled-Z obstruction on n=6, using spectator two-qubit singlet.
s=np.array([0,1,-1,0])/np.sqrt(2); Pi=np.outer(s,s)
Z=np.diag([1,-1]); Ztarget=np.kron(np.eye(8),Z)
U=np.kron(np.eye(16),np.eye(4)-Pi)+np.kron(Ztarget,Pi)
V=singlets(6); E=V[:,:4]
result['rare_sector']=evaluate([U],6,E)
result['all_assertions_passed']=True
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
# Independent Pauli twirl through actual completed decoder Kraus, K=2 and K=4.
P1=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
result['retired_key_twirl']=[]
for n in [4,6]:
    V=singlets(n); k=2**int(math.floor(math.log2(V.shape[1]))); E=V[:,:k]; D=2**n
    A=channel(D); w,v=eigh(np.eye(D)-E@E.conj().T); B=v[:,w>.5]
    dec=[E.conj().T]+[np.outer(np.eye(k)[:,0],b.conj()) for b in B.T]
    L=[d@a@E for d in dec for a in A]
    ps=[]
    for seq in itertools.product(P1,repeat=int(math.log2(k))):
        p=np.array([[1.]])
        for v in seq: p=np.kron(p,v)
        ps.append(p)
    J=sum(np.outer(l.reshape(-1),l.reshape(-1).conj()) for l in L)/k
    Jt=sum(np.outer((p.conj().T@l@p).reshape(-1),(p.conj().T@l@p).reshape(-1).conj()) for l in L for p in ps)/(k*len(ps))
    phi=np.eye(k).reshape(-1)/np.sqrt(k); fe=np.vdot(phi,J@phi).real
    bell=np.stack([p.reshape(-1)/np.sqrt(k) for p in ps],axis=1)
    jbell=bell.conj().T@Jt@bell
    off=np.linalg.norm(jbell-np.diag(np.diag(jbell)))
    tracedist=np.abs(eigh(Jt-np.outer(phi,phi),eigvals_only=True)).sum()/2
    assert off<1e-12 and abs(tracedist-(1-fe))<1e-12
    result['retired_key_twirl'].append(dict(K=k,offdiagonal_norm=float(off),bell_loss=float(1-fe),choi_half_trace_distance=float(tracedist)))
# Finite confidence coverage enumeration (not an inferential approximation).
from scipy.stats import beta, binom
worst=0.
for m in [1,2,5,10,20,60]:
    alpha=.05; limits=np.array([beta.ppf(1-alpha,r+1,m-r) if r<m else 1 for r in range(m+1)])
    assert abs(limits[0]-(1-alpha**(1/m)))<1e-12
    for q in np.linspace(0,1,1001):
        bad=binom.pmf(np.arange(m+1),m,q)[limits<q].sum()
        worst=max(worst,bad)
assert worst<=.05+1e-12
result['binomial_grid_max_undercoverage_probability']=float(worst)
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print('Additional twirl and confidence checks passed')

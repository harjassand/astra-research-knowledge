import numpy as np, json
from itertools import product
rng=np.random.default_rng(76124)
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]).astype(complex)
H=(X+Z)/np.sqrt(2); T=np.diag([1,np.exp(1j*np.pi/4)])
def kron(*xs):
    v=np.array([[1]],complex)
    for x in xs:v=np.kron(v,x)
    return v
def op(n,site,a):return kron(*[a if j==site else I for j in range(n)])
def swap(n,a,b):
    s=np.zeros((2**n,2**n),complex)
    for j in range(2**n):
        bs=[(j>>(n-1-i))&1 for i in range(n)]
        bs[a],bs[b]=bs[b],bs[a]
        i=sum(z<<(n-1-k) for k,z in enumerate(bs));s[i,j]=1
    return s
def reset(rho,n,site,state):
    out=np.zeros_like(rho)
    for b in range(2):
        leaf=np.outer(state,np.eye(2)[b]);k=op(n,site,leaf);out+=k@rho@k.conj().T
    return out
def transfer(rho,n,a,b,u):
    r=reset(rho,n,b,np.array([1,0]));s=swap(n,a,b);r=s@r@s.conj().T
    v=op(n,b,u);return v@r@v.conj().T

def partial(rho,n,keep):
    keep=list(keep);drop=[i for i in range(n) if i not in keep]
    rr=rho.reshape([2]*2*n).transpose(keep+drop+[n+i for i in keep]+[n+i for i in drop])
    rr=rr.reshape(2**len(keep),2**len(drop),2**len(keep),2**len(drop))
    return np.einsum('aibi->ab',rr)
def trace_distance(a,b):return float(np.linalg.svd(a-b,compute_uv=False).sum()/2)
# Reference R, old bank A, bank B, final bank C.
psi=np.zeros(16,complex);psi[0]=psi[12]=1/np.sqrt(2);rho=np.outer(psi,psi.conj())
r=transfer(rho,4,1,2,H);r=transfer(r,4,2,3,T)
base=partial(r,4,[0,3]);r_replay=r.copy()
for _ in range(30):r_replay=transfer(r_replay,4,1,2,H)
late_replay=trace_distance(base,partial(r_replay,4,[0,3]))
# A replay before consumption is a genuine live-wire error.
r_early=transfer(rho,4,1,2,H);r_early=transfer(r_early,4,1,2,H);r_early=transfer(r_early,4,2,3,T)
early_replay=trace_distance(base,partial(r_early,4,[0,3]))
# Three-vertex graph-state pumps.
n=3;ug=np.eye(8,dtype=complex)
for a,b in [(0,1),(1,2)]:
    diag=[]
    for j in range(8):diag.append(-1 if ((j>>(2-a))&1) and ((j>>(2-b))&1) else 1)
    ug=np.diag(diag)@ug
plus=np.array([1,1])/np.sqrt(2);K=[];pumps=[]
for v in range(n):
    kv=ug@op(n,v,X)@ug.conj().T;pp=(np.eye(8)+kv)/2;pm=(np.eye(8)-kv)/2
    pumps.append([pp,op(n,v,Z)@pm]);K.append(kv)
def ch(r,ks):return sum((a@r@a.conj().T for a in ks),np.zeros_like(r))
v=rng.normal(size=8)+1j*rng.normal(size=8);v/=np.linalg.norm(v);test=np.outer(v,v.conj())
conjugacy=max(trace_distance(ch(test,pumps[v]),ug@reset(ug.conj().T@test@ug,n,v,plus)@ug.conj().T) for v in range(n))
commute=max(trace_distance(ch(ch(test,pumps[a]),pumps[b]),ch(ch(test,pumps[b]),pumps[a])) for a,b in product(range(n),repeat=2))
graph=ug@kron(plus[:,None],plus[:,None],plus[:,None]);graph=graph@graph.conj().T
r=test.copy()
for v in [2,0,1]:r=ch(r,pumps[v])
prep=trace_distance(r,graph)
# Inject arbitrary unknown input at qubit 0; pump at qubit 1 originally stabilizes CZ(|psi>|+>).
# After measuring 0 in X, pump 1 no longer preserves the teleported output.
q=np.array([np.sqrt(.3),1j*np.sqrt(.7)]);cz=np.diag([1,1,1,-1]);s=cz@kron(q[:,None],plus[:,None]);r=s@s.conj().T
m=kron((I+X)/2,I);post=m@r@m;post/=np.trace(post)
k1=kron(Z,X);ks=[(np.eye(4)+k1)/2,kron(I,Z)@(np.eye(4)-k1)/2]
frontier=trace_distance(partial(post,2,[1]),partial(ch(post,ks),2,[1]))
res={'late_replay_reference_output_trace_distance':late_replay,'early_replay_reference_output_trace_distance':early_replay,'graph_pump_conjugacy_residual':conjugacy,'graph_pump_commutator_residual':commute,'one_application_each_graph_preparation_residual':prep,'pump_left_on_at_measured_frontier_output_trace_distance':frontier}
assert late_replay<1e-12 and early_replay>.4 and conjugacy<1e-12 and commute<1e-12 and prep<1e-12 and frontier>.1
print(json.dumps(res,indent=2))

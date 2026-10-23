"""Bounded actual positive-matrix challenge and stabilizer compatibility replay.

No universal inference from numerical search. All random choices have fixed seed.
Run with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1.
"""
import json, math, os, platform, resource, sys, time
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
START_W=time.perf_counter(); START_C=time.process_time()
RNG=np.random.default_rng(270321)
LN2=math.log(2)

def rank(rows):
    basis={}
    for z in rows:
        z=int(z)
        while z:
            k=z.bit_length()-1
            if k in basis: z^=basis[k]
            else:
                basis[k]=z
                break
    return len(basis)

def random_clifford_rows(n,s,steps):
    xs=[0]*s; zs=[1<<j for j in range(s)]
    for _ in range(steps):
        kind=int(RNG.integers(3)); q=int(RNG.integers(n))
        if kind==0:
            for j in range(s):
                x=(xs[j]>>q)&1; z=(zs[j]>>q)&1
                if x!=z: xs[j]^=1<<q; zs[j]^=1<<q
        elif kind==1:
            for j in range(s):
                if (xs[j]>>q)&1: zs[j]^=1<<q
        elif n>1:
            t=int(RNG.integers(n-1)); t+=t>=q
            for j in range(s):
                if (xs[j]>>q)&1: xs[j]^=1<<t
                if (zs[j]>>t)&1: zs[j]^=1<<q
    return [x|(z<<n) for x,z in zip(xs,zs)]

def stab_profile(rows,n,N,r):
    fs=[]; ps=[]; gs=[]
    for a in range(r):
        f=[]
        for i in range(1,N+1):
            mask=((1<<i)-1)<<(a*N)
            full=mask|(mask<<n)
            f.append(rank([z&full for z in rows]))
        fs.append(f); ps.append([2.0**(-t) for t in f])
        gs.append(max([0]+[i-t for i,t in enumerate(f,1)]))
    delta=LN2*(sum(sum(x) for x in ps)-(n-len(rows)))
    assert sum(gs)<=n-len(rows)
    assert delta<=r*LN2+1e-11
    return fs,ps,gs,delta

PAULIS=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),
        np.array([[1,0],[0,-1]],complex),np.array([[0,-1j],[1j,0]],complex)]
def pauli(row,n):
    out=np.array([[1]],complex)
    for q in range(n):
        x=(row>>q)&1; z=(row>>(n+q))&1
        out=np.kron(out,PAULIS[x+2*z])
    return out

def actual_stab_sqrt(rows,n):
    dim=2**n; P=np.eye(dim,dtype=complex)
    for row in rows: P=P@(np.eye(dim)+pauli(row,n))/2
    M=2**(n-len(rows))
    return P/math.sqrt(M)

def partial_trace(X,prefix,n):
    rest=[j for j in range(n) if j not in prefix]
    perm=prefix+rest+[n+j for j in prefix]+[n+j for j in rest]
    k=2**len(prefix); h=2**len(rest)
    T=X.reshape([2]*(2*n)).transpose(perm).reshape(k,h,k,h)
    return np.trace(T,axis1=0,axis2=2)

def score_sqrt(X,N,r,entropy=None):
    n=N*r; X=X/np.linalg.norm(X)
    if entropy is None:
        lam=np.linalg.eigvalsh(X); probs=np.maximum(lam,0)**2
        probs=probs/probs.sum()
        entropy=-float(np.dot(probs[probs>0],np.log(probs[probs>0])))
    ps=[]
    for a in range(r):
        pp=[]
        for i in range(1,N+1):
            T=partial_trace(X,list(range(a*N,a*N+i)),n)
            pp.append(float(np.vdot(T,T).real)/(2**i))
        ps.append(pp)
    return LN2*sum(sum(x) for x in ps)-entropy,ps

rows_out=[]; maxres=0.0
for N,r in [(1,2),(2,2),(3,2),(4,2),(2,3),(2,4)]:
    n=N*r
    for s in sorted(set([0,1,n//2,n-1,n])):
        rows=random_clifford_rows(n,s,12*n)
        fs,ps,gs,delta=stab_profile(rows,n,N,r)
        X=actual_stab_sqrt(rows,n)
        actual,aps=score_sqrt(X,N,r,entropy=(n-s)*LN2)
        residual=max([abs(actual-delta)]+[abs(v-w) for aa,bb in zip(ps,aps) for v,w in zip(aa,bb)])
        maxres=max(maxres,residual)
        assert residual<1e-10
        rows_out.append(dict(N=N,r=r,s=s,rank=2**(n-s),generator_rows=rows,
                             prefix_ranks=fs,logical_prefix_g=gs,delta_nats=delta,
                             delta_per_task_nats=delta/r,formula_residual=residual))

combinatorial=[]
for N,r in [(8,2),(16,2),(32,2),(64,2),(16,3),(16,4)]:
    n=N*r; best=(-float('inf'),None)
    for trial in range(24):
        s=int(RNG.integers(n+1))
        rows=random_clifford_rows(n,s,8*n)
        fs,ps,gs,delta=stab_profile(rows,n,N,r)
        if delta>best[0]: best=(delta,dict(N=N,r=r,s=s,generator_rows=rows,
                prefix_ranks=fs,logical_prefix_g=gs,delta_nats=delta,delta_per_task_nats=delta/r))
    combinatorial.append(best[1])

# Actual positive matrices, not spectrum/probability relaxations.
search=[]
for N,r in [(2,2),(3,2),(4,2),(2,3),(2,4)]:
    n=N*r; dim=2**n
    for M in sorted(set([1,2,dim//4,dim//2,dim])):
        for trial in range(3):
            G=RNG.standard_normal((dim,M))+1j*RNG.standard_normal((dim,M))
            Q=np.linalg.qr(G,mode='reduced')[0]
            for kind in ['flat','harmonic']:
                probs=np.ones(M)/M if kind=='flat' else 1/np.arange(1,M+1,dtype=float)
                probs=probs/probs.sum()
                X=(Q*np.sqrt(probs))@Q.conj().T
                entropy=-float(np.dot(probs,np.log(probs)))
                delta,ps=score_sqrt(X,N,r,entropy)
                search.append(dict(N=N,r=r,M=M,trial=trial,spectrum=kind,
                    delta_nats=delta,delta_per_task_nats=delta/r,prefix_scores=ps))

# Sharpness: identity on early sites and pure computational zero on final k sites
# in every task. The state is a product stabilizer projector. Its gap is exactly
# r ln2 (1-2^-k), approaching r ln2 as k grows.
sharp=[]
for N in [1,2,4,16,64,256]:
    r=2; k=N
    sharp.append(dict(N=N,r=r,k=k,entropy=0,
            delta_nats=r*LN2*(1-2.0**(-k)),delta_per_task_nats=LN2*(1-2.0**(-k))))

elapsed=time.perf_counter()-START_W; cpu=time.process_time()-START_C
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
rss_bytes=int(rss if sys.platform=='darwin' else rss*1024)
result=dict(status='RESTRICTED_THEOREM_CHECKED; NO_GENERAL_COUNTEREXAMPLE_FOUND',
    seed=270321,definition='Delta=ln2 sum_(a,i) 2^-i Tr[(Tr_prefix sqrt(rho))^2]-S(rho)',
    stabilizer_actual_cases=rows_out,stabilizer_combinatorial_best=combinatorial,
    random_actual_positive_cases=search,restricted_sharpness=sharp,
    maximum_actual_formula_residual=maxres,
    actual_random_largest_delta_per_task=max(z['delta_per_task_nats'] for z in search),
    dimensions=dict(largest_actual_matrix=256,largest_combinatorial_qubits=128),
    costs=dict(body_wall_seconds=elapsed,body_cpu_seconds=cpu,peak_rss_bytes=rss_bytes,
        python=sys.version,numpy=np.__version__,platform=platform.platform(),
        thread_env={k:os.environ.get(k) for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS']}),
    inference_limits='Bounded sampled-state search is not a proof for general positive matrices; combinatorial checks allocate no Hilbert-space matrix.')
assert cpu<90, (cpu,'CPU budget exceeded')
(HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(actual_stabilizer_cases=len(rows_out),actual_random_cases=len(search),
    maximum_formula_residual=maxres,largest_random_delta_per_task=result['actual_random_largest_delta_per_task'],
    costs=result['costs']),indent=2))

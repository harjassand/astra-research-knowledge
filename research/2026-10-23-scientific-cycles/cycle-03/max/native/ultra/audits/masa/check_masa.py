"""Finite quantum check of group-GHZ invariant MASA / nonlinear coordinate proof.
No optimization or asymptotic empirical claim. Run single-thread BLAS.
"""
import itertools, json, math, os, platform, resource, time
from pathlib import Path
import numpy as np
start=time.perf_counter(); cpu=time.process_time()
HERE=Path(__file__).resolve().parent
# S_3 multiplication (permutation composition), not cyclic group addition.
group=list(itertools.permutations(range(3))); D=len(group); ell=3
index={g:i for i,g in enumerate(group)}
def mul(a,b): return index[tuple(group[a][group[b][i]] for i in range(3))]
identity=index[(0,1,2)]
def inv(a): return next(b for b in range(D) if mul(a,b)==identity and mul(b,a)==identity)
noncommuting=next((a,b) for a in range(D) for b in range(D) if mul(a,b)!=mul(b,a))
labels=list(itertools.product(range(D),repeat=ell)) # (a2,a3,c)
physical=list(itertools.product(range(D),repeat=ell)); flat={x:j for j,x in enumerate(physical)}
q=D**ell; U=np.zeros((q,q),complex)
for j,(a,b,c) in enumerate(labels):
    for g in range(D):
        U[flat[(g,mul(g,a),mul(g,b))],j]=np.exp(2j*np.pi*c*g/D+0.137j*(a+1)*(b+2)*(g+1)**2)/math.sqrt(D)
orth=float(np.max(np.abs(U.conj().T@U-np.eye(q))))
# Explicit nonlinear spectral-label coordinates from proof.
y=[(c,mul(c,a),mul(c,b)) for a,b,c in labels]
assert len(set(y))==q
subsets=[s for k in range(ell+1) for s in itertools.combinations(range(ell),k)]
def erasure(X,S):
    # Partial trace, then reinsert I_S / D^|S|, using ordinary matrix units.
    keep=tuple(i for i in range(ell) if i not in S)
    red=np.zeros((D**len(keep),D**len(keep)),complex)
    keep_index={x:i for i,x in enumerate(itertools.product(range(D),repeat=len(keep)))}
    for u in physical:
        for v in physical:
            if all(u[i]==v[i] for i in S):
                red[keep_index[tuple(u[i] for i in keep)],keep_index[tuple(v[i] for i in keep)]]+=X[flat[u],flat[v]]
    out=np.zeros_like(X)
    for u in physical:
        for v in physical:
            if all(u[i]==v[i] for i in S):
                out[flat[u],flat[v]]=red[keep_index[tuple(u[i] for i in keep)],keep_index[tuple(v[i] for i in keep)]]/(D**len(S))
    return out
# Compute true erasure cells directly from the remaining computational support.
def support_key(label,S):
    a,b,c=label; aa=(identity,a,b); keep=tuple(i for i in range(ell) if i not in S)
    if not S: return ('individual',label)
    return tuple(sorted(tuple(mul(g,aa[i]) for i in keep) for g in range(D)))
partitions={}
for S in subsets:
    cells={}
    for j,L in enumerate(labels): cells.setdefault(support_key(L,S),[]).append(j)
    partitions[S]=list(cells.values())
    for cell in cells.values():
        expected=1 if not S else D**ell if len(S)==ell else D**(len(S)+1)
        assert len(cell)==expected
    # Every ordinary S-coordinate fiber is contained in one actual erasure cell.
    keep=tuple(i for i in range(ell) if i not in S); seen={}
    for j in range(q):
        key=tuple(y[j][i] for i in keep); ckey=support_key(labels[j],S)
        assert key not in seen or seen[key]==ckey
        seen[key]=ckey
max_quantum_residual=0.
for S in subsets:
    for j in (0,37,q-1):
        p=np.outer(U[:,j],U[:,j].conj())
        actual=erasure(p,S)
        cell=next(c for c in partitions[S] if j in c)
        predicted=U[:,cell]@U[:,cell].conj().T/len(cell)
        max_quantum_residual=max(max_quantum_residual,float(np.max(np.abs(actual-predicted))))
# Test the common-cell stochastic projections and domination on correlated spectra.
rng=np.random.default_rng(314159)
max_kernel_idempotence=0.; max_kernel_commuting_union=0.; max_projection_domination=-math.inf
kernels={}
for S in subsets:
    K=np.zeros((q,q))
    for cell in partitions[S]: K[np.ix_(cell,cell)]=1/len(cell)
    kernels[S]=K
    max_kernel_idempotence=max(max_kernel_idempotence,float(np.max(np.abs(K@K-K))))
for S in subsets:
    for T in subsets:
        union=tuple(sorted(set(S)|set(T)))
        max_kernel_commuting_union=max(max_kernel_commuting_union,float(np.max(np.abs(kernels[S]@kernels[T]-kernels[union]))))
for trial in range(20):
    f=np.sqrt(rng.dirichlet(np.full(q,.3))); assert abs(np.dot(f,f)-1)<1e-12
    for S in subsets:
        score=float(np.dot(kernels[S]@f,kernels[S]@f))
        keep=tuple(i for i in range(ell) if i not in S); fibers={}
        for j in range(q): fibers.setdefault(tuple(y[j][i] for i in keep),[]).append(j)
        classical=sum(float(np.sum(f[c])**2/len(c)) for c in fibers.values())
        max_projection_domination=max(max_projection_domination,score-classical)
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
out={
 'scope':'S3 order-6 group, 3 physical sites, 216-dimensional ACTUAL basis; no global optimization',
 'tuple_dependent_hadamard':'F6 with independent support-dependent column phases exp[.137i(a+1)(b+2)(g+1)^2]',
 'group_order':D,'block_sites':ell,'basis_dimension':q,'basis_orthogonality_max_error':orth,
 'noncommuting_pair':list(noncommuting),'sample_projectors_per_erasure':3,
 'erasure_subsets':len(subsets),'max_actual_quantum_erasure_vs_cell_residual':max_quantum_residual,
 'max_kernel_idempotence_error':max_kernel_idempotence,
 'max_kernel_commuting_union_error':max_kernel_commuting_union,
 'coordinate_fiber_containment':'EXACT integer group check for all labels and all erasures',
 'random_correlated_spectra_tested':20,
 'max_actual_minus_coordinate_score':max_projection_domination,
 'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,
 'peak_rss_bytes':int(rss if platform.system()=='Darwin' else rss*1024),
 'python':platform.python_version(),'numpy':np.__version__,
 'threads':{k:os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')},
 'total_research_cost':'UNKNOWN; these costs are this verification script only',
}
assert orth<1e-12 and max_quantum_residual<1e-12 and max_kernel_idempotence<1e-12 and max_kernel_commuting_union<1e-12 and max_projection_domination<1e-12
(HERE/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

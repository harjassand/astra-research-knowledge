#!/usr/bin/env python3
"""Admission/replay checks, not a numerical proof of the invariant-MASA theorem."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import itertools, json, math, platform, resource, sys, time
from pathlib import Path
import numpy as np

wall=time.perf_counter(); cpu=time.process_time()

def ptrace(a, sites, n, D=2):
    t=a.reshape([D]*(2*n)); cur=n
    for s in sorted(sites,reverse=True):
        t=np.trace(t,axis1=s,axis2=s+cur); cur-=1
    return t.reshape(D**cur,D**cur)

def bell(a,c,theta):
    v=np.zeros(4,complex)
    v[a]=1/math.sqrt(2)
    v[2+(1^a)]=(-1)**c*np.exp(1j*theta[a])/math.sqrt(2)
    return v

# Two Bell-type factors paired across a balanced A0 A1 : B0 B1 cut.
# Arbitrary relative phases make this a non-Pauli-stabilizer admission example.
vectors=[]
for a,c,b,e in itertools.product(range(2),repeat=4):
    v=np.kron(bell(a,c,[0.17,0.61]),bell(b,e,[0.29,0.83]))
    vectors.append(v.reshape(2,2,2,2).transpose(0,2,1,3).reshape(16))
V=np.column_stack(vectors)
assert np.linalg.norm(V.conj().T@V-np.eye(16))<1e-12
P=np.array([np.outer(v,v.conj()) for v in vectors])
kernels={}
max_projector_error=0.0
for mask in range(16):
    S=tuple(i for i in range(4) if mask>>i&1)
    red=np.array([ptrace(p,S,4) for p in P]).reshape(16,-1)
    K=(red.conj()@red.T).real/2**len(S)
    assert np.max(abs(K.imag if np.iscomplexobj(K) else 0))<1e-12
    err=float(np.linalg.norm(K@K-K))
    max_projector_error=max(max_projector_error,err)
    assert err<1e-12
    assert np.max(abs(K.sum(axis=0)-1))<1e-12
    kernels[frozenset(S)]=K
for S,K in kernels.items():
    for T,J in kernels.items():
        assert np.linalg.norm(K@J-kernels[S|T])<1e-12
max_cut_error=max(float(np.linalg.norm(ptrace(p,(2,3),4)-np.eye(4)/4)) for p in P)
assert max_cut_error<1e-12

def coordinates(side):
    labels=[]
    for s in side:
        K=kernels[frozenset(set(side)-{s})]
        cells=[tuple(np.flatnonzero(row>1e-10)) for row in K]
        unique={cell:k for k,cell in enumerate(sorted(set(cells)))}
        assert len(unique)==4
        labels.append([unique[cell] for cell in cells])
    Y=np.array(labels).T
    assert len({tuple(y) for y in Y})==16
    err=0.0
    for count in range(len(side)+1):
        for S in itertools.combinations(side,count):
            outside=[j for j,s in enumerate(side) if s not in S]
            A=np.array([[float(np.array_equal(Y[j,outside],Y[k,outside]))/4**len(S)
                         for k in range(16)] for j in range(16)])
            err=max(err,float(np.linalg.norm(A-kernels[frozenset(S)])))
    assert err<1e-12
    return Y.tolist(),err
YL,errL=coordinates((0,1)); YR,errR=coordinates((2,3))

# Sparse product-partition admission at N=8. No 65536-square matrix is made.
# The two sides have identical scores in this example; their coordinate
# interpretations remain separate in the general theorem.
D=2; Q=D*D; N=8
C=min(2*Q-math.log(Q),math.log(Q)/(1-Q**(-0.5))**2)
rng=np.random.default_rng(20261022)
families=[]
for kind in ('uniform','point','random','sparse16','sparse1024'):
    f=np.zeros(Q**N)
    if kind=='uniform': f[:]=1
    elif kind=='point': f[0]=1
    elif kind=='random': f=rng.random(Q**N)
    else:
        rank=int(kind.removeprefix('sparse'))
        f[rng.choice(len(f),rank,replace=False)]=rng.random(rank)
    f/=np.linalg.norm(f)
    p=f*f; entropy=-float(np.sum(p[p>0]*np.log(p[p>0])))
    t=f.reshape([Q]*N)
    scores=[float(np.sum(np.sum(t,axis=tuple(range(i)))**2)/Q**i) for i in range(1,N+1)]
    deficit=2*math.log(D)*sum(scores)-entropy
    assert deficit<=C+1e-11
    families.append({'kind':kind,'entropy_nats':entropy,'one_side_prefix_scores':scores,
                     'two_side_entropy_deficit_nats':deficit})

rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
if sys.platform!='darwin': rss*=1024
out={'status':'PASS','scope':'Finite admission checks; analytic theorem is in PROOF.txt',
     'dense_example':{'D':2,'r':2,'N':2,'all_erasure_subsets':16,
       'max_kernel_projection_error':max_projector_error,
       'max_balanced_cut_reduction_error':max_cut_error,
       'left_D_squared_coordinates':YL,'right_D_squared_coordinates':YR,
       'max_coordinate_kernel_error':max(errL,errR)},
     'sparse_example':{'D':D,'r':2,'N':N,'spectral_labels':Q**N,
       'C_D_squared':C,'families':families},
     'measured':{'body_wall_seconds':time.perf_counter()-wall,
       'body_cpu_seconds':time.process_time()-cpu,'peak_rss_bytes':rss},
     'environment':{'python':platform.python_version(),'numpy':np.__version__,
       'blas_threads':1},
     'unmeasured_total_discovery_cost':'UNKNOWN'}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'measured':out['measured'],
                  'max_projection_error':max_projector_error}))

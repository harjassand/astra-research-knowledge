import itertools, json
import numpy as np

rng=np.random.default_rng(713049)
n=6
triples=list(itertools.combinations(range(n),3))
idx={t:i for i,t in enumerate(triples)}
full=set(range(n))
dualidx=[idx[tuple(sorted(full-set(t)))] for t in triples]
matidx=[]
for i in range(n):
    others=[j for j in range(n) if j!=i]
    M=np.full((5,5),-1,dtype=int)
    for a,b in itertools.combinations(range(5),2):
        M[a,b]=M[b,a]=idx[tuple(sorted((i,others[a],others[b])))]
    matidx.append(M)
def derivative_matrices(c):
    A=c[:, np.maximum(np.array(matidx),0)]
    A*=np.array(matidx)[None]>=0
    return A

accepted=0
for roundnum in range(40):
    c=rng.integers(1,5,size=(2500,20))
    eigen=np.linalg.eigvalsh(derivative_matrices(c))
    good=np.max(eigen[:,:,-2],axis=1)<-1e-7
    accepted+=int(good.sum())
    if not good.any(): continue
    cand=c[good]
    deigen=np.linalg.eigvalsh(derivative_matrices(cand[:,dualidx]))
    bad=np.max(deigen[:,:,-2],axis=1)>1e-6
    if bad.any():
        k=int(np.flatnonzero(bad)[0])
        out={'triples':[list(t) for t in triples], 'coefficients':cand[k].tolist(),
             'p_derivative_eigenvalues':np.linalg.eigvalsh(derivative_matrices(cand[k:k+1]))[0].tolist(),
             'dual_derivative_eigenvalues':deigen[k].tolist(), 'accepted_before':accepted}
        print(json.dumps(out,indent=2))
        break
else:
    print(json.dumps({'result':'NO_COUNTEREXAMPLE_FOUND','trials':100000,'accepted':accepted}))

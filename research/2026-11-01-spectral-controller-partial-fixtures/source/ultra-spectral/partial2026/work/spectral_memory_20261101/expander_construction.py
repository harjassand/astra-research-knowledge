"""An exact LPS Cayley graph and its bipartite double cover.

The construction is finite arithmetic. Sparse eigenvalues below are
floating diagnostics; the family input is the cited LPS theorem.
"""
from __future__ import annotations
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,bmat
from scipy.sparse.linalg import eigsh

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/spectral_memory_20261101'


def canonical(a,q):
    a=tuple(v%q for v in a);v=next(v for v in a if v)
    inv=pow(v,-1,q);return tuple((v*inv)%q for v in a)
def mul(a,b,q):
    return canonical((a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],
                      a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3]),q)


def main():
    p=17;q=13;sqrt_minus_one=5
    assert sqrt_minus_one**2%q==q-1 and pow(p,(q-1)//2,q)==1
    generators=[];quaternions=[]
    for a0 in (1,3):
        for a1,a2,a3 in itertools.product(range(-4,5,2),repeat=3):
            if a0*a0+a1*a1+a2*a2+a3*a3!=p:continue
            quaternions.append((a0,a1,a2,a3))
            generators.append(canonical((a0+sqrt_minus_one*a1,a2+sqrt_minus_one*a3,
                                         -a2+sqrt_minus_one*a3,a0-sqrt_minus_one*a1),q))
    assert len(set(generators))==18
    ident=canonical((1,0,0,1),q);vertices=[ident];index={ident:0};queue=deque([ident])
    adjacency=[]
    while queue:
        a=queue.popleft();neighbors=[]
        for g in generators:
            ag=mul(a,g,q)
            if ag not in index:
                index[ag]=len(vertices);vertices.append(ag);queue.append(ag)
            neighbors.append(index[ag])
        adjacency.append(neighbors)
    n=len(vertices);assert n==q*(q*q-1)//2==1092
    assert all(len(set(a))==18 and i not in a for i,a in enumerate(adjacency))
    assert all(i in adjacency[j] for i,a in enumerate(adjacency) for j in a)
    row=np.repeat(np.arange(n),18);col=np.array(adjacency,dtype=int).ravel()
    A=csr_matrix((np.ones(len(row)),(row,col)),shape=(n,n))
    upper=np.sort(eigsh(A,k=3,which='LA',return_eigenvectors=False))
    lower=np.sort(eigsh(A,k=2,which='SA',return_eigenvectors=False))
    diagnostic=max(abs(float(upper[-2])),abs(float(lower[0])))
    assert diagnostic<2*np.sqrt(17)+1e-8
    doubled=[[n+j for j in a] for a in adjacency]+[list(a) for a in adjacency]
    nn=2*n
    assert all(all((j<n)!=(i<n) for j in a) for i,a in enumerate(doubled))
    # Exact rational constants from lambda_2<=17/2 and |S|<=n/72.
    # Cut >=(18-17/2-18/72)|S|=37|S|/4.
    out={'family':'LPS p=17, q=13 PSL(2,q), then bipartite double cover',
         'p':p,'q':q,'quaternion_generators':quaternions,
         'base_vertices':n,'vertices':nn,'degree':18,
         'adjacency':doubled,'bipartition':[list(range(n)),list(range(n,nn))],
         'controllers_per_data':9,'total_qubits':10*nn,'controller_frequencies_in_J':[4*r for r in range(1,10)],
         'base_nontrivial_eigenvalue_diagnostic':diagnostic,'primary_family_bound':'2 sqrt(17) < 17/2',
         'small_set_fraction':'1/72','cut_per_reduced_weight_lower':'37/4',
         'active_centers_per_cut_lower':'1/333',
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'scope':'Exact finite graph and primitive layout; floating spectral diagnostic; no dynamical simulation, useful threshold, or device validation'}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'expander_construction.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(path),'passed':True,'data_qubits':nn,'physical_qubits':10*nn,
                     'spectral_diagnostic':diagnostic}))


if __name__=='__main__':main()

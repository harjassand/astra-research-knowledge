#!/usr/bin/env python3
"""CONSTRUCTOR ONLY. Numerics may propose an integer Gram witness;
           verify_gram_k5.py proves it without numerical eigenvalues.
"""
import numpy as np
import json
from pathlib import Path
from verify_replica_exact import shapes

SCALE=400
S=1<<18
DELTA=8

def construct_integer_matrix(w):
    k=len(w);n=2*k
    states=[s for s in range(1<<n) if s.bit_count()==k]
    lookup={st:i for i,st in enumerate(states)}
    M=np.zeros((len(states),len(states)),dtype=np.int64)
    def insert_bond(i,j,j400):
        assert j400%4==0
        for st in states:
            idx=lookup[st]
            if ((st>>i)^(st>>j))&1:
                M[idx,idx]-=j400//4
                M[lookup[st^(1<<i)^(1<<j)],idx]+=j400//2
            else:M[idx,idx]+=j400//4
    for i in range(k):
        for j in range(i):
            j400=int(200*w[i][j])
            if j400:
                insert_bond(i,j,j400);insert_bond(k+i,k+j,j400)
    for i in range(k):
        for j in range(k):
            j400=-400*(i==j)-int(200*w[i][j])
            if j400:insert_bond(i,k+j,j400)
    M[np.diag_indices(len(states))]+=182*k
    assert np.array_equal(M,M.T)
    return M

def run():
    base=Path(__file__).resolve().parent
    shapes5=shapes(5)[5]
    bundle={};manifest={'k':5,'scale_int':400,'R_denominator':S,
        'matrix':'400*(W_B+91*k/200*I) restricted to total Sz=0',
        'numerical_solver_only_proposes_R':'numpy.linalg.cholesky',
        'independent_verifier':'verify_gram_k5.py','cases':[]}
    for caseid,(key,data) in enumerate(shapes5.items()):
        M=construct_integer_matrix(data['w'])
        L=np.linalg.cholesky(M.astype(float)-DELTA*np.eye(M.shape[0]))
        R=np.rint(S*L).astype(np.int64)
        assert np.array_equal(R,np.tril(R))
        # Exact integer Gershgorin check already in constructor; verifier repeats independently.
        E=S*S*M-R@R.T
        margin=np.min(np.diag(E)-(np.abs(E).sum(axis=1)-np.abs(np.diag(E))))
        assert margin>0,(caseid,key,margin)
        name=f'witness_{caseid:03d}'
        bundle[name]=R
        manifest['cases'].append({'index':caseid,'id':name,
            'weighted_graph_key':list(key),'representative':data['points'],
            'gershgorin_integer_margin':int(margin)})
        print('CONSTRUCT',caseid, 'PASS', 'size',len(M),'margin',int(margin),flush=True)
    np.savez_compressed(base/'K5_GRAM_WITNESSES.npz',**bundle)
    (base/'K5_GRAM_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('CONSTRUCTED',len(manifest['cases']),'Gram witnesses')
if __name__=='__main__':run()

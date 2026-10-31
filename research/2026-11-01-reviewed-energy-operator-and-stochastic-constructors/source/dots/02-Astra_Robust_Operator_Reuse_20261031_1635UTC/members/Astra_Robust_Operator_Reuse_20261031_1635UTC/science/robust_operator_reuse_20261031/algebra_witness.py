#!/usr/bin/env python3
"""Exact modular witness for full generated algebra on the mean-zero subspace."""
import json
from pathlib import Path
import numpy as np
import sympy as sp
from learn import fixture


def mod_matrix(A,p):
    return np.array([[int(A[i,j].p)%p*pow(int(A[i,j].q)%p,-1,p)%p
                      for j in range(A.cols)] for i in range(A.rows)],dtype=np.int64)


def witness(matrices,p=1000003):
    n=matrices[0].rows;d=n-1
    if type(p) is not int or not sp.isprime(p):raise ValueError('prime required')
    if d<1 or d*(p-1)**2>np.iinfo(np.int64).max:
        raise ValueError('outside exact int64 modular-product budget')
    T=sp.Matrix.vstack(sp.eye(d),-sp.ones(1,d))
    # Doubly-stochastic input preserves sum-zero; first d coordinates invert T.
    reduced=[]
    for A in matrices:
        R=(A*T)[:d,:]
        assert A*T==T*R
        reduced.append(mod_matrix(R,p))
    basis={};words=[];queue=[]
    def insert(M,w):
        x=M.reshape(-1).copy()%p
        for k,v in sorted(basis.items()):
            if x[k]:x=(x-int(x[k])*v)%p
        nz=np.flatnonzero(x)
        if not len(nz):return False
        k=int(nz[0]);basis[k]=x*pow(int(x[k]),-1,p)%p
        words.append(w);queue.append((M,w));return True
    insert(np.eye(d,dtype=np.int64),[])
    done=0
    while done<len(queue) and len(basis)<d*d:
        M,w=queue[done];done+=1
        for a,A in enumerate(reduced):insert(M@A%p,w+[a])
    return {'prime':p,'ambient_mean_zero_dimension':d,'rank':len(basis),
            'full':len(basis)==d*d,'word_witnesses':words,
            'max_word_length':max(map(len,words)),
            'scope':'Full modular rank proves full rational rank. Non-full search is not a general lower-rank proof.'}


if __name__=='__main__':
    result={}
    for label,noise in [('unperturbed',sp.Rational(0)),('perturbed',sp.Rational(1,10000))]:
        result[label]=witness(fixture(noise=noise)[0]);print(label,result[label]['rank'],flush=True)
    Path('algebra_witness.json').write_text(json.dumps(result,indent=2)+'\n')
